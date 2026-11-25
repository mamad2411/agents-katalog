---
name: chrome-store-promo-screenshot
description: >-
  Compose Chrome Web Store promo screenshots at 1280×800 from real UI captures:
  gradient backdrop, brand + title/subtitle, macOS browser chrome, optional
  two-step overlay. Use when the user asks for Chrome store screenshots,
  商店截图, 商店宣传图, 1280x800 promo images, or store listing visuals from
  raw captures.
---

# Chrome Store Promo Screenshot

Generate polished **1280 × 800 PNG** listing screenshots from real product UI captures. Do not invent fake UI; compose around the user’s real screenshots.

Human-readable Chinese notes: [SKILL.zh.md](SKILL.zh.md) · [themes.zh.md](themes.zh.md) · [README.zh.md](README.zh.md)

## When to use

- Chrome Web Store / Edge Add-ons listing screenshots
- User provides raw captures and wants titles, browser frame, brand styling
- Two-step flows (e.g. toolbar button → result popup) in one image

## Inputs to confirm

Before rendering, confirm if missing:

1. **Source image(s)** path(s)
2. **Brand name** (e.g. `Your App`)
3. **Main title** (required)
4. **Subtitle** (optional)
5. **Layout mode**: `full` | `two-step` | `replace-overlay`
6. **Theme** (default `teal-blue`) — see [themes.md](themes.md)
7. **Output path** (default beside sources, e.g. `*-store-1280x800.png` or `*-商店图-1280x800.png`)

If main title is empty, ask before rendering.

## Visual template (non-negotiable)

| Element | Spec |
|---------|------|
| Canvas | 1280 × 800 PNG |
| Backdrop | Theme gradient + soft translucent circles |
| Top-left | Brand (~22pt semibold) → main title (~49pt bold) → subtitle (~20–21pt medium, optional) |
| Title color | White (themes must stay dark enough for contrast) |
| Window | Rounded white card + shadow; dark chrome bar; traffic lights; fake address pill |
| Content | Real screenshot inside chrome; do not edit/redraw UI pixels |

Keep one theme across a listing set (4–5 shots).

## Layout modes

### `full` — preferred default

- Fit full source width into content area (~1100px wide)
- Scale down only; never enlarge small text
- Crop only empty margins if needed

### `two-step`

- Base: full (or lightly cropped) scene showing step 1
- Overlay: second image (popup-only preferred) as floating card on the right
- Optional step badges: `① …` / `② …`
- Prefer a **popup-only** crop for step 2 so definitions stay readable

### `replace-overlay`

- Reuse an existing composed shot; only replace the overlay popup region
- Keep badges/titles unless user asks to change copy

## Sharpness rules

1. Prefer high-res sources; downscale into the frame
2. Do not default to “zoom the popup until it fills half the canvas” unless user asks
3. **Always render at 2× (2560×1600) then high-quality downsample to 1280×800** (see `scripts/render_store_shot.swift`)
4. If UI screenshot text looks soft: ask for a tighter capture or popup-only PNG
5. On Retina Macs, Preview “Actual Size” often upscales a 1280px image ~2× — soft titles at 100% can be display scaling. Check near ~50% for nearer 1:1 screen pixels

## Implementation (macOS)

1. Read [themes.md](themes.md) for gradient hex values
2. Use AppKit Swift offscreen compose ([scripts/render_store_shot.swift](scripts/render_store_shot.swift)) — keep **2× master → 1× export**
3. Adapt the script for the chosen mode; write a temp script next to assets if needed
4. Run: `swift path/to/script.swift`
5. Verify: `sips -g pixelWidth -g pixelHeight output.png` → 1280×800
6. Delete temporary scripts after success
7. Report output path to the user

If not on macOS, use an equivalent local pipeline (Pillow/cairo/etc.) that matches the same visual template; do not ship AI-generated fake UI as the product screenshot.

## Naming

- Sources: user-provided paths (e.g. `store-screenshots/`)
- Outputs: `{feature}-store-1280x800.png` or `{feature}-商店图-1280x800.png`

## Out of scope

- Chrome store privacy questionnaire / permission justifications
- Writing listing long-description (unless user also asks)
- Taking screenshots inside the user’s browser for them
