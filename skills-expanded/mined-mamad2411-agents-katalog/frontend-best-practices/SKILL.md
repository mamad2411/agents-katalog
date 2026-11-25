---
name: frontend-best-practices
description: Frontend development best practices for building and reviewing user-facing UI across web, mini-program, and app surfaces with fewer rework loops. Use when creating, changing, polishing, or reviewing frontend interfaces, especially async buttons, forms, modals, drawers, tables, filters, uploads, dashboards, admin tools, responsive layouts, loading/error/empty/success states, accessibility, UX copy, visual polish, platform-specific interaction, or validation decisions. Also use when the user mentions frontend best practices, repeated rework, duplicate clicks, 防重复提交, 不好看, 返工, 状态不完整, 小程序, app 端, or wants UI quality checked before handoff.
---

# Frontend Best Practices

Use this skill as a frontend quality gate before handoff. The goal is to reduce the loop where the agent implements a UI, the user clicks through it, finds predictable interaction gaps, and the agent patches them afterward.

## Core Workflow

1. Classify the surface and intent.
   - Platform surface: identify whether the target is web, mini-program, native/hybrid app, or a mixed wrapper before choosing interaction constraints or validation.
   - Product/admin/dashboard/tool UI: prioritize restrained utility, information density, predictable controls, and stable workflows.
   - Brand/landing/portfolio/game UI: use stronger visual direction, but still preserve interaction completeness.
   - Narrow bug or polish request: keep the existing product shape unless the user asks for a redesign.
   - "Looks bad" or "average" feedback: treat it as a direction or taste problem, not just a CSS tweak.

2. Read local context before designing.
   - Inspect nearby screens, shared components, design tokens, form/table/request helpers, permissions, route patterns, and validation/build scripts.
   - Prefer existing components, idioms, and project rules over new abstractions.
   - If present, use project taste/context files such as `PRODUCT.md`, `DESIGN.md`, `AGENTS.md`, or local style docs.

3. Implement with complete states.
   - Any async write action needs both visual feedback and a method-level re-entry guard.
   - Do not rely only on a disabled button; protect the handler too.
   - Preserve usable content during refreshes when possible. Avoid sudden page-level dimming for local or fast operations.

4. Review before handoff.
   - Check state completeness, edge cases, responsiveness, copy, accessibility, performance, and project fit.
   - Validate at the lightest layer that can catch the likely regression; use a real browser for complex interaction or responsive behavior.

## Reference Routing

- Read [workflow.md](references/workflow.md) at the start of substantial frontend work or when choosing validation scope.
- Read [platform-surfaces.md](references/platform-surfaces.md) when the target may be web, mini-program, app, mobile-first, cross-platform, or when choosing platform-specific validation.
- Read [interaction-states.md](references/interaction-states.md) when touching buttons, forms, tables, modals, drawers, uploads, filters, async requests, optimistic UI, permissions, or list refreshes.
- Read [product-ui-taste.md](references/product-ui-taste.md) for admin/product tools, dashboard UI, RuoYi-style systems, visual polish, Chinese product copy, or user taste alignment.
- Read [review-checklist.md](references/review-checklist.md) before final handoff, and whenever the user asks for a review or audit.

## Hard Defaults

- Prefer local, scoped loading states over full-page overlays unless the whole page is genuinely blocked.
- For writes, use `submitting`/`pending`/row-action locks, set them before the request can race, and release them on every failure, validation-cancel, and success path.
- Prevent stale read responses from overwriting newer UI state when filters, pagination, tabs, or route params can change quickly.
- Treat empty states, no-result states, permission states, long CJK text, slow networks, API errors, and duplicate user actions as normal production paths.
- Keep admin/product UI restrained: no marketing hero, decorative gradients, card-on-card layouts, or novelty interactions unless the product context calls for them.
- When reviewing, lead with findings and file references. When implementing, finish with changed surfaces, validation performed, and any residual risk.
