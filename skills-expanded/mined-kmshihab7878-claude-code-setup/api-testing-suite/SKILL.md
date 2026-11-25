---
name: api-testing-suite
description: API testing with Bruno, Schemathesis, Hypothesis property-based testing, and OpenAPI validation for REST APIs
triggers:
  - api testing
  - bruno
  - schemathesis
  - api test
  - contract testing
  - openapi test
---

# API Testing Suite

Comprehensive API testing: Bruno (manual/collection), Schemathesis (property-based), Hypothesis (fuzzing), Spectral (linting), Locust (load).

## Schemathesis (Property-Based API Testing)

Automatically generates test cases from your OpenAPI spec:

```bash
# Run against local server
schemathesis run http://localhost:8000/openapi.json --checks all

# With authentication
schemathesis run http://localhost:8000/openapi.json \
  --header "Authorization: Bearer $TOKEN" \
  --checks all --stateful=links

# Target specific endpoints
schemathesis run http://localhost:8000/openapi.json \
  --endpoint "/api/v1/agents" --method POST
```

## Hypothesis for API Fuzzing

```python
from hypothesis import given, strategies as st, settings
import httpx

@given(
    name=st.text(min_size=1, max_size=100),
    priority=st.integers(min_value=0, max_value=10),
)
@settings(max_examples=200)
def test_create_agent_fuzz(name, priority):
    response = httpx.post("http://localhost:8000/api/v1/agents", json={
        "name": name, "priority": priority
    })
    assert response.status_code in (201, 422)  # Created or validation error
    if response.status_code == 201:
        data = response.json()
        assert data["name"] == name
```

## Spectral (OpenAPI Linting)

```bash
# Lint OpenAPI spec
spectral lint openapi.yaml --ruleset .spectral.yaml
```

```yaml
# .spectral.yaml
extends: spectral:oas
rules:
  operation-operationId: error
  operation-description: warn
  oas3-api-servers: error
  no-eval-in-markdown: error
```

## Load Testing with Locust

```python
from locust import HttpUser, task, between

class CoreMindUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def list_agents(self):
        self.client.get("/api/v1/agents")

    @task(1)
    def create_task(self):
        self.client.post("/api/v1/tasks", json={
            "description": "Test task", "agent": "default"
        })
```

```bash
locust -f tests/load/locustfile.py --host http://localhost:8000 --headless -u 100 -r 10 -t 60s
```
