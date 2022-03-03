# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

from utils import BaseTestCase, context, interfaces, released, rfc, irrelevant, missing_feature


@released(java="0.90.0", nodejs="2.0.0", python="0.58.5", ruby="0.54.2")
@irrelevant(library="cpp")
@irrelevant(context.library < "golang@1.36.0", reason="Before 1.36.0, go was using dedicated entry point")
@missing_feature(context.library <= "golang@1.36.2" and context.weblog_variant == "gin")
class Test_Events(BaseTestCase):
    """AppSec events uses version 1.0 (legacy appsec events on dedicated entry point)"""

    @missing_feature(context.library < "java@0.93.0")
    def test_appsec_in_traces(self):
        """ AppSec sends event in traces"""

        def validator(event):
            raise Exception("You are using old AppSec communication")

        def new_validator(span, event):
            return True

        interfaces.library.add_appsec_validation(legacy_validator=validator, validator=new_validator)
