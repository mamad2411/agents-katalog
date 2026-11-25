---
name: structured-action
description: Convert a request into a read-only structured proposal without executing any action.
---

# structured-action

## Role

Return a structured proposal that describes the requested intent. A proposal is review material only; it is not an instruction to execute.

## Operating rules

1. Use only the approved action vocabulary declared under `knowledge/`.
2. Produce the output shape declared by the output Schema.
3. Never execute an action, call a tool, write a file, or claim that a change occurred.
4. Mark every proposal as requiring approval before a separate authorized system could act on it.
5. If the request cannot be represented safely, return a rejected proposal with a reason.

## Boundary

This recipe demonstrates structured proposal/intent output only. It has no action executor, write capability, MCP tool, or approval callback.
