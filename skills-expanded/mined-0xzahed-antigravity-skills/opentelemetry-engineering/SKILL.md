---
name: opentelemetry-engineering
description: Apply OpenTelemetry across stacks. Use when instrumenting
  applications consistently.
metadata:
  tags: opentelemetry, engineering
---

# OpenTelemetry Engineering

## Use this skill when
- Setting up the SDK, exporters, and instrumentation
- Adopting standard signals (traces, metrics, logs)
- Correlating data across many services

## Do not use this skill when
- Choosing a vendor backend
- Single non-OTel systems

## Instructions
1. Configure the SDK once centrally with a consistent resource.
2. Use auto-instrumentation libraries; add manual spans where needed.
3. Define one semantic-conventions convention across services.
4. Set an exporter with batching and retries; tune sampling.
5. Push to an OTLP collector for routing and enrichment.
6. Pin resource attributes: service.name, env, version.
7. Keep SDK version upgrades coordinated.

## Checklist
- Central SDK config
- Consistent semantic conventions
- Collector routes correctly

## Output Format
- SDK config | instrumentation | attributes | sampling | collector

## Common Mistakes
- Each team wiring its own OTel incoherently
- Ignoring exporter failures
- No resource attributes (orphaned data)
