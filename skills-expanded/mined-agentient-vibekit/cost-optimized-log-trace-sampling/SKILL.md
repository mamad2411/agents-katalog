---
name: cost-optimized-log-trace-sampling
version: "1.0"
description: >
  Sampling strategies for logs and traces to optimize costs while maintaining observability.
  PROACTIVELY activate for: (1) Configuring trace sampling, (2) Log volume reduction,
  (3) Head-based vs tail-based sampling, (4) Priority-based sampling, (5) Cost optimization.
  Triggers: "sampling", "trace sampling", "log sampling", "cost optimization", "head-based", "tail-based", "sample rate"
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

# Cost-Optimized Log and Trace Sampling

This skill provides expertise in sampling strategies for managing observability costs.

## Overview

Observability data can be expensive at scale. Smart sampling strategies maintain visibility while controlling costs.

## Sampling Strategies

### Head-Based Sampling

Decision made at trace start:
- **Probabilistic**: Sample X% of traces randomly
- **Rate-limiting**: Sample up to N traces per second

```yaml
# OpenTelemetry config
sampler:
  type: traceidratio
  ratio: 0.1  # Sample 10%
```

### Tail-Based Sampling

Decision made after trace completes:
- **Error-based**: Always sample traces with errors
- **Latency-based**: Sample slow traces (> p99 latency)
- **Attribute-based**: Sample specific user IDs or endpoints

### Hybrid Approaches

1. Sample 100% of errors
2. Sample 100% of slow requests
3. Sample 10% of successful, fast requests

## Log Sampling Strategies

1. **Dynamic log levels**: Debug in dev, warn in prod
2. **Sample verbose logs**: Log 1% of debug statements
3. **Aggregate before sending**: Count similar events locally

## Cost Optimization Tips

1. Set appropriate retention periods
2. Use log aggregation to reduce volume
3. Filter noise before export
4. Use tiered storage (hot/warm/cold)

[Content to be expanded based on plugin_spec_agentient-observability.md specifications]
