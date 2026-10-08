# AVCD Tech UI Design System — Cursor Rules
# Drop this file as `.cursorrules` in the root of your project.
# Cursor's AI will follow these rules when generating any UI component.

## Project Design System

This project uses the AVCD Tech design system: a Bloomberg-inspired editorial aesthetic
built on dark forest green and warm beige. All UI components must follow these rules exactly.

---

## Color Palette (never deviate from these values)

```
--green:     #1B4332   Primary text, headers, borders, section bars
--green-mid: #2D6A4F   Accents, active states, financial highlights
--green-lt:  #52B788   Eyebrows, status dots, tertiary accents
--beige:     #F5F0E8   Page/card background (NOT white)
--beige-2:   #EDE8DF   Hover states, topbars, inset surfaces
--beige-3:   #E0D9CE   Pressed states
--text:      #1B4332   Primary text
--text-2:    #4A6741   Secondary text
--text-3:    #7A8C75   Labels, metadata, muted content
--border:    #C8C0B0   All borders (warm taupe, never cool gray)
```

Rules:
- Background is ALWAYS #F5F0E8, NEVER white or #ffffff
- All borders use #C8C0B0, NEVER use gray, #e5e7eb, or any cool-toned border
- Modal overlays: rgba(27,67,50,0.45) — green-tinted scrim, not black
- NO gradients, NO box-shadows, NO border-radius on layout containers

---

## Typography (always import and use these three fonts)

Google Fonts import (required in every file):
```
https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Roboto+Condensed:wght@400;700&family=Roboto+Mono:wght@400;500&display=swap
```

Font assignment:
- `font-family: 'Libre Baskerville', Georgia, serif` → Display names, headings, card names
- `font-family: 'Roboto Condensed', sans-serif` → ALL labels, buttons, eyebrows, roles, section titles
- `font-family: 'Roboto Mono', monospace` → ALL data values, IDs, emails, salaries, dates, numbers

NEVER use: Inter, Roboto (regular), Arial, system-ui, or any other font.
Font weights: 400 and 700 only.

---

## Label Style (applies to every metadata label in the UI)

```css
font-family: 'Roboto Condensed', sans-serif;
font-size: 9px–11px;
font-weight: 700;
text-transform: uppercase;
letter-spacing: 0.08em–0.14em; /* smaller font = more spacing */
color: #7A8C75; /* --text-3 */
```

---

## Card Pattern

Every data card follows this structure:
1. Eyebrow (ID/category): Roboto Condensed 9px, #52B788, uppercase, letter-spacing 0.14em
2. Name/title: Libre Baskerville 18px bold, #1B4332
3. Subtitle/role: Roboto Condensed 11px, #7A8C75, uppercase
4. 1px #C8C0B0 horizontal rule
5. Field rows: label (Roboto Condensed, #7A8C75) + value (Roboto Mono, #1B4332) space-between
6. Footer: status dot + category, separated by top border

Grid system: border-top + border-left on grid, border-right + border-bottom on each card.
No gap. This creates seamless grid without double borders.

---

## Section Bar Pattern

```html
<div style="display:flex;align-items:center;gap:10px;border-bottom:2px solid #1B4332;padding-bottom:6px;margin-bottom:20px;">
  <span style="font-family:'Roboto Condensed',sans-serif;font-size:10px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;background:#1B4332;color:#F5F0E8;padding:2px 8px;">Live</span>
  <span style="font-family:'Roboto Condensed',sans-serif;font-size:13px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#1B4332;">Section Title</span>
  <span style="font-family:'Roboto Mono',monospace;font-size:10px;color:#7A8C75;margin-left:auto;">N records</span>
</div>
```

---

## Detail Panel / Modal Pattern

- `border-top: 3px solid #1B4332` — signature accent (always present on panels)
- `border: 1px solid #C8C0B0` on all other sides
- Topbar: background #EDE8DF, mono label left, close button right
- Panel body: eyebrow → serif name (28px bold) → condensed role → 2px green rule → field rows
- Field rows: `border-bottom: 1px solid #C8C0B0` between each row
- Overlay: `background: rgba(27,67,50,0.45)`

---

## Hover States

- Cards: `background: #EDE8DF` (--beige-2)
- Buttons/links: `text-decoration: underline`, no background change (for text buttons)
- Filled buttons: darken to `#2D6A4F` (--green-mid)

---

## What NOT to Do

- Do NOT use white (#ffffff) as background
- Do NOT use cool gray borders (#e5e7eb, #d1d5db, etc.)
- Do NOT add box-shadow to cards or panels
- Do NOT add border-radius to cards, panels, or grids
- Do NOT use any font other than the three specified
- Do NOT use purple, blue, orange, or any color outside the palette
- Do NOT use font-weight 500 or 600 on any element
- Do NOT use `rgba(0,0,0,0.5)` for overlays — use the green-tinted scrim

---

## Component Quick Reference

### Status dot
```html
<span style="display:inline-flex;align-items:center;gap:5px;font-family:'Roboto Condensed',sans-serif;font-size:10px;font-weight:700;text-transform:uppercase;color:#2D6A4F;">
  <span style="width:6px;height:6px;border-radius:50%;background:#52B788;"></span>active
</span>
```

### Field row
```html
<div style="display:flex;justify-content:space-between;align-items:baseline;padding:8px 0;border-bottom:1px solid #C8C0B0;">
  <span style="font-family:'Roboto Condensed',sans-serif;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#7A8C75;">Label</span>
  <span style="font-family:'Roboto Mono',monospace;font-size:12px;font-weight:500;color:#1B4332;">Value</span>
</div>
```

### Tag / badge
```html
<!-- Filled -->
<span style="font-family:'Roboto Condensed',sans-serif;font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;background:#1B4332;color:#F5F0E8;padding:2px 8px;">Active</span>

<!-- Outline -->
<span style="font-family:'Roboto Condensed',sans-serif;font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;border:1px solid #C8C0B0;color:#7A8C75;padding:2px 8px;">Inactive</span>
```

### Form input
```html
<input style="width:100%;font-family:'Roboto Mono',monospace;font-size:13px;color:#1B4332;background:#F5F0E8;border:1px solid #C8C0B0;padding:8px 10px;outline:none;" />
```

---

## Currency / Number Formatting

Always format salary and financial values:
```js
const fmt = n => '$' + n.toLocaleString();
// e.g. fmt(118000) → "$118,000"
```

Never display raw numbers like 118000 — always format with toLocaleString().
