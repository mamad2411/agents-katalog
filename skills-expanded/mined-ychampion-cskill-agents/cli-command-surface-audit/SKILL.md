---
name: cli-command-surface-audit
description: "Audit a command surface end to end so registration, discoverability, permissions, and execution all line up before shipping."
metadata:
  author: ychampion
---

# SKILL: CLI Command Surface Audit
**Domain:** command-surfaces  
**Trigger:** Use when adding, migrating, or debugging commands or slash-command skills in a coding CLI that builds its surface from multiple registries.  
**Source Pattern:** Distilled from reviewed command-surface, help-menu, and execution-path consistency implementations.

## Core Method
Audit the entire command surface, not just the handler. Confirm where the command is registered, how it is filtered, how it is described to users, and which runtime modes can actually execute it. Check help output, skill pickers, slash-command lookup, remote-safe filtering, and user-invocable flags against the real execution path. A command is only complete when the same name, description, permissions, and invocation contract stay aligned across all of those layers.

## Key Rules
- Verify both visibility and executability; a command that only exists in code is still broken.
- Audit registration order and source precedence before debugging the handler itself.
- Check feature gates, permission filters, and remote-safe filters separately because each can hide the command for a different reason.
- Keep the displayed description and argument hint consistent with the actual invocation contract.
- Exercise at least one real end-user invocation path after wiring the command in.

## Example Application
If you add a new slash command to a coding CLI, trace it from registry construction to help output to command execution. Confirm it survives the feature gate, appears in the skill list with the right summary, remains visible in the modes that should expose it, and actually dispatches through the same runtime path the user will hit.

## Anti-Patterns (What NOT to do)
- Don’t stop after the handler compiles; the command may still be absent from the visible surface.
- Don’t assume a help entry means the command is executable under the current permission or runtime mode.
- Don’t let multiple registries describe the same command differently.
