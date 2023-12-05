import pytest
from utils.parametric.spec.trace import Span
from utils.parametric.spec.trace import find_span_in_traces
import json
from utils import rfc, scenarios
from utils.parametric.spec.trace import SAMPLING_PRIORITY_KEY, SAMPLING_RULE_PRIORITY_RATE


@scenarios.parametric
@rfc("https://docs.google.com/document/d/1HRbi1DrBjL_KGeONrPgH7lblgqSLGlV5Ox1p4RL97xM/")
class Test_Trace_Sampling_Basic:
    @pytest.mark.parametrize(
        "library_env",
        [
            {
                "DD_TRACE_SAMPLE_RATE": 0,
                "DD_TRACE_SAMPLING_RULES": json.dumps(
                    [
                        {"service": "webserver.non-matching", "sample_rate": 0},
                        {"service": "webserver", "sample_rate": 1},
                    ]
                ),
            },
            {
                "DD_TRACE_SAMPLE_RATE": 0,
                "DD_TRACE_SAMPLING_RULES": json.dumps(
                    [{"name": "web.request.non-matching", "sample_rate": 0}, {"name": "web.request", "sample_rate": 1}]
                ),
            },
            {
                "DD_TRACE_SAMPLE_RATE": 0,
                "DD_TRACE_SAMPLING_RULES": json.dumps(
                    [
                        {"service": "webserver.non-matching", "name": "web.request", "sample_rate": 0},
                        {"service": "webserver", "name": "web.request.non-matching", "sample_rate": 0},
                        {"service": "webserver", "name": "web.request", "sample_rate": 1},
                    ]
                ),
            },
        ],
    )
    def test_trace_sampled_by_trace_sampling_rule_exact_match(self, test_agent, test_library):
        """Test that a trace is sampled by the exact matching trace sampling rule"""
        with test_library:
            with test_library.start_span(name="web.request", service="webserver"):
                pass
        span = find_span_in_traces(test_agent.wait_for_num_traces(1), Span(name="web.request", service="webserver"))

        assert span["metrics"].get(SAMPLING_PRIORITY_KEY) == 2
        assert span["metrics"].get(SAMPLING_RULE_PRIORITY_RATE) == 1.0

    @pytest.mark.parametrize(
        "library_env",
        [
            {
                "DD_TRACE_SAMPLE_RATE": 1,
                "DD_TRACE_SAMPLING_RULES": json.dumps(
                    [{"service": "webserver", "name": "web.request", "sample_rate": 0}]
                ),
            }
        ],
    )
    def test_trace_dropped_by_trace_sampling_rule(self, test_agent, test_library):
        """Test that a trace is dropped by the matching defined trace sampling rule"""
        with test_library:
            with test_library.start_span(name="web.request", service="webserver"):
                pass
        span = find_span_in_traces(test_agent.wait_for_num_traces(1), Span(name="web.request", service="webserver"))

        assert span["metrics"].get(SAMPLING_PRIORITY_KEY) == -1
        assert span["metrics"].get(SAMPLING_RULE_PRIORITY_RATE) == 0.0


@scenarios.parametric
@rfc("https://docs.google.com/document/d/1S9pufnJjrsxH6pRbpigdYFwA5JjSdZ6iLZ-9E7PoAic/")
class Test_Trace_Sampling_Globs:
    @pytest.mark.parametrize(
        "library_env",
        [
            {
                "DD_TRACE_SAMPLE_RATE": 0,
                "DD_TRACE_SAMPLING_RULES": json.dumps(
                    [{"service": "web.non-matching*", "sample_rate": 0}, {"service": "web*", "sample_rate": 1},]
                ),
            },
            {
                "DD_TRACE_SAMPLE_RATE": 0,
                "DD_TRACE_SAMPLING_RULES": json.dumps(
                    [{"name": "web.non-matching*", "sample_rate": 0}, {"name": "web.*", "sample_rate": 1}]
                ),
            },
            {
                "DD_TRACE_SAMPLE_RATE": 0,
                "DD_TRACE_SAMPLING_RULES": json.dumps(
                    [
                        {"service": "webserv?r.non-matching", "name": "web.req*", "sample_rate": 0},
                        {"service": "webserv?r", "name": "web.req*.non-matching", "sample_rate": 0},
                        {"service": "webserv?r", "name": "web.req*", "sample_rate": 1},
                    ]
                ),
            },
        ],
    )
    def test_trace_sampled_by_trace_sampling_rule_glob_match(self, test_agent, test_library):
        """Test that a trace is sampled by the glob matching trace sampling rule"""
        with test_library:
            with test_library.start_span(name="web.request", service="webserver"):
                pass
        span = find_span_in_traces(test_agent.wait_for_num_traces(1), Span(name="web.request", service="webserver"))

        assert span["metrics"].get(SAMPLING_PRIORITY_KEY) == 2
        assert span["metrics"].get(SAMPLING_RULE_PRIORITY_RATE) == 1.0

    @pytest.mark.parametrize(
        "library_env",
        [
            {
                "DD_TRACE_SAMPLE_RATE": 1,
                "DD_TRACE_SAMPLING_RULES": json.dumps([{"service": "w?bs?rv?r", "name": "web.*", "sample_rate": 0}]),
            }
        ],
    )
    def test_trace_dropped_by_trace_sampling_rule(self, test_agent, test_library):
        """Test that a trace is dropped by the matching defined trace sampling rule"""
        with test_library:
            with test_library.start_span(name="web.request", service="webserver"):
                pass
        span = find_span_in_traces(test_agent.wait_for_num_traces(1), Span(name="web.request", service="webserver"))

        assert span["metrics"].get(SAMPLING_PRIORITY_KEY) == -1
        assert span["metrics"].get(SAMPLING_RULE_PRIORITY_RATE) == 0.0


@scenarios.parametric
@rfc("https://docs.google.com/document/d/1S9pufnJjrsxH6pRbpigdYFwA5JjSdZ6iLZ-9E7PoAic/")
class Test_Trace_Sampling_Resource:
    @pytest.mark.parametrize(
        "library_env",
        [
            {
                "DD_TRACE_SAMPLE_RATE": 0,
                "DD_TRACE_SAMPLING_RULES": json.dumps(
                    [{"resource": "/bar.non-matching", "sample_rate": 0}, {"resource": "/?ar", "sample_rate": 1},]
                ),
            },
            {
                "DD_TRACE_SAMPLE_RATE": 0,
                "DD_TRACE_SAMPLING_RULES": json.dumps(
                    [
                        {"name": "web.request.non-matching", "resource": "/bar", "sample_rate": 0},
                        {"name": "web.request", "resource": "/bar.non-matching", "sample_rate": 0},
                        {"name": "web.request", "resource": "/b*", "sample_rate": 1},
                    ]
                ),
            },
            {
                "DD_TRACE_SAMPLE_RATE": 0,
                "DD_TRACE_SAMPLING_RULES": json.dumps(
                    [
                        {"service": "webserver.non-matching", "resource": "/bar", "sample_rate": 0},
                        {"service": "webserver", "resource": "/bar.non-matching", "sample_rate": 0},
                        {"service": "webserver", "resource": "/bar", "sample_rate": 1},
                    ]
                ),
            },
            {
                "DD_TRACE_SAMPLE_RATE": 0,
                "DD_TRACE_SAMPLING_RULES": json.dumps(
                    [
                        {
                            "service": "webserver.non-matching",
                            "name": "web.request",
                            "resource": "/bar",
                            "sample_rate": 0,
                        },
                        {
                            "service": "webserver",
                            "name": "web.request.non-matching",
                            "resource": "/bar",
                            "sample_rate": 0,
                        },
                        {
                            "service": "webserver",
                            "name": "web.request",
                            "resource": "/bar.non-matching",
                            "sample_rate": 0,
                        },
                        {"service": "webserver", "name": "web.request", "resource": "/b?r", "sample_rate": 1},
                    ]
                ),
            },
        ],
    )
    def test_trace_sampled_by_trace_sampling_rule_exact_match(self, test_agent, test_library):
        """Test that a trace is sampled by the exact matching trace sampling rule"""
        with test_library:
            with test_library.start_span(name="web.request", service="webserver", resource="/bar"):
                pass
        span = find_span_in_traces(
            test_agent.wait_for_num_traces(1), Span(name="web.request", service="webserver", resource="/bar")
        )

        assert span["metrics"].get(SAMPLING_PRIORITY_KEY) == 2
        assert span["metrics"].get(SAMPLING_RULE_PRIORITY_RATE) == 1.0

    @pytest.mark.parametrize(
        "library_env",
        [
            {
                "DD_TRACE_SAMPLE_RATE": 1,
                "DD_TRACE_SAMPLING_RULES": json.dumps(
                    [
                        {"service": "non-matching", "sample_rate": 1},
                        {"name": "non-matching", "sample_rate": 1},
                        {"resource": "non-matching", "sample_rate": 1},
                        {"service": "webserver", "name": "web.request", "resource": "/bar", "sample_rate": 0},
                    ]
                ),
            }
        ],
    )
    def test_trace_dropped_by_trace_sampling_rule(self, test_agent, test_library):
        """Test that a trace is dropped by the matching trace sampling rule"""
        with test_library:
            with test_library.start_span(name="web.request", service="webserver", resource="/bar"):
                pass
        span = find_span_in_traces(
            test_agent.wait_for_num_traces(1), Span(name="web.request", service="webserver", resource="/bar")
        )

        assert span["metrics"].get(SAMPLING_PRIORITY_KEY) == -1
        assert span["metrics"].get(SAMPLING_RULE_PRIORITY_RATE) == 0.0


@scenarios.parametric
@rfc("https://docs.google.com/document/d/1S9pufnJjrsxH6pRbpigdYFwA5JjSdZ6iLZ-9E7PoAic/")
class Test_Trace_Sampling_Tags:
    @pytest.mark.parametrize(
        "library_env",
        [
            {
                "DD_TRACE_SAMPLE_RATE": 0,
                "DD_TRACE_SAMPLING_RULES": json.dumps(
                    [{"tags": {"tag1": "non-matching"}, "sample_rate": 0}, {"tags": {"tag1": "val1"}, "sample_rate": 1}]
                ),
            },
            {
                "DD_TRACE_SAMPLE_RATE": 0,
                "DD_TRACE_SAMPLING_RULES": json.dumps(
                    [
                        {"tags": {"tag1": "non-matching"}, "sample_rate": 0},
                        {"tags": {"tag2": "non-matching"}, "sample_rate": 0},
                        {"tags": {"tag1": "non-matching", "tag2": "val2"}, "sample_rate": 0},
                        {"tags": {"tag1": "val1", "tag2": "non-matching"}, "sample_rate": 0},
                        {"tags": {"tag1": "val1", "tag2": "val2"}, "sample_rate": 1},
                    ]
                ),
            },
            {
                "DD_TRACE_SAMPLE_RATE": 0,
                "DD_TRACE_SAMPLING_RULES": json.dumps(
                    [{"tags": {"tag1": "v?r*"}, "sample_rate": 0}, {"tags": {"tag1": "val?"}, "sample_rate": 1}]
                ),
            },
            {
                "DD_TRACE_SAMPLE_RATE": 0,
                "DD_TRACE_SAMPLING_RULES": json.dumps(
                    [
                        {"service": "webs?rver.non-matching", "sample_rate": 0},
                        {"name": "web.request.non-matching", "sample_rate": 0},
                        {"resource": "/ba*.non-matching", "sample_rate": 0},
                        {"tags": {"tag1": "v?l1", "tag2": "va*.non-matching"}, "sample_rate": 0},
                        {
                            "service": "webs?rver",
                            "name": "web.request",
                            "resource": "/ba*",
                            "tags": {"tag1": "v?l1", "tag2": "val*"},
                            "sample_rate": 1,
                        },
                    ]
                ),
            },
        ],
    )
    def test_trace_sampled_by_trace_sampling_rule_tags(self, test_agent, test_library):
        """Test that a trace is sampled by the matching trace sampling rule"""
        with test_library:
            with test_library.start_span(name="web.request", service="webserver", resource="/bar") as span:
                span.set_meta("tag1", "val1")
                span.set_meta("tag2", "val2")
        span = find_span_in_traces(
            test_agent.wait_for_num_traces(1), Span(name="web.request", service="webserver", resource="/bar")
        )

        assert span["metrics"].get(SAMPLING_PRIORITY_KEY) == 2
        assert span["metrics"].get(SAMPLING_RULE_PRIORITY_RATE) == 1.0

    @pytest.mark.parametrize(
        "library_env",
        [
            {
                "DD_TRACE_SAMPLE_RATE": 1,
                "DD_TRACE_SAMPLING_RULES": json.dumps(
                    [
                        {"tags": {"tag1": "v?l1", "tag2": "non-matching"}, "sample_rate": 1},
                        {"tags": {"tag1": "v?l1", "tag2": "val*"}, "sample_rate": 0},
                    ]
                ),
            },
        ],
    )
    def test_trace_dropped_by_trace_sampling_rule_tags(self, test_agent, test_library):
        """Test that a trace is dropped by the matching trace sampling rule"""
        with test_library:
            with test_library.start_span(name="web.request", service="webserver", resource="/bar") as span:
                span.set_meta("tag1", "val1")
                span.set_meta("tag2", "val2")
        span = find_span_in_traces(
            test_agent.wait_for_num_traces(1), Span(name="web.request", service="webserver", resource="/bar")
        )

        assert span["metrics"].get(SAMPLING_PRIORITY_KEY) == -1
        assert span["metrics"].get(SAMPLING_RULE_PRIORITY_RATE) == 0.0