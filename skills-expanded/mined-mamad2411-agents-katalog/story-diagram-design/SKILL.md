# Story Diagram Design

## Purpose
Produces MermaidJS diagrams per story to visualise business logic, service interactions, and data model changes.

## Role
Solution Architect

## Phase
Planning (Stage 3)

## Triggered By
`service-boundary-definition` complete for this story.

## Inputs
- Service boundaries and interactions for the story

## Diagram Requirements
- Flowchart: ALWAYS required — every story gets one
- Sequence diagram: required when story involves >1 service
- ERD: required when story creates, modifies, or deletes a data entity

### File Header Format (REQUIRED on every diagram file)
```
<!-- Story: #{issue-number} — {story-title} -->
<!-- Type: flowchart | sequence-diagram | erd -->
<!-- Generated: {date} -->
```

## Process
1. Create flowchart (always): shows user action → system steps → outcome. Format: MermaidJS `flowchart LR` or `TD`.
2. Create sequence diagram (if >1 service): shows which service calls which, in what order, via which protocol; shows gRPC calls, Kafka events, GraphQL queries explicitly. Format: MermaidJS `sequenceDiagram`.
3. Create ERD (if data entity changes): shows affected entities, their fields, their relationships, and which service owns each entity. Format: MermaidJS `erDiagram`.
4. Add GitHub Issue reference header to each file.
5. Commit to `openspec/changes/{slug}/diagrams/`.

## Outputs
- `openspec/changes/{slug}/diagrams/{slug}-flowchart.md`
- `openspec/changes/{slug}/diagrams/{slug}-sequence.md` (if needed)
- `openspec/changes/{slug}/diagrams/{slug}-erd.md` (if needed)

Published to `apps/docs/` by Technical Writer after story ships.

## Quality Gates
- [ ] Flowchart created for every story
- [ ] Sequence diagram created for multi-service stories
- [ ] ERD created for stories with data entity changes
- [ ] GitHub Issue reference in every file header
- [ ] MermaidJS syntax valid

## References
- `.claude/skills/solution-architect/service-boundary-definition/SKILL.md`
- `.claude/skills/technical-writer/` (publishing)
