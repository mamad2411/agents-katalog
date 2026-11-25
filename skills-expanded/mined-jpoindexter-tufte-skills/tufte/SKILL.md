---
name: tufte
description: "Use when invoked by name (/tufte in Claude Code, $tufte in Codex, or 'tufte' in any agent), or when creating, reviewing, or auditing any data display — chart, graph, table, dashboard, map, timeline, sparkline, diagram, annotated image, slide deck, meeting doc, or evidence presentation — and it's unclear which tufte-* skill applies. Router for the 38-skill Edward Tufte pack."
tags: [tufte, data-visualization, router, dispatcher]
---

# Tufte Router

Front door to the 38-skill Edward Tufte pack. Route the task to the smallest set of sibling skills, load them, apply them to the work at hand. Do not return a catalog or a description of the pack — use it. (Tufte's own trilogy framing, VE p.10: VDQI = pictures of numbers, EI = pictures of nouns, VE = pictures of verbs.)

## Loading sibling skills — works in any agent

Every sibling skill is installed beside this one, in the same skills directory: `../<slug>/SKILL.md` relative to this file (e.g. `~/.claude/skills/tufte-sparklines/SKILL.md`, `~/.codex/skills/tufte-sparklines/SKILL.md`).

- **Claude Code:** invoke the sibling by slug with the Skill tool.
- **Codex CLI, Copilot CLI, Gemini CLI, opencode, or any other agent:** read the sibling's `SKILL.md` with your file-read tool, then follow it. Reading the file IS loading the skill — no special tool required.
- **Single-file fallback:** if the siblings are not installed, read `CANON.md` in this folder — the complete pack condensed into one document. Use it whenever loading multiple siblings is impractical in your runtime.

## Route

1. Treat any arguments after the invocation as the task. No arguments → use the active task.
2. Select 1–4 skills from the routing table. Load them, apply them, and name which you used in one line.
3. About to ship a display? Run the Master Audit below and load the matching skill for any point that fails.

## Routing table

| Task signal | Load |
|---|---|
| New chart or graphic from scratch; choosing graphic vs table vs sentence | `tufte-graphical-excellence` |
| Axis scaling, truncated baseline, "is this misleading", pictogram sizing | `tufte-graphical-integrity` |
| Decluttering, "too busy", gridlines, fills, frames | `tufte-data-ink-ratio` + `tufte-chartjunk` |
| Visual noise, figure/ground, layer weights, boxed labels | `tufte-layering-and-separation` |
| Many series or conditions to compare; faceting; trellis | `tufte-small-multiples` |
| "How much data can this hold", sparse-vs-dense calls | `tufte-data-density` |
| Inline trends, KPI rows, word-sized graphics, table cells with history | `tufte-sparklines` |
| Choosing or reviewing color | `tufte-color-in-information-design` + `tufte-redundant-encoding` |
| Geographic or spatial data | `tufte-data-maps` + `tufte-micro-macro-readings` |
| Schedules, timetables, movement over time | `tufte-space-time-graphics` |
| Causal claims, A/B results, "did X cause Y", pre/post charts | `tufte-causal-reasoning-in-graphics` + `tufte-evidence-corruption` |
| Slide decks, report vs presentation, bullet hierarchies | `tufte-cognitive-style` + `tufte-analytical-design` |
| Diagrams with arrows or connectors; architecture diagrams | `tufte-link-differentiation` |
| Annotating images, screenshots, photos as evidence | `tufte-mapped-pictures` |
| Before/after, side-by-side, overlay comparisons | `tufte-parallelism` |
| Multi-image argument, poster, explainer composition | `tufte-visual-confections` |
| Labels, legends, table typography, linebreaks in data | `tufte-typography-for-data` |
| Multivariate data on a flat screen; >2 variables | `tufte-escaping-flatland` + `tufte-multifunctioning-elements` |
| Reports/docs where figures, tables, and text are segregated; "see Figure 3" | `tufte-integration-of-modes` |
| Annotating evidence, commentary layers, explaining a display in place | `tufte-annotation-as-thinking` |
| UI copy, wayfinding, help text, labels at the point of action | `tufte-instructions-at-point-of-need` |
| Step-by-step narrative, instructional sequence, motion in stills | `tufte-narrative-and-sequence` |
| Evidence quality, cherry-picking, model-searching, integrity of analysis | `tufte-evidence-corruption` + `tufte-visual-thinking` |
| Aesthetic polish, proportion, line weight, friendliness | `tufte-aesthetics-and-technique` |
| Sentence vs table vs graphic; dense reference tables, supertables | `tufte-tables-and-text-tables` |
| An org keeps shipping bad graphics; who makes them; review gates | `tufte-graphical-competence` |
| Suspected deceptive display; instructions showing hidden mechanics | `tufte-disinformation-design` |
| Chrome, frames, mounts, packaging accreting around finished work | `tufte-presentation-of-artifacts` |
| Backlogs, nav menus, taxonomies, tag systems — what order and why | `tufte-lists` |
| Design reviews, decision meetings, pre-reads, study-hall protocol | `tufte-meetings-and-documents` |
| Auditing an analysis or dataset for errors, bias, provenance, fraud | `tufte-data-forensics` |
| Reference indexes, back matter, asset registries, changelogs | `tufte-visual-index` |
| Dashboard, KPI card grid, metric tiles, status board | `tufte-sparklines` + `tufte-tables-and-text-tables` + `tufte-data-density` |
| Small-screen or mobile display; chart on a phone; how small can this go | `tufte-data-density` + `tufte-sparklines` |
| A specific chart type is in question — pie, donut, funnel, gauge, stacked area, dual axis, 3-D | `tufte-graphical-integrity` + `tufte-graphical-excellence` |
| Long table, many rows, big list, long log — must read at a glance and up close | `tufte-micro-macro-readings` + `tufte-tables-and-text-tables` |
| Heatmap, density plot, choropleth, session or attention map | `tufte-micro-macro-readings` + `tufte-color-in-information-design` |
| Accessibility, color-blind safety, grayscale survival, contrast of encodings | `tufte-redundant-encoding` + `tufte-color-in-information-design` |
| PRD, spec, RFC, technical doc, or report carrying numbers and figures | `tufte-integration-of-modes` + `tufte-meetings-and-documents` |
| Vendor demo, sales deck, procurement or tool evaluation, benchmark claim | `tufte-disinformation-design` + `tufte-data-forensics` |
| Portfolio, case study, app-store screenshots, showcasing finished work | `tufte-presentation-of-artifacts` + `tufte-visual-confections` |
| Glossary, definitions, terminology page, taxonomy of terms | `tufte-lists` + `tufte-tables-and-text-tables` |
| Incident timeline, project timeline, Gantt, sequence of events | `tufte-space-time-graphics` + `tufte-narrative-and-sequence` |
| Aspect ratio, proportion of a plot, slopes look wrong, chart is too tall or too wide | `tufte-aesthetics-and-technique` + `tufte-sparklines` |
| "Compared with what?" — missing baseline, control, or reference class | `tufte-causal-reasoning-in-graphics` + `tufte-parallelism` |
| How strong should a contrast be — smallest effective difference, contrast sizing | `tufte-layering-and-separation` |
| "Our audience won't understand this"; dumbing a display down for stakeholders | `tufte-graphical-competence` + `tufte-cognitive-style` |
| Accepting an inherited format, template, style sheet, or default chart type | `tufte-visual-thinking` |
| Interaction hides data — tooltips, hovers, drill-downs, collapsed panels | `tufte-annotation-as-thinking` + `tufte-micro-macro-readings` |

**Precedence when several rows fire.** Pick the *narrowest* matching row, then add at most one broader row. Specific collisions:

- Analysis-quality tasks: `tufte-data-forensics` when auditing a **dataset or method**; `tufte-evidence-corruption` when auditing a **presentation of results**; `tufte-causal-reasoning-in-graphics` when a **causal claim** is at stake. Load one, not all three.
- Decks: `tufte-meetings-and-documents` when the question is **the meeting** (format, pre-read, time budget); `tufte-cognitive-style` when the question is **the deck** (density, bullets, headlines). `tufte-analytical-design` only when defending a design against a standard.
- Annotation: `tufte-mapped-pictures` when the base is a **photograph or scientific image** needing scales and grids; `tufte-annotation-as-thinking` when the base is a **chart, diagram, or screen** needing commentary.

## Master Audit — run before shipping any data display

Each point names the skill to load for depth on a failure.

1. **Format** — does this deserve a graphic at all (vs sentence/table)? Right form chosen? → `tufte-graphical-excellence`
2. **Truth** — Lie Factor ≈ 1.0; visual dims ≤ data dims; no truncated baseline or spare dimension → `tufte-graphical-integrity`
3. **Ink** — two-pass erasure done; grid gray or gone; no fills/3-D/shadows → `tufte-data-ink-ratio`
4. **Chartjunk** — no moiré fills, dark grids, or ducks → `tufte-chartjunk`
5. **Density** — data matrix as large as the question warrants; shrinkable by half? → `tufte-data-density`
6. **Multivariate** — variables shown vs variables the phenomenon has → `tufte-escaping-flatland`
7. **Comparison** — "compared with what?" answered on the display; everything compared in one eyespan, like against like, causal variable on the axis → `tufte-causal-reasoning-in-graphics` (the question), `tufte-small-multiples` (the eyespan)
8. **Layering** — weight ∝ importance; 1+1=3 effects hunted; nothing boxed → `tufte-layering-and-separation`
9. **Color** — role named (label/measure/represent/decorate); no red/green solo → `tufte-color-in-information-design`
10. **Type** — direct labels, no legend; horizontal; tabular figures → `tufte-typography-for-data`
11. **Documentation** — author, sources, scales, units, date on the display itself → `tufte-analytical-design`
12. **Integrity** — data traceable; no cherry-picked baselines, bins, or models; headline = actual finding → `tufte-evidence-corruption`

## Guardrails

- Load 1–4 siblings, not the whole pack; `CANON.md` covers the everything-at-once case.
- Routing must end in application to the current task, not a summary of what the skills say.
- Chart *selection and encoding* mechanics (which chart type, perceptual channel ranking) live outside this pack — pair with a data-visualization skill if installed.
