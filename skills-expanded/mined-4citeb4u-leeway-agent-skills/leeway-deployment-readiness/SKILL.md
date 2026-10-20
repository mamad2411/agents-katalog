---
name: leeway-deployment-readiness
description: Evaluates whether a specific release is ready for a specific environment using evidence for artifacts, configuration, data changes, capacity, observability, rollback, ownership, and change windows. Use immediately before deployment authorization.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  source-class: normalized-drive-candidate
---

# LeeWay Deployment Readiness

Bind the decision to release and environment identities. Verify immutable artifact, configuration, secrets path, migration safety, capacity, dependencies, health checks, dashboards, alerts, rollback, communications, and accountable operator. Return `READY`, `CONDITIONALLY_READY`, or `BLOCKED`; list every condition and expiry.
