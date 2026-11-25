---
name: mukhon-ui
description: |
  Comprehensive sovereign UI design system and frontend engineering standard for MUKHON.
  Enforces Sovereign Dark Luxury aesthetic tokens, bilingual typography (Bangla & English),
  zero-Tailwind modular vanilla CSS, responsive 3-column shell layouts, WCAG 2.1 AA accessibility,
  resilient micro-interactions, optimistic state updates, and portal-anchored popovers.
license: MIT
metadata:
  version: v1.0.0
  publisher: mukhon-core
---

# MUKHON Sovereign UI & Design System

The **MUKHON UI System** defines the non-negotiable visual language, layout architecture, component standards, and design invariants for the MUKHON platform.

---

## 1. Core Architectural Invariants

1. **Zero Tailwind Dependency:**
   - MUKHON strictly uses a modular **Vanilla CSS** token architecture (`layout.css`, `feed.css`, `profile.css`, etc.) using native CSS custom properties.
   - Do NOT introduce Tailwind utility classes into components.
2. **Sovereign Dark Luxury Aesthetic:**
   - Deep charcoal backgrounds (`#08090B`, `#0E1217`, `#14171D`), emerald sovereign trust accents (`#10B981`, `#006A4E`), gold merchant accents (`#D97706`), subtle border luminescence (`rgba(255, 255, 255, 0.08)`), and soft drop shadows.
   - Light mode is fully supported via `data-theme="light"` and `body.light-theme`.
3. **Bilingual Typography (Bangla & English):**
   - High-legibility Bengali font pairing: `Hind Siliguri`, `Noto Sans Bengali`, and `Anek Bangla` for Bengali text.
   - Clean geometric sans for Latin UI and numerals: `Inter`, system UI fallbacks.
   - Consistent font size and leading scales that accommodate complex Bengali conjuncts and diacritics without vertical clipping.
4. **Clipping Immunity via React Portals:**
   - Any floating element (dropdowns, popovers, context menus, tooltips, modals) triggered inside scrollable containers (such as `.sidebar-right` or `.feed-center`) **MUST** render via React `createPortal(content, document.body)` with dynamic viewport `position: fixed` coordinates to prevent ancestor `overflow-y: auto` or `overflow: hidden` bounding boxes from clipping the UI.
5. **Real Dynamic Data over Mock Personas:**
   - Never populate widgets with fake hardcoded citizen profiles or mock data fallbacks. When backend data is empty or loading, always show polished skeleton primitives or clear sovereign empty states with action triggers.

---

## 2. Token Architecture Overview

Token definitions are layered across three tiers:
- **Primitive Tokens:** Raw color palettes, base font sizes, spacing scale multiples.
- **Semantic Tokens:** Functional tokens mapped to theme contexts (`--bg-body`, `--bg-card`, `--text-primary`, `--border-light`, `--color-accent`).
- **Component Tokens:** Scoped parameters for buttons, badges, modals, and feed cards.

See [references/luxury-tokens.md](references/luxury-tokens.md) for full token values and palette matrices.

---

## 3. Responsive Shell & Layout Grid

MUKHON employs a responsive 3-column sovereign grid:

```
+-----------------------------------------------------------------------------------+
| Desktop Layout (>= 1120px)                                                        |
| +--------------------+ +-------------------------------+ +----------------------+ |
| | Sidebar Left       | | Feed Center Column            | | Sidebar Right        | |
| | (Command Rail)     | | (Search, Nav, Composer, Posts)| | (Utilities, Stories, | |
| | Width: ~260px      | | Width: 600px - 640px          | |  People & Pages)     | |
| | Sticky top: 24px   | | Gap: 16px                     | | Width: ~330px        | |
| +--------------------+ +-------------------------------+ +----------------------+ |
+-----------------------------------------------------------------------------------+
| Mobile Layout (<= 768px / <= 1023px)                                              |
| +-------------------------------------------------------------------------------+ |
| | Top Mobile Header (Logo, Search, Notifications, Menu)                         | |
| | Feed Center Column (Search, Nav Pills, Stories Strip, Composer, Feed Stream)   | |
| | Fixed Bottom Navigation Bar (.mobile-bottom-nav)                              | |
| +-------------------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

- When `.sidebar-right` collapses at `<= 1120px`, the Stories strip adapts into the center column immediately beneath the navigation pills and above the post composer.
- In mobile view (`<= 1023px`), personal suggestion cards ("People You May Know" and "Popular Pages") are hidden from the feed stream to keep focus on citizen posts.

See [references/layout-system.md](references/layout-system.md) for detailed breakpoint definitions.

---

## 4. Component Standards

- **TrustBadges:** 6-tier sovereign identity hierarchy rendered with official SVG badges (`UNVERIFIED`, `NID_VERIFIED`, `NID_PREMIUM`, `VERIFIED_STARTUP`, `VERIFIED_BUSINESS`, `VERIFIED_GOVERNMENT`, `PARODY`).
- **Post Composer & Media:** Multi-aspect responsive media rendering (`1:1`, `4:5`, `16:9`) with clean object containment. No arbitrary image zooming or layout distortion.
- **Micro-Interactions & Optimistic State:** Reactions, follow toggles, and bookmarking update instantly with optimistic client state and rollback on API error.

See [references/component-specs.md](references/component-specs.md), [references/accessibility.md](references/accessibility.md), and [references/mobile-and-pro-ux.md](references/mobile-and-pro-ux.md).
