---
name: frogoe-core
description: >
  The frogoe technical contract — how one game is built. Use for the folder form
  (index.html / game.js / BRIEF.md / frogoe.json / .frogoe/), the defineGame closure
  and its four nouns (stage, input, loop, finish), pointer dx semantics, the
  window.__frogoe host handle, HUD block bindings, external libraries (three.js,
  gsap, fonts) and the bundler that dissolves them, plus check rules and teaching
  errors. Read before writing or editing any game code.
---

# frogoe core

A game is **one closure**. The platform hands it four nouns; everything visible is the
game's own (DOM+CSS for HUD, canvas for the world). The contract ships zero taste —
if it ever draws something, that is a defect.

```js
// game.js — the whole game
import { defineGame } from "frogoe";

defineGame(({ stage, input, loop, finish }) => {
  let y = stage.height / 2;
  let vy = 0;

  input.on("down", () => {
    vy = -300;
  });

  loop.update = (dt) => {
    vy += 900 * dt;
    y += vy * dt;
  };

  loop.render = (ctx) => {
    ctx.fillStyle = "#8fe9ff";
    ctx.fillRect(stage.play.center - 12, y, 24, 24);
  };
});
```

## References

| File                         | Read it to…                                                        |
| ---------------------------- | ------------------------------------------------------------------ |
| `references/folder-form.md`  | lay out or extend a game folder (index.html, .frogoe/, assets/)    |
| `references/brief-format.md` | author BRIEF.md (frontmatter schema: verb, mood, palette)          |
| `references/contract.md`     | every platform guarantee and teaching error in one table           |
| `references/hud-bindings.md` | place, theme, and bind registry HUD blocks to game state           |
| `references/externals.md`    | use three.js / gsap / web fonts and how the bundler dissolves them |
| `references/audio.md`        | make sound that survives phones (gesture unlock, interrupted state, no selection UI — iOS + Android) |

## Non-negotiable rules (silent bugs the eye misses)

- **Pointer dx/dy are anchor-relative** — measured since touch-down, not per event.
  Steer with `x = grabX + p.dx` or track your own `lastX`. Never `x += p.dx` inside a
  drag handler: every pointermove re-applies the cumulative offset and the actor
  rockets into a wall. This bug shipped once; `check` rejects it on sight.
- **All HUD text lives in the DOM layer**, not canvas: crisp on every DPR, themeable,
  accessible. Canvas `fillText` HUD is allowed only inside the play field (combo
  popups at world positions).
- **Gameplay coordinates use `stage.play`** (capped centered column), never raw
  `window.innerWidth` — parity between phone and desktop.
- **Fixed furniture respects `stage.safe`** — notches cover fixed y=34 text.
- **One page, zero runtime requests** after bundling: everything the game needs is
  inline. Author-time externals are fine; the bundler dissolves them.
- **`finish(score)` ends the run** — report once; the game-over CARD is a registry
  block you show yourself, never something the platform draws.
- **WebAudio unlocks only inside a user gesture** — `input.on("down"/"up")`
  both qualify (the contract fires them inside the native pointer events).
  Resume when `state !== "running"` (iOS has an extra `"interrupted"` state),
  play a 1-sample silent buffer to hard-unlock, and never check only
  `"suspended"` — that ships the "sound randomly goes quiet" bug. Full
  recipe: `references/audio.md`.

## Editing existing games

Read `BRIEF.md` first; its palette and verb are the game's identity. Keep block
`--block-*` theming on a single parent element. Never edit `.frogoe/` — it is
regenerated from `frogoe.json`.
