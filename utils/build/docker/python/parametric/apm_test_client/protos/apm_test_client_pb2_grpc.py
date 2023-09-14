# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from apm_test_client.protos import apm_test_client_pb2 as parametric_dot_protos_dot_apm__test__client__pb2


class APMClientStub(object):
    """Interface of APM clients to be used for shared testing.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StartSpan = channel.unary_unary(
            "/APMClient/StartSpan",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.StartSpanArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.StartSpanReturn.FromString,
        )
        self.FinishSpan = channel.unary_unary(
            "/APMClient/FinishSpan",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.FinishSpanArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.FinishSpanReturn.FromString,
        )
        self.SpanSetMeta = channel.unary_unary(
            "/APMClient/SpanSetMeta",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.SpanSetMetaArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.SpanSetMetaReturn.FromString,
        )
        self.SpanSetMetric = channel.unary_unary(
            "/APMClient/SpanSetMetric",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.SpanSetMetricArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.SpanSetMetricReturn.FromString,
        )
        self.SpanSetError = channel.unary_unary(
            "/APMClient/SpanSetError",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.SpanSetErrorArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.SpanSetErrorReturn.FromString,
        )
        self.HTTPClientRequest = channel.unary_unary(
            "/APMClient/HTTPClientRequest",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.HTTPRequestArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.HTTPRequestReturn.FromString,
        )
        self.HTTPServerRequest = channel.unary_unary(
            "/APMClient/HTTPServerRequest",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.HTTPRequestArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.HTTPRequestReturn.FromString,
        )
        self.InjectHeaders = channel.unary_unary(
            "/APMClient/InjectHeaders",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.InjectHeadersArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.InjectHeadersReturn.FromString,
        )
        self.FlushSpans = channel.unary_unary(
            "/APMClient/FlushSpans",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.FlushSpansArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.FlushSpansReturn.FromString,
        )
        self.FlushTraceStats = channel.unary_unary(
            "/APMClient/FlushTraceStats",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.FlushTraceStatsArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.FlushTraceStatsReturn.FromString,
        )
        self.OtelStartSpan = channel.unary_unary(
            "/APMClient/OtelStartSpan",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelStartSpanArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelStartSpanReturn.FromString,
        )
        self.OtelEndSpan = channel.unary_unary(
            "/APMClient/OtelEndSpan",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelEndSpanArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelEndSpanReturn.FromString,
        )
        self.OtelIsRecording = channel.unary_unary(
            "/APMClient/OtelIsRecording",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelIsRecordingArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelIsRecordingReturn.FromString,
        )
        self.OtelSpanContext = channel.unary_unary(
            "/APMClient/OtelSpanContext",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelSpanContextArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelSpanContextReturn.FromString,
        )
        self.OtelSetStatus = channel.unary_unary(
            "/APMClient/OtelSetStatus",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelSetStatusArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelSetStatusReturn.FromString,
        )
        self.OtelSetName = channel.unary_unary(
            "/APMClient/OtelSetName",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelSetNameArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelSetNameReturn.FromString,
        )
        self.OtelSetAttributes = channel.unary_unary(
            "/APMClient/OtelSetAttributes",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelSetAttributesArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelSetAttributesReturn.FromString,
        )
        self.OtelFlushSpans = channel.unary_unary(
            "/APMClient/OtelFlushSpans",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelFlushSpansArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelFlushSpansReturn.FromString,
        )
        self.OtelFlushTraceStats = channel.unary_unary(
            "/APMClient/OtelFlushTraceStats",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelFlushTraceStatsArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelFlushTraceStatsReturn.FromString,
        )
        self.StopTracer = channel.unary_unary(
            "/APMClient/StopTracer",
            request_serializer=parametric_dot_protos_dot_apm__test__client__pb2.StopTracerArgs.SerializeToString,
            response_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.StopTracerReturn.FromString,
        )


class APMClientServicer(object):
    """Interface of APM clients to be used for shared testing.
    """

    def StartSpan(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def FinishSpan(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def SpanSetMeta(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def SpanSetMetric(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def SpanSetError(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def HTTPClientRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def HTTPServerRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def InjectHeaders(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def FlushSpans(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def FlushTraceStats(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OtelStartSpan(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OtelEndSpan(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OtelIsRecording(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OtelSpanContext(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OtelSetStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OtelSetName(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OtelSetAttributes(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OtelFlushSpans(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OtelFlushTraceStats(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def StopTracer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_APMClientServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "StartSpan": grpc.unary_unary_rpc_method_handler(
            servicer.StartSpan,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.StartSpanArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.StartSpanReturn.SerializeToString,
        ),
        "FinishSpan": grpc.unary_unary_rpc_method_handler(
            servicer.FinishSpan,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.FinishSpanArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.FinishSpanReturn.SerializeToString,
        ),
        "SpanSetMeta": grpc.unary_unary_rpc_method_handler(
            servicer.SpanSetMeta,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.SpanSetMetaArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.SpanSetMetaReturn.SerializeToString,
        ),
        "SpanSetMetric": grpc.unary_unary_rpc_method_handler(
            servicer.SpanSetMetric,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.SpanSetMetricArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.SpanSetMetricReturn.SerializeToString,
        ),
        "SpanSetError": grpc.unary_unary_rpc_method_handler(
            servicer.SpanSetError,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.SpanSetErrorArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.SpanSetErrorReturn.SerializeToString,
        ),
        "HTTPClientRequest": grpc.unary_unary_rpc_method_handler(
            servicer.HTTPClientRequest,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.HTTPRequestArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.HTTPRequestReturn.SerializeToString,
        ),
        "HTTPServerRequest": grpc.unary_unary_rpc_method_handler(
            servicer.HTTPServerRequest,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.HTTPRequestArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.HTTPRequestReturn.SerializeToString,
        ),
        "InjectHeaders": grpc.unary_unary_rpc_method_handler(
            servicer.InjectHeaders,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.InjectHeadersArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.InjectHeadersReturn.SerializeToString,
        ),
        "FlushSpans": grpc.unary_unary_rpc_method_handler(
            servicer.FlushSpans,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.FlushSpansArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.FlushSpansReturn.SerializeToString,
        ),
        "FlushTraceStats": grpc.unary_unary_rpc_method_handler(
            servicer.FlushTraceStats,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.FlushTraceStatsArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.FlushTraceStatsReturn.SerializeToString,
        ),
        "OtelStartSpan": grpc.unary_unary_rpc_method_handler(
            servicer.OtelStartSpan,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelStartSpanArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelStartSpanReturn.SerializeToString,
        ),
        "OtelEndSpan": grpc.unary_unary_rpc_method_handler(
            servicer.OtelEndSpan,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelEndSpanArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelEndSpanReturn.SerializeToString,
        ),
        "OtelIsRecording": grpc.unary_unary_rpc_method_handler(
            servicer.OtelIsRecording,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelIsRecordingArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelIsRecordingReturn.SerializeToString,
        ),
        "OtelSpanContext": grpc.unary_unary_rpc_method_handler(
            servicer.OtelSpanContext,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelSpanContextArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelSpanContextReturn.SerializeToString,
        ),
        "OtelSetStatus": grpc.unary_unary_rpc_method_handler(
            servicer.OtelSetStatus,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelSetStatusArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelSetStatusReturn.SerializeToString,
        ),
        "OtelSetName": grpc.unary_unary_rpc_method_handler(
            servicer.OtelSetName,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelSetNameArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelSetNameReturn.SerializeToString,
        ),
        "OtelSetAttributes": grpc.unary_unary_rpc_method_handler(
            servicer.OtelSetAttributes,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelSetAttributesArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelSetAttributesReturn.SerializeToString,
        ),
        "OtelFlushSpans": grpc.unary_unary_rpc_method_handler(
            servicer.OtelFlushSpans,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelFlushSpansArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelFlushSpansReturn.SerializeToString,
        ),
        "OtelFlushTraceStats": grpc.unary_unary_rpc_method_handler(
            servicer.OtelFlushTraceStats,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelFlushTraceStatsArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.OtelFlushTraceStatsReturn.SerializeToString,
        ),
        "StopTracer": grpc.unary_unary_rpc_method_handler(
            servicer.StopTracer,
            request_deserializer=parametric_dot_protos_dot_apm__test__client__pb2.StopTracerArgs.FromString,
            response_serializer=parametric_dot_protos_dot_apm__test__client__pb2.StopTracerReturn.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler("APMClient", rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class APMClient(object):
    """Interface of APM clients to be used for shared testing.
    """

    @staticmethod
    def StartSpan(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/StartSpan",
            parametric_dot_protos_dot_apm__test__client__pb2.StartSpanArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.StartSpanReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def FinishSpan(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/FinishSpan",
            parametric_dot_protos_dot_apm__test__client__pb2.FinishSpanArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.FinishSpanReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def SpanSetMeta(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/SpanSetMeta",
            parametric_dot_protos_dot_apm__test__client__pb2.SpanSetMetaArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.SpanSetMetaReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def SpanSetMetric(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/SpanSetMetric",
            parametric_dot_protos_dot_apm__test__client__pb2.SpanSetMetricArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.SpanSetMetricReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def SpanSetError(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/SpanSetError",
            parametric_dot_protos_dot_apm__test__client__pb2.SpanSetErrorArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.SpanSetErrorReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def HTTPClientRequest(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/HTTPClientRequest",
            parametric_dot_protos_dot_apm__test__client__pb2.HTTPRequestArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.HTTPRequestReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def HTTPServerRequest(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/HTTPServerRequest",
            parametric_dot_protos_dot_apm__test__client__pb2.HTTPRequestArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.HTTPRequestReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def InjectHeaders(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/InjectHeaders",
            parametric_dot_protos_dot_apm__test__client__pb2.InjectHeadersArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.InjectHeadersReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def FlushSpans(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/FlushSpans",
            parametric_dot_protos_dot_apm__test__client__pb2.FlushSpansArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.FlushSpansReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def FlushTraceStats(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/FlushTraceStats",
            parametric_dot_protos_dot_apm__test__client__pb2.FlushTraceStatsArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.FlushTraceStatsReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OtelStartSpan(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/OtelStartSpan",
            parametric_dot_protos_dot_apm__test__client__pb2.OtelStartSpanArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.OtelStartSpanReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OtelEndSpan(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/OtelEndSpan",
            parametric_dot_protos_dot_apm__test__client__pb2.OtelEndSpanArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.OtelEndSpanReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OtelIsRecording(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/OtelIsRecording",
            parametric_dot_protos_dot_apm__test__client__pb2.OtelIsRecordingArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.OtelIsRecordingReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OtelSpanContext(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/OtelSpanContext",
            parametric_dot_protos_dot_apm__test__client__pb2.OtelSpanContextArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.OtelSpanContextReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OtelSetStatus(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/OtelSetStatus",
            parametric_dot_protos_dot_apm__test__client__pb2.OtelSetStatusArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.OtelSetStatusReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OtelSetName(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/OtelSetName",
            parametric_dot_protos_dot_apm__test__client__pb2.OtelSetNameArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.OtelSetNameReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OtelSetAttributes(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/OtelSetAttributes",
            parametric_dot_protos_dot_apm__test__client__pb2.OtelSetAttributesArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.OtelSetAttributesReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OtelFlushSpans(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/OtelFlushSpans",
            parametric_dot_protos_dot_apm__test__client__pb2.OtelFlushSpansArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.OtelFlushSpansReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OtelFlushTraceStats(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/OtelFlushTraceStats",
            parametric_dot_protos_dot_apm__test__client__pb2.OtelFlushTraceStatsArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.OtelFlushTraceStatsReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def StopTracer(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/APMClient/StopTracer",
            parametric_dot_protos_dot_apm__test__client__pb2.StopTracerArgs.SerializeToString,
            parametric_dot_protos_dot_apm__test__client__pb2.StopTracerReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
