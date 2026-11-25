---
name: perf-ci-gates
description: Set up the CI quality gates for an Astro 7 site on Cloudflare Workers — Lighthouse CI for Core Web Vitals and resource-weight budgets, and Biome as the single lint and format gate, wired into GitHub Actions; the workflow also hosts the axe job from a11y-deep. Use when adding performance budgets, gating pull requests on Lighthouse scores, wiring LHCI into CI, configuring Biome checks, or building a ci.yml. Covers serving the build for collection (staticDistDir on dist/client, or astro preview for SSR routes), the lighthouserc.json assertion shape with TBT as the lab proxy for INP, regression lab budgets versus field thresholds, and Biome with prettier-plugin-astro. Trigger on Lighthouse CI, performance budget, gate PRs on Core Web Vitals, LHCI in GitHub Actions, Biome CI, or biome ci. Gates and thresholds only — the a11y 0.95 floor is a cheap tripwire, full WCAG discipline is a11y-deep; producing lighter images and video is media-optimization; animation weight is motion-system; deep SEO is seo-aeo-schema.
---

# Performance and Code-Quality CI Gates for Astro on Cloudflare

> Two independent gates in GitHub Actions for an Astro 7 plus Cloudflare Workers site. Lighthouse CI catches Core Web Vitals and resource-weight regressions before merge; Biome gates lint, format, and import order. Lighthouse CI is a pre-merge regression gate on stable lab signals, not the source of truth for real-user Core Web Vitals, which come from field monitoring.

## TL;DR
- Run two parallel jobs in one ci.yml: a quality job (`biome ci`) and a lighthouse job (build, then LHCI collect, assert, upload). Make both required status checks for merge.
- Collect with `staticDistDir` pointed at `./dist/client`. The Cloudflare adapter defaults to `output: 'server'`, so client assets land in `dist/client`, not `dist`. Use `astro preview` only when on-demand (SSR) routes must be audited.
- Lighthouse cannot measure INP in the lab. Gate Total Blocking Time as the INP proxy. LCP, CLS, FCP, Speed Index, and TTI are lab-measurable.
- Lab budgets are regression-oriented, not the field thresholds. The official field Core Web Vitals are unchanged: LCP 2.5s, INP 200ms, CLS 0.1 at the 75th percentile. The claim that Google tightened LCP to 2.0s in 2026 is false; do not encode 2.0s.
- Biome is the single lint and format tool. Its Astro template support is still experimental, so ship the experimental flag off, disable Biome's formatter for `.astro`, and let prettier-plugin-astro format templates. Biome owns JS, TS, CSS, and JSON.
- Critical caveats, repeated under Limitations: set `fetch-depth: 20` or more (shallow clones break LHCI ancestor detection), run `numberOfRuns: 5` (single runs are flaky), and pin Biome with `--save-exact`.

## Reference materials — load when relevant

This SKILL.md is the verdict, the two-gate split, and the minimal recipe. Load a reference only when its condition is met:

- references/lighthouse-config.md — load when writing lighthouserc.json or budget.json, choosing the collection target, or tuning assertions, presets, and run count.
- references/github-actions-workflow.md — load when writing or debugging the ci.yml, wiring branch protection and status checks, caching, or report output and PR comments.
- references/biome-setup.md — load when writing biome.json, deciding the Astro template-formatting split, wiring `biome ci`, or adding prettier-plugin-astro.
- references/budgets-and-thresholds.md — load for the Core Web Vitals field thresholds, the lab proxies, and the recommended regression-oriented lab budget tables.

## Architecture — two gates, one workflow

The gates are independent and run in parallel. The quality gate is fast and cheap and fails first on a typo; the lighthouse gate is heavier because it builds and runs a browser. Keeping them as separate jobs means a lint failure does not consume a Lighthouse run, and each reports its own status.

| Gate | Tool | What it blocks |
|---|---|---|
| Performance | Lighthouse CI via treosh/lighthouse-ci-action | Core Web Vitals lab regressions (LCP, TBT, CLS), category-score drops, and resource-weight budget overruns |
| Code quality | Biome (`biome ci`) | lint violations, format drift, and unsorted imports across JS, TS, CSS, JSON |

Deep SEO and schema work belongs to the seo-aeo-schema skill, and deep accessibility plus reduced-motion belongs to the motion and visuals skills. This gate asserts only coarse Lighthouse category floors (performance and accessibility as errors, best-practices and SEO as warnings) so gross regressions fail the build without duplicating those skills.

## The two forks that shape the setup

### Collection target

Point LHCI at the built static files with `staticDistDir: ./dist/client`. This is the most reproducible path for a mostly-static site: LHCI serves the files itself, no Cloudflare runtime needed. It does not replicate the adapter's immutable cache headers, which is fine because the gate measures regressions, not production cache behavior.

Use `collect.startServerCommand` with `astro preview` only when on-demand (SSR) routes must be audited. In Astro 7 with `@astrojs/cloudflare` v14, `astro preview` runs on the real Cloudflare workerd runtime, so it is the production-parity path, but it is heavier and slower in CI. Do not set an absolute `site` plus `base` on the audited build: the Cloudflare build writes assets to `dist/client` without the base prefix, so they 404 when LHCI serves from a localhost port. See references/lighthouse-config.md.

### Runner

Use treosh/lighthouse-ci-action@v12. It is GitHub-Actions-native, stores reports as Actions artifacts plus temporary-public-storage in one step, and needs no GitHub App. It consumes the same lighthouserc.json as the CLI, so there is no lock-in: switching to raw `lhci autorun` later reuses the config unchanged. Raw `lhci autorun` is viable but needs the LHCI GitHub App installed to set PR status, which is more setup, not less. See references/github-actions-workflow.md.

## Minimal recipe

### 1. Install

```bash
npm install --save-dev --save-exact @biomejs/biome@2.5.8
npm install --save-dev prettier prettier-plugin-astro
# @lhci/cli is pulled by the treosh action; install it locally only for `lhci` runs
```

### 2. lighthouserc.json

```json
{
  "ci": {
    "collect": {
      "staticDistDir": "./dist/client",
      "numberOfRuns": 5
    },
    "assert": {
      "preset": "lighthouse:no-pwa",
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "categories:accessibility": ["error", { "minScore": 0.95 }],
        "categories:best-practices": ["warn", { "minScore": 0.9 }],
        "categories:seo": ["warn", { "minScore": 0.9 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "total-blocking-time": ["error", { "maxNumericValue": 300 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "first-contentful-paint": ["warn", { "maxNumericValue": 2000 }],
        "speed-index": ["warn", { "maxNumericValue": 3400 }],
        "interactive": ["warn", { "maxNumericValue": 3800 }]
      },
      "budgetsFile": "budget.json"
    },
    "upload": { "target": "temporary-public-storage" }
  }
}
```

The metric values above are regression ceilings for mobile, not Google field thresholds. Calibrate them to the site's current measured values (start around 110 to 115 percent of current, then ratchet down). See references/budgets-and-thresholds.md.

### 3. budget.json

Sizes are in kilobytes (LHCI assertion `maxNumericValue` uses bytes, but budget.json uses kilobytes).

```json
[
  {
    "path": "/*",
    "resourceSizes": [
      { "resourceType": "script", "budget": 150 },
      { "resourceType": "stylesheet", "budget": 60 },
      { "resourceType": "image", "budget": 400 },
      { "resourceType": "font", "budget": 100 },
      { "resourceType": "total", "budget": 800 }
    ],
    "resourceCounts": [
      { "resourceType": "third-party", "budget": 5 },
      { "resourceType": "total", "budget": 30 }
    ]
  }
]
```

### 4. biome.json

Flag off, Biome formatter disabled for `.astro` so it does not fight prettier, the false-positive-prone rules turned off for component files.

```json
{
  "$schema": "https://biomejs.dev/schemas/2.5.8/schema.json",
  "files": { "ignoreUnknown": true, "includes": ["**", "!**/dist", "!**/.astro"] },
  "assist": { "actions": { "source": { "organizeImports": "on" } } },
  "linter": { "enabled": true, "rules": { "recommended": true } },
  "formatter": { "enabled": true, "indentStyle": "space" },
  "overrides": [
    {
      "includes": ["**/*.astro", "**/*.svelte", "**/*.vue"],
      "formatter": { "enabled": false },
      "linter": {
        "rules": {
          "style": { "useConst": "off", "useImportType": "off" },
          "correctness": { "noUnusedVariables": "off", "noUnusedImports": "off" }
        }
      }
    }
  ]
}
```

Add prettier for the templates Biome leaves alone:

```json
// .prettierrc.json
{ "plugins": ["prettier-plugin-astro"], "overrides": [{ "files": "*.astro", "options": { "parser": "astro" } }] }
```

### 5. package.json scripts

```json
{
  "scripts": {
    "lint": "biome check",
    "format": "biome format --write && prettier --write \"**/*.astro\"",
    "ci:biome": "biome ci --reporter=github"
  }
}
```

### 6. ci.yml

A minimal two-job workflow. The full version with caching, comments, and branch protection is in references/github-actions-workflow.md.

```yaml
name: ci
on:
  push: { branches: [main] }
  pull_request: {}
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci
      - run: npx @biomejs/biome ci --reporter=github
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          fetch-depth: 20
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci && npm run build
      - uses: treosh/lighthouse-ci-action@v12
        with:
          configPath: ./lighthouserc.json
          uploadArtifacts: true
          temporaryPublicStorage: true
```

## Gotchas

- Shallow clones break LHCI git-ancestor detection and cause "Could not find hash" errors. Always set `fetch-depth: 20` or higher and check out the PR head SHA.
- Asserting against a single Lighthouse run is flaky. Use `numberOfRuns: 5`; the median of 5 is roughly twice as stable as one run.
- The Cloudflare adapter defaults to `output: 'server'`, so the static output is at `dist/client`, not `dist`. Pointing `staticDistDir` at `./dist` collects nothing.
- An absolute `site` plus `base` makes `_astro/*` assets 404 when LHCI serves from a localhost port. Avoid `base` on the audited build, or use the preview-server path.
- Biome does not auto-enable the GitHub reporter inside Actions (the docs imply it does; it is a known gap). Pass `--reporter=github` explicitly or annotations will not appear.
- If Biome's formatter is left on for `.astro`, `biome ci` fails on files prettier formatted. Disable Biome's formatter for `.astro` (and `.svelte`, `.vue`) as in the recipe.
- Ubuntu runners ship Chrome at /usr/bin/google-chrome, so no Chrome install step is needed.
- Lighthouse 13 requires Node 22.19+ and is not yet bundled by LHCI 0.15.x; do not assume a newer Lighthouse than 12.6.1 until LHCI ships it.
- The PWA category was removed in Lighthouse 12, so `lighthouse:no-pwa` and `lighthouse:recommended` are nearly equivalent; prefer no-pwa to avoid any stale PWA assertion.

## Limitations and out-of-scope

- This skill does NOT measure real-user (field) performance. Lighthouse is lab-only and diagnostic; INP in particular is not lab-measurable. Field Core Web Vitals come from real-user monitoring (for example Cloudflare Web Analytics), which is a runtime concern outside this gate.
- Lab budgets here are regression ceilings, not Google ranking thresholds. The field "good" thresholds are LCP 2.5s, INP 200ms, CLS 0.1 at the 75th percentile and are unchanged as of mid-2026; the 2.0s LCP claim is false. Re-verify against web.dev and Google Search Central on any major revision.
- Deep SEO and schema gating is out of scope (seo-aeo-schema skill); this gate only asserts a coarse Lighthouse SEO category floor as a warning. Deep accessibility and reduced-motion is out of scope (motion and visuals skills).
- Runtime caching and Cache-Control are out of scope. The adapter already sets an immutable Cache-Control on hashed `_astro/*` assets; custom Cache-Control for non-hashed assets via `_headers` is unreliable on Cloudflare Workers Static Assets (issue 13164). Only this assumed-performance note lives here.
- Biome Astro template support is experimental (still, as of 2.5.8 — review-gate re-checked 2026-08-17, NOT triggered); this skill ships it off and uses prettier-plugin-astro for templates. That two-formatter split is a deliberate exception, kept until Biome marks HTML formatting stable, at which point the experimental flag can replace prettier. Note 2.5.2+ removed false-positive noUnusedImports/noUnusedVariables reports for bindings used only in Astro templates under the flag. See references/biome-setup.md.
- Version pins are current as of 2026-08-17: astro 7.2.2, @astrojs/cloudflare 14.2.1, @lhci/cli 0.15.1 (Lighthouse 12.6.1 — Lighthouse 13 has NOT landed in LHCI, issue 1136 idle), @biomejs/biome 2.5.8, treosh/lighthouse-ci-action v12 (12.6.2, still the current major), Node 22. Re-verify on upgrades.
