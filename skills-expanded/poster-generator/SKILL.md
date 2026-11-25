---
name: poster-generator
description: Generates professional designer-grade posters, flyers, campaign visuals, event posters, and product posters. Use when the user asks for 海报, poster, flyer, campaign visual, event poster, product poster, promotional visual, or high-end marketing key visual.
---

# Poster Generator

Choose from 20 visual styles. The skill organizes the poster composition automatically from the content, channel, and aspect ratio.

This skill creates polished, modern, practical posters with production-ready image prompts.

## Usage

```bash
/poster-generator path/to/content.md
/poster-generator path/to/content.md --style swiss-editorial
/poster-generator path/to/content.md --aspect 4:5 --lang zh
/poster-generator "新品发布会，6月30日，上海" --style luxury-minimal
/poster-generator  # then paste content
```

## Options

| Option | Values |
|--------|--------|
| `--style` | 20 options, default: swiss-editorial |
| `--aspect` | 1:1, 4:5, 2:3, 3:4, 9:16, 16:9; default: 2:3 |
| `--lang` | en, zh, ja, etc.; default: source language |
| `--renderer` | name of an installed image-generation skill or MCP tool to use for rendering (e.g. `image-gen`, `baoyu-image-gen`). Default: auto-discovered at runtime. |
| `--backend` | passed through to the chosen renderer when it supports sub-backends (e.g. `jimeng`, `banana`, `gpt-image-2` for `image-gen`). Default: renderer's own default. |
| `--quality` | 1K, 2K, 4K where the renderer supports it |

Composition (how content is arranged on the poster) is handled automatically by the skill based on content, channel, and aspect ratio — users only choose a style. Advanced internal controls (including an optional `--layout` override for backward compatibility) are documented in `references/advanced.md`.

## Available Systems

Styles: `swiss-editorial`, `neo-brutalist`, `luxury-minimal`, `constructivist-impact`, `bauhaus-modular`, `pop-commercial`, `cinematic-key-art`, `data-editorial`, `organic-craft`, `futurist-gradient`, `editorial-collage`, `japanese-ma`, `monochrome-typographic`, `art-deco-luxe`, `risograph-zine`, `glassmorphism-ui`, `surreal-3d-editorial`, `retro-futurism`, `botanical-premium`, `hyperreal-product`.

Aspect ratios: `1:1`, `4:5`, `2:3`, `3:4`, `9:16`, `16:9`.

Use `references/selection-guide.md` to select the internal composition and recommend styles/aspect ratios. Style definitions live in `references/styles/<style>.md`; internal composition definitions live in `references/layouts/<layout>.md`.

## Output Structure

```text
poster/{topic-slug}/
├── source-{slug}.{ext}
├── analysis.md
├── structured-content.md
├── prompts/poster.md
└── poster.png
```

Slug: 2-4 words kebab-case from topic. Conflict: append `-YYYYMMDD-HHMMSS`.

## Design System

Universal poster rules live in `references/base-prompt.md`. Layout files define structure; style files define visual language; `quality-rubric.md` is only for review.

## Workflow

### Step 1: Setup & Analyze

**1.1 Load Preferences (EXTEND.md)**

Use Bash to check EXTEND.md existence (priority order):

```bash
# Check project-level first
test -f .baoyu-skills/poster-generator/EXTEND.md && echo "project"

# Then user-level
test -f "$HOME/.baoyu-skills/poster-generator/EXTEND.md" && echo "user"
```

If found: read, parse, and display a short summary. If not found: continue with defaults unless the user explicitly asks to configure preferences.

**EXTEND.md Supports**: preferred style, default aspect ratio, renderer preference (`renderer:`), sub-backend (`backend:`), quality preference, language preference, custom style definitions, brand constraints. A legacy layout preference remains supported for backward compatibility but should not be offered as a normal user setting. Validate any legacy layout value against the basename of a file in `references/layouts/`; if it is invalid, stop before rendering and list the valid IDs.

**1.2 Analyze and Extract → `analysis.md`**

1. Save source content (file path or paste → `source-{slug}.{ext}`).
2. Use `references/content-analysis.md` to identify input type, poster goal, audience, channel, language, constraints, and missing information.
3. Extract only poster-useful fields: headline, subheadline, key points, source-supplied CTA, metadata, visual subject, tone, and information priority. A CTA is extractive-only: leave it empty unless its wording exists in the source. If output language differs, preserve the exact source quote alongside the translated CTA for verification.
4. Save analysis.

### Step 2: Generate Structured Poster Content → `structured-content.md`

Transform `analysis.md` into poster-ready structure:

1. Main headline / title.
2. Subheadline or supporting message.
3. Must-show copy, optional copy, and omitted content.
4. Source-supplied CTA or intended communication goal. Do not invent action/status copy such as "敬请期待", "了解更多", "立即选购", "Coming soon", "Learn more", or "Shop now".
5. Metadata, visual subject, brand cues, required text labels.
6. Production constraints and design instructions.

**Rules**: Markdown only. Preserve required copy verbatim. Do not invent missing facts, CTA copy, or interface/status labels. If the source explicitly supplies a CTA, retain it as static poster copy; later prompt construction must not style it as a clickable button, pill, chip, tab, or input field.

See `references/structured-poster-template.md` for detailed format.

### Step 3: Select Composition & Recommend Styles

Use `references/selection-guide.md` for two separate decisions:

1. **Select the composition internally.** Resolve one layout from content goal, information density, visual subject, channel, aspect ratio, and any direct composition intent in the brief. Apply this priority order:
   - Explicit `--layout` override.
   - Legacy EXTEND.md layout preference.
   - Automatic selection rules in the guide, including recognized natural-language composition intent.
   - `centered-hero` only when no rule produces a clear result.
2. **Record the internal decision in `analysis.md`.** Store the selected layout ID, source (`cli-override`, `legacy-extend`, `auto`, or `fallback`), and the signals used. Do not show layout candidates or layout IDs in the normal user confirmation.
3. **Resolve the style source.** An explicit `--style` takes precedence over an EXTEND.md preferred style. If either is present, resolve it against a built-in `references/styles/<style>.md` definition or a custom style definition loaded from EXTEND.md, use it directly, and skip style recommendations. Otherwise, recommend 3-5 built-in visual styles based on audience, tone, subject, channel, and user design instructions. Each user-facing option includes only the style, why it fits, expected visual outcome, and any material risk. If a selected style ID is invalid, stop before rendering and list the valid built-in and configured custom style IDs.

### Step 4: Confirm Options

Present all options in a single confirmation:

1. **Style** (unless already specified by `--style` or EXTEND.md): 3-5 options with rationale. Tell the user that composition is handled internally as part of production; do not expose layout names.
2. **Aspect** (always): 2:3, 4:5, 9:16, 1:1, 3:4, 16:9.
3. **Language** (only if source language differs from requested/user language).
4. **Renderer/backend** (always — surface the auto-discovered renderer, plus sub-backend/quality if it supports them; let the user override).
5. **Update the draft artifact.** Write the confirmed style, aspect ratio, language, backend, quality, and production notes back into `structured-content.md`; confirmed values take precedence over the draft defaults from Step 2.

If the confirmed aspect ratio differs from the value used in Step 3, rerun automatic composition selection and update the internal record before generating the prompt. Do not rerun it when an explicit or legacy layout override is active.

### Step 5: Generate Prompt → `prompts/poster.md`

Combine:

1. Final internal layout definition from `references/layouts/<layout>.md`.
2. Selected style definition from `references/styles/<style>.md`, or the matching custom style definition loaded from EXTEND.md.
3. Base template from `references/base-prompt.md`.
4. Structured content from Step 2.
5. All confirmed output options.

Before rendering, apply this CTA guard to the combined prompt:

1. Verify every CTA against the source. If the output is translated, verify its recorded exact source quote instead.
2. Remove invented action/status copy even when it appears in headline, subheadline, key points, metadata, or must-show lists rather than the CTA field.
3. If no CTA is sourced, explicitly tell the renderer to leave the action area empty and invent no action/status wording.
4. If a CTA is sourced, render it as ordinary static poster typography in a footer or text lockup—no filled/outlined button, rounded rectangle, pill, chip, shadow, arrow, chevron, or cursor icon.
5. Treat the poster canvas as static print/editorial artwork. Preserve a browser window, dashboard, device mockup, or product UI when the user explicitly requests it as depicted content; only prohibit invented poster-level interaction chrome.

### Step 6: Generate Image

This skill does **not** hard-depend on any specific image-generation tool. At render time, discover the best available renderer in this order:

1. **User override** — `--renderer <name>` flag (skill name or MCP tool name), optionally combined with `--backend <sub-backend>` and `--quality`.
2. **EXTEND.md preference** — `renderer:` / `backend:` fields if present.
3. **Auto-discovery** — scan the environment for any working image-generation capability:

   **a. Image-generation skills** — look for skill names matching: `image-gen`, `*-image-gen`, `baoyu-image-gen`, `baoyu-cover-image`, `baoyu-article-illustrator`, or any skill whose description mentions generating / rendering / creating images from prompts. Invoke via the Skill tool.
   **b. MCP image tools** — look for MCP tools whose names match `*generate*image*`, `*image*generate*`, `*render*`, `*t2i*`, or `*text_to_image*`. Invoke directly with the prompt, aspect ratio, and output path.
   **c. CLI fallback** — if a known image-generation CLI is on `$PATH` (e.g. `image_gen.py`, `bananapro`, etc.), invoke it directly.

4. **Selection** — if multiple renderers are available, prefer in this order: user override > EXTEND.md > a skill that exposes sub-backends (e.g. one that can target `jimeng` / `gpt-image-2` / `banana`) > any other working renderer. Surface which one was picked in the confirmation step.
5. **No renderer found** — stop and tell the user explicitly: *"No image-generation skill or MCP tool detected. Install one (e.g. `image-gen`, `baoyu-image-gen`, or an MCP server that exposes image generation) and re-run."* Do not silently skip rendering.

**Mapping to renderer inputs** — when invoking the chosen renderer, pass:
- The full prompt from `prompts/poster.md`.
- Aspect ratio (mapped to the renderer's supported values; if the renderer only takes width/height, convert from the chosen `--aspect`).
- Output path: `poster/{topic-slug}/poster.png`.
- Sub-backend / quality only if the renderer accepts them.

**On failure** — inspect the error, adjust only the renderer invocation or prompt mechanics (not the structured content), and retry once. If it still fails, fall back to the next available renderer in the discovery list and retry once more.

### Step 7: Output Summary

Report: topic, style, aspect, language, backend, output path, and files created. Do not report the automatically selected layout. If the user explicitly passed `--layout`, add `Advanced layout override: <id>` to make that override auditable.

## References

- `references/content-analysis.md` - Input analysis, extraction, density control, and missing information policy
- `references/structured-poster-template.md` - Poster content structure
- `references/base-prompt.md` - Image prompt template
- `references/selection-guide.md` - Internal composition / style / aspect recommendations
- `references/quality-rubric.md` - Professional design quality checks
- `references/styles/<style>.md` - 20 style definitions
- `references/layouts/<layout>.md` - Internal composition definitions (not user-facing)
- `references/advanced.md` - Advanced internal controls (`--layout` override, legacy EXTEND.md layout preference)
