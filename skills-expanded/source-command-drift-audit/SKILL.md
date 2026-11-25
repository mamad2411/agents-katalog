---
name: "source-command-drift-audit"
description: "Validate every Wasp Nest component and diff the pest-controller-suit roster against the filesystem in both directions, check pairing integrity, guide coverage, dead references, stale paths, prose dash violations, and Cowork upload readiness, then produce a findings report with a prioritized fix list. Trigger with \"audit the nest\", \"drift check\", \"is the roster in sync with the filesystem\", \"find orphaned drones\", \"check for unregistered skills\"."
license: "AGPL-3.0-or-later"
disable-model-invocation: true
---

# source-command-drift-audit

Use this skill when the user asks to run the migrated source command `drift-audit`.

Read [the command procedure](../../commands/drift-audit.md) in full before acting. Resolve paths in that procedure relative to its `commands/` directory. Codex invokes this as a skill, not a slash command.

This command maintains The Wasp Nest itself. Require a writable source checkout and read its live `src/commands/drift-audit.md` before making changes; never edit the installed plugin cache.
