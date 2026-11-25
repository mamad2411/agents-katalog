---
name: cross-source-correlation
description: Correlate near-in-time events across PR merges, deploys, monitoring (Sentry/NewRelic/Datadog/AppDynamics) and ticket trackers (Jira/Azure DevOps) into confidence-scored clusters that answer "which deploy caused this bug" without manual tab-switching.
tags: [observability, incident-response, correlation, ai-agent, devops]
publisher: agena
---

# Cross-Source Correlation

When a Sentry alert fires, a senior engineer mentally cross-references the
last deploy time, recent PRs, NewRelic apdex, and the support tickets
opened in the last hour. AGENA's Cross-Source Correlation engine does the
same correlation deterministically, producing a single confidence-scored
cluster per incident.

## How to apply this pattern

1. **Pick a time window** (default 60 minutes ending now) and pull every
   event your platform observed inside it: PR merges, deploys, error
   imports (Sentry / NewRelic / Datadog / AppDynamics), and work-item
   imports (Jira / Azure DevOps).

2. **Score candidate clusters** using a heuristic that rewards co-location
   in time + repo:
   - PR merge inside the window → `+40`
   - Deploy from the same repo inside the window → `+20`
   - One monitoring signal in the window → `+20` (`+30` if more than one)
   - One work-item opened in the window → `+10` (`+20` if more than one)
   - Bonus `+10` when a PR is present alongside any monitoring signal

3. **Surface only clusters ≥ 70**. Below that the noise / signal ratio
   collapses; above it you get the "vay" moment for incident triage.

4. **Persist the cluster** with: `primary_kind`, `primary_label`,
   `related_events[]`, `confidence`, `severity`, `narrative`,
   `repo_mapping_id`. Keep a `fingerprint` for idempotency so repeated
   poller runs don't double-insert the same cluster.

5. **Offer triage actions** on each cluster: confirm, false-positive,
   undo, and (when a PR is the prime suspect) one-click rollback.

## Example

```
🔴 CRITICAL · confidence 94%

PR #4519 (erinc, merged 14:18) in checkout-api correlates with
2 monitoring signal(s) (sentry, newrelic) and 1 work-item opened
in the same window.

Timeline:
  14:18  🔀 PR #4519 merged — payment_service.py, +47/-12
  14:18  🚀 deploy a1b2c3d4 → production
  14:23  🚨 Sentry: TypeError in payment_service.py:88 (47×)
  14:24  📡 NewRelic: apdex 0.92 → 0.41
  14:31  🪐 Jira SUP-128 opened — 12 customers report failed checkout
```

## Notes

- Run as a background poller every ~5 minutes on a fresh window — no
  webhook fan-out needed when you control all the sources.
- Sub-70 clusters can still be useful for trending dashboards even if you
  don't want to surface them as actionable.
- Store the cluster's narrative as a one-sentence summary (LLM-generated
  off the timeline) so it's readable in Slack alerts and post-mortem docs.
- Designed to be agnostic to specific monitoring backends — add a new
  source by writing a single mapper that emits `(timestamp, kind, ref,
  label)` rows into the same window query.
