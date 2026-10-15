---
name: support-sla-breach-detector
description: Vendor-neutral skill for detecting support-ticket SLA breaches from exported ticket timelines.
---

## When to invoke
- You have a CSV export of support tickets with timestamps (created, first response, resolved).
- You want to identify tickets that violated response or resolution SLAs.
- You need a vendor-neutral report that can work with exports from many helpdesk tools.

## Inputs needed
- CSV file with at least: `ticket_id`, `priority`, `created_at`, `first_response_at`, `resolved_at`.
- SLA thresholds (minutes) per priority for first response and resolution.

## Workflow
1. Load CSV and parse ISO timestamps.
2. For each ticket, compute:
   - minutes to first response
   - minutes to resolution
3. Compare against SLA thresholds by priority.
4. Emit:
   - list of breached tickets
   - breach reason (response, resolution, both)
   - aggregate counts by priority

## Output format
- JSON report written to a path.
- Human-readable summary printed to stdout.

## Guardrails
- Assume timestamps are in a consistent timezone; do not guess missing timezone.
- If a timestamp is missing, mark metric as `null` and do not treat as breach unless instructed.

## Reference code
- `support_sla_breach_detector.py`
