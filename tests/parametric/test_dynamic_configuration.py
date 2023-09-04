"""
Test the dynamic configuration via Remote Config (RC) feature of the APM libraries.

TODO:
 - test case for new version of config, ensure it doesn't break libraries
 - test no config change = no telemetry event
"""
import json
from typing import Any
from typing import Dict
from typing import List

from utils.parametric.spec.trace import Span
from utils import context, missing_feature, released, rfc, scenarios

import pytest


parametrize = pytest.mark.parametrize


DEFAULT_SAMPLE_RATE = 1.0
TEST_SERVICE = "test_service"
TEST_ENV = "test_env"
DEFAULT_ENVVARS = {
    "DD_SERVICE": TEST_SERVICE,
    "DD_ENV": TEST_ENV,
    # Needed for .NET until Telemetry V2 is released
    "DD_INTERNAL_TELEMETRY_V2_ENABLED": "1",
    # Decrease the heartbeat/poll intervals to speed up the tests
    "DD_TELEMETRY_HEARTBEAT_INTERVAL": "0.2",
    "DD_REMOTE_CONFIG_POLL_INTERVAL_SECONDS": "0.2",
}


def send_and_wait_trace(test_library, test_agent, **span_kwargs) -> List[Span]:
    with test_library.start_span(**span_kwargs):
        pass
    traces = test_agent.wait_for_num_traces(num=1, clear=True)
    assert len(traces) == 1
    return traces[0]


def _default_config(service: str, env: str) -> Dict[str, Any]:
    return {
        "action": "enable",
        "service_target": {"service": service, "env": env},
        "lib_config": {
            # v1 dynamic config
            "tracing_sampling_rate": None,
            "log_injection_enabled": None,
            "tracing_header_tags": None,
            # v2 dynamic config
            "runtime_metrics_enabled": None,
            "tracing_debug": None,
            "tracing_service_mapping": None,
            "tracing_sampling_rules": None,
            "span_sampling_rules": None,
            "data_streams_enabled": None,
        },
    }


def _set_rc(test_agent, config: Dict[str, Any]) -> None:
    cfg_id = hash(json.dumps(config))
    test_agent.set_remote_config(
        path="datadog/2/APM_TRACING/%s/config" % cfg_id, payload=config,
    )


def set_and_wait_rc(test_agent, config_overrides: Dict[str, Any]) -> Dict:
    """Helper to create an RC configuration with the given settings and wait for it to be applied.

    It is assumed that the configuration is successfully applied.
    """
    rc_config = _default_config(TEST_SERVICE, TEST_ENV)
    for k, v in config_overrides.items():
        rc_config["lib_config"][k] = v

    _set_rc(test_agent, rc_config)

    # Wait for both the telemetry event and the RC apply status.
    test_agent.wait_for_telemetry_event("app-client-configuration-change", clear=True)
    return test_agent.wait_for_rc_apply_state("APM_TRACING", state=2, clear=True)


def assert_sampling_rate(trace: List[Dict], rate: float):
    """Asserts that a trace returned from the test agent is consistent with the given sample rate.

    This function assumes that all traces are sent to the agent regardless of sample rate.

    For the day when that is not the case, we likely need to generate enough traces to
        1) Validate the sample rate is effective (approx sample_rate% of traces should be received)
        2) The `_dd.rule_psr` metric is set to the correct value.
    """
    # This tag should be set on the first span in a chunk (first span in the list of spans sent to the agent).
    assert trace[0]["metrics"].get("_dd.rule_psr", 1.0) == pytest.approx(rate)


ENV_SAMPLING_RULE_RATE = 0.55


@released(
    java="1.17.0",
    dotnet="2.33.0",
    ruby="1.13.0",
    nodejs="4.11.0",  # also in 3.32.0 and 2.45.0
    python="?",
    golang="?",
    php="?",
    cpp="?",
)
@rfc("https://docs.google.com/document/d/1SVD0zbbAAXIsobbvvfAEXipEUO99R9RMsosftfe9jx0")
@scenarios.parametric
class TestDynamicConfigV1:
    """Tests covering the v1 release of the dynamic configuration feature.

    v1 includes support for:
        - tracing_sampling_rate
        - log_injection_enabled
        - tracing_header_tags
    """

    @parametrize("library_env", [{"DD_TELEMETRY_HEARTBEAT_INTERVAL": "0.1"}])
    def test_telemetry_app_started(self, library_env, test_agent, test_library):
        """Ensure that the app-started telemetry event is being submitted.

        Telemetry events are used as a signal for the configuration being applied
        by the library.
        """
        # Python doesn't start writing telemetry until the first trace.
        with test_library.start_span("test"):
            pass
        events = test_agent.wait_for_telemetry_event("app-started")
        assert len(events) > 0

    @parametrize("library_env", [{**DEFAULT_ENVVARS}])
    def test_apply_state(self, library_env, test_agent, test_library):
        """Create a default RC record and ensure the apply_state is correctly set.

        This signal, along with the telemetry event, is used to determine when the
        configuration has been applied by the tracer.
        """
        set_and_wait_rc(test_agent, {})
        cfg_state = test_agent.wait_for_rc_apply_state("APM_TRACING", state=2)
        assert cfg_state["apply_state"] == 2
        assert cfg_state["product"] == "APM_TRACING"

    @missing_feature(context.library in ["java", "dotnet", "ruby", "nodejs"], reason="Not implemented yet")
    @parametrize(
        "library_env",
        [
            {
                **DEFAULT_ENVVARS,
                # Override service and env
                "DD_SERVICE": s,
                "DD_ENV": e,
            }
            for (s, e) in [
                (DEFAULT_ENVVARS["DD_SERVICE"] + "-override", DEFAULT_ENVVARS["DD_ENV"]),
                (DEFAULT_ENVVARS["DD_SERVICE"], DEFAULT_ENVVARS["DD_ENV"] + "-override"),
                (DEFAULT_ENVVARS["DD_SERVICE"] + "-override", DEFAULT_ENVVARS["DD_ENV"] + "-override"),
            ]
        ],
    )
    def test_not_match_service_target(self, library_env, test_agent, test_library):
        """Test that the library reports an erroneous apply_state when the service targeting is not correct.

        This can occur if the library requests Remote Configuration with an initial service + env pair and then
        one or both of the values changes.

        We simulate this condition by setting DD_SERVICE and DD_ENV to values that differ from the service
        target in the RC record.
        """
        _set_rc(test_agent, _default_config(TEST_SERVICE, TEST_ENV))
        cfg_state = test_agent.wait_for_rc_apply_state("APM_TRACING", state=3)
        assert cfg_state["apply_state"] == 3
        assert cfg_state["apply_error"] != ""

    @parametrize("library_env", [{**DEFAULT_ENVVARS}])
    def test_trace_sampling_rate_override_default(self, test_agent, test_library):
        """The RC sampling rate should override the default sampling rate.

        When RC is unset, the default should be used again.
        """
        # Create an initial trace to assert the default sampling settings.
        trace = send_and_wait_trace(test_library, test_agent, name="test")
        assert_sampling_rate(trace, DEFAULT_SAMPLE_RATE)

        # Create a remote config entry, wait for the configuration change telemetry event to be received
        # and then create a new trace to assert the configuration has been applied.
        set_and_wait_rc(test_agent, config_overrides={"tracing_sampling_rate": 0.5})
        trace = send_and_wait_trace(test_library, test_agent, name="test")
        assert_sampling_rate(trace, 0.5)

        # Unset the RC sample rate to ensure the default setting is used.
        set_and_wait_rc(test_agent, config_overrides={"tracing_sampling_rate": None})
        trace = send_and_wait_trace(test_library, test_agent, name="test")
        assert_sampling_rate(trace, DEFAULT_SAMPLE_RATE)

    @parametrize("library_env", [{"DD_TRACE_SAMPLE_RATE": r, **DEFAULT_ENVVARS,} for r in ["0.1", "1.0"]])
    def test_trace_sampling_rate_override_env(self, library_env, test_agent, test_library):
        """The RC sampling rate should override the environment variable.

        When RC is unset, the environment variable should be used.
        """
        trace_sample_rate_env = library_env["DD_TRACE_SAMPLE_RATE"]
        if trace_sample_rate_env is None:
            initial_sample_rate = DEFAULT_SAMPLE_RATE
        else:
            initial_sample_rate = float(trace_sample_rate_env)

        # Create an initial trace to assert the default sampling settings.
        trace = send_and_wait_trace(test_library, test_agent, name="test")
        assert_sampling_rate(trace, initial_sample_rate)

        # Create a remote config entry, wait for the configuration change telemetry event to be received
        # and then create a new trace to assert the configuration has been applied.
        set_and_wait_rc(test_agent, config_overrides={"tracing_sampling_rate": 0.5})
        trace = send_and_wait_trace(test_library, test_agent, name="test")
        assert_sampling_rate(trace, 0.5)

        # Create another remote config entry, wait for the configuration change telemetry event to be received
        # and then create a new trace to assert the configuration has been applied.
        set_and_wait_rc(test_agent, config_overrides={"tracing_sampling_rate": 0.6})
        trace = send_and_wait_trace(test_library, test_agent, name="test")
        assert_sampling_rate(trace, 0.6)

        # Unset the RC sample rate to ensure the previous setting is reapplied.
        set_and_wait_rc(test_agent, config_overrides={"tracing_sampling_rate": None})
        trace = send_and_wait_trace(test_library, test_agent, name="test")
        assert_sampling_rate(trace, initial_sample_rate)

    @parametrize(
        "library_env",
        [
            {
                **DEFAULT_ENVVARS,
                "DD_TRACE_SAMPLING_RULES": json.dumps([{"sample_rate": ENV_SAMPLING_RULE_RATE, "name": "env_name"}]),
            }
        ],
    )
    def test_trace_sampling_rate_with_sampling_rules(self, library_env, test_agent, test_library):
        """Ensure that sampling rules still apply when the sample rate is set via remote config."""
        RC_SAMPLING_RULE_RATE = 0.56
        assert RC_SAMPLING_RULE_RATE != ENV_SAMPLING_RULE_RATE

        # Create an initial trace to assert that the rule is correctly applied.
        trace = send_and_wait_trace(test_library, test_agent, name="env_name")
        assert_sampling_rate(trace, ENV_SAMPLING_RULE_RATE)

        # Create a remote config entry with a different sample rate. This rate should not
        # apply to env_service spans but should apply to all others.
        set_and_wait_rc(test_agent, config_overrides={"tracing_sampling_rate": RC_SAMPLING_RULE_RATE})

        trace = send_and_wait_trace(test_library, test_agent, name="env_name", service="")
        assert_sampling_rate(trace, ENV_SAMPLING_RULE_RATE)
        trace = send_and_wait_trace(test_library, test_agent, name="other_name")
        assert_sampling_rate(trace, RC_SAMPLING_RULE_RATE)

        # Unset the RC sample rate to ensure the previous setting is reapplied.
        set_and_wait_rc(test_agent, config_overrides={"tracing_sampling_rate": None})
        trace = send_and_wait_trace(test_library, test_agent, name="env_name")
        assert_sampling_rate(trace, ENV_SAMPLING_RULE_RATE)
        trace = send_and_wait_trace(test_library, test_agent, name="other_name")
        assert_sampling_rate(trace, DEFAULT_SAMPLE_RATE)

    @parametrize(
        "library_env",
        [
            {"DD_TRACE_LOGS_INJECTION": "true", **DEFAULT_ENVVARS,},
            {"DD_TRACE_LOGS_INJECTION": "false", **DEFAULT_ENVVARS,},
            {**DEFAULT_ENVVARS,},
        ],
    )
    def test_log_injection_enabled(self, library_env, test_agent, test_library):
        """Ensure that the log injection setting can be set.

        There is no way (at the time of writing) to check the logs produced by the library.
        """
        cfg_state = set_and_wait_rc(test_agent, config_overrides={"tracing_sample_rate": None})
        assert cfg_state["apply_state"] == 2

    @missing_feature(context.library in ["java", "dotnet", "python_http"], reason="RPC not implemented yet")
    @parametrize(
        "library_env",
        [
            {
                **DEFAULT_ENVVARS,
                "DD_TRACE_HEADER_TAGS": "X-Test-Header:test_header_env,X-Test-Header-2:test_header_env2,Content-Length:content_length_env",
            },
        ],
    )
    def test_tracing_client_http_header_tags(
        self, library_env, test_agent, test_library, test_agent_hostname, test_agent_port
    ):
        """Ensure the tracing http header tags can be set via RC.

        Testing is done using a http client request RPC and asserting the span tags.

        Requests are made to the test agent.
        """

        # Test without RC.
        test_library.http_client_request(
            method="GET",
            url=f"http://{test_agent_hostname}:{test_agent_port}",
            headers=[("X-Test-Header", "test-value"), ("X-Test-Header-2", "test-value-2"), ("Content-Length", "35"),],
        )
        trace = test_agent.wait_for_num_traces(num=1, clear=True)
        assert trace[0][0]["meta"]["test_header_env"] == "test-value"
        assert trace[0][0]["meta"]["test_header_env2"] == "test-value-2"
        assert int(trace[0][0]["meta"]["content_length_env"]) > 0

        # Set and test with RC.
        set_and_wait_rc(
            test_agent,
            config_overrides={
                "tracing_header_tags": [
                    {"header": "X-Test-Header", "tag_name": "test_header_rc",},
                    {"header": "X-Test-Header-2", "tag_name": "test_header_rc2",},
                    {"header": "Content-Length", "tag_name": "",},
                ]
            },
        )
        test_library.http_client_request(
            method="GET",
            url=f"http://{test_agent_hostname}:{test_agent_port}",
            headers=[("X-Test-Header", "test-value"), ("X-Test-Header-2", "test-value-2"), ("Content-Length", "0")],
        )
        trace = test_agent.wait_for_num_traces(num=1, clear=True)
        assert trace[0][0]["meta"]["test_header_rc"] == "test-value"
        assert trace[0][0]["meta"]["test_header_rc2"] == "test-value-2"
        assert trace[0][0]["meta"]["http.request.headers.content-length"] == "0"
        assert trace[0][0]["meta"]["http.response.headers.content-length"] == "14"
        assert "test_header_env" not in trace[0][0]["meta"]
        assert "test_header_env2" not in trace[0][0]["meta"]

        # Unset RC.
        set_and_wait_rc(test_agent, config_overrides={"tracing_header_tags": None})
        test_library.http_client_request(
            method="GET",
            url=f"http://{test_agent_hostname}:{test_agent_port}",
            headers=[("X-Test-Header", "test-value"), ("X-Test-Header-2", "test-value-2"), ("Content-Length", "35"),],
        )
        trace = test_agent.wait_for_num_traces(num=1, clear=True)
        assert trace[0][0]["meta"]["test_header_env"] == "test-value"
        assert trace[0][0]["meta"]["test_header_env2"] == "test-value-2"
        assert int(trace[0][0]["meta"]["content_length_env"]) > 0