# AGENTS.md

Instructions for AI agents working in this repo. (Work in progress; more to come.)

## What this repo is
A workspace for creating content **agentically**: infographics, short videos, Instagram Reels, social posts, posters, and more. Agents do the design and production. Humans give direction and taste.

## House rules (non-negotiable, apply to every graphic and every video)
**Less is more.** The piece is the content, nothing else. These rules override any design language, reference site, or example in this repo.

1. **No metadata on the graphic.** No series name ("Jev for beginners"), no topic or category tags, no source or credit footers, no dates, no header or footer bars.
2. **No numbering.** Every piece stands alone. It is not a carousel or a chapter: no "06 / 15", "Part 1 of 5", "Video 2", scene counters, or numbered section labels ("01 —").
3. **No slashes or dividers.** No hairline rules, separator lines, progress lines, "/" or "·" used as separators, "—" used as decoration, or "↳" arrows.
4. **No random decorative elements.** No corner ticks, crosshair marks, stray dots, or construction marks that do not explain anything. If an element does not carry meaning, delete it.
5. **No kicker or subtitle above the headline.** Don't stack a subheader, headline, subtext, big text, and small text. Keep the type **simple, clear, and clean**: one headline, then the main content, plus at most one short supporting sentence if it is truly needed. Use about two text sizes per piece. (Labels inside a diagram are fine when they name things.)
6. **The main content is what matters:** a beautiful Fictive Kin-style illustration and nicely designed diagrams or flowcharts. Use the space for the illustration and for air.
7. Separate sections with **space or a surface colour** (a card or panel), never with a line.
8. **Monochrome, on white.** Use a white background and greyscale only, with no accent colour. Show emphasis through ink vs. light grey and filled vs. outlined. A **dark-mode variant** is made on request by generating it, not redesigning it: `skills/lib/make-dark.mjs` (see `house-style.md` §2b).
9. **No italic or coloured emphasis** in headlines (e.g. a green italic phrase, or a greyed-out line). A headline is one colour and one weight.
10. **Icons come from Lucide** (`node_modules/lucide`), at stroke 1.5.
11. **Generous negative space.** When in doubt, remove something.
12. **Formats:** author every design as **HTML** (the editable source). Export stills to **PNG** and animations to **MP4**; those are the files that get posted.

## Where things go
| Path | What | In git? |
|---|---|---|
| `output/` | **All generated content.** One folder per project, e.g. `output/jev-explainers/`. | **No** (gitignored) |
| `output/<project>/brief.md` | The project's brief: audience, verified facts, deliverables. Read it first. | No |
| `design-languages/` | Written style guides studied from reference sites, plus CSS kits that implement them | Yes |
| `skills/` | Reusable how-tos and tools for each content type | Yes |

**Always write generated files (HTML sources, PNGs, MP4s, stills, scratch) inside `output/<project>/`.** Never put generated content anywhere else in the repo.

Suggested project layout:
```
output/<project>/
  brief.md
  infographics/src/NN-slug.html   → infographics/NN-slug.png
  videos/src/slug.html            → videos/slug.mp4
  videos/stills/                  (frame checks)
```

## How to make things
1. Read `output/<project>/brief.md`. If it does not exist, write one with the human first.
2. Follow **`design-languages/house-style.md`** (Monochrome Editorial, distilled from Palantir, Oregon Symphony, and Modal) for everything. For video, add **`design-languages/animations/ordinary-folk.md`** for motion. The individual reference guides explain where each rule comes from.
3. Follow the matching skill:
   - Static graphics (infographics, posts, posters) → [`skills/infographic/SKILL.md`](skills/infographic/SKILL.md)
   - Animated video (reels, LinkedIn video) → [`skills/animated-video/SKILL.md`](skills/animated-video/SKILL.md)
4. **Look at your output** (open the PNG or still frames) and iterate. Never ship a render you have not looked at.

## Quality gate: content must fit the format (always)
Before calling anything done, **check that all content sits inside the borders of the format** (1080×1350, 2160×2700, 1080×1440…). Nothing may be cut off at the bottom or sides, crammed against an edge, or hidden inside a clipped box. This is the most common failure: a dense cheat sheet quietly running off the bottom.
- Both renderers run an automatic fit check (`skills/lib/fit-check.mjs`) and print `⚠ OVERFLOW`, `⚠ CLIPPED` (content hidden inside a box), or `⚠ MARGIN` (content in the outer half of the margin). They exit with an error when anything fails. The video renderer checks the whole timeline before it encodes.
- **A piece is not done until the renderer prints `✓`** *and* you have looked at the image yourself, especially the bottom edge and the last line of every card.
- If it doesn't fit, cut content or simplify. Don't shrink type below the minimums or squeeze the margins.
- Only an element deliberately designed to bleed off the edge may opt out, with `data-bleed="true"`.

## Content rules
- Use only facts you have verified; put them in the brief with their sources. Do not invent numbers.
- Default audience is beginners: grade-5 vocabulary, short sentences, concrete examples over theory.
- Social formats: LinkedIn/IG portrait still = **1080×1350** (4:5); portrait video = **1080×1440** (3:4), or 1080×1920 (9:16) for Reels/Shorts.

## Setup
```bash
npm install          # playwright; uses your local Google Chrome
brew install ffmpeg  # for video
```
