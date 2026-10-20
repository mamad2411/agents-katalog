# Staging Sign-Off

## Purpose
Produces a go/no-go recommendation for the Release Manager based on all Staging phase results.

## Role
QA Engineer

## Phase
Staging

## Triggered By
`performance-testing`, `stress-testing`, `zap-full-scan`, `semi-automated-pentest`, and combined `regression-testing` all complete.

## Inputs
- Performance/stress test results
- ZAP full scan + pentest results
- Combined regression test results
- Documentation spot-check from Technical Writer

## Process
Produce Green (GO) recommendation when:
- All SLAs met in `performance-testing`
- Stress test shows acceptable breaking point
- No critical/high security findings from ZAP
- Regression test suite passing
- Documentation spot-checked by Technical Writer

No-go → escalate to Edward with specific blocking reason.

## Outputs
Go/no-go recommendation to Release Manager.

## Quality Gates
- [ ] All five conditions checked explicitly
- [ ] No-go reasons are specific, not general
- [ ] Escalation raised to Edward on no-go

## References
- `.claude/skills/qa-engineer/performance-testing/SKILL.md`
- `.claude/skills/qa-engineer/stress-testing/SKILL.md`
- `.claude/skills/security-engineer/zap-full-scan/SKILL.md`
- `.claude/skills/shared/escalation-to-owner/SKILL.md`
