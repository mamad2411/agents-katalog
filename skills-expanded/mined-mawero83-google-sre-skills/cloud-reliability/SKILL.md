---
name: cloud-reliability
description: >-
  Apply SRE in cloud and hybrid environments: shared responsibility, managed services, multi-cloud observability, and platform trends from Google SRE 2e and sre.google/cloud. Use for cloud architecture and ops model design.
---

# Cloud Reliability

**Domain:** `ai`  
**Sources:** SRE Book 2e Ch3/22, https://sre.google/cloud/

## When to use

- Cloud migration reliability design
- Shared responsibility debates
- Hybrid/multi-cloud observability

## Principles

- Cloud shifts undifferentiated work but not accountability for user journeys.
- Managed services need explicit SLIs mapping provider SLAs ≠ your CUJ SLOs.
- OpenTelemetry and portable telemetry reduce lock-in of insight.
- Design for provider failure domains and control-plane outages.

## Workflow

1. Map CUJs to cloud components + shared responsibility.
2. Translate provider SLAs into your error budget math carefully.
3. Instrument app-level SLIs above infrastructure metrics.
4. Plan for control-plane and identity failures.
5. Test restore/failover across zones/regions you claim.

## Decision guide

- If relying on provider SLA alone → insufficient for customer SLO.

## Output template

```markdown
# Cloud reliability map
- CUJ → components:
- Shared responsibility notes:
- App SLIs vs provider metrics:
- Failure drills:
```

## Anti-patterns

- Assuming multi-AZ checkbox equals tested failover.

## Related skills

`monitoring-observability`, `disaster-planning`, `sli-slo-design`

## Canonical references

- [SRE on Google Cloud](https://sre.google/cloud/)
- [SRE Book 2e](https://sre.google/books/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
