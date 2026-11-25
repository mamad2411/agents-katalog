---
name: image-generation
description: Generate and edit images via OpenAI's GPT Image 2.6 API. Use for requests to create, draw, edit, extend, combine, or remove backgrounds from images. Outputs PNG, JPEG, or WebP files to disk and requires OPENAI_API_KEY.
---

# Image Generation (OpenAI GPT Image 2.6)

Generate images from text or edit existing images using OpenAI's GPT Image 2.6 models (released 04.11.2026). Run `scripts/generate.py`, which has no third-party Python dependencies.

Use `gpt-image-2.6-flare` by default. It is OpenAI's fast model: with `--quality low` it returns in about six seconds. Use `gpt-image-2.6-sunburst` when detail, layout or edit accuracy matter more than latency. `--complexity low|medium|high` (2.6 only) sets how hard the model reasons about the prompt; the API uses `high` when omitted, so pass `low` or `medium` for simple assets to save time.

## Prerequisite

`OPENAI_API_KEY` must be exported in the shell. The user keeps it in `~/dotfiles/zsh/ignored/` (auto-sourced). If unset, the script exits with a clear error. To verify:

```bash
[ -n "$OPENAI_API_KEY" ] && echo ok || echo "set OPENAI_API_KEY first"
```

## Quick start (text-to-image)

```bash
~/.claude/skills/image-generation/scripts/generate.py \
  "A minimalist watercolor of a fjord at dawn, soft blues" \
  --size 1024x1024 --quality high
```

Writes `image_<timestamp>_1.png` to the current directory and prints the absolute path. The user expects you to print the path so they can open it.

## Quick start (image edit)

```bash
~/.claude/skills/image-generation/scripts/generate.py \
  "Make the sky a vivid sunset" \
  --edit-image ./photo.png \
  --quality high
```

Multiple input images (up to 16) compose into a single output:

```bash
~/.claude/skills/image-generation/scripts/generate.py \
  "Combine these into a product hero shot" \
  --edit-image mug.png --edit-image background.png
```

## Workflow

1. **Flesh out the prompt.** Never pass the user's request verbatim. Expand the brief into a richer prompt that names:
   - subject and pose/action
   - setting and time of day
   - art style or medium (photo, watercolor, 3D render, line art, etc.)
   - lighting, mood, palette
   - composition, framing, camera angle
   - level of detail and any "no X" exclusions

2. **Present the drafted prompt before executing.** Show the user the rewritten prompt and the planned flags (size, quality, n, edit images if any) and wait for confirmation. Format:

   ```
   Drafted prompt:
   > <full rewritten prompt>

   Flags: --size 1024x1024 --quality high --n 1
   Proceed? (or tell me what to tweak)
   ```

   If the user says "go" / "yes" / "ship it", run the script. If they tweak, redraft and re-confirm.

3. Confirm `OPENAI_API_KEY` is set. If not, tell the user to `export OPENAI_API_KEY=...` and stop.

4. Decide generate vs. edit based on the request. Edit needs at least one `--edit-image`. For edits, the prompt should describe the *change*, not redescribe the whole image.

5. Pick a sensible model, size, quality, and complexity. Use Flare unless the request calls for Sunburst's tighter edit control. Default `auto` for size and quality. Use `xhigh` or `max` only when the user values detail more than latency and cost.

6. Run the script. If it exits non-zero, surface the error message verbatim (it includes the OpenAI error body).

7. Print the output path(s). Do not embed the image inline.

## Skipping the confirmation

If the user pre-approves with phrases like "just generate it", "go ahead", "no need to confirm", or "iterate until I say stop", skip step 2 for the rest of the session. Otherwise always confirm.

## Style presets

The `styles/` subdirectory holds named style presets the user has saved as favorites. Each file documents the visual DNA, trigger keywords, and a reusable prompt fragment for one named aesthetic.

When the user references a style by name or uses any of its trigger keywords (e.g. "editorial illustration", "the post 35 look", "magazine style", "Economist vibe", "like The Atlantic", "app mascot", "app icon", "app branding", "Disco Elysium", "Revachol"), read the matching file and weave its reusable prompt fragment into the prompt you build, then add the subject-specific details on top. List the current presets with `ls ~/.claude/skills/image-generation/styles/` if you are unsure which one applies.

## Parameters

| Flag | Default | Values |
|------|---------|--------|
| positional `prompt` | (required) | up to 32,000 chars |
| `--model` | `gpt-image-2.6-flare` | `gpt-image-2.6-flare`, `gpt-image-2.6-sunburst`, `gpt-image-2.5-flare`, `gpt-image-2.5-sunburst`, `gpt-image-2`, `gpt-image-1.5`, `gpt-image-1`, `gpt-image-1-mini` |
| `--size` | `auto` | `auto`, recommended sizes `1024x1024`, `1536x1024`, `1024x1536`, or custom `WxH` for GPT Image 2.5 and 2.6 where both edges are multiples of 16, the aspect ratio is 1:3 to 3:1, neither edge exceeds 3840 px, and total pixels are 655,360 to 8,294,400 |
| `--quality` | `auto` | `auto`, `low`, `medium`, `high`; GPT Image 2.5 and 2.6 also support `xhigh` and `max` |
| `--complexity` | unset (API uses `high`) | `low`, `medium`, `high`; GPT Image 2.6 only |
| `--n` | `1` | `1`-`10` |
| `--format` | `png` | `png`, `jpeg`, `webp` |
| `--background` | `auto` | `auto`, `transparent`, `opaque` (transparent requires png/webp) |
| `--output` | `image_<ts>_<i>.<ext>` | output path; with `--n>1`, `_<i>` is appended before the extension |
| `--edit-image` | (none) | path to an input image; repeatable, max 16 |
| `--mask` | (none) | PNG mask file; transparent pixels mark editable regions (edit mode only) |
| `--input-fidelity` | unset | `low`, `high` in edit mode. `gpt-image-2` always uses high-fidelity image inputs, so the script warns and drops this flag for that model. |
| `--compression` | unset | `0`-`100` (jpeg/webp only) |

## Notes

- The script loads the macOS system CA bundle when Python has no CA roots (python.org builds), so no `SSL_CERT_FILE` is needed.
- OpenAI also announced SVG export, animated GIF output and `markup` edits for 2.6. The script does not expose them yet; check the API reference before adding them.

- GPT Image returns base64; the script decodes and writes it to disk.
- Complex prompts can take up to two minutes. `xhigh`, `max`, `--complexity high`, and Sunburst can take longer than everyday Flare requests.
- Cost varies by size and quality. The script does not estimate cost.
- For brand-safe or work content, keep `moderation` at default `auto`. The `--moderation low` flag exists for less restrictive filtering but is rarely needed.
- This skill does not view the resulting image. If the user wants to see it, suggest `open <path>` on macOS.
