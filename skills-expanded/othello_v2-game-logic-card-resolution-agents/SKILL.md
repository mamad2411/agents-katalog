# game/logic/card-resolution/ AGENTS.md

Canonical headless card-resolution modules extracted from compatibility layers. Read `../AGENTS.md` and `../../AGENTS.md` first.

## Where to look

| Task | Start here | Notes |
| --- | --- | --- |
| Pending-selection resolution side effects | `trap.ts`, `ownership.ts`, `protect.ts`, `position-swap.ts`, `status-cells.ts`, `board-expansion-apply.ts` | These modules mutate canonical game/card state only through injected deps. |
| Hand-overlay resolution | `hand-effects.ts` | Hand reveal / condemn / execution / selection resolution logic. |

## Conventions

- Keep this layer headless and deterministic.
- Consume dependencies via injected `deps` parameters; do not import UI/runtime globals.
- Treat `game/cards/effects/*` as compatibility facades that delegate here.

## Anti-patterns

- Adding DOM / `window` / network publish logic in this layer.
- Reintroducing card rule math into `game/cards/effects/*` wrappers.
- Diverging behavior between this layer and `game/logic/cards.ts` orchestration paths.
