---
name: distributed-tracing-context-propagation
version: "1.0"
description: >
  W3C Trace Context propagation across service boundaries for distributed tracing.
  PROACTIVELY activate for: (1) Implementing trace context propagation, (2) Cross-service correlation,
  (3) Setting up traceparent headers, (4) Baggage propagation, (5) Multi-service debugging.
  Triggers: "distributed tracing", "trace context", "traceparent", "correlation", "span", "baggage", "propagation"
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

# Distributed Tracing Context Propagation

This skill provides expertise in distributed tracing and context propagation across microservices.

## Overview

Distributed tracing enables tracking requests as they flow through multiple services, making it possible to understand system behavior and diagnose issues in microservice architectures.

## Key Concepts

- **W3C Trace Context**: Standard for trace context propagation (traceparent, tracestate)
- **Span**: A single operation within a trace
- **Trace ID**: Unique identifier for an entire request flow
- **Span ID**: Unique identifier for a specific operation
- **Baggage**: Key-value pairs propagated across service boundaries

## Implementation Patterns

### HTTP Header Propagation

```
traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
tracestate: vendor1=value1,vendor2=value2
```

### Context Extraction and Injection

1. Extract context from incoming request headers
2. Create child spans for local operations
3. Inject context into outgoing request headers

## Best Practices

1. Always propagate trace context across service boundaries
2. Use baggage for cross-cutting concerns (user ID, tenant ID)
3. Correlate logs with trace IDs
4. Set appropriate sampling rates

[Content to be expanded based on plugin_spec_agentient-observability.md specifications]
