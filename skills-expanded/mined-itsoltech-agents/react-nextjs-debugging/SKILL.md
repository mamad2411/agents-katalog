---
name: react-nextjs-debugging
description: "Debug React/Next rendering, hydration, App Router, cache, auth, bundles, and performance."
---

# React Next.js Debugging

For bugfix authorization and plan prerequisites, defer to `itsol-workflow-mode`; retain evidence, root-cause analysis, proportionate verification, and final review in every mode.

Debug React 19 and Next.js issues by isolating whether the failure belongs to server render, client render, hydration, App Router, API, cache, auth, CSS, bundle, runtime config, or deployment mode.

## Process

1. State expected behavior, actual behavior, impact, affected route/component, environment, and smallest reproducible symptom.
2. Gather evidence from browser console, terminal logs, Network tab, request ids, telemetry, tests, build output, generated API output, config, and package versions before proposing a fix.
3. Use `itsol-current-tech-context` when symptoms depend on React, Next.js, TanStack Query, Hey API, browser APIs, or package versions.
4. Isolate one failing boundary and compare with a known working path.
5. Write or update a regression test when repo policy supports it; otherwise document replacement verification.
6. Use `itsol-bug-debugging`; in `governed`, require an approved Technical Fix Plan before implementation, while autonomous/direct prerequisites come from `itsol-workflow-mode`.

## Coordination

Use with `react-nextjs-app-router-rendering`, `react-nextjs-api-cache-forms`, `react-nextjs-quality-security`, `security-frontend-browser-review`, and `ui-frontend-testing-qa`.

## Focused References

- [01-triage-rendering-hydration.md](./references/01-triage-rendering-hydration.md) - Triage Rendering And Hydration
- [02-api-auth-runtime.md](./references/02-api-auth-runtime.md) - API Auth And Runtime
- [03-ui-performance-fix-discipline.md](./references/03-ui-performance-fix-discipline.md) - UI Performance And Fix Discipline
