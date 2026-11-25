---
name: pptx-creator
description: "Create professional PowerPoint presentations with clean, modern design. Uses a customizable color palette, professional typography, and structured layouts."
---

# PowerPoint Creator Skill

Create professional presentations with clean, modern design following best practices for visual communication.

## When to Use This Skill

Use this skill when creating:
- Team and leadership presentations
- Strategy documents and roadmaps
- Performance reviews and updates
- Training materials
- Product and design reviews

## Color Palette

### Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Primary Blue** | `#2563EB` | 37, 99, 235 | Primary brand color, CTAs, headers |
| **Dark Navy** | `#1E293B` | 30, 41, 59 | Dark backgrounds, text |
| **White** | `#FFFFFF` | 255, 255, 255 | Backgrounds, reversed text |

### Secondary Colors

| Name | Hex | Usage |
|------|-----|-------|
| **Sky Blue** | `#60A5FA` | Hover states, lighter accents |
| **Light Blue** | `#93C5FD` | Backgrounds, highlights |
| **Pale Blue** | `#DBEAFE` | Subtle backgrounds |
| **Coral** | `#F87171` | Alerts, highlights |
| **Emerald** | `#10B981` | Positive indicators |
| **Amber** | `#F59E0B` | Warnings, attention |

### Neutral Grays

| Name | Hex | Usage |
|------|-----|-------|
| **Gray 900** | `#111827` | Primary text |
| **Gray 600** | `#4B5563` | Secondary text |
| **Gray 400** | `#9CA3AF` | Muted text, borders |
| **Gray 200** | `#E5E7EB` | Dividers, light borders |
| **Gray 50** | `#F9FAFB` | Light backgrounds |

## Typography

### Font Family
**Inter** — Clean, modern sans-serif optimized for readability

Fallbacks: `Inter`, `Segoe UI`, `system-ui`, `sans-serif`

### Font Weights

| Weight | Name | Usage |
|--------|------|-------|
| 400 | Regular | Body text, descriptions |
| 600 | Semi-Bold | Subheadings, emphasis |
| 700 | Bold | Headlines, titles |

### Type Scale for Presentations

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Title Slide | 54pt | Bold | Primary Blue or White |
| Section Header | 44pt | Bold | Dark Navy or Primary Blue |
| Slide Title | 36pt | Semi-Bold | Dark Navy |
| Subtitle | 24pt | Regular | Gray 600 |
| Body Text | 18pt | Regular | Gray 900 |
| Caption | 14pt | Regular | Gray 400 |

## Slide Templates

### 1. Title Slide
- **Background:** Primary Blue or White
- **Title:** 54pt Bold, centered
- **Subtitle:** 24pt Regular

### 2. Section Divider
- **Background:** Dark Navy
- **Section title:** 44pt Bold, White, left-aligned
- **Accent bar:** Primary Blue, left edge

### 3. Content Slide
- **Background:** White
- **Title:** 36pt Semi-Bold, Dark Navy, top left
- **Body:** 18pt Regular, Gray 900

### 4. Two Column
- **Split:** 50/50 or 60/40
- **Divider:** 2px Primary Blue line or no divider

### 5. Data/Metrics
- **Numbers:** 72pt Bold, Primary Blue
- **Labels:** 18pt Regular, Gray 600
- **Charts:** Use brand colors in order of priority

## Best Practices

### Do
- ✅ Use Primary Blue as the dominant accent color
- ✅ Maintain generous white space
- ✅ Use bold typography for headlines
- ✅ Keep slide content focused (one idea per slide)
- ✅ Ensure high contrast for accessibility

### Don't
- ❌ Crowd slides with too much text
- ❌ Use decorative fonts
- ❌ Place text over busy backgrounds without overlay
- ❌ Use more than 3-4 colors per slide

## Code Example (pptxgenjs)

```javascript
const pptxgen = require('pptxgenjs');

const colors = {
  primaryBlue: '2563EB',
  darkNavy: '1E293B',
  white: 'FFFFFF',
  skyBlue: '60A5FA',
  lightBlue: '93C5FD',
  paleBlue: 'DBEAFE',
  coral: 'F87171',
  emerald: '10B981',
  amber: 'F59E0B',
  gray900: '111827',
  gray600: '4B5563',
  gray400: '9CA3AF',
  gray50: 'F9FAFB'
};

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
pptx.title = 'Presentation Title';

// Title Slide
let slide = pptx.addSlide();
slide.background = { color: colors.primaryBlue };
slide.addText('Presentation Title', {
  x: 0.5, y: 2.5, w: '90%',
  fontSize: 54, fontFace: 'Inter', bold: true,
  color: colors.white, align: 'center'
});

pptx.writeFile({ fileName: 'presentation.pptx' });
```
