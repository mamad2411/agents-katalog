# User Flow Definition

## Purpose
Maps the logical sequence of screens/states for a user story, independent of visual design.

## Role
UI/UX Designer

## Phase
Planning (Stage 4)

## Triggered By
Stage 3 complete.

## Inputs
- Story AC
- Architect's `story-diagram-design` flowchart (if relevant)

## Process
1. Map entry point, each screen/state, user decisions, and exit points for the story.
2. Show logical sequence only — not visual layout, specific UI components, or colours.
3. Write as MermaidJS flowchart.
4. Add file header with Story reference.

## Outputs
Location: `openspec/changes/{slug}/diagrams/{slug}-user-flow.md`

File header must include `Story: #{issue-number}` reference.

## Quality Gates
- [ ] Entry point, all screens/states, decisions, and exit points shown
- [ ] No visual layout or component detail included
- [ ] MermaidJS flowchart format used
- [ ] Story reference in file header

## References
- `.claude/skills/ui-ux-designer/interaction-specification/SKILL.md`
- `.claude/skills/solution-architect/story-diagram-design/SKILL.md`
