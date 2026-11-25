---
name: notion-ops
description: "Knowledge capture, meeting prep, research docs, and spec-to-implementation — stored as structured local Markdown. Replaces Codex notion:* skills. Use when user says 'capture decision', 'meeting prep', 'research doc', 'spec to tasks', '记录决策', '整理笔记', or needs structured knowledge management."
---

# Notion-style Knowledge Operations (Local Markdown)

Replaces Codex Notion plugin skills with local Markdown equivalents.
All outputs are saved to `docs/` directory in the current project (or a user-specified path).

## Modes

### /notion-ops capture
**Replaces: notion:notion-knowledge-capture**

Capture decisions, discussions, and knowledge into structured Markdown.

Output format (`docs/decisions/YYYY-MM-DD-<topic>.md`):
```markdown
# Decision: <Topic>
**Date:** YYYY-MM-DD
**Status:** Decided / Proposed / Superseded
**Participants:** <who was involved>

## Context
<what prompted this decision>

## Decision
<what was decided>

## Rationale
<why this choice over alternatives>

## Alternatives Considered
1. <option A> — <pros/cons>
2. <option B> — <pros/cons>

## Consequences
- <positive/negative implications>

## Action Items
- [ ] <next steps>
```

### /notion-ops meeting
**Replaces: notion:notion-meeting-intelligence**

Prepare meeting materials, agenda, and pre-read documents.

Output format (`docs/meetings/YYYY-MM-DD-<topic>.md`):
```markdown
# Meeting: <Topic>
**Date:** YYYY-MM-DD HH:MM
**Attendees:** <list>
**Duration:** <estimated>

## Agenda
1. <item> (N min) — <owner>

## Pre-read Materials
- <document/link> — <why it's relevant>

## Key Questions to Resolve
1. <question>

## Notes
<to be filled during meeting>

## Action Items
- [ ] <task> — @<owner> — due: <date>
```

### /notion-ops research
**Replaces: notion:notion-research-documentation**

Aggregate research findings into structured documentation.

Output format (`docs/research/YYYY-MM-DD-<topic>.md`):
```markdown
# Research: <Topic>
**Date:** YYYY-MM-DD
**Sources:** <list of sources consulted>

## Summary
<executive summary>

## Key Findings
1. <finding> — <evidence/source>

## Analysis
<deeper analysis>

## Recommendations
1. <recommendation> — <rationale>

## Open Questions
- <unresolved items>

## References
- <citations>
```

### /notion-ops spec-to-tasks
**Replaces: notion:notion-spec-to-implementation**

Convert a specification document into implementation tasks.

Input: A spec document (Markdown, or user description)
Output format (`docs/implementation/YYYY-MM-DD-<feature>.md`):
```markdown
# Implementation Plan: <Feature>
**Spec Source:** <link/file>
**Date:** YYYY-MM-DD
**Estimated Effort:** <time>

## Requirements Summary
<distilled from spec>

## Task Breakdown
### Phase 1: <name>
- [ ] Task 1.1: <description> — <effort> — <dependencies>
- [ ] Task 1.2: ...

### Phase 2: <name>
- [ ] Task 2.1: ...

## Technical Decisions
- <decision>: <rationale>

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| ... | ... | ... |

## Definition of Done
- [ ] <criterion>
```

## Rules
- Always create the `docs/` subdirectory if it doesn't exist
- Use ISO dates (YYYY-MM-DD) in filenames
- Link related documents to each other
- Keep documents self-contained and readable
