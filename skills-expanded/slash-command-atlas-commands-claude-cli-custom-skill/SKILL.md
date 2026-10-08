# `/<skill-name> [ARGUMENTS]`

> Invokes a user, project, or plugin skill by its discovered name.

- **Product:** Claude Code
- **Surface:** Claude Code CLI
- **Category:** Customization authoring
- **Data snapshot:** 2026-09-14
- **Flags:** custom

## What it does

Invokes a user, project, or plugin skill by its discovered name.

Skills in `~/.claude/skills/` and `.claude/skills/` become commands. Legacy Markdown files in `.claude/commands/` still work, and plugins use namespaced commands. Current builds can chain as many as six skills at the start of one prompt. These are dynamic, so the Atlas does not pretend to enumerate your installation.

## Canonical example

`/review-api src/auth`

## Related commands

- [`/skills`](./skills.md)
- [`/reload-skills`](./reload-skills.md)
- [`/plugin`](./plugin.md)
- [`/mcp__<server>__<prompt>`](./mcp-prompt.md)

## Official sources

- [Extend Claude Code with skills](https://code.claude.com/docs/en/skills)
- [Claude Code CLI slash command reference](https://code.claude.com/docs/en/commands)

## Atlas links

- [Interactive command view](https://codylindley.github.io/slash-command-atlas/#/claude-cli/custom-skill)
- [All commands as JSON](https://codylindley.github.io/slash-command-atlas/data/commands.json)
- [AI-readable command index](https://codylindley.github.io/slash-command-atlas/llms.txt)

---

This page is generated from the Slash Command Atlas data files. Longer explanations and use-case guidance are editorial; linked vendor documentation is authoritative.
