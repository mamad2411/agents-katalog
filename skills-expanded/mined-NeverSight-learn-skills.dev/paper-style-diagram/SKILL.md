---
name: paper-style-diagram
description: Create or revise clean white-background academic/paper-style diagrams and article infographics with modular boxes, restrained pastel colors, precise hierarchy, arrows, and Chinese-first labels. Use for 论文风配图、白底关系图、产品架构图、流程图、技术路线图、系统图、概念图谱，或把已有图重新排版为用户指定的任意宽高比或像素尺寸。
---

# Paper Style Diagram

Create polished raster diagrams for articles. Prioritize semantic accuracy, readable Chinese, clean hierarchy, and exact requested canvas proportions over decoration.

## Load references

- Read [references/style-spec.md](references/style-spec.md) before composing any diagram.
- Read [references/prompt-template.md](references/prompt-template.md) before calling image generation.
- Use [assets/example.png](assets/example.png) only as an optional visual-style reference. Ignore its brands, words, and topology unless the user explicitly requests them.

## Workflow

### 1. Resolve the request

Extract or infer:

- intended use and audience
- title and optional subtitle
- required entities or steps
- directed relationships and relationship labels
- exact in-image copy
- target aspect ratio or pixel dimensions
- output location

Ask only when missing information would materially change the meaning. Otherwise make conservative assumptions and state them briefly while working.

### 2. Resolve any requested canvas

Accept all positive aspect ratios. Do not restrict the user to a preset list or silently substitute the nearest common ratio.

Supported forms include:

- ratio: `3:4`, `7:10`, `1.91:1`, `21/9`, or another positive `W:H`
- dimensions: `1080x1440`, `1240×1754`, or another positive `WIDTH×HEIGHT`
- natural language: portrait, landscape, tall poster, long horizontal banner, article inline image

Apply these rules:

1. Exact pixel dimensions override a separately stated ratio when they conflict. Mention the conflict.
2. A numeric ratio overrides a generic orientation word.
3. If only a ratio is supplied, choose sensible final pixel dimensions that preserve that ratio exactly when integer dimensions permit.
4. If no canvas is supplied, infer one from the content density and publishing context; do not default every request to the same ratio.
5. For an existing diagram, **reflow the layout** for the target canvas. Do not merely stretch, squash, or crop the old composition.
6. Keep all text and connectors inside a safe margin of roughly 5% of the canvas.

### 3. Build the semantic blueprint

Before generating, write a compact internal blueprint:

```text
Title: ...
Subtitle: ...
Reading direction: top-to-bottom | left-to-right | center-out | layered
Nodes:
- ID | exact label | role | group/layer
Edges:
- source -> target | exact relationship label | solid/dashed
Footer takeaway: ...
```

Resolve ambiguous relationships here. Never ask the image model to invent product facts, arrows, rankings, or causal links. If current or niche facts are important, verify them using an appropriate authoritative source before generation.

Keep copy economical. Prefer one short heading plus one short explanatory line per module. Split dense material into multiple diagrams when readability would otherwise fail.

### 4. Apply language rules

- Use Simplified Chinese for all ordinary labels, captions, explanations, and relationship text.
- Preserve necessary proper nouns and established technical terms such as `Agent`, `LLM`, `API`, `WorkBuddy`, or model names.
- Do not add decorative English section labels such as `Overview`, `Layer`, or `Workflow` when a clear Chinese equivalent exists.
- Treat supplied text as verbatim. Do not translate, abbreviate, or rewrite it unless the user asks.

### 5. Generate

Treat the task as `infographic-diagram`. Follow the installed `imagegen` skill and use its built-in generation tool by default.

For a new diagram:

1. Convert the blueprint into the template from `references/prompt-template.md`.
2. State the target ratio or dimensions near both the start and end of the prompt.
3. List every required text string verbatim.
4. Describe exact edge directions separately from the visual style.
5. Request one clean final diagram, not a page of variants.

For an edit:

1. Inspect the edit target first.
2. Repeat invariants on every edit: exact text to preserve, unchanged nodes, unchanged relations, and target canvas.
3. Make one targeted correction per iteration when possible.

### 6. Validate and repair

Inspect the generated image before delivery. Check:

- all required nodes appear exactly once
- Chinese and proper nouns are spelled correctly
- every arrow begins and ends at the intended modules
- relationship labels sit beside the correct connectors
- no connector crosses through text or an unrelated module
- grouping, hierarchy, and reading order match the blueprint
- the background, palette, typography, spacing, and line weights match the style specification
- nothing is clipped and the requested ratio is respected
- no watermark, mock UI chrome, stock illustration, or invented logo appears

When a semantic or text error exists, repair that single error with an edit instead of regenerating an unrelated composition. Re-check after every repair.

### 7. Enforce exact dimensions when needed

Image generation may return a composition close to, but not exactly at, the requested dimensions. First generate or edit the composition so it visually fits the target shape. Then use the bundled script only for deterministic final canvas sizing:

```bash
python scripts/fit_canvas.py \
  --input <generated.png> \
  --output <final.png> \
  --width <WIDTH> \
  --height <HEIGHT>
```

For a ratio without explicit dimensions:

```bash
python scripts/fit_canvas.py \
  --input <generated.png> \
  --output <final.png> \
  --ratio <W:H> \
  --long-edge 1600
```

The default `contain` mode preserves the whole diagram without distortion and adds only white canvas where necessary. Do not use `cover` for diagrams unless the user accepts cropping. If the added whitespace is visually excessive, return to image generation and reflow the composition before fitting again.

### 8. Save and report

- Copy the final image into the user-requested destination or current project.
- Never overwrite an existing file unless replacement was explicitly requested; use a versioned filename.
- Report the final path, pixel dimensions, aspect ratio, final prompt, and whether generation or edit mode was used.

## Quality bar

Do not deliver a first draft with wrong text, ambiguous arrows, clipped elements, or a substituted ratio. A successful result should be understandable within a few seconds and remain legible at normal article width.
