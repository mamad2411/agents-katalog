---

name: gpt-image-2
description: gpt-image-2 lets the user generate original images or edit existing ones using AI, which is useful for marketing graphics, concept visuals, branded content, ad creatives, mockups, thumbnails, and stylized scene creation when they need a fast way to turn an idea, prompt, or reference image into a finished visual asset.
category: creative

---
**Use this skill for every image-generation request unless Charles names a different model.**

## What This Skill Does

This skill gpt-image-2 lets the user generate original images or edit existing ones using AI, which is useful for marketing graphics, concept visuals, branded content, ad creatives, mockups, thumbnails, and stylized scene creation when they need a fast way to turn an idea, prompt, or reference image into a finished visual asset.

## Why this skill exists

Hermes's built-in `image_generate` tool routes through FAL's gateway, including the `fal-ai/gpt-image-2` proxy. That path is currently unusable because **FAL's balance is exhausted** — every call returns HTTP 403 "User is locked. Reason: Exhausted balance."

This skill bypasses FAL and calls OpenAI's Images API directly with `OPENAI_API_KEY`. It uses the same `gpt-image-2` model Charles wants ("Image 2", the OpenAI model), with no shared-billing middleman. A Gemini Flash 3.1 fallback runs automatically if OpenAI itself fails (network, quota, etc.).

## How to use it

### One-shot run

```bash
uv run /root/.hermes/skills/gpt-image-2/scripts/generate_image.py \
  --prompt "a high-contrast YouTube thumbnail: white-on-red headline 'BALTIMORE WHOLESALING 101', Charles Blair headshot left, MAD Scientist branding" \
  --filename /tmp/baltimore-thumb.png \
  --size 1536x1024 \
  --quality high
```

The script prints `provider=openai` or `provider=gemini` on the last line so you know which model produced the image. After it succeeds, deliver the file to Charles immediately:

```bash
hermes-send-file "/tmp/baltimore-thumb.png" "Baltimore Wholesaling 101 thumbnail"
```

### Args

| Flag | Default | Notes |
|---|---|---|
| `--prompt` / `-p` | required | The image description. Be specific about composition, text, style, brand. |
| `--filename` / `-f` | required | Output path. Always `.png`. Use `/tmp/` for ephemeral, `/root/.hermes/cache/images/` for keep. |
| `--size` / `-s` | `1024x1024` | One of `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait), `auto`. OpenAI-only — Gemini ignores. |
| `--quality` / `-q` | `high` | `low` / `medium` / `high` / `auto`. Higher quality = more cost; medium is plenty for most reels/thumbnails. |

### Sizes by use case

- **YouTube thumbnail (16:9)**: `--size 1536x1024`
- **Instagram post (1:1)**: `--size 1024x1024`
- **Instagram story / TikTok cover (9:16)**: `--size 1024x1536`

## Banned alternatives — do not use these

- ❌ `image_generate` tool (built-in) — FAL-based, **out of credit**.
- ❌ `nano-banana-image-gen` skill — old Gemini default, Charles moved off this.
- ❌ OpenRouter image models — Charles does not use OpenRouter for images.
- ❌ Any other generic Fal endpoint (`fal-ai/flux-*`, `fal-ai/recraft-*`, etc.) — same FAL billing wall.

## When to use `gemini-image-editor` instead

Only when Charles asks for an *edit* of an existing image (background swap, object remove, text overlay) — `gpt-image-2` via this skill is generation-only. For edits, load `gemini-image-editor`.

## Failure modes

- `OPENAI_API_KEY not set` — env var missing. Check `/root/.hermes/.env` line `OPENAI_API_KEY=…`.
- OpenAI returns 4xx — check the error; usually rate limit, content-policy block, or expired key. Fallback to Gemini runs automatically; if Gemini also fails, both errors are printed and exit code is 1.
- Both providers fail — relay the actual errors to Charles. Do **not** invent failure modes ("Fal is out of credit" — wrong path entirely).

## Skill state

This skill is **pinned** in the Hermes curator (`hermes curator pin gpt-image-2`). It will not be auto-archived.
