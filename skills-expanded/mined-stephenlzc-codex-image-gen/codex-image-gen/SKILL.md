---
name: codex-image-gen
description: 'Generate raster images with the locally installed, OAuth-authenticated Codex CLI — no API key required. Trigger words: "generate/create/draw an image", photo, illustration, poster, avatar, logo, UI mockup, infographic, sprite, and Chinese equivalents (生图, 画一张, 生成图片, 海报, 头像, 插画). Do NOT use for editing existing SVG/vector/code-native assets, or when the user explicitly wants the OpenAI API with their own key. Requires `codex` in PATH and `~/.codex/auth.json`.'
---

# Codex Image Gen

## Overview

Routes image generation through the user's local OAuth-authenticated Codex
CLI (`codex exec`, non-interactive) instead of any cloud API. The bundled
script `scripts/codex_generate_image.sh` performs the full pipeline
(dispatch, locate, resize, verify, archive prompt). Do NOT hand-craft
`codex exec` calls unless the script cannot be used.

## Hard rules

- Never report success to the user before every item in the verification
  checklist has passed.
- Never ask the user for an OpenAI API key; this skill is OAuth-only. If auth
  is missing or expired, direct the user to run `codex login`.
- Never hand-edit the produced PNG; if the user wants changes, regenerate with
  a refined prompt.
- Never state or imply image dimensions without verifying them (the script
  verifies via `sips`/ImageMagick).

## When not to use this skill

Routing triggers live in the frontmatter `description`. Skip only when:
editing existing SVG/vector/code-native assets; the user explicitly wants
the OpenAI API or a non-Codex provider; Codex CLI/OAuth login is missing;
or the task is better served by writing HTML/CSS/canvas directly.

## Quick Start

Use the bundled script (path is relative to the skill's install directory).
It prints the final image path on stdout and exits 0 on success.

```bash
scripts/codex_generate_image.sh \
  --prompt  "a sandy beach with a tropical island in the distance and many people enjoying the shore" \
  --output  /tmp/beach.png \
  --size    1024x1024 \
  --style   photorealistic-natural
```

Exit codes: `0` = success · `1` = no codex/OAuth · `2` = no image produced ·
`3` = size mismatch after resize · `4` = bad arguments.

## Output convention

Write images to an `assets/` folder inside the user's workspace, named
`<task-slug>-<YYYYMMDD-HHMMSS>.png` (slug derived from the request). The
script saves the full prompt as a sibling `.md` with the same basename
(disable with `--no-archive`), so every image is reproducible.

## Workflow

1. Decide the output path per the convention above: pass
   `assets/<task-slug>-<YYYYMMDD-HHMMSS>.png` via `--output`, preferring the
   workspace `assets/` over `/tmp` so the artifact persists (the script
   `mkdir -p`s parents).
2. Draft a specific, self-contained prompt. Include the subject, scene,
   composition, style, and any constraints. Translate Chinese prompts to
   English when targeting photorealistic styles unless the user specifies a
   language requirement.
3. Confirm before generating — but only when it matters. Text edits are
   free; each generation is a real Codex call. If the request is vague or a
   high-impact field is undecided (subject, style slug, text in the image,
   size/purpose), show the draft and ask option-based questions via the
   host's structured user-input tool (AskUserQuestion-style) or numbered
   plain text, always offering "generate as drafted". If the prompt is
   already specific, skip confirmation. Full protocol: `references/prompting.md`.
4. Choose a target size. Default is `1024x1024`. Codex's built-in `image_gen`
   does not guarantee exact pixel dimensions, so the script enforces them
   after the fact via `sips` (macOS) with an ImageMagick fallback elsewhere.
5. Optionally pass `--style` using one of Codex's supported use-case slugs
   (see `references/prompting.md`). If omitted, Codex picks a sensible default.
6. Invoke the script with the arguments above. Capture the path it prints on
   stdout. Note that the archived `.md` prompt file lands next to the image
   (same basename).
7. Verify the file exists at the returned path and present the image to the
   user using whatever display mechanism the host provides.
8. If the user requested edits or variants, run the script again with a refined
   prompt; do not edit the PNG by hand.

## Common pitfalls

- **"image_generation feature not enabled"** — the script passes
  `--enable image_generation` per call; if your Codex version rejects the
  flag, enable `image_generation` in `~/.codex/config.toml` instead.
- **OAuth expired** — re-run `codex login` (NOT `codex login --api-key`).
  Do NOT ask the user for an API key.
- **Wrong dimensions** — Codex may produce a non-matching size; the script
  resizes via `sips` (ImageMagick fallback). Expected behavior. If neither
  tool exists, it warns and keeps the native size.
- **Sandbox permissions** — broad permissions are scoped per invocation
  (`--sandbox danger-full-access` + `-c approval_policy="never"`); no global
  config change needed. Pass `--sandbox workspace-write` to tighten,
  accepting that generation may fail.

## Verification checklist

Confirm all of the following before reporting success to the user:

- [ ] Exit code is `0`
- [ ] File exists at the path printed on stdout
- [ ] File is a PNG (`file <path>` reports `PNG image data`)
- [ ] Pixel dimensions match `--size` (`sips -g pixelWidth -g pixelHeight`,
      or ImageMagick's `identify` where `sips` is unavailable)
- [ ] Visual content matches the prompt (read the image and confirm)