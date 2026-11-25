---
name: ns-proto-visual-guide
description: >-
  (NS) Normative visual appearance guides for UI surfaces (card/form/shell/overlay):
  block order, states, palette, Action|What-changes tables. MUST use for
  descrição normativa, guia visual, aparência, visual QA checklist, "how this
  looks", docs named *-visual.md / *-painel-visual.md / *-appearance.md (and
  kin), or shell vs content / card vs form / carcaça vs formulário. Prefer
  prototype/ as source of truth when present; after behavioral UX guides, offer
  ns-sdd-living-spec-consolidator appearance mode. Do NOT use for business
  rules, ERDs, layout/grid math, API/auth, e2e, or prototype create/evolve
  (ns-proto-creator).
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.0"
depends:
  - ns-harness
  - ns-sdd-living-spec-consolidator
---

# Normative visual description

Normative guides: **how UI surface must look** — not how implemented. Audience: design, product, visual QA. Need block order, hierarchy, states, sibling consistency.

Project-agnostic. Canonical specimens: [examples/](examples/README.md).

Guide language = project docs language (often English; follow repo). Section intent identical even when localizing headings.

When `{product_root}/prototype/` exists, prefer its components as **source of truth** over legacy app trees unless user points elsewhere. Cite `prototype/` paths in source-of-truth table.

## Instructions

1. **Name surface** — card / form / shell / overlay; match project doc language.
2. **Read before write** — open source components (prefer `prototype/`) + sibling docs same surface type. Invent absent UI → QA trust break.
3. **Load specimen** — one matching file under [examples/](examples/README.md); mirror tone, section density, table style.
4. **Boundary first** — write **Does not cover** (links to siblings) before body. Unscoped guides swallow business rules + layout math.
5. **Draft from template** — keep section order; prefer `Element | How it should appear` tables over long prose.
6. **Wire graph** — update docs index + cross-links (card ↔ form ↔ shell ↔ layout). Orphans never reviewed.
7. **Stay honest** — document what code shows today; desired look differs → say explicit.
8. **Living specs (when needed)** — guide documents product-visible behavioral UX (not pure chrome polish) → invoke `ns-sdd-living-spec-consolidator` **appearance** mode with guide path + short behavioral delta. Skip polish-only.

### Why these constraints

| Constraint | Reason |
|------------|--------|
| Normative voice ("must" / "should") | Validation checklists need pass/fail, not narrative |
| Visual form only | Deep domain in product/spec docs; mix kills scanability |
| One file = one surface | Card and form answer different questions |
| Code as source of truth | Specs drift from components → decoration |
| Full states | Empty, overflow, disabled, warning, conditional visibility — where QA fails |
| Behavior as `Action \| What changes on screen` | Ties interaction to visible change; no hooks/state story |

## Output template

ALWAYS structure new guides like this (adapt titles; keep opening contract):

```markdown
# [Surface] — appearance [on the canvas / in the side panel / on screen]

Normative guide for **how [surface] must appear** in [context]: [short scope].

For design, product, and visual validation. **Does not describe** [explicit limits].

**Does not cover:**
- [Item] — see [sibling doc link]

**Source of truth in code:**
| File | Responsibility |

**Related documents:**
- [links]

---

## What it is
[1–3 short paragraphs: role, read-only vs editable, relation to siblings]

## What it [does not show / does not cover in the body]  ← optional; useful for forms
| Absent section | Reason |

## Overview — block order
[ASCII of vertical/horizontal structure]

### [Modes / branches]  ← when mutually exclusive modes exist
| State | Body shown |
[mermaid if it clarifies branching]

## [Block / section name]
| Element | How it should appear |

## Palette and style
| Element | Appearance |

## Expected visual behavior
| User action | What changes on screen |

## Quick visual checklist
- [ ] ...
```

### Optional sections (when surface needs)

- **What it does not show** — contrast sibling surface (e.g. child item vs top-level)
- **Modes** — normal/variant; edit vs follow-along
- **Selection and hover** — container states
- **Handles / anchors** — graph cards

## Surface types

| Type | Doc focus | Keep out |
|------|-----------|----------|
| Canvas card | Zones, RO content, badges, handles, create buttons | Panel form fields; layout formulas |
| Panel form | Field order, toggles, empty states, modes | Shell chrome; canvas card chrome |
| Shell | Fixed chrome (width, header, scroll) | Per-selection form bodies |
| Technical layout | Grid, gaps, resize | Visual appearance (sibling normative doc) |

One file = one surface.

## Anti-patterns

- Mix shell with content, or card with form — reviewers cannot tell which surface failed
- Paste long domain rules into visual guide — link; no dump
- Describe implementation (`useState`, class names as story) instead of appearance
- Skip empty states, warnings, conditional visibility
- Publish without index entry or cross-links
- Replace normative guide with summary matrix (matrix points *to* guide)
- Cite `vN/prototype/` as layout — product has one `prototype/` tree; versioning = git

## Examples

Before draft, open specimen for surface:

| Intent | Read first |
|--------|------------|
| Canvas card | [examples/card-canvas.md](examples/card-canvas.md) |
| Panel form | [examples/form-panel.md](examples/form-panel.md) |
| Panel chrome only | [examples/shell-panel.md](examples/shell-panel.md) |

Naming + publish checklist: [examples/README.md](examples/README.md).

## Related skills

- `ns-proto-creator` — capture live UI; create/evolve single `prototype/` tree
- `ns-sdd-living-spec-consolidator` — **appearance** mode after behavioral UX documented
