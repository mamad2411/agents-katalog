---
name: convert-scripts
description: Create a `scripts/` folder and turn the given commands or workflow into script files
argument-hint: "<commands-or-workflow>"
allowed-tools:
  - read
  - write
  - edit
  - exec
  - find_file_by_name
  - ask_user_question
  - todo_write
  - skill
triggers:
  - user
  - model
related:
  - use-scripts
  - use-bun-shell
  - use-pwsh-shell
  - use-nu-shell
---

## Goal

Create a `scripts/` folder in the project and turn the user's commands, workflow steps, or context into working script files.

## Scope

Use when a project should centralize scripts under `scripts/` — build scripts, deployment scripts, test helpers, automation tasks, or utility scripts.

## Execute

### 1. Discover Project

> Goal: Know the project environment

1. Check the project root and look for `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, or other manifests
2. Check whether a `scripts/` folder already exists
3. Identify the runtime in use: Bun, Node.js, Python, PowerShell, Nushell, Bash, Rust, Go
4. If a shell or runtime choice is needed, use `/use-bun-shell`, `/use-pwsh-shell`, `/use-nu-shell`, or `/use-scripts`
5. Follow the project's existing conventions

### 2. Create `scripts/` Directory

> Goal: Create the scripts folder

1. If `scripts/` is missing, create it at the project root with `exec` or a suitable tool
2. If `scripts/` already exists, list the existing files
3. Create a `README.md` or `index.md` inside `scripts/` if none exists, explaining how to use the scripts

### 3. Convert Input To Scripts

> Goal: Convert input into scripts

1. Take input from the user, e.g. commands, workflow steps, or context to automate
2. If the input is unclear, ask follow-up questions
3. Choose the script language based on the project runtime and use case
4. Give files meaningful names such as `build.ts`, `deploy.ps1`, `test-all.nu`, `lint.sh`
5. Write clear scripts with error handling and comments where needed

### 4. Verify

> Goal: Verify the script works

1. Read the generated script
2. Run the script or do a dry-run if possible
3. Check permissions (chmod +x for shell scripts)
4. If there are errors → fix and rerun
5. Update `package.json` `scripts` or docs where appropriate

## Rules

- Always create `scripts/` at the project root if it is missing
- Choose the script language based on the project runtime and the user's skills
- Default to Bun/TypeScript when the project uses Bun/Node
- Use PowerShell when the project or user is on Windows and the script is tooling/admin
- Use Nushell when a structured data pipeline is needed
- Never hardcode secrets in scripts
- Use relative paths within the project
- Add a shebang when needed
- Dry-run before running scripts with side effects

## Expected Outcome

- The project has a `scripts/` folder
- Working script file(s) exist
- Scripts have error handling and follow project conventions
- The user knows how to invoke them and where the files live
