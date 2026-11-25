---
name: visual-regression-ci
description: Catch silent visual breakage of an Astro 7 site in CI with Playwright screenshot comparisons — the fourth gate next to Lighthouse, Biome, and axe. Use when adding visual regression testing, when a refactor or token change may have silently changed how pages look, reviewing screenshot diffs, or choosing between Playwright snapshots, Chromatic, Percy, or Argos. Verdict — native-first Playwright toHaveScreenshot, baselines committed in the repo and generated in the SAME environment CI runs in (rendering differs across operating systems; locally-made baselines fail in CI by design). Covers diff thresholds, the baseline update flow, the SaaS escalation with free tiers, and the tombstones (Lost Pixel archived into Figma, BackstopJS stalled two years). Trigger on visual regression, screenshot tests, pixel diff, the design broke silently, or update baselines. Not for the Lighthouse, Biome, and budget gates themselves (perf-ci-gates) or accessibility scanning (a11y-deep).
---

# Visual Regression in CI — the fourth gate

> The stack already gates performance, code health, and accessibility; nothing gates LOOKS. A token refactor, a Tailwind upgrade, or a stray global style can ship a visually broken page while all three gates stay green — that is the silent failure this skill closes. The verdict is native-first: Playwright's built-in `toHaveScreenshot`, baselines committed to the repo, zero new services, zero new pins — the same Playwright the axe job already runs. SaaS tools are the escalation, not the default, and two former defaults are now tombstones.

## TL;DR

- Engine — Playwright `toHaveScreenshot` (v1). The runner, the browser, and the pin (playwright 1.62.1) are ALREADY in the repo for the axe gate; the fourth gate adds one spec file and one CI job, no new dependency.
- Baselines live IN the repo, next to the spec (`*-snapshots/`), reviewed as PR diffs like any other change. They are generated in the SAME environment CI runs in — Playwright's own docs warn rendering varies by OS/hardware/settings; a macOS-generated baseline diffed on a Linux runner fails by design.
- Thresholds are EXPLICIT: set `maxDiffPixelRatio` (or `maxDiffPixels`) consciously per project; the unset default is exact-match, which turns anti-aliasing noise into red builds.
- Escalation (v3): Argos or Chromatic-for-Playwright when a human review UI, multi-viewport matrices, or non-committed baselines earn their place — both have real 5,000-snapshot/month free tiers; Percy (5,000/month) is the alternative.
- Tombstones (v4): Lost Pixel — repo ARCHIVED 2026-04-22, team joined Figma, product sunset; BackstopJS — no release since 2024-09, open security issue unanswered. Do not adopt either.
- Reference: `references/visual-ci-job.md` — the spec file, the workflow job, the baseline-update flow, and the flake discipline.

## The forks

### v1 — Engine

| Option | Verdict |
|---|---|
| Playwright `toHaveScreenshot` | DEFAULT — zero new tools, baselines in git, same pin as the axe job |
| SaaS (Argos / Chromatic / Percy) | Escalation — see v3 |
| Lost Pixel / BackstopJS | TOMBSTONES — see v4 |

The default wins on this stack because the marginal cost is one spec file: Playwright is installed, the browser is installed, the CI job pattern (build, install chromium, run) is copy-adjacent to the axe job perf-ci-gates already hosts.

### v2 — Determinism (the fork that actually bites)

Screenshot tests fail for environment reasons before they fail for real ones. The discipline:

- Baselines are GENERATED where they are COMPARED — in CI itself (the update flow in the reference) or in the official Playwright Docker image pinned to the exact version. Never commit baselines rendered on a developer laptop.
- `maxDiffPixelRatio` explicit (0.01 is a sane start for full-page shots; tighten per-component), `animations: 'disabled'` in the screenshot options, fonts self-hosted (this stack already does — brand fonts ship as woff2), and dynamic regions (video posters, third-party widgets) masked with `mask:`.
- A visual gate that flakes gets deleted by humans within a month. Spend the setup effort on determinism or do not add the gate.

### v3 — SaaS escalation

| Tool | Free tier | Wins when |
|---|---|---|
| Argos | 5,000 screenshots/mo, native GitHub checks, baselines NOT in repo | PR review UI for a team; repo stays light |
| Chromatic for Playwright | 5,000 billed snapshots/mo, no Storybook required | Design-review workflow, multi-viewport matrices |
| Percy (BrowserStack) | 5,000 screenshots/mo | Ecosystem preference; otherwise interchangeable |

Flip triggers: more than one human reviews visual diffs; viewport/browser matrix outgrows one runner; baseline churn pollutes git history. Until one fires, the committed-baseline default costs nothing.

### v4 — Tombstones

- Lost Pixel: GitHub repo archived 2026-04-22 — "Lost Pixel is joining Figma… sunsetting the product." Final npm 3.22.0 (2024-11). Dead; do not pin.
- BackstopJS: last npm publish 6.3.25 on 2024-09-07 (~2 years), ~500 open issues including an unanswered security report on its bundled dependencies. Not archived, but stalled — treat as unmaintained.

### v5 — Where the gate lives

The workflow is perf-ci-gates territory: the visual job joins Lighthouse, Biome, and axe in the SAME ci.yml, same seam contract as the axe job — this skill owns the spec, the baselines, and the update flow; perf-ci-gates owns the workflow file that hosts them. Anti-vacuous-gate habit applies here too: the job log must state how many pages were screenshotted, and zero pages is a failure, not a pass.

## Pins and review-gates

| Thing | Pin (2026-08-18) | Review-gate |
|---|---|---|
| playwright | 1.62.1 — SAME pin as the axe job, bump them together | monthly cadence; snapshot rendering can shift across versions — regenerate baselines on every bump, in CI |
| Argos / Chromatic / Percy free tiers | 5,000/mo each | re-check quotas at adoption; free tiers move |
| lost-pixel | 3.22.0 — DO NOT ADOPT (archived) | none; tombstone |
| backstopjs | 6.3.25 — DO NOT ADOPT (stalled 2 years) | only if the project visibly revives |

## Limitations

- This skill does NOT cover: the CI workflow file itself (perf-ci-gates hosts all four gates); accessibility scanning (a11y-deep); performance budgets (perf-ci-gates); cross-browser functional testing (out of catalog scope today).
- Screenshot tests assert PIXELS, not correctness — they catch unintended change, and they equally flag intended redesigns; the update flow is part of the gate, not an afterthought.
- Verified 2026-08-18. The SaaS quota table and the Playwright rendering behavior are the volatile edges; the committed-baseline pattern itself is stable.
