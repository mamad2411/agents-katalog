# Prompt for Claude Design — Wardrobe Whimsy Design System

Copy everything below into Claude Design.

---

Build a **design system reference** for **Wardrobe Whimsy**, a wardrobe management and outfit-collage web app. This is a portfolio product: a user catalogues clothing items, organizes them into outfits, arranges outfits as drag-and-drop visual collages, and logs when outfits are worn. The deliverable is a single-page, living style guide showing every design token and component together — not app screens or user flows.

Base everything on **shadcn/ui** conventions and **Tailwind CSS** with **lucide-react** icons, so the system maps directly onto a real shadcn-based build.

## Design direction

Aim for **"editorial closet"**: the clean, spacious bones of a modern SaaS product (think Linear or Notion — generous whitespace, restrained borders, calm hierarchy) combined with the warmth and tactility of a fashion editorial or physical closet (soft rounded cards with a slight lift/shadow like polaroids or swatches, warm neutral tones instead of cold grays). Avoid heavy glassmorphism, neon, or dark-mode-only aesthetics — this should feel like sunlight through a closet window, not a tech dashboard.

## 1. Foundations

**Color tokens** — present as swatches with token name, HSL, hex, and usage note. Use these as shadcn CSS variables:

| Token | HSL | Hex (approx) | Use |
|---|---|---|---|
| `background` | 30 33% 97% | #FAF6F0 | page background, warm ivory |
| `foreground` | 20 14% 16% | #2B2521 | body text, charcoal ink |
| `card` | 0 0% 100% | #FFFFFF | cards on ivory background |
| `primary` | 15 55% 45% | #C1653A | primary buttons, active nav, key CTAs (terracotta/rust) |
| `primary-foreground` | 30 40% 98% | #FDF9F5 | text on primary |
| `secondary` | 350 40% 88% | #F1D7DA | secondary buttons, soft highlights (dusty rose) |
| `secondary-foreground` | 350 30% 25% | #4A2A2E | text on secondary |
| `accent` | 82 20% 42% | #6F7A4C | tags, categories, success/active states (sage/olive) |
| `muted` | 30 20% 92% | #EDE6DC | subtle backgrounds, dividers |
| `muted-foreground` | 25 10% 45% | #7A716A | secondary text, placeholders |
| `border` | 30 15% 88% | #E4DCD1 | card borders, dividers |
| `destructive` | 5 65% 50% | #D1493A | delete actions, errors |
| `gold` (custom) | 40 70% 55% | #E0A93F | favourite flag, highlights |

Also define a **dark mode** variant of this palette (deepened charcoal background, desaturated terracotta/rose/sage that still read as warm, not a generic cold dark theme).

**Typography** — a type scale (display, h1–h4, body, small, caption) using a warm humanist sans for UI text, with an optional serif display face for headlines/outfit names to reinforce the editorial feel. Show weight, size, and line-height for each step.

**Spacing & sizing** — an 4/8px-based spacing scale, a border-radius scale (shadcn's `sm`/`md`/`lg`/`xl`/`full`, skewed slightly rounder than default shadcn to feel softer), and an elevation/shadow scale (flat, card, raised, floating) styled as soft warm-toned shadows rather than pure black.

**Iconography** — lucide-react, consistent stroke width, sized at 16/20/24px with usage guidance.

## 2. Core components (show all variants and states for each)

- **Buttons** — primary, secondary, outline, ghost, destructive, link; sizes sm/md/lg; default/hover/active/focus-visible/disabled/loading states.
- **Badges/tags** — category tag, status badge (DRAFT / ACTIVE), favourite indicator.
- **Cards** — base card, clothing item card, outfit card — each with default, hover, and selected states.
- **Form fields** — text input, select, textarea, checkbox, with default/focus/error/disabled states and inline validation messaging.
- **Navigation** — sidebar/topbar nav item (default/active/hover), tabs.
- **Overlays** — dialog/modal, dropdown menu, tooltip.
- **Feedback** — toast/alert (success/error/info), skeleton loader, progress bar, empty state pattern.
- **Avatar** — user avatar with fallback initials.

## 3. Domain-specific components

- **Clothing item card** — image, name, category tag, favourite star; a visually distinct DRAFT treatment (e.g. dashed border + "finish details" badge) vs. a clean ACTIVE treatment.
- **Outfit card** — cover image or fallback placeholder, name, tag row.
- **Collage canvas token** — a draggable item chip showing a drag handle, resize/rotate handles sized for touch (≥44×44px), and a layer/z-index indicator.
- **Stat card** — dashboard metric tile (icon, number, label).
- **Wear-log entry** — date, outfit name, optional note, in a compact list row.

## 4. Accessibility & responsiveness notes

Annotate color pairs with contrast ratios where relevant, confirm all interactive elements meet a ≥44×44px touch target, and show how the same components adapt from a 360px-wide mobile layout to desktop (at least for the clothing item card and nav).

## Deliverable

A single React artifact structured as a scrollable style-guide page: foundations first (colors, type, spacing, shadows), then core components, then domain-specific components, each section clearly labeled and showing every variant/state side by side with small captions — a reference I could hand to an engineer to implement pixel-for-pixel in shadcn/ui.
