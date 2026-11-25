---
name: illustrations
description: Generate absurd hand-drawn in-text illustrations for articles and posts. Use when the user asks to generate "absurd", "Xiaohei", "Tony Cozy Builder", "Tony Pocket Helper", "mascot", "hand-drawn", "in-text illustration", "article illustration", "illustration suggestions", "shot list", "remove title", or "edit image" work for articles, posts, blogs, Notion documents, workflow documents, methodologies, workflows, structures, states, metaphors, or viewpoints. Supports three mascot presets: Xiaohei, Tony Cozy Builder, and Tony Pocket Helper.
---

# Illustrations

## Core Positioning

Design and generate 16:9 horizontal in-text illustrations for articles and posts. The goal is not commercial illustration, PPT infographics, or cute cartoons, but to turn a key judgment, workflow, structure, state, or metaphor from the article into a clean, absurd, creative, readable hand-drawn explanatory image that does not feel like an instruction manual.

This skill supports three mascot presets: Xiaohei, Tony Cozy Builder, and Tony Pocket Helper. Xiaohei is the default deadpan absurd operator. Tony Cozy Builder and Tony Pocket Helper are warmer "aww" mascots with glasses, soft proportions, and earnest helper energy. The selected mascot must participate in the core action of the image and cannot just stand beside it as decoration.

## Read These References First

Read as needed for the task; do not load everything into context at once:

- `references/style-dna.md`: style DNA, colors, text, and taboos.
- `references/mascots.md`: mascot selection rules, including Xiaohei and Tony.
- `references/xiaohei-ip.md`: Xiaohei's appearance, personality, action library, and taboos.
- `references/composition-patterns.md`: structure types, original metaphor methods, and anti-copying rules.
- `references/prompt-template.md`: prompt template for generating a single image.
- `references/qa-checklist.md`: post-generation checking and iteration rules.
- `assets/examples/`: only for occasional visual calibration. Do not put it on the default generation path. Do not copy the compositions, objects, or labels from these examples.
- `assets/mascots/`: Tony mascot calibration examples. Use only when the user asks for Tony or another warm mascot direction.

## Workflow

### 1. Digest The Body Text

First read the body text, link, Notion page, Markdown file, or screenshot content provided by the user. Extract:

- The core point
- Which paragraphs carry cognitive turns
- Which content is suitable for visual explanation
- Which parts should remain text-only and do not need images

Do not illustrate evenly. Prioritize "cognitive anchors" such as a core judgment, two breakpoints, input-output loop, branching, before/after comparison, one source serving many uses, handoff path, common pitfalls, or character state change.

### 2. Produce An Illustration Strategy First

If the user only says "analyze how to illustrate this" or "think through which parts need illustrations", provide a shot list first. For each image, clearly state:

- Which paragraph it should follow
- Image theme
- Core idea
- Structure type
- What the selected mascot is doing in the image
- Suggested elements
- Suggested annotation words

Default to 4-8 images. For short articles, use 1-3 images. Even for long articles, do not casually exceed 9 images. Enough is enough; avoid turning the body text into a picture book.

### 3. Single-Image Generation

If the user explicitly asks to "generate", "output", "make an image", or "help me generate", do not stop for confirmation; generate each image separately using whichever image-generation tool is available in the session. Do not combine multiple images into one.

Claude Code has no built-in image generator, so use whatever image-generation capability is connected — for example an image-generation MCP server (a Hugging Face image space, a hosted text-to-image model, etc.). If no image tool is connected, do not silently stop: produce the per-image prompts from `references/prompt-template.md` and tell the user to either connect an image MCP or paste each prompt into their image generator of choice.

Each image should explain only one core structure. The prompt must include:

- 16:9 horizontal article illustration
- Pure white background
- Black hand-drawn line art
- Sparse red/orange/blue handwritten annotations in the user's requested language, defaulting to English
- Lots of whitespace
- The selected mascot as the subject performing the core action
- No PPT, commercial illustration, childish cuteness, complex architecture, or top-left type title

Do not copy previous examples. Examples only provide style density and ways a mascot can participate; do not directly reuse existing compositions such as "conveyor belt breakpoints / mascot pulling lines / source-material fish / stamped handoff-copy toolbox / common-pit path" unless the user explicitly asks to recreate a specific image. Every time, reinvent a strange but coherent metaphor from the current article.

### 4. Check And Iterate

After generation, check `references/qa-checklist.md`. If any of the following problems appear, prioritize regenerating or locally editing:

- The selected mascot is only decoration
- The image is too full
- It looks too much like a flowchart or PPT
- There is too much text or the generated text errors are severe
- A title such as "common pitfalls / flowchart / system architecture diagram" appears in the top-left corner
- The style is too cute, childish, or stiff
- The background is not clean white

### 5. Save And Deliver

If the user is working inside a workspace, copy the final images to:

```text
assets/<article-slug>-illustrations/
```

Name them in order:

```text
01-topic-name.png
02-topic-name.png
```

Preserve the original generated files and do not overwrite existing assets unless the user explicitly asks to replace them.

## Output Style

Strategy output before generation should be short and precise. Delivery after generation should include:

- How many images were generated
- The purpose of each image
- Save paths
- Which images are the strongest and which are optional

Do not give long explanations of style theory; let the images speak for themselves.
