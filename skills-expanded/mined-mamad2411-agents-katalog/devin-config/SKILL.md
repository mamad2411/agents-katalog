---
name: devin-config
description: Use when evolving the agent's capabilities with a new skill, custom subagent, plugin, hook, MCP server, or project rule — or when auditing/managing a project's `.devin/` configuration, producing deterministic read-only reports, detecting broken references/duplicates/divergences, and generating plans that persist under `.devin/` only after approval.
triggers: [user, model]
---

# Devin Config

Extend Devin CLI (devin-config) and audit `.devin/` (devin-config). Files go
to the project (`./.devin/`) or global config (`~/.config/devin/` /
`%APPDATA%\devin\`). Most changes load at next session/reload.

## What to create for each need

| I want to... | Create | Location | Reload |
|---|---|---|---|
| Reusable invocable workflow | Skill | `.devin/skills/<name>/SKILL.md` or `~/.config/devin/skills/<name>/SKILL.md` | next `skill list` |
| Specialized worker profile | Custom subagent | `.devin/agents/<name>.md` or `<name>/AGENT.md` (global: `~/.config/devin/agents/`) | next session |
| Always-on context | Rules | `.devin/global_rules.md`, `.devin/rules/*.md` (global: `~/.config/devin/AGENTS.md`) | session start |
| Lifecycle logic | Hooks | `.devin/hooks.v1.json` | next session |
| API/DB tools | MCP server | `.devin/mcp_config.json` or `~/.config/devin/mcp_config.json` | next session |
| Distributable bundle | Plugin | `.devin-plugin/plugin.json` + skills/rules/hooks/mcp | install/reload |

## Creating skills

Before writing any skill/rule, follow `writing-skills` conventions
(frontmatter, discovery keywords, completion criteria).

```markdown
---
name: my-skill
description: Use when [specific triggering conditions]
---
```

Optional frontmatter: `allowed-tools`, `subagent: true`, `agent: <profile>`,
`model` (free variants only — `swe-2-max`/`swe-2-medium`, never paid),
`permissions` (`allow`/`deny`), `triggers` (default `[user, model]`).

Discover: `skill list --path .`, `skill search --path . --keywords "..."`.
Invoke: `/my-skill`.

## Custom subagents

`.devin/agents/reviewer.md` or `.devin/agents/reviewer/AGENT.md`:

```markdown
---
name: reviewer
---
You are a careful code reviewer. Report concrete issues with file:line only.
```

Reference via skill frontmatter `agent: reviewer`, or dispatch a
`subagent_general`/`researcher` subagent (never `subagent_explore` on a free
parent — it may route to a paid model).

## Rules

`.devin/global_rules.md` + `.devin/rules/*.md` load by default — keep them
small, detail lives in skills. `.devin/rules/*.md` support `trigger`
frontmatter (`always_on`, `manual`, `model_decision`, `agent`, `glob`).

## Hooks

`.devin/hooks.v1.json`. Events: `PreToolUse`, `PostToolUse`,
`PermissionRequest`, `UserPromptSubmit`, `Stop`, `SessionStart`,
`SessionEnd`, `PostCompaction`. Command hooks run a shell command; prompt
hooks run an LLM evaluation per event.

## MCP servers

`.devin/mcp_config.json` (project) / `~/.config/devin/mcp_config.json`
(global). Audit cost and trust review first with `mcp-governance`.

## Auditing `.devin/` (devin-config mode)

Deterministic, read-only ops via `scripts/devin-manager.py` (this skill's
`scripts/`). Notes persist only under `.devin/notes/devin-config/` and only
with `--write --approve`.

| Op | Purpose |
|---|---|
| `scan` | Inventory `.devin/` + `agents/` + `mcp_config.json` with sha256, provenance, frontmatter, references |
| `explain` | One artifact and its outgoing references |
| `diff` | Compare two `.devin/` states by hash |
| `doctor` | Broken refs, duplicate content/skill names, config/hook divergences |
| `plan` | Plan note from doctor findings |

```bash
python skills/devin-config/scripts/devin-manager.py scan [PROJECT]
python skills/devin-config/scripts/devin-manager.py doctor [PROJECT]
python skills/devin-config/scripts/devin-manager.py diff [A] [B]
```

Approval rule: editing `.devin/config.json`, hooks, or memory requires
explicit user approval — reports are read-only by default.
