---
name: appshots-design-workflow
description: >
  End-to-end screenshot design workflows with the App Screenshots CLI.
  Create multi-screenshot sets, apply styling, and export PNGs.
  Includes research-backed layout ratios and design patterns.
---

# App Screenshots Design Workflow

Build complete App Store screenshot sets from scratch using the CLI.

> **Max 10 design slots** per set (matches App Store's 10-screenshot limit per display size).

## Best Practice: Screenshot Order

The first 2–3 screenshots determine 80% of download decisions (users decide in ~7 seconds):

1. **Hero shot** — your app's #1 value proposition
2. **Key differentiator** — what makes you unique
3. **Social proof or depth** — trust indicator or key workflow
4. **Features 4–7** — additional capabilities
5. **Platform extras 8–10** — Watch, iPad, widgets

## Complete Workflow

### 1. Open the Multi-Editor

```bash
appshots multi open --display-type APP_IPHONE_67
```

### 2. Add Design Slots (up to 10)

```bash
# Start with 1 slot. Add more as needed:
appshots multi add    # 2
appshots multi add    # 3
appshots multi add    # 4
appshots multi add    # 5
# ... up to 10 total
```

> **Tip:** Use all 10 slots to maximize App Store real estate.

### 3. Set Screenshot Images

```bash
appshots multi set-image --file screenshot1.png --index 0
appshots multi set-image --file screenshot2.png --index 1
appshots multi set-image --file screenshot3.png --index 2
appshots multi set-image --file screenshot4.png --index 3
appshots multi set-image --file screenshot5.png --index 4
```

### 4. Batch Styling (All Designs at Once)

Apply consistent styling across all designs — consistency is critical for a professional appearance:

```bash
# Padding: 180–220px is the sweet spot
appshots multi batch --action set-padding --value 200

# Corner radius: 30–50px for modern rounded look
appshots multi batch --action set-corner-radius --value 40
```

### 5. Set Backgrounds

Dark backgrounds convert better and make text more readable:

```bash
appshots multi switch --index 0
appshots editor set-background --color "#0A0A1A"

appshots multi switch --index 1
appshots editor set-background --color "#0D1117"

# -- or use gradients for premium feel --
appshots multi switch --index 2
appshots editor set-gradient --json '{"type":"linear","colors":["#1A1A2E","#16213E"]}'
```

### 6. Set Device Frames

Use the latest device model for a modern look:

```bash
appshots editor list-devices

# Apply to each design
appshots multi switch --index 0
appshots editor set-frame --device "iPhone 16 Pro Max"

# Optional: subtle 3D tilt (values in RADIANS, not degrees!)
appshots editor set-rotation --x 0.03 --y -0.02 --z 0.01
```

### 7. Position Screenshots

Push the screenshot down to make room for text above:

```bash
# y = 250–350 depending on text length
appshots editor set-image-position --x 0 --y 280
```

### 8. Add Centered Text (Copy-First!)

**Write copy BEFORE designing.** Bad copy ruins good design. Follow the Iron Rules:
- **3–5 words per line**, max 2 lines
- **Benefits, not features** ("Save 2hrs/week" > "Automatic tracking")
- **One idea per slide** — never join with "and"
- **Arm's length test** — if you can't parse it in 1 second, too complex

Three caption approaches:
| Type | Example |
|------|---------|
| **Paint a moment** | "Check your streak without opening the app" |
| **State an outcome** | "A home for every habit you build" |
| **Kill a pain** | "Never lose your daily streak" |

```bash
appshots multi switch --index 0
appshots editor add-text \
  --text "Track Your Habits" \
  --font "Poppins" --size 90 \
  --color "#FFFFFF" \
  --y 80 --x 0 \
  --width 1290 --align center

appshots multi switch --index 1
appshots editor add-text \
  --text "AI-Powered Insights" \
  --font "Poppins" --size 90 \
  --color "#FFFFFF" \
  --y 80 --x 0 \
  --width 1290 --align center
```

> **Centering formula:** `--x 0 --width <canvas-width> --align center`
> For iPhone 6.7", canvas width = 1290px. For iPhone 6.9" = 1320px.

### 9. Save & Export

```bash
# Save design set to library
appshots multi save-design --name "My App Store Screenshots"

# Export all as PNG (recommended over JPEG for sharp text)
appshots editor export-all --dir ~/Desktop/screenshots
```

## Using Presets

```bash
# List available presets
appshots preset list

# Apply preset to all designs
appshots multi apply-preset --id dark_premium

# Customize individual designs after preset
appshots multi switch --index 0
appshots editor set-background --color "#1A1A2E"
```

## Design Layout Ratios

Based on research, optimal layouts follow these proportions (iPhone 6.7" = 1290×2796):

| Zone | Position | Height | Content |
|------|----------|--------|---------|
| **Text area** | Top 25–30% | y: 0–840 | Headline + subtitle |
| **Device frame** | Center–bottom | y: 280 onward | App screenshot |
| **Safe margin** | All sides | 60–100px | Breathing room |

## Multi-Editor Commands Reference

| Command | Description |
|---------|-------------|
| `multi open --display-type X` | Open multi-editor |
| `multi state` | Get current state |
| `multi switch --index N` | Switch active design |
| `multi add` | Add new slot (max 10) |
| `multi remove --index N` | Remove a design |
| `multi duplicate --index N` | Duplicate a design |
| `multi reorder --from N --to M` | Reorder designs |
| `multi batch --action X --value Y` | Batch operation on all |
| `multi set-image --file F --index N` | Set image for design |
| `multi save-design --name "..."` | Save design set |
| `multi apply-preset --id X` | Apply preset to all |
