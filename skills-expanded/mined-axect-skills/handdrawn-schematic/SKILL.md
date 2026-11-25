---
name: handdrawn-schematic
description: "Generate a hand-drawn, whiteboard-sketch schematic that explains a concept, pipeline, architecture, algorithm, or mechanism at a glance, on a pure white background. Composes a friendly hand-lettered infographic prompt (wavy marker strokes, numbered panels flowing left to right, chunky chalk arrows, hand-written notes beside shapes) and by default renders it to a PNG via the bundled codex image_generation tool (ChatGPT OAuth); falls back to emitting the copy-paste prompt when codex is unavailable. Use when the user wants a hand-drawn / hand-written / whiteboard-style schematic, a sketch diagram that shows a schema, a friendly explainer figure, a doodle-style method overview, or 손그림/화이트보드 스타일 도식/개념도. For matplotlib data plots use scienceplot-py or xkcd-py; for a multi-style (editorial, blueprint, neon, poster) prompt-only composer use wide-slide-illustrator; for the paper-review method+results pair use journal-club-review."
---

# Hand-Drawn Schematic

Turn any schema (a concept, pipeline, architecture, algorithm, or mechanism)
into a single friendly hand-drawn whiteboard illustration on a **pure white
background**: wavy marker strokes, numbered panels flowing left to right, chunky
chalk-style arrows, and short hand-written notes drawn beside the shapes. Every
label, number, and equation is lettered by the same hand into the one drawing,
so it reads like a research postdoc's explainer sketch for a small-group talk.

By default this skill **renders a PNG** with the bundled `codex`
image_generation tool (ChatGPT OAuth, no API key). When codex is not available
it falls back to emitting the finished prompt so the user can paste it into any
image generator.

## When to use

- "Draw a hand-drawn schematic of how X works"
- "Make a whiteboard-sketch figure explaining this pipeline / architecture"
- "Sketch a doodle-style diagram of this algorithm"
- "이 개념/구조 손그림 도식으로 그려줘" / "화이트보드 스타일 개념도 만들어줘"

Do NOT use for:

- Real data plots (matplotlib, seaborn, plotly) → `scienceplot-py` (publication
  `science`+`nature` style) or `xkcd-py` (sketch-style matplotlib from data).
- A multi-style prompt-only composer across six looks (Editorial Magazine,
  Engineering Blueprint, Swiss Minimalist, Dark Tech/Neon, Scientific Poster)
  → `wide-slide-illustrator`.
- The paired method + results infographics inside a paper walkthrough →
  `journal-club-review` (this skill is the reusable single-figure generator
  extracted from it, retuned to a white background).

## Inputs

Whatever the user gives you about the schema to draw. Gather (or infer from the
provided source: a paragraph, a code file, a paper section, a research-log
entry):

1. **Headline** — the figure title, <= 8 words.
2. **Subtitle** — one sentence saying what the figure shows.
3. **Panels** — the 3 to 6 stages/steps the schema breaks into, left to right,
   each with a short label and a concrete visual description (boxes, arrows,
   small charts, symbols, the exact equations/labels to hand-letter).

Do not hallucinate domain content. Pull equations, symbols, axis labels, and
parameter names verbatim from the source when one is provided.

## Workflow

### 1. Build the figure brief

Compose a small brief from the schema (schema and rules in
`references/style-block.md`):

```
{
  "headline": "<= 8 words, the figure title",
  "subtitle": "one sentence describing what the figure shows",
  "panels": [
    {"name": "Panel label", "content": "visual description: boxes, arrows, labels, small charts"},
    ...
  ]
}
```

- Panels flow left to right as a pipeline / narrative (input -> ... -> output),
  or as parallel facets of one idea. Aim for 3-6; widen the most content-heavy
  panel slightly.
- `content` is a **visual** description (what to draw), not prose.
- Every label is a **hand-written note drawn beside the shape**, never a pasted
  box or floating caption.
- Panels are **English-only** and keep labels short (<= 6 words per line), even
  when the surrounding conversation is in another language.
- If a panel contains a chart (bars, curve, box plot), say so explicitly and
  demand it stay hand-drawn: "wobbly hand-drawn marker bars with uneven tops,
  hand-lettered numbers, NOT a clean digital/matplotlib chart." Otherwise the
  model renders a crisp vector chart that clashes with the sketch.

### 2. Compose the full prompt

Read `references/style-block.md` and concatenate, in order: the SINGLE COHESIVE
block, the OVERALL LOOK block (pure white background), TYPOGRAPHY, COMPOSITION,
MOOD, then the title bar + panels filled from the brief, then the English guard.
The style wording is load-bearing; use it verbatim, do not paraphrase.

### 3. Render (default) or fall back to prompt-only

Check codex first:

```bash
codex login status        # need "Logged in using ChatGPT"
```

**If logged in**, write the composed prompt to a temp file and run codex,
saving the PNG where the user wants it (default `./schematic.png`):

```bash
mkdir -p <out_dir>/.codex-logs
codex exec \
  --sandbox workspace-write \
  --skip-git-repo-check \
  --cd <out_dir> \
  -o <out_dir>/.codex-logs/schematic.md \
  "Use the image_generation tool to create the following wide 18:9 infographic slide and save it as ./schematic.png in the current directory. Do not edit any other files. Report only the saved file path.

PROMPT:
<composed prompt>"
```

For several figures, launch the codex jobs in the same turn with
`run_in_background: true` so they render concurrently (~1-2 min each). After a
job finishes, verify the PNG exists and is non-empty before reporting it:

```bash
[ -s <out_dir>/schematic.png ] && echo ok
```

**If codex is not logged in** (or the user asked for "prompt only" / "no
render"), skip generation and deliver the composed prompt inside a fenced code
block so the user can paste it into their own image generator (ChatGPT Image,
gpt-image, DALL-E, Midjourney). Note the aspect-ratio caveat: gpt-image-1
supports 1024×1024 / 1024×1536 / 1536×1024, so generate 18:9 at 1536×1024 and
crop, or use a service with custom dimensions.

### 4. Deliver

- Tell the user the saved PNG path (or hand over the prompt if prompt-only).
- If a render came out garbled (broken labels, vector-looking chart), say so and
  offer one retry; text rendering usually needs 1-2 tries.

## Notes

- Rendering depends on a logged-in bundled `codex` runtime (ChatGPT OAuth). No
  API key is used. Without it the skill still produces the finished prompt.
- The only surface difference from the journal-club friendly-whiteboard block is
  the background: **pure white (#FFFFFF)**, no cream/beige tint. Everything else
  (palette, wavy strokes, numbered badges, chalk arrows) is unchanged.

## Files

- `references/style-block.md`: the canonical pure-white style block (verbatim,
  load-bearing), the figure-brief schema, the English guard, and the exact
  `codex exec` invocation.
