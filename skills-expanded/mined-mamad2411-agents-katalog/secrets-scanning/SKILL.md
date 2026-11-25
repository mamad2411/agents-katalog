# Secrets Scanning

## Purpose
Monitors CI/CD secrets scanning results to detect committed secrets, API keys, tokens, or passwords.

## Role
Security Engineer

## Phase
Development (passive monitoring)

## Triggered By
New CI scan results available (DevOps wires GitLeaks/TruffleHog).

## Inputs
- CI scan reports from GitLeaks/TruffleHog

Note: DevOps wires the tool into CI (see `devops/secrets-scanning-pipeline-integration`). Security Engineer monitors results and interprets findings.

## Process
1. Review CI scan reports from GitLeaks/TruffleHog.
2. For any finding (always severity: critical):
   a. Create immediate kanban card: `type: task`, `priority: critical`
   b. Notify Tech Lead immediately
   c. Finding must be resolved before PR can merge
3. Track patterns: same developer repeatedly committing secrets? → Create knowledge-update card for next retro discussion.

## Outputs
Kanban cards for any secret findings; pattern tracking for retro.

## Quality Gates
- [ ] CI scan reports reviewed per sprint
- [ ] Any finding creates immediate critical kanban card
- [ ] Patterns tracked for retro improvement actions

## References
- `.claude/skills/devops/secrets-scanning-pipeline-integration/SKILL.md`
- `.claude/skills/pm/kanban-board-management/SKILL.md`
