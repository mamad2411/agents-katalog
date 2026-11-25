# Integration Test Case Design

## Purpose
Designs backend service-to-service test cases based on the Architect's sequence diagram.

## Role
QA Engineer

## Phase
Planning (Stage 6) + Development (implementation in `qa/` branch)

## Triggered By
Stage 6 begins; Architect's sequence diagram available.

## Inputs
- Architect `story-diagram-design` sequence diagram

## Process
1. Read the story's sequence diagram to identify service-to-service calls.
2. Design test cases covering each call path, including error/failure modes.
3. Implement using Vitest against real services in local dev or SIT; mock external dependencies only.
4. Raise branch `qa/{KAN-N}` from `feat/{KAN-N}`.

## Outputs
- Design: `openspec/changes/{slug}/test-cases/integration/`
- Test files: `apps/servers/{service}/test/integration/`

## Quality Gates
- [ ] Test cases cover all service-to-service call paths from sequence diagram
- [ ] Real services used (not mocked) except external dependencies
- [ ] Tests implemented on qa/{KAN-N} branch

## References
- `.claude/skills/solution-architect/story-diagram-design/SKILL.md`
- `.claude/skills/qa-engineer/e2e-test-case-design/SKILL.md`
