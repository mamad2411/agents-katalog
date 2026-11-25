# SonarQube Monitoring

## Purpose
Passively observes SonarQube dashboard during the sprint, flagging systemic patterns without reviewing individual PRs.

## Role
QA Engineer

## Phase
Development (passive)

## Triggered By
Sprint in progress — continuous observation.

## Inputs
- SonarQube dashboard/metrics

## Process
1. Observe SonarQube dashboard during sprint.
2. Do NOT review individual PRs.
3. Flag to Tech Lead if systemic patterns emerge across multiple PRs.
4. Collect quality metrics for `qa-metrics-report`.

No active intervention — observation and trend detection only.

## Outputs
Systemic pattern flags to Tech Lead; quality metrics for reporting.

## Quality Gates
- [ ] Dashboard observed continuously through sprint
- [ ] No individual PR reviews performed under this skill
- [ ] Systemic patterns flagged to Tech Lead when found
- [ ] Metrics collected for qa-metrics-report

## References
- `.claude/skills/qa-engineer/qa-metrics-report/SKILL.md`
