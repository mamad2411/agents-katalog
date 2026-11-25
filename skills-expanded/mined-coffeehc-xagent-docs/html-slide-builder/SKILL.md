---
name: html-slide-builder
description: Use when creating a self-contained HTML slide deck, web-native presentation, visual pitch deck, briefing deck, teaching deck, product walkthrough, strategy deck, or meeting presentation that should open locally without build tools, network access, package installs, or external runtimes. Do not use for general HTML reports, frontend app prototypes, PPTX editing, deployment, or external publishing flows.
meta:
  version: 1
  display_name: HTML 幻灯片生成器
  source: nexu-io/open-design design craft and deck templates
  license: Apache-2.0
---

# HTML Slide Builder

## Purpose

Create one production-ready HTML slide deck that can be opened from local disk, presented in a browser, printed to PDF, and archived. The deck must be self-contained, visually deliberate, source-grounded, and free of runtime dependencies.

This Skill adapts design craft and deck constraints from reviewed open-source Open Design material. It intentionally excludes Open Design CLI, MCP server, daemon, apps, package manager, export pipeline, templates as runtime dependencies, and deployment workflows.

## Use When

Use for:

- HTML slide decks, web-native presentations, briefing decks, pitch decks, teaching decks, walkthroughs, strategy decks, or decision presentations.
- Turning notes, Markdown, research, meeting outcomes, product material, or structured recommendations into a slide-by-slide narrative.
- Creating an offline deck for browser presentation, print/PDF handoff, or static artifact archival.
- Designing visual slides where layout, typography, color discipline, density, and presentation flow matter.
- Reworking an existing HTML deck for clarity, structure, accessibility, print behavior, or visual quality.

Prefer this Skill over `html-report-builder` when the primary artifact is a paged presentation with slide navigation. Prefer `html-report-builder` when the output is a scrollable report, evidence brief, dashboard, or document-like page.

## Do Not Use When

Do not use for:

- General reports, research briefs, dashboards, or long-form scroll pages; use `html-report-builder`.
- Data analysis where computation, chart selection, or statistical interpretation is central; use `data-visual-report-builder` first.
- PowerPoint/PPTX file editing, Office conversion, or document export workflows.
- Frontend app prototypes, product UI implementations, landing pages, or deployable websites.
- React, Vue, Next.js, Vite, Tailwind projects, component libraries, local dev servers, or multi-file frontend apps.
- Open Design CLI, `od` daemon, MCP setup, package install, browser automation, deploy, publishing, Figma, or external design platform workflows.
- Inventing metrics, quotes, customers, financials, owner names, dates, roadmap commitments, or evidence.

## Material Gate

Before building the deck, identify:

- Audience, presentation setting, title, language, expected duration, and desired slide count.
- Core message, decision ask, teaching goal, sales motion, or narrative arc.
- Source material: notes, research, meeting transcript, roadmap, screenshots, product facts, data, brand constraints, or existing artifacts.
- Required slide types: title, agenda, section divider, insight, comparison, timeline, chart, workflow, demo frame, quote, decision, appendix, or speaker notes.
- Visual constraints: brand palette, tone, aspect ratio, printable needs, accessibility needs, and whether screenshots/images are available.
- Claims requiring evidence, missing facts, caveats, and confidentiality constraints.

If key evidence is missing, keep the deck structure and mark `待确认` / `Not verified`. Do not fill gaps with decorative placeholder facts.

## Output Contract

The default output is:

- Exactly one `.html` file unless the user asks only for an outline or critique.
- Fully self-contained: inline CSS, inline vanilla JavaScript, inline SVG, inlined data, and local or embedded media only when already available and safe.
- Openable from local disk without network access, package install, build step, local server, MCP, daemon, or external renderer.
- A fixed 16:9 slide stage by default, responsive by scaling the stage to fit the viewport without distorting layout.
- Keyboard and click navigation, visible current slide position, URL hash or equivalent stable slide addressing, and print/PDF styling.
- Accessible text alternatives or adjacent textual summaries for visual information.
- Printable with `@media print`, one slide per page where feasible, controls hidden, and backgrounds/text preserved.

Do not depend on CDN libraries, remote fonts, remote images, iframe embeds, analytics, package managers, Open Design runtime, browser extensions, local listeners, or deployment services.

## Workflow

1. Classify the deck mode: briefing, pitch, teaching, product walkthrough, strategy, decision, status, workshop, or appendix-heavy deck.
2. Produce or infer a slide outline before writing HTML: one idea per slide, clear section breaks, and a visible end state.
3. Read `references/deck-rules.md` for slide structure, navigation, print, notes, and validation rules.
4. Read `references/design-craft.md` for visual quality rules when the deck needs strong design judgment.
5. Choose a restrained visual system: typography scale, palette, spacing, chart tokens, layout grid, and motion policy.
6. Implement a single static HTML document with semantic slide sections, inline CSS, optional inline vanilla JS, and native SVG where needed.
7. Keep JavaScript as progressive enhancement. The deck should remain readable if JS fails.
8. Use data-backed charts and tables only when they clarify the narrative. Include units, source, and exact values.
9. Add speaker notes only when useful, hidden from normal presentation view and visible in print or notes mode only if requested.
10. Validate offline, responsive, keyboard, print, source, and accessibility requirements before delivery.

## Checks

- The first three slides make the audience, topic, and thesis clear.
- Each slide has one primary job and does not mix unrelated claims.
- Long prose is moved into speaker notes, appendix, or handout text.
- Layout uses stable dimensions so labels, controls, numbers, and media do not resize the slide.
- Typography, color, and spacing feel intentional rather than default generated styling.
- The deck avoids decorative blobs, generic purple gradients, glassmorphism, emoji icon systems, fake metrics, filler copy, and stock-like visuals.
- Navigation works by keyboard and pointer, slide count is visible, and the current slide can be linked or restored.
- Print/PDF output is usable without overlapping controls or clipped content.
- No external network, package, runtime, deployment, or MCP dependency is present.
- Claims, metrics, dates, screenshots, and comparisons trace to provided or fetched sources, or are marked `待确认`.

## Outputs

Produce one or more of:

- slide outline
- storyboard
- self-contained HTML deck
- visual redesign notes
- deck critique
- speaker notes
- appendix structure
- print/PDF readiness checklist
- source and caveat list

## Recovery

If the requested deck is too broad, produce a concise outline and the first production-ready section, then list what is needed to finish the rest. If the user asks for a PPTX or PDF but only this Skill is active, create the HTML deck and state that conversion/export must be handled by the visible XAgent tools or an approved Office/PDF workflow.

If the source material is weak, build a structure with clearly labeled gaps. If visual assets are missing, use text, CSS, native SVG diagrams, or clearly marked placeholders rather than remote stock imagery.

## Boundary

Skill owns deck narrative, slide structure, HTML slide implementation rules, visual craft guidance, accessibility checks, print behavior, and offline validation checklist.

It does not own XAgent tool schemas, ToolResult fields, runtime path selection, file permissions, artifact lifecycle, browser automation, image generation, Office conversion, PDF/PPTX export, deployment, or final factual authority for unverified claims. It must not run shell, Python, Node, npm, pnpm, yarn, curl, MCP, browser-open, local server, package install, deploy, publish, Figma, image generation, PPTX export, PDF export, or document-export commands by itself; those actions belong to XAgent tools visible in the current session and require the current task context.

## Resources

- `references/deck-rules.md`: slide structure, fixed-stage layout, navigation, print/PDF, speaker notes, data visualization, and validation rules.
- `references/design-craft.md`: visual quality rules adapted from Open Design craft guidance.
- `LICENSE`: source and license notice.
