---
name: ui-reel
description: Use when recording a real web app, site, desktop-plugin or Electron UI for a demo reel, launch film, walkthrough or showcase video and cutting it into a cinematic edit - smooth 60 fps footage of the real product, a virtual camera that pushes and pans, a crisp redrawn cursor, captions, a match cut from a still or generated clip into the live UI, phone-size shots, an end card. Also use when screen recordings stutter, drop frames, look soft, miss animations, or a demo needs to look like a trailer instead of a screen capture.
---

# ui-reel

Record the real product in a headless browser so every frame of its motion is captured, then edit it in Remotion
with a virtual camera. The footage is the proof; the camera, cursor, captions and cuts make it a film.

```
assets/rig/        launch.sh  take.mjs  takes.example.mjs  frames2cfr.py  storyboard.py  cdp.mjs
../../templates/reel/   a Remotion project: Reel.tsx, tl.json, takes.ts
../../examples/demo/    a demo product, its takes, timeline and score, and the film they make
```

## Record

```bash
CHROME=/path/to/chrome-for-testing bash assets/rig/launch.sh &     # once; CDP on :9447
node assets/rig/cdp.mjs open "http://127.0.0.1:3000/" > out/target.txt
node assets/rig/take.mjs hero --dry          # rehearse: runs the take, records nothing
node assets/rig/take.mjs hero                # record (reads ./takes.mjs, or TAKES=path)
VIEW=phone node assets/rig/take.mjs menu     # a 390 x 844 touch viewport
python assets/rig/storyboard.py out/rec/hero # contact sheet with marks: check before encoding
python assets/rig/frames2cfr.py out/rec/hero public/scenes/hero.mp4
```

A take is `{ setup(a), run(a) }` in `takes.mjs`: `setup` loads and arranges the page and is not recorded; `run` is
what a person would do. The api: `sleep`, `mark(label)`, `eval(js)`, `rect(selector, textRegex)`,
`move(to, ms, ease)`, `trace(fn, ms)`, `click()`, `type(text, msPerChar)`, `press(key)`, `wheel(total, ms)`,
`setMouse(p)`, `shot(file)`, `W`, `H`. Presses and keystrokes are logged in `take.json`, so `score/assets/cues.py`
puts a click or key sound on every one.

Why the footage is smooth:

- **Slow motion while recording.** Before any page loads, `take.mjs` installs a shim that slows `performance.now`,
  `Date.now`, `requestAnimationFrame`, `setTimeout`, `setInterval` and Web Animations by `SLOW` (default 4), and
  the driver moves 4x slower too. Screencast timestamps are divided back, so a capture that delivers 15 to 75
  frames a second becomes 60 to 300 of film time. `rAF` callbacks get the slowed clock itself, because headless
  `rAF` timestamps can lag `performance.now()` by seconds and break any animation that mixes them.
- **Device scale 2.** A 1280 x 720 page records at 2560 x 1440, so the camera can push to 2x and stay sharp.
- **Constant 60 fps.** `frames2cfr.py` turns the capture into a clip where frame i is what the page showed at i/60 s.
- **The cursor is redrawn.** Headless shows no cursor. `take.json` holds the pointer path and presses; the film
  draws a crisp arrow and a press ring from it, in sync.

## Demo data, never anyone's real account

Serve the product against a throwaway profile the film seeds itself: a dev server with a curated state, or a seed
script that runs the product's own backend over invented data. Mount the real front-end unchanged. For a plugin of
a host app, mount it in a harness page with the host's real CSS tokens and a stand-in SDK.

## Cut (`templates/reel`)

Copy the template, `npm install`, list your takes in `src/takes.ts`, write `src/tl.json`, then
`npm run still` for a frame and `npm run render`.

- **Everything in `tl.json`, in seconds**: `intro` (below), `opening` (generated stills or clips before the product, each pushing in
  about `ox, oy`), shots (`take`, `from`, `to`, `t0` = where in the take to start, `speed`, `cam` keys, `phone`),
  captions, end card (`mark`, `wordmark` or `name`, `install`, `fact`), `bars`, `audio`, `look`, `sfx` (story
  sounds for `cues.py`) and `heroes` (below).
- **Camera keys** `{T, s, fx, fy, sx, sy}`: zoom `s`, the footage point `(fx, fy)` (2560 x 1440 pixels) placed at
  screen `(sx, sy)`. Eased in and out, zoom in log space so a push reads as one move. One job per shot: push to what
  changes, hold, land. No drift.
- **Speed** per shot tightens slow UI without re-recording; `t0` skips the dead start of a take.
- **Cuts** hide inside a short blur and a bloom of the film's glow colour.
- **Cut into the action, never toward it.** A cut's whoosh and bloom promise something: the first frame after it is
  already framed on what the shot is about (its first camera key), and the shot starts (`t0`) just before that thing
  moves. Never cut wide and then pan or push to the subject, and never cut while the thing it leads to has not started
  yet: hold the outgoing shot instead. `npm run check` runs `check-tl.mjs`, which fails a shot whose first camera move
  after the cut travels more than 300 px or 1.6x over more than 0.6 s.
- **Heroes land on the music; the rest breathe.** `heroes` lists the 3 to 5 moments that carry the film (the match
  cut, the payoff, the end card, one product moment that changes everything), in seconds. Those land exactly on a beat
  and get the biggest sounds. Every other cut is free: on a beat or clearly off one, never a near miss. Locking every
  cut to the grid makes a film tick like a metronome and leaves nothing special. Without the key, the match cut, the
  `moment` and the end card are the heroes. `song_fit.py` (in `score`) says which heroes to move.
- **Captions**: 2 to 6 plain words, one per shot, voices rotating (rise, track, wipe), over a low scrim. A caption
  takes about 0.3 s to land, then needs 0.8 s held, or 0.18 s a word if that is longer; `npm run check` fails one
  that leaves too soon. Hold it longer or cut words.
- **The match cut** from a cold open: the first camera key frames the hero object exactly where the last generated
  frame leaves it. Measure both in pixels, set the key, bloom over the cut, carry the letterbox `bars` and open them. Or give
  the last still `dissolve` (seconds): no bloom, the still fades out over the product's own entrance.
- **A title intro, no pictures** (`intro`, what the demo opens on): dots stream in and land as the wordmark's letters
  (sampled from `image`, placed in `box`), the real wordmark resolves over them at `lock`, a line of light along the
  wordmark's own slash (`line`, frame pixels) cuts it in two at `cut`, then the dots swirl toward `into` (the product's
  first shape: centre and radius in frame pixels) and fade over the first shot for `handoff` seconds while the
  product's own entrance takes over. `over` and `under` are one short line each above and below the word.
- **End card**: the mark, the name, the install line or URL, one true fact, creeping in about its centre while the
  music rings out. The mark lands on the hit a little past its size and settles: the film's one overshoot. Every
  other move eases in and out plainly, so this one reads as a landing, not a bounce.

## Check

- A storyboard of every take before encoding (`storyboard.py`). It caught the `rAF` clock bug: a progress ring
  counting to negative percentages.
- `npm run check` (types, cuts that travel, captions too short to read, heroes), a still at each caption, then a
  contact sheet of the render at the caption times.
- Measure the sound (`score`), and watch the 720p preview once end to end.

## Pitfalls

- Pop-ups or toasts left from earlier state: wait them out in `setup`.
- A take that navigates during `run` stays slow (the shim re-arms on every new document).
- A stale frame before the viewport override: `frames2cfr.py` keeps the majority frame size.
- A take ends early on a still page: the screencast only sends frames on change; the film holds the last frame.
- After a re-record, update `frames` for that shot in `tl.json` (the encoder prints it).
- A heavy page (a canvas globe, big blurs) captures under 60 fps: `take.mjs` prints the rate; re-record with
  `SLOW=8` until it reads above 60.
