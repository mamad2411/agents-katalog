---
name: target-instructions-bootstrap
description: "Create the target repository's local AI instruction scaffold during first-use bootstrap. Use from repo-init-scan when `.github/instructions`, runtime adapters such as `AGENTS.md` / `CLAUDE.md`, or the neutral project facts scaffold are missing. Do not use to overwrite existing project-specific rules."
---

# Target Instructions Bootstrap

Create or repair target-local instruction entrypoints during `repo-init-scan`. The neutral project facts scaffold is not enough to pass initialization until `repo-init-scan` replaces neutral markers with bounded repository facts or bounded-scan `unknown` gaps, verifies required artifacts, and writes the root `best-copilot.md` sentinel.

Load `references/templates.md` for exact file contents and repair snippets.

## Boundary

- Write into the target repository, never into the installed plugin package or plugin cache.
- Create missing files only. Preserve existing project-specific instructions.
- If an existing file lacks a required compatible section, append the smallest compatible section instead of replacing the file.
- Do not copy this plugin repository's active state, specs, memory, or private workflow examples into the target repository.
- Keep generated target files short and runtime-neutral unless a runtime-specific adapter is explicitly requested.
- Do not generate hooks or script-based enforcement; init, native ask, closeout, and state sync gates must be instruction-text enforceable.
- Do not create `best-copilot.md` here. Only `repo-init-scan` writes the verified-init sentinel after full verification.

## Verified Init Sentinel

`repo-init-scan` writes target root `best-copilot.md` only after full init verification:

```md
---
version: "0.8.0"
---
```

## Files

Create when absent, repair only compatible missing sections when present:

- `.github/instructions/project.instructions.md`
- `.github/instructions/must.instructions.md`
- `.github/instructions/skills-index.instructions.md`
- `AGENTS.md` when Codex compatibility is requested or current runtime needs it
- `.codex/agents/*.toml` when Codex custom-agent compatibility is requested or current runtime needs target-local Codex agents
- `CLAUDE.md` when Claude Code compatibility is requested or current runtime is Claude Code
- `.claude/settings.json` when Claude Code needs a stable Senior Project Expert session entry and current-branch worktree base

## Required Local Rules

Target `.github/instructions/must.instructions.md` must cover:

- source priority and language policy
- request flow, per-request timestamp, init normalization, and packet freeze
- reliability gates: think before coding, simplicity, surgical changes, read before writing, verification evidence
- native ask and no-silent-closeout rules
- PM/specialist ask boundary
- shared `work_mode`, `task_type`, and specialist handback vocabulary
- search precision and command output budget
- memory/spec progressive disclosure
- seven-part self-evolution loop and `evolution_signal`
- first-use scaffold gate
- Spec Bundle rule for MEDIUM/LARGE work
- `STATE_SYNC`: task status changes update `tasks.md` and `memories/repo/current-workstreams.md` before continuing
- agents/dispatch and cross-review lanes
- implementation/review/verification requirements

## Repair Rules

- Never replace an existing file wholesale.
- Append missing headings from `references/templates.md` only when compatible.
- If `.claude/settings.json` already has a different `agent`, do not overwrite it silently; return `BLOCKED target_instructions_bootstrap_conflict` unless the user explicitly requested the change.
- If `.claude/settings.json` already has a different worktree policy, preserve it and report the difference.
- If safe JSON repair is not possible, return `BLOCKED target_instructions_bootstrap_conflict` and list `.claude/settings.json`.
- If a required section cannot be inserted without conflicting with project-specific rules, return `BLOCKED target_instructions_bootstrap_conflict` and list the file.

## Procedure

1. Determine target root and requested runtime compatibility from `repo-init-scan`.
2. Read only the listed target instruction/adapter files that exist.
3. Create missing files from `references/templates.md`.
4. Append compatible missing sections from the reference to existing files.
5. Verify required paths, required headings, Codex TOML adapter names when applicable, Claude import lines when applicable, and valid JSON when `.claude/settings.json` is present.
6. Return created, preserved, repaired, conflict, and missing path lists.

## Verification

- Confirm generated files exist in the target repository.
- Confirm path existence plus required sections; path existence alone is insufficient.
- Confirm existing files were not overwritten.
- Confirm `.github/instructions/must.instructions.md` contains request flow, reliability gates, native ask, memory/spec, `STATE_SYNC`, self-evolution, `evolution_signal`, agents/dispatch, implementation/verification, and mixed-language rules.
- Confirm `.github/instructions/skills-index.instructions.md` contains Claude Code skill-name guidance when relevant.
- For Claude Code, confirm `CLAUDE.md` has standalone unindented imports for `.github/instructions/project.instructions.md`, `.github/instructions/must.instructions.md`, and `.github/instructions/skills-index.instructions.md`.
- For Claude Code, confirm PM coordinator dispatch, foreground/background policy, isolated worktree closeout, scoped plugin agent names, namespaced skill commands, skill-load-is-not-execution, code intelligence fallback, TypeScript LSP fallback, provider compatibility smoke check, `AskUserQuestion`, and `STATE_SYNC` are covered.
- When a stable Claude PM entry is required, confirm `.claude/settings.json` is valid JSON and contains `"agent": "senior-project-expert"` plus `"worktree": {"baseRef": "head"}` unless a different explicit policy was preserved.
- For Codex, confirm `AGENTS.md` references `.codex/agents/*.toml`, all eight `.codex/agents/*.toml` files exist, and each file contains its expected `name = "<role>"` field plus `developer_instructions`.
- Confirm no generated file contains unresolved project-specific claims, secrets, plugin-cache paths, or active plugin-package state.
- If invoked because instructions or adapters were missing and required files still do not exist, return `BLOCKED target_instructions_bootstrap_incomplete` with missing paths.
