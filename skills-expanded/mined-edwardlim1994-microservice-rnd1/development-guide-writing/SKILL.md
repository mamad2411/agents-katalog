# Development Guide Writing

## Purpose
Writes rich reference documentation for developers, complementing (not replacing) CLAUDE.md and README.md.

## Role
Technical Writer

## Phase
Cross-phase (triggered by convention changes from retro improvement actions)

## Triggered By
Retrospective improvement actions identify documentation gaps.

## Inputs
- Retro improvement action identifying the gap

## Rule
Complements CLAUDE.md (agent-facing) and README.md (quick start). Does NOT replace CLAUDE.md or README.md.

## Process
Write rich reference documentation for developers:
- Detailed setup guide with screenshots/diagrams
- Generator usage examples
- Common patterns and anti-patterns
- Debugging guides
- Environment setup troubleshooting

## Outputs
Location: `apps/docs/src/content/internal/latest/development/`

## Quality Gates
- [ ] Content complements, not duplicates, CLAUDE.md/README.md
- [ ] Addresses the specific gap identified in the retro action
- [ ] Includes concrete examples, not just prose

## References
- `.claude/skills/po/retrospective-conclusion/SKILL.md`
- `.claude/skills/technical-writer/docs-site-management/SKILL.md`
