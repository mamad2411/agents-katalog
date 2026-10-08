---
description: Always-on workspace policy; canonical instructions live in AGENTS.md
alwaysApply: true
---

# Workspace instructions

Follow **[AGENTS.md](../../AGENTS.md)** at the repository root for all product, engineering, collaboration, and **MCP** defaults (including Context7 via `resolve-library-id` then `query-docs`).

Do not contradict `AGENTS.md`. Blog 3.0 ticket → code map: **[docs/blog-3-jira-conventions.md](../../docs/blog-3-jira-conventions.md)**. If something tool-specific is needed, keep it minimal here and expand only in `AGENTS.md`.

**Before building, read the ADRs.** Decisions are tool-agnostic and live in the register at **[docs/adr/README.md](../../docs/adr/README.md)** (e.g. ADR-005 component organization, ADR-006 design tokens) — the *same* canon Claude Code follows. Using Cursor never changes the rules; if a task would contradict an ADR, stop and flag it rather than diverging. See `AGENTS.md` § "Decision compliance".

## Preserve shared UI primitives (no preemptive changes)

- **Do not edit** existing components under [`packages/ui/src/components`](packages/ui/src/components) (e.g. button, badge, dropdown-menu) except when fixing a confirmed bug you were explicitly asked to fix.
- **Do not change** [`packages/ui/src/globals.css`](packages/ui/src/globals.css) or [`apps/www/src/app/globals.css`](apps/www/src/app/globals.css) for new features: no new tokens, `@theme` tweaks, or drive-by restyling.
- **Allowed exception:** **add** new primitive files only when required (e.g. `navigation-menu.tsx` from the shadcn CLI)—additive files only; leave existing primitive source unchanged.
- Prefer fixing layout or one-off styling in **app or block code** (e.g. `apps/www/src/components/shadcn-studio/blocks/…`, page components) using existing tokens and arbitrary `className` values where needed—not by changing the shared design system.
- **Do not change** global shell layout (e.g. root `layout.tsx`, existing navbar blocks) unless the task explicitly asks for it.
