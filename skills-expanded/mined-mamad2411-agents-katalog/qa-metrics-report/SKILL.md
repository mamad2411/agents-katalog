# QA Metrics Report

## Purpose
Produces a data-driven QA metrics report for the retrospective session.

## Role
QA Engineer

## Phase
Retrospective

## Triggered By
`/metrics` command.

## Inputs
- UAT and Staging results from the sprint
- SonarQube trend data from `sonarqube-monitoring`

## Process
Report is data-driven — specific numbers, no opinions.

Reports:
- UAT: bug count, acceptance pass rate, regression pass rate, avg UAT cycles/story
- Staging: performance baselines vs previous sprint, stress test results, resource cost estimate, resource ceiling type
- SonarQube trends: coverage delta, issue categories
- Improvement suggestions (specific, data-backed with root cause)

Suggestions go to backlog via PO `retrospective-conclusion`.

## Outputs
Contributes to Sections 3, 4 of `retro-template.md`.

## Quality Gates
- [ ] All metrics are actual counts, not estimates
- [ ] Delta vs previous sprint calculated
- [ ] Improvement suggestions specific and data-backed
- [ ] Report ready before /retro session begins

## References
- `.claude/skills/pm/retrospective-facilitation/SKILL.md`
- `.claude/skills/qa-engineer/sonarqube-monitoring/SKILL.md`
- `openspec/retro-template.md`
