---
name: lighthouse-ci
description: Lighthouse CI on the production build — 5-run median budgets, regression attribution, routes each failed metric to its scanner. Lab only; no INP.
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash]
---

# lighthouse-ci

## Premise

Find real perf regressions, not noise. Every failure cites the metric + measured value + budget + the suspected cause (commit / file / chunk). "Score dropped" without numbers is not a finding. A single run is not a measurement — the median of 5 runs (`numberOfRuns: 5`, `aggregationMethod: "median-run"` on every numeric assertion) against the production build, or the result is invalid. Five runs, median-run, production build is `THR-LHCI` in `templates/governance/thresholds.json`; [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Lighthouse median" uses the same shape. Dev-mode runs are forbidden; HMR inflates TBT and LCP misleadingly.

A failed budget without a named cause is unfinished investigation — and naming it is step 7 below, not an act of intuition.

**This skill is also the pack's performance front door.** Eight of this pack's skills are performance scanners; this is the only one that measures, so it is the one that decides which of the other seven to run and in what order. See § Triage routing.

Run Lighthouse against the production build, enforce budgets, and detect regressions vs a stored baseline.

## When to run

- Before merging a PR that touches frontend files.
- After upgrading a heavy dep (Vue / Vite / a UI library).
- Weekly in CI to track Core Web Vitals trend.
- Before a marketing campaign that will spike traffic.

## Prerequisites

- Built artifact served locally (NOT `pnpm dev` — HMR mode masks the perf issues you're hunting).
- `@lhci/cli` pinned: `pnpm add -D @lhci/cli@0.15.1`. 0.15.1 (2025-06-25) is still the latest release on 2026-10-05 and bundles **Lighthouse 12.6.1** (`npm view @lhci/cli dependencies`), whatever global `lighthouse` is installed. Audit ids differ between Lighthouse 12 and 13 — § Lighthouse ids by version.
- A `lighthouserc.json` at repo root with assertions + the URLs to audit.
- Optional: `LHCI_GITHUB_APP_TOKEN` to post results back to GitHub PRs.

## Procedure

1. Build for production:
   ```bash
   pnpm build
   pnpm preview --port 4173 &     # Vite preview, or `nuxi preview`, or `next start`
   sleep 3                         # let server bind
   ```
2. Run Lighthouse on the configured URLs:
   ```bash
   npx lhci autorun --config=./lighthouserc.json
   ```
3. Inspect the generated `.lighthouseci/` directory. Reports are JSON + HTML; `assertions.json` has pass/fail per metric.
4. **Compare against the baseline.** `lhci assert` checks the absolute budgets below on the median run; it has no notion of a previous build. `--preset=lighthouse:no-pwa` / `lighthouse:recommended` only seed default assertions, so a preset is not a baseline. A relative regression needs a stored series: the LHCI server's compare view (`lhci upload --target=lhci`), or the § Baseline registration entry that G4 compares. Without either, report absolute budgets only and say `baseline: none`.
5. On a `bf-cache` failure (same id in Lighthouse 12 and 13), read the audit's `notRestoredReasons` — it lists the ACTUAL disqualifiers; cite those as the finding, not "bf-cache failed". The hard disqualifier is an `'unload'` (or `'beforeunload'`) listener → fix is to replace it with `'pagehide'` / `'visibilitychange'`. `Cache-Control: no-store` on the document is a WARN/review detector, NOT an error — Chrome rolled bfcache-for-CCNS to ~100% in 2025 where safe, so don't fail the build on it; flag it for review.
6. Stop the preview server when done:
   ```bash
   kill %1
   ```
7. **Attribute the regression.** The Output block and the Halt conditions both require a likely cause (commit / file / chunk); steps 1-6 build, run, compare and read — none of them produces one. This step does. Three sources, strongest first; stop at the first that answers:

   **a. The chunk.** A failed `resource-summary:script:size`, or a TBT jump, is a bundle question rather than a Lighthouse one. Run `bundle-analyze` and take its named chunk + anchoring import. A file beats any commit guess.

   **b. The diff since the baseline.** Bound the search to what actually changed:
   ```bash
   git log --oneline "$BASELINE_SHA..HEAD" -- src/ package.json
   git diff --stat "$BASELINE_SHA..HEAD" -- package.json   # a dependency bump is the most common single cause
   ```
   Record `$BASELINE_SHA` **beside the baseline when you store it** — a baseline with no commit attached is a number nobody can attribute later, which is how this step came to be missing in the first place.

   **c. Bisect the assertion, not the app.** More than a handful of candidate commits and no obvious dependency bump: re-run step 2 against the midpoint build. Two or three runs localise it, and the run is already scripted above — this is cheap because the measurement is automated.

   If all three come back empty, the report says `likely cause: unattributed (<N> candidate commits in range <sha>..<sha>)` and names the range. That is an honest outcome. "Score dropped" is not, and neither is a plausible-sounding commit nobody checked.

## Triage routing — this pack's performance entry point

Eight of this pack's skills are performance scanners and none of them is a front door. A developer holding *"the dashboard is slow"* otherwise has to know all eight names, guess an order, and reconcile the overlaps by hand — the work `/a11y-audit` and `/i18n-audit` already do for their axes. This section is that front door.

**Run this skill first.** It is the only artifact here that measures; every other scanner reads source. Then route by the metric that actually failed — do not fan out to all eight and merge afterwards, because each row's first scanner usually explains the rest, and eight merged reports are exactly the pile the developer came here to avoid.

| Failed / regressed here | Route to, in this order | Stop when |
|---|---|---|
| **LCP** | `lcp-audit` (which element, is it prioritized) → then `image-optimization` if that element is an image, `font-optimization` if it is text, or `streaming-ssr` if TTFB dominates the sub-phases | the LCP element is identified **and** its dominant sub-phase is named |
| **CLS** | `font-optimization` (swap-CLS from a fallback with unmatched metrics) → `image-optimization` (missing `width`/`height`) | the shifting element is cited at `file:line` |
| **TBT** (the lab proxy for main-thread cost; not INP) | `bundle-analyze` (what is on the main thread) → `code-splitting.md` (ai-pattern) for where to cut | a named chunk **and** its anchoring import |
| **`server-response-time`** (TTFB) | `streaming-ssr` (can the shell paint before the slow query) → `ssr-audit` if the route is wrong-strategy rather than merely slow | the blocking call is cited with its measured latency |
| **`resource-summary:script:size`** | `bundle-analyze` → `image-optimization` / `font-optimization` for the non-JS budgets | the over-budget bytes are attributed to files |
| **`bf-cache` ineligible** | `navigation-speed` — it owns the disqualifier detectors; this runner only knows the audit failed | the evicting listener is cited at `file:line` |
| **Nothing failed, but navigation feels slow** | `navigation-speed` — prefetch, route loading UI, bfcache and soft-nav announcement are all invisible to a single page-load measurement | its per-route table is filled |
| **Lab is clean, users still complain** | field data — `web-vitals-field` *(performance pack, when co-installed)*. Absent that pack, say `field source unavailable` and stop; there is no lab substitute | — |
| **The SEO or accessibility category regressed** | different axes, with their own owners: `seo-audit` / `@technical-seo`, and `a11y-scan` under `/a11y-audit` | — |

**Merging: one ranked list, not N reports.** Rank by **savings per unit of effort**, not by size — each routed scanner returns findings with a cited `file:line` and a fix, so order them by (bytes or milliseconds recovered) ÷ (files touched), and state which single item closes the budget on its own. A list the developer still has to rank is the menu they arrived with.

**When the `performance` pack is co-installed**, its `/perf-audit` command owns this orchestration end-to-end — run that instead and let this table defer to it. This table is what the frontend pack does when it is installed alone, which is the normal case for a frontend-only project.

## Default budgets

```json
{
  "ci": {
    "collect": { "numberOfRuns": 5 },
    "assert": {
      "assertions": {
        "categories:performance":              ["error", { "minScore": 0.9, "aggregationMethod": "median-run" }],
        "largest-contentful-paint":            ["error", { "maxNumericValue": 2500, "aggregationMethod": "median-run" }],
        "cumulative-layout-shift":             ["error", { "maxNumericValue": 0.1, "aggregationMethod": "median-run" }],
        "total-blocking-time":                 ["error", { "maxNumericValue": 300, "aggregationMethod": "median-run" }],
        "server-response-time":                ["error", { "maxNumericValue": 600, "aggregationMethod": "median-run" }],
        "bf-cache":                            ["error", {}],
        "first-contentful-paint":              ["warn",  { "maxNumericValue": 1800, "aggregationMethod": "median-run" }],
        "speed-index":                         ["warn",  { "maxNumericValue": 3400, "aggregationMethod": "median-run" }],
        "resource-summary:script:size":        ["error", { "maxNumericValue": 307200 }],
        "resource-summary:stylesheet:size":    ["warn",  { "maxNumericValue": 102400 }]
      }
    }
  }
}
```

Customize per-project. Mobile budgets stricter than desktop. Critical-JS budget tighter than total-JS. The run count and aggregation are `THR-LHCI` (`templates/governance/thresholds.json`: 5 runs, median-run, production build); cite the id, not the literal.

Notes:
- **No `interaction-to-next-paint` assertion.** That audit declares `supportedModes: ['timespan']` in both Lighthouse 12.6.1 and 13.5.0 (read from the unpacked packages, 2026-10-05); `lhci autorun` collects navigation runs, where it does not exist. TBT is the lab proxy; INP is field-only (callout below).
- `server-response-time` is the TTFB audit (good ≤ 600ms). `document-latency-insight` also covers it; the audit itself survives in Lighthouse 13. Reframe any "TTFB as a share of LCP" guidance as diagnostic prose, NOT an assertion — `lhci` can only assert the single `largest-contentful-paint` numeric audit, not its sub-phases. Do NOT add an LCP-decomposition (resourceLoadDelay / resourceLoadDuration / TTFB-share) assertion or a `bf-cache`-less `interactive` (TTI) assertion — TTI was removed from Lighthouse 10's scored set.
- `bf-cache` asserts back/forward-cache eligibility; the audit reports `notRestoredReasons` (the actual disqualifiers) — see the bf-cache Procedure note.

> **There is no lab INP here.** A navigation run has no user interaction, and the INP audit only exists in timespan mode. Authoritative INP comes from field data (CrUX, or RUM `onINP` via the `web-vitals-field` skill *(performance pack, when co-installed)*); absent that pack, the report says `INP: field source unavailable`. TBT is reported as TBT, never relabelled INP.

## Lighthouse ids by version

Lighthouse 13 (13.0.0 on 2025-10-10; 13.5.0 on 2026-09-18) removed the legacy diagnostic audits; the `*-insight` audits replace them. LHCI 0.15.1 runs Lighthouse 12.6.1, which ships **both** sets. A standalone `npx lighthouse` is 13.x and ships only the insight ids. Facts below were read from the `default-config.js` and each insight's `replacesAudits` in the unpacked 12.6.1 and 13.5.0 packages on 2026-10-05.

| Class | Lighthouse 12.6.1 (LHCI 0.15.1) | Lighthouse 13.x |
|---|---|---|
| LCP element | `largest-contentful-paint-element` (informative); `lcp-phases-insight` | `lcp-breakdown-insight` (renamed from `lcp-phases-insight`) |
| LCP lazy / not prioritised | `lcp-lazy-loaded`, `prioritize-lcp-image`; `lcp-discovery-insight` | `lcp-discovery-insight` |
| Render-blocking | `render-blocking-resources`; `render-blocking-insight` | `render-blocking-insight` |
| Third parties | `third-party-summary`, `third-party-facades`; `third-parties-insight` | `third-parties-insight` (no facade audit) |
| Legacy JS | `legacy-javascript`; `legacy-javascript-insight` | `legacy-javascript-insight` |
| Duplicated JS | `duplicated-javascript`; `duplicated-javascript-insight` | `duplicated-javascript-insight` |
| Images | `uses-responsive-images`, `modern-image-formats`, `uses-optimized-images`, `offscreen-images`; `image-delivery-insight` | `image-delivery-insight` |
| Fonts | `font-display`; `font-display-insight` | `font-display-insight` |
| Preconnect | `uses-rel-preconnect` | folded into `network-dependency-tree-insight` |
| Layout shift | `layout-shifts`, `unsized-images`; `cls-culprits-insight` | `layout-shifts`, `unsized-images`, `cls-culprits-insight` |
| Unchanged | `largest-contentful-paint`, `cumulative-layout-shift`, `total-blocking-time`, `server-response-time`, `bf-cache`, `resource-summary`, `unused-javascript` | same |

Read the runner's version and pick the column. When both ids exist, assert on the insight id so the assertion survives the upgrade, and keep the legacy id beside it while CI runs LHCI 0.15.x:

```bash
LHV=$(npx --no-install lighthouse --version 2>/dev/null || echo 12.6.1)   # under LHCI the bundled 12.6.1 applies whatever this prints
echo "lighthouse ${LHV} → ids column: $([ "${LHV%%.*}" -ge 13 ] && echo 13.x || echo 12.6.1)"
```

An assertion on an id the runner does not ship proves nothing either way: the row prints `blocked (id absent in Lighthouse <v>)`, never PASS.

## Output

```
Lighthouse CI — /products (mobile, median run of 5; LHCI 0.15.1 / Lighthouse 12.6.1)

  PASS  LCP             2210ms  (budget 2500)
  PASS  CLS             0.04    (budget 0.1)
  FAIL  TBT             420ms   (budget 300)   regression vs baseline 210ms
  INFO  INP             field source unavailable (performance pack not installed)
  PASS  TTFB            410ms    (budget 600)
  FAIL  bf-cache        ineligible             notRestoredReasons: unload listener
  PASS  FCP             1640ms  (budget 1800)
  PASS  performance     0.92    (budget 0.90)

Bundle (resource-summary):
  PASS  JS total        284 KB  (budget 300)
  FAIL  JS critical     162 KB  (budget 150)   12 KB over

Likely cause  (step 7, source b — diff since baseline 9f2e1c0):
  Commit a1b2c3d added `import { Editor } from "tiptap"` to HomePage.
  Confirmed by source a — bundle-analyze names chunk `home-*.js` (+41 KB) with that import
  as its anchor. Move Editor behind a lazy boundary or a per-route chunk.

Routed next (§ Triage routing):
  TBT + JS-critical over budget -> bundle-analyze (done, above) -> code-splitting.md
  Nothing else routed: LCP / CLS / TTFB / bf-cache all within budget.

Reports:  .lighthouseci/lhr-1745492045123.html
```


## False positives / gotchas

- Run against the BUILT artifact, not `pnpm dev`. Dev mode injects HMR + uncompressed source, which inflates TBT and LCP misleadingly.
- Network flake produces a one-shot regression — re-run before blocking.
- Baseline = median of last 10 successful runs. A single fast run isn't a baseline.
- Mobile throttling defaults to "Slow 4G + 4x CPU" — unchanged for years; matches real low-end devices, don't relax it.
- CLS often regresses from font swaps or hero images without `width/height` — verify in the diagnostic, not just the score.
- Skip server-rendered admin pages (no public traffic, no Core Web Vitals to chase). Keep the budget on customer-facing routes.
- Lighthouse audits ONE page load — it cannot see INP on in-app SPA route changes or post-hydration interactions; rely on field RUM per route (the `web-vitals-field` skill *(performance pack, when co-installed)*).

## Halt conditions

- Halt on hand-waves: every regression must cite metric + measured value + budget + likely cause (commit hash / file / chunk) — produced by Procedure step 7, or reported as `unattributed` with the candidate range named. A cause nobody derived is a guess wearing a hash.
- Halt if the stored baseline carries no `$BASELINE_SHA` — without it step 7's diff source cannot run, and the next regression is unattributable by construction. Record it with the baseline or the baseline is incomplete.
- Halt if a failed metric is reported with no routed next step while § Triage routing names one. Measuring is this skill's job; leaving the developer to pick from eight scanners is the gap it exists to close.
- Halt if the run targeted `pnpm dev` instead of the built artifact — invalid measurement, re-run.
- Halt if `numberOfRuns < 5` or a numeric assertion lacks `aggregationMethod: "median-run"` — one Lighthouse run moves 5–10 points ([`precedents/performance.md`](../../../../snippets/precedents/performance.md) § 51).
- Halt if an assertion names an id the runner's Lighthouse version does not ship (§ Lighthouse ids by version) and the row reads PASS.
- Halt if any INP value is reported without a field source cited (CrUX or RUM `onINP`, the `web-vitals-field` skill *(performance pack, when co-installed)*). Without that pack the run prints `INP: field source unavailable` — never a TBT number relabelled.
- Halt if a budget is relaxed in `lighthouserc.json` to make the build pass — that's masking, not fixing. Relaxation requires an ADR.

## Baseline registration

The budgets above are absolute. A regression relative to the base needs a stored series. Register one metric per route in the behavioural-baseline registry (`.claude/baselines/main/manifest.json`, proposal §7) as kind `performance`:

```bash
bash .claude/scripts/baseline-capture.sh register --id=lcp-products-mobile --kind=performance \
  --engine=frontend/lighthouse-ci --scope='src/**,package.json,vite.config.*' \
  --command='bash scripts/perf/lighthouse-metric.sh /products largest-contentful-paint' \
  --harness=scripts/perf/lighthouse-metric.sh --artifact=.claude/baselines/main/lcp-products-mobile.samples.json \
  --compare=perf --unit=ms --cadence=nightly
```

- The harness builds and previews its own checkout, runs **one** Lighthouse collection and prints **one** number: the metric's `numericValue`. G4 runs it in a worktree at the base sha too. For the performance score, print `categories.performance.score` and add `--higher-is-better`.
- `--artifact` is a samples file the capture writes. `lighthouserc.json` and `.lighthouseci/` stay as they are and are not registered.
- **Gate G4**, in CI, nightly: `behavior-diff.py --gate=G4` drives `perf-compare.py`, base and head interleaved, at least 10 runs a side (`THR-PERF-REGRESSION`). Lighthouse is noisy, so `TOO-NOISY` is common. That verdict is a refusal, reported UNVERIFIED and never as a pass. Nothing re-runs until the number turns green.
- A G4 `REGRESSION` is not explained by an acceptance criterion: `changes_baseline` explains G14 diffs only. An accepted slowdown needs a human waiver (`THR-WAIVER`: owner, expiry, reason, ticket). Re-recording the samples file needs a criterion naming `lcp-products-mobile` in `changes_baseline`, or `test-integrity.py` fails it as `undeclared-baseline-rewrite`. Relaxing a budget is never the fix.

## Related

- **§ Triage routing above is the index** — every skill in this list is reachable from a failed metric there, in a stated order. These one-line boundaries say what each owns; that table says when to run it.
- `navigation-speed` — bf-cache disqualifiers + soft-nav prefetch; this runner reports `bf-cache` ineligible, that skill tells you which listener caused it.
- `bundle-analyze` — when a JS budget fails here, that skill names the chunk and the anchoring import; this one only knows the total.
- `code-splitting.md` (ai-pattern) — where to cut what `bundle-analyze` measured.
- `lcp-audit` / `image-optimization` / `font-optimization` — the three asset scanners that fix what an LCP or CLS regression here is usually made of.
- `visual-check` — run against the same built artifact; a CWV regression and a visual regression often share one cause.
- Cross-pack (`performance`, when co-installed): `web-vitals-field` — authoritative field INP via CrUX / RUM `onINP`. Lab INP here is a synthetic proxy; absent that pack, report `INP: field source unavailable` rather than promoting the proxy.
