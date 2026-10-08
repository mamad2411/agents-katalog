# `/<skill name> [CONTEXT]`

> Runs one of your own agent skills by name.

- **Product:** GitHub Copilot
- **Surface:** GitHub Copilot Chat in VS Code
- **Category:** Customization authoring
- **Data snapshot:** 2026-09-14
- **Flags:** custom

## What it does

Runs one of your own agent skills by name.

For example, `.github/skills/webapp-testing/SKILL.md` with `name: webapp-testing` exposes `/webapp-testing`. The name must match the directory. `user-invocable: false` hides it from the menu; plugin-distributed skills receive a plugin-name prefix automatically. Optional text after the command provides task context.

## Canonical example

`/webapp-testing`

## Related commands

- [`/skills`](./skills.md)
- [`/create-skill`](./create-skill.md)
- [`/<prompt name>`](./custom-prompt.md)

## Official sources

- [Agent skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [GitHub Copilot Chat in VS Code slash command reference](https://code.visualstudio.com/docs/agents/reference/ai-features-cheat-sheet)

## Atlas links

- [Interactive command view](https://codylindley.github.io/slash-command-atlas/#/vscode/custom-skill)
- [All commands as JSON](https://codylindley.github.io/slash-command-atlas/data/commands.json)
- [AI-readable command index](https://codylindley.github.io/slash-command-atlas/llms.txt)

---

This page is generated from the Slash Command Atlas data files. Longer explanations and use-case guidance are editorial; linked vendor documentation is authoritative.
