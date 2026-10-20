# Rollback Execution

## Purpose
Decides and initiates emergency rollback in response to a production issue.

## Role
Release Manager

## Phase
Release (emergency response)

## Triggered By
`post-release-monitoring` detects an issue, or Edward instructs a rollback.

## Inputs
- Post-release monitoring findings or Edward's instruction

## Process
1. Release Manager decides whether rollback is needed.
2. Create rollback kanban card:
   - type: `hotfix`, priority: `critical`
   - Body: what failed, target rollback version (`v{X}.{Y}.{Z-1}`), database migration rollback needed (yes/no and why), communication plan
3. DevOps executes rollback against this ticket.
4. After rollback: verify system stable in Grafana.
5. Root cause investigation → new bug card for next sprint.

## Outputs
Rollback kanban card created; DevOps executes; system verified stable.

## Quality Gates
- [ ] Rollback decision made by Release Manager (documented)
- [ ] Kanban card includes target version and migration rollback need
- [ ] System verified stable in Grafana after rollback
- [ ] Root cause bug card created for next sprint

## References
- `.claude/skills/release-manager/post-release-monitoring/SKILL.md`
- `.claude/skills/devops-engineer/rollback-deployment/SKILL.md`
