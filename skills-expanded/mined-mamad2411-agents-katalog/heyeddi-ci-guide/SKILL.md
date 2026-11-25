---
name: heyeddi-ci-guide
description: Reference for HeyEddi CI commands, authorize-merge auth, feedback via debate + support@, and Spot runners placeholder status. Use when asking how to work with HeyEddi CI.
version: 1.1.0
product-version: 3.4.2
author: HeyEddi-com
---

# HeyEddi CI Guide

Short reference for agents and humans working with **HeyEddi CI**. Depth lives in `reference/commands.md`.

## Skills in this pack

| Skill | Job |
|-------|-----|
| `@heyeddi-ci-config` | Author `eddi-ci.yaml` from the live policy contract |
| `@heyeddi-pr-respond` | Address all PR review feedback (human + HeyEddi CI) |
| `@heyeddi-ci-fails` | Diagnose and fix failing Checks (default on PR work; `/heyeddi fails` for App path) |
| `@heyeddi-ci-runners` | PLACEHOLDER: declare `pipeline:` YAML; Spot fail-closed |
| `@heyeddi-ci-guide` | This skill |

Human PR review stays on `@heyeddi-pr-review` / `@heyeddi-pr-respond`.

## Default PR workflow

On any PR work (open PR, PR branch, review request):

1. **Always** run `@heyeddi-ci-fails` first — fetch failing Checks, diagnose, fix actionable failures, commit + push
2. **Always** run `@heyeddi-pr-respond` — fix all review items, commit + push, post every reply in-thread
3. **Never** ask "do you want me to fix?" or "should I comment on threads?" — that is always the default
4. **Never** skip CI because the user did not mention it
5. Only **merge** requires **authorize merge** in the current turn

## Commands (PR comments)

See `reference/commands.md`. Common:

- `/heyeddi review` / `again` / `check` / `deep` — review passes
- `/heyeddi ci` / `/heyeddi fails` — failed Checks analysis (billable path)
- `/heyeddi ask …` / `/heyeddi debate …` — Q&A on findings
- Reply on an inline HeyEddi finding — debate when parent looks like HeyEddi

## Auth matrix

| Action | Allowed when |
|--------|----------------|
| Commit + push (PR workflow) | Automatic during `@heyeddi-ci-fails` / `@heyeddi-pr-respond` — do not ask |
| Merge (`gh pr merge`) | User says **authorize merge** in the **current turn** |
| `auto_merge` in YAML | Never (schema rejects / forbidden) |
| Billable knobs (`on_ci_failure`, runners) | Explicit opt-in |

## Feedback (real paths only)

There is **no** structured FP/telemetry API yet.

1. Disagree on a finding: `/heyeddi ask` / debate on that thread
2. Product or skill feedback: `support@heyeddi.com` (skills may draft a mail body)

## Runners status

Spot / isolated runners are **PLACEHOLDER / fail-closed**. Skills may author valid `pipeline:` YAML; never claim jobs ran. See `@heyeddi-ci-runners`.

## Install

```bash
npx skills add HeyEddi-com/heyeddi-skills -a cursor -y --skill '*'
# or CI skills by name / Marketplace plugin heyeddi-ci-skills
# or Team Marketplace plugin heyeddi-ci-skills
```

## Tools

None (`tools: []`). This skill is documentation only.

## Notes

- Living knobs: always `@heyeddi-ci-config` → `load_policy_contract`
- Ephemeral `.heyeddi/docs/pr-*` scratch: never commit
