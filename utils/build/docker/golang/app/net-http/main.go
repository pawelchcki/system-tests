package main

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"net/http/httptest"
	"os"
	"strconv"
	"time"
	"weblog/internal/common"
	"weblog/internal/grpc"

	"github.com/Shopify/sarama"
	saramatrace "gopkg.in/DataDog/dd-trace-go.v1/contrib/Shopify/sarama"
	"gopkg.in/DataDog/dd-trace-go.v1/datastreams"

	"go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/trace"
	oteltrace "go.opentelemetry.io/otel/trace"

	"gopkg.in/DataDog/dd-trace-go.v1/appsec"
	httptrace "gopkg.in/DataDog/dd-trace-go.v1/contrib/net/http"
	ddotel "gopkg.in/DataDog/dd-trace-go.v1/ddtrace/opentelemetry"
	"gopkg.in/DataDog/dd-trace-go.v1/ddtrace/tracer"
	ddtracer "gopkg.in/DataDog/dd-trace-go.v1/ddtrace/tracer"
)

func main() {
	ddtracer.Start()
	defer ddtracer.Stop()
	mux := httptrace.NewServeMux()

	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// "/" is the default route when the others don't match
		// cf. documentation at https://pkg.go.dev/net/http#ServeMux
		// Therefore, we need to check the URL path to only handle the `/` case
		if r.URL.Path != "/" {
			w.WriteHeader(http.StatusNotFound)
			return
		}
		w.WriteHeader(http.StatusOK)
	})

	mux.HandleFunc("/waf", func(w http.ResponseWriter, r *http.Request) {
		body, err := common.ParseBody(r)
		if err == nil {
			appsec.MonitorParsedHTTPBody(r.Context(), body)
		}
		w.Write([]byte("Hello, WAF!\n"))
	})

	mux.HandleFunc("/waf/", func(w http.ResponseWriter, r *http.Request) {
		body, err := common.ParseBody(r)
		if err == nil {
			appsec.MonitorParsedHTTPBody(r.Context(), body)
		}
		write(w, r, []byte("Hello, WAF!"))
	})

	mux.HandleFunc("/users", func(w http.ResponseWriter, r *http.Request) {
		userId := r.URL.Query().Get("user")
		if err := appsec.SetUser(r.Context(), userId); err != nil {
			return
		}
		w.Write([]byte("Hello, user!"))
	})

	mux.HandleFunc("/sample_rate_route/", func(w http.ResponseWriter, r *http.Request) {
		// net/http mux doesn't support advanced patterns, but the given prefix will match any /sample_rate_route/{i}
		w.Write([]byte("OK"))
	})

	mux.HandleFunc("/status", func(w http.ResponseWriter, r *http.Request) {
		if c := r.URL.Query().Get("code"); c != "" {
			if code, err := strconv.Atoi(c); err == nil {
				w.WriteHeader(code)
			}
		}
		w.Write([]byte("OK"))
	})

	mux.HandleFunc("/make_distant_call", func(w http.ResponseWriter, r *http.Request) {
		if url := r.URL.Query().Get("url"); url != "" {

			client := httptrace.WrapClient(http.DefaultClient)
			req, _ := http.NewRequestWithContext(r.Context(), http.MethodGet, url, nil)
			_, err := client.Do(req)

			if err != nil {
				log.Fatalln(err)
				w.WriteHeader(500)
			}
		}
		w.Write([]byte("OK"))
	})

	mux.HandleFunc("/headers", headers)
	mux.HandleFunc("/headers/", headers)

	identify := func(w http.ResponseWriter, r *http.Request) {
		if span, ok := ddtracer.SpanFromContext(r.Context()); ok {
			ddtracer.SetUser(
				span, "usr.id", ddtracer.WithUserEmail("usr.email"),
				ddtracer.WithUserName("usr.name"), ddtracer.WithUserSessionID("usr.session_id"),
				ddtracer.WithUserRole("usr.role"), ddtracer.WithUserScope("usr.scope"),
			)
		}
		w.Write([]byte("Hello, identify!"))
	}
	mux.HandleFunc("/identify/", identify)
	mux.HandleFunc("/identify", identify)
	mux.HandleFunc("/identify-propagate", func(w http.ResponseWriter, r *http.Request) {
		if span, ok := ddtracer.SpanFromContext(r.Context()); ok {
			ddtracer.SetUser(span, "usr.id", ddtracer.WithPropagation())
		}
		w.Write([]byte("Hello, identify-propagate!"))
	})

	mux.HandleFunc("/kafka/produce", func(w http.ResponseWriter, r *http.Request) {
		var message = "Test"

		topic := r.URL.Query().Get("topic")
		if len(topic) == 0 {
			w.Write([]byte("missing param 'topic'"))
			w.WriteHeader(422)
			return
		}

		_, _, err := kafkaProduce(topic, message)
		if err != nil {
			w.Write([]byte(err.Error()))
			w.WriteHeader(500)
			return
		}

		w.Write([]byte("OK"))
		w.WriteHeader(200)
	})

	mux.HandleFunc("/kafka/consume", func(w http.ResponseWriter, r *http.Request) {
		topic := r.URL.Query().Get("topic")
		if len(topic) == 0 {
			w.Write([]byte("missing param 'topic'"))
			w.WriteHeader(422)
			return
		}

		timeout, err := strconv.ParseInt(r.URL.Query().Get("timeout"), 10, 0)
		if err != nil {
			timeout = 20
		}

		message, status, err := kafkaConsume(topic, timeout)
		if err != nil {
			panic(err)
		}

		w.Write([]byte(message))
		w.WriteHeader(status)
	})

	mux.HandleFunc("/user_login_success_event", func(w http.ResponseWriter, r *http.Request) {
		uquery := r.URL.Query()
		uid := "system_tests_user"
		if q := uquery.Get("event_user_id"); q != "" {
			uid = q
		}
		appsec.TrackUserLoginSuccessEvent(r.Context(), uid, map[string]string{"metadata0": "value0", "metadata1": "value1"})
	})

	mux.HandleFunc("/user_login_failure_event", func(w http.ResponseWriter, r *http.Request) {
		uquery := r.URL.Query()
		uid := "system_tests_user"
		if q := uquery.Get("event_user_id"); q != "" {
			uid = q
		}
		exists := true
		if q := uquery.Get("event_user_exists"); q != "" {
			parsed, err := strconv.ParseBool(q)
			if err != nil {
				exists = parsed
			}
		}
		appsec.TrackUserLoginFailureEvent(r.Context(), uid, exists, map[string]string{"metadata0": "value0", "metadata1": "value1"})
	})

	mux.HandleFunc("/custom_event", func(w http.ResponseWriter, r *http.Request) {
		uquery := r.URL.Query()
		name := "system_tests_event"
		if q := uquery.Get("event_name"); q != "" {
			name = q
		}
		appsec.TrackCustomEvent(r.Context(), name, map[string]string{"metadata0": "value0", "metadata1": "value1"})
	})

	mux.HandleFunc("/e2e_otel_span", func(w http.ResponseWriter, r *http.Request) {
		parentName := r.URL.Query().Get("parentName")
		childName := r.URL.Query().Get("childName")

		tags := []attribute.KeyValue{}
		// We need to propagate the user agent header to retain the mapping between the system-tests/weblog request id
		// and the traces/spans that will be generated below, so that we can reference to them in our tests.
		// See https://github.com/DataDog/system-tests/blob/2d6ae4d5bf87d55855afd36abf36ee710e7d8b3c/utils/interfaces/_core.py#L156
		userAgent := r.UserAgent()
		tags = append(tags, attribute.String("http.useragent", userAgent))

		if r.URL.Query().Get("shouldIndex") == "1" {
			tags = append(tags,
				attribute.Int("_dd.filter.kept", 1),
				attribute.String("_dd.filter.id", "system_tests_e2e"),
			)
		}

		p := ddotel.NewTracerProvider()
		tracer := p.Tracer("")
		otel.SetTracerProvider(p)
		otel.SetTextMapPropagator(propagation.TraceContext{})
		defer p.ForceFlush(time.Second, func(ok bool) {})

		// Parent span will have the following traits :
		// - spanId of 10000
		// - tags {'attributes':'values'}
		// - tags necessary to retain the mapping between the system-tests/weblog request id and the traces/spans
		// - error tag with 'testing_end_span_options' message
		parentCtx, parentSpan := tracer.Start(ddotel.ContextWithStartOptions(context.Background(),
			ddtracer.WithSpanID(10000)), parentName,
			trace.WithAttributes(tags...))
		parentSpan.SetAttributes(attribute.String("attributes", "values"))
		ddotel.EndOptions(parentSpan, ddtracer.WithError(errors.New("testing_end_span_options")))

		// Child span will have the following traits :
		// - tags necessary to retain the mapping between the system-tests/weblog request id and the traces/spans
		// - duration of one second
		// - span kind of SpanKind - Internal
		start := time.Now()
		_, childSpan := tracer.Start(parentCtx, childName, trace.WithTimestamp(start), trace.WithAttributes(tags...), trace.WithSpanKind(trace.SpanKindInternal))
		childSpan.End(oteltrace.WithTimestamp(start.Add(time.Second)))
		parentSpan.End()

		w.Write([]byte("OK"))
	})

	mux.HandleFunc("/e2e_otel_span/mixed_contrib", func(w http.ResponseWriter, r *http.Request) {
		parentName := r.URL.Query().Get("parentName")

		tags := []attribute.KeyValue{}
		// We need to propagate the user agent header to retain the mapping between the system-tests/weblog request id
		// and the traces/spans that will be generated below, so that we can reference to them in our tests.
		// See https://github.com/DataDog/system-tests/blob/2d6ae4d5bf87d55855afd36abf36ee710e7d8b3c/utils/interfaces/_core.py#L156
		userAgent := r.UserAgent()
		tags = append(tags, attribute.String("http.useragent", userAgent))

		if r.URL.Query().Get("shouldIndex") == "1" {
			tags = append(tags,
				attribute.Int("_dd.filter.kept", 1),
				attribute.String("_dd.filter.id", "system_tests_e2e"),
			)
		}

		p := ddotel.NewTracerProvider()
		tracer := p.Tracer("")
		otel.SetTracerProvider(p)
		otel.SetTextMapPropagator(propagation.TraceContext{})
		defer p.ForceFlush(time.Second, func(ok bool) {})

		parentCtx, parentSpan := tracer.Start(context.Background(), parentName, trace.WithAttributes(tags...))

		h := otelhttp.NewHandler(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			receivedSpan := oteltrace.SpanFromContext(r.Context())
			// Need to propagate the user agent header to retain the mapping between
			// the system-tests/weblog request id and the traces/spans
			receivedSpan.SetAttributes(tags...)
			if receivedSpan.SpanContext().TraceID() != parentSpan.SpanContext().TraceID() {
				log.Fatalln("error in distributed tracing: Datadog OTel API and Otel net/http package span are not connected")
				w.WriteHeader(500)
				return
			}
		}), "testOperation")
		testServer := httptest.NewServer(h)
		defer testServer.Close()

		// Need to propagate the user agent header to retain the mapping between
		// the system-tests/weblog request id and the traces/spans
		c := http.Client{Transport: otelhttp.NewTransport(nil, otelhttp.WithSpanOptions(oteltrace.WithAttributes(tags...)))}
		req, err := http.NewRequestWithContext(parentCtx, http.MethodGet, testServer.URL, nil)
		if err != nil {
			log.Fatalln(err)
			w.WriteHeader(500)
			return
		}
		resp, err := c.Do(req)
		_ = resp.Body.Close() // Need to close body to cause otel span to end
		if err != nil {
			log.Fatalln(err)
			w.WriteHeader(500)
			return
		}
		parentSpan.End()

		w.Write([]byte("OK"))
	})

	mux.HandleFunc("/read_file", func(w http.ResponseWriter, r *http.Request) {
		path := r.URL.Query().Get("file")
		content, err := os.ReadFile(path)

		if err != nil {
			log.Fatalln(err)
			w.WriteHeader(500)
			return
		}
		w.Write([]byte(content))
	})

	mux.HandleFunc("/dsm", func(w http.ResponseWriter, r *http.Request) {
		var message = "Test DSM Context Propagation"

		integration := r.URL.Query().Get("integration")
		if len(integration) == 0 {
			w.WriteHeader(422)
			w.Write([]byte("missing param 'integration'"))
			return
		}

		if integration == "kafka" {
			queue := r.URL.Query().Get("queue")
			if len(queue) == 0 {
				w.WriteHeader(422)
				w.Write([]byte("missing param 'queue' for kafka dsm"))
				return
			}

			_, _, err := kafkaProduce(queue, message)
			if err != nil {
				w.WriteHeader(500)
				w.Write([]byte(err.Error()))
				return
			}

			timeout, err := strconv.ParseInt(r.URL.Query().Get("timeout"), 10, 0)
			if err != nil {
				timeout = 20
			}

			_, _, err = kafkaConsume(queue, timeout)
			if err != nil {
				w.WriteHeader(500)
				w.Write([]byte(err.Error()))
				return
			}
		}

		w.WriteHeader(200)
		w.Write([]byte("ok"))
	})

	mux.HandleFunc("/dsm/inject", func(w http.ResponseWriter, r *http.Request) {
		topic := r.URL.Query().Get("topic")
		if len(topic) == 0 {
			w.WriteHeader(422)
			w.Write([]byte("missing param 'topic'"))
			return
		}
		intType := r.URL.Query().Get("integration")
		if len(intType) == 0 {
			w.WriteHeader(422)
			w.Write([]byte("missing param 'integration'"))
			return
		}

		edges := []string{"direction:out", "topic:" + topic, "type:" + intType}
		carrier := make(carrier)
		ctx := context.Background()
		ctx, ok := tracer.SetDataStreamsCheckpoint(ctx, edges...)
		if !ok {
			w.WriteHeader(422)
			w.Write([]byte("failed to create DSM checkpoint"))
			return
		}
		datastreams.InjectToBase64Carrier(ctx, carrier)

		jsonData, err := json.Marshal(carrier)
		if err != nil {
			w.WriteHeader(422)
			w.Write([]byte("failed to convert carrier to JSON"))
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(200)
		w.Write(jsonData)
	})

	mux.HandleFunc("/dsm/extract", func(w http.ResponseWriter, r *http.Request) {
		topic := r.URL.Query().Get("topic")
		if len(topic) == 0 {
			w.WriteHeader(422)
			w.Write([]byte("missing param 'topic'"))
			return
		}
		intType := r.URL.Query().Get("integration")
		if len(intType) == 0 {
			w.WriteHeader(422)
			w.Write([]byte("missing param 'integration'"))
			return
		}
		rawCtx := r.URL.Query().Get("ctx")
		if len(rawCtx) == 0 {
			w.WriteHeader(422)
			w.Write([]byte("missing param 'ctx'"))
			return
		}
		carrier := make(carrier)
		err := json.Unmarshal([]byte(rawCtx), &carrier)
		if err != nil {
			w.WriteHeader(422)
			w.Write([]byte("failed to parse JSON"))
			return
		}

		edges := []string{"direction:in", "topic:" + topic, "type:" + intType}
		ctx := datastreams.ExtractFromBase64Carrier(context.Background(), carrier)
		_, ok := tracer.SetDataStreamsCheckpoint(ctx, edges...)
		if !ok {
			w.WriteHeader(422)
			w.Write([]byte("failed to create DSM checkpoint"))
			return
		}

		w.WriteHeader(200)
		w.Write([]byte("ok"))
	})

	common.InitDatadog()
	go grpc.ListenAndServe()
	http.ListenAndServe(":7777", mux)
}

type carrier map[string]string

func (c carrier) Set(key, val string) {
	c[key] = val
}

func (c carrier) ForeachKey(handler func(key, val string) error) error {
	for k, v := range c {
		if err := handler(k, v); err != nil {
			return err
		}
	}
	return nil
}

func write(w http.ResponseWriter, r *http.Request, d []byte) {
	span, _ := ddtracer.StartSpanFromContext(r.Context(), "child.span")
	defer span.Finish()
	w.Write(d)
}

func headers(w http.ResponseWriter, r *http.Request) {
	//Data used for header content is irrelevant here, only header presence is checked
	w.Header().Set("content-type", "text/plain")
	w.Header().Set("content-length", "42")
	w.Header().Set("content-language", "en-US")
	w.Write([]byte("Hello, headers!"))
}

func kafkaProduce(topic, message string) (int32, int64, error) {
	var server = "kafka:9092"

	cfg := sarama.NewConfig()
	cfg.Producer.Return.Successes = true

	producer, err := sarama.NewSyncProducer([]string{server}, cfg)
	if err != nil {
		return 0, 0, err
	}
	defer producer.Close()

	producer = saramatrace.WrapSyncProducer(cfg, producer, saramatrace.WithDataStreams())

	msg := &sarama.ProducerMessage{
		Topic:     topic,
		Partition: 0,
		Value:     sarama.StringEncoder(message),
	}

	partition, offset, err := producer.SendMessage(msg)
	if err != nil {
		return 0, 0, err
	}

	log.Printf("PRODUCER SENT MESSAGE TO (partition offset): %d %d", partition, offset)
	return partition, offset, nil
}

func kafkaConsume(topic string, timeout int64) (string, int, error) {
	var server = "kafka:9092"
	cfg := sarama.NewConfig()

	consumer, err := sarama.NewConsumer([]string{server}, cfg)
	if err != nil {
		return "", 0, err
	}
	defer consumer.Close()

	consumer = saramatrace.WrapConsumer(consumer, saramatrace.WithDataStreams())
	partitionConsumer, err := consumer.ConsumePartition(topic, 0, sarama.OffsetOldest)
	if err != nil {
		return "", 0, err
	}
	defer partitionConsumer.Close()

	timeOutTimer := time.NewTimer(time.Duration(timeout) * time.Second)
	defer timeOutTimer.Stop()
	log.Printf("CONSUMING MESSAGES from topic: %s", topic)
	for {
		select {
		case receivedMsg := <-partitionConsumer.Messages():
			responseOutput := fmt.Sprintf("Consumed message.\n\tOffset: %s\n\tMessage: %s\n", fmt.Sprint(receivedMsg.Offset), string(receivedMsg.Value))
			log.Print(responseOutput)
			return responseOutput, 200, nil
		case <-timeOutTimer.C:
			timedOutMessage := "TimeOut"
			log.Print(timedOutMessage)
			return timedOutMessage, 408, nil
		}
	}
}
