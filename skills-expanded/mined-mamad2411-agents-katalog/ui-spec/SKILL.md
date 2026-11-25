---
name: ui-spec
description: "Use when creating a UI specification. Documents visual design: components, typography, color system, spacing, layout, and design tokens. Pure UI only — no user flows, task logic, or business rules."
---

# UI Specification

Documents the interface design: what the product looks like and how its visual elements are defined. No user flows or business logic here — that lives in `ux-spec`.

**UI covers:** components, typography, color system, spacing scale, layout grids, iconography, design tokens, visual states (default/hover/active/disabled/error).  
**UI does NOT cover:** user flows, task sequences, navigation logic, business rules, interaction decisions.

## Process

```
Scan context → Design language → Color system → Typography → Spacing
→ Component inventory → Per component: states + specs → Tokens → Write
```

## Detect docs folder

Run:
```bash
find . -maxdepth 3 -type d -name "docs" | grep -v node_modules | grep -v ".git" | sort
```

- **1 result:** use that path as docs root (e.g., `./docs`)
- **Multiple results:** use AskUserQuestion — "Found multiple docs folders: [list]. Which one should I use for this project?"
- **No result:** use `docs/` and create it if missing

## Step 0 — Scan context

Before asking anything:
- Read `docs/03_design/ux_spec.md` if exists → extract sections and flow names (informs component needs)
- Read `docs/01_product/03_product_principles.md` if exists → visual personality clues
- Tell user what you found.

## Step 1 — Design language

**Q1:** "How would you describe the visual personality of this product?" (AskUserQuestion options: Clean and minimal / Bold and expressive / Warm and approachable / Professional and structured)

**Q2:** "Are there existing brand assets? (logo, brand colors, font already chosen)" (free text or "None yet")

**Q3:** "Is there a design system or component library being used as a base?" (AskUserQuestion options: None — custom / Tailwind CSS / Material Design / Apple HIG / Shadcn/ui / Other)

## Step 2 — Color system

**Q4:** "Define the core colors. List by role." (free text)
Expected format:
- Primary: [color / hex]
- Secondary: [color / hex]
- Background: [color / hex]
- Surface: [color / hex]
- Text primary: [color / hex]
- Text secondary: [color / hex]
- Error: [color / hex]
- Success: [color / hex]
- Warning: [color / hex]

If user says "not decided yet", document as TBD with intent description (e.g., "Primary: warm green, exact hex TBD").

**Q5:** "Does the product support dark mode?" (options: Light only / Dark only / Both)

## Step 3 — Typography

**Q6:** "What font(s) are used?" (free text)
Example: "Inter for all text", "Playfair Display for headings + Inter for body"

**Q7:** "Define the type scale. List sizes by role." (free text)
Expected: heading-xl, heading-lg, heading-md, body-lg, body-md, body-sm, caption, label

## Step 4 — Spacing and layout

**Q8:** "What is the base spacing unit?" (AskUserQuestion options: 4px / 8px / Other)

**Q9:** "Describe the layout grid." (free text)
Example: "Mobile: 16px margins, 8px gutter. Tablet+: 24px margins, 12-column grid."

## Step 5 — Component inventory

**Q10:** "List the UI components this product needs." (free text)
Example: "Button (primary/secondary/ghost), Input, Card, Modal, Toast notification, Bottom sheet, Tab bar, Avatar, Badge, Empty state"

For each component the user lists, ask:

**Q11a:** "What variants does [component] have?" (free text)
Example for Button: "primary, secondary, destructive, ghost — each in default/hover/active/disabled states"

**Q11b:** "Any specific specs for [component] that differ from the base design system?" (free text or "Standard")

Only ask Q11a+b for components with non-obvious behavior or custom specs. Skip for clearly standard ones.

## Step 6 — Iconography and imagery

**Q12:** "What icon set is used?" (free text or "TBD")
Example: "Lucide Icons", "Custom SVGs", "SF Symbols (iOS only)"

**Q13:** "Are there any imagery guidelines? (photos, illustrations, avatars)" (free text or "N/A")

## Document Generation

```markdown
# UI Specification

**Project:** [name]
**Platform:** [from ux-spec or ask]
**Status:** Foundational UI spec
**Date:** [today]

> This document covers interface design only: components, visual styles, and design tokens.
> User flows, navigation logic, and interaction rules are in `docs/03_design/ux_spec.md`.

## 1. Design Language

**Visual personality:** [Q1]

**Base system:** [Q3]

## 2. Color System

| Token | Value | Usage |
|-------|-------|-------|
| color-primary | [hex] | Primary actions, links |
| color-secondary | [hex] | Secondary actions |
| color-background | [hex] | Page/screen background |
| color-surface | [hex] | Cards, modals, sheets |
| color-text-primary | [hex] | Main body text |
| color-text-secondary | [hex] | Supporting text, labels |
| color-error | [hex] | Errors, destructive states |
| color-success | [hex] | Confirmations, positive states |
| color-warning | [hex] | Warnings, caution states |

**Dark mode:** [Q5]

## 3. Typography

**Fonts:** [Q6]

| Token | Size | Weight | Line height | Usage |
|-------|------|--------|-------------|-------|
| text-heading-xl | [size] | [weight] | [lh] | Page titles |
| text-heading-lg | [size] | [weight] | [lh] | Section headers |
| text-heading-md | [size] | [weight] | [lh] | Card titles |
| text-body-lg | [size] | [weight] | [lh] | Primary body |
| text-body-md | [size] | [weight] | [lh] | Secondary body |
| text-body-sm | [size] | [weight] | [lh] | Supporting text |
| text-caption | [size] | [weight] | [lh] | Labels, captions |

## 4. Spacing Scale

**Base unit:** [Q8]

| Token | Value | Usage |
|-------|-------|-------|
| space-1 | [base×1] | Tight internal padding |
| space-2 | [base×2] | Component internal padding |
| space-3 | [base×3] | Between related elements |
| space-4 | [base×4] | Between sections |
| space-6 | [base×6] | Large gaps |
| space-8 | [base×8] | Page margins |

**Layout grid:** [Q9]

## 5. Components

### [Component name]

**Variants:** [Q11a]

**States:** default / hover / active / disabled / [error if applicable]

**Specs:** [Q11b — custom specs or "follows base system"]

---

[Repeat per component]

## 6. Iconography

**Icon set:** [Q12]

**Size scale:** [e.g., 16px / 20px / 24px]

## 7. Imagery

[Q13 — guidelines or N/A]
```

## File Output

- Create `docs/03_design/` if missing
- Write to `docs/03_design/ui_spec.md`
- After writing, ask if user wants to create `docs/03_design/prototype_docs.md` using `pi-dev:prototype-docs`

## Quality Check Before Writing

- No user flows or task sequences in this document
- Every color token has a defined role (not just a hex value)
- Every component has explicit states listed (not just "default")
- Typography scale uses tokens, not raw pixel values
