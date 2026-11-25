---
name: design-system
description: Use when starting a frontend or working on its look and feel, to establish and enforce a DESIGN.md-driven custom design system as the single source of truth for tokens, components, and icons. Make any generated UI (including 21st.dev Magic output) conform to DESIGN.md.
---

# Design System

**Announce at start:** "I'm using claude-engineer:design-system to make DESIGN.md the source of truth."

## Iron Law
**DESIGN.md is the single source of truth.** No component ships with off-token colors, spacing, type,
or radii. Tools generate; DESIGN.md governs.

## Procedure
1. **Author `DESIGN.md`** (Google design.md spec) at the frontend root - YAML token front-matter
   (colors, typography, spacing, radii, elevation, components) + markdown sections (Overview, Colors,
   Typography, Layout, Elevation, Shapes, Components, Do's/Don'ts). Optionally **seed from a getdesign.md
   kit** matching the desired vibe, then customize to the brand.
2. **Wire tokens into the stack** - export DESIGN.md tokens to Tailwind/CSS variables and consume them
   everywhere (Tailwind v4 `@theme`, OKLCH, class-based dark mode). See `claude-engineer:frontend-development`.
3. **Generate components** with shadcn/ui + Radix and/or 21st.dev Magic, then **run the conformance loop**:
   generate → audit against DESIGN.md tokens → refine until on-token. Magic ignores your DESIGN.md, so the
   audit/refine step is mandatory.
4. **Icons** - default to Lucide (or Phosphor); add bespoke icons via a typed SVG-component pattern; use
   Magic `logo_search` for brand logos.
5. **Validate** - run the design.md linter (`@google/design.md` → `lint`) including the contrast rule
   (WCAG AA 4.5:1); use `diff` to catch token regressions across iterations.
6. **Register patterns** - record established component/token patterns in `docs/conventions.md` so they're reused.

## Tooling (BYO keys; install per `templates/recommended-mcps.md`)
- Google design.md CLI: `npm i -D @google/design.md` → `lint` / `diff` / `export` / `spec`.
- designmd (getdesign.md) MCP: `claude mcp add -s user designmd -e DESIGNMD_API_KEY=dk_... -- npx designmd-mcp` (browse/search keyless; download needs the key).
- 21st.dev Magic MCP: `npx @21st-dev/cli@latest install claude --api-key <key>`.

**Full detail:** read `references/design-tooling.md` (exact spec sections, MCP tool names, the conformance loop, pricing) on demand.

## Red flags - STOP
- Hardcoded hex/px in a component instead of a token → fix to token.
- Shipping Magic output without the audit/refine pass.
- Skipping the contrast lint (fails WCAG AA gate later).
