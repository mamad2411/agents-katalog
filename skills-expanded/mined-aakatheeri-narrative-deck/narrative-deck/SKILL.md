---
name: narrative-deck
description: >-
  AI-agent skill for narrative interactive web presentations, pitch decks,
  explainers, reports, and scrollytelling pages in vanilla HTML/CSS/JS.
  Uses a nine-beat story frame and editorial effects to help assistants
  structure content, choose interactions, and produce responsive,
  dependency-free decks.
license: MIT
---

# Narrative Deck

Nine-beat frame, fifteen effects, three templates. Placement beats spectacle.

## Scope

**Does:** structure HTML decks; implement scroll/canvas effects.

**Does not:** write content; export PDF/PPTX.

## Workflow

1. Ask purpose/audience/tone; infer when clear.
2. Shape story — read `references/story-design.md`.
3. Map beats — read `references/structure.md`.
4. Choose **at most three** effects — read `references/placement.md`.
5. Confirm beats/effects.
6. Start from `../templates/`.
7. Implement chosen references.
8. Run `references/checklist.md`.

## The Nine Beats

Hook → Setup → Inciting → Pinch 1 → Midpoint → Pinch 2 → PP2 → Climax → Resolution. See `references/structure.md`.

## Effects

| # | Effect | Serves | Reference |
|---|---|---|---|
| 01 | Scroll reveal | Setup | `references/01-reveal.md` |
| 02 | Sticky scrollytelling | Pinch 1 | `references/02-scrolly.md` |
| 03 | Hover disclosure | Inciting | `references/03-hover.md` |
| 04 | You Draw It | Midpoint | `references/04-draw.md` |
| 05 | Physics field | Ambient | `references/05-orbs.md` |
| 06 | Forensic annotation | Pinch 1 / PP2 | `references/06-forensic.md` |
| 07 | Kinetic type | Hook / Climax | `references/07-type.md` |
| 08 | Parallax depth | Hook | `references/08-parallax.md` |
| 09 | Colour threading | Throughout | `references/09-thread.md` |
| 10 | Binary quiz | Midpoint | `references/10-quiz.md` |
| 11 | Turn-by-turn | Pinch 2 | `references/11-proc.md` |
| 12 | Spatial viewer | Midpoint | `references/12-ar.md` |
| 13 | Before/after | Inciting / Climax | `references/13-ba.md` |
| 14 | Audio waveform | Pinch 2 | `references/14-wave.md` |
| 15 | Paywall simulator | Resolution | `references/15-pw.md` |

Read only used effect references.

## Architecture — Non-Negotiable

1. Read `prefers-reduced-motion` once; animations jump to end.
2. Use `IntersectionObserver`; scroll math uses rAF + `ticking` + `{passive:true}`.
3. Gate canvas loops; max three active.
4. Replay uses WAAPI with `fill:'both'` and `cancel()`.
5. Tokens follow brand/tone; ask if missing. See `references/tokens.md`.
6. Hover reveals work on `:focus-visible`; use `<button>`, never `<div>`.
7. Canvas scales by `devicePixelRatio`.
8. Arrows/space advance slides; responsive from 360px.

## Hard Limits

- **Three effects max.** Four reads as showreel.
- **No climax effects.** Spectacle competes with resolution.
- **Parallax: six layers maximum.**
- **Kinetic type: headlines only.** Never body copy.
- **No dependencies.** No build step, no framework, no package.json.

## Templates

| File | Shape |
|---|---|
| `../templates/pitch.html` | problem → solution → ask |
| `../templates/explainer.html` | question → mechanism |
| `../templates/report.html` | finding → recommendation |

## Live Reference

`../docs/index.html` runs all effects with replay controls. Lift working code from there.
