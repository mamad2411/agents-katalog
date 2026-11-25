---
name: minimalist-ui
description: "Editorial, document-style minimal look (Notion/Linear feel): warm monochrome, serif display, flat bento grids. Use only when the user asks for this editorial look, not for every UI task."
---

# Minimalist UI

Goal: a calm, document-like interface where typography and whitespace do the work. Warm monochrome base, color used only for meaning, flat surfaces separated by hairline borders.

## Defaults and why

- **Type:** pick faces with character rather than Inter, Roboto, or Open Sans, which read as unstyled defaults. Sans for UI and body (`'Geist Sans', 'SF Pro Display', 'Helvetica Neue', 'Switzer'`), an editorial serif for hero headings and quotes (`'Newsreader', 'Instrument Serif', 'Lyon Text', 'Playfair Display'`) with `letter-spacing: -0.02em` to `-0.04em` and `line-height: 1.1`, mono for code, keys, and metadata (`'Geist Mono', 'SF Mono', 'JetBrains Mono'`).
- **Text color:** off-black `#111111` or `#2F3437`, not `#000`; body `line-height: 1.6`; secondary text `#787774`.
- **Shadows:** none, or ultra-diffuse under 0.05 opacity. Tailwind's `shadow-md` and up break the flat look.
- **Color:** no large saturated sections, gradients, neon, or heavy glass (a subtle navbar blur is fine). Color is scarce and semantic.
- **Shape:** crisp radius on containers and primary buttons; pills only for small tags.
- **Icons:** slightly heavier stroke (Phosphor Bold/Fill, Radix Icons) suits this look better than thin-line sets like Lucide or Feather. Keep stroke width consistent.
- **Content:** realistic names and copy, no Lorem Ipsum or "Acme". No emojis.

## Palette

- Canvas `#FFFFFF`, or warm off-white `#F7F6F3` / `#FBFBFA`. Cards `#FFFFFF` or `#F9F9F8`.
- Borders and dividers `#EAEAEA` or `rgba(0,0,0,0.06)`.
- Pastel accents for tags, inline code, and icon backgrounds only (background / text):
  - Red `#FDEBEC` / `#9F2F2D`
  - Blue `#E1F3FE` / `#1F6C9F`
  - Green `#EDF3EC` / `#346538`
  - Yellow `#FBF3DB` / `#956400`

## Components

- **Bento grid:** asymmetric CSS Grid, cards with `1px solid #EAEAEA`, radius 8 to 12px, padding 24 to 40px.
- **Primary button:** `#111` background, white text, radius 4 to 6px, no shadow. Hover to `#333`, or `scale(0.98)` on active.
- **Tags:** pill, `text-xs`, uppercase, `letter-spacing: 0.05em`, pastel background.
- **FAQ accordion:** no boxes; items separated by a bottom border; plain `+` / `-` toggle.
- **Keyboard shortcuts:** `<kbd>` with `1px solid #EAEAEA`, radius 4px, `#F7F6F3` background, mono font.
- **Software mockups:** minimal window frame with a white top bar and three small light gray dots.

## Layout

Generous vertical space between sections (`py-24` to `py-32`) and a content width around `max-w-4xl` / `max-w-5xl`. Sections can get quiet depth from a low-opacity image, a faint warm radial light (about 0.03 opacity), or fine line patterns instead of sitting empty.

## Imagery

Desaturated, warm-toned photos (a faint grain overlay around 0.04 opacity helps them blend). Illustrations as monochrome continuous-line sketches with one offset pastel shape. `https://picsum.photos/seed/{context}/1200/800` as a placeholder when no assets exist.

## Motion

Quiet and optional. Content can fade in with `translateY(12px)` and opacity over 600ms, `cubic-bezier(0.16, 1, 0.3, 1)`, via `IntersectionObserver` (not scroll listeners), with an 80ms stagger for lists. Card hover can shift to `0 2px 8px rgba(0,0,0,0.04)` over 200ms. Any ambient background drift stays very slow (20s+), very faint (0.02 to 0.04), on a fixed `pointer-events: none` layer. Animate only `transform` and `opacity`.
