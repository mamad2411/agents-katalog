---
name: "source-command-kb-refresh"
description: "Run the full documentation audit and refresh pipeline on a repository: inventory, writer fleet, grounded citations, adversarial verification, security and quality gates, one ready PR per unit, then the work report in PDF plus markdown and the master suspect list. Trigger with \"refresh the docs\", \"kb refresh\", \"rebuild the knowledge base\", \"doc swarm\"."
license: "AGPL-3.0-or-later"
disable-model-invocation: true
---

# source-command-kb-refresh

Use this skill when the user asks to run the migrated source command `kb-refresh`.

Read [the command procedure](../../commands/kb-refresh.md) in full before acting. Resolve paths in that procedure relative to its `commands/` directory. Codex invokes this as a skill, not a slash command.
