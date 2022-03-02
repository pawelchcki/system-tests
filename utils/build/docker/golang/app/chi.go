package main

import (
	"net/http"

	"github.com/go-chi/chi/v5"

	chitrace "gopkg.in/DataDog/dd-trace-go.v1/contrib/go-chi/chi.v5"
	"gopkg.in/DataDog/dd-trace-go.v1/ddtrace/tracer"
)

func main() {
	tracer.Start()
	defer tracer.Stop()

	mux := chi.NewRouter().With(chitrace.Middleware())

	mux.HandleFunc("/waf/*", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Hello, WAF!\n"))
	})

	mux.HandleFunc("/sample_rate_route/:i", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("OK"))
	})

	mux.HandleFunc("/params/{myParam}", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("OK"))
	})

	mux.HandleFunc("/headers/", func(w http.ResponseWriter, r *http.Request) {
		//Data used for header content is irrelevant here, only header presence is checked
		w.Header().Set("Content-Type", "text/plain")
		w.Header().Set("Content-Length", "42")
		w.Header().Set("Content-Language", "en-US")
		w.Write([]byte("Hello, headers!"))
	})

	mux.HandleFunc("/*", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
	})

	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	})

	initDatadog()
	http.ListenAndServe(":7777", mux)
}