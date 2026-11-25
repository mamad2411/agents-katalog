---
name: whats-new
description: Explain what changed in Operator Powers, which version is installed, whether a newer release exists, and how to update.
---

# What's New

## The Job

Tell the user what their installed version contains, what changed recently, and whether something newer exists.

## How to Run It

1. Read the installed release metadata at `${CLAUDE_PLUGIN_ROOT}/catalog/release.json` (fall back to `catalog/release.json` two directories above this skill file). That file states the installed version and its changelog entries.
2. Present the installed version and its changes in plain language, newest first: new powers as jobs ("you can now turn a meeting into a deliverable"), then improvements, then fixes. Skip internal or build-only changes. When a release entry credits user input (feedback or requests), lead with that: this collection is self-improving, and "this exists because users asked for it" is the most important line in any release.
3. If the `operator_powers` MCP server is connected, you may call `get_whats_new` with the installed version to learn about releases newer than the installed one. If something newer exists, say what it adds and how updating works: "updates arrive through your marketplace; refresh it and update the plugin, then start a new session."
4. If the service is unreachable, show the installed changelog and say plainly that live release information was unavailable, without guessing whether an update exists.

## Boundaries

- Never claim a newer skill is already installed; live catalogue data describes what an update would bring.
- Never promise instant updates; the user's client controls when updates apply.
- The only data sent to the service is the installed version number, and only when live information is wanted.
