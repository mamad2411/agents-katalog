# Rollback Deployment

## Purpose
Executes a rollback to a prior release version against a Release Manager rollback ticket.

## Role
DevOps Engineer

## Phase
Release (emergency response)

## Triggered By
Release Manager creates a rollback kanban card.

## Inputs
- Rollback kanban card (target release tag, migration rollback needed)

## Process
1. Identify target rollback version from kanban card.
2. ArgoCD rollback to specified release tag (same image, no rebuild).
3. If schema migration needed: run Prisma down migration.
4. Wait for all pods healthy.
5. Run smoke tests to verify rollback successful.
6. Check Grafana: error rates returning to baseline.
7. Update rollback kanban card: complete + verification status.

## Outputs
System rolled back to target version; kanban card updated with verification status.

## Quality Gates
- [ ] Correct target version identified from kanban card
- [ ] Same image used, no rebuild
- [ ] Down migration run if needed
- [ ] Smoke tests and Grafana error rate confirm successful rollback
- [ ] Kanban card updated with outcome

## References
- `.claude/skills/release-manager/rollback-execution/SKILL.md`
- `.claude/skills/backend-developer/database-migration/SKILL.md`
