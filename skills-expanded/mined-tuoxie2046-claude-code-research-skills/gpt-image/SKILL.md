---
name: gpt-image
description: Generate, edit, describe, or batch-generate images from the terminal using OpenClaw + OpenAI gpt-image-2 (billed to the ChatGPT/Codex subscription, not the API). Use whenever the user asks to create / draw / generate an image, picture, icon, logo, illustration, poster, diagram, architecture figure, flowchart, or infographic — to produce a set / batch of multiple images from several prompts — or to edit an existing image (inpaint / restyle / combine) or describe what is in an image file.
allowed-tools: Bash, Read
---

# gpt-image — image generation via OpenClaw (gpt-image-2)

Wraps `openclaw infer image` so Claude Code can produce and inspect images. Image
generation runs through OpenClaw's OpenAI provider on the **Codex/ChatGPT OAuth**
subscription (`transport=codex-responses`), so it consumes subscription quota, **not**
`OPENAI_API_KEY` billing.

All commands go through the helper:

```
~/.claude/skills/gpt-image/scripts/oc-image.sh <generate|edit|describe|batch|check> [args]
```

The helper auto-injects sensible defaults (`--model openai/gpt-image-2`, `--json`,
and an `--output` path), retries once on transient failures, and prints clean results.

## Workflow (follow this every time)

1. **Preflight once per session:** run `oc-image.sh check`. If it warns "not
   authenticated", tell the user to run (themselves, interactively):
   `openclaw models auth login --provider openai` and stop until done.
2. **Write a strong prompt** (see Prompt tips). Prefer **English** text inside the
   image — label rendering is much more accurate in English.
3. **Generate / edit** with the helper. Choose an explicit `--output` path the user
   will want (e.g. `./architecture.png`); otherwise it defaults to
   `./oc-image-<timestamp>.png`.
4. **Always `Read` the produced PNG** to view it, verify the text/layout came out
   right, then report the saved path to the user.
5. If labels are garbled or the layout is off, **iterate**: tighten the prompt (fewer
   words per box, explicit positions) and regenerate, or `edit` the existing file.

## Commands

Generate (text → image):
```bash
~/.claude/skills/gpt-image/scripts/oc-image.sh generate \
  --prompt "PROMPT TEXT" \
  --output ./out.png \
  --size 1536x1024 \
  --output-format png        # png | jpeg | webp
# optional: --background transparent   --count 2   --aspect-ratio 16:9
```
With `--count N` (N>1) openclaw writes suffixed files `out-1.png`, `out-2.png`, … and
prints one `IMAGE` line per file.

Edit (image(s) + prompt → image). Repeat `--file` for multiple inputs:
```bash
~/.claude/skills/gpt-image/scripts/oc-image.sh edit \
  --file ./in.png --prompt "make the background transparent, keep the logo" \
  --output ./edited.png
```

Describe (image → text). Uses a vision model, not gpt-image-2:
```bash
~/.claude/skills/gpt-image/scripts/oc-image.sh describe --file ./in.png \
  --prompt "Describe this in one sentence."
```

Batch (many prompts → many images). Prompts come from a file (one per line; blank
lines and `#` comments skipped) and/or repeated `--prompt`. Runs sequentially,
continues on error, and writes `manifest.tsv` in the output dir:
```bash
# from a file
~/.claude/skills/gpt-image/scripts/oc-image.sh batch \
  --prompts-file ./prompts.txt --outdir ./renders \
  --size 1536x1024 --output-format png      # passthrough applies to every image

# inline prompts
~/.claude/skills/gpt-image/scripts/oc-image.sh batch \
  --prompt "a red circle icon" --prompt "a green triangle icon" --outdir ./icons

# prompts from stdin
printf 'icon one\nicon two\n' | ~/.claude/skills/gpt-image/scripts/oc-image.sh batch --prompts-file -
```
Name an output file by prefixing a line with `stem<TAB>prompt` (otherwise files are
`001.png`, `002.png`, …). Default `--outdir` is `./oc-batch-<timestamp>/`. Passthrough
flags (applied to every image): `--size --output-format --background --aspect-ratio
--resolution --model --timeout-ms`. Batch is one image per prompt — `--count` is
ignored here (use `generate` for multiples).

On success `generate`/`edit`/`batch` print one line per image:
`IMAGE\t<path>\t<WxH>` — Read each `<path>`. `describe` prints the description text.
After a `batch`, read `<outdir>/manifest.tsv` for the stem→status→path→prompt map.

## Prompt tips (what makes gpt-image-2 produce good results)

- **English labels only** inside the image; correct spelling is far more reliable.
- For **diagrams / architecture figures**: state the layout explicitly — e.g. "three
  stacked horizontal layers", "circular clockwise loop of 6 stages", "left-to-right
  pipeline of N boxes connected by arrows". Name **each box's exact label** and the
  **arrow directions/labels**. Add "crisp, correctly-spelled, readable sans-serif
  labels, flat vector, white background, no clutter".
- Keep per-box text short (2–5 words). Long sentences inside boxes get garbled.
- Specify palette and style ("blue/teal/orange flat enterprise infographic", or
  "dark navy blueprint with glowing cyan lines") for consistent results.
- The provider auto-expands the prompt (`revisedPrompt`, echoed to stderr) — useful to
  see how it interpreted the request when iterating.

## Options & sizes

- Sizes (OpenAI provider): `1024x1024`, `1536x1024`, `1024x1536`, `2048x2048`,
  `2048x1152`, `3840x2160`, `2160x3840`. Use landscape `1536x1024` for most diagrams.
- Output formats: `png` (default), `jpeg`, `webp`. Backgrounds: `transparent`,
  `opaque`, `auto` (transparent only with png/webp).
- Image models available: `gpt-image-2` (default), `gpt-image-1.5`, `gpt-image-1`,
  `gpt-image-1-mini`. Override via `--model openai/<id>` or env `OC_IMAGE_MODEL`.

## Known limitations

- **Exact pixel size is NOT honored under the Codex OAuth backend** — `--size` acts as
  an aspect/scale hint and the returned image often has different dimensions (e.g.
  asking 2048×2048 may return ~1254×1254). For exact dimensions, use API-key access
  instead: `export OPENAI_API_KEY=...` (then the request routes through the OpenAI
  Images API). The subscription path is fine for everyday use.
- Very dense diagrams (many tiny labels) may still produce a few misspelled or
  squeezed labels — split into fewer boxes or iterate.
- Cost: image generation draws on the ChatGPT/Codex subscription quota
  (check with `openclaw models status`); a handful of images is a tiny fraction of the
  5-hour window. No per-image API charge while on OAuth.

## Troubleshooting

- `not authenticated` → `openclaw models auth login --provider openai`.
- `Unknown model: openai/gpt-image-2` on **describe** → that's a vision task; the
  helper already uses `openai/gpt-5.5` for describe (override with `OC_VISION_MODEL`).
- `openclaw: command not found` → `npm install -g openclaw@latest` (the helper also
  tries to add the npm global bin to PATH automatically).
