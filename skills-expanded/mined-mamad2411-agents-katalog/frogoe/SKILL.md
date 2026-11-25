---
name: frogoe
description: >
  Mandatory entry point: read this first for any request to make, create, edit, or ship a
  game — arcade, puzzle, runner, hyper-casual, single-file or folder — or to check, run,
  bundle, or diagnose an existing frogoe game. Also use it to pick HUD recipe blocks from
  the registry, wire them to game state, or place a game in a feed/shell. Inputs may be a
  genre idea, a reference game, a brief, or an existing project folder. It confirms the
  BRIEF up front, then routes to the owning skill.
---

# frogoe entry point

frogoe games are **one folder, one closure**. The DOM+CSS layer is where beauty lives
(HUD blocks from the registry); the canvas layer is where the simulation lives (60 Hz
update loop). The platform contract is four nouns — `stage`, `input`, `loop`, `finish` —
and nothing visual. Read `/frogoe-core` before writing any game code.

## 1. Start from project state

| State                                                 | Action                                                    |
| ----------------------------------------------------- | --------------------------------------------------------- |
| Existing frogoe folder (`frogoe.json` present)        | Resume: read `BRIEF.md`, then `game.js`; make the change. |
| Explicit request to only restyle/HUD an existing game | Load `/frogoe-creative`, skip the interview.              |
| Fresh creation                                        | Run the intent pass below, then route.                    |

## 2. Fresh creation — confirm the BRIEF first

Before any code, `BRIEF.md` must exist and be honest (see `/frogoe-core` →
`references/brief-format.md` for the schema). If the user gave a genre or reference game,
derive the brief and confirm it in one message: title, **one verb** (`tap`/`hold`/
`steer`/`aim`), mood, and a **declared palette** (bg / fg / accent hex). A game whose
core action cannot be named in one word is input soup — push back once, then proceed
with the closest single verb.

## 3. Route

| Priority | Request shape                                                                                                      | Skill                                                        |
| -------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| 1        | Technical contract, folder form, `defineGame`, input semantics, `finish`, `window.__frogoe`, lint/bundler behavior | `/frogoe-core`                                               |
| 2        | Visual direction, palettes, typography, lazy defaults, HUD styling, juice polish                                   | `/frogoe-creative`                                           |
| 3        | Choosing / theming / binding HUD blocks (score, hearts, fuel, game-over)                                           | `/frogoe-core` → `references/hud-bindings.md` + the registry |
| 4        | Anything 3D or with external libs (three.js, gsap, fonts)                                                          | `/frogoe-core` → `references/externals.md`                   |

Always load `/frogoe-core` once for any code-touching task; add `/frogoe-creative`
whenever pixels change.

## 4. The loop (build → check → eyeball)

1. Author the folder (`index.html`, `game.js`, `BRIEF.md`, blocks from the registry).
2. Run the game (`frogoe run` or any static server) and **look at it** — a screenshot is
   the only quality gate that matters.
3. `frogoe check` (lint contract + output measures) until clean.
4. `frogoe bundle` before shipping: externals dissolve, one self-contained HTML.

## Boundaries

- Do not add engine opinions: the contract draws nothing. Anything visible comes from
  game code or registry blocks.
- Do not bypass `BRIEF.md` for feed games — the brief is what the gate measures against.
- Do not read every reference for a one-line edit; the tables above route narrowly.
