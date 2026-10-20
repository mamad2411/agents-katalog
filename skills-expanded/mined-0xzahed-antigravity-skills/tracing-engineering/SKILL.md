---
name: tracing-engineering
description: Implement distributed tracing. Use when understanding latency across services.
metadata:
  tags: tracing, engineering
---

# Distributed Tracing Engineering

## Use this skill when
- Instrumenting requests across services
- Propagating trace context
- Using traces to find latency hotspots

## Do not use this skill when
- Aggregate metrics for alerting (use metrics-engineering)
- Log details (use logging-engineering)

## Instructions
1. Propagate trace context (W3C) through all hops and async work.
2. Instrument automatic middleware + key manual spans.
3. Keep span naming consistent and set meaningful attributes.
4. Sample sensibly: head-based + priority for hot paths.
5. Budget data: push only what you query.
6. Give every service a trace exporter with batching.
7. Correlate traces to logs by trace ID.

## Checklist
- Context propagates through queues too
- Sample rate sane
- Spans at boundaries

## Output Format
- Trace model | instrumentation map | sampling | export

## Common Mistakes
- Spans restarting context
- Async work outside trace context
- Tracing every DB call at 100% cost
