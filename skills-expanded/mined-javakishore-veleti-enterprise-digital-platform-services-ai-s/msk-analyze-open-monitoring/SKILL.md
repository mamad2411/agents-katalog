---
name: msk-analyze-open-monitoring
description: Analyze Amazon MSK open monitoring with Prometheus-compatible broker and JMX metrics and integration into enterprise observability such as Datadog. Use for deeper Kafka telemetry beyond default CloudWatch monitoring.
---

# Analyze Open Monitoring

1. Confirm open monitoring is enabled and identify the telemetry path.
2. Inspect relevant broker/JMX and node metrics exposed by MSK.
3. Correlate Kafka-native metrics with CloudWatch and application telemetry.
4. Evaluate scrape/collection gaps before interpreting missing data as healthy behavior.
5. Route Datadog-specific analysis to `datadog-*` skills when telemetry is ingested there.
6. Avoid exposing sensitive configuration.

## Output
- Monitoring Configuration
- Kafka-Native Signals
- CloudWatch/Datadog Correlation
- Coverage Gaps
- Recommended Action
