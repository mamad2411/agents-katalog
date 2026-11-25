---
name: harness
description: "Full Harness Engineering workflow: requirement → OpenSpec → implement → verify → deliver. Project-agnostic. Usage: /harness <requirement-description-or-file-path>"
---

# Harness Engineering — Automated Development Pipeline

Launch a coordinated agent team to take a requirement from idea to verified, delivered code in any project.

**Input**: `$ARGUMENTS` — either a path to a requirement document, or a text description of what to build.

This skill is **project-agnostic**. It discovers the project's conventions at startup and uses them throughout — no language, framework, or domain is assumed.

---

## Step 0: Bootstrap Project Context

Before spawning any agents, establish project context. The team must agree on **how this project works** so every agent uses the same commands and conventions.

### 0.1 Resolve project root

Use `pwd` (current working directory) as the project root unless the user supplied an explicit path. All later commands run relative to this root.

### 0.2 Load or create `.harness/project.md`

The framework reads project-specific configuration from `.harness/project.md` at the project root. This is the single source of truth shared by all agents.

```bash
ls .harness/project.md 2>/dev/null
```

**If it exists**: read it; pass its contents to every agent.

**If it does not exist**: do a one-shot detection pass and offer to create it:

1. Detect language/build system from manifest files:
   - `package.json` / `pnpm-lock.yaml` / `yarn.lock` → Node/JS/TS
   - `pyproject.toml` / `poetry.lock` / `requirements.txt` / `setup.py` → Python
   - `go.mod` → Go
   - `Cargo.toml` → Rust
   - `pom.xml` / `build.gradle*` → JVM
   - `Gemfile` → Ruby
   - `composer.json` → PHP
   - `Makefile` / `justfile` / `Taskfile.yml` → custom recipes (read scripts directly)
2. Inspect existing scripts (`package.json` `scripts`, `pyproject.toml` `[tool.*]`, `Makefile` targets, etc.) to derive build/lint/format/test/run commands.
3. Read `CLAUDE.md`, `AGENTS.md`, `README.md`, and any `docs/` index for layer rules, file placement conventions, and domain knowledge sources.
4. Draft a `.harness/project.md` (template below) and ask the user to confirm before writing.

### 0.3 `.harness/project.md` template

```markdown
# Project Harness Config

## Identity
- name: <project name>
- root: <absolute path>
- primary_language: <python | typescript | go | rust | java | …>
- package_manager: <poetry | pnpm | npm | go | cargo | …>

## Commands
> Use these EXACT commands. Agents must not invent equivalents.

- install:    <e.g. `poetry install` | `pnpm install` | `go mod download`>
- build:      <e.g. `pnpm build` | `cargo build`>
- format:     <e.g. `poetry run black .` | `pnpm format`>
- format_check: <command that fails if formatting is off>
- lint:       <e.g. `poetry run flake8` | `pnpm lint` | `golangci-lint run`>
- typecheck:  <if applicable; else: none>
- test:       <e.g. `poetry run pytest -v` | `pnpm test` | `go test ./...`>
- test_changed: <fast subset for iteration; optional>
- run:        <e.g. `poetry run uvicorn app.main:app --port 19080` | `pnpm dev` | `go run ./cmd/server`>
- smoke_url:  <optional; HTTP endpoint to curl as health check>

## Source Layout
- source_dirs: [<e.g. app/, src/, internal/>]
- test_dirs:   [<e.g. tests/, __tests__/, *_test.go siblings>]
- entrypoints: [<files that bootstrap the app>]

## Architectural Rules (optional)
> Layer or module rules the verifier must enforce. Leave empty if the project has none.

- layer_order: [<e.g. constants, schemas, utils, configs, clients, models, tools, handlers, services, routers, main>]
- placement_rules:
  - <e.g. "all Pydantic models live under app/schemas/">
  - <e.g. "tool functions take `tool_context: ToolContext` as last param">

## Registration / Wiring (required if the project has an entry-point that aggregates handlers, tools, routes, or commands)
> List EVERY layer a new public symbol must touch to be reachable from production. The verifier will demand grep + live-import evidence covering each layer before passing the "Integration Impact" dimension.

- new_symbol_layers:
  - <e.g. "package `__init__.py`: add to `from .<module> import <fn>` AND to `__all__`">
  - <e.g. "agent/root.py: add to the `from <package> import (...)` block AND to the `LlmAgent(tools=[...])` list">
- wiring_probe: <fresh-subprocess import command that asserts a concrete count or membership, e.g. `poetry run python -c "from app.agent import root_agent; assert '<fn>' in [t.__name__ for t in root_agent.tools]"`>

## Conventions
- error_handling: <e.g. "use app/exceptions/ types; no bare raise Exception">
- logging:        <e.g. "use LogUtil; no direct print">
- secrets:        <e.g. "via app/configs/config.py only; never read env vars elsewhere">
- verification:   "evidence-based — every PASS claim from any agent must include the exact command + verbatim output. Self-reports without command output are treated as unverified."

## Knowledge Sources (priority order)
1. <e.g. `Skill("feed-knowledge")` — domain concepts>
2. <e.g. `mcp__notion__notion-search` — product docs>
3. <e.g. in-repo `docs/` and `CLAUDE.md`>
4. <codebase grep>

## Runtime Smoke Test
- start_command: <command to start a dev server, optional>
- health_check:  <curl recipe to confirm it's up, optional>
- stop_command:  <how to stop, optional>

## Notes
<anything else the team should know>
```

### 0.4 Pin OpenSpec presence

Run:
```bash
openspec --version 2>/dev/null && ls openspec/ 2>/dev/null
```

If OpenSpec is not installed or no `openspec/` directory exists, ask the user how to proceed:
- **A.** Install / initialize OpenSpec, then continue.
- **B.** Skip the OpenSpec layer and produce lighter artifacts (proposal + checklist) under `.harness/changes/<feature>/`.

Default to (A) when OpenSpec is available; otherwise (B).

---

## Step 1: Read the Requirement

If `$ARGUMENTS` is a file path that exists, `Read` it. Otherwise treat it as the requirement text directly.

---

## Step 2: Create the Agent Team

```
TeamCreate: harness-<feature-short-name>
```

The feature short name should be kebab-case, derived from the requirement.

---

## Step 3: Spawn Agents

Spawn the four core agents in parallel. **Pass each agent the full `.harness/project.md` content as part of its initial prompt** so they share a single source of truth without re-discovering conventions.

### Agent 1 — `harness-planner`
Owns planning: gathers context, generates OpenSpec artifacts, creates implementation tasks.

### Agent 2 — `harness-implementer`
Picks up tasks one at a time, writes code + tests using the project's commands.

### Agent 3 — `harness-verifier`
Independent adversarial reviewer. Verifies each completed task across seven dimensions using the project's commands. **Does not share context with the implementer.**

### Agent 4 — `harness-finalizer`
Activates when every task has passed verification. Runs full integration checks and produces the delivery report.

Each agent's behavior is defined in its agent file (`~/.claude/agents/harness-*.md`). The skill only orchestrates.

---

## Step 4: Monitor as Team Lead

- Receive messages from agents.
- Handle escalations (a task failing verification 3×).
- On `HANDOFF` messages, spawn a fresh `harness-handoff` agent into the same team with the handoff document path and the previous role.
- When the finalizer delivers its report, present it to the user and shut down the team.

---

## Step 5: Deliver

Show the user:
- OpenSpec change summary (`openspec status --change "<feature>"`) — or the lightweight summary if OpenSpec was skipped.
- Files changed (`git diff --stat`).
- Test and coverage results.
- Spec coverage matrix (requirement → code → test).
- Warnings, skipped checks, open questions.
- Suggest next step: `/opsx:archive` if using OpenSpec, otherwise `git commit` / `gh pr create`.

---

## Knowledge Sources

Agents resolve domain knowledge in the order declared in `.harness/project.md` → `Knowledge Sources`. If that section is empty, they fall back to:

1. `CLAUDE.md`, `AGENTS.md` at the project root
2. `README.md`, `docs/`
3. Codebase via `Grep` / `Read`

The framework does **not** assume any specific MCP server (Notion, Linear, etc.) is available.

---

## Context Handoff

Long-running features risk context fatigue. Any agent may declare `HANDOFF` when it senses pressure. The flow:

1. The agent writes a handoff document under `.harness/changes/<feature>/handoff/<role>-<N>.md` (or `openspec/changes/<feature>/handoff/...` when OpenSpec is in use).
2. It sends `HANDOFF: written to <path>` and shuts down.
3. The team lead spawns a `harness-handoff` agent into the same team with the handoff path + original role.
4. The fresh agent verifies state, then continues.

Full context resets beat compression. A fresh agent with a good handoff outperforms a fatigued agent with a stuffed window.

---

## Error Handling

| Situation | Behavior |
|-----------|----------|
| Planner can't understand the requirement | Ask the user for clarification before generating artifacts. |
| Implementer fails 3× on one task | Verifier escalates to team lead → present to user. |
| Runtime check fails because of missing external deps | Mark `SKIP` with note, not `FAIL`. |
| Project commands fail at bootstrap | Stop and ask the user to fix `.harness/project.md`. |
| Agent requests handoff | Spawn fresh continuation agent (above). |

---

## Project Hygiene

- Never modify files outside the project root.
- Never invent commands not present in `.harness/project.md`.
- Never assume a language ecosystem; read the config.
- Never hardcode absolute paths in code or artifacts — use project-relative paths.
