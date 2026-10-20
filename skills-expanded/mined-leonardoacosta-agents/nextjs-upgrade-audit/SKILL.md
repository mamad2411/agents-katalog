---
name: nextjs-upgrade-audit
description: >
  Audits a Next.js app's observable repo state — package.json, next.config.*,
  turbo.json, CI config, and the app tree — against a Next.js 16.2/16.3
  capability matrix, and emits ranked findings with concrete fixes. Use when
  asked to review a Next.js upgrade, audit a repo for unclaimed new-feature
  wins, check for stale or superseded config flags (prefetchInlining,
  unstable_catchError, middleware.ts), or evaluate whether
  cacheComponents/Turbopack/Instant Navigations adoption is available and
  unclaimed. NOT a Next.js documentation mirror — next dev on 16.3+ already
  writes version-matched docs into the project's own node_modules/AGENTS.md;
  this skill only reasons about this repo's delta against that. Triggers on:
  next.config audit, turbopack audit, cacheComponents, partialPrefetching,
  unstable_catchError, unstable_retry, middleware.ts vs proxy.ts,
  turbopackFileSystemCacheForBuild, --webpack flag, Next.js upgrade review,
  "is our app using Next.js's new features".
allowed-tools: Read, Glob, Grep, Bash
---


# Next.js Upgrade Audit

> Repo-state differ for Next.js 16.2/16.3 feature adoption — not a docs mirror.
> Load with: `@skill nextjs-upgrade-audit`

## Why this skill isn't a docs mirror

Next.js 16.3+ makes `next dev` write a version-matched `AGENTS.md` block pointing at the docs
bundled in the project's own `node_modules`, and the vendor retired its earlier Skills that
existed solely to bring current documentation to an app. Mirroring framework docs here would be
redundant on day one and rot on every minor release. What bundled docs *can't* tell an agent is
**this repo's delta** — what's configured, what's stale, what's sitting unclaimed. That delta is
the only thing this skill produces: repo-observable predicates, not documentation.

## Thinking Framework

1. **Anchor the version first.** Every check below is conditioned on a `next` version range
   (`>=16.2`, `>=16.3`). Read every `apps/*/package.json` (or the single root `package.json` in a
   non-monorepo) before running anything else — a check that fires against the wrong version is a
   false positive, not a finding.
2. **Route to first-party detectors — don't reimplement them.** See § Route to Vendor Tooling.
   Instant Insights, the `instant()` Playwright helper, and Vercel's own Cache Components
   migration skill exist and are maintained upstream; this skill audits *whether* a repo has
   adopted them, and never hand-rolls their function.
3. **Work tier by tier and report ranked, not raw.** Correctness/security first, then stale
   config, then available wins, then test-coverage gaps. A dump of every grep hit is not an audit
   — group by tier, cite the file (and line where practical), and pair every finding with its fix.
4. **State confidence explicitly.** Several checks are structurally unreliable from repo state
   alone (a CSP set at the edge/CDN is invisible to a repo grep). Say so in the finding — never
   present an inference as a settled fact.

## Route to Vendor Tooling (do not reimplement)

| Repo-observable need | Route to |
|---|---|
| Diagnosing *which* navigations are slow | Next.js DevTools **Instant Insights** panel (`next dev`) |
| Regression-proofing that a navigation stays instant | `instant()` helper from `@next/playwright` |
| Actually performing a `cacheComponents` migration | Vercel's first-party Cache Components migration skill |

This skill's job stops at *detecting* that these are missing or under-used — see § Test Coverage
in `references/test-coverage.md`.

## Load References

| Tier | Working on | Load |
|---|---|---|
| 1 — Correctness / security | Forfeited Turbopack line, inert cache config, CSP/SRI gaps, de-opted shared layouts | `references/correctness-and-security.md` |
| 2 — Stale config | Renamed APIs, superseded experimental flags, committed debug flags, no-op `no-store` | `references/stale-config.md` |
| 3 — Available wins | Unclaimed zero-config speedups, `cacheComponents`/`partialPrefetching`, TS7, build caching, root params | `references/available-wins.md` |
| 4 — Test coverage | Missing `instant()` regression guard, zero-Suspense routes, per-link prefetch anti-pattern | `references/test-coverage.md` |

## Worked Examples (Highlights From `references/`)

Three checks pulled in-body to show the shape every predicate follows — the full set with
severity, fix, and confidence caveats lives in `references/`.

**1. Highest-severity correctness check — the `--webpack` opt-out
(`references/correctness-and-security.md`).**

```bash
grep -E '"(dev|build)":.*--webpack' apps/*/package.json
```

If this matches on a repo running `next >= 16.3`, the app has opted out of Turbopack — the
*default* bundler since Next.js 16 — and forfeits the whole 16.3 line in one flag: up to 90% less
dev-server memory, up to 5.5x faster CI compile times, up to 22% more requests served under load,
and `import.meta.glob`. Severity: **high**. Fix: drop `--webpack` unless a named, current
incompatibility is documented next to the flag.

**2. Inert-config check — `cachedNavigations` without `cacheComponents`
(`references/correctness-and-security.md`).**

```ts
// next.config.ts — silent no-op without its dependency
experimental: { cachedNavigations: true }   // requires cacheComponents: true, not set
```

Next.js states this dependency explicitly — it isn't inferred. A repo shipping `cachedNavigations`
alone believes it has repeat-visit caching and does not. Severity: **medium** — not a security
hole, but a config a reader will trust and a reviewer won't catch without knowing the coupling.

**3. Low-confidence-by-construction check — "no CSP configured"
(`references/correctness-and-security.md`).**

```bash
grep -rEn "Content-Security-Policy" next.config.* middleware.ts proxy.ts 2>/dev/null
```

A miss here is **not** proof the app has no CSP — many deployments set CSP at the edge/CDN, which
a repo grep cannot see. Report as **low confidence** and phrase the finding as "no CSP found
in-repo," never as "this app has no CSP."

## Severity Legend

| Severity | Meaning |
|---|---|
| **High** | Forfeits a major capability line wholesale, or is a live security/correctness defect |
| **Medium** | Config is inert, stale, or misleading; no immediate outage but wrong behavior is trusted |
| **Low** | Unclaimed win or minor hygiene; report but don't block on it |
| *(confidence tag)* | Attached to any check whose predicate can't be fully confirmed from repo state alone |

## References

Load the tier(s) relevant to the audit at hand — each file is a flat checklist: predicate → how
to check → severity → fix → confidence caveat (where one applies).

- [correctness-and-security.md](references/correctness-and-security.md) — MANDATORY first pass
- [stale-config.md](references/stale-config.md)
- [available-wins.md](references/available-wins.md)
- [test-coverage.md](references/test-coverage.md)
