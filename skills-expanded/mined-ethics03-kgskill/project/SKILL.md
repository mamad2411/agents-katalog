---
name: project-skill
description: Project-specific instructions for this workspace. Use when ingesting sources and maintaining wiki for this domain.
---

# [PROJECT NAME] Skill

Project-specific instructions for the Knowledge Graph.

## Project Overview

[Brief description of the project, domain, or topic]

## Domain

[What domain is this project about? Examples:
- Research: "Quantum computing research"
- Reading: "The Lord of the Rings"
- Personal: "Health and fitness tracking"
- Code: "Codebase documentation"
]

## Source Types

[What types of sources will be ingested?]

- Articles
- Papers
- Transcripts
- Notes
- [Other]

## Key Entities

[What kinds of entities are relevant to this domain? Examples:
- People, organizations, tools, places
- Characters, locations, items
- Concepts, frameworks, methods
]

## Key Concepts

[What concepts are central to this domain?]

## Ingestion Workflow

[Custom steps for ingesting sources in this domain]

1. Read source
2. Extract entities and concepts
3. Create/update wiki pages
4. Note contradictions with existing knowledge
5. Update index and log

## Page Types

[Project-specific page types beyond the standard entities/concepts/synthesis]

## Conventions

[Project-specific naming and formatting conventions]

### File Naming
- Entities: `entity-name.md`
- Concepts: `concept-name.md`
- Sources: `source-title-slug.md`

### Cross-References
- Link to related entities: `[[entities/Related]]`
- Link to concepts: `[[concepts/Topic]]`

## Current Focus

See [[../Active.md]] for current focus items.

## Key Files

| File | Purpose |
|------|---------|
| `raw/` | Source documents |
| `wiki/entities/` | Entity pages |
| `wiki/concepts/` | Concept pages |
| `wiki/synthesis/` | High-level summaries |
| `../Active.md` | Current priorities |