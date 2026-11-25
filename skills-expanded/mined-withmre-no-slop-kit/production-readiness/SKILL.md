---
name: production-readiness
description: Run a release-readiness audit for a web application or service. Use before production launch, a public event, a high-traffic release, or when asked for a comprehensive audit.
---

# Production readiness

This is a router and reporting contract, not a substitute for the specialist skills.

## 1. Choose the relevant checks

| If the system has… | Load… |
|---|---|
| auth, database, API, payments, webhooks, uploads or secrets | `security` |
| queries, external calls, queues, caching, logs, backups or load concerns | `reliability` |
| Docker, Compose, Kubernetes, ports, images or deployment configuration | `container-security` |
| user-facing pages or an admin interface | `ui-design` |

Start with a short threat model: assets to protect, actors, trust boundaries, abusive actions, sensitive data and the impact of failure. Do not claim a control exists until you have evidence.

## 2. Critical-path drills

For each critical workflow, check its success path, invalid input, duplicate request, dependency outage, worker crash and recovery path. Include the expected observability signal and rollback path.

For asynchronous work, require: bounded queue, idempotency key, lease or retry ownership, backoff with jitter, terminal failure state, backlog metric and a retention policy.

For high traffic, require: a target load profile, p95/p99 latency target, database query plan for hot queries, connection capacity, rate limits and a load test outside production.

## 3. Report

Read `report-format.md`. Do not change production state during an audit unless the user explicitly asked for a remediation.
