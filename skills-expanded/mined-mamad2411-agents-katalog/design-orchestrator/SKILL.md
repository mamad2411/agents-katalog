---
name: design-orchestrator
description: "Route a UI/visual-design task to the right skill among 9 design specialists — research-first methodology, the design-intelligence database, concrete style systems, senior engineering rules, spec emitters, design-agent workflows, theming, static art, and brand extraction. USE WHEN a user is designing, styling, redesigning, or polishing an interface, artifact, or brand surface but hasn't named the specific skill or approach."
cluster: design
version: 1.0.0
---

# Design Orchestrator

The single entry skill for design work. It locates the task on the **intent × deliverable**
map and delegates to one of 9 specialist spokes. The cross-cutting model every design task
shares — **research and constraints before generation**, the decision ledger, and the
anti-AI-slop quality gate — lives in `design-core`; read it before generating any pixels.

## Routing map (intent → spoke)

**Design a real product UI (default path)**
- Any interface, landing page, dashboard, redesign, or visual polish → `refero-design` *(research is mandatory — reference before implementation)*
- Need styles / palettes / font pairings / chart types per stack → `ui-ux-pro-max` *(searchable design-intelligence DB)*
- Want a specific, opinionated look applied → `swiss-design` *(Swiss/modernist system in Tailwind)*

**Engineer the interface to a senior bar**
- Metric-based rules, component architecture, motion, hardware-accelerated performance → `taste-skill`
- Emit a reusable, agent-enforceable spec file (anti-generic standards) → `stitch-design-taste` *(produces DESIGN.md)*

**Run a design-agent workflow**
- Iterate drafts / branch variations / extend to more pages from a component → `superdesign`

**Theme an existing artifact**
- Apply or generate a theme for slides, docs, reports, or HTML → `theme-factory`

**Produce static visual art**
- Poster, art piece, print-ready `.png` / `.pdf` → `canvas-design`

**Pull brand identity from the web**
- Extract logos, colors, backdrops, brand name from a URL → `openbrand`

## Standard Operating Flow

1. Locate the task on **intent × deliverable**: is the output a *product UI*, a *spec*, a *themed artifact*, *static art*, or *brand data*?
2. If the output is a product UI or anything user-facing, pull the gate from `design-core` first — **research → lock references → ledger decisions → generate → check against the slop gate.** Skipping research is the failure mode.
3. Delegate to the spoke(s). Multi-step asks fan out in deliverable order (e.g. "brand this landing page" → `openbrand` for tokens → `refero-design` for the layout → `taste-skill` for the build).
4. Return: chosen spoke(s), the references/constraints that anchored the work, the deliverable type, and the next action.

## Guardrails

See `design-core`. In short: **research before generation** — never average from the model's
defaults; ground every choice in a concrete reference and record it in the decision ledger.
Keep type scale, spacing, and color on a system, not ad-hoc. Treat "make it look good" as a
request to *find references and commit to a direction*, not to improvise. The cluster's value
is craft that resists generic AI output — don't quietly fall back to the default look.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as
skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke
named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
