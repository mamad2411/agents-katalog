---
name: reviewer-handoff
description: Structured review summary format with verdict logic and coverage scoring.
usedBy: [reviewer]
version: 0.2.0
lastUpdated: 2026-09-12
---

## Purpose

This skill defines the output format for review handoffs — the structured summary a Reviewer delivers after inspecting work. The progress file (`.memory/reviews/review-<type>-<timestamp>.md`) contains the full findings trail. The handoff adds the verdict and planned commits on failure.

## Procedure

1. **Assemble the handoff** using the template below. The progress file path is required — it contains all findings.

```markdown
## Review Summary

**Verdict:** <pass | partial-pass | fail>
**Type:** <code | architecture | documentation | configuration | other>
**Progress file:** <path to review progress file>

## SHIELD Self-Review Scorecard
[Complete the scorecard from `skills/reviewer-self-review/SKILL.md`]
```

2. **Determine the verdict.**
   - `pass` — zero blockers and all review phases completed.
   - `partial-pass` — zero blockers but a review phase was skipped (e.g., external tool unavailable).
   - `fail` — one or more blockers.

3. **Append planned commits on failure.** When the verdict is `fail` and the type is `code`, add a "Planned Commits" section after the summary. Write conventional-commit messages (follows: `rules/git.md`) for each requested fix. This gives the next step ready-made commit messages once the fixes land.

## Guardrails

- Never omit the Progress file reference — it contains the full analysis trail and is required on every review.
