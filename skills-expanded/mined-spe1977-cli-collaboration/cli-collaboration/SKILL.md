---
name: cli-collaboration
description: "Use when multiple CLI agents or IDE assistants alternate on a repository or single-session handoff workflow — especially with AGENT_HANDOFF.md, AGENTS.md/CLAUDE.md/GEMINI.md, dirty worktrees, ownership rules, red tests, resume requests, brainstorming.md, or /cli-collaboration. Do not use for isolated one-off questions, pure web searches, or clean single-turn tasks with no handoff state."
metadata:
  version: "2.6.0"
  short-description: "Safe multi-agent and cross-session handoffs via AGENT_HANDOFF.md"
---

# CLI Collaboration

Use a written handoff as the source of truth when coding agents, or one agent across sessions, work in the same project. The goal is continuity without destroying state left by the user or another agent.

## Core Rule

Read `AGENT_HANDOFF.md` before interpreting `git status`. Never infer ownership from a dirty worktree alone.

If collaboration is paused via `.cli-collaboration-off` or `Status: paused` in the handoff, still preserve existing work, obey `## File ownership`, and ask before touching shared files.

## Script Resolution

Bundled scripts live inside this skill's directory (`<SKILL_DIR>/scripts/`), not necessarily inside the target repository:

- [check-ownership.sh](./scripts/check-ownership.sh)
- [lang.sh](./scripts/lang.sh)
- [hook-guard.py](./scripts/hook-guard.py)
- [install-skill.sh](./scripts/install-skill.sh) / [sync-skill.sh](./scripts/sync-skill.sh)

Resolve `<SKILL_DIR>` from the location of this `SKILL.md`. Never assume `scripts/` exists in the active project root.

## Language Preference

Run this once at activation so the session speaks the user's chosen language:

1. Run `<SKILL_DIR>/scripts/lang.sh get`.
2. **If it prints a value (exit 0):** continue in that language. Do not ask again.
3. **If it exits `3` (not configured):** ask the user in English (`Choose your language:`), then run `<SKILL_DIR>/scripts/lang.sh set "<answer>" --by <AGENT_NAME>` (or `--local` for project-only `.cli-collaboration.json`).
4. **If `set` exits `4` (read-only or sandboxed `$HOME`, e.g., Antigravity or Codex sandboxes):** never bypass the sandbox or request elevated access just to save language config; continue in the user's prompt language (or set `CLI_COLLAB_LANG`).

Non-interactive CI runs use `<SKILL_DIR>/scripts/lang.sh ensure-noninteractive`.

## Start Gate

Before editing any file, state explicitly:

```text
Handoff read: <path, last-updated timestamp>
Current task: <one line>
Files I will touch: <explicit file list>
Expected red test: <test name, or no test with reason>
Reserved zones confirmed: <user-reserved/frozen areas>
Stop condition: <task-complete | context-budget | blocker>
```

If you cannot fill a field, read more or ask. Do not improvise.

## Bootstrap Without Handoff

If no handoff exists, create or propose `AGENT_HANDOFF.md` using [references/handoff-template.md](./references/handoff-template.md) before normal work. Include the user's request, current path, `git status --short --branch` if available, declared ownership, and the next concrete action. Mark `Status: bootstrap`.

If `AGENT_HANDOFF.md` is missing but a workflow seed file such as `brainstorming.md` exists, read that seed file first and load [references/alternate-workflows.md](./references/alternate-workflows.md). Load alternate workflow docs only when explicitly requested or declared.

## Ownership

Use this exact line shape under `## File ownership`:

```text
- <path-or-glob>: <agent-name> — <reason>
```

Required subsections (keep all three headings even when empty):

- `### agent-owned`: files assigned to `Codex`, `Claude`, `Gemini`, `Grok`, `Antigravity`, or another named agent.
- `### user-reserved`: user-owned files. Stop before editing.
- `### frozen`: protected files. Stop before editing.

**Agent Identity & Normalization:** Canonical names are `Codex`, `Claude`, `Gemini`, `Grok`, and `Antigravity`. Keep `Antigravity` distinct from `Gemini` / `Gemini CLI`. Common aliases (`Claude Code`, `Gemini CLI`, `OpenAI Codex`, `Grok Build`, `Antigravity IDE`, `agy`) and parenthetical notes normalize automatically in `check-ownership.sh`.

**Globs & Paths:** Patterns use bash `case` semantics where `*` matches `/` (`scripts/*` covers `scripts/sub/foo.sh`; `**` is not special). `check-ownership.sh` strips `./` prefixes and relativizes absolute paths inside the handoff directory automatically.

Run `<SKILL_DIR>/scripts/check-ownership.sh --agent <name> <files...>` before editing near ownership boundaries. Exit `0` = clear, `1` = conflict, `2` = malformed handoff or usage error.

## Conflict Handling

When a file is owned by someone else, `user-reserved`, `frozen`, or unexpectedly changed:

1. Stop before editing.
2. Name the file, owner, and risk.
3. Offer reassignment, deferment, or a smaller scope.
4. Wait for the user or owning agent to decide.

Never resolve ownership conflicts by overwriting, reverting, stashing, or cleaning.

## Work Discipline

- Keep edits inside declared files; announce any newly required file before editing.
- Prefer small complete increments and precise handoffs over half-finished broad refactors.
- A failing test is a valid handoff artifact; record it, never delete or skip it to look green.
- Single-agent sessions still maintain `AGENT_HANDOFF.md` as cross-session memory.
- **Single-writer rule:** only one parent/coordinator session updates `AGENT_HANDOFF.md`; parallel subagents or Antigravity swarms report files and tests back to the coordinator instead of editing concurrently.

## User Supersession

The user's latest instruction wins. If scope changes mid-turn, adjust `Files I will touch` before editing new files and record a brief supersession note in the final handoff.

## Destructive Actions

Never run or recommend these without explicit user approval:

- `git reset --hard`
- `git clean`
- `git stash`
- `git restore`
- `git checkout --`
- lateral overwrite of files you did not author

## Adapters & Deterministic Hooks

Load only the adapter relevant to your active runtime:

- [references/codex-adapter.md](./references/codex-adapter.md): Codex install paths, `AGENTS.md`, and script ABI.
- [references/claude-adapter.md](./references/claude-adapter.md): Claude Code hooks (`SessionStart`, `PreToolUse`), commands, and `CLAUDE.md`.
- [references/gemini-adapter.md](./references/gemini-adapter.md): Gemini CLI `activate_skill`, `.agents/skills` precedence, and `BeforeTool` hooks.
- [references/grok-adapter.md](./references/grok-adapter.md): Grok Build discovery, tools, Bluefin paths, and `Grok` identity.
- [references/antigravity-adapter.md](./references/antigravity-adapter.md): Antigravity IDE / App 2.0 / `agy` CLI rules budget, Plan Mode, swarms, and `hooks.json`.

For deterministic enforcement of `SessionStart` injection, `PreToolUse` ownership/destructive-git guards, and `Stop` checks, configure [hook-guard.py](./scripts/hook-guard.py) (see `examples/hooks/`). For semantic pitfalls and pressure tests, see [references/handoff-anti-patterns.md](./references/handoff-anti-patterns.md) and [references/validation-scenarios.md](./references/validation-scenarios.md).

## End Of Shift

Update `AGENT_HANDOFF.md` last so its structure matches [references/handoff-template.md](./references/handoff-template.md) and `evals/lint-handoff.py`:

```markdown
**Last updated:** <ISO 8601 timestamp with timezone>
**Last agent:** <Codex | Claude Code | Gemini CLI | Grok | Antigravity | other>
**Status:** <bootstrap | in-progress | done | blocked | paused>

## Current task
<One paragraph describing what this shift delivered.>

## Files changed this shift
- <path>: <one-line summary>

## Tests
- Red: <name + failure mode, or "none">
- Green: <name, or "none ran">

## Open concerns
- <Concrete risk or unfinished thread; never write "all good".>

## Next agent starts from
<Exact next step with file:line, expected agent, and "Do not touch:" list.>

## History
- <ISO 8601 timestamp with timezone> - <agent>: <one-line shift summary> (<status>)
```

Keep the last three detailed shift contexts useful and summarize older entries into single `## History` lines as the file grows.
