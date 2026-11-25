---
name: card-catalog-explainer
description: >-
  Renders a ~56 s 16:9 explainer that opens on a wall of real code-made videos, then walks one request through a library card catalog: an agent gets a
  request in a terminal, searches a catalog drawer, pulls an index card, follows its call number to the
  source shelf, installs from there and renders the result. Every string lives in config.json, so it explains
  any registry, marketplace or catalog (agent skills, templates, packages, MCP servers). HyperFrames, local
  render, no credits. Use when asked for a "how our catalog / registry / marketplace works" video, an animated
  explainer of "listed here, lives there", or this varg skills catalog video. NOT for slide decks, data charts
  or talking-head explainers.
compatibility: bun, ffmpeg, Node with npx (HyperFrames 0.8.186 renders locally). No credits.
metadata:
  author: vargHQ
  version: "1.0.0"
  varg.engine: "hyperframes"
  varg.category: "explainers"
  varg.outputs: "mp4 1920x1080 30 fps, ~56 s, silent unless music.* is added"
  varg.cost.typical: "0 credits (local render)"
  varg.runtime.typical: "build 1 s, check 1 min, render 2-4 min"
---

# Card catalog explainer

Code: this folder. `config.json` is the whole video: copy, colours, catalog contents and scene lengths.
`engine/build.ts` turns it into a HyperFrames project in `out/hf/`, and `make.command` checks and renders it.

## The film, scene by scene

| scene | what happens | config |
|---|---|---|
| showcase | a wall of real renders from other templates plays side by side under two lines ("every frame here is code") | `showcase` |
| ask | a terminal types the user's request; a line asks where the agent finds a template | `request` |
| drawer | a card-catalog drawer slides in; category tabs pop up one by one | `catalog` |
| search | a search command types; three index cards rise out of the drawer; one is picked and grows to full size | `search` |
| card | the index card fills in: call number (repo, path, sha), fields, install command; then moves left | `card` |
| shelf | shelves of source repos build; a dashed line runs from the call number to the shelf and the skill comes off it; then the source changes and a sync line rewrites the card's sha | `shelves`, `install`, `sync` |
| result | the terminal installs and renders; a phone shows the result | `result` |
| end | the one-line conclusion | `end` |

## Steps

1. **Collect the content.** What is listed (the catalog: name, count, categories), where it really lives
   (the shelves: repos and item names), one concrete request and the item that answers it (its card fields,
   install command, sha), and the result to show. Ask the user for anything you would otherwise invent;
   numbers and shas must be real or labelled as an example.
2. **Write `config.json`.** Keep the keys; change values. `*stars*` in any `line` mark the accent words.
   Respect the lengths in "Limits" below or text collides.
3. **Build and check:** `bun engine/build.ts && npx --yes hyperframes@0.8.186 check out/hf --json`.
   It must report `"ok": true`. Expected warnings, fine to keep: `line_unread` on typed text (each typed
   letter is its own span, so the check counts letters as words), `text_below_floor` on the scaled card,
   the mini cards and the book spines (texture, not reading), `film_silent` when there is no music.
4. **Look at frames** before rendering: `npx --yes hyperframes@0.8.186 snapshot out/hf --at 2.5,8,14.5,22.5,32.3,35.6,41.6,47.5`
   and open the contact sheet. Check every line is inside the frame and nothing overlaps the bookcase.
5. **Render:** `bash make.command [config]` (or the render line from it) → `out/<output.name>.mp4`.
   Run it in the background; it takes a few minutes.

If `npx` is a broken nvm shell function, call it by path: `NPX=$HOME/.nvm/versions/node/<v>/bin/npx bash make.command`
with that `bin` on `PATH`.

## What to change for a request

| request | where |
|---|---|
| another catalog or product | `catalog.label`, `catalog.count`, `catalog.tabs`, `shelves[]` |
| another example request | `request.text`, `search.command`, `search.results`, `card.*`, `result.lines` |
| another language | every `line`, `card.fields` labels, `card.installLabel`, `output.lang`; fonts are Montserrat + IBM Plex Mono (Latin + Cyrillic). English is `config.json`, Russian is `examples/varg-catalog.ru.json` |
| brand colours | `colors.accent` (rules, lines), `colors.accentInk` (accent text on paper, keep it dark enough for 4.5:1), `colors.ground` |
| slower / faster | `timing.<scene>` in seconds; every scene's beats are placed from its own length |
| music | put `music.mp3` / `.m4a` / `.wav` next to `make.command`; it plays at 0.55 with a 1.5 s fade-out |
| result picture | `result.covers` (pairs of colours for the stamps on the phone) |
| opening examples | `showcase.clips[]`: `src` (path relative to the config, or an https URL), `label`, `start` (seconds into the source). Clips are cropped to 9:16 and looped to the scene length; a missing file is skipped, no clips skips the scene |

## Limits (1920×1080)

- `showcase.clips` 3–5 (five fill the width), labels ≤ 18 characters; `showcase.line1` / `line2` one row ≤ 40 each.
- `request.text` ≤ 90 characters (two terminal lines). `search.command` ≤ 50.
- `request.line`, `search.line` one row each, ≤ 34 characters. `catalog.line` two rows ≤ 30 each.
- `card.line` two rows ≤ 20 each (it sits right of the shrunken card). `install.line`, `sync.line` two rows ≤ 30 each
  (they must stay left of the bookcase at x = 960).
- `result.line` two rows ≤ 32. `end.line` two rows ≤ 26.
- `card.title` ≤ 28. Call-number parts (`repo` owner, repo name, `path`, `sha`) ≤ 15 each. `card.fields` values ≤ 50.
  `card.install` ≤ 54. Three fields plus the install row fit; a fourth runs into the punch hole.
- `shelves`: exactly three rows. Row 1 ≤ 11 spines, rows 2–3 ≤ 8; spine names ≤ 20 characters.
  The item named `card.path` on an `own` shelf is the one that gets pulled out.
- `result.lines` ≤ 6 rows, each ≤ 56 characters; kinds `cmd` (typed), `ok` (green tick), `progress` (bar).

## Rules

- Everything is on the GSAP timeline; no CSS animations, timers or random numbers. Positions are set through GSAP,
  never with CSS `transform`, or HyperFrames lint fails.
- Don't hard-code new numbers in the scene CSS without checking the snapshot: the install and sync paths are
  computed from the card's scaled position (`sceneShelf`, `call`), so moving the card means moving them too.
- Never commit `out/`, `showcase/` or music files; the repo blocks media. Host previews and showcase clips on s3.varg.ai and put their URLs in `showcase.clips[].src`.
- Real values only: the counts, repos and shas on screen should come from the user's catalog. The bundled
  config uses real numbers from vargHQ/skills-marketplace (294 entries) and real templates commits.
