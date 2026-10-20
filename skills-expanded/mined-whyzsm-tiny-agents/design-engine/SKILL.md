---
name: design-engine
description: "Design engine expert-team router for UI/UX prototype delivery: requirement discovery, design system selection, brand extraction, design tokens, high-fidelity HTML prototypes, prototype templates, quality critique, anti-slop review, and HTML/PDF/PPTX/ZIP export. Coordinates discovery analysis, design systems, prototype building, critique review, and export delivery."
metadata:
  short-description: Design prototype expert team router
---

# Design Engine

Use this skill as the expert-team entry point for design prototype work. It converts the imported `design-engine` team package into the same lightweight router shape as `harmony-expert-team`: coordinate design capability paths instead of requiring the original plugin runtime, avatars, or member Markdown files.

Team mode: `internal-router-labels`. The role names below are internal capability labels handled inside `$design-engine`; they are not standalone `$discovery-analyst`, `$design-system-expert`, `$prototype-builder`, `$critique-reviewer`, or `$export-specialist` skills unless separate top-level packages are created later.

## Expert Roles

- `discovery-analyst`: requirement discovery through a five-dimension intake: surface, audience, tone, brand context, and scale.
- `design-system-expert`: design system selection, 71 brand-grade system matching, five visual directions, brand extraction, and design token generation.
- `prototype-builder`: high-fidelity HTML/CSS prototype generation for web pages, SaaS landing pages, dashboards, mobile app screens, decks, pricing pages, docs pages, blog posts, and email templates.
- `critique-reviewer`: five-dimensional design review, anti-slop checks, P0/P1/P2 issue gating, and actionable repair suggestions.
- `export-specialist`: approved prototype export to standalone HTML, PDF, PPTX, or ZIP with assets inlined or packaged.

## Routing

Classify the task before acting. Use these labels as internal routing paths within `$design-engine`, not as separate top-level skill invocations:

1. Use `discovery-analyst` when the user has a vague idea, needs design requirements clarified, or has not specified surface, audience, tone, brand context, or scale.
2. Use `design-system-expert` when the user asks for style direction, brand-grade visual language, design tokens, brand extraction, DESIGN.md, color palette, typography, component style, or a specific reference brand such as Stripe, Linear, Apple, Vercel, Notion, or Tesla.
3. Use `prototype-builder` when the main output is a high-fidelity HTML/CSS prototype, landing page, dashboard, mobile app flow, pricing page, docs page, blog post, deck, or email template.
4. Use `critique-reviewer` when the user asks to audit, polish, score, de-slop, quality gate, or review an existing design or generated prototype.
5. Use `export-specialist` when the task is to export an approved prototype to HTML, PDF, PPTX, or ZIP, inline assets, or prepare a handoff bundle.
6. For full design delivery, run the phased flow: discovery, design system selection, prototype build, quality review, revision if needed, export, and final handoff.

## Design-First Flow

When a task depends on a design idea, UI surface, brand, or target prototype:

1. Inspect the available design context before generating artifacts: surface, audience, tone, brand assets, reference systems, content scope, target format, and interaction requirements.
2. Ask only for missing information that blocks a useful next step. If the request is already clear, proceed with explicit assumptions.
3. Select the smallest useful role path. Do not run the full pipeline for a simple style recommendation, existing-design review, or export-only task.
4. For new prototypes, choose a design system or visual direction before writing HTML/CSS. Do not invent ungrounded visual styles.
5. Apply anti-slop guardrails: avoid generic AI gradients, fake metrics, emoji-as-icons, broken layouts, inaccessible contrast, and unresponsive screens.
6. For generated prototype files, prefer standalone HTML with inline CSS/SVG and no external CDN dependency unless the user explicitly asks otherwise.
7. If quality review finds P0 issues or any five-dimensional score below 3/5, revise before export when the user wants a finished deliverable.

## Delivery Checklist

For design prototype tasks, make sure the final work accounts for:

- Requirement summary: surface, audience, tone, brand context, scale, content, and constraints.
- Design system decision: selected system, visual direction, color tokens, typography, layout, components, cautions, and responsive behavior.
- Prototype structure: semantic HTML, CSS variables, realistic placeholder content, stable responsive layout, hover/focus states, and no external resource dependency by default.
- Quality gate: philosophy, hierarchy, execution, specificity, restraint, P0/P1/P2 issues, and repair notes.
- Export package: target format, file path, asset handling, browser or viewer assumptions, and usage notes.

## Output Style

- Be explicit about which design expert path you selected and why.
- Separate confirmed design facts from assumptions and recommendations.
- When creating files, summarize generated files, validation commands, and remaining risks.
- When answering without files, keep the response concrete and design-specific; use compact tables for design system comparisons and review reports.
