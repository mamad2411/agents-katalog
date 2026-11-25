---
name: design-usage-with-me-first
description: Design USAGE.md in chat with the user first — iterate until agreed, then /update-usage-md
argument-hint: "[workspace]"
related:
  - follow-devin-global-skills
  - update-usage-md
  - design-cli-prototype
  - design-tui-prototype
  - design-web-prototype
  - ask-me
  - apply
  - report
  - suggest-next-action
  - update-docs
  - report-usage
---

## Goal

Design the outline and content of `USAGE.md` together with the user `in chat only` — iterate until the user agrees, then hand off to `/update-usage-md` to actually write `USAGE.md` in the workspace

## Scope

Use when you want to lay out usage documentation before writing it for real — discussion-first, user in the loop for every iteration

- The surface itself (CLI commands/flags, TUI screens) is not agreed yet → `/design-cli-prototype` / `/design-tui-prototype` first
- Discuss and draft in chat only — `do not create any files` (no temp file, no touching the workspace) until the user confirms
- Content structure follows the `/update-usage-md` standard — code is the source of truth
- Always start from `/ask-me` and `/suggest-next-action` to understand the requirements
- Do not commit — the user must confirm before handing off to the real write

## Execute

### 1. Load Skills

> Goal: follow the docs conventions that already exist, not from memory

1. Run `/follow-devin-global-skills` — list global (`%APPDATA%\devin\skills`) and project (`.devin/skills/`) skills matching the target workspace
2. Read `/update-usage-md` (the standard this draft must satisfy) plus the surface skills it points to (`/follow-tool-usage` for CLI specs, `/follow-lib-*` for the libraries in use)
3. Project `AGENTS.md` → read its `### Skills` section; reuse the section names and tone the project's docs already use

### 2. Clarify Intent

> Goal: Understand what the USAGE doc must cover

1. Run `/suggest-next-action` to see the common options for usage docs (library API / CLI / service / internal tool)
2. Run `/ask-me` to ask about: audience (dev/ops/end-user), depth (quick-start vs full reference), any special sections wanted
3. Summarize the requirements with `/report table` columns: `No.`, `Requirement`, `Priority`

### 3. Detect Usage Surface

> Goal: Get the real API/CLI surface from the code

1. Follow step 2 of `/update-usage-md` — read the manifest, public API, bin targets, and examples from the real code
2. Never guess the API — every entry must come from the code or be clearly stated by the user
3. If an existing `USAGE.md` is present → pull it as a baseline and compare in chat

### 4. Draft In Chat

> Goal: Draft the outline and content in chat until the user agrees — create no files

1. Show the draft outline in chat with the standard sections: `## Overview`, `## Installation`, `## Usage`, `## API Reference`/`## Commands`, `## Examples`, `## Configuration`
2. Expand into a full draft in chat (markdown block) per the requirements + code surface
3. Ask for feedback via `/ask-me` — collect it into a checklist before revising
4. Revise the draft in chat per the feedback → repeat until agreed — show the diff/changed parts every iteration
5. If there are multiple options → use `/apply choose`

### 5. Handoff

> Goal: Turn the agreed draft into the real file

1. Run `/report table` to summarize: `No.`, `Section`, `Source`, `Status`
2. Ask the user: write the real `USAGE.md` in the workspace now?
3. If confirmed → run `/update-usage-md` using the chat draft as the spec
4. Run `/suggest-next-action`

## Rules

- Discuss and draft in chat only — do not create any files until the user confirms
- Always run `/follow-devin-global-skills` first — `/update-usage-md` and the project's own skills define the structure; never invent a parallel one
- Always start with `/ask-me` and `/suggest-next-action`
- Code is the source of truth — never write API/commands that do not exist in the code (unless the user marks them as a planned feature and states it clearly)
- Do not commit/push automatically
- Use `/update-docs` if needed
- Use `/report-usage` if needed

## Expected Outcome

- A chat draft the user has agreed to — ready as the spec for `/update-usage-md`
- The skills read first are listed, and the draft follows the structure `/update-usage-md` already defines
- Feedback log with all iterations
- A clear path to the real write (`/update-usage-md`)
