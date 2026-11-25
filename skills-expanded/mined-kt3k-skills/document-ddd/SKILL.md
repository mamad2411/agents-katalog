---
name: document-ddd
description: |
  Update or create DDD documentation based on the current state of the codebase.
  Generates a single DOMAIN.md with context map, glossary, and aggregate documentation.
---

## Document DDD Skill

Generate or update Domain-Driven Design documentation to keep it in sync with the current codebase. All documentation is maintained in a single `DOMAIN.md` file at the project root.

### Execution Flow

1. **Assess current state**: Check if `DOMAIN.md` already exists. Read the codebase to understand the current domain model.

2. **Generate/update `DOMAIN.md`** with the following sections:

   - **Context Map**:
     - List all bounded contexts discovered in the codebase
     - Document relationships between contexts (upstream/downstream, shared kernel, anti-corruption layer, etc.)
     - Note integration patterns used

   - **Glossary**:
     - Canonical list of ubiquitous language terms with definitions
     - Update from current code — add new terms, remove obsolete ones, fix inconsistencies

   - **Aggregates**:
     - One section per aggregate root
     - Document: purpose, invariants, entities contained, value objects, domain events emitted
     - Include key code references

3. **Diff and confirm**: Before writing, show the user what will be created or changed. Apply changes only after approval.

### Output Format

A single file `DOMAIN.md` at the project root with the following structure:

```markdown
# Domain Model

## Context Map

...

## Glossary

| Term | Definition | Code Location |
|------|------------|---------------|
| ...  | ...        | ...           |

## Aggregates

### <Aggregate Name>

- **Purpose**: ...
- **Invariants**: ...
- **Entities**: ...
- **Value Objects**: ...
- **Domain Events**: ...

...
```

### Guidelines

- Keep documentation concise and developer-focused — not academic.
- Reference actual code paths so docs stay grounded.
- If `DOMAIN.md` already exists, update it incrementally rather than replacing wholesale.
- Always ask for user confirmation before writing files.
