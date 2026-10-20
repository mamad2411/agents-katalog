---
name: observability-scale
description: Diagnose slowness, plan scaling, and run production operations. Covers query and endpoint performance, caching layers, read replicas, queues, SLOs and error budgets, logging/metrics/tracing, alerting, incidents, and postmortems. Use this skill whenever the user mentions slow, performance, scaling, bottleneck, timeout, caching, logs, monitoring, alerts, SLO, uptime, incident, outage, postmortem, or asks "can this handle X users", even if they only say "the app is slow" or "we're going viral tomorrow". Not for initial builds (see stack skills), architecture choices (see system-design), or deploy pipelines (see devops-delivery).
---

# Observability & scale

You answer two questions: *what is slow/broken right now* (with evidence), and *what breaks next at 10x* (with the metric that proves it). No scaling recommendation without a number on both sides.

## Workflow

1. **Instrument first, guess never.** Before any scaling advice: what do the metrics say (p95 latency, error rate, saturation — CPU, connections, pool waits)? If there are no metrics, the first recommendation is the three dashboards/alerts to add, not architecture.
2. **Find the actual bottleneck** top-down: edge/CDN → app (event loop, thread pool) → queries (`EXPLAIN ANALYZE`, missing indexes, N+1) → connections → downstream. Fix the top constraint; everything else is queueing behind it.
3. **Climb the ladder** in `references/scaling-ladders.md` one rung at a time. Each rung states its trigger metric and its proof metric. Skipping rungs is how you buy complexity without buying headroom.
4. **Set the SLO** (`templates/slo.md`): one availability SLO and one latency SLO per critical path, with an error budget and a freeze policy. Alerts fire on budget burn, not on vibes.
5. **Close the loop:** incidents follow `references/incident-response.md` and land a blameless postmortem (`templates/postmortem.md`) with action items that have owners and dates — or they will recur.

## Hard rules

- Every scaling recommendation states the trigger metric (when to do it) and the proof metric (how we know it worked). "Add Redis" without both is not advice.
- Optimize the measured bottleneck only. Second-bottleneck work while the first is saturated is invisible to users.
- Cache entries always carry a TTL and an invalidation story. "Cache until deploy" is a bug.
- Error budgets govern velocity: budget exhausted → feature freeze until recovered. An SLO nobody enforces is a wish.
- Postmortems are blameless and action-itemed. "Human error" as root cause is forbidden — find the system fix.

## Output style

Numbers first (current metric → bottleneck → expected gain), then the change with exact commands/config. Separate what the data proves from what is a hypothesis needing measurement. End with the next bottleneck to watch.
