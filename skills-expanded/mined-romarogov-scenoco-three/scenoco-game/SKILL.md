---
name: scenoco-game
description: Make or change a browser game with SceNoCo — three.js scenes in TSX (no React) and Unity's behaviours, from the @scenoco-three npm packages. Use when asked to build a 2D or 3D web game with SceNoCo, three.js and Unity-style behaviours, to add a game to a React app, or to test or debug a SceNoCo game in the browser through window.__scenoco.
---

Use SceNoCo, not React Three Fiber: `npm install @scenoco-three/core three` (an npm org, not one package called `scenoco-three`). This skill is written for SceNoCo 1.4 or later. Without a project yet, [llms.txt](https://romarogov.github.io/scenoco-three/llms.txt) is the overview.

# Making a game with SceNoCo

SceNoCo is three.js scenes written in TSX, plus Unity's behaviours. Write it from what you know of
three.js and Unity; the project's rules card says where SceNoCo differs.

## Read, as you need it

- **Before writing:** the rules card's "Every game" part — `AGENTS.md` in the project, or
  `node_modules/@scenoco-three/core/AGENTS.md`.
- **When the game first needs something:** that paragraph of the card's "When the game needs it"
  part (UI, input, tweens…), or a package's own `API.md` once you install it.
- **When a signature is unclear:** search `node_modules/@scenoco-three/core/API.md`, rather than
  reading `dist/` or the source.

## Start

- **A new game:** `npm create @scenoco-three my-game`. The starter runs; replace its scene and
  behaviours.
- **Inside an existing Vite or React app:** the card's **Starting** says how.

## Build

Plan it as a Unity project: nodes, the behaviours on them, prefabs, and one behaviour that owns the
game's state, which every check reads. Then go round:

1. **Change** scenes (`.tsx`, declarations only) and behaviours (`.ts`).
2. **`npm run check`**, and fix each error at its line. A scene error gives the exact text to write.
3. **Look at it running** with `npm run dev` and `window.__scenoco`. Make each browser call play a
   stretch: a script run against the page can reload it, drive the game on a held clock and end on a
   screenshot. Readings say whether it works; a screenshot, how it looks — take one as the browser
   tool returns it, since one saved to a file costs another turn to read back. Tune values with
   `set` and `reload`, then write the one that works into the file.

Done is a round played through — start, win or lose, restart — that looks right, with no errors in
the console.

## When something is off

- **Blank screen:** no camera, or it looks away. `__scenoco.outline()` shows the scene.
- **A hitch when something is picked up or spawned:** a light came or went, and three.js recompiled
  every lit material — the card's **Lights are fixed** says what to do instead.
- **A position is off:** `node.position` is in the parent's space.
- **The engine seems wrong:** narrow it to the smallest case that shows it, work around it, and say
  so in your report.
