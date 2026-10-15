---
name: kanban-init
description: >
  Bootstrap a Kanban board for any project. Clones the kanban CLI from GitHub,
  creates docs/kanban/ with config.json, board.json, cards/, and copies skills
  into .claude/skills/.
  Usage: /kanban-init
license: Apache-2.0
metadata:
  author: Dani
  version: "3.3"
  scope: [root]
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion
---

## Overview

`/kanban-init` is an interactive wizard that sets up `docs/kanban/` for a project:
1. Copies the kanban CLI from this skill's bundled `cli/` into `docs/kanban/cli/`
2. Creates `config.json`, `board.json` (via CLI), and `cards/` directory
3. Copies the sibling kanban skills into `.claude/skills/` so the board travels with the repo

The kanban CLI and its companion skills are bundled with `minilink-skills`
itself — no network access required.

---

## Step 1: Detect project

1. Find git root: `git rev-parse --show-toplevel`
2. Detect main branch
3. Get directory name as default project name

If `docs/kanban/board.json` already exists, ask:
- Reinitialize (overwrite config)
- Update CLI only (pull latest from repo)
- Skip (just fix skills)
- Cancel

---

## Step 2: Gather project info

Ask with AskUserQuestion:

**Question 1: Project basics**
- Project name (default: directory name)
- Card ID style: `PREFIX_SLUG` (P1-FEATURE) or `SLUG_ONLY` (FEATURE)

**Question 2: Worktree & port config**
- Use git worktrees? (default: yes for larger projects)
- Port isolation? (default: yes if project has dev servers)

---

## Step 3: Understand project architecture

This step has two paths depending on whether the project has existing code.

### Path A: Existing project (files detected)

Scan project structure to auto-detect:
- **Domains**: directories like `src/`, `frontend/`, `backend/`, `api/`, `lib/`, etc.
- **Tech stack**: from package.json, pyproject.toml, Cargo.toml, go.mod, etc.
- **Commands**: test/build/dev from package.json scripts, Makefile targets, etc.

Present findings to user for review and correction with AskUserQuestion.

### Path B: Empty/new project (no source files detected)

**CRITICAL**: Do NOT skip this step or write empty placeholders. An empty project is when asking matters MOST — there's nothing to infer from, so you MUST ask.

Ask with AskUserQuestion (up to 2 rounds):

**Round 1: Project purpose and stack**

- **Question 1**: "What is this project about? Give a one-line description."
  - Options: provide 2-3 plausible guesses based on the project name, plus "Other"
  - This feeds into board metadata and helps `/plan-card` generate better cards

- **Question 2**: "What tech stack will you use?"
  - Options based on common stacks: "Next.js + TypeScript", "Python + FastAPI", "Go", "Rust", etc.
  - The answer determines default test/build/dev commands

**Round 2: Architecture and commands**

- **Question 3**: "What domains/areas will this project have?"
  - Options: "Frontend + Backend", "Monolith", "CLI tool", "Library/SDK", etc.
  - Populates the `domains` array in config.json

- **Question 4**: "What commands will you use?" (pre-filled from stack choice)
  - Test command (e.g., `npm test`, `pytest`, `go test ./...`)
  - Dev command (e.g., `npm run dev`, `uvicorn main:app --reload`)
  - Build command (e.g., `npm run build`, `cargo build`)
  - Let user confirm or override

### Output

After either path, you should have:
- `description`: one-line project summary (for board metadata)
- `stack`: detected or chosen tech stack
- `domains`: list of project areas/modules
- `commands.test`: how to run tests
- `commands.dev`: how to start dev server(s)
- `commands.build`: how to build (if applicable)

All of these feed into `config.json` in Step 5.

---

## Step 4: Copy CLI from this skill

The kanban CLI is bundled inside this skill at `cli/` (next to this
SKILL.md). Copy it into the project — no network, no clone:

```bash
# SKILL_DIR is the directory containing this SKILL.md.
# For Claude Code:  ~/.claude/skills/kanban-init
# For Codex:        ~/.codex/skills/kanban-init
# Use whichever path matches the agent you are running under.

mkdir -p docs/kanban/cards docs/kanban/cli/lib docs/kanban/assets

cp "$SKILL_DIR/cli/kanban.ts"      docs/kanban/cli/
cp "$SKILL_DIR/cli/lib/"*.ts        docs/kanban/cli/lib/
cp "$SKILL_DIR/cli/package.json"   docs/kanban/cli/
cp "$SKILL_DIR/cli/tsconfig.json"  docs/kanban/cli/
cp "$SKILL_DIR/cli/test.ts"        docs/kanban/cli/

# Install dependencies
cd docs/kanban/cli && npm install
cd -
```

If the bundled `cli/` directory is missing (very old install, manual
copy), tell the user to reinstall the skills:

```
npx skills add gwlabdev/minilink-releases -g
```

---

## Step 5: Write config.json

Build `docs/kanban/config.json` from gathered info. The schema below is the **contract** consumed by `/sprint`, `/merge`, and the CLI. All fields under `project` are required.

```jsonc
{
  "project": {
    "name": "<project name from Step 2>",
    "description": "<one-line summary from Step 3>",
    "repo": "<owner/repo from git remote>",
    "mainBranch": "<detected main branch from Step 1>",   // REQUIRED — e.g. "main"
    "branchPrefix": "feat/"                                // REQUIRED — e.g. "feat/"
  },
  "board": {
    "cardIdStyle": "<PREFIX_SLUG or SLUG_ONLY from Step 2>",
    "prefix": "<e.g. P — only if PREFIX_SLUG>"
  },
  "worktrees": {
    "enabled": true,                         // from Step 2
    "baseDir": ".claude/worktrees",          // or "~/{project-name}-worktrees"
    "ports": {                               // optional — only if port isolation chosen
      "enabled": true,
      "baseBackend": 4000,
      "baseFrontend": 3000,
      "envFile": ".env.local",
      "envVars": {
        "PORT": "{backendPort}",
        "NEXT_PUBLIC_PORT": "{frontendPort}"
      }
    }
  },
  "stack": {
    "language": "<e.g. TypeScript>",
    "framework": "<e.g. Next.js 16>",
    "ui": "<e.g. React 19 + Tailwind 4>",
    "runtime": "<e.g. Node.js>"
  },
  "domains": ["<from Step 3>"],
  "commands": {
    "dev": "<from Step 3>",
    "build": "<from Step 3>",
    "test": "<from Step 3>",
    "lint": "<from Step 3>"
  }
}
```

**Critical fields consumed by `/sprint`:**

| Field | Used for | If missing |
|-------|----------|------------|
| `project.mainBranch` | Base branch for `git branch {name} {mainBranch}` | Branch creation fails with "undefined" |
| `project.branchPrefix` | Prefix for branch name: `{prefix}{card-id}` | Branch name starts with "undefined" |
| `worktrees.enabled` | Whether to create a git worktree | Defaults to false |
| `worktrees.baseDir` | Directory for worktree checkout | Defaults to `~/{name}-worktrees` |
| `commands.test` | Injected into sprint prompt template | Empty string |

---

## Step 6: Initialize board.json via CLI

```bash
npx tsx docs/kanban/cli/kanban.ts init --json
```

This creates an empty `board.json` with default columns and scans the project for tech stack, commands, and domains.

---

## Step 7: Project-scope the kanban skills

Copy the kanban skills into the project's `.claude/skills/` so other
collaborators get them automatically when they clone the repo. The
skills live next to this one inside the `minilink-skills` install:

```bash
# SIBLINGS is the directory holding all minilink-skills.
# For Claude Code:  ~/.claude/skills
# For Codex:        ~/.codex/skills
SIBLINGS="$(dirname "$SKILL_DIR")"

mkdir -p .claude/skills
for skill in board sprint merge plan-card kanban-init; do
  cp -r "$SIBLINGS/$skill" .claude/skills/
done
```

If skills already exist in `.claude/skills/`, overwrite only the kanban
ones — preserve any other existing skills.

---

## Step 8: Report

```
Kanban board initialized for {ProjectName}

  Board:    docs/kanban/board.json
  Config:   docs/kanban/config.json
  CLI:      docs/kanban/cli/kanban.ts (bundled with minilink-skills)
  Cards:    docs/kanban/cards/
  Skills:   5 copied to .claude/skills/

Commands:
  npx tsx docs/kanban/cli/kanban.ts list        — view board
  npx tsx docs/kanban/cli/kanban.ts ready       — actionable cards
  npx tsx docs/kanban/cli/kanban.ts show <ID>   — card detail

Skills:
  /plan-card "your first feature"   — create a card
  /board                            — view the board
  /sprint {CARD_ID}                 — start working on a card
  /merge {CARD_ID}                  — merge and complete a card
```

---

## Edge cases

| Scenario | Behavior |
|----------|----------|
| Board already exists | Ask: reinitialize, update CLI, fix skills, or cancel |
| Not a git repo | Error: "Must be in a git repository" |
| **Empty project (no source files)** | **Use Step 3 Path B: ask user about purpose, stack, domains, and commands. NEVER write empty placeholders.** |
| No package.json | Skip auto-detection of commands, ask user instead |
| Existing .claude/skills/ | Preserve non-kanban skills, overwrite kanban ones |
| Bundled `cli/` missing | Tell the user to reinstall: `npx skills add gwlabdev/minilink-releases -g` |
