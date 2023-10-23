# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

from utils import context, coverage, irrelevant
from .._test_iast_fixtures import BaseSinkTestWithoutTelemetry


def _expected_location():
    if context.library.library == "java":
        if context.weblog_variant.startswith("spring-boot"):
            return "com.datadoghq.system_tests.springboot.AppSecIast"
        if context.weblog_variant == "resteasy-netty3":
            return "com.datadoghq.resteasy.IastSinkResource"
        if context.weblog_variant == "jersey-grizzly2":
            return "com.datadoghq.jersey.IastSinkResource"
        if context.weblog_variant == "vertx3":
            return "com.datadoghq.vertx3.iast.routes.IastSinkRouteProvider"
        if context.weblog_variant == "vertx4":
            return "com.datadoghq.vertx4.iast.routes.IastSinkRouteProvider"
    if context.library.library == "nodejs":
        return "iast/index.js"


@coverage.basic
class TestUnvalidatedRedirect(BaseSinkTestWithoutTelemetry):
    """Verify Unvalidated redirect detection."""

    vulnerability_type = "UNVALIDATED_REDIRECT"
    http_method = "POST"
    insecure_endpoint = "/iast/unvalidated_redirect/test_insecure_redirect"
    secure_endpoint = "/iast/unvalidated_redirect/test_secure_redirect"
    data = {"location": "http://dummy.location.com"}
    location_map = _expected_location()

    @irrelevant(library="java", weblog_variant="vertx3", reason="vertx3 redirects using location header")
    def test_insecure(self):
        super().test_insecure()

    @irrelevant(library="java", weblog_variant="vertx3", reason="vertx3 redirects using location header")
    def test_secure(self):
        super().test_secure()


@coverage.basic
class TestUnvalidatedHeader(BaseSinkTestWithoutTelemetry):
    """Verify Unvalidated redirect detection threw header."""

    vulnerability_type = "UNVALIDATED_REDIRECT"
    http_method = "POST"
    insecure_endpoint = "/iast/unvalidated_redirect/test_insecure_header"
    secure_endpoint = "/iast/unvalidated_redirect/test_secure_header"
    data = {"location": "http://dummy.location.com"}
    location_map = _expected_location()
