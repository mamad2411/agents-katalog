---
mode: agent
description: Scaffold a new component, service, or module consistent with this repository's existing structure and standards.
---

# New Component

Scaffold a new component in this repository.

1. Read `.github/copilot-instructions.md` and the scoped files in `.github/instructions/` that will apply to the new files.
2. Find the closest existing component and match its structure, naming, layering, error handling, and test layout. Consistency outranks personal preference.
3. Ask only for what the repository cannot answer: component name, responsibility, and its trust boundary. Use `clarify-the-ask` if the request is materially ambiguous.
4. Create the implementation, its registration or wiring, and its tests in the same change.
5. Cover the success path and the primary failure path with tests. Run them.
6. Update `README.md` or `docs/` only if setup, commands, or architecture changed.

Do not introduce a new dependency, framework, or architectural pattern without an ADR. Do not create placeholder files with no implementation.
