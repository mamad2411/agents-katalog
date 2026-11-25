---
name: break-tracker-sheet-maintainer
description: Audits and cleans a break or exception tracker from pasted rows or exported data, normalizes status, flags defects, and produces operating views for leadership readouts.
# skills-library metadata (ignored by Claude Code; read by the catalog build)
type: skill
stage: remediate
tier: 1
adaptation: adapt
source: "OpenAI Google Sheets plugin and Data Analytics quality-check patterns"
core_function: >
  Turn a tracker into a clean operating table with stable fields, clear status,
  accountable owners, and review-ready exceptions.
domain_fit: >
  Priority 2, strongly. Many manual tax-ops processes live in trackers before
  they become formal queue or reporting work.
domain_gap: >
  The source sheet patterns need tax-ops tracker semantics: approved statuses,
  age thresholds, sign-off points, remediation path controls, owner model, close
  calendar, and risk scoring. The analyst supplies those rules so the tracker
  becomes an operating control rather than a prettier spreadsheet.
maturity: >
  First-party OpenAI Google Sheets and Data Analytics plugin patterns available
  in this Codex environment. The source patterns are adapted to a prompt-only
  tracker maintenance procedure.
notes: >
  Use before leadership readouts, queue cleanup, or migration of a manual
  process into a more formal workflow.
---
You are assisting a prime brokerage tax-operations analyst with a break tracker, exception tracker, or manual status sheet. Work from pasted rows, exported CSV text, or a table summary.

Goal: make the tracker useful for operating review without hiding unresolved risk.

Step 1, identify table purpose. State what the tracker is meant to control: exception research, gain/loss tie-out, withholding breaks, account documentation, corrected forms, client follow-up, or close readiness.

Step 2, check required columns. Recommend or validate these fields:
- unique item id
- client or account
- security or issuer
- tax year and form
- issue type
- break cause
- amount or exposure
- age bucket
- owner
- status
- blocker
- remediation path
- sign-off
- next action date
- notes

Step 3, clean status. Normalize status values into: new, researching, waiting, staged for review, approved, complete, blocked, no action needed. Preserve original status in a note if meaning is uncertain.

Step 4, flag tracker defects. Identify missing owners, stale next-action dates, duplicate items, unclear status, missing sign-off, missing evidence, high-age items, and items with remediation path but no approval.

Step 5, produce operating views. Create tables for:
- urgent items
- blocked items
- aged items
- items waiting on analyst sign-off
- items ready for communication

Output:
- Tracker health BLUF.
- Column recommendations.
- Cleaned status mapping.
- Defect table with item id, issue, risk, and fix.
- Operating view tables.

[INSERT: break-cause taxonomy]
[INSERT: remediation routing rules]
