---
name: claude-design-production-architect
description: Production-grade implementation workflow for Claude Design exports, handoff ZIPs, screenshots, or HTML/CSS/JSX prototypes. Use when the user wants to create a Claude Design prompt, convert Claude Design files into React/TypeScript, implement a design into a complex app/backend, wire AI-powered features safely, audit responsive/layout problems, or detect and repair AI-slop/prototype-only design patterns. Builds on claude-design-handoff by adding converter-assisted inventory, backend/AI contract discovery, responsive breakpoint triage, design issue repair, and strict verification gates.
---

# Claude Design Production Architect

Use this skill as the deeper layer on top of `$claude-design-handoff`. The baseline handoff skill teaches how to read Claude Design bundles and recreate visual fidelity. This skill adds the missing production work: feature-agnostic handoff generation, backend and AI wiring discovery, responsive repair, design-quality triage, and converter-assisted HTML/CSS/JSX inventory.

## Operating Rule

Recreate the design output, not the prototype internals. Claude Design files are usually HTML, CSS, and browser-loaded JSX. Treat them as a visual and structural source, then build typed React/TypeScript using the target repo's routing, data, permissions, styling, and AI conventions.

## Workflow

1. Load the baseline context.
   - If the existing `$claude-design-handoff` skill is available, apply its Phase 0 to Phase 6 workflow first.
   - Then apply this skill's stricter production pass.

2. Identify the work type.
   - Creating a new Claude Design prompt: use `assets/CLAUDE_DESIGN_PRODUCTION_HANDOFF_PROMPT.md`.
   - Implementing a handoff ZIP/folder: run the scanner, read all source files, inspect the repo, then plan.
   - Auditing an implementation: compare the shipped code against the scanner report, handoff files, and repo contracts.

3. Run converter-assisted inventory, not blind conversion.
   - Use `scripts/analyze-claude-design.mjs` on an extracted design folder:
     `node <base_dir>/scripts/analyze-claude-design.mjs <design-folder> --out <report.md>`
   - If the user only supplied a ZIP, extract it into a temporary workspace first.
   - Use converter ideas from the attached resources as aids:
     - `html-react-parser`: useful for AST walking, `replace`, `domToReact`, and attribute-to-prop translation.
     - `html-to-react-components`: useful when markup is annotated with `data-component`; its TypeScript output is a draft, not production.
     - BeautifulSoup/Python converters: useful for recursive HTML inventory, asset gathering, and route-like page grouping.
   - Do not ship generated converter output without rewriting it into the repo's component/data/style patterns.

4. Build four inventories before editing.
   - Source inventory: primary HTML, imported JSX/JS/CSS, assets, screenshots, markdown handoff docs.
   - Prototype drop-list: CDN React, Babel, `text/babel`, `window.*`, tweak panels, hidden editor controls, hardcoded fixtures, global CSS ownership.
   - Component inventory: page sections, repeated primitives, charts, forms, tables, modals, drawers, AI actions, empty/error/loading views.
   - Data inventory: fixtures, generated copy, metrics, statuses, permissions, evidence/citations, backend candidates, unknown fields.

5. Classify the feature archetype.
   - Public page, dashboard, admin control plane, wizard, editor, data table, report, AI generation flow, messaging workflow, financial/deal/portfolio surface, media/content surface, settings/security surface, or hybrid.
   - Load only the domain rules that apply. In HypeStake, high-trust finance, deal, creator genome, portfolio, contracts, and admin rules override generic design preferences.

6. Repair design issues during implementation.
   - Responsive risks: fixed desktop widths, brittle multi-column grids, nowrap labels, hidden overflow, chart label collision, sticky/fixed overlap, non-touch controls, missing mobile action placement.
   - AI-slop patterns: generic "AI insights" panels with no source, fake confidence, hallucinated logos/metrics, nonfunctional controls, hero-plus-random-cards layouts, unlabeled charts, decorative gradients replacing data, repeated cards with no information hierarchy.
   - Production risks: hardcoded demo data, missing loading/empty/error/permission states, fake backend endpoints, direct LLM calls from UI, unscoped CSS, secret/env leakage, missing asset manifest.
   - Record repairs in a design issue log or final implementation notes.

7. Discover the live codebase before editing.
   - Read package scripts and lockfile to infer package manager.
   - Locate router/shell, design system/tokens, shared components, data hooks, generated types, API clients, edge functions, jobs, auth/permission helpers, and existing tests.
   - Do not infer routes, table names, backend function names, environment variables, or model/provider names.
   - For HypeStake, start from `docs/codebase-wiki/index.md` and `CLAUDE.md` when present, and preserve Supabase/Trigger/AI routing conventions.

8. Convert in vertical slices.
   - Tokens and design primitives first.
   - Typed view models and fixtures second.
   - Page/shell integration third.
   - One P0 section with loading, empty, error, degraded, permission, and success states fourth.
   - Then expand section by section, keeping data adapters and UI separate.

9. Wire backend and AI only through existing seams.
   - Map every visible value to a confirmed source, a typed derived value, or `UNKNOWN_UNTIL_CODEBASE_DISCOVERY`.
   - AI actions must define required input, output schema, loading/partial/error/degraded states, user review requirements, persistence, and retry behavior.
   - Do not add direct model calls, new queues, new migrations, RLS changes, or prompt DB changes unless the user explicitly scopes backend work.

10. Verify before final.
   - Run the strongest relevant repo checks: typecheck, lint, tests, build.
   - Run forbidden-pattern greps:
     `rg "window\\." src`
     `rg "text/babel|unpkg.com|cdn.tailwindcss.com|@babel/standalone" src`
     `rg "tweaks-panel|prototype-only|reference-only" src`
     `rg "TODO: invent|TODO: backend" src`
   - For UI work, verify desktop, tablet, and mobile. Use browser screenshots when a local app can run.
   - Document pre-existing failures separately from introduced issues.

## Output Expectations

For implementation work, final responses should include changed files, behavior changed, checks run, known risks, and what was intentionally not touched. For handoff prompt creation, provide the generated prompt file and the plugin/package path.

