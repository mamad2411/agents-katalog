---
name: web-perf-audit
description: Run an evidence-based web performance and RUM (Real User Monitoring) audit on a live site or a codebase, and produce two documents — PERFORMANCE_AUDIT.md with every finding ranked, and PERFORMANCE_PLAN.md with the fixes organized into delivery phases. Measures field data first (Core Web Vitals p75 from CrUX/PageSpeed Insights), then lab (Lighthouse), response headers, runtime traces and static causes, covering LCP/INP/CLS/TTFB, JavaScript bundles and execution, network waterfalls, API latency, images, fonts, third-party scripts, caching, memory, mobile performance, performance budgets and per-deploy regressions. Use when asked to audit or improve site speed, page load, Core Web Vitals, LCP/INP/CLS, TTFB, bundle size, hydration cost, API latency, RUM or field performance, why a site is slow for real users, why a deploy made things slower, or to set performance budgets and regression gates. Measures before it recommends — it never invents a number and labels everything it could not measure.
license: MIT
compatibility: Node 18+ (native fetch). Field data comes from the CrUX API (needs a free key) or PageSpeed Insights (keyless at low volume); runtime/INP diagnosis prefers the chrome-devtools MCP server; static analysis and the report/budget/regression tooling run with no dependencies at all. Designed for Codex and Claude Code using the Agent Skills open standard.
metadata:
  author: Ezzat Malak
  version: "1.0.0"
---

# Web Performance & RUM Audit

Audit a site's real-user and lab performance, find the **root cause** behind each
failing metric, and write two documents:

- **`PERFORMANCE_AUDIT.md`** — what was measured, every substantiated finding with evidence and a code-level fix, ranked P0–P3.
- **`PERFORMANCE_PLAN.md`** — the same findings as six phases of delivery work, each task with files, impact, risk, complexity and a verification method.

This is a **hybrid** skill: deterministic checks run in `scripts/` (a Node engine)
and emit structured findings plus baseline documents; you orchestrate the runtime
capture, interpret the results, and finalize the report.

## The rule everything else follows

**Measure first. Never fabricate a number. Label what you could not measure.**

The audit's job is to tell the truth about production. A missing measurement is
reported as `Info — not measured`; it is never a pass, never an estimate, and
never quietly replaced with a lab number. `scripts/validate-report.py` fails the
report if an unmeasured metric is rendered as good.

## Non-negotiable output

- Produce **both** documents. Defaults: `PERFORMANCE_AUDIT.md` and `PERFORMANCE_PLAN.md` at the working-directory root, unless the user names other paths.
- **Field p75 is the production signal.** A good Lighthouse score never closes a finding.
- **Mobile is a separate target**, reported separately. Good desktop numbers say nothing about mobile.
- **Every** discovered issue is reported and ranked — not a top-10.
- No vague findings. Not "optimize JavaScript" but "`/products/[slug]` ships 612 KB of JavaScript; ~280 KB is the gallery library, which executes before LCP and adds ~420ms of main-thread blocking on a mid-range phone."
- Do not modify the audited project unless the user asks for fixes afterwards.

Use [assets/PERFORMANCE_AUDIT_TEMPLATE.md](assets/PERFORMANCE_AUDIT_TEMPLATE.md) and
[assets/PERFORMANCE_PLAN_TEMPLATE.md](assets/PERFORMANCE_PLAN_TEMPLATE.md) as the required
structure, and [references/SEVERITY_RUBRIC.md](references/SEVERITY_RUBRIC.md) for severity,
priority and scoring.

## Phase 0: Resolve inputs and mode

Determine these first, then echo them into the report's run-metadata table.

1. **Mode** (auto-detect): **Live URL** (`--url`) is primary and the only mode that measures anything. **Codebase** (`--path`) finds *causes* statically. Both may be combined.
2. **Routes.** `--routes /,/pricing,/products/example` — audit the routes that carry traffic, not just the homepage. Cap with `--max-pages` (default 10).
3. **Keys.** `--crux-key` (free, unlocks CrUX + 25-week history) and `--psi-key` (optional quota). Without either, PSI still returns CrUX-backed field data at low volume.
4. **Depth.** Default **Standard**. **Quick** = homepage, field + lab only. **Deep** = every route, MCP runtime capture per route, history, budgets, regression comparison, plus a self-audit pass.
5. **Optional.** `--budgets budgets.json`, `--baseline snapshot.json`, `--deploy <id>`, `--mcp <dir>`, `--work <dir>`, `--out`, `--plan-out`.

Resolve `<skill-directory>` from the loaded skill path.

## Phase 1: Field data first — this is the audit's spine

```bash
node <skill-directory>/scripts/crux.mjs --origin https://example.com \
  --routes /,/pricing --crux-key <key> --history --out <work>/field.json
```

CrUX gives p75 for LCP, INP, CLS, FCP and TTFB, split PHONE vs DESKTOP, plus a
good/needs-improvement/poor distribution and 25 weeks of history.

**State the limits in the report, do not work around them silently:**
CrUX publishes **p75 only** (p50/p90 are histogram-derived approximations, labelled
`approx`; p95/p99 are **not derivable**), covers **Chrome only**, lags on a **28-day
rolling window**, and has **no record** for staging, authenticated or low-traffic
URLs. When there is no record, say so in the executive summary and treat every
Core Web Vitals verdict as lab-only. See
[references/FIELD_DATA_SOURCES.md](references/FIELD_DATA_SOURCES.md).

## Phase 2: Lab measurement

```bash
node <skill-directory>/scripts/psi.mjs --url https://example.com \
  --routes /,/pricing --strategy both --out <work>/lab.json
```

One PSI call returns a full Lighthouse run **and** CrUX field data — which is why
field numbers exist even without a CrUX key. The engine mines the Lighthouse
audits for the JavaScript, network, image, font and third-party findings.

## Phase 3: Runtime capture (prefer MCP) — the half Lighthouse cannot see

Lighthouse measures a page load. **INP, route transitions, animation cost and
memory leaks all live after it.** Capture them with the chrome-devtools MCP server
and write the JSON into `<work>/mcp/`:

1. `emulate` — **4× CPU throttling + Slow 4G**. Never conclude anything from an unthrottled desktop run.
2. `performance_start_trace` / `performance_stop_trace` around a page load → `performance_analyze_insight` for the LCP breakdown.
3. A second trace around the **real interaction** (add to cart, open the filter) → INP value, its three phases, and the scripts in the responsible Long Animation Frames.
4. `list_network_requests` → the API waterfall.
5. `take_heapsnapshot` before/after repeated navigation when a leak is suspected.

Full playbook and the exact JSON shapes: [references/DIAGNOSTICS.md](references/DIAGNOSTICS.md).
With no capture, runtime findings are reported as **not measured** — do not infer
INP from total blocking time and present it as measured.

## Phase 4: Run the check engine

```bash
node <skill-directory>/scripts/run.mjs \
  --url https://example.com --routes /,/pricing \
  --crux-key <key> --psi-key <key> --strategy both --history \
  --mcp <work>/mcp --budgets budgets.json --deploy <id> \
  --out PERFORMANCE_AUDIT.md --plan-out PERFORMANCE_PLAN.md --work <work>
```

Codebase mode: `node <skill-directory>/scripts/run.mjs --path <repo> --out PERFORMANCE_AUDIT.md`
(optionally with `bash <skill-directory>/scripts/detect-stack.sh <repo>` first).

The engine writes `<work>/findings.json` and `<work>/snapshot.json` and renders both
documents. Check areas:

- **A. Core Web Vitals** — field p75 per route/device, lab attribution, lab-vs-field divergence, 8-week trend.
- **B. JavaScript** — route weight, unused, duplicated, legacy, execution time, DOM size.
- **C. Network & caching** — render-blocking, compression, cache TTLs, redirects, preconnect, critical chains, page weight.
- **D. APIs** — slow endpoints, duplicates, N+1 patterns, oversized payloads.
- **E. Images & fonts** — oversized/legacy formats, unsized images, lazy LCP, `font-display`, face count, third-party hosting.
- **F. Third party** — bytes, main-thread time and blocking time per entity; facade opportunities.
- **G. Runtime** — long tasks, INP attribution, route transitions, memory growth, non-composited animation.
- **H. Static causes** (codebase mode) — `"use client"` spread, `useEffect` data fetching, unmanaged script tags, heavy dependencies, built chunk sizes, missing RUM.

## Phase 5: Interpret — refine, do not rubber-stamp

Read `<work>/findings.json` and:

1. Drop false positives the source disproves, and anything you cannot evidence.
2. Confirm each root cause is a **cause**, not a restatement of the symptom. Use the decision trees in [references/CORE_WEB_VITALS.md](references/CORE_WEB_VITALS.md): every LCP splits into four subparts, every INP into three phases — name the dominant one.
3. Add findings only the trace revealed, using the same stable-ID scheme.
4. Frame framework-specific fixes with [references/NEXTJS_REACT.md](references/NEXTJS_REACT.md) and [references/NETWORK_API.md](references/NETWORK_API.md).
5. In codebase mode, label findings **static** and note that URL mode is required for any real measurement.

## Phase 6: Budgets and regression

```bash
node <skill-directory>/scripts/budgets.mjs --measured <work>/snapshot.json --budgets budgets.json
node <skill-directory>/scripts/compare.mjs --baseline baseline.json --current <work>/snapshot.json --tolerance 0.1
```

Both exit non-zero on breach, so they work as CI gates. Adapt the budgets to the
project rather than pasting the defaults ([assets/budgets.example.json](assets/budgets.example.json),
[references/BUDGETS_REGRESSION.md](references/BUDGETS_REGRESSION.md)). Field metrics move on
a 28-day window, so on deploy day the lab metrics and byte weights are the signals
that gate — say that rather than reporting "field unchanged" as a pass.

## Phase 7: Write, validate, report back

1. Finalize both documents from the templates.
2. Validate the structure:
   ```bash
   python3 <skill-directory>/scripts/validate-report.py PERFORMANCE_AUDIT.md --plan PERFORMANCE_PLAN.md
   ```
   Fix every structural error before finishing.
3. Self-audit (always in Deep, briefly in Standard): every finding names a route, a resource, a measured value, a target and a fix; no unmeasured metric is asserted as passing; mobile and desktop are reported separately; no PII or secrets appear in evidence.
4. In chat, return a short summary only — score, severity and priority counts, the top three fixes, and the two file paths. Do not paste the documents.

## RUM design and review

If the project has no first-party RUM, that is itself a finding (`STATIC-NO-RUM`),
because CrUX cannot see Safari, authenticated routes, low-traffic pages, deploy
IDs or any percentile beyond p75. Recommend the beacon in
[assets/rum-collector.js](assets/rum-collector.js) — a working `web-vitals`
attribution collector with route/device/connection/deploy dimensions — and the
schema, segmentation and privacy rules in
[references/RUM_IMPLEMENTATION.md](references/RUM_IMPLEMENTATION.md).
**Ship it only if the user asks**; this skill audits, it does not install code.

If RUM already exists, review it: is INP collected, is the attribution build in
use, is `route` a pattern rather than a raw URL, is there a deploy ID, are
percentiles available, is mobile separated, does anything alert.

## Guardrails

- Measure before optimizing; state the source of every number.
- Never invent a percentile. p95/p99 without a RUM stream are `not available`.
- Missing keys, MCP or a build reduce coverage with a clear warning — they never fabricate a result and never crash the run.
- Find root causes, not symptoms. "LCP is slow" is not a finding.
- Do not recommend caching to hide a slow backend — find the query first.
- Do not remove required functionality to win a score. Third-party integrations get a cheaper loading strategy and a cost figure for their owner, not a blind deletion.
- Prioritize mobile users.
- Never emit PII, credentials or secrets found in headers, payloads or traces.
- After fixes, re-measure and compare against the original baseline in **both** lab and field.
