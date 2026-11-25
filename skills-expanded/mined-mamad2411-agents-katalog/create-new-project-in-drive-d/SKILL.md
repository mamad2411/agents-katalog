---
name: create-new-project-in-drive-d
description: Create a new project on drive D using the follow-create-* skill for its type
argument-hint: "<project-type> <project-name>"
related:
  - follow-create-cli
  - follow-create-web
  - follow-create-sdk
  - deep-review-codebase
  - follow-your-suggestion
  - follow-create-mobile
  - follow-create-bot

---

## Goal

Create a new project on drive D by selecting the `follow-create-*` skill that matches the project type

## Scope

Use when the user wants to start a new project on drive D, whether CLI, website, mobile, library, plugin, bot, or extension

## Execute

### 1. Gather Requirements

> Goal: Gather Requirements

1. Determine `project-type` from the argument or context, e.g. `cli`, `website`, `mobile`, `library`, `mcp`, `bot`, `extension`
2. Determine `project-name` from the argument or ask the user
3. Default the target path to `D:\newkub\<project-name>`, or use a path the user specifies
4. If `project-type` or `project-name` is missing → run `/follow-your-suggestion` to pick the type and project name from context

### 2. Select Create Skill

> Goal: Select Create Skill

1. `cli` → `/follow-create-cli`
2. `website` or `web` → `/follow-create-web`
3. `mobile` → `/follow-create-mobile-cross-with-capacitor`
4. `telegram-bot` → `/follow-create-bot`
5. `discord-bot` → `/follow-create-bot`
6. `line-bot` → `/follow-create-bot`
7. `browser-extension` → `/follow-create-browser-extensions-wxt`
8. `obsidian-plugin` → `/follow-create-obsidian-plugin`
9. `vscode-extension` → `/follow-create-vscode-extensions`
10. `zed-extension` → `/follow-create-zed-extensions`
11. `rust-crate` or `rust-lib` → `/follow-create-rust-crate`
12. `mcp` → `/follow-create-mcp`
13. If nothing matches or you are unsure → use `/follow-create-sdk` to ask and pick a stack

### 3. Prepare Target Path

> Goal: Prepare Target Path

1. Check that no directory exists at the target path yet
2. If one exists → ask the user whether to overwrite, rename, or cancel
3. Use `mkdir` to create parent directories if needed, or let the `follow-create-*` skill handle it

### 4. Run Create Skill

> Goal: Run Create Skill

1. Pass `project-name` and `target-path` to the selected skill
2. If the skill needs a stack, use `/deep-review-codebase` to confirm it
3. Follow through until the selected skill finishes creating the project

### 5. Validate And Ship

> Goal: Validate And Ship

1. Verify the project files were actually created at the target path
2. Run `/run-check` for the stack if needed
3. Run `/ship` when the work is complete
4. Report the path and next actions

## Rules

### 1. Target Path

- Projects must live on `D:\` or the drive the user specifies
- Never overwrite an existing directory without asking
- Always use absolute paths

### 2. Skill Selection

- Pick the `follow-create-*` skill whose `project-type` matches best
- If nothing matches, use `/follow-create-sdk` to route
- Do not create the project directly yourself; delegate to the specialized skill

### 3. Safety

- Check disk space before creating
- Never put secrets or API keys in templates
- If the target already has a git repo → ask first

## Expected Outcome

- The new project is created on drive D with the correct structure
- A `follow-create-*` skill matching the project type was used
- Validation passed and the project is ready to ship
- Target path, stack, and next actions are reported

