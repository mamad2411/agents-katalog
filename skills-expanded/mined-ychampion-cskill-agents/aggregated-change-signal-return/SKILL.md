---
name: aggregated-change-signal-return
description: "Collapse multiple change sources into one caller-facing boolean so headless bootstraps know whether a downstream refresh is necessary."
metadata:
  author: ychampion
---

# SKILL: Aggregated Change Signal Return
**Domain:** extensions-mcp  
**Trigger:** Apply when a headless setup flow can change state through several mechanisms but callers only need one final answer about whether they must refresh downstream registries.
**Source Pattern:** Distilled from reviewed extension lifecycle and source-reconciliation patterns.

## Core Method
Aggregate every state-changing branch inside the headless install flow into one caller-facing signal. Seed registration, marketplace reconciliation, and delisting can each materially change the runtime even if the others do nothing, so the function should accumulate them into a single boolean that tells the caller whether a follow-up refresh is required. This keeps the internal branching detailed while exposing a minimal external contract.

## Key Rules
- Initialize the change signal from the earliest state-changing step instead of only from the main reconcile path.
- Fold every later state mutation into the same signal, even if it comes from cleanup or enforcement rather than install.
- Keep the caller contract narrow: one signal that means "refresh downstream state now," not a grab bag of internal counters.
- Update the signal only on genuine state changes so callers do not refresh on no-op runs.

## Example Application
If a headless extension bootstrap registers seeds, installs missing registries, and removes delisted plugins, return one `extensionsChanged` boolean that becomes true if any of those paths modified the effective plugin set. The caller can then refresh command discovery once, regardless of which branch caused the change.

## Anti-Patterns (What NOT to do)
- Do not expose only install counts when cleanup or seed registration can also require a downstream refresh.
- Do not make callers reconstruct change state from several independent metrics when the callee already knows the full picture.
