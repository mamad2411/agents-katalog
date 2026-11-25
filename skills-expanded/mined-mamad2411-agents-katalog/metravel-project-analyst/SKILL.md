---
name: metravel-project-analyst
description: "Map metravel repository structure, active features, dependencies, validation surfaces, and risk hotspots. Use for read-only onboarding or broad scope analysis before larger work."
---

# Metravel Project Analyst

Use this skill for read-only project analysis before larger changes, onboarding, risk mapping, or multi-agent handoff. Do not edit code or docs while acting as this role.

`AGENTS.md` is inherited. Start with `package.json` and repository structure.
Load `docs/README.md`/`docs/INDEX.md`, feature docs, testing, release, or exact
`docs/RULES.md` headings only when the requested analysis needs them.

## What To Inspect

- App shape: routes, screens, reusable UI, hooks, services, API clients, utilities, tests, scripts, and deployment files.
- Platform shape: shared Expo/React Native code, desktop/mobile web adapters,
  Android and active iPhone files, native modules/config boundaries, and
  available browser/Android-USB/iPhone validation.
- Localization shape: locale registry, RU/BE/UK/PL/EN resources, web/native
  runtime split, formatting helpers, UI-literal governance, and i18n tests.
- Active feature areas and existing feature maps.
- High-risk contracts: external links, image/media rendering, design tokens, auth/e2e secrets, server paths, release and caching rules.
- Validation surface: targeted checks, fast/preflight checks, governance scripts, Jest, Playwright, production build, Lighthouse.
- Risk hotspots: oversized files, duplicated logic, stale docs, missing tests, fragile web/mobile differences, dead code, or known blockers.

## Output Contract

Return one compact artifact:

```md
## Project Analysis

Scope:
Project shape:
Active feature areas:
Platform impact:
Localization impact:
Validation map:
Risk hotspots:
Recommended agents/skills:
Suggested next steps:
Blockers / unknowns:
```

## Rules

- Stay read-only unless the user explicitly asks to update docs or code after the analysis.
- Prefer evidence from files, commands, and docs over broad guesses.
- Do not create one-off reports by default; summarize in the handoff unless the user asks for a persistent doc.
- If the analysis discovers a concrete bug in scope, route it to `$metravel-feature-builder` or `$metravel-qa-agent` instead of silently folding it into generic debt.
