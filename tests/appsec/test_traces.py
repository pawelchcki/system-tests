# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

import pytest

from utils import BaseTestCase, context, interfaces, released, bug, missing_feature, irrelevant


if context.library == "cpp":
    pytestmark = pytest.mark.skip("not relevant")

RUNTIME_FAMILIES = ["nodejs", "ruby", "jvm", "dotnet", "go", "php", "python"]


@released(golang="1.36.0")
@released(dotnet="1.29.0", java="0.92.0")
@released(nodejs="2.0.0", php_appsec="0.1.0", ruby="0.54.2")
@missing_feature(context.library <= "golang@1.36.2" and context.weblog_variant == "gin")
@missing_feature(context.library < "python@0.58.5")
class Test_AppSecEventSpanTags(BaseTestCase):
    """ AppSec correctly fill span tags. """

    @classmethod
    def setup_class(cls):
        """Send a bunch of attack, to be sure that something is done on AppSec side"""
        get = cls().weblog_get

        get("/waf", params={"key": "\n :"})  # rules.http_protocol_violation.crs_921_160
        get("/waf", headers={"random-key": "acunetix-user-agreement"})  # rules.security_scanner.crs_913_110

    @missing_feature(library="python")
    def test_appsec_event_span_tags(self):
        """
        Spans with AppSec events should have the general AppSec span tags, along with the appsec.event and
        _sampling_priority_v1 tags
        """

        def validate_appsec_event_span_tags(span):
            if span.get("parent_id") not in (0, None):  # do nothing if not root span
                return

            if "appsec.event" not in span["meta"]:
                raise Exception("Can't find appsec.event in span's meta")

            if span["meta"]["appsec.event"] != "true":
                raise Exception(f'appsec.event in span\'s meta should be "true", not {span["meta"]["appsec.event"]}')

            if "_sampling_priority_v1" not in span["metrics"]:
                raise Exception("Metric _sampling_priority_v1 should be set on traces that are manually kept")

            MANUAL_KEEP = 2
            if span["metrics"]["_sampling_priority_v1"] != MANUAL_KEEP:
                raise Exception(f"Trace id {span['trace_id']} , sampling priority should be {MANUAL_KEEP}")

            return True

        r = self.weblog_get("/waf/", headers={"User-Agent": "Arachni/v1"})
        interfaces.library.add_span_validation(r, validate_appsec_event_span_tags)

    def test_custom_span_tags(self):
        """AppSec should store in all APM spans some tags when enabled."""

        def validate_custom_span_tags(span):
            if span.get("type") != "web":
                return

            if span.get("parent_id") not in (0, None):  # do nothing if not root span
                return

            if "_dd.appsec.enabled" not in span["metrics"]:
                raise Exception("Can't find _dd.appsec.enabled in span's metrics")

            if "_dd.runtime_family" not in span["meta"]:
                raise Exception("Can't find _dd.runtime_family in span's meta")

            if span["metrics"]["_dd.appsec.enabled"] != 1:
                raise Exception(
                    f'_dd.appsec.enabled in span\'s metrics should be 1 or 1.0, not {span["metrics"]["_dd.appsec.enabled"]}'
                )

            if span["meta"]["_dd.runtime_family"] not in RUNTIME_FAMILIES:
                raise Exception(f"_dd.runtime_family {span['_dd.runtime_family']}, should be in {RUNTIME_FAMILIES}")

            return True

        interfaces.library.add_span_validation(validator=validate_custom_span_tags)

    @missing_feature(context.library < "golang@1.36.0")
    @irrelevant(context.library not in ["golang", "nodejs"], reason="test")
    def test_header_collection(self):
        """
        AppSec should collect some headers for http.request and http.response and store them in span tags.
        Note that this test checks for collection, not data.
        """

        def assertHeaderInSpanMeta(span, h):
            if h not in span["meta"]:
                raise Exception("Can't find {header} in span's meta".format(header=h))

        def validate_request_headers(span):
            for h in ["user-agent", "host", "content-type"]:
                assertHeaderInSpanMeta(span, f"http.request.headers.{h}")
            return True

        def validate_response_headers(span):
            for h in ["content-type", "content-length", "content-language"]:
                assertHeaderInSpanMeta(span, f"http.response.headers.{h}")
            return True

        r = self.weblog_get("/headers/", headers={"User-Agent": "Arachni/v1", "Content-Type": "text/plain"})
        interfaces.library.add_span_validation(r, validate_request_headers)
        interfaces.library.add_span_validation(r, validate_response_headers)

    @missing_feature(library="python")
    @bug(context.library < "java@0.93.0")
    @missing_feature(library="php")  # need to generate a user trace
    def test_root_span_coherence(self):
        """ Appsec tags are not on span where type is not web """

        def validator(span):
            if span.get("type") == "web":
                return

            if "_dd.appsec.enabled" in span["metrics"]:
                raise Exception("_dd.appsec.enabled should be present when span type is web")

            if "_dd.runtime_family" in span["meta"]:
                raise Exception("_dd.runtime_family should be present when span type is web")

            return True

        interfaces.library.add_span_validation(validator=validator)
