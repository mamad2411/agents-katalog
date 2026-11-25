---
name: cgx-selector
description: Apply the selector profile bundled with this plugin, then enter the shared Cognigrex handshake without creating a new agent, runtime, filespace, or authority.
---

# CGX Selector

Read `references/selector.json` first.

The selector profile supplies defaults only. It answers one of:
- which actor should lead the reasoning lens,
- which domain/filespace should be resolved,
- which existing system/runtime surface should be used.

Then invoke the shared `cgx-handshake` workflow.

## Rules

- Explicit user choices override selector defaults where current authority permits.
- Combining an agent selector with a domain selector changes the reasoning lens and domain context; it does not transfer domain authority.
- Never instantiate a duplicate agent or create a parallel Cognigrex/LightSpeed runtime.
- Never treat the selector profile as canonical state. Resolve live .cgx/Recovery state through the handshake.
- If the requested task is already answered by a valid receipt/result, return that result rather than executing again.
- If compatible prior results can validly derive the requested state, reconcile them rather than launching a wider test/sweep.
- When execution is required, use the minimum appropriate existing surface and return a compact receipt.
