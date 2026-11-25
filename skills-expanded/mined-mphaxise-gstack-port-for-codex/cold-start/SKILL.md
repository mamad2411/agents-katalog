---
name: cold-start
description: Bootstrap a new local brain by sequencing the highest-value first data sources and setup checks.
---

# Cold Start

Use this skill when the user is starting a new brain and wants it useful quickly.

## Workflow

1. Run `setup-gbrain`.
2. Identify first sources:
   - user-authored notes
   - project docs
   - meeting notes
   - key contacts
   - active tasks
3. Ingest a small sample before bulk import.
4. Run `brain-taxonomist` for unclear page types.
5. Run `frontmatter-guard`, `citation-fixer`, and `query` smoke checks.
6. Produce a day-one brain status report.

## Guardrails

- Do not ingest credentials or private exports wholesale.
- Keep source scope explicit.
- Prefer useful sample coverage over indiscriminate bulk import.
