---
name: appshots-background-effects
description: >
  Background styling for App Screenshots: solid colors, gradients,
  mesh gradients, doodle patterns, and transparent backgrounds.
  Includes color psychology and 2025 design trend guidance.
---

# App Screenshots Background Effects

Style screenshot backgrounds with solid colors, gradients, mesh gradients, doodle patterns, or transparency.

## Color Psychology for App Store

Background color significantly impacts conversion rates. Research-backed guidance:

| Style | Hex Examples | Effect | Best For |
|-------|-------------|--------|----------|
| **Dark/black** | `#0A0A1A`, `#0D1117`, `#111827` | Premium, modern, high contrast | Most apps (top trend 2025) |
| **Deep blue** | `#0F172A`, `#1E293B`, `#1A1A2E` | Trust, professional | Finance, productivity |
| **Vibrant** | `#7C3AED`, `#EC4899`, `#F59E0B` | Energy, playful | Social, games, creative |
| **White/light** | `#FFFFFF`, `#F8FAFC`, `#F1F5F9` | Clean, minimal | Business, health |
| **Warm** | `#7C2D12`, `#92400E`, `#78350F` | Cozy, organic | Food, lifestyle |

> **Tip:** Dark backgrounds are the dominant trend in 2025 — they make white text pop and feel premium. Most top-ranking apps use dark backgrounds.

## Solid Color

```bash
# Premium dark (most popular)
appshots editor set-background --color "#0A0A1A"

# Deep blue
appshots editor set-background --color "#0F172A"

# Vibrant purple
appshots editor set-background --color "#7C3AED"
```

## Gradients (Linear / Radial / Sweep)

Gradients add depth and visual sophistication:

```bash
# Linear gradient (most common)
appshots editor set-gradient --json '{
  "type": "linear",
  "colors": ["#1A1A2E", "#16213E"],
  "stops": [0.0, 1.0],
  "begin": {"x": 0, "y": 0},
  "end": {"x": 1, "y": 1}
}'

# Radial gradient (spotlight effect)
appshots editor set-gradient --json '{
  "type": "radial",
  "colors": ["#3B0764", "#1E1B4B"],
  "stops": [0.0, 1.0],
  "center": {"x": 0.5, "y": 0.3},
  "radius": 0.8
}'

# Sweep/angular gradient
appshots editor set-gradient --json '{
  "type": "sweep",
  "colors": ["#FF0000", "#00FF00", "#0000FF", "#FF0000"],
  "stops": [0.0, 0.33, 0.66, 1.0]
}'

# Remove gradient
appshots editor set-gradient --clear
```

### Popular Gradient Combinations

| Name | Colors | Vibe |
|------|--------|------|
| **Midnight** | `#0A0A1A` → `#1A1A3E` | Deep, premium dark |
| **Ocean** | `#0F172A` → `#1E3A5F` | Professional blue |
| **Sunset** | `#7C2D12` → `#DC2626` | Warm, energetic |
| **Aurora** | `#4C1D95` → `#0EA5E9` | Creative, vibrant |
| **Forest** | `#064E3B` → `#059669` | Natural, health |

## Mesh Gradient

Rich multi-point gradients for modern, premium feel (Glassmorphism 2.0 trend):

```bash
# Set mesh gradient
appshots editor set-mesh-gradient --json '{
  "points": [
    {"x": 0.0, "y": 0.0, "color": "#3B0764"},
    {"x": 1.0, "y": 0.0, "color": "#1E40AF"},
    {"x": 0.0, "y": 1.0, "color": "#0E7490"},
    {"x": 1.0, "y": 1.0, "color": "#7C3AED"}
  ]
}'

# Remove mesh gradient
appshots editor set-mesh-gradient --clear
```

## Doodle Pattern

Repeating icon/emoji patterns as background decoration — adds texture without overwhelming the main content:

```bash
# Subtle SF Symbols pattern
appshots editor set-doodle \
  --icon-source 0 \
  --icon-size 40 \
  --spacing 60 \
  --opacity 0.08 \
  --rotation 15 \
  --color "#FFFFFF"

# Material Symbols pattern
appshots editor set-doodle \
  --icon-source 1 \
  --icon-size 50 \
  --spacing 80 \
  --opacity 0.05

# Icon sources:
#   0 = SF Symbols
#   1 = Material Symbols
#   2 = Emoji

# Remove doodle
appshots editor set-doodle --clear
```

> **Best practice:** Keep doodle opacity very low (0.03–0.10) so it adds subtle texture without distracting from the screenshot and text.

## Transparent Background

Useful for compositing in external tools:

```bash
# Enable transparent
appshots editor set-transparent

# Disable transparent
appshots editor set-transparent --no-value
```

## Consistency: Batch Backgrounds

Use the same background style across all 10 screenshots for a cohesive set:

```bash
# Option A: Same color for all (via multi batch)
appshots multi batch --action set-background --color "#0A0A1A"

# Option B: Per-design color series (manual switch + set)
appshots multi switch --index 0
appshots editor set-background --color "#0A0A1A"
appshots multi switch --index 1
appshots editor set-background --color "#0D1117"
# ... create a subtle gradient progression across screenshots
```

## 2025 Design Trends

- **Dark mode dominance** — vast majority of top apps use dark backgrounds
- **Glassmorphism 2.0** — translucent layers with vibrant underlays (mesh gradients)
- **Panoramic/continuous** — backgrounds that flow across screenshots when swiped
- **Bold + minimal** — clean layouts with one strong accent color
- **Depth with shadows** — 3D elements and subtle shadow gradients

## Commands Reference

| Command | Description |
|---------|-------------|
| `set-background --color "#HEX"` | Solid color |
| `set-gradient --json '{...}'` | Linear/radial/sweep gradient |
| `set-gradient --clear` | Remove gradient |
| `set-mesh-gradient --json '{...}'` | Mesh gradient |
| `set-mesh-gradient --clear` | Remove mesh gradient |
| `set-doodle --icon-size N ...` | Doodle pattern |
| `set-doodle --clear` | Remove doodle |
| `set-transparent` | Toggle transparent |
