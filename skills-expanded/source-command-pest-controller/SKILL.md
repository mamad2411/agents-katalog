---
name: "source-command-pest-controller"
description: "Orchestrate the Wasp Swarm. Routes a task through the pest-controller-suit roster and dispatches wasp-drone sub-agents, each armed with its paired Stinger skill before it starts."
license: "AGPL-3.0-or-later"
disable-model-invocation: true
---

# source-command-pest-controller

Use this skill when the user asks to run the migrated source command `pest-controller`.

Read [the command procedure](../../commands/pest-controller.md) in full before acting. Resolve paths in that procedure relative to its `commands/` directory. Codex invokes this as a skill, not a slash command.
