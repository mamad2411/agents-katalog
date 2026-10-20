# UAT Deployment Verification

## Purpose
Verifies a story's UAT environment is fully ready before testing begins.

## Role
QA Engineer

## Phase
UAT

## Triggered By
ArgoCD deploys story to `uat-{KAN-N}.uat.internal`.

## Inputs
- UAT environment URL
- Data Engineer's seed confirmation

## Process
1. Verify all services running.
2. Verify endpoints reachable.
3. Verify test data seeded (confirm Data Engineer's seed ran correctly — do NOT seed data here).
4. Signal QA + PO: environment ready to begin testing.

## Outputs
Environment-ready signal to QA and PO.

## Quality Gates
- [ ] All services confirmed running
- [ ] All endpoints reachable
- [ ] Test data seed confirmed (not performed by this skill)
- [ ] QA + PO signalled

## References
- `.claude/skills/qa-engineer/test-data-strategy/SKILL.md`
- Data Engineer `test-data-seeding`
- `.claude/skills/qa-engineer/acceptance-testing/SKILL.md`
