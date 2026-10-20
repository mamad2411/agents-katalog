---
description: Persist architecture decisions in docs/ADR with wave-coded filenames
alwaysApply: true
---

# ADRs

Folder: `docs/ADR/`. Template: `docs/ADR/TEMPLATE.md`. Index: `docs/ADR/README.md`. Full rules: `.cursorrules` §13.

## Filename (wave is in the id)

```text
ADR-W{wave:02d}-{seq:03d}-{kebab-slug}.md
```

Example: `ADR-W00-001-electron-vite-monorepo.md`. Seq restarts per wave. Never reuse or rename an id; supersede.

## Write when

Lock or deviate from the implementation plan; pick among real alternatives; introduce a contract later waves depend on; accept residual risk; change a previous ADR.

Not for trivia (button styles). If it touches security, cost, providers, or data shape — write it **in the same wave**, as soon as the decision is made.

Wave-close audit: missing ADR for a trust/architecture lock is **High**. Update the README index in the same change. No secrets in ADRs.
