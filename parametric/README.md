# APM library parametric tests

The test fixtures in this submodule allow features of the APM libraries to be easily parameterized while still targeting
each of the libraries.

Example:

```python
@all_libs()
@pytest.mark.parametrize("apm_test_server_env", [
    {
        "DD_SERVICE": "svc1",
    },
    {
        "DD_SERVICE": "svc2",
    }
])
def test_the_suite(apm_test_server_env: Dict[str, str], test_agent: TestAgentAPI, test_client: _TestTracer):
    with test_client:
        with test_client.start_span(name="web.request", resource="/users") as span:
            span.set_meta("mytag", "value")

    traces = test_agent.traces()
    assert traces[0][0]["meta"]["mytag"] == "value"
    assert traces[0][0]["service"] == apm_test_server_env["DD_SERVICE"]
```

- This test case runs against all the APM libraries (`all_libs()`) and is parameterized with two different environments specifying two different values of the environment variable `DD_SERVICE`.
- The test case creates a new root span and sets a tag on it using the shared GRPC interface.
- Data is flushed to the test agent after the with test_client block closes.
- Data is retrieved using the `test_agent` fixture and asserted on.

## Implementation

### Shared Interface

In order to achieve shared tests, we introduce a shared GRPC interface to the clients. Thus, each client need only implement the GRPC interface server and then these shared tests can be run against the library. The GRPC interface implements common APIs across the clients which provide the building blocks for test cases.

```proto
service APMClient {
  rpc StartSpan(StartSpanArgs) returns (StartSpanReturn) {}
  rpc FinishSpan(FinishSpanArgs) returns (FinishSpanReturn) {}
  rpc SpanSetMeta(SpanSetMetaArgs) returns (SpanSetMetaReturn) {}
  rpc SpanSetMetric(SpanSetMetricArgs) returns (SpanSetMetricReturn) {}
  rpc FlushSpans(FlushSpansArgs) returns (FlushSpansReturn) {}
  rpc FlushTraceStats(FlushTraceStatsArgs) returns (FlushTraceStatsReturn) {}
}
```

### Architecture

- Shared tests are written in Python (pytest).
- GRPC servers for each language are built and run in docker containers.
- [test agent](https://github.com/DataDog/dd-apm-test-agent/) is started in a container to collect the data from the GRPC servers. 

Test cases are written in Python and target the shared GRPC interface. The tests use a GRPC client to query the servers and the servers generate the data which is submitted to the test agent. Test cases can then query the data from the test agent to perform assertions.


<img width="869" alt="image" src="https://user-images.githubusercontent.com/6321485/182887064-e241d65c-5e29-451b-a8a8-e8d18328c083.png">


## Local Development

### Requirements
- docker
- protobuf
- Python >= 3.7

### Running the Tests

In the root of the system-tests repo, run the following:

(Note that `parametric/run.sh` explicitly ignores the root `conftest.py`, otherwise the root `conftest.py` will interfere with the parametric tests.)

```bash
cd parametric
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
CLIENTS_ENABLED=<client_language> ./run.sh
```