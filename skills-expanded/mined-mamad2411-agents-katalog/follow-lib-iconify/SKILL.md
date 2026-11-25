---
name: follow-lib-iconify
description: Use @iconify-json/* icon sets — Iconify API, offline bundles, on-demand loading
argument-hint: "[target-or-scope]"
related:
  - follow-lib-unocss
  - run-verify
  - run-test

---

## Goal

Use @iconify-json/* icon sets — Iconify API, offline bundles, on-demand loading

## Scope

Use when the task involves Iconify — icon components, `@iconify-json/*` offline data, on-demand loading (lib iconify)

- Use this skill to choose/install icon components and icon data — for deep UnoCSS `presetIcons` integration do `/follow-lib-unocss` instead
- Tailwind v3 uses `@iconify/tailwind`; Tailwind v4 uses `@iconify/tailwind4`
- Optimize bundle (offline bundles, subsetting, lazy loading) → `workflows/optimize-icons/SKILL.md`
- If the project uses very few icons and wants no dependency → consider inline SVG instead

- Latest: `@iconify/react@6.0.2` / `@iconify/vue@5.0.3` / `iconify-icon@3.0.3` (web component) / `@iconify/tailwind@1.2.0` / `@iconify/tailwind4@1.2.3` (verified 2026-09-24)
- References: [apis](references/apis.md) 
## Execute

### Workflows

| Topic | Workflow |-------|----------| Setup | `workflows/setup-iconify/SKILL.md` — install + usage patterns per framework | Optimize | `workflows/optimize-icons/SKILL.md` — offline bundles, on-demand loading, subsetting 
### 1. Setup And Usage

> Goal: use correctly per the official docs

1. Use `@iconify-json/<set>` (e.g. mdi, lucide) with UnoCSS `presetIcons`, the Tailwind `@iconify/tailwind` plugin, or an icon component
1. Use the component matching the framework: `@iconify/react`, `@iconify/vue`, `@iconify/svelte`, or the `iconify-icon` web component for framework-agnostic
1. Pick the icon set by design: mdi (material), lucide (minimal), tabler
1. Use on-demand loading — bundle only the icons actually used; use `@iconify/utils` when generating icon data yourself
1. For custom icons, use `customizations` or inline SVG instead

### 2. Verify

> Goal: verify correct usage

1. Run `/run-verify` for lint, typecheck
2. Run `/run-test` if related tests exist
3. Check the latest official docs before using an uncertain API (lib iconify)

## Rules

- Never import a whole icon set — always use per-icon
- Set `size`/`color` via props/class, don't hardcode them in the SVG
- Use the iconify API runtime only for dynamic icons — bundle static icons directly

- Use `/follow-lib-unocss` if deep UnoCSS `presetIcons` config is needed
- Use `/run-verify` if needed
- Use `/run-test` if needed
- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The library is used correctly per best practices (lib iconify)
- No known security/performance pitfalls (lib iconify)
- Lint, typecheck, tests pass
