---
name: requirement-create
description: Use when the user wants to create, write, split, or update a closed-loop requirement PRD for a feature in an Obsidian software specification vault.
license: MIT
compatibility: Agent Skills clients; requires access to the target Obsidian specification vault.
metadata:
  category: requirement
  workflow: create
---

# Requirement Create

## Load Standard

Read target-vault `.open-canal/standards/product.md` and `.open-canal/standards/repository.md`. If `.open-canal/standards/` is missing, stop and ask the user to run `framework-init` first.

## Load Template

Use `.open-canal/templates/prd.md` as the document skeleton.

## Workflow

1. Inspect the target vault's `.open-canal/AGENTS.md`, `modules/index.md`, and relevant module indexes.
2. Help the user narrow the request into one closed-loop requirement point (criteria in `.open-canal/standards/product.md`).
3. Run the confirmation gate — confirm the requirement boundary before writing. Skip only when the user explicitly gave enough detail.
4. Generate or update `modules/<module-slug>/requirements/<requirement-slug>/prd.md` from the template. On update, produce a change summary before writing.
5. Run the completeness checklist from `.open-canal/standards/product.md` before confirming.
6. Update `modules/index.md`, the module index, and affected version files. Report downstream docs needing refresh.

## Output

Return the PRD path, confirmation status, changed indexes, unresolved product questions, and downstream follow-up skills.
