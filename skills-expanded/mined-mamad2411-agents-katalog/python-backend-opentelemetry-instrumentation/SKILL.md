---
name: python-backend-opentelemetry-instrumentation
version: "1.0"
description: >
  OpenTelemetry instrumentation for Python backend services including FastAPI and Flask.
  PROACTIVELY activate for: (1) Setting up OpenTelemetry in Python, (2) Auto-instrumenting FastAPI,
  (3) Creating manual spans, (4) Log correlation with traces, (5) Exporter configuration.
  Triggers: "opentelemetry python", "otel python", "flask trace", "fastapi trace", "setup-tracing", "python tracing"
core-integration:
  techniques:
    primary: ["systematic_analysis"]
    secondary: ["structured_evaluation"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Python Backend OpenTelemetry Instrumentation

Instrument Python backend services with OpenTelemetry for distributed tracing and continuing traces from upstream services.

## Installation

```bash
pip install opentelemetry-api opentelemetry-sdk \
  opentelemetry-exporter-otlp \
  opentelemetry-instrumentation-fastapi \
  opentelemetry-instrumentation-requests
```

## FastAPI Auto-Instrumentation

```python
# main.py
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Initialize tracing
resource = Resource.create({"service.name": "python-api", "service.version": "1.0.0"})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)  # Automatic tracing

@app.get("/users")
async def get_users():
    return {"users": []}
```

## Manual Spans

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("database-query") as span:
    span.set_attribute("db.system", "postgresql")
    result = await db.query("SELECT * FROM users")
    span.set_attribute("result.count", len(result))
```

## Log Correlation

```python
span = trace.get_current_span()
ctx = span.get_span_context()
logger.info("query", trace_id=format(ctx.trace_id, '032x'))
```

## Flask Integration

```python
from flask import Flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
```

## Requests Library Instrumentation

```python
from opentelemetry.instrumentation.requests import RequestsInstrumentor

RequestsInstrumentor().instrument()

# Now all requests.get/post calls are automatically traced
response = requests.get("https://api.example.com/data")
```

## Context Propagation

```python
from opentelemetry.propagate import inject
import requests

headers = {}
inject(headers)  # Injects traceparent header

response = requests.get("https://downstream.service/api", headers=headers)
```

## Best Practices

1. Use auto-instrumentation where available
2. Add custom spans for business logic
3. Set meaningful span attributes
4. Correlate logs with trace IDs
5. Configure appropriate sampling for production
