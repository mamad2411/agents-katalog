---
name: incident-triage
description: Classify a supplied service alert using the supplied versioned runbook and return a cited draft-only JSON result.
---

# Incident triage

Read only `samples/alert.json` and `samples/runbook.md`.

1. Preserve `alert_id` exactly.
2. Compare every supplied metric with the explicit runbook thresholds.
3. Choose one of `SEV1`, `SEV2`, or `SEV3`; do not invent a threshold.
4. Cite the metric IDs and `runbook:runbook-v3` in `evidence_ids`.
5. Propose at least two approved diagnostic checks.
6. State uncertainty or missing evidence explicitly.
7. Do not claim that a service was restarted, a ticket submitted, or a notification sent.

Return JSON only:

```json
{
  "alert_id": "ALT-2048",
  "service": "checkout-api",
  "severity": "SEV2",
  "reason": "one concise threshold-based explanation",
  "evidence_ids": ["metric:p95_latency_ms", "metric:error_rate_pct", "runbook:runbook-v3"],
  "recommended_checks": ["check 1", "check 2"],
  "ticket_draft": {"summary": "draft summary", "submitted": false},
  "action_performed": false
}
```
