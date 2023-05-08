# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

import pytest
from utils import context, coverage, released, missing_feature
from ..iast_fixtures import SinkFixture

if context.library == "cpp":
    pytestmark = pytest.mark.skip("not relevant")


@coverage.basic
@released(dotnet="?", golang="?", php_appsec="?", python="?", ruby="?")
@released(
    java={
        "spring-boot": "1.1.0",
        "spring-boot-jetty": "1.1.0",
        "spring-boot-openliberty": "1.1.0",
        "spring-boot-wildfly": "1.1.0",
        "spring-boot-undertow": "1.1.0",
        "resteasy-netty3": "1.11.0",
        "jersey-grizzly2": "1.11.0",
        "vertx3": "1.12.0",
        "*": "?",
    }
)
@released(nodejs={"express4": "3.11.0", "*": "?"})
@missing_feature(context.weblog_variant == "spring-boot-native", reason="GraalVM. Tracing support only")
@missing_feature(context.weblog_variant == "spring-boot-3-native", reason="GraalVM. Tracing support only")
class TestCommandInjection:
    """Test command injection detection."""

    sink_fixture = SinkFixture(
        vulnerability_type="COMMAND_INJECTION",
        http_method="POST",
        insecure_endpoint="/iast/cmdi/test_insecure",
        secure_endpoint="/iast/cmdi/test_secure",
        data={"cmd": "ls"},
        location_map={"java": "com.datadoghq.system_tests.iast.utils.CmdExamples", "nodejs": "iast.js",},
    )

    def setup_insecure(self):
        self.sink_fixture.setup_insecure()

    def test_insecure(self):
        self.sink_fixture.test_insecure()

    def setup_secure(self):
        self.sink_fixture.setup_secure()

    @missing_feature(reason="Endpoint not implemented")
    def test_secure(self):
        self.sink_fixture.test_secure()