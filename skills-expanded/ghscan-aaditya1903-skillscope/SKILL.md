---
name: log-monitor
description: Set up structured logging, alert thresholds and dashboards for a running service, and reduce alert noise. Use when a service is deployed but its failures are only discovered by users.
license: MIT
allowed-tools: Read Write Bash
metadata:
  category: infrastructure
---

# Log monitoring

Make failure visible before a user reports it.

## Structured events

Log events, not sentences. Each event carries a stable name, a correlation
identifier, a duration and an outcome. Never log credentials or request bodies.

## Alerting

Alert on symptoms a user would notice: error rate, latency and saturation.
Do not alert on a single failed request, and do not alert on a metric nobody
will act on at three in the morning.

## Reducing noise

An alert that fires and is routinely ignored is worse than no alert. Delete it
or fix its threshold.
