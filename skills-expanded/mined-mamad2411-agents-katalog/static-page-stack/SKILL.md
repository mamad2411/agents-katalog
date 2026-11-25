---
name: static-page-stack
description: SOTA stack recommendations for elegant, controlled, semantic static HTML pages — dashboards, post-mortems, technical-investigation reports,
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch
---

# Static Page Stack (SOTA, 2026)

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## When to use this skill

The user wants to produce **static HTML pages** that combine three aesthetic DNAs:

- Magazine / data-journalism (The Pudding, NYT Upshot)
- Technical documentation (Material/Docusaurus/Starlight)
- Computational notebook (Quarto/Observable/Jupyter Book)

…and embed three kinds of SVG:

- Programmatic charts (Vega-Lite / Observable Plot / D3)
- Hand-authored inline SVG (illustrative)
- Whiteboard-style (Excalidraw / tldraw)

Triggers include: "create a static page", "build a dashboard", "design a post-mortem", "set up a technical-doc site", "what HTML/CSS stack should I use", "this Tailwind soup is unmaintainable".

## The recommended stack (TL;DR)

| Layer                    | Pick                                     | Backup                                   | Why                                                                                                                                      |
| ------------------------ | ---------------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Authoring                | **Quarto**                               | Quartz, Jupyter Book 2 / MyST            | Multi-page, native code+prose+math+execution, MIT, used by Bundesbank/BIS/USGS                                                           |
| Visual system            | **Open Props + native modern CSS**       | Pico.css                                 | Replaces Tailwind utility soup with semantic tokens (4 KB Brotli); OKLCH + container queries + light-dark() are production-ready in 2026 |
| Typography               | **Inter + Crimson Pro + Fira Code**      | IBM Plex family                          | All FOSS; pairing tested at NYT/Pudding-grade                                                                                            |
| Programmatic charts      | **Observable Plot**                      | Vega-Lite, ECharts                       | Cleaner defaults than Vega-Lite, ~95% of needs without going to D3, ISC, Bostock-led                                                     |
| Whiteboard               | **Excalidraw** + `excalidraw_export` CLI | tldraw (note: $6k/yr commercial license) | MIT, mature, build-time SVG render works                                                                                                 |
| Hand-drawn programmatic  | **rough.js** (sparingly)                 | roughViz, chart.xkcd                     | Only for "this is exploratory / uncertainty implied" framing                                                                             |
| Hand-authored inline SVG | CSS-vars-in-SVG pattern                  | `<symbol><use>` for shared icons         | `var(--token)` propagates through inline SVG, giving single design-token surface                                                         |
| Scrollytelling           | **Closeread** (Quarto-native)            | Scrollama                                | Closeread is purpose-built for Quarto; Scrollama (~7 KB) for non-Quarto                                                                  |

## Critical clarifications (don't skip these)

### "XHTML" in 2026 means semantic HTML5, not strict XHTML

Nobody writes literal `application/xhtml+xml` any more. What "elegant XHTML" actually means in modern usage is **well-formed semantic HTML5 enforced by the build tool**. Quarto outputs exactly this — `<article>`, `<aside>`, `<figure>` — without making you hand-author every angle bracket. If a user says "XHTML", clarify they probably mean semantic HTML5 with structural discipline.

### Tailwind itself isn't the problem

The problem is **Tailwind CDN + ad-hoc utility-class soup, no design system, regenerated each time**. Open Props gives you the same "drop-in tokens for everything" feel but as semantic CSS variables that propagate INTO inline SVG. That last property is what makes the stack coherent.

### Distill is dead, Idyll is dormant — don't recommend them

- Distill.pub stopped publishing in 2021. The `distillpub/template` repo looks alive (972 stars) but has no funding story.
- Idyll-lang's last meaningful update was Feb 2023.
- The 2026 spiritual successor is **Quarto's article layout + Closeread**, not a Distill fork.

### tldraw has a non-FOSS commercial clause

tldraw 2.x+ is source-available under a dual license: hobby (watermarked, non-commercial) or **$6,000/year** for commercial. Default to **Excalidraw** (MIT) unless tldraw's specific features (interactive embeds, polished hand-drawn aesthetic) justify the cost.

## Decision flow

```
User wants a static page →
  ├─ Single document, code-heavy, math? → Quarto (single-file render)
  ├─ Multi-page investigation/dashboard? → Quarto with sidebar nav OR Quartz (digital garden) if cross-linking dominates
  ├─ "Pure data dashboard, no narrative"? → Observable Framework (caveat: Observable Inc layoff risk)
  ├─ "I want sidebar nav, search, code blocks"? → Astro Starlight + MDX (functional docs aesthetic)
  └─ "I want maximum flexibility, willing to design"? → Astro + custom theme + Open Props

User wants a chart →
  ├─ Static, magazine-quality default? → Observable Plot (default pick)
  ├─ Need interactivity, dynamic spec generation? → Vega-Lite
  ├─ Need polished interactive dashboards, Canvas OK? → ECharts
  ├─ Want sketchy "this is exploratory" framing? → rough.js / roughViz
  └─ Need bespoke custom path/glyph? → D3 (rare; Plot covers ~95%)

User wants a diagram →
  ├─ Architecture, flow, illustrative? → Excalidraw + excalidraw_export
  ├─ Premium aesthetic, budget for $6k/yr? → tldraw + tldraw-cli
  ├─ Inline SVG with design tokens? → Hand-author with var(--token-*)
  └─ Reused across many pages? → <symbol><use> pattern (caveat: shadow DOM blocks per-instance CSS)
```

## Concrete migration: Tailwind CDN soup → Quarto + Open Props

Phased migration (~5-6 weeks total for a multi-spoke dashboard):

**Phase 1 — Pilot (1-2 weeks):** Convert one page/spoke to Quarto. Match current visual output by writing custom SCSS theme that reuses existing palette but expressed as Open Props tokens + OKLCH. Ship as separate `dashboard-quarto/` directory.

**Phase 2 — Aesthetic upgrade (1 week):** Swap to Inter + Crimson Pro + Fira Code, replace ad-hoc Tailwind colors with OKLCH-generated palette ramps from `oklch.fyi`, standardize figure/chart components.

**Phase 3 — Charts (1 week):** Convert hand-authored data-bearing SVGs to Observable Plot specs. Illustrative SVGs (architecture, flowcharts) move to Excalidraw.

**Phase 4 — Scrollytelling (1 week):** Pick 2-3 mechanism explainer pages. Rewrite as Closeread scroll-driven explainers.

**Phase 5 — Roll out (~1 week per remaining page):** Use phase 1's templates.

## Anti-patterns to call out

When you see these in user code, recommend alternatives from the stack:

1. **`<script src="https://cdn.tailwindcss.com">`** in a static page → Use Quarto + Open Props instead. Tailwind CDN doesn't tree-shake → bloated CSS, no design system, every regeneration drifts.
2. **Inline base64-encoded SVG `<img>`** → Use inline `<svg>` with `var(--token)` for design-system propagation, OR `<svg><use href="#sym">` for shared icons.
3. **Hand-typed numeric values in charts** ("forecast: 189K, actual: 223K") → Use Observable Plot reading from a CSV/parquet so the chart re-renders if the number is corrected.
4. **`style="color: #abc123"` repeated across pages** → Define an OKLCH palette in `:root`, expose via Open Props tokens, reference via `var(--color-*)`.
5. **Mermaid/Graphviz in a project that wants editorial-quality diagrams** → Switch to Excalidraw or hand-authored inline SVG. (Mermaid is great for "boxes-and-arrows generated from text" but never reaches editorial quality.)

## Honest tradeoffs (don't oversell)

- **Quarto's default theme is not magazine-grade.** Bundesbank-quality output exists, but you'll spend ~1-2 weeks on a custom SCSS theme. If the user wants plug-and-play magazine aesthetic with zero design work, no FOSS option in 2026 truly delivers — The Pudding's `svelte-starter` is closest but it's Svelte+Vite (not Quarto).
- **Observable Framework has post-layoff risk** at Observable Inc (2023, possibly 2025). ISC license means a fork is viable but corporate backing is thinner than Posit's commitment to Quarto.
- **Open Props requires learning the token naming scheme.** Not "plug and play" like Tailwind. The payoff is a coherent design system, but the first week is steeper.

## How to apply this skill

1. **Identify the user's actual ask** — single page or multi-page? Code-heavy or prose-heavy? Charts or just diagrams? Pure narrative or data-driven?
2. **Use the decision flow above** to pick the framework + chart-lib + diagram-lib trio.
3. **Default to Quarto + Open Props + Observable Plot + Excalidraw** unless something specific rules it out.
4. **Reference `references/full-research-synthesis.md`** for the per-layer evidence summary if the user wants to see the comparative analysis.
5. **Don't recommend dead/dormant tools** (Distill, Idyll, plain Tailwind CDN).
6. **Pull starter templates from the URLs in `references/sota-urls.md`** when scaffolding a new project.

## Post-Execution Reflection

If a recommendation didn't fit the user's needs in practice (e.g., Quarto's build was too heavy for their scale, or Observable Plot couldn't express their viz), update this skill — note the case and the alternative that actually worked. Don't defer to "next time."
