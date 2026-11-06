---
name: web-design-taste-workflow
description: A 3-step workflow for getting Claude Code to produce a web design that doesn't look like generic "AI slop" — build a personal Taste Library of real design references (grouped by family, not project), arm Claude with anti-slop design tools it doesn't ship with, then never one-shot the result (build 5 aesthetic directions side by side, narrow to 1, then iterate visually with a live tweaks bar instead of guessing in the terminal). Includes a reusable 4-part prompt template (Aesthetic + Reference + Intent + Guardrails) for briefing a multi-direction landing page build. Use when a Claude Code build is producing generic-looking frontends (purple gradients, Inter font, rounded-everything, icon-grid feature rows), when starting a new landing page/site build and wanting several real aesthetic options instead of one guess, or when asked to fix "AI slop" in a design.
---

# Web Design Taste Workflow

Source: reviewed from an uploaded infographic — "How to Turn Claude Code
Into a Web Design Genius" (@ai_slacker, "The 3-step workflow that kills
generic AI websites"). Complements this repo's existing `hallmark` skill
(a vendored anti-AI-slop design skill for greenfield builds/audits/
redesigns) rather than duplicating it: `hallmark` is Claude's own internal
design-study process; this skill is the external-tooling + prompting
workflow that feeds it — install the tools below, then either skill can
use the resulting taste library and prompt structure.

## What "AI slop" actually is

Not a technical problem — a generic one. Better models just move the
average result up; taste is what breaks the mold, not raw capability.
The tells: blue-purple gradients, Inter font everywhere, the same layout
every time, rounded-everything friendliness, icon-grid feature rows,
evenly-distributed colorful palettes. If a design looks like it took only
a prompt or two, everyone can tell — because a real design took curation,
tools, and iteration, and it shows.

## Step 1 — Build a Taste Library

Curate real design references before writing a single prompt — your
taste is the moat, not the model:

1. **Source from real places**: Dribbble (search web design, sort by
   popular), Pinterest (hero layouts you'd never think to prompt), X/
   Twitter (designers posting live UI work), and screenshot anything that
   stops your scroll. Save links, not just images — a real live site
   beats a static screenshot for reference fidelity.
2. **Group by design family, not by project** — "print-tech x data,"
   "dither mono," "vast quiet," "classical" — categories you can name and
   reuse across many future builds, not a folder per client.
3. **Name it** — vocabulary is power. A named style ("Print-Tech Paper")
   drops straight into a prompt as a keyword; an unnamed folder of images
   doesn't.
4. **Reuse it** — every future build starts from this library, not from a
   blank prompt.

Optional: have Claude build a small library app around this collection —
each entry gets a design family (auto-grouped), a vocabulary (the words
the style is made of), keywords (drop straight into prompts), an image
prompt (for hero backgrounds), and a brief (the whole site's foundation).
Think of the progression as screenshots → library → better prompts, each
step compounding on the last.

## Step 2 — Arm Claude with anti-slop tools

Claude doesn't ship with eyes for its own design output or a shared
design vocabulary — install these:

- **[`pbakaus/impeccable`](https://github.com/pbakaus/impeccable)** —
  "the missing design vocabulary for agents." Verified real, 50,000+
  GitHub stars, runs inside Claude Code/Cursor/Codex/Gemini CLI. One
  skill, 23 commands, 59 deterministic detector rules for AI-slop and
  general design-quality issues (side-tab borders, purple gradients,
  bounce easing, dark glows, cramped padding, skipped headings, and
  more) across 7 dimensions (typography, color, spatial, responsive,
  interaction, motion, UX writing). Key commands: `/bolder` (pushes a
  safe design toward more impact without chaos), a slop audit that runs
  on a live dev server and clicks through component by component. Install
  by pasting the GitHub URL into Claude Code — it installs itself.
- **[`Leonxlnx/taste-skill`](https://github.com/Leonxlnx/taste-skill)**
  ("Taste Skill") — verified real, tens of thousands of stars. A portable
  skill that upgrades layout, typography, motion, and spacing decisions
  instead of boilerplate defaults; v2 reads the brief, infers the design
  language, and tunes three dials (VARIANCE / MOTION / DENSITY).
- **[21st.dev](https://21st.dev)** — copy-paste component prompts
  (buttons, cards, pricing sections) for when a specific component needs
  taste, not a from-scratch prompt.
- **Higgsfield MCP** — image/video generation reachable from inside
  Claude Code for hero imagery (model picks per the source: an image
  model for stills, a video model for motion). Already available as a
  connected MCP server in environments where Higgsfield is configured —
  check `/mcp` before assuming it needs installing.

Caution from the source, worth repeating: prefer flexible, taste-steered
tools over "one-trick" skills that are narrow, prescriptive, and produce
the same output every time regardless of input — the point of this whole
workflow is that *your* taste does the steering, not a fixed template.

## Step 3 — Never one-shot. Cast wide, then narrow.

One-shotting a design is a prompt lottery — if it lands, it was luck, not
process. Build wide instead:

1. **Five styles** — one page, five aesthetic families side by side, each
   fully committed to its own direction (no blending).
2. **Pick one, then three variants** — three body variants of the winning
   style.
3. **Pick again** — now nail the hero image (e.g. via Higgsfield: 4
   options, pick one, refine the color).
4. **Tweaks** — small moves: fonts, colors, motion.

Why wide beats deep: every option is visible on one screen at once
(compare, don't guess), and a terminal-only workflow hides the choices
that were actually available — fidelity rises as options get narrowed
visually, not blindly re-prompted.

## The 4-part prompt template

A reusable structure for briefing a multi-direction build in one prompt,
generalized from the source's worked example (a fictional "Kestrel"
analytics landing page):

```text
Build a landing page for "[PRODUCT NAME]" – [one-line description of what it is and who it's for].
Conversion goal: [primary action]. Primary CTA on every version is "[CTA TEXT]"; it must appear in the hero and repeat at the end of the page.

Intent: [the feeling/positioning in one sentence]. Should feel like [tone adjectives], not [the generic version of this category]. A [target reader] should think "[the one-line reaction you want]" within 3 seconds.

Guardrails – always: [non-negotiable visual rule 1]; [rule 2]; [rule 3]; [rule 4].
Never: [specific anti-slop bans — name the actual clichés to avoid: e.g. purple gradients, glossy 3D blobs, untextured stock photography, rounded-everything friendliness, icon-grid feature rows, system-font-only typography, evenly-distributed colorful palettes].

Create 5 versions of this page, each in its own folder (v1/ ... v5/), one per direction below. Same intent and guardrails for all five. Do NOT blend directions – each version commits fully to its own aesthetic.

IMPORTANT – hero images come later. Do NOT generate or source any imagery. For each version, reserve the hero slot exactly where the placement note says (<img> or background with the correct aspect and position) and fill it with a flat CSS stand-in that matches the direction's palette. Size all typography and negative space as if the described image were already there, so the real image drops in with zero layout changes.

--- DIRECTION 1 (v1) – [Named style from your Taste Library] ---
Aesthetic: [style keywords] – [palette/ground description], [signature visual technique]
[repeat for DIRECTION 2 (v2) through DIRECTION 5 (v5), one named style per direction from Step 1's library]
```

The **Aesthetic**, **Reference** (screenshots/live URLs — match the feel,
never copy), **Intent** (what it is, who it's for, what they should do),
and **Guardrails** (always/never lists) are the 4 inputs this prompt
encodes — the same 4 inputs work for a single-direction build, not just
a 5-way bake-off; just drop the multi-folder instructions.

## Iterate until it's yours

Once a direction is picked, don't beg the model for "more premium" —
build the actual controls and turn the dials:

1. **First**: nail the hero (multiple image options, pick one, refine the
   color).
2. **Then**: transitions — no hard cuts between hero and body.
3. **Next**: motion — check for heavy, over-weighted page loads and trim
   them.
4. **After**: ask Claude for a live tweaks bar (fonts, sizes, accents) —
   tweak visually, never guess values in the terminal.
5. **Always**: keep feeding it references from the Taste Library until
   the result feels like a specific choice, not a generic one.

## Related skills in this repo

- **hallmark**: This repo's existing vendored anti-AI-slop design skill —
  install the tools above, then hand a Taste-Library-informed brief to
  either `hallmark` or this skill's own 4-part prompt template, whichever
  the build calls for.
- **design-templates**: Ready-to-use HTML/CSS starting points — a good
  seed for the flat-CSS hero stand-ins this skill's prompt template asks
  for before real imagery is dropped in.
- **design-token-extractor**: Extract a token set from a chosen reference
  once Step 3 narrows to a winning direction, to keep the tweaks-bar step
  consistent.
- **design-review-audit**: A manual checklist companion to `impeccable`'s
  automated slop audit — run both before shipping.
- **design-dev-resources**: The design-inspiration-gallery and AI
  prompt-discovery-library entries there are additional Taste-Library
  sourcing options beyond Dribbble/Pinterest/X named in Step 1.
