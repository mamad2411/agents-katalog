# AGENTS.md

## Framework

> Framework-managed section. Add project-specific instructions outside this section.

This project follows the Aircury engineering framework defined in [FRAMEWORK.md](./FRAMEWORK.md).

All agents contributing to this repository MUST read and apply FRAMEWORK.md before doing any work. It is not optional and it is not advisory.

All framework workflow rules, delivery constraints, and enabled standards now live in `FRAMEWORK.md` as the single source of truth.

If this repository also has project-specific agent instructions, keep them outside the framework-managed section or in `FRAMEWORK.local.md`, and treat `FRAMEWORK.md` as the governing framework layer.

## Delivery board

The project's canonical backlog is the **Backlog** column of the delivery board named in `README.md § AI delivery board`.
File actionable work through `overboards-add-card`, which checks the board for duplicates before creating or enriching a card.

When a user mentions an `EWM-<number>` reference, treat it as a card public key on that board.
Read it through the Boards API as the `overboards-*` skills document (`.agents/skills/overboards-add-card/SKILL.md`), not as a local file, branch name or plain-text search term.
