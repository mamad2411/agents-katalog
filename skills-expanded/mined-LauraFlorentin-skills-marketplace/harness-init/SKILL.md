---
name: harness-init
description: Scaffold a project-local agent harness with concise repository instructions, acceptance criteria, environment checks, session handoffs, optional task coordination, and architecture notes. Use when starting an agent-assisted repository or when repeated sessions lose context; inspect and preserve existing project conventions before writing.
---

# Harness Init

Create only the harness components that solve observed project needs. Do not impose a web-app workflow, feature count, commit policy, model, port, or architecture on every repository.

## 1. Inspect

Read repository instructions and contributor docs first. Identify the stack, entry points, test and validation commands, package boundaries, current planning system, CI, existing agent instructions, and whether parallel agents are actually used.

If files such as `AGENTS.md`, `CLAUDE.md`, planning documents, task trackers, scripts, or `.harness/config.json` exist, preserve their useful content. Present conflicts or material replacements to the user before overwriting.

## 2. Choose components

Recommend the smallest useful set:

| Component | Add when |
|---|---|
| `AGENTS.md` | Agents need a concise repository map or scoped instructions |
| `docs/architecture.md` | Important boundaries are not obvious from code |
| `docs/plans/` | Complex work needs durable decisions and handoffs |
| `features.json` | The project benefits from machine-readable acceptance criteria |
| `claude-progress.txt` | Work spans fresh sessions without another tracker |
| `init.sh` | A safe, repeatable environment check can be automated |
| `layers.json` | Layer rules exist and can be validated mechanically |
| `current_tasks/` | Multiple agents truly need task claims |
| `.harness/config.json` | The user wants plugin hook guidance enabled |

Do not create redundant sources of truth. Prefer linking to an existing issue tracker, test suite, design system, or contributor guide.

## 3. Generate safely

Use relevant files from `../../templates/` as starting points, not immutable canon.

- Keep `AGENTS.md` short, specific, and navigational. Put detailed knowledge in linked docs.
- Give each feature a stable ID, observable acceptance criteria, priority, and status. If using the feature template, copy and validate against `features.schema.json.template`. Do not manufacture hundreds of speculative features.
- Make `init.sh` idempotent and stack-specific. It must not install dependencies, kill unrelated processes, or start a persistent service without user approval.
- Encode only real architectural boundaries in `layers.json`; pair them with a validator or label them advisory.
- If task locks are used, include owner, task, timestamp, and a manual stale-lock review process.
- Add `.harness/state/` to the appropriate ignore file only after reviewing existing patterns.

To enable packaged hooks, create `.harness/config.json` directly or, with user authorization, run:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/install.sh" --configure
```

Plugin hooks are already discovered from `hooks/hooks.json`; do not copy hook scripts or modify `.claude/settings.json`.

## 4. Verify

- Parse every generated JSON file.
- Run shell syntax checks on generated scripts.
- Run the project's existing validation and tests relevant to changed files.
- Confirm every path referenced by the repository map exists.
- Review the diff with the user-authored content preserved.
- Report files created, assumptions, optional components skipped, and any manual configuration still needed.

Do not stage or commit the scaffold unless the user explicitly asks for that Git operation.
