import time

import pytest

from parametric.spec.otel_trace import SK_PRODUCER
from parametric.spec.trace import SAMPLING_PRIORITY_KEY, ORIGIN
from parametric.utils.test_agent import get_span


@pytest.mark.skip_library("dotnet", "Not implemented")
@pytest.mark.skip_library("nodejs", "Not implemented")
@pytest.mark.skip_library("python", "Not implemented")
@pytest.mark.skip_library("java", "Not implemented")
def test_otel_start_span(test_agent, test_library):
    """
        - Start/end a span with start and end options
        - Start a tracer with options
    """
    test_library.otel_env = "otel_env"
    test_library.otel_service = "otel_serv"

    # entering test_otel_library starts the tracer with the above options
    with test_library:
        duration_s = int(2 * 1000000)
        start_time = int(time.time())
        with test_library.start_otel_span(
                "operation",
                span_kind=SK_PRODUCER,
                timestamp=start_time,
                new_root=True,
                attributes={"start_attr_key": "start_attr_val"},
        ) as parent:
            parent.finish(timestamp=start_time + duration_s)
    duration_ns = duration_s / (1e-9)

    root_span = get_span(test_agent)
    assert root_span["meta"]["env"] == "otel_env"
    assert root_span["service"] == "otel_serv"
    assert root_span["name"] == "operation"
    assert root_span["resource"] == "operation"
    assert root_span["meta"]["start_attr_key"] == "start_attr_val"
    assert root_span["duration"] == duration_ns


@pytest.mark.skip_library("dotnet", "Not implemented")
@pytest.mark.skip_library("nodejs", "Not implemented")
@pytest.mark.skip_library("python", "Not implemented")
@pytest.mark.skip_library("java", "Not implemented")
def test_otel_span_with_w3c_headers(test_agent, test_library):

    with test_library:
        with test_library.start_otel_span(
                name="name",
                http_headers=[["traceparent", "00-000000000000000000000000075bcd15-000000003ade68b1-01"]], ) as span:
            context = span.span_context()
            assert context.get("trace_flags") == '01'
            assert context.get("trace_id") == '00000000075bcd150000000000000000'

    span = get_span(test_agent)
    assert span.get("trace_id") == 123456789
    assert span.get("parent_id") == 987654321
    assert span["metrics"].get(SAMPLING_PRIORITY_KEY) == 1
    assert span["meta"].get(ORIGIN) is None
