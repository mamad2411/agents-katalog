---
name: visual-design
description: >-
  Visual design system, brand tokens, and SVG illustration. Defines colors,
  illustration style, and produces optimized SVG assets for marketing surfaces.
  Use with visual-designer subagent when illustrations, brand refresh, or OG
  visuals are needed.
---

# Visual Design & SVG Illustration

**Agent:** `/visual-designer`
**Canonical brand doc:** `docs/design/DESIGN_SYSTEM.md` (create or update **before** feature illustrations)

## Workflow order

1. **Establish / refresh design system** → update `docs/design/DESIGN_SYSTEM.md` (+ theme/Tailwind via FE handoff if tokens change)
2. **Feature asset brief** → `docs/handoffs/{slug}/02c-visual-design.md`
3. **Produce SVG files** → public assets path from `project-context` (e.g. `apps/web/public/illustrations/`)
4. **Frontend integrates** → `frontend-developer` uses paths + `alt` from `02c`

Do not illustrate before colors and illustration style are agreed (even if provisional).

---

## When PM invokes `/visual-designer`

| Invoke                                   | Skip                                |
| ---------------------------------------- | ----------------------------------- |
| Landing hero / section illustrations     | API-only, admin filters             |
| How-it-works step visuals, section icons | Copy-only change with no new assets |
| OG/social share image (1200×630)         | Backend-only work                   |
| Brand refresh, logo, icon set            |                                     |

Note in `00-intake.md`: `visual-design: required | skip | design-system-only`

---

## Design system contents (`docs/design/DESIGN_SYSTEM.md`)

Must define:

| Section            | Contents                                                |
| ------------------ | ------------------------------------------------------- |
| Brand personality  | Tone, audience, anti-patterns                           |
| Color tokens       | Primary, accent, neutrals, semantic, illustration tints |
| Typography         | Font families, scale, weights                           |
| Spacing & radius   | Section rhythm, card style, button shapes               |
| Illustration style | Line weight, palette usage, metaphor rules, do/don't    |
| Iconography        | Stroke vs fill, size grid (24/32/48)                    |
| Accessibility      | Contrast minimums; decorative vs informative images     |

Document token → CSS/Tailwind mapping for FE.

---

## Illustration principles

1. **One idea per asset**
2. **Clear focal point**, works at ~320px and ~1200px width
3. **Limited palette** — ~2 brand colors + 2 neutrals per illustration
4. **Consistent stroke** across a set
5. **Human but abstract** — simplified figures/shapes
6. **No misleading UI** — do not invent fake metrics or peer comparisons
7. Prefer **no text inside SVG** (copy in HTML); OG may have minimal approved text

---

## SVG production rules

| Rule             | Detail                                                             |
| ---------------- | ------------------------------------------------------------------ |
| **viewBox**      | Always set; responsive via CSS                                     |
| **IDs**          | Unique within file; project prefix optional                        |
| **Colors**       | Prefer `currentColor` or CSS variables tied to tokens              |
| **Optimization** | Remove metadata; target < 30KB per hero                            |
| **No raster**    | Embedded PNG/JPEG forbidden in inline SVG for landing              |
| **Usage**        | Static files in `public/` via `<img>` or framework image component |

---

## OG / social image

- **Size:** 1200×630 px
- **Safe zone:** Keep key visuals center
- Coordinate with `.agents/skills/seo/SKILL.md`

---

## Handoff artifact (`02c-visual-design.md`)

- Asset ID, file path, dimensions/viewBox
- Design system version / date
- `alt` text (informative vs decorative) in UI language from `project-context`
- Which page sections consume the asset
- FE integration notes

---

## Collaboration

| Role                   | Responsibility                                          |
| ---------------------- | ------------------------------------------------------- |
| `visual-designer`      | Design system + SVG assets + `02c`                      |
| `marketing-specialist` | Messaging; alt text approval; no fake claims in visuals |
| `frontend-developer`   | Integrate assets, update theme tokens                   |
| `ux-reviewer`          | Composition on page                                     |
| `seo` skill            | OG image wired in metadata                              |

## Review self-check

- [ ] `docs/design/DESIGN_SYSTEM.md` updated if tokens or style changed
- [ ] New SVGs follow design system rules
- [ ] `02c-visual-design.md` lists assets + alt + integration map
- [ ] No metric/claim misrepresentation in artwork
- [ ] Hero/OG tested at mobile and desktop width
