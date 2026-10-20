---
name: react-nextjs-quality-security
description: "Harden React/Next apps across CSP, auth, runtime config, accessibility, performance, and CI."
---

# React Next.js Quality Security

Assess or implement React 19 and Next.js quality, security, performance, accessibility, tests, CI, runtime config, and production-readiness concerns.

## Process

1. Inspect changed routes/components, security boundaries, auth/session model, env strategy, dependencies, tests, CI, and deployment target.
2. Use `itsol-current-tech-context` for version-sensitive Next.js, React Compiler, Tailwind, testing, security header, or package behavior.
3. Treat frontend code as public and all browser/API/form/storage/query-param data as untrusted.
4. Verify server-side authorization, CSP/header strategy, safe env separation, cache cleanup, UI states, keyboard behavior, bundle impact, and production build behavior where relevant.
5. For large PRs, split review with `security-frontend-browser-review`, `ui-code-review`, `ui-performance-stability`, and `ui-frontend-testing-qa` subagents.

## Coordination

Use with `react-nextjs-review`, `react-nextjs-debugging`, `ui-code-review`, `security-frontend-browser-review`, `security-auth-session-review`, `security-authz-tenant-review`, `security-supply-chain-review`, and `infra-production-readiness-review`.

## Focused References

- [01-security-and-runtime-config.md](./references/01-security-and-runtime-config.md) - Security And Runtime Config
- [02-ux-performance-stability.md](./references/02-ux-performance-stability.md) - UX Performance And Stability
- [03-tests-ci-definition-of-done.md](./references/03-tests-ci-definition-of-done.md) - Tests CI And Definition Of Done
