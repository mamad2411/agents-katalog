---
name: brainerd
description: "Use Brainerd as the umbrella router for repo-memory actions across Pi, Codex, and Claude. Repos that already have a brain may load Brainerd ambiently without invoking this skill."
license: MIT
---

# Brainerd

Brainerd may already be ambient in repos that have a brain. In that case the
active harness should already be reading `brain/index.md` and
`brain/principles.md` before non-trivial work.

Use this root skill only to route to the correct action surface.

## Canonical surfaces

- `brainerd-init`
- `brainerd-reflect`
- `brainerd-ruminate`

## Routing rules

- If the repo already has a Brainerd brain, you do not need this skill just to
  make the harness read it.
- If the user wants first-time setup, use `brainerd-init`.
- If the user wants to preserve something from the current conversation, use
  `brainerd-reflect`.
- If the user wants to mine older repo-scoped session history, use
  `brainerd-ruminate`.
- Do not use the removed harness-prefixed public names `pi-*`, `codex-*`, or
  `claude-*`.
- Do not use legacy names like `/brain-init`, `/reflect`, or `/ruminate`.

## Shared rules

- Edit only under `brain/` plus the managed Brainerd block in `AGENTS.md`.
- Do not hand-edit generated entrypoints like `brain/index.md` or
  `brain/principles.md`.
- Claude imports belong under `brain/imports/claude/`; distill them into notes
  or principles instead of copying them verbatim.
- End with a short summary of what changed, what was only previewed, or why no
  brain changes were written.
