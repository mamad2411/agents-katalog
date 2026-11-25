---
name: references
description: Reference material for the cloud-solution-architect skill. Use when you need the supporting best practices, pattern catalogs, or technology decision tables behind the parent guidance.
source: https://github.com/MicrosoftDocs/azure-architecture-center
---

# Cloud Solution Architect References

Supporting reference pack for the parent cloud-solution-architect skill.

## Files In This Folder

- `best-practices.md`: twelve Azure Architecture Center practices covering APIs, autoscaling, background jobs, and caching
- `design-patterns.md`: cloud pattern catalog grouped by reliability, data, messaging, security, and performance concerns
- `mission-critical.md`: active-active, deployment stamp, and health-model guidance for 99.99% workloads
- `technology-choices.md`: decision tables for compute, storage, databases, messaging, and networking

## How To Use This Folder

- Start with `technology-choices.md` when service selection is still open
- Use `best-practices.md` to pressure-test an existing design for obvious gaps
- Use `design-patterns.md` when a workload has a specific failure mode, integration problem, or scaling constraint
- Reach for `mission-critical.md` only when the availability target justifies the extra operational cost and complexity
