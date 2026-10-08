---
name: peanut-illustrations
description: Turn a short prompt into one clean, hand-drawn concept illustration starring a deadpan peanut. Use when the user gives an idea, judgment, process, feeling, or metaphor as a short prompt and wants a single "peanut" illustration, concept sketch, explainer image, article figure, or visual for it. Default style is a deadpan in-shell peanut, black hand-drawn line art on white, one warm-orange accent, lots of whitespace, one idea per image, and the exact bottom-right watermark "© peanut-illustrations-by-aish" added after generation — composed first, then generated.
---

# Peanut Illustrations

## Core idea

Turn a short prompt into one 16:9 hand-drawn concept illustration. The goal is not commercial art, a PPT infographic, or a cute cartoon — it is to take a single idea (a judgment, process, contrast, state, or metaphor) and draw it as a clean, deadpan, slightly absurd sketch that reads in about one second.

The recurring character is **the peanut**: a whole in-shell peanut with dot eyes, two thin legs, and a blank, serious expression — completely unbothered while gravely doing a ridiculous job. The peanut must perform the core action of the image, not stand beside it as decoration.

Input is a **short prompt**, not an article. The user already knows the idea; this skill's job is to invent a fitting visual metaphor, put the peanut to work inside it, and draw it well.

## The contract: compose first, then draw

For each prompt, **think briefly out loud, then generate one image**. Before calling the image model, state:

- **Metaphor** — the fresh low-tech metaphor you invented for this prompt.
- **Peanut's action** — what the peanut is physically doing to drive the idea.
- **Labels** — the short English handwritten labels that will appear (a few; at most 5-8).
- **Composition** — where the peanut sits, the main object, and how the eye moves.
- **Watermark** — reserve a quiet lower-right margin for the exact watermark `© peanut-illustrations-by-aish`; do not ask the image model to render this text.

Then generate **one** image. One prompt → one composed image. Do not fan out into variations unless the user asks. If the user gives several prompts, make one image each.

## Read these references as needed

Pull in only what the task needs; do not load everything at once:

- `references/style-dna.md` — the visual DNA: line, color (single warm-orange accent), whitespace, hard nos.
- `references/peanut-character.md` — the peanut's form, personality, action vocabulary, and don'ts.
- `references/composition-patterns.md` — structure types and how to invent a fresh metaphor every time.
- `references/prompt-template.md` — the fill-in-the-blanks single-image generation prompt.
- `references/qa-checklist.md` — post-generation checks and iteration moves.

## Workflow

### 1. Read the prompt

Take the user's short prompt and decide what *kind* of idea it is: a judgment, an input→output process, a before/after contrast, a character/user state, or a concept metaphor. That choice picks the structure type. Do not over-interpret a one-liner into a whole article — illustrate the single idea in front of you.

### 2. Compose (think briefly)

State the metaphor, the peanut's action, the labels, and the composition (see "The contract" above). Keep it to a few lines — enough for the user to catch a wrong take in one second, not an essay.

### 3. Generate one image

If the user clearly asks to generate, do not stop for confirmation — use the built-in image tool and produce one image with the prompt template. Each prompt must include:

- 16:9 horizontal concept illustration
- pure white background
- black hand-drawn line art
- exactly one warm-orange accent color (no other colors)
- lots of whitespace
- the peanut as the subject performing the core action
- a few short handwritten English labels
- a quiet lower-right margin for the watermark
- no PPT look, no commercial illustration, no childish cuteness, no complex architecture diagram, no top-left type-title

Invent a fresh metaphor for every prompt. Do not reuse a metaphor from a previous image unless the user explicitly asks to reuse or remix one.

### 4. Check and iterate

Run `references/qa-checklist.md`. Regenerate or do a local edit if:

- the peanut is only decorative
- the canvas is too full
- it looks like a flowchart or slide
- there is too much text or garbled text
- a type-title appears in the top-left corner
- the style drifts cute, childish, or stiff
- a second accent color crept in, or the background is not clean white

### 5. Add the watermark

After choosing the final generated image, add the exact watermark locally before reporting it:

```text
© peanut-illustrations-by-aish
```

Use `scripts/add_watermark.py` so the text is exact and does not depend on the image model. Keep the watermark small, black, low-prominence, and tucked into the bottom-right quiet margin. It is not a concept label and does not count toward the label limit. Do not use the warm-orange accent for the watermark.

### 6. Save and report

If working inside a workspace, copy the final image to:

```text
assets/<prompt-slug>-illustrations/
```

Name in order:

```text
01-topic-name.png
02-topic-name.png
```

Keep the original generated file and the unwatermarked generated source. Do not overwrite existing assets unless the user asks to replace them.

## Output register

Keep the pre-generation "compose" note short and concrete. After generating, report:

- how many images were made
- what each one is
- the save path

Let the image do the talking; do not lecture about style theory.
