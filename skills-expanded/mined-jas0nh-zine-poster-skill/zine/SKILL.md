---
name: zine
description: Create or transform ideas and photos into tactile editorial zine posters with an available image-generation model or harness. Use for `/zine`, `/zine --help`, minimal paper posters, photo-preserving Gathered Scenes collages, faithful-photo plus abstract-memory editorial diptychs, source-distilled illustrated zines, `单色块模式`, prompt-only zine art direction, and zine-style edits of supplied images. Always run the bundled style harness before generation.
---

# Zine Poster Studio

Route every generation through the deterministic style harness before the host agent's image-generation tool. Prefer GPT-Image-2 when available, but allow any model or harness that supports prompt-based generation and reference images. Never read or handle provider credentials directly.

## Command contract

Treat the instruction appended to `/zine` as command arguments.

- For `/zine --help`, `/zine -h`, or a bare `/zine`, run:

  ```bash
  python3 <skill-directory>/scripts/zine-command.py --command '/zine --help'
  ```

  Return the JSON `text` and exact `media` value. Do not generate a new image.
  The bundled guide is a single GPT-Image-2 composition showing all three channels and both `scenes` modes. Return it unchanged; do not crop, rebuild, or regenerate it during help display.
- Prefer three mutually exclusive subchannels: `/zine minimal`, `/zine scenes`, and `/zine editorial`.
- In `scenes`, accept `--preserve-photo` for the Gathered Scenes photo-anchor contract and `--distill` for semantic-only illustration.
- Accept `--mono-block`, `--ratio auto|portrait|landscape|square`, `--prompt-only`, and `--show-prompt`.
- Keep legacy `--style`, `--minimal`, `--gathered`, `--editorial`, and `--distilled` syntax compatible, but never combine contracts from different channels.
- Interpret the exact phrase `单色块模式` like `--mono-block`; do not infer it from ordinary minimal requests.
- Default to `--style auto`:
  - no reference image → `minimal`;
  - reference image + explicit semantic-only/redraw/reinterpret intent → `distilled`;
  - reference image + explicit faithful-photo/abstract-panel/diptych intent → `editorial`;
  - other reference-image requests → `gathered`.
- Require a reference image for `gathered` and `editorial`.

Examples:

```text
/zine minimal 雨夜旧书店
/zine scenes --preserve-photo 把这张街景做成保留照片锚点的纸刊
/zine scenes --distill --mono-block 把这张海边照片重构成关于距离的作品
/zine editorial 把原照和它的抽象记忆做成上下双联画
/zine --prompt-only --style minimal 一把被遗忘的雨伞
```

## Mandatory workflow

1. Read [references/style-harness.md](references/style-harness.md), but load and apply only the selected channel section.
   For `editorial`, follow its dedicated section and the linked upstream provenance without copying constraints from the other channels.
2. Inspect every supplied reference image before writing the card. Do not browse for replacement imagery.
3. Build a compact JSON card in a temporary file. Include only fields supported by the harness:
   - `brief`, `has_reference`, `reference_image`, `reference_images`;
   - `semantic_nucleus`, `subject`, `supporting`, `spatial_invariant`, `dominant_gesture`;
   - `mood`, `proposition`, `tension`, `metaphor`, `interpretive_opening`;
   - `composition`, `illustration_grammar`, `typography`, `text`, `hue`, `color_role`, `edge`, `discard`, `orientation`;
   - `observed_facts`, `palette`, `photo_panel_ratio` for `editorial`;
   - `preserve_photo` when the request explicitly settles that choice.
4. Keep analysis specific to the user's source. Do not put generic style prose into card values.
5. Confirm that the host exposes an image-generation tool capable of accepting a prompt and, for source-image channels, reference images. Prefer GPT-Image-2 when available; otherwise adapt the compiled arguments to the host tool without changing the prompt.
6. Compile through the harness:

   ```bash
   python3 <skill-directory>/scripts/zine-command.py \
     --command '/zine --style auto <user brief>' \
     --card /tmp/zine-card.json
   ```

7. Use the exact JSON `call.arguments.prompt` for one generation call. Map aspect ratio and reference-image fields to the host tool without rewriting, shortening, appending to, or bypassing the compiled prompt.
8. If `call` is `null`, return prompt-only output. Otherwise generate once. Regenerate at most once and only for a concrete failure named in the quality gate.
9. Return the generated image and one short Chinese rationale. Show the final prompt only for `--show-prompt`, `--prompt-only`, or an explicit user request.
10. For source-image runs, state briefly that the prompt and supplied reference image were sent to the configured image-generation service.

## Tool-call rules

- Use `call.arguments.prompt` exactly.
- Map `call.arguments.aspect_ratio` directly to `image_generate`.
- Pass `image_url` and `reference_image_urls` exactly when present.
- Do not pass an image to another service for inspection, hosting, search, or conversion.
- Do not persist source images into the skill or project.
- Generated output may remain in the host harness's normal cache path.

## Output

Default:

```markdown
![Zine poster](absolute-image-path-or-rendered-image)

**创作思路**

[One compact Chinese paragraph about the central visual decision and emotional intent.]
```

When prompt display is requested, append:

````markdown
**最终 Prompt**

```text
[exact compiled prompt]
```

**风格配方**

- Style: [minimal / gathered / editorial / distilled]
- Recipe: [composition / grammar / typography / hue / edge / mood]
````

## Quality gate

Before returning, verify:

- the harness ran and the prompt came from its JSON output;
- the result is a flat tactile paper artwork, not a glossy mockup, ad, UI, 3D render, cinematic frame, anime poster, or dense scrapbook;
- the selected style contract is visibly respected;
- 68–90% of the canvas reads as quiet paper unless source fidelity requires otherwise;
- one source-specific subject or relationship anchors the work;
- one exact high-chroma hue has a structural job, except `editorial`, whose panel palette must come only from the source photo and may stay muted;
- typography is short, intentional, legible enough for its role, and not invented metadata;
- `gathered` retains truthful photographic material and a visible hand-torn fibrous handoff;
- `editorial` keeps a faithful photo region beside a clean ivory abstract panel; its marks are source-traceable and the join has no torn edge, frame, shadow or collage depth;
- `distilled` contains no reproduced, embedded, cropped, traced, or photorealistic source pixels;
- `minimal` does not become a full illustrated scene or commercial poster;
- `单色块模式` contains one contiguous saturated field and no other chromatic printed form;
- the output includes an actual generated image unless prompt-only was requested.

For a correction, keep the same style and change only the failed dimension: source fidelity, density, hierarchy, color structure, photo boundary, no-photo rule, or text rendering.

## Provenance

This skill combines and adapts the MIT-licensed `gathered-scenes-zine-skill` and `gc-minimal-zine-poster`. See [references/upstream-licenses.md](references/upstream-licenses.md).
