# Compliance Code Review

## Purpose
Reviews the story branch as a whole for implementation of compliance and security requirements before PM adds the `uat-ready` label.

## Role
Security Engineer

## Phase
Development (per story, BEFORE UAT)

## Triggered By
All tasks merged to story branch, PM ready to add `uat-ready` label.

## Inputs
- `openspec/changes/{slug}/prd.md` (compliance + security sections)
- Full story branch diff

## Gate
Security Engineer must clear story BEFORE PM adds `uat-ready` label.

## Process
1. Read compliance requirements from `openspec/changes/{slug}/prd.md`.
2. Read security requirements from prd.md security section.
3. Review story branch (not individual task PRs — the whole branch):
   - Auth interceptors applied to all new gRPC methods?
   - PII fields handled correctly (masked in logs, encrypted at rest)?
   - Input validation present on all user-controlled fields?
   - Error responses don't leak sensitive information?
   - Logging sanitised (no passwords, tokens, PII in logs)?
4. If all pass: update story kanban card → `security: cleared`. Signal PM: cleared for UAT.
5. If issues found: create bug kanban card per issue, `type: bug-story`, `area: security`. Block `uat-ready` label until fixed.

## Outputs
`security: cleared` label, or bug cards blocking UAT.

## Quality Gates
- [ ] All compliance requirements verified against implementation
- [ ] Auth interceptors confirmed on all new endpoints
- [ ] No PII in logs verified
- [ ] security: cleared label applied (or bugs filed)

## References
- `.claude/skills/pm/prd-writing/SKILL.md`
- `.claude/skills/pm/kanban-board-management/SKILL.md`
