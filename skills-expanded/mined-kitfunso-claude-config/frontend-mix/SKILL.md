---
name: frontend-mix
description: "Five wildly different frontend variants (page, hero, app UI, mockup) or one launch-video preview, taste locked from DESIGN.md, ending at a human pick. Use for 'make it look amazing / viral / wow / surprise me'."
---

# frontend-mix

Design engineer with a dice cup. Make five things the user has not seen, show them side by side, let a human choose. The roller keeps the chaos honest: seeded, logged, never a known clash, never a performance pile-up.

**Dice choose technology, never taste.** Taste is `DESIGN.md`; the dice get hero, material, motion and layout. Precedence for every visual choice: the user's words, then `DESIGN.md`, then the rolled recipe. Free and open-source tech only; the catalog is already filtered, and a gated package means the catalog is wrong.

| Mode | Trigger | Output | Human gate |
|---|---|---|---|
| `web` | page, app, hero, dashboard, mockup | 5 single-file HTML variants + contact sheet + board | user picks or remixes |
| `video` | launch video, demo, promo, teaser, reveal | one HyperFrames composition, previewed, unrendered | user approves the render |

Read `references/design-standards.md` once per session: it folds `/design-consultation`, `/frontend-design`, `/design-review` and `/frontend-build` into the four stages below.

## Step 0: read the brief

Pin the subject (one product, one audience), the page's single job (convert, explain, impress, operate) and the mode. Pull real content from the repo, README or the user's words; real content is what lets a reviewer judge hierarchy. If the subject is unknown, ask one question and stop. Everything else you decide. Note `package.json` and `DESIGN.md` if a project exists.

Done when: subject, job, mode and a content source are each written down in one line.

## Step 1: lock taste

`DESIGN.md` at the project root: read it and go. Missing: run the short-form consultation from `references/design-standards.md` section 1 (context confirmed in one question, the memorable thing, ONE complete proposal with SAFE / RISKS), then STOP for the user's answer. On approval write `DESIGN.md` in the standards shape (the roller parses the bold labels) and add the "Design System" pointer to the project `CLAUDE.md`. Record the direction phrase and the memorable thing; every builder brief carries both.

Exception: the user asks in their own words for exploration before a brand exists ("surprise me, no brand yet"). Then roll without `--design`, treat the round as taste discovery, and run the consultation on the winner.

Done when: `DESIGN.md` exists and was approved, or the user opted into brand-free exploration.

## Step 2: roll

```bash
python ~/.claude/skills/frontend-mix/scripts/roll.py --mode web --n 5 --design DESIGN.md --out <workdir>/mix --brief "<one line>"
```

`--design` locks palette and type from the file; `--seed` reproduces, `--lock hero=splat` pins a slot the user named, `--avoid` excludes. The roller enforces distinctness, clash, perf and novelty rules and prints its warnings; a roll that is wrong for the brief is re-rolled with `--avoid` and a reason, never hand-edited.

Then read `manifest.json`, the rolled entries in `references/catalog.md` (verified CDN imports, snippets, perf caveats), and `references/anti-slop.md` once per session.

## Step 3 (web): brief five builders

For each variant write the four `/frontend-design` answers yourself (purpose, tone in one phrase, constraints, differentiation: the memorable thing restated for this hero) and set the three dials from `references/design-standards.md` section 2. Five variants share one `DESIGN.md` and differ in hero, material, motion, layout and direction phrase; two briefs that read like siblings means the weaker one is rewritten.

Fill `assets/builder-brief.md` per variant: every `{{field}}`, the manifest importmap pasted verbatim, the catalog snippets for that variant, the real content. The brief is the single source of the rules a variant must satisfy; when you fix a variant yourself in Step 4, its rules bind you too.

Dispatch five Sonnet sub-agents in ONE message, one per variant, each writing exactly one file `<out>/variants/v<N>-<hero>.html`. Builders build; you brief and judge.

Done when: five briefs with no `{{` left, five agents dispatched.

## Step 4 (web): gate, look, board

Score every variant against `references/design-standards.md` section 3: classify landing / app / hybrid, the eight hard rejections, the seven litmus questions (six YES), then the checklist with impact ratings. Write verdicts to `<out>/qa/review.md` in the critique format, quick wins first. A hard rejection or litmus fail goes back to its builder with the specific fix, or you fix it, before the board.

```bash
python ~/.claude/skills/frontend-mix/scripts/screenshot.py <out>/variants --sheet <out>/contact-sheet.png
python ~/.claude/skills/frontend-mix/scripts/roll.py --board <out>
```

Read the contact sheet PNG. Blank, console error, or flat fallback where the GPU layer should run: fix or re-dispatch. The board (`<out>/board.html`) is five iframes with recipe chips and a notes box each; open it locally in the browser and hand it over by path, never through the Artifact tool.

Then STOP: one line per variant naming its tech mix in words, the board path, and the question: which wins, or which slots to keep and re-roll. Porting and polish wait for the answer.

Done when: every variant has a review.md verdict with zero open hard rejections, the sheet has been read, and the user has been asked.

## Step 5 (web): after the pick

- Re-roll with kept slots locked: `roll.py --design DESIGN.md --lock hero=...`.
- Record: `roll.py --approve <out> v3` writes the winner to `history.json`; add a Decisions Log line to `DESIGN.md` naming the hero and why.
- Port on request: `/design-html` for a Pretext-native page, `/frontend-build` for React (its Stage 1 is done). `ui_base` decides shadcn on Base UI vs Astryx; ThreeUI and Canvas UI become dependencies here, not before.
- Run the full `/design-review` on the served result and fix what it finds.

## Video mode

Read `references/video.md` first (slot-to-adapter map, determinism under `hf-seek`, scene recipe per hero).

1. Lock taste as in Step 1. Roll `--mode video --n 1 --design DESIGN.md`.
2. Route through `/hyperframes` with `flow: automation`, `storyboard: no`, the recipe passed as constraints.
3. MVP: 2-3 scenes (hook, product moment, close), 8-15 s, one composition. `npx hyperframes preview`, snapshot sheet at scene midpoints, read it: the product name is legible in every scene.
4. STOP with the preview and the recipe in words: render, re-roll a slot, or change the story? Rendering waits for that answer.
