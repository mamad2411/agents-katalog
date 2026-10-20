---
name: check-secrets
description: Check secrets hygiene — env vars, hardcoded values, and leaks via workflows
argument-hint: "[domain]"
related:
  - follow-secret-manager
  - deep-review-codebase
  - report
  - ask-me

---

## Goal

Dispatch to a workflow by secrets-check domain — the parent only routes

## Scope

- The argument is the domain; if omitted → `/ask-me` to pick a domain

## Execute

### Workflows

| Domain | Workflow |
|---|---|
| `env-vars` | `workflows/env-vars/SKILL.md` — compares `.env` vs `.env.example` vs code usage |
| `hardcoded-values` | `workflows/hardcoded-values/SKILL.md` — hardcoded values that should move to config/env |
| `secrets-leak` | `workflows/secrets-leak/SKILL.md` — secrets leaked in code/config/history |
| `report`, `inventory` | `workflows/report-inventory/SKILL.md` — secrets inventory report with redaction |

1. Resolve the domain from the argument (e.g. `/check-secrets secrets-leak`)
2. If the domain is supported → follow `workflows/<domain>/SKILL.md` through the whole flow
3. If the domain is missing or unknown → `/ask-me` to pick a domain

## Rules

- The parent only dispatches — never duplicate a workflow's content
- Never echo actual values of found secrets — report only location + type

- Use /follow-secret-manager if needed
- Use /deep-review-codebase if needed

## Expected Outcome

- The caller is dispatched to the workflow matching the domain and runs the secrets check per that flow
