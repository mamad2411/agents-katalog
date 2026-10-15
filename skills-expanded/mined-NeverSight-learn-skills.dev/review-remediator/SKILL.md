---
name: review-remediator
description: Verify review or audit findings and fix confirmed issues
---

# Review Remediator

Read the review text the user provides (from other agents, not the user's own opinion), cross-check each finding against the actual source files, and apply targeted fixes. Small, safe fixes proceed automatically; large or risky changes require user confirmation.

## Focus Areas

- Parse review text (markdown, bullet list, log output, or free-form) and identify each issue
- Locate referenced files; search the repo if paths are partial or ambiguous
- Verify issues against actual code; skip false positives or stale line numbers
- Auto-fix small, low-risk changes (roughly <= 5 lines, no logic deletion)
- Escalate large, complex, or sensitive fixes (auth, crypto, payment, API changes) for approval
- Generate a concise summary of what was fixed, skipped, or pending

## Guardrails

- Keep behavior unchanged unless fixing a confirmed issue.
- Prefer minimal, focused edits over broad rewrites.
- Do not guess if an issue is ambiguous; ask the user for clarification.
- Never modify read-only or generated files without explicit permission.
- Keep the final summary concise (1-3 sentences or a short table).
