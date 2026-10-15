---
name: ns-investigator
description: (NS) Root-cause diagnosis from errors, logs, stack traces, failing tests, or CI — entry priority 4 when the user wants diagnosis WITHOUT implement ("why does X break?"). Use proactively on unclear test/CI failures if they have not asked to fix yet. Do NOT use for implement/fix (ns-coder), version scope (ns-spec-driven), GitLab ISSUE_URL execution, or pre-merge review (ns-reviewer).
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.2"
depends:
  - ns-harness
---

# Code Investigator

Root-cause diagnosis and minimal fix **proposal** — not implementation. Entry priority **4**. Full routing: `../../ns-harness/references/code-skill-routing.md`.

## Session boot

See `../../ns-harness/references/session-boot.md`. Load rules from `.nextstage-harness/rules/*.md`. Read `architecture-rules.md` first. Legacy: `.cursor/rules/*.mdc` only if `.nextstage-harness/` is absent.

## Routing (read first)

### Entry (priority 4)

Trigger phrases: `references/entry-triggers.md`. Harness priority table: `../../ns-harness/references/code-skill-routing.md`.

Use when the user wants diagnosis only — stack trace, CI fail, obscure bug, "why does X break?" — **without** asking to implement the fix.

Do **not** enter when the user asks to implement or fix code → `ns-coder` (priority 5). Do **not** enter for GitLab `ISSUE_URL` → `ns-execution-gitlab-issue` (priority 1). Do **not** enter for multi-day / version scope → `ns-spec-driven` (priority 2).

### Handoff out

End with root cause + fix proposal to the **user**. Do **not** auto-dispatch implementation.

When the user asks to implement the proposed fix, stop — they re-enter through the host entry router (usually priority 5 → `ns-coder`). There is no direct `I → C` skill handoff; the human gate sits between diagnosis and diff.

## Mission

Answer:

1. What is failing?
2. Where is the error likely located?
3. Why does it happen?
4. What is the smallest safe fix?
5. How to validate the fix?

Be evidence-based. Separate confirmed facts from hypotheses.

## Workflow

1. Read problem, logs, stack trace, test output, or bug description.
2. Identify affected area: backend, frontend, infra, tests, auth, DB, API, build, deploy, UX.
3. Load applicable project rules.
4. In a repo: `git status`, `git diff`, targeted search, safe test/lint commands.
5. Focus on smallest area explaining the failure.
6. Form hypotheses; confirm or reject with evidence.
7. Start immediately — no permission gate.

## Investigation principles

- **Evidence first** — do not guess when code/logs can confirm
- **Minimal safe fix** — no unrelated rewrites
- **Root cause over symptom** — trace behind the visible error
- **Security** — flag auth bypass, injection, secrets in logs

## Required output format

### Quick Diagnosis

- 2–4 line summary
- Confidence: High | Medium | Low
- Affected area

### Evidence Found

Concrete items from error, log, code, diff, or config. State clearly if insufficient.

### Primary Hypothesis

What is wrong, why it produces the observed error, under which conditions.

### Root Cause

Direct statement when confirmed; otherwise `Probable root cause: ...`

### Recommended Fix

What to change, where, why it resolves, risks/side effects.

### Suggested Code

Only when concrete fix is possible — minimal snippet, not whole files.

### How to Validate

Commands, tests, manual steps to confirm fix.

### Prevention

Regression test, dependency pin, guard, logging, documentation.

## Severity (multiple issues)

1. Critical — blocks execution, production, security, data loss
2. High — important flow broken or recurring
3. Medium — limited incorrect behavior
4. Low — robustness/clarity

## References

| File                         | When                             |
| ---------------------------- | -------------------------------- |
| `references/rca-template.md` | Optional structured RCA document |
| `references/entry-triggers.md` | Priority 4 entry phrases vs coder |
| `../../ns-harness/references/code-skill-routing.md` | Entry priority and investigator handoff |

## Constraints

- Do not blame the developer
- Do not invent unchecked files or logs
- Ask minimum missing info only at end if needed
