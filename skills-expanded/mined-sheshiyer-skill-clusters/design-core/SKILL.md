---
name: design-core
description: "Shared reference for the design cluster: the one decision every design turns on — research-first vs generate-from-defaults — plus the decision ledger, type/space/color conventions, the spoke capability matrix, and the anti-AI-slop quality gate. USE WHEN designing, styling, or polishing any UI or visual artifact and choosing how to ground the work before generating pixels."
cluster: design
version: 1.0.0
---

# Design Core

Shared model for the `design` cluster. The methodology, system, and engineering spokes all
depend on these concepts — keep them consistent here so no spoke contradicts another.

## 1. The defining decision: research-first, not generate-from-defaults

A design is **grounded**, never averaged. The failure mode of an AI designer is reaching for
its mean output ("AI slop"): centered hero, generic SaaS gradient, default shadows, Inter at
three sizes. The cluster exists to prevent that. Every design follows one direction of flow:

```
Research references ──> Lock a direction ──> Record decisions (ledger) ──> Generate ──> Check against the slop gate
```

- **Research** — find concrete references before touching layout. `refero-design` makes this mandatory; `ui-ux-pro-max` supplies a searchable database when live references are thin.
- **Lock** — commit to one visual direction (a reference set, a system like Swiss, or a brand). Don't blend three.
- **Ledger** — write down each non-obvious choice and *why* (the reference it came from). This is what makes the result defensible and editable.
- **Gate** — before shipping, check the output against the anti-averaging gate in §5.

**Rule:** when the ask is "make it look good," that means *find references and commit to a
direction* — not improvise from defaults. Skipping research is the one thing that breaks the cluster.

## 2. Conventions every spoke shares

- **Type** on a scale (modular, e.g. 1.25×), not arbitrary px; limit families; weight and size carry hierarchy.
- **Space** on a system (4 / 8 px rhythm); whitespace is a design choice, not leftover.
- **Color** as tokens with explicit roles (primary / secondary / surface / text), enough contrast for accessibility; opacity for hierarchy over new hues.
- **Motion** is purposeful and hardware-accelerated (`transform`/`opacity`), never decorative jank.
- **Tokens** (color, type, spacing) are the contract between brand extraction, theming, and build — keep one source of truth.

## 3. Deliverable types & ownership

The frontend is the eventual surface; these spokes own different *stages* before it:

- **Methodology / research** → `refero-design` (default), `ui-ux-pro-max` (DB), `swiss-design` (a ready system).
- **Engineering / spec** → `taste-skill` (senior rules + perf), `stitch-design-taste` (emits an enforceable `DESIGN.md`).
- **Workflow** → `superdesign` (drafts, branch iterations, multi-page flows).
- **Artifact theming** → `theme-factory` (slides/docs/HTML).
- **Static art** → `canvas-design` (`.png`/`.pdf`).
- **Brand input** → `openbrand` (logos/colors/name from a URL → tokens).

## 4. Capability matrix

| I need to… | Spoke | Output |
|---|---|---|
| Design a product UI, grounded in references | `refero-design` | layout + rationale |
| Pick styles / palettes / fonts / charts per stack | `ui-ux-pro-max` | design-intelligence lookups |
| Apply an opinionated modernist system | `swiss-design` | Tailwind Swiss styling |
| Hit a senior engineering bar (rules + perf) | `taste-skill` | component architecture |
| Emit a reusable anti-generic spec file | `stitch-design-taste` | `DESIGN.md` |
| Iterate drafts / variations / extra pages | `superdesign` | design-agent run |
| Theme slides / docs / reports / HTML | `theme-factory` | applied theme |
| Make a poster / print-ready art piece | `canvas-design` | `.png` / `.pdf` |
| Extract a brand from a URL | `openbrand` | brand tokens |

## 5. The anti-AI-slop quality gate

Before calling a design done, check it does **not** read as default AI output:

- Did it start from a **real reference**, or from the model's mean? (References required.)
- Is there a **point of view** — one direction committed to — or a blend of three?
- Are type, space, and color on a **system**, or ad-hoc?
- Is there **intentional asymmetry / tension**, or just a centered column with a gradient?
- Could you **defend each choice** from the ledger?

If any answer is "default," return to §1 step 1.

## 6. Conventions / scope

- Most spokes are **stack-agnostic** craft; `ui-ux-pro-max` carries stack-specific data (React, Next, Vue, Svelte, SwiftUI, RN, Flutter, Tailwind), and `swiss-design` targets Tailwind.
- `openbrand` depends on an external MCP/npm service for live extraction — treat it as the *input* edge that feeds tokens into the rest of the cluster.

## 7. Shared guardrails

- **Research before generation**; never average from defaults.
- Commit to **one** direction; don't blend references.
- Keep type / space / color on a **system** with explicit tokens.
- Record non-obvious choices in the **decision ledger** with their source.
- Run the **slop gate** (§5) before shipping any user-facing surface.
- Motion and effects must be purposeful and performant — no decorative jank.
