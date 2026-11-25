---
name: team-bootstrap
description: Set up a complete 4-role AI agent team with workflow, doc management, and hooks for any project. Use when starting a new project and need team structure, when asked to "set up agents" or "create a team", when bootstrapping Claude Code for collaborative development, or when someone mentions needing roles, workflow, or team management. Don't use for modifying an existing team setup or for single-agent automation tasks.
user-invokable: true
disable-model-invocation: true
args:
  - name: project
    description: Project name
    required: false
---

# Team Bootstrap

Bootstrap a complete AI agent team management system. One command creates 4 agent roles, a 10-step development workflow, document management rules, protective hooks, and session continuity scaffolding.

This skill exists because managing an AI agent team requires coordinated infrastructure across multiple layers (roles, process, docs, enforcement, memory) — setting these up individually is error-prone and inconsistent. This skill ensures every project starts with a battle-tested foundation.

## Step 1: Gather Project Info

Ask the user for the following. If `$ARGUMENTS` provides the project name, use it and ask the rest:

1. **Project name** — used in CLAUDE.md header, board.md, scaffold files
2. **Tech stack** — backend language+framework, frontend framework, database, ORM
3. **Verify commands** — the commands that prove code works:
   - Backend check (e.g., `cd backend && uv run python -c "from app.main import app"`)
   - Frontend build (e.g., `cd frontend && npm run build`)
   - Frontend typecheck (e.g., `cd frontend && npx tsc --noEmit`)
4. **Main directories** — backend path, frontend path
5. **Design tool** — pencil (.pen files) / figma / none
6. **Protected file patterns** — files that need founder approval to edit (e.g., `.env`, credentials)

## Step 2: Create Directory Structure

```bash
mkdir -p .claude/agents .claude/rules
mkdir -p docs/product/{modules,requirements,archive}
mkdir -p docs/technical/{deliverables,archive}
```

If design tool is not "none", also create:
```bash
mkdir -p docs/design/{deliverables,archive}
```

## Step 3: Generate CLAUDE.md

Read `references/claude-md.md` in this skill directory for the template. Replace all `{{PLACEHOLDER}}` values with the user's answers. The result should be under 150 lines and contain:

- Tech stack table, project structure, setup/dev commands
- Verification section (organized by change type: frontend/backend/deploy)
- Team section (links to agents, workflow, doc-management)
- Session Recovery steps (board → handoff → memory)
- ALWAYS rules (5 habits: verify before reporting, read model before referencing, read design before implementing, include affected_files, update board+handoff at end)
- NEVER rules (safety rails: no force-push, no --no-verify, no schema without migration, no .env without approval, no production trial-and-error, plus protected file patterns from user input)
- Compact Instructions (what survives context compression)

## Step 4: Generate 4 Agent Definitions

Read `references/agents/` for templates. Create 4 files in `.claude/agents/`:

Each agent follows 6 sections: Identity / Capabilities / Boundaries / Output Standards / Quality Gates / Context Loading.

| Agent | Model | maxTurns | Customize |
|-------|-------|----------|-----------|
| product-designer.md | opus | 30 | Add design tool MCP tools to `tools` list |
| cto.md | opus | 40 | Add design tool to `disallowedTools` |
| dev.md | sonnet | 50 | Match tech stack in context loading |
| tester.md | sonnet | 30 | Read-only: no Edit, no Write |

The reason for tool isolation: each role accumulates domain expertise in its context, and tool boundaries prevent accidental cross-contamination (e.g., Dev can't modify design files, Tester can't modify code).

## Step 5: Generate Team Workflow

Read `references/team-workflow.md` and copy it to `docs/team-workflow.md`. This file is **100% portable** — no customization needed.

It contains the complete 10-step process (requirements → design → tech review → development → testing → code review → acceptance → deployment → verification → archival), plus task management, communication patterns, feedback loops, version management, context hygiene practices, and session lifecycle.

## Step 6: Generate Doc Management

Read `references/doc-management.md` and copy it to `docs/doc-management.md`.

Only adjustment: if design tool is "none", remove the `design/` section from the directory tree.

Key concept in this file: [规格] (spec) documents are the **living, complete product requirements** for each module — not summaries. When a feature ships, requirement details merge into the spec verbatim, then the requirement doc is archived.

## Step 7: Generate Hooks

Read `references/hooks.md` for hook patterns. Create `.claude/settings.json` with:

**PreToolUse/Bash** (3 hooks):
1. Block `git push --force` / `-f` → exit 2
2. Block `--no-verify` → exit 2
3. Verify build before any `git push` → run frontend build + backend check

**PreToolUse/Edit|Write** (1-2 hooks):
- Block protected file patterns from user input → exit 2

**PostToolUse/Edit|Write** (1 hook):
- Type check after edits (ts/tsx → tsc, py → py_compile)

All hook commands must include output truncation (`| tail -N` or `| head -N`) to prevent context pollution. This matters because hook output goes into the conversation context — unbounded output from a failed build can consume thousands of tokens.

## Step 8: Configure Design Tool Connection (if needed)

If the user chose a design tool in Step 1, help them connect it. If no design tool was chosen, skip this step.

**This step is important** — without it, the Product Designer agent won't be able to read or edit design files. Walk the user through it step by step.

### Pencil (.pen files)

Tell the user:
> 我来帮你连接 Pencil 设计工具。只需要在项目的 `.claude/settings.json` 中添加一段配置。

Then **automatically** merge the following into the existing `.claude/settings.json` (which already has hooks from Step 7):

```json
"mcpServers": {
  "pencil": {
    "command": "npx",
    "args": ["-y", "@anthropic/pencil-mcp"]
  }
}
```

No API key needed for Pencil. After adding, tell the user: "Pencil 已配置好。下次启动 Claude Code 时生效。"

### Figma

Tell the user:
> 要连接 Figma，需要一个 API Key。获取方式很简单：
> 1. 打开 figma.com，登录你的账号
> 2. 点击左上角头像 → Settings（设置）
> 3. 滚动到 Personal Access Tokens（个人访问令牌）
> 4. 点击 Create new token（创建新令牌），名字随意填
> 5. 复制生成的 token，发给我

After receiving the key, merge into `.claude/settings.json`:

```json
"mcpServers": {
  "figma": {
    "command": "npx",
    "args": ["-y", "figma-developer-mcp", "--stdio"],
    "env": {
      "FIGMA_API_KEY": "<user's token>"
    }
  }
}
```

**Security note**: The API key goes into `.claude/settings.json`. Make sure this file is in `.gitignore` — never commit API keys to version control. If the project's `.gitignore` doesn't include it, add `settings.local.json` to `.gitignore`, and put the `mcpServers` config in `settings.local.json` instead of `settings.json`.

If the user doesn't have a Figma account or wants to skip, tell them they can set it up later by running `/team-bootstrap` again or manually editing the config file.

## Step 9: Generate Scaffold Files

Create 3 starter files using templates from `references/scaffolds.md`:

- **docs/board.md** — Task board with ID/type/task/status/assignee columns
- **docs/handoff.md** — Session handoff with 4 sections: completed, tried-but-failed, blockers, next-steps
- **docs/product/decisions.md** — Decision record (append-only, never modify history)

## Step 10: Verify & Report

Check every generated file exists. Report to user:

```
✅ Team Bootstrap Complete

Generated:
- CLAUDE.md (project contract, ~150 lines)
- .claude/agents/ (4 role definitions)
- .claude/settings.json (6 hooks: 3 pre-bash + 1-2 pre-edit + 1 post-edit)
- docs/team-workflow.md (10-step process + collaboration)
- docs/doc-management.md (document lifecycle system)
- docs/board.md + handoff.md + decisions.md (scaffolding)

Next steps:
1. Review CLAUDE.md — customize ALWAYS/NEVER for your project
2. Add .claude/rules/ files for your languages (e.g., backend.md, frontend.md)
3. Create [规格] docs for existing modules in docs/product/modules/
4. Try a small feature end-to-end to validate the workflow
```
