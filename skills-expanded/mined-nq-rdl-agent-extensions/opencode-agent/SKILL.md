---
name: opencode-agent
license: CC-BY-4.0
compatibility: >-
  OpenCode agent, command, and rules config (markdown frontmatter or opencode.json);
  checked against v1.18.33 docs and source on 2026-09-29.
description: >-
  Write OpenCode agents, custom commands, and AGENTS.md rules — files in
  `.opencode/agents/` or `.opencode/commands/`, or the `agent`, `command`, and
  `instructions` keys. Use for `mode`, `steps`, per-agent `permission`,
  `$ARGUMENTS`/`!cmd`/`@file` templates, the CLAUDE.md fallback, or a stale
  `tools:`/`maxSteps`/modes setup. Not Claude Code subagents or OpenAI Codex.
argument-hint: "What agent/command/rule do you want to build? (e.g. 'a read-only review subagent', 'a /test command with args', 'why is my CLAUDE.md ignored')"
user-invocable: true
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# OpenCode agents, commands & rules

OpenCode's (opencode.ai; not OpenAI Codex) config-as-markdown surface: **agents** (specialized assistants),
**custom commands** (reusable prompt templates), and **rules** (`AGENTS.md`
project instructions). All three are plain markdown-with-frontmatter or JSON keys
in `opencode.json` — no code required.

> **Verify-canonical guard.** OpenCode's API moves fast and predates the model's
> training cutoff — before writing agent/command/rule config, read
> `references/agents.rst`, `references/commands.rst`, or `references/rules.rst` AND
> re-check <https://opencode.ai/docs/agents/> (and `/docs/commands/`, `/docs/rules/`)
> for drift. The traps below are the deltas a fresh model gets wrong. The `/docs/modes/`
> 404, the singular-directory globs, and the config merge order were checked on
> 2026-09-29 against the live site, v1.18.33 source (`config/agent.ts`,
> `config/command.ts`), and `/docs/config/`.

---

## The traps (what a fresh model gets wrong)

| Trap | Wrong (don't) | Right (do) |
|------|---------------|------------|
| **Modes are gone** | Looking up `/docs/modes/` — it **404s** | `mode` is now an **agent field**: `primary` \| `subagent` \| `all` (default `all`). Legacy `.opencode/modes/*.md` still load as primary agents |
| **`tools:` deprecated** | `tools: { write: false }` per agent | Use `permission:` (`allow`/`ask`/`deny`); `tools` still parses but is legacy |
| **`maxSteps`** | `maxSteps: 5` | `steps: 5` — `maxSteps` is **deprecated** |
| **Dir is plural** | `.opencode/agent/`, `.opencode/command/` | `.opencode/agents/`, `.opencode/commands/` (singular accepted for back-compat only) |
| **Filename = name** | `description:` sets the id | The **markdown filename** is the documented id: `review.md` → `review` agent; `test.md` → `/test` command. Don't add a `name:` key: v1.18.33 lets it silently replace the filename id (undocumented) |
| **No CLAUDE.md fallback awareness** | Assuming only `AGENTS.md` is read | OpenCode falls back to `CLAUDE.md` / `~/.claude/CLAUDE.md` when no `AGENTS.md` |

Read `references/*.rst` before writing — these are the only non-obvious bits.

---

## Agents

Two types. **Primary** = main assistant you drive (Tab / `switch_agent` keybind to
cycle); **subagent** = invoked by a primary or by `@mention`. Built-in primaries:
`build` (all tools), `plan` (`edit`+`bash` default to `ask`). Built-in subagents:
`general`, `explore`, `scout`. Declare in `opencode.json` under the `agent` key, or
as one markdown file per agent in **plural** `.opencode/agents/` (project) or
`~/.config/opencode/agents/` (global). **The filename is the agent name.**

Frontmatter fields (see `references/agents.rst` for the full table):

| Field | Notes |
|-------|-------|
| `description` | **Required.** What it does / when to use it (drives auto-invocation) |
| `mode` | `primary` \| `subagent` \| `all` — defaults to `all` |
| `permission` | **Preferred** access control — per-tool `allow`/`ask`/`deny`, or `{pattern: level}` |
| `steps` | Max agentic iterations (**not** `maxSteps`) |
| `prompt` | System prompt — inline string or `{file:./prompts/x.txt}` (relative to config) |
| `disable` / `hidden` / `color` | Off / hide from `@`-menu (subagents only) / UI color |
| `tools` | **Deprecated** — migrate to `permission` |

`permission` keys, their shapes, and defaults are owned by `/opencode-dev:policies`.
Two traps matter while writing an agent: `edit` covers **`write` + `edit` +
`apply_patch`**, and the **last matching rule wins** — put `"*"` first, exceptions
after. `permission.task` (a glob map) controls which
subagents this agent may invoke via the Task tool. Per-agent `permission` overrides
top-level. Scaffold interactively with `opencode agent create`. See
`assets/agent.md`.

## Custom commands

Markdown files in **plural** `.opencode/commands/` (or `~/.config/opencode/commands/`)
— **filename = command name** (`test.md` → `/test`). The body is the **prompt
template**; frontmatter configures it. JSON form lives under the `command` key and
**requires `template`** (the body equivalent).

Frontmatter / JSON fields: `description`, `agent` (which agent runs it — if that's a
subagent, it triggers a subagent invocation **by default**), `subtask` (`true` forces
subagent even for a `primary` agent; `false` disables the auto-subtask), `model`.

Template syntax (in the body / `template`):

- `$ARGUMENTS` — all args; `$1`, `$2`, `$3`, … — positional args.
- Shell output: an exclamation mark written directly before a backtick-quoted command
  runs in the **project root** and splices stdout into the prompt. The literal form is in
  `assets/command.md`; it is spelled out in words here because Claude Code runs that
  pattern as a shell command when it loads a skill body.
- `@path/to/file` — includes file content in the prompt.

Built-ins `/init`, `/undo`, `/redo`, `/share`, `/help` are **overridable** by a
same-named custom command. See `assets/command.md`.

## Rules (AGENTS.md)

Project instructions go in `AGENTS.md` at the repo root (commit it; `/init`
generates/updates it). Global rules: `~/.config/opencode/AGENTS.md`.

**Claude Code compatibility (the key delta):** when no `AGENTS.md` exists, OpenCode
falls back to `CLAUDE.md` (project) and `~/.claude/CLAUDE.md` (global). Precedence on
startup: (1) local files walking **up** from cwd (`AGENTS.md`, then `CLAUDE.md`),
(2) global `~/.config/opencode/AGENTS.md`, (3) `~/.claude/CLAUDE.md`. **First match
wins per category** — if both `AGENTS.md` and `CLAUDE.md` exist, only `AGENTS.md` is
used. Disable the fallback with env vars:

```bash
export OPENCODE_DISABLE_CLAUDE_CODE=1        # all .claude support
export OPENCODE_DISABLE_CLAUDE_CODE_PROMPT=1 # only ~/.claude/CLAUDE.md
export OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1 # only .claude/skills
```

Add extra instruction files via the `instructions` config key (globs + remote URLs;
URLs fetched with a 5s timeout) — these **combine** with `AGENTS.md`:

```json
{ "$schema": "https://opencode.ai/config.json",
  "instructions": ["CONTRIBUTING.md", "docs/guidelines.md", "packages/*/AGENTS.md"] }
```

> `AGENTS.md` does **not** auto-parse `@file` references — use `instructions` for
> file inclusion, or write explicit "Read @x on demand" prose in the body.

---

## Config & precedence (shared)

Config files **merge** (later overrides earlier): remote `.well-known/opencode` →
global `~/.config/opencode/opencode.json` → `OPENCODE_CONFIG` → project
`opencode.json` → `.opencode/` dirs → `OPENCODE_CONFIG_CONTENT` → managed files.
Substitution: `{env:VAR}`, `{file:path}`. Full model: `/docs/config/`.

## References

| File | Source |
|------|--------|
| [references/agents.rst](references/agents.rst) | `/docs/agents/` — frontmatter, permission table, built-ins, `opencode agent create` |
| [references/commands.rst](references/commands.rst) | `/docs/commands/` — templating, `$ARGUMENTS`/`!cmd`/`@file`, JSON `template` |
| [references/rules.rst](references/rules.rst) | `/docs/rules/` — `AGENTS.md`, `CLAUDE.md` fallback, `instructions` key |

## Assets

| File | What it is |
|------|------------|
| [assets/agent.md](assets/agent.md) | A read-only review subagent (markdown, `permission`-based) |
| [assets/command.md](assets/command.md) | A `/test` command using `$ARGUMENTS`, shell-output injection, and `@file` |
