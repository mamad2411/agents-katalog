---
name: careful
description: Destructive-action guardrail for Codex. Use when the user wants extra caution around risky commands, production work, or irreversible changes.
---

# Careful

Use this skill when the work touches destructive commands, production systems, or changes that are hard to undo.

This port is adapted from `garrytan/gstack` at commit `94993f74012782fd94416dd44b8314f6363a13a4`.

## Protected Actions

Treat deletion, force-pushes, history rewrites, production mutations, credential changes, destructive database operations, and bulk replacement of user-authored files as protected actions. Inspect first, state the exact blast radius, and require an explicit user decision when the action is irreversible or materially broader than the request.

Safe read-only inspection, creation of new reversible artifacts, and narrowly scoped edits inside the authorized workspace do not need an extra confirmation merely because they use a shell command.

## Workflow

1. Identify the risky action before taking it.
2. State the specific risk plainly.
3. Prefer a safer alternative when one exists.
4. If the destructive action is still the right move, make the minimum necessary change and verify the result immediately.

## Guardrails

- Never treat destructive commands as routine.
- Treat chained commands, command substitution, and both lowercase `-r` and
  macOS/BSD uppercase `-R` as part of the destructive-command review. A safe
  final path does not make an earlier command or substituted path safe.
- Prefer reversible operations over irreversible ones.
- Be especially cautious around production, shared branches, and data deletion.
