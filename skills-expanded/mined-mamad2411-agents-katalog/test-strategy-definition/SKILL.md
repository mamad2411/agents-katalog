# Test Strategy Definition

## Purpose
Determines which test types apply to a story and evaluates regression impact on existing flows.

## Role
QA Engineer

## Phase
Planning (Stage 2)

## Triggered By
`acceptance-criteria-challenge` complete.

## Inputs
- Tightened AC
- Existing flows the story may touch

## Process
1. Determine test types needed: unit, component integration, frontend interaction, e2e.
2. Evaluate regression impact: does story touch existing flows?
3. If yes, produce regression impact matrix:
   - Location: `openspec/changes/{slug}/regression-impact-matrix.md`
   - Format: `Story touches {service} {method} → regression scope: {test suites}`
4. Test-infrastructure-awareness checkpoint: verify `test/e2e/`, `test/smoke/`, `test/zap/` directories ready for this story.

## Outputs
Test strategy (types needed) and regression impact matrix (if applicable).

## Quality Gates
- [ ] Test types identified for the story
- [ ] Regression impact matrix produced when existing flows touched
- [ ] Test infrastructure readiness confirmed

## References
- `.claude/skills/qa-engineer/acceptance-criteria-challenge/SKILL.md`
- `.claude/skills/qa-engineer/regression-testing/SKILL.md`
