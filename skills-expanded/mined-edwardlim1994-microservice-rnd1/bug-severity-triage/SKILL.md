# Bug Severity Triage

## Purpose
Classifies bugs found during UAT and Staging into blocking vs backlog severity.

## Role
QA Engineer

## Phase
UAT + Staging

## Triggered By
Any bug found during acceptance, regression, performance, or stress testing.

## Inputs
- Bug details from the finding skill

## Process

### Critical/High (fix immediately, current sprint)
- Blocks core functionality
- SonarQube critical/high/medium findings
- Any security finding
- Any compliance violation

### Low/Non-blocking (backlog)
- Minor UX issues, cosmetic problems, SonarQube low/info

Bug card must include: steps to reproduce, expected vs actual, environment, severity, area.
External-facing bugs → also file in external issue tracker.

## Outputs
Severity-classified bug kanban card.

## Quality Gates
- [ ] Severity classified per criteria above
- [ ] Bug card includes repro steps, expected vs actual, environment
- [ ] External-facing bugs filed in external tracker

## References
- `.claude/skills/qa-engineer/acceptance-testing/SKILL.md`
- `.claude/skills/pm/issue-triage/SKILL.md`
