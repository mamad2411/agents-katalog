---
name: modellix-image-prompt-engineering
description: Engineer clear, high-density prompts for AI image generation and editing before execution. Use this skill whenever a user asks for a poster, banner, product shot, packaging concept, editorial illustration, UI mockup, slide visual, icon set, character sheet, card set, sprite sheet, image edit, or a better image prompt—even when they do not say "prompt engineering." Turn vague visual requests into an execution-ready T2I or I2I brief, then hand generation to modellix-design. Skip article covers, in-article illustration sets, casting boards, knowledge comics, product TVCs, video/audio tasks, structured infographics, CLI/auth troubleshooting, and requests that already contain a complete prompt and only need execution.
license: MIT
compatibility: No external tools required; pairs with the modellix-design skill for image execution.
metadata:
  author: Modellix
  version: "1.2.0"
  modellix-hermes-tags: image-generation,prompt-engineering,art-direction,visual-design,modellix
---

# Modellix Image Prompt Engineering

Convert an image idea into a deliberate, execution-ready prompt. This skill is the
creative planning layer; `modellix-design` is the execution layer.

Do not submit, poll, download, authenticate, or inspect model schemas here. Do not
run the Modellix CLI. Do not recommend a model, a provider, or a slug. Catalogs
change quickly, and choosing a model is outside this skill. When the user wants an
image generated, finish the brief first and then hand it to `modellix-design`.

## Route the request

Use this skill when any of these are true:

- The request is a vague visual brief: "make it premium," "create a launch cover,"
  or "give me a clean product graphic."
- The user wants a prompt written, expanded, repaired, or made less generic.
- The task needs art direction, composition, on-image text, a reference strategy,
  or a coherent batch/grid.
- An earlier result failed visually and the prompt needs a targeted revision.

Skip or keep the pass minimal when:

- The user supplied a complete prompt and explicitly asked only to run it. Pass it
  directly to `modellix-design`.
- The request is a structured infographic, visual summary, or information diagram.
  Use `modellix-infographic`.
- The request is an article, blog, or newsletter cover. Use `modellix-cover-image`.
- The request is a set of illustrations placed through an article. Use `modellix-article-illustrator`.
- The request is a casting board, talent board, 选角图, 定妆照, or turnaround lookbook. Use `modellix-casting`.
- The request is a knowledge comic, educational comic, biography comic, or four-panel strip that still needs a storyboard. Use `modellix-comic`.
- The request is a vertical ecommerce UGC video that still needs a shot plan.
  Use `modellix-ecomm-ugc-video`.
- The request is a cinematic product commercial, TVC, or brand film. Use
  `modellix-tvc`.
- The request is a finished video prompt, audio, credentials, task status,
  downloads, model schemas, or command syntax. Use `modellix-design`.
- The user only wants image compression, format conversion, cropping, or reuse of
  an existing asset without generative changes.

If a supplied prompt is already specific, perform at most a one-line readiness
check. Do not rewrite it merely to demonstrate this skill.

## Core principle: maximize decision density

Prompt quality is not proportional to prompt length. A strong prompt packs useful
visual decisions into each phrase.

Before writing, fill three slots:

1. **Subject** — the actual person, object, product, scene, or information.
2. **Visual system** — an established design movement, studio, brand language,
   medium tradition, or precisely described visual grammar.
3. **Medium** — poster, instruction manual, editorial illustration, packaging,
   product photograph, UI screen, icon sheet, and so on.

Prefer precise, recognizable references over adjective piles:

- Weak: "premium, minimalist, modern, professional product layout"
- Stronger: "Dieter Rams-era Braun product manual for a pocket camera"

A name is useful only when it compresses relevant decisions. Check that its native
medium fits the target. A reference known for industrial products may transfer
well to packaging or manuals but poorly to a dense statistical table.

Do not invent designers, studios, movements, brands, products, quotations, dates,
or specifications. If a factual reference matters and cannot be verified, replace
it with explicit visual attributes.

## Choose a working mode

### Explore

Use when the user has a topic but no visual direction. Offer three genuinely
different directions. For each, state:

- the visual-system anchor,
- why it fits the audience and purpose,
- the medium and composition idea,
- the main risk or cliché to avoid.

Ask the user to choose only when the directions would materially change the
result. If the user delegated the choice, pick the strongest direction and explain
the decision in one sentence.

### Hybrid

Use for most everyday work. Lock the audience, message, medium, and major
constraints. Leave room for the image model to contribute secondary details.

### Execute

Use when the user already has a brand system, reference images, exact copy, or a
defined layout. Translate those decisions faithfully; do not add a competing art
direction.

## Build the prompt

Work through these layers internally, then produce one natural prompt rather than
fake configuration sections.

### 1. Intent

Identify:

- who will see the image,
- what they should notice first,
- what they should understand or feel,
- where the image will be used.

For a platform-specific asset, verify current dimensions when tools are available.
Do not rely on remembered platform sizes. If dimensions cannot be verified, state
an aspect ratio and mark exact pixels as unresolved.

### 2. Visual hierarchy and composition

Specify only decisions that affect the image:

- primary focal point and scale,
- subject placement,
- foreground/background relationship,
- text-safe or empty space,
- camera angle, lens language, or illustration viewpoint,
- information hierarchy for diagrams and UI,
- crop and aspect ratio.

Spatial relationships are valuable detail. Decorative adjective lists are not.

### 3. Visual system

Choose one strong primary anchor. Add a second only when it has a distinct job,
such as one anchor for layout and another for material or color.

When a named reference is obscure, atmosphere-driven, or likely to be interpreted
superficially, add concrete attributes: grid, palette, line quality, lighting,
texture, typography class, and density.

Publication and media names can appear as accidental mastheads or watermarks.
When using one as a visual reference, explicitly exclude the publication name,
logo, masthead, and unrelated English copy from the image.

### 4. Text and factual content

Follow the user's language or the intended audience's language. Preserve official
brand names, product names, acronyms, and requested quotations exactly.

- Put exact on-image copy in quotation marks.
- Keep text short enough to remain legible.
- Never fabricate data, testimonials, product specifications, logos, or legal
  claims. Use an intentional blank or a clearly marked placeholder when facts are
  unavailable.
- State whether descriptive on-image text should be Chinese, English, bilingual,
  or absent.

### 5. Constraints

Add constraints only for likely failure modes:

- no unrelated logo, watermark, signature, or masthead,
- no extra text,
- preserve identity or product geometry,
- keep key information inside a safe area,
- avoid a named cliché relevant to this task.

Avoid generic negative-prompt inventories. Too many prohibitions dilute the main
intent.

## Prompt style

Write the actual image prompt in the audience's language unless the user requests
otherwise. Keep official names in their original form.

Do not use pseudo-structured headings inside the prompt, such as `Subject:`,
`Style:`, or `Constraints:`. Those headings often create verbose, generic output.
The handoff brief may use labels; the prompt string itself should read naturally.

Short prompts are appropriate when the subject, visual system, and medium are all
strong anchors. Complex compositions may need longer prompts because positions,
copy, and factual relationships are real decisions. Remove a phrase if deleting it
would not change the intended image.

## Specialized routes

Read only the reference needed for the task:

- Read `references/prompt-playbook.md` for mode selection, prompt patterns, and
  single-image workflows.
- Read `references/concept-library.md` when the request needs a better named anchor
  or the chosen reference does not fit the medium.
- Read `references/batch-grids.md` for icon sets, character sheets, card sets, or
  sprite sheets.
- Read `references/failure-modes.md` when repairing a failed result.

For I2I, describe what must remain unchanged before describing the change. Assign
each reference image a role: subject identity, style, composition, product, or
background. Do not assume that every image controls every property.

A structured infographic belongs to `modellix-infographic`. That skill confirms
the information structure and writes the single image prompt.

For UI mockups, identify the user's decision on that screen, the primary action,
and the information hierarchy. Do not optimize only for visual polish.

## Batch and grid principle

When the user wants a coherent set, prefer one semantic grid prompt for small
sets when consistency matters. Match the overall canvas ratio to the grid and cell
ratio. Describe an imagined grid but prohibit drawn grid lines, borders, labels,
registration marks, and cell numbers unless requested.

Do not promise automatic extraction or transparent assets. This skill does not
ship image-processing dependencies. Read `references/batch-grids.md` for the
handoff and post-processing caveats.

## Pre-handoff review

Before presenting the result, check:

1. **Intent:** Is the audience, purpose, and first-read message clear?
2. **Three slots:** Are subject, visual system, and medium specific?
3. **Fit:** Does the reference's native medium transfer to this target?
4. **Density:** Does every phrase change a visual decision?
5. **Composition:** Are hierarchy and spatial relationships clear where needed?
6. **Text:** Is exact copy quoted, audience language explicit, and fabricated
   content avoided?
7. **Reference risk:** Could a brand or publication become a masthead or watermark?
8. **Execution boundary:** Has this skill avoided submission, model-schema work, and any model recommendation?

If an item fails, repair the prompt before handoff.

## Handoff format

Return this compact brief:

```text
Image brief
- Task: T2I | I2I
- Prompt: "<final natural-language prompt>"
- On-image text: <none | language and exact copy>
- Aspect/size: <verified value | requested value | unresolved>
- Reference images: <none | paths/URLs with roles>
- Model: <only a slug the user already named | omitted>
- Next step: <stop after prompt | pass to modellix-design for execution>
```

Leave `Model` blank unless the user already named a slug. Do not fill one in, and
do not browse the catalog from this skill.

If the user asked only for prompt work, stop after the brief. If the original
request asked for generation or editing, pass the finished brief to
`modellix-design` and let that skill own schema validation, credentials, paid
submission, waiting, and download.

## Revision after a generated result

Do not repeat the same prompt and hope for a different outcome. Identify the
failed layer:

- wrong idea or emotion → revise intent,
- weak hierarchy or crop → revise composition,
- generic look → replace or clarify the visual-system anchor,
- incorrect text → reduce and foreground exact copy,
- unwanted masthead/watermark → remove the risky reference name or add a narrow
  exclusion,
- identity/product drift → strengthen preservation instructions and reference
  roles,
- overloaded image → remove secondary elements.

Then return a revised handoff brief. The execution skill decides how to recover an
existing task or whether a new paid submission is appropriate.

## Attribution

The decision-density, named-reference, and failure-diagnosis approach is inspired
by [alchaincyf/huashu-gpt-image](https://github.com/alchaincyf/huashu-gpt-image)
(MIT). This skill is an English, Modellix-oriented methodology layer; it is not a
fork and is not tied to GPT-image-2.
