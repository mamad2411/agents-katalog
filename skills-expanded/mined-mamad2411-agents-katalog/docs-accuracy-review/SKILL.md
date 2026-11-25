# Docs Accuracy Review

## Purpose
Spot-checks the highest-risk documentation against the real UAT environment before release.

## Role
Technical Writer

## Phase
UAT (spot-check before release)

## Triggered By
UAT environment ready, before staging deployment.

## Inputs
- UAT environment
- Recently changed docs (new endpoints, changed schemas, new runbooks)

## Process
Spot-check key docs against the UAT environment:
- Does the API reference match what the endpoint actually returns?
- Do runbooks execute successfully against a real environment?
- Are schema docs accurate for the deployed version?

Focus: highest-risk docs only (new endpoints, changed schemas, new runbooks). Not exhaustive — targeted spot-check.

Inaccuracies found → update docs before release, notify Tech Lead.

## Outputs
Verified or corrected documentation before release; Tech Lead notified of any inaccuracies found.

## Quality Gates
- [ ] Highest-risk docs identified and checked
- [ ] Checks performed against real UAT environment, not assumptions
- [ ] Inaccuracies corrected before release
- [ ] Tech Lead notified when inaccuracies are found

## References
- `.claude/skills/technical-writer/api-reference-documentation/SKILL.md`
- `.claude/skills/technical-writer/runbook-writing/SKILL.md`
- `.claude/skills/qa-engineer/uat-deployment-verification/SKILL.md`
