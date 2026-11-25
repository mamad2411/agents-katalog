---
name: ui-ux-promax
description: "UI/UX Pro Max design system — 50+ styles, 161 color palettes, 57 font pairings. Auto-applies to any website build. Feeds into website-builder Actor 2."
allowed-tools: Read, Bash, Write
---

# UI/UX Pro Max — Design System

## Triggers
"ui ux pro max" / "uipro" / "design system" / "161 palettes" / "57 fonts" / "50 styles" / "design spec" / "color palette" / "font pairing"

## What It Does

Takes business brief → outputs complete design spec JSON:
- Style (from 50+ options: minimal, bold, corporate, playful, luxury, brutalist, glassmorphism...)
- Color palette (from 161 options — auto-matched to brand vibe)
- Font pairing (from 57 options — heading + body)
- Spacing system (4px/8px grid)
- Component variant guidelines

## Setup (one-time)

```bash
npm install -g uipro-cli
uipro init --ai claude
```

## Repos

- `~/installed-repos/ui-ux-design-pro-skill-main/` — design system v1
- `~/installed-repos/ui-ux-pro-max-skill-main/` — Pro Max version
- `~/installed-repos/frontend-design/` — frontend patterns
- `~/installed-repos/ai-design-team/` — design agent refs

## Output Format (Design Spec JSON)

```json
{
  "style": "luxury-minimal",
  "palette": {
    "primary": "#1A1A2E",
    "accent": "#E94560",
    "bg": "#F5F5F0",
    "text": "#2C2C2C"
  },
  "fonts": {
    "heading": "Playfair Display",
    "body": "Inter"
  },
  "spacing": "8px-grid",
  "border_radius": "4px",
  "shadow": "subtle-drop"
}
```

## Integration

- **Actor 2** in `website-builder` pipeline — feeds design spec to Actor 3 (Component Selector)
- Works with `premium-web-design` skill for Stitch + Nano Banana mockups
- Output passed directly to Claude Code for site build
