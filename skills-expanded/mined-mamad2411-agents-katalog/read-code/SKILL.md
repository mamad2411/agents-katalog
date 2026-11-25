---
name: read-code
description: Orient quickly in an unfamiliar codebase area; produce a one-page map of structure, entry points, and the most likely place a change should land.
---

# read-code

> Orient in an unfamiliar codebase area before changing anything. Output is a concise map, not a tour.

## When to use

- Joining a new repo or area.
- Before `feature-dev` if the area is unfamiliar.
- The user says "explain this", "where does X live?", "walk me through this".

## Inputs

- Area of interest: a path, file glob, or feature description.

## Procedure

1. List the top-level structure (`README.md`, `package.json`, `Cargo.toml`, `pyproject.toml`, etc.) to identify the language and build system.
2. From the entry point (`main`, `app`, route table, CLI dispatch), trace one user-facing flow end-to-end.
3. Identify:
   - Where requests / commands enter the system.
   - Where they leave (database, external API, response).
   - Major layers in between.
4. Spot the place where a change for the stated request would most likely land. List 2 alternatives.

## Output

```text
Codebase map: <area>

Entry points:
  - <file>:<line> — <function/route>

Flow:
  - <step 1>
  - <step 2>
  - <step 3>

Likely change site:
  - <file>:<line> — <reason>

Alternative change sites:
  - <file>:<line> — <reason>
  - <file>:<line> — <reason>

Open questions:
  - <thing you couldn't determine from reading>
```

## Quality bar

- ≤ 30 lines of summary.
- Every file path is real.
- At least one open question if the area is non-trivial.
