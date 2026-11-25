---
name: document-generate
description: Generate or refresh missing project documentation using a Diataxis-style split of tutorials, how-to guides, reference, and explanation.
---

# Document Generate

Use this skill when the user asks to generate docs, fill missing docs, document a feature, or improve repo documentation after implementation.

This complements `document-release`: `document-generate` creates or refreshes the docs; `document-release` checks that shipped changes are reflected in release-facing documentation.

## Workflow

1. Identify the doc need:
   - tutorial: helps a new user complete a first task
   - how-to: solves a practical goal
   - reference: lists exact behavior, commands, options, or schemas
   - explanation: teaches design intent and tradeoffs
2. Inspect the code, tests, and existing docs before drafting.
3. Update the smallest useful doc surface:
   - prefer existing docs when the topic already has a home
   - create a new doc only when the repo structure supports it
4. Add verification examples when the reader would otherwise have to guess.
5. Run the repo's validation checks if docs are tied to skill registries or scripts.

## Guardrails

- Do not invent behavior that the code does not implement.
- Do not bury user-facing behavior only in commit messages.
- Keep docs consistent with README claims and the skill maps.
