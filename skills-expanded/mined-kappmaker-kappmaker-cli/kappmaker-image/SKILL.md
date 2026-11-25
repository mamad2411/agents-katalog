---
name: kappmaker-image
description: Generate any other AI image for a KAppMaker app — illustrations, empty-state and error art, onboarding graphics, backgrounds, one-off artwork from a prompt. Use when the user asks for an image, illustration or artwork that is not the logo (kappmaker-logo) and not store screenshots (kappmaker-screenshots).
---

# KAppMaker — Image

## Before running any command

1. **Prerequisites** — `kappmaker --version` (install: `npm i -g kappmaker`). If a credential is
   missing the CLI says so; re-run `kappmaker config init`.
2. **Read `AiGuidelines/` first** — the PRD, positioning and UI spec already answer most questions.


### generate-image — Generic AI Image Generator

**Syntax**: `kappmaker generate-image --spec <spec.json> [options]` (preferred) or
`kappmaker generate-image --prompt <text> [options]` (quick one-liners only)

**Default to a JSON spec, not a prose prompt.** Structured JSON steers nano-banana-2 noticeably
better than free text: it pins down composition, palette, lighting and hard constraints separately
instead of hoping the model untangles them from a sentence — the result is far more accurate and
repeatable. Reserve bare `--prompt` for genuinely trivial requests ("a red heart icon"); for
anything with brand, layout or mood requirements, author a spec:

1. `kappmaker spec-template image --output Assets/image-spec.json` — canonical skeleton; its
   `_instructions` key explains each field and is auto-stripped before generation.
2. Fill it from `AiGuidelines/` and the user's request: `subject`, `purpose`, `composition`
   (mention intended aspect ratio framing), `style`, `color_palette` (2–4 values, use brand colors),
   `lighting`, `mood`, `background`, `constraints` (hard rules — e.g. "no text", "transparent-look
   background", "leave top third empty for overlay"). Delete fields that don't apply. The skeleton
   is a baseline — restructure or enrich it freely when that captures the request better.
3. Run `kappmaker generate-image --spec Assets/image-spec.json [--aspect-ratio ...] [--output ...]`.
4. Iterating on feedback = edit one or two spec fields and re-run — much more controllable than
   rewriting a prose prompt.

If the user hands you a predefined spec JSON, pass it through as-is.

**Options**:
- `--spec <path>` — Pre-authored JSON spec used verbatim as the structured prompt (preferred, see above)
- `--prompt <text>` — Free-text description (required unless `--spec`; quick one-liners only)
- `--output <path>` — Output file or directory (default: `Assets/generated.png`)
- `--num-images <n>` — Number of images, 1–8 (default: 1)
- `--aspect-ratio <ratio>` — `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `21:9`, `9:21`, `auto` (default: `1:1`)
- `--resolution <res>` — `1K`, `2K`, `4K` (default: `2K`)
- `--output-format <fmt>` — `png`, `jpg`, `webp` (default: `png`)
- `--reference <paths...>` — Reference inputs; switches to fal.ai's `nano-banana-2/edit` endpoint. Each entry can be a file path, a directory (all `.png`/`.jpg`/`.jpeg`/`.webp` inside are auto-picked, sorted, non-recursive), or an HTTP(S) URL. Capped at 10 references total.

**Prerequisites**: `falApiKey` (prompted on first use if not set). `imgbbApiKey` is optional but recommended when using `--reference` with local files — if set, refs are uploaded to imgbb for reliable URLs; if not, they are sent inline as data URIs.

**What it does**: Thin wrapper around fal.ai's `nano-banana-2` (text-to-image) or `nano-banana-2/edit` (if any reference images are supplied). Submits the request, polls until complete, and downloads the result(s).

**Output path rules**:
- No `--output` → defaults to `Assets/generated.png` (or `generated_1.png`, `_2.png`… for multi)
- `--output` without a file extension → treated as a directory
- `--output` with a file extension → used verbatim for single image; for multi, `_1`, `_2`, … are appended before the extension

**When to use this vs `create-logo`**: Use `create-logo` when the user specifically wants an app logo (grid selection, background removal flow). Use `generate-image` for one-off marketing images, hero shots, backgrounds, illustrations, mockups, or any other general-purpose image task.

---

## Where this sits in the flow

- **Before this:** —
- **After this:** **kappmaker-image-tools** if the result needs cropping, background removal or WebP.
