---
name: profile-detection
description: Use when starting a cs-loop session, when profile detection fails or returns the wrong profile, when environment-specific commands (pytest, ruff, conda) aren't running correctly, or when session state needs recovery after context compaction.
user-invocable: false
---

# Profile Detection Skill

Reference material for the `/cs-loop` INIT phase — detecting project profile, environment, and loading context.

## Session State Recovery

1. **Compaction recovery** — Check `.claude/state/compact-context.json` (written by pre-compact hook). If present, restore current task ID, recent file changes, decisions, and phase context.

2. **Profile loading** — Read `.claude/state/session_start.json` (created by session-start hook). Use the `profile` field. If missing or stale, fall back to scanning for project indicator files (see `.claude-sentient/profiles/CLAUDE.md`). For gate commands, read `.claude-sentient/profiles/{name}.yaml`.

## Python Environment Detection

| Indicator | Environment | Command Prefix |
|-----------|-------------|----------------|
| `environment.yml` | Conda | `conda run -n <env> --no-capture-output` |
| `.venv/`, `venv/` | Virtualenv | Activate first or use `.venv/bin/python` |
| `poetry.lock` | Poetry | `poetry run` |
| `pdm.lock` | PDM | `pdm run` |

Report: `[INIT] Environment: conda (myenv)` or `[INIT] Environment: system python`

## Web Project Detection

| Indicators | Profile | Auto-load |
|------------|---------|-----------|
| next.config, vite.config, react, vue, svelte | TypeScript Web | ui-ux-design |
| templates/, django, flask, jinja2 | Python Web | ui-ux-design |

## Rule Auto-Loading

Rules with `paths:` frontmatter in `.claude/rules/` are loaded automatically by Claude Code based on file context. For supplementary keyword-based loading, see `.claude/rules/_index.md` for the full keyword-to-rule mapping. The INIT phase does keyword matching first, then a semantic pass over `.claude/rules/_index.md` to catch logically relevant rules that keywords missed.

## MCP Context Gathering

| Server | What to Load | When |
|--------|-------------|------|
| **context7** | Library docs for detected imports | Always (scan task-related files) |
| **github** | Issue/PR requirements, recent commits | When task references #issues or PRs |
| **memory** | Prior decisions/patterns matching task keywords | Always (search nodes) |
| **memory** | Cross-project global/org learnings | Always (search scope:global, scope:org) |

## Dependency Changelogs

Trigger keywords: "update", "upgrade", "migrate", "bump". Use WebFetch to load CHANGELOG.md or release notes for the dependency being changed. Prevents breaking changes from surprising you.

## Governance Files

Check these exist, create from `.claude-sentient/templates/` if missing: `STATUS.md`, `CHANGELOG.md`, `DECISIONS.md`, `.claude/rules/learnings.md`.

Check for `CLAUDE.md` — if missing, report: `[INIT] No CLAUDE.md found. Run /cs-init to create context architecture.`

Check for `CLAUDE.local.md` in project root. If missing and first session, note: `[INIT] Tip: Create CLAUDE.local.md for personal preferences (gitignored). Template: .claude-sentient/templates/CLAUDE.local.md`

- **Cross-model workflow**: For high-stakes changes, consider Claude + Codex QA review. See `references/cross-model.md`

## Gotchas

- **Conda env not activated**: If `environment.yml` exists but commands run in system Python, the `conda run -n <env>` prefix was not applied. Always check for this indicator before running any Python commands.
- **nvm FUNCNEST explosion**: On zsh systems with nvm, bare `node` triggers recursive shell function loading (500+ `_nvm_load command not found` lines). Hook commands must use absolute node paths via `process.execPath`. The `fixHookPaths()` function in session-start.cjs self-heals this, but if hooks fail with FUNCNEST errors, check that `settings.json` hook commands use absolute paths.
- **session_start.json stale or missing**: The `profile` field in session state may be from a previous session or absent on first run. Always fall back to scanning indicator files (`pyproject.toml`, `tsconfig.json`, `go.mod`, etc.) when the state file seems stale.
- **Two-step rule loading**: Keyword matching alone misses logically relevant rules (e.g., `error-handling` for a debug task that uses no keyword triggers). The semantic pass over `rules/_index.md` catches these — don't skip it.
- **Windows MCP servers**: MCP servers require `cmd /c npx` wrapper on Windows, not direct `npx`. See learnings.md for the `add-json` pattern.
