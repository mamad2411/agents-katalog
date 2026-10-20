---
name: source-driven-development-pro
description: Prefer existing source code, tests, docs, and project conventions over assumptions. Use before modifying unfamiliar repositories, integrating new features, refactoring, debugging, or when examples in docs may not match local code.
---

# Source Driven Development Pro

## Workflow

1. Locate project root and guidance files.
2. Read nearby implementation and tests before creating new patterns.
3. Search for existing helpers, services, components, hooks, clients, schemas, and conventions.
4. Reuse local abstractions when they fit.
5. If local code conflicts with external docs, prefer local behavior unless it is clearly wrong.
6. Document discovered conventions when they affect future work.

## Rules

- Do not invent a new structure before checking existing structure.
- Do not assume framework defaults when local wrappers exist.
- Do not add dependencies until local alternatives are checked.
- Do not change public contracts without finding consumers.

## Output

State the local pattern found, how the change follows it, and any convention worth documenting.
