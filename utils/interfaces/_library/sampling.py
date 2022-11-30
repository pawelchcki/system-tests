# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

from collections import defaultdict

from utils.tools import logger
from utils.interfaces._core import BaseValidation
from utils.interfaces._library._utils import _spans_with_parent


class _TracesSamplingDecisionValidator:
    def __init__(self, sample_rate):
        super().__init__()
        self.sample_rate = sample_rate

    def __call__(self, data, root_span):
        sampling_priority = root_span["metrics"].get("_sampling_priority_v1")
        if sampling_priority is None:
            raise Exception(
                f"Message: {data['log_filename']}:"
                "Metric _sampling_priority_v1 should be set on traces that with sampling decision"
            )
        if sampling_priority not in (
            expected := self.get_sampling_decision(self.sample_rate, root_span["trace_id"], root_span["meta"])
        ):
            raise Exception(
                f"Trace id {root_span['trace_id']} " f"sampling priority is {sampling_priority}, should be {expected}"
            )

    @staticmethod
    def get_sampling_decision(sampling_rate, trace_id, meta):
        """Algorithm described in the priority sampling RFC
        https://github.com/DataDog/architecture/blob/master/rfcs/apm/integrations/priority-sampling/rfc.md"""
        MAX_TRACE_ID = 2 ** 64
        KNUTH_FACTOR = 1111111111111111111
        AUTO_REJECT = 0
        AUTO_KEEP = 1
        MANUAL_KEEP = 2
        MANUAL_REJECT = -1

        if meta.get("appsec.event", None) == "true" or meta.get("_dd.appsec.event_rules.errors", None) is not None:
            return (MANUAL_KEEP,)

        if ((trace_id * KNUTH_FACTOR) % MAX_TRACE_ID) <= (sampling_rate * MAX_TRACE_ID):
            return (AUTO_KEEP, MANUAL_KEEP)
        return (AUTO_REJECT, MANUAL_REJECT)


class _DistributedTracesDeterministicSamplingDecisisonValidation(BaseValidation):
    """Asserts that traces with the same id have the same sampling decisions"""

    path_filters = ["/v0.4/traces", "/v0.5/traces"]
    is_success_on_expiry = False

    def __init__(self, traces, request=None):
        super().__init__(request=request)
        self.traces = {trace["parent_id"]: trace for trace in traces}
        self.sampling_decisions_per_trace_id = defaultdict(list)

    def check(self, data):
        for span in _spans_with_parent(data["request"]["content"], self.traces.keys()):
            self.is_success_on_expiry = True
            expected_trace_id = self.traces[(span["parent_id"])]["trace_id"]
            if self.expect(
                span["trace_id"] == expected_trace_id,
                f"Message: {data['log_filename']}: If parent_id matches, "
                f"trace_id should match too expected trace_id {expected_trace_id} "
                f"span trace_id : {span['trace_id']}, span parent_id : {span['parent_id']}",
            ):
                return
            sampling_priority = span["metrics"].get("_sampling_priority_v1")
            if self.expect(
                sampling_priority is not None, f"Message: {data['log_filename']}: sampling priority should be set",
            ):
                return
            self.sampling_decisions_per_trace_id[span["trace_id"]].append(sampling_priority)

    def final_check(self):
        fail = False
        for trace_id, decisions in self.sampling_decisions_per_trace_id.items():
            if len(decisions) < 2:
                continue
            if not all((d == decisions[0] for d in decisions)):
                logger.error(f"Sampling decisions are not deterministic for trace_id {trace_id}")
                fail = True

        if fail:
            raise Exception("Some trace does not respect the sampling decision")


class _AddSamplingDecisionValidation(BaseValidation):
    """Asserts that a trace sampling decisions are taken for choosen traces and spans"""

    path_filters = ["/v0.4/traces", "/v0.5/traces"]
    is_success_on_expiry = False

    def __init__(self, traces, request=None):
        super().__init__(request=request)
        self.traces = {trace["parent_id"]: trace for trace in traces}
        self.errors = set()
        self.count = 0

    def check(self, data):
        for span in _spans_with_parent(data["request"]["content"], self.traces.keys()):
            self.is_success_on_expiry = True
            expected_trace_id = self.traces[span["parent_id"]]["trace_id"]
            if self.expect(
                span["trace_id"] == expected_trace_id,
                f"Message: {data['log_filename']}: If parent_id matches, "
                f"trace_id should match too expected trace_id {expected_trace_id} "
                f"span trace_id : {span['trace_id']}, span parent_id : {span['parent_id']}",
            ):
                return
            sampling_priority = span["metrics"].get("_sampling_priority_v1")
            if self.expect(
                sampling_priority is not None,
                f"Message: {data['log_filename']}: sampling priority should be set on span {span['span_id']}",
            ):
                return
            self.count += 1

    def final_check(self):
        if self.count != len(self.traces):
            raise Exception("Didn't see all requests")
