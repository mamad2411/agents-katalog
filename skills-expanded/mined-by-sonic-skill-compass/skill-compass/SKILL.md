---
name: skill-compass
description: >-
  Install, configure, and operate the skill-compass hooks for Claude Code —
  UserPromptSubmit + PostToolUse hooks that route to the right skills/agents from
  three signals: the project's composition (languages, frameworks, config files),
  project/topic keywords in your prompt, and keywords the AI surfaces mid-turn via
  Bash/Grep/Glob/Read/Task (UI → design, API → api-design, DB → db-patterns, Auth,
  LLM, infra, plus named projects/topics).
  Use this skill whenever the user wants to install, set up, enable, disable, or
  uninstall skill-compass; edit or inspect its routing rules in directions.json;
  add a new stack→direction mapping; run its --self-test; or debug why the hook
  is/isn't suggesting skills. Trigger on mentions of "skill-compass", "the
  compass hook", "skill router/dispatcher", "directions.json", "UserPromptSubmit
  hook that suggests skills", or "auto-suggest skills based on my project" — even
  if the user doesn't name the file explicitly.
---

# skill-compass

`UserPromptSubmit` + `PostToolUse` hooks for Claude Code. They route to the right
skills/agents from three signals: the working directory's composition (languages,
frameworks, config files), project/topic keywords in your prompt, and keywords the
AI surfaces mid-turn (a `Bash`/`Grep`/`Glob`/`Read`/`Task` result). E.g. UI files →
frontend-design, API routes → api-design, a `Dockerfile` → infra, "find the
clickhouse migration" → the database skills. It nudges the model toward the right skill instead of
relying on memory.

## Layout (this repo)

Run paths are relative to the repo root (the parent of `skill/`):

- `compass.js` — the hook engine (handles both events). Flags: `--self-test`, `--force`, `--post` (PostToolUse mode). Disable per-session with env `SKILL_COMPASS=off`.
- `directions.json` — the routing table: maps detected stacks/files → suggested directions. **This is the file users edit.**
- `install.js` — installer. Copies `compass.js` + `directions.json` into `~/.claude/skill-compass/` and registers both the `UserPromptSubmit` and `PostToolUse` hooks in `~/.claude/settings.json`. Idempotent. `--uninstall` removes both hooks.

After install the live copy runs from `~/.claude/skill-compass/`, so edits to the
installed `directions.json` survive re-installs (the installer keeps an existing
one).

## Tasks

### Install / enable the hook

Run from the repo root:

```
node install.js
```

It copies files, registers the hook, and prints the test command. Tell the user
to **restart Claude Code** afterward — the hook is loaded at process start. If
they re-run it, it's a no-op (idempotent), which is the expected, safe outcome.

### Uninstall / disable

- Permanent removal: `node install.js --uninstall` (strips the hook from `settings.json`, leaves files in place).
- Temporary, one session: set `SKILL_COMPASS=off` in the environment before launching Claude Code.

### Inspect or edit routing rules

`directions.json` is the source of truth for what gets suggested. To see current
rules, read it. To change behavior, edit it directly. After editing the
*installed* copy at `~/.claude/skill-compass/directions.json`, no reinstall is
needed — the running hook reads it fresh.

When adding a new stack→direction mapping, match the existing entries' shape (a
detector for the stack and the direction text it emits). After any edit, always
run the self-test below to confirm nothing broke.

### Run the self-test

This is the verification step before claiming any change works:

```
node compass.js --self-test
```

It exercises stack detection, direction routing, and the empty-project guard,
then prints `ALL PASSED` (non-zero exit on failure). If a user reports the hook
mis-suggesting, reproduce by adding or adjusting a case here first — a failing
self-test case localizes the bug before you touch the engine.

### Debug "it's not suggesting anything"

Walk these in order:
1. Hooks registered? Check `~/.claude/settings.json` → `hooks.UserPromptSubmit` and `hooks.PostToolUse` each contain a command with `skill-compass` (the PostToolUse one ends with `--post`).
2. Disabled? Check the `SKILL_COMPASS` env var isn't `off`.
3. Restarted? Hooks only load at Claude Code startup.
4. Empty/at-root project? With no stack manifest, no prompt keyword and no mid-turn tool finding, the engine intentionally stays silent (junk-drawer guard) — `cd` into a real project, mention a project/topic keyword, or pass `--force`.
