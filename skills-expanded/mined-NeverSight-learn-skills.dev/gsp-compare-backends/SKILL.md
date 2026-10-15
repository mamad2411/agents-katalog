---
name: gsp-compare-backends
description: "Use when backend uncertainty remains and only a narrow two- or three-option compare is needed."
---

# Game Compare Backends

## Goal
Help choose between backend profiles when the choice is genuinely uncertain.

## Important warning
Compare mode usually costs more tokens and time than a single recommended route.
Say this explicitly before or while using it.

## Good use cases
- greenfield work where two routes appear plausibly viable
- UI-first vs world-first uncertainty
- 2D vs lightweight 3D preview uncertainty

## Bad use cases
- obvious stack choice
- live-product iteration
- post-architecture situations where the real blocker is not the backend

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present comparison results in conversation (compared options, criteria, result, why the winner won, token / cost note).
- **minimal** or **full**: update `docs/game-studio/backend-decision.md`.
