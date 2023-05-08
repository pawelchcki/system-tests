from utils import weblog, interfaces, context


def _get_expectation(d):
    if d is None:
        return None
    if isinstance(d, str):
        return d
    elif callable(d):
        return d()
    else:
        expected = d.get(context.library.library)
        if isinstance(expected, dict):
            expected = expected.get(context.weblog_variant)
        return expected


class SinkFixture:
    def __init__(
        self,
        vulnerability_type,
        http_method,
        insecure_endpoint,
        secure_endpoint,
        data,
        location_map=None,
        evidence_map=None,
    ):
        self.vulnerability_type = vulnerability_type
        self.http_method = http_method
        self.insecure_endpoint = insecure_endpoint
        self.secure_endpoint = secure_endpoint
        self.data = data
        self.expected_location = _get_expectation(location_map)
        self.expected_evidence = _get_expectation(evidence_map)
        self.insecure_request = None
        self.secure_request = None

    def setup_insecure(self):
        if self.insecure_request is None:
            self.insecure_request = weblog.request(method=self.http_method, path=self.insecure_endpoint, data=self.data)

    def test_insecure(self):
        interfaces.library.expect_iast_vulnerabilities(
            self.insecure_request,
            vulnerability_count=1,
            vulnerability_type=self.vulnerability_type,
            location_path=self.expected_location,
            evidence=self.expected_evidence,
        )

    def setup_secure(self):
        self.secure_request = weblog.request(method=self.http_method, path=self.secure_endpoint, data=self.data)

    def test_secure(self):
        if self.secure_request is None:
            interfaces.library.expect_no_vulnerabilities(self.secure_request)