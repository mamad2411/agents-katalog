---
name: datadog-diagnose-incident
description: Diagnose production and non-production incidents using Datadog logs, APM traces, metrics, events, deployments, infrastructure, dependencies, and service metadata. Use as the primary Datadog incident workflow when the failure domain is not yet known.
---

# Diagnose Incident

1. Read `.digital-platform-ai/observability.yaml`, service metadata, dependencies, and environment context.
2. Establish the incident time window and affected user/service behavior.
3. Gather independent evidence in parallel:
   - logs
   - traces
   - metrics
   - deployment/change events
   - infrastructure/container signals
4. Follow request/dependency evidence across services when needed.
5. Establish a timeline and identify the first confirmed abnormal event.
6. Separate symptom, contributing condition, and supported root cause.
7. State unknowns when evidence is insufficient.

## Output
- Incident Scope
- Timeline
- First Confirmed Failure
- Correlated Evidence
- Root Cause Status
- Recommended Action
