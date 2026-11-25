---
name: grok-build-setup
description: >
  Scaffold a full Grok Build Final Boss project structure (.grok/, AGENTS.md,
  rules, skills, agents, hooks). Use when the user runs /grok-build-setup,
  asks to "setup grok build", "final boss setup", "initialize .grok", or
  "configure project for Grok Build".
when-to-use: /grok-build-setup, setup grok build, final boss, scaffold .grok
argument-hint: "[--merge] [stack: node|python|rust|go]"
---

# Grok Build Setup

Scaffold the **Final Boss** Grok Build layout in the target project. All templates live beside this skill:

```
<dirname of this SKILL.md>/references/
```

Read `references/structure.md` first for the target tree, context ladder, and migration table.

## Invocation

```
/grok-build-setup
/grok-build-setup node
/grok-build-setup --merge python
```

| Argument | Meaning |
|----------|---------|
| `node`, `python`, `rust`, `go` | Stack hint for command defaults |
| `--merge` | Add missing files only; never overwrite without confirmation |

## Step 0 — Detect context

1. Confirm the target directory (`pwd`) — scaffold here unless the user names another path.
2. Check for existing setup:
   - `AGENTS.md`, `.grok/`, `CLAUDE.md`, `GROK.md`
   - Legacy root dirs: `rules/`, `skills/`, `agents/`, `hooks/`
3. Detect stack from manifests when possible:

| Signal | Stack | Default commands |
|--------|-------|------------------|
| `package.json` | node | test: `npm test`, lint: `npm run lint`, build: `npm run build`, format: `npm run format` |
| `pyproject.toml` or `requirements.txt` | python | test: `pytest`, lint: `ruff check .`, build: `python -m build`, format: `ruff format .` |
| `Cargo.toml` | rust | test: `cargo test`, lint: `cargo clippy`, build: `cargo build`, format: `cargo fmt` |
| `go.mod` | go | test: `go test ./...`, lint: `golangci-lint run`, build: `go build ./...`, format: `gofmt -w .` |
| none | generic | test/lint/build/format: `echo "configure in AGENTS.md"` |

4. If legacy paths exist, show the migration table from `references/structure.md` and ask whether to migrate content into the new layout.

## Step 1 — Collect info (only if missing)

Ask at most three questions:

1. Stack (if not detected)
2. Real test / lint / build commands (if defaults are wrong)
3. Greenfield or `--merge` (if ambiguous)

Skip questions when the user already provided answers in the invocation or conversation.

## Step 2 — Scaffold (Full Final Boss)

Create the following in the **target project root**. In `--merge` mode, skip any path that already exists unless the user explicitly approves overwrite.

### Directories

```
.grok/skills/security-review/
.grok/skills/deploy/
.grok/skills/release/
.grok/agents/
.grok/hooks/
.grok/rules/frontend/
.grok/personas/
.grok/roles/
docs/decisions/
tools/scripts/
```

### Files to create

| Target path | Template source | Notes |
|-------------|-------------------|-------|
| `AGENTS.md` | `references/AGENTS.md.tmpl` | Replace `{{PROJECT_NAME}}`, `{{STACK}}`, command placeholders |
| `.grok/config.toml` | `references/config.toml.tmpl` | As-is unless user needs MCP |
| `.grok/rules/testing.md` | `references/rules/testing.md.tmpl` | Fill `{{TEST_CMD}}` |
| `.grok/rules/api-design.md` | `references/rules/api-design.md.tmpl` | As-is |
| `.grok/rules/frontend/react.md` | `references/rules/frontend/react.md.tmpl` | Only if stack is node or user confirms frontend |
| `.grok/agents/code-reviewer.md` | `references/agents/code-reviewer.md.tmpl` | As-is |
| `.grok/agents/debugger.md` | `references/agents/debugger.md.tmpl` | Fill `{{TEST_CMD}}` |
| `.grok/agents/db-validator.md` | `references/agents/db-validator.md.tmpl` | As-is |
| `.grok/hooks/protect.json` | `references/hooks/protect.json.tmpl` | As-is |
| `.grok/hooks/format.json` | `references/hooks/format.json.tmpl` | As-is |
| `tools/scripts/protect.sh` | `references/scripts/protect.sh.tmpl` | `chmod +x` |
| `tools/scripts/format.sh` | `references/scripts/format.sh.tmpl` | `chmod +x` |
| `.grok/skills/security-review/SKILL.md` | `references/skills/security-review/SKILL.md.tmpl` | As-is |
| `.grok/skills/security-review/checklist.md` | `references/skills/security-review/checklist.md.tmpl` | As-is |
| `.grok/skills/deploy/SKILL.md` | `references/skills/deploy/SKILL.md.tmpl` | Fill command placeholders |
| `.grok/skills/release/SKILL.md` | `references/skills/release/SKILL.md.tmpl` | Fill command placeholders |
| `.grok/skills/release/changelog.tmpl` | `references/skills/release/changelog.tmpl` | As-is |
| `docs/architecture.md` | inline stub | One-paragraph placeholder |
| `docs/decisions/.gitkeep` | empty | Preserve empty dir |
| `.grok/personas/.gitkeep` | empty | Optional dir |
| `.grok/roles/.gitkeep` | empty | Optional dir |

### `docs/architecture.md` stub

```markdown
# Architecture

Describe system components, boundaries, and data flow here.
Update when making structural changes.
```

### `.gitignore` updates

If `.gitignore` exists, append (if not already present):

```
.env
.env.*
*.local.*
```

If no `.gitignore`, create one with those lines.

### Placeholder substitution

Replace all `{{...}}` tokens in templates:

| Token | Value |
|-------|-------|
| `{{PROJECT_NAME}}` | Directory name or user-provided name |
| `{{PROJECT_DESCRIPTION}}` | One line from README or "Application codebase" |
| `{{STACK}}` | Detected stack |
| `{{PACKAGE_MANAGER}}` | npm, pip/poetry, cargo, go modules, etc. |
| `{{FRAMEWORK}}` | Detected framework or "TBD" |
| `{{TEST_CMD}}` | From detection or user |
| `{{LINT_CMD}}` | From detection or user |
| `{{BUILD_CMD}}` | From detection or user |
| `{{FORMAT_CMD}}` | From detection or user |
| `{{DEPLOY_CMD}}` | `echo "configure deploy command"` unless user provides |

### Safety rules

- Never put literal API keys in `config.toml` — use `$ENV_VAR` references only
- Keep generated `AGENTS.md` under ~200 lines
- Never overwrite existing files without explicit user approval
- Do not scaffold application source under `src/` unless the user asks

## Step 3 — Customize

1. If `README.md` exists, align `AGENTS.md` project description with it.
2. For monorepos, offer optional `src/<package>/AGENTS.md` per package (only after confirmation).
3. If legacy `CLAUDE.md` or root `rules/` existed, offer to copy relevant content into `AGENTS.md` or `.grok/rules/` (user must approve each merge).

## Step 4 — Verify

Run in the target project root:

```bash
grok inspect
```

Confirm discovery of:

- Project Instructions (`AGENTS.md`)
- Skills: `security-review`, `deploy`, `release`
- Agents: `code-reviewer`, `debugger`, `db-validator`
- Hooks: `protect.json`, `format.json`

If `grok` is not on PATH, list created files manually and tell the user to run `grok inspect` locally.

## Step 5 — Report

Provide a concise summary:

1. **Created** — list of new files and directories
2. **Skipped** — existing paths left untouched (merge mode)
3. **Next steps:**
   - Trust project hooks: `/hooks-trust` or launch with `--trust`
   - Enable cross-session memory: `GROK_MEMORY=1` or `[memory] enabled = true` in `~/.grok/config.toml`
   - Run `/security-review`, `/deploy`, `/release` in this project
   - Use `explore` subagent for research; `code-reviewer` for reviews
4. **Reminder:** commit `.grok/` and `AGENTS.md` to version control

## Stack-specific notes

- **node**: include `frontend/react.md` rule when React is detected in dependencies
- **python**: prefer `pyproject.toml` scripts for commands when present
- **rust**: ensure `cargo fmt` is referenced in format hook env hint (`FORMAT_CMD=cargo fmt`)
- **go**: use `go test ./...` not bare `go test` for monorepo safety
