---
name: cds-set-profile
description: "Switch model profile for GSD agents (quality/balanced/budget/inherit)"
argument-hint: "<profile (quality|balanced|budget|inherit)>"
allowed-tools:
  - Bash
---


Show the following output to the user verbatim, with no extra commentary:

!`node "$HOME/.claude/cds-workflow/bin/gsd-tools.cjs" config-set-model-profile $ARGUMENTS --raw`
