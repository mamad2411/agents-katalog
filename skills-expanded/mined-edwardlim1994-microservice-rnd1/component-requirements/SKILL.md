# Component Requirements

## Purpose
Specifies structural component requirements per screen — what components are needed, not how they look.

## Role
UI/UX Designer

## Phase
Planning (Stage 4)

## Triggered By
`interaction-specification` complete.

## Inputs
- `interaction-specification` output

## Process
1. For each screen, specify which UI components are needed (form, table, modal, etc.).
2. Specify what each component contains — not visual appearance.
3. Document for consumption by Frontend/Mobile developers before implementation.

## Outputs
Component requirement list per screen, consumed by Frontend/Mobile developers.

## Quality Gates
- [ ] Every screen from interaction-specification has component requirements
- [ ] No visual appearance detail included
- [ ] Requirements are structural (component type + contents) only

## References
- `.claude/skills/ui-ux-designer/interaction-specification/SKILL.md`
- Frontend/Mobile developer skills
