---
name: eu-ai-label
description: Add the official EU AI-content labels (EU icons for labelling AI-generated content, AI Act Art. 50) to images and videos. Use when the user asks to label, watermark, mark, or badge media as AI-generated, AI-modified, or a deepfake, mentions the EU AI icons / AI Act transparency disclosure, or asks to put an "AI" label/badge in a corner of a photo, screenshot, GIF or video.
license: The EU icons are published by the European Commission for free use without attribution. This skill's code is MIT.
compatibility: Requires ffmpeg and ffprobe on PATH (brew install ffmpeg / apt install ffmpeg) and Python 3.9+.
---

# EU AI content labels

Burns the **official European Commission icons** for labelling AI-generated content into
images and videos. Source: <https://digital-strategy.ec.europa.eu/en/policies/eu-icons-labelling-ai-generated-content>
(icons bundled in `assets/`, PNG + SVG, all four colour variations).

## Quick start

```bash
python3 scripts/ai-label.py <file...>          # basic "AI" icon, bottom-right, auto colour
```

Writes `<name>-ai-label.<ext>` next to the input and prints the recommended alt text.
Always use the absolute skill path when calling from another directory, e.g.
`python3 ~/.pi/agent/skills/eu-ai-label/scripts/ai-label.py clip.mp4`.

## Pick the right variant

| `--variant` | Icon | When to use |
|---|---|---|
| `ai` (default) | "AI" badge | AI was involved in creating a deep fake or published text, or you add your own text label / second layer (e.g. "voices generated with" + icon) |
| `generated` | "AI GENERATED" | The whole thing is AI-generated, no human-created elements or editorial control beyond prompting |
| `modified` | "AI MODIFIED" | Pre-existing human-made content partially altered with AI (face swap, AI-furnished room, …) |

Ask the user which case applies if it is not obvious; when unsure default to `ai`.

## Common usage

```bash
# fully AI-generated video, white icon, bottom-left, slightly bigger
python3 scripts/ai-label.py clip.mp4 -v generated -c white -p bottom-left --height 10

# partially modified photo
python3 scripts/ai-label.py photo.jpg -v modified

# batch into a folder (note: use --suffix=-xyz for values starting with a dash)
python3 scripts/ai-label.py shots/*.png --outdir labelled/ -v generated

# label only the first 5 seconds (still must be visible at first exposure)
python3 scripts/ai-label.py clip.mp4 --enable 'between(t,0,5)'

# busy background: add a backing plate
python3 scripts/ai-label.py clip.mp4 --padding 10 --padding-color 'white@0.85'

# just get the raw asset path / alt text for use elsewhere (web, editor, Figma)
python3 scripts/ai-label.py --print-asset generated --color black
python3 scripts/ai-label.py --print-alt modified
python3 scripts/ai-label.py --list
```

## Options that matter

- `-c/--color auto|black|white` — `auto` samples the target corner and picks the contrasting icon.
- `--half` — the 50 %-transparency icon variants (only when the full-opacity one is too dominant).
- `-p/--position` — `bottom-right` (default), `bottom-left`, `top-right`, `top-left`, `bottom-center`, `top-center`; `br/bl/tr/tl/bc/tc` aliases work.
- Size: `--height` (% of frame height, default 8) or `--width` (% of frame width), or absolute `--height-px` / `--width-px`. Guards: `--min-px` (24), `--max-width` (40 %).
- `--margin` % of the shorter side (default 2.5) or `--margin-px`.
- Video encode: `--crf 18`, `--preset medium`, `--vcodec libx264`; audio is stream-copied. Add anything else with `--ffmpeg-arg`.
- `-n/--dry-run` prints the ffmpeg command, `-f/--force` overwrites, `--no-metadata` skips the disclosure comment tag.

Behaviour notes: images keep their format (JPEG q2, PNG flattened unless `--keep-alpha`),
GIFs are re-encoded with a generated palette, audio-only inputs are skipped with a hint
(the EU icons are visual — disclose audio in the player UI, description or an accompanying label).

**Metadata is video-only.** The disclosure comment tag is written for video containers (MP4/MOV/…),
but ffmpeg's still-image muxers discard it, so PNG/JPEG/WebP/TIFF/GIF outputs carry no tag — the
script says so instead of pretending otherwise. This is cosmetic for compliance: Art. 50 wants a
visible mark, and the label is burned into the pixels either way. To add a tag anyway:
`exiftool -Comment='…' out.png`.

## Placement rules to respect

Follow these unless the user explicitly overrides them:

1. Visible **at first exposure** — first frame / above the fold, not only at the end.
2. Put it where no UI overlay covers it (avoid platform-specific hot corners such as the
   TikTok/Reels right rail or a YouTube progress bar area — prefer `top-left` or `bottom-left` there).
3. **Burn it into the pixels** so it survives resharing and downloading; metadata alone is not enough.
4. Clearly visible size — don't shrink below ~5 % of frame height; the default 8 % is a good floor.
5. Give the recommended alt text / ARIA label to any surface that publishes the file
   (the script prints it; also available via `--print-alt`).
6. If the disclosure is time-limited, keep it on screen long enough to read.

Full rules and scope: [references/eu-rules.md](references/eu-rules.md).

## Important caveats

- Using the icon **does not by itself establish legal compliance**. Deployers stay responsible
  under Article 50 AI Act; signatories of the Code of Practice must follow its placement specs.
- Not everything needs a label: the duty covers deep fakes (image/audio/video resembling real
  persons/places/events) and AI-generated text on matters of public interest published without
  human editorial review. Artistic/satirical/fictional works get limited disclosure that must not
  hamper enjoyment of the work; law-enforcement-authorised uses are exempt.
- The icon is a visual disclosure, not provenance. For machine-readable provenance use C2PA /
  Content Credentials in addition.
