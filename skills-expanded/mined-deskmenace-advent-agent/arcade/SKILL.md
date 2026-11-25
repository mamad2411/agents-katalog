---
name: arcade
description: Small games, puzzles, quizzes, crosswords, escape rooms and tactile toys (snow globe, jelly, bubble wrap, magic 8-ball) as one offline HTML page. Emotion and interaction first, a share frame (high-score card or the toy mid-shake) with a capture hook, the Arcade kit (loop, input, collision, physics, particles, score, UI, wordgrid, quiz, locks), vendored matter.js and three.js, keyboard plus touch, reduced motion, mute, restart, testing.
license: MIT
---

# Arcade

A gift game is a toy, not a product. Aim for 2–5 minutes of fun that works the first time, on a phone and on a laptop, with no instructions longer than one sentence. Read `gift-director` first: the game has one clear `emotion` (usually `funny`, `ridiculous` or `absurd`), a first `interaction` they find in under 3 seconds, one surprise they didn't expect, and a share frame.

The best gift games star *them*: their dog as the hero, their commute as the level, their running joke as the boss. A generic game with their name on the title screen is the lazy version.

## Pick a shape

| Shape | Good scope | Kit |
|---|---|---|
| Action toy (catch, dodge, bounce, stack) | One mechanic, one screen, score, restart | `loop.js`, `input.js`, `collision.js`, `physics.js`, `particles.js`, `score.js`, `ui.js` |
| Puzzle (sliding, matching, logic grid) | 1–3 hand-made levels you have solved yourself | `input.js`, `ui.js`, `locks.js` |
| Quiz | 8–12 questions with a point of view and a funny results screen | `quiz.js` |
| Crossword / word search | 8–15 words on a theme the recipient shared; clues written by you | `wordgrid.js` |
| Escape room | 3–5 locks in one or two scenes, every clue visible in the page | `locks.js`, `ui.js` |
| Tactile toy (no goal) | Snow globe, jelly fruit, bubble wrap, magic 8-ball, kaleidoscope | `kit/toys/` when present, `loop.js`, `input.js`, `particles.js`, `kit/art/*` |
| Physics toy or game | Stacking, throwing, soft bodies | `physics.js`, or vendored matter.js from `workshop/kit/vendor/` (MIT, credit it) |
| 3D scene | A tiny world to orbit, a glass object | vendored three.js from `workshop/kit/vendor/` (MIT, credit it), tier M and above |

Scope rule: if you cannot describe the whole game in two sentences, cut it.

## Non-negotiables

- **Keyboard and touch.** Arrows/WASD plus Space/Enter for action; on-screen buttons or tap/swipe for the same actions. `input.js` unifies both; still test with the keyboard only and with taps only.
- **Reduced motion.** `loop.js` exposes `reducedMotion()`; when true, cut particles, screen shake and parallax, slow nothing that affects fairness. Never flash more than three times per second.
- **Pause and reset.** Visible pause button and `Escape`; a reset that restores a clean state without reloading. `ui.js` has overlay helpers with real `<button>`s and focus management.
- **Scale.** Fit a 360×640 phone viewport and a 1280×800 laptop. Use CSS `aspect-ratio` and `max-width`, or scale the canvas with `devicePixelRatio`.
- **No autoplay audio.** Sound starts after the first tap or key. Offer a mute toggle.
- **Restart, always.** Every game has a visible restart.
- **Offline.** No CDN, no `fetch`. Physics and 3D libraries come only from `workshop/kit/vendor/`, inlined, and go in `credits`.
- **Deterministic fairness.** Seed randomness with `kit/art/prng.js` when the puzzle must be solvable; verify solvability in code before showing it.
- **Readable.** Text at least 16 px, contrast at least 4.5:1, no colour as the only signal.

## Workflow

1. `advent-agent progress thinking`: choose shape, mechanic, theme, emotion, win and lose conditions, one surprise (a message at 50 points, a hidden door), and the share frame.
2. `advent-agent progress making`: copy only the kit modules you need into one `<script type="module">` (or plain `<script>`; drop `export`). Write the game; keep state in one object; make `reset()` rebuild it.
3. `advent-agent progress testing`: open the file mentally and walk through: load, first input, score, lose, reset, pause, resize, keyboard only, touch only, reduced motion. If you can run code, run the pure logic (grid generation, quiz scoring) in Node.
4. `advent-agent progress wrapping`: `gift@2` manifest with `form: "interactive-html"`, `family` (`games` or `tactile-toys`), `emotion`, `interaction`, `tierUsed`, `share`, `credits`, a `note` that says why you made it (controls go in the page, not the note), `incomplete` for anything cut.

## The share frame

A game's share frame is usually the **result**: a high-score card ("Biscuit the husky: 4,210 sausages, personal best"), the escape room's opened door, the quiz verdict, the toy mid-shake. Expose `window.adventCapture.prepare(kind)` that jumps there without playing: set the state, render one frame, hide the pause and mute buttons. For a loop, run 5–8 seconds of attract-mode play (a scripted demo, not random input). Mark real names with `data-advent-private`. Offer the result card as a PNG in `downloads` too.

## Quizzes

Write questions that could only come from this season: about the recipient's shared interests, about the earlier doors (callbacks), about the world. Each answer set has one correct answer and funny wrong ones. Results screen: at least three tiers, each with its own line. `quiz.js` handles scoring, keyboard (1–4 and arrow keys) and a summary.

## Word grids

`wordgrid.js` places words with crossings and fills the rest; it reports what it could not place so you can choose shorter words. Clues are the gift: write them with wit. Provide "reveal letter" and "check" buttons.

## Escape rooms

`locks.js` normalises answers (case, accents, spaces, punctuation) so "Sankt Gallen" and "sankt-gallen" both open the lock. Every clue must be visible in the page; no external search needed. Offer a hint after 60 seconds, and a "give me the answer" after three wrong tries: a gift never traps.

## Packaging

Single file, inline everything, no CDN, under 5 MB. `form: "interactive-html"`. In a folder gift, `entry` points to the file. Test that `prepare("still")` gives the frame you pictured.
