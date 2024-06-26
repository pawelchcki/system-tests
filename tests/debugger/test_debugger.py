# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

import tests.debugger.utils as base

from utils import scenarios, interfaces, weblog, features


@features.debugger
@scenarios.debugger_probes_status
class Test_Debugger_Probe_Statuses:
    def test_method_probe_status(self):
        expected_probes = {
            "loga0cf2-meth-45cf-9f39-591received": "RECEIVED",
            "loga0cf2-meth-45cf-9f39-59installed": "INSTALLED",
            "metricf2-meth-45cf-9f39-591received": "RECEIVED",
            "metricf2-meth-45cf-9f39-59installed": "INSTALLED",
            "span0cf2-meth-45cf-9f39-591received": "RECEIVED",
            "span0cf2-meth-45cf-9f39-59installed": "INSTALLED",
            "decorcf2-meth-45cf-9f39-591received": "RECEIVED",
            "decorcf2-meth-45cf-9f39-59installed": "INSTALLED",
        }

        base.validate_probes(expected_probes)

    def test_line_probe_status(self):
        expected_probes = {
            "loga0cf2-line-45cf-9f39-59installed": "INSTALLED",
            "metricf2-line-45cf-9f39-59installed": "INSTALLED",
            "decorcf2-line-45cf-9f39-59installed": "INSTALLED",
        }

        base.validate_probes(expected_probes)


@features.debugger
@scenarios.debugger_method_probes_snapshot
class Test_Debugger_Method_Probe_Snaphots(base._Base_Debugger_Test):
    def setup_method_probe_snaphots(self):
        self.expected_probe_ids = [
            "log170aa-acda-4453-9111-1478a6method",
            "metricaa-acda-4453-9111-1478a6method",
            "span70aa-acda-4453-9111-1478a6method",
            "decor0aa-acda-4453-9111-1478a6method",
        ]

        interfaces.library.wait_for_remote_config_request()
        interfaces.agent.wait_for(self.wait_for_all_probes_installed, timeout=30)
        self.weblog_responses = [
            weblog.get("/debugger/log"),
            weblog.get("/debugger/metric/1"),
            weblog.get("/debugger/span"),
            weblog.get("/debugger/span-decoration/asd/1"),
        ]

    def test_method_probe_snaphots(self):
        self.assert_remote_config_is_sent()
        self.assert_all_probes_are_installed()
        self.assert_all_weblog_responses_ok()

        expected_probes = {
            "log170aa-acda-4453-9111-1478a6method": "INSTALLED",
            "metricaa-acda-4453-9111-1478a6method": "INSTALLED",
            "span70aa-acda-4453-9111-1478a6method": "INSTALLED",
            "decor0aa-acda-4453-9111-1478a6method": "INSTALLED",
        }
        expected_snapshots = ["log170aa-acda-4453-9111-1478a6method"]
        expected_spans = ["span70aa-acda-4453-9111-1478a6method", "decor0aa-acda-4453-9111-1478a6method"]

        base.validate_probes(expected_probes)
        base.validate_snapshots(expected_snapshots)
        base.validate_spans(expected_spans)


@features.debugger
@scenarios.debugger_line_probes_snapshot
class Test_Debugger_Line_Probe_Snaphots(base._Base_Debugger_Test):
    def setup_line_probe_snaphots(self):
        self.expected_probe_ids = [
            "log170aa-acda-4453-9111-1478a697line",
            "metricaa-acda-4453-9111-1478a697line",
            "decor0aa-acda-4453-9111-1478a697line",
        ]

        interfaces.library.wait_for_remote_config_request()
        interfaces.agent.wait_for(self.wait_for_all_probes_installed, timeout=30)
        self.weblog_responses = [
            weblog.get("/debugger/log"),
            weblog.get("/debugger/metric/1"),
            weblog.get("/debugger/span-decoration/asd/1"),
        ]

    def test_line_probe_snaphots(self):
        self.assert_remote_config_is_sent()
        self.assert_all_probes_are_installed()
        self.assert_all_weblog_responses_ok()

        expected_probes = {
            "log170aa-acda-4453-9111-1478a697line": "INSTALLED",
            "metricaa-acda-4453-9111-1478a697line": "INSTALLED",
            "decor0aa-acda-4453-9111-1478a697line": "INSTALLED",
        }
        expected_snapshots = ["log170aa-acda-4453-9111-1478a697line"]
        expected_spans = ["decor0aa-acda-4453-9111-1478a697line"]

        base.validate_probes(expected_probes)
        base.validate_snapshots(expected_snapshots)
        base.validate_spans(expected_spans)


@features.debugger
@scenarios.debugger_mix_log_probe
class Test_Debugger_Mix_Log_Probe(base._Base_Debugger_Test):
    def setup_mix_probe(self):
        self.expected_probe_ids = [
            "logfb5a-1974-4cdb-b1dd-77dba2method",
            "logfb5a-1974-4cdb-b1dd-77dba2f1line",
        ]

        interfaces.library.wait_for_remote_config_request()
        interfaces.agent.wait_for(self.wait_for_all_probes_installed, timeout=30)
        self.weblog_responses = [weblog.get("/debugger/mix/asd/1")]

    def test_mix_probe(self):
        self.assert_remote_config_is_sent()
        self.assert_all_probes_are_installed()
        self.assert_all_weblog_responses_ok()

        expected_probes = {
            "logfb5a-1974-4cdb-b1dd-77dba2method": "INSTALLED",
            "logfb5a-1974-4cdb-b1dd-77dba2f1line": "INSTALLED",
        }

        expected_snapshots = [
            "logfb5a-1974-4cdb-b1dd-77dba2method",
            "logfb5a-1974-4cdb-b1dd-77dba2f1line",
        ]

        base.validate_probes(expected_probes)
        base.validate_snapshots(expected_snapshots)
