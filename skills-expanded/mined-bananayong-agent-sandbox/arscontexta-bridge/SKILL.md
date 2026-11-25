---
name: arscontexta-bridge
description: Use the local Ars Contexta reference bundle in Codex (manual bridge mode, not Claude plugin mode)
---

# Ars Contexta Bridge Mode (Codex)

This sandbox installs Ars Contexta source files at:

- `~/.codex/vendor/arscontexta`

Use this bundle as a methodology and template reference while working in Codex.

## What Works in Codex

- Read research claims in `~/.codex/vendor/arscontexta/methodology/`
- Reuse reference specs in `~/.codex/vendor/arscontexta/reference/`
- Adapt generation patterns from `~/.codex/vendor/arscontexta/generators/`

## What Does Not Work Natively in Codex

- Claude plugin slash commands such as `/arscontexta:setup`
- Claude plugin marketplace lifecycle
- Claude hook events/config under `.claude/`

## Recommended Workflow

1. Read `~/.codex/vendor/arscontexta/README.md`.
2. Treat `~/.codex/vendor/arscontexta/skills/setup/SKILL.md` as a design spec.
3. Implement Codex-native files (`AGENTS.md`, scripts, skills) in the current workspace.
