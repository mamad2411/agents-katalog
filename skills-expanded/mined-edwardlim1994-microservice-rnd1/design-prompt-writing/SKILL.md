# Design Prompt Writing

## Purpose
Translates the interaction specification into a detailed prompt for an external design tool.

## Role
UI/UX Designer

## Phase
Planning (Stage 4, written LAST after all other specs complete)

## Triggered By
`interaction-specification`, `component-requirements`, and `accessibility-requirements` complete.

## Inputs
- `interaction-specification`
- `component-requirements`
- `accessibility-requirements`

## Process
Compatible with: Figma AI, Claude Design, OpenDesign.

Prompt must include:
- Layout intent (not pixel values — general structure)
- Component types needed (form, table, modal, navigation)
- User flows and state transitions
- Accessibility requirements
- Brand/style context if available

## Outputs
`design-prompt.md` in `openspec/changes/{slug}/`

## Quality Gates
- [ ] Written after all other Stage 4 specs complete
- [ ] Includes layout intent, components, flows, accessibility, brand context
- [ ] No pixel-level values specified

## References
- `.claude/skills/ui-ux-designer/interaction-specification/SKILL.md`
- `.claude/skills/ui-ux-designer/component-requirements/SKILL.md`
- `.claude/skills/ui-ux-designer/accessibility-requirements/SKILL.md`
