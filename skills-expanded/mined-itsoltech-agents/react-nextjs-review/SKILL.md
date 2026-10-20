---
name: react-nextjs-review
description: "Review React/Next rendering, App Router, cache, forms, security, accessibility, and tests."
---

# React Next.js Review

Review React 19 and Next.js changes for behavior, rendering boundaries, API/cache correctness, browser security, accessibility, performance, test evidence, and deployment risk.

## Process

1. Inspect the diff, package versions, route structure, generated code, configs, tests, and surrounding conventions before applying checklist items.
2. Use `itsol-current-tech-context` for findings that depend on React, Next.js, TanStack Query, Hey API, Tailwind, testing tools, or runtime versions.
3. Build a coverage map: architecture, Server/Client Component boundary, data fetching, cache, API contract, forms, auth/permissions, security, UI states, accessibility, performance, tests, CI, and deployment.
4. Lead with concrete findings by severity, file reference, affected behavior, and required fix or verification.
5. Separate confirmed defects from risks, questions, and non-blocking improvements.

## Large PR Subagent Review

For large or multi-area React/Next pull requests, subagent review is mandatory before the final verdict. Split by pragmatic risk area such as App Router/rendering, API/cache/forms, UI/UX, browser security, performance/bundle, generated OpenAPI client, tests/QA, or deployment/runtime config.

The main agent consolidates subagent findings, removes duplicates, resolves conflicts, decides final severity, and reports remaining coverage gaps.

## Coordination

Use with `itsol-code-review-workflow`, `react-nextjs-app-router-rendering`, `react-nextjs-api-cache-forms`, `react-nextjs-quality-security`, `ui-code-review`, `security-frontend-browser-review`, and `hey-api-openapi-review` as relevant.

## Focused References

- [01-review-coverage-and-findings.md](./references/01-review-coverage-and-findings.md) - Review Coverage And Findings
- [02-architecture-and-rendering.md](./references/02-architecture-and-rendering.md) - Architecture And Rendering
- [03-api-security-ux-tests.md](./references/03-api-security-ux-tests.md) - API Security UX And Tests
