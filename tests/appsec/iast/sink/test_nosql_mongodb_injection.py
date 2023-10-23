# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

from utils import context, coverage, missing_feature, scenarios
from .._test_iast_fixtures import BaseSinkTest


@coverage.basic
class TestNoSqlMongodbInjection(BaseSinkTest):
    """Verify NoSQL injection detection in mongodb database."""

    vulnerability_type = "NOSQL_MONGODB_INJECTION"
    http_method = "POST"
    insecure_endpoint = "/iast/mongodb-nosql-injection/test_insecure"
    secure_endpoint = "/iast/mongodb-nosql-injection/test_secure"
    data = {"key": "somevalue"}
    location_map = {"nodejs": "iast/index.js"}

    @scenarios.integrations
    def test_insecure(self):
        super().test_insecure()

    @scenarios.integrations
    def test_secure(self):
        super().test_secure()

    @missing_feature(context.library < "java@1.13.0", reason="Not implemented yet")
    @missing_feature(library="nodejs", reason="Not implemented yet")
    @missing_feature(library="python", reason="Not implemented yet")
    def test_telemetry_metric_instrumented_sink(self):
        super().test_telemetry_metric_instrumented_sink()

    @missing_feature(context.library < "java@1.13.0", reason="Not implemented yet")
    @missing_feature(library="nodejs", reason="Not implemented yet")
    @missing_feature(library="python", reason="Not implemented yet")
    def test_telemetry_metric_executed_sink(self):
        super().test_telemetry_metric_executed_sink()
