---
description: One maintenance sweep for the whole OS. Say "run housekeeping", "clean up the OS", or "what maintenance is due" (or run /founder-os:housekeeping). Default is detect - read-only, every piece of accumulated debt on one screen with its fix command. Pass "fix" to run the safe reversible fixes in dependency order and get back a punch-list of the judgment calls plus a verify table. The remediation companion to the read-only /founder-os:audit.
argument-hint: "[fix]"
---

# Housekeeping

Run the `housekeeping` skill (`skills/housekeeping/SKILL.md`) exactly as written.

- `$ARGUMENTS` empty -> Detect mode: read-only sweep, render the DETECT block, write nothing.
- `$ARGUMENTS` is `fix` -> Fix mode: run the AUTO fixes in the skill's dependency order, then the FIX block with punch-list and verify table.
- Any other argument -> reply `Usage: /founder-os:housekeeping [fix]` and stop.
