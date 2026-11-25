# Frontend Interaction Test Design

## Purpose
Tests functional presence and behaviour of frontend elements — not visual layout.

## Role
QA Engineer

## Phase
Planning (Stage 4) + Development (implementation in `qa/` branch)

## Triggered By
Stage 4 begins, in parallel with UI/UX Designer.

## Inputs
- Story AC (primary)
- Wireframe (secondary — element discovery only)

## Process
1. Use AC as the primary input; use wireframe only to discover elements, never for layout.
2. Design tests validating:
   - Required fields exist
   - Correct input types
   - Validation rules trigger
   - Submit fires correct Apollo operation
   - Success/error feedback displays
   - Loading states work
   - Navigation occurs correctly
3. Explicitly do NOT validate layout, colours, spacing, animations, fonts.
4. Implement using Vitest + React Testing Library + MSW (Mock Service Worker).
5. Raise branch `qa/{KAN-N}` from `feat/{KAN-N}`.

## Outputs
Frontend interaction test suite on `qa/{KAN-N}` branch.

## Quality Gates
- [ ] Every AC maps to at least one interaction test
- [ ] No visual/layout assertions included
- [ ] Apollo operations and feedback states covered
- [ ] Tests implemented with Vitest + RTL + MSW

## References
- `.claude/skills/ui-ux-designer/interaction-specification/SKILL.md`
- `.claude/skills/qa-engineer/acceptance-criteria-challenge/SKILL.md`
