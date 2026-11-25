---
name: svenstar-workflow-installer
description: Install and manage Svenstar's dual-mode development workflow for repositories, supporting both Codex and Claude Code agents (managed block merged into AGENTS.md, which both read). Use when the user asks to install, update, check, or create feature folders for the lightweight/long-task develop workflow, or mentions svenstar workflow installer or workflow setup.
---

# Svenstar Workflow Installer

Use the bundled script for deterministic edits. It installs a dual-mode workflow:

- Light mode: small fixes use normal code edits, tests, git diff/commit messages; no task directory.
- Long-task mode: large features use one `docs/develops/<date-slug>/` root directory. `docs/develops/current.json` can point either to that root or to a phase subdirectory such as `docs/develops/<date-slug>/<phase-slug>/`. Each active directory keeps its own `task.json` and `current.md`; completed tasks require git commits.
- Candidate requirements and design drafts live in `docs/superpowers/`; they stay outside the development workflow until the user explicitly promotes one into `docs/develops/`.

## Commands

Run from the target repository root unless `--cwd` is supplied:

```bash
python3 /path/to/skill/scripts/develop_workflow.py install
python3 /path/to/skill/scripts/develop_workflow.py update
python3 /path/to/skill/scripts/develop_workflow.py check
python3 /path/to/skill/scripts/develop_workflow.py new-feature "feature name"
python3 /path/to/skill/scripts/develop_workflow.py new-phase "phase name"
```

Command behavior:

- `install`: First-time setup. Creates `WORKFLOW.md`, `docs/develops/current.json`, `docs/develops/task.schema.json`, `docs/develops/_template/*`, `docs/superpowers/README.md`, missing `memory-bank/*.md` starter files, and merges a managed block into `AGENTS.md`. Does not overwrite existing files unless `--force`; `docs/superpowers/README.md` and `memory-bank/*.md` are only created when missing.
- `update`: Refreshes managed workflow files. Preserves the custom section inside `WORKFLOW.md` and preserves non-managed `AGENTS.md` content. Also fills in missing `docs/superpowers/README.md` and `memory-bank/*.md` starter files without overwriting project-specific content.
- `check`: Reports missing files and whether `AGENTS.md` contains the managed workflow block.
- `new-feature <name>`: Creates `docs/develops/YYYY-MM-DD-slug/` from templates and updates `docs/develops/current.json` to point at the demand root.
- `new-phase <name>`: Creates `docs/develops/<feature>/<phase-slug>/` from templates and updates `docs/develops/current.json` to point at that phase directory. If `--feature` is omitted, it uses the current active demand root.

Long-task commit rule:

- Before a long-task deliverable is considered complete, check whether user-facing and operator-facing docs must be synced, especially `README.md`, `memory-bank/*.md`, deployment/runbook docs, and examples/scripts mentioned by the feature.
- If the change introduces or changes commands, workflows, public behavior, architecture boundaries, operations steps, or troubleshooting paths, update the relevant docs in the same task or phase instead of deferring silently.
- When a task enters `done`, commit the task-related files.
- When switching phases, keep only the minimum handoff needed in the next active directory's `current.md` or in stable docs.
- The commit message should summarize scope, verification, decisions, and leftovers when they matter.

## Rules

- Prefer `install` for a new repo.
- Prefer `update` for repos that already use this workflow.
- Use `check` before modifying an uncertain repo.
- Do not manually rewrite generated files unless the user asks; patch the script/templates instead.
