---
name: OpenCode V2
description: Work with OpenCode V2 itself — opencode.jsonc config, skills, agents, commands, plugins, and the OpenCode SDK. Use when the user asks about OpenCode setup, customization, integration, or invokes /opencode. V2 only.
---

# OpenCode V2

Use this skill when the task is about OpenCode itself: configuring `opencode.jsonc`,
scaffolding skills/agents/commands, wiring plugins, or building integrations with the
OpenCode SDK/clients/API.

## Hard rule: V2 only

- Source of truth: <https://v2.opencode.ai/> and its `llms.txt` index.
- V1 docs (<https://opencode.ai/docs/>) and <https://opencode.ai/config.json> describe V1 — do NOT use them to infer V2 field names.
- If V2 docs are missing or contradictory, say so instead of falling back to V1.

## Project layout (OpenCode V2)

| Scope                 | Sources                                |
| --------------------- | -------------------------------------- |
| Global                | `~/.config/opencode/`                  |
| Global compatibility  | `~/.claude/`, `~/.agents/`             |
| Project               | `.opencode/`                           |
| Project compatibility | `.claude/`, `.agents/`                 |

Subdirectories under `.opencode/`:

- `opencode.jsonc` — main config (include `"$schema": "https://opencode.ai/config.json"`).
- `agents/<name>.md` — custom agents (frontmatter + Markdown body = `system`).
- `skills/<name>/SKILL.md` — skills (frontmatter: `name`, `description`; optional `metadata: { opencode/slash: "true" }`).
- `commands/<name>.md` — slash commands (frontmatter: `description`, `agent`, `model`; body is the prompt template).
- `plugins/` and provider/model config as documented.

## Agents (V2 frontmatter fields)

`description`, `mode` (`primary` | `subagent` | `all`), `model` (`provider/model#variant`),
`system` (or Markdown body), `color`, `steps` (max model steps), `hidden`, `disabled`,
`permissions`, `request` (headers/body overlay — currently preserved but not applied).

Permissions are ordered rules; **last matching rule wins**:

```yaml
permissions:
  - action: edit       # covers write/edit/patch
    resource: "*"
    effect: deny
  - action: shell      # shell commands (raw command text, no ~ expansion)
    resource: "git push *"
    effect: ask
  - action: subagent   # child agents
    resource: "explore"
    effect: allow
```

Put broad wildcards first, exceptions after. Other tool actions: `read`, `glob`, `grep`, `webfetch`, `websearch`, `skill`.

## Commands (V2)

- Markdown body is the template. Use `$ARGUMENTS` for the full arg string, or `$1` `$2` … for positional args (highest number consumes the rest).
- Shell interpolation: wrap a command in `!` + backticks, e.g. `!`git diff --stat``. Runs at evaluation time, outside the agent permission flow — only use trusted sources.
- `agent` / `model` override the session before the prompt runs. `subtask` is accepted but currently ignored (commands run in the current session).

## Workflow when the user asks to extend OpenCode

1. Decide the artifact: config change, skill, agent, or command.
2. Read the relevant V2 doc page before writing.
3. Propose the change, then apply it minimally and V2-valid.
4. Never write V1-style fields (`temperature`, `top_p`, `tools`, `maxSteps`, `permission`, `disable`) at the top level.
