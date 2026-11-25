# Web Performance

## Purpose
Measure and improve page performance with Core Web Vitals (LCP, INP, CLS), Lighthouse budgets, bundle analysis, network waterfalls, and RUM field data, enforcing lab-plus-field gates in CI before release.

## Use when
- Diagnosing slow pages, layout shift, input lag, or Core Web Vitals regressions in CrUX or RUM.
- Setting Lighthouse budgets, bundle limits, image and font policies for a web property.
- Analyzing network waterfalls, TTFB, render-blocking chains, and third-party script cost.
- Comparing lab measurements against field data before declaring a performance win.

## Do not use when
- Changing UI components, markup, or accessibility behavior itself (use `frontend-web`).
- Tuning server caches or database queries without page-level measurement (use `caching` or `database-review`).
- Load-testing backend APIs without browser rendering (use `backend-api` k6 procedures).

## Required context
- Target URLs and flows: homepage, listing, checkout, plus authenticated flows with seeded sessions.
- Budgets: LCP under 2.5 s, INP under 200 ms, CLS under 0.1, TTFB under 800 ms, initial JS under 200 KB gzip.
- Test rig: Lighthouse 12 with mobile emulation on Moto G4 profile, WebPageTest 4G throttled, RUM provider and CrUX history.
- Third-party inventory: analytics, chat, ads, tag managers with owners and removal candidates.

## Procedure
1. **Establish the baseline in lab and field**: run Lighthouse 12 three times per URL on mobile emulation, capture WebPageTest waterfalls at 4G throttled, and pull the last 28 days of CrUX plus RUM p75 values for LCP, INP, and CLS.
2. **Read the waterfall critically**: identify TTFB above 800 ms, render-blocking CSS/JS chains, unoptimized hero images, font-induced invisible text, and third-party scripts exceeding 200 ms main-thread time each.
3. **Attack the biggest lever first**: defer or remove third parties, compress hero to AVIF under 100 KB with fetchpriority high, inline critical CSS, defer non-critical JS, preconnect to two origins max, and subset fonts with font-display swap.
4. **Enforce bundle and asset budgets**: run the Vite bundle visualizer (or webpack-bundle-analyzer), keep initial route JS under 200 KB gzip, lazy-load below-fold widgets, serve responsive images with srcset, and fail CI builds that exceed budget by more than 5 percent.
5. **Validate lab gains in the field**: deploy behind a flag to 10 percent of traffic, compare RUM p75 LCP/INP/CLS over 7 days against control, require CrUX direction agreement, and roll back if field p75 does not improve.
6. **Record evidence and run scripts/verify.sh** from the repo root with Lighthouse reports, waterfall links, and RUM deltas attached.

## Decision rules
- **Field data outranks lab**: a Lighthouse win that RUM p75 does not confirm is not a win.
- **Budgets are CI gates**: LCP 2.5 s, INP 200 ms, CLS 0.1, TTFB 800 ms, JS 200 KB gzip; breaches fail the build.
- **Third parties need owners**: every external script has a named owner, a measured cost, and a removal path; ownerless scripts are removed.
- **One lever per experiment**: change a single performance variable per release so RUM attribution stays valid.
- **Never regress the checkout**: any change raising checkout-flow p75 LCP by more than 100 ms is reverted immediately.

## Evidence required
- Lighthouse reports (mobile + desktop, 3 runs each) with scores and metric values.
- WebPageTest waterfall links with annotated bottlenecks and TTFB breakdown.
- RUM p75 before/after comparison over at least 7 days plus CrUX trend reference.
- Passing execution log from scripts/verify.sh.

## Output contract
- Performance findings report with ranked opportunities, measured costs, and owners.
- Budget configuration (Lighthouse CI assertions, bundle limits) merged into CI.
- Field-validated before/after comparison proving p75 improvement or honest no-change verdict.

## Stop conditions
- Budgets green in lab and RUM p75 improved or confirmed stable over 7 days.
- Third-party owner refuses removal and blocks the only path to budget; needs product decision.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to Product if the only path to budget requires removing a revenue-attached third party.
- Escalate to backend-api owner if TTFB above 800 ms traces to server latency rather than frontend assets.
