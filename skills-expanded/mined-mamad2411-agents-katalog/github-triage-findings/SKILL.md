---
name: github-triage-findings
description: >-
  Decide WHICH findings become GitHub Issues and in what order/batches, working
  from a findings.json produced by github-extract-findings. Use this AFTER findings are
  extracted and BEFORE creating issues — especially when there are more findings
  than you want to file at once. Triggers on "start with the critical ones",
  "which should we file first", "don't dump everything into GitHub", "let's do
  this in batches/waves", "only the confirmed ones for now", "hold the
  needs-review items", "scope down the backlog", "prioritize these findings",
  or any request to pick a subset of findings to turn into issues. Produces a
  scoped, ordered subset and hands it to classify-github-issues.
effort: max
---

# github-triage-findings

You have a `findings.json` (from `github-extract-findings`). Filing every row blindly
creates a noisy, unprioritized backlog. This skill is the human-in-the-loop gate:
**show the shape of the findings, agree on a scope and order, emit a smaller set**,
then hand off to `classify-github-issues`. The win is an auditable *wave* structure.

This is a reasoning/filtering step — there is no script to run. You read JSON,
summarize, and write a smaller JSON.

## 1. Read and profile the findings

Show counts before asking anything:

- **by `severity`**: Critical / High / Medium / Low (and how many have none)
- **by `status`**: `confirmed` vs `needs-review` (bucket what you see)
- **by `section`**: which areas the findings cluster in
- **by `kind`** (optional): `rename` / `disambiguation` / `missing` / `other`

```
42 findings total
  severity: Critical 6 | High 14 | Medium 18 | Low 4
  status:   confirmed 30 | needs-review 12
  section:  Cargo Classification 19 | Port Calls 11 | Misc 12
```

## 2. Recommend a default, then follow the user's call

**Recommended default: `severity = Critical` AND `status = confirmed` first.**
Hold `needs-review` for a later verification pass — filing unconfirmed findings
creates issues you may have to close.

Ask one focused question: *"Start with the 6 Critical + confirmed as wave 1, and
hold the 12 needs-review for a verification pass? Or a different cut?"*

## 3. Order within the scope

Order: **Critical → High → Medium → Low**, `confirmed` before softer statuses.
Stable-sort within a tie by `section`. This ordering carries into `github_backlog_input.json`.

## 4. Emit the scoped subset

Write `findings.wave1.json` (preferred for clean waves) or annotate findings in place
with `"selected": true`. Preserve every original field verbatim — especially `key`.

```json
{
  "source": "Downloads/CRM_Audit.xlsx",
  "keyColumn": "#",
  "findings": [
    { "key": "1", "severity": "Critical", "status": "confirmed", "kind": "rename",
      "current": "Auto", "expected": "Automotive Cargo" }
  ]
}
```

## 5. Hand off

Report the wave (count, filter applied, file written) and tell the user the next step:
**`classify-github-issues`** turns this scoped set into `github_backlog_input.json`.
Note any held-back waves so they are not forgotten.

## Notes

- Keep waves small enough to review before the next wave. 5–15 items is usually right.
- If `findings.json` has no `severity`/`status`, triage on `section`/`kind` or count, and say so.
- Triage writes nothing to GitHub — creation happens in `github-create-issues`.
