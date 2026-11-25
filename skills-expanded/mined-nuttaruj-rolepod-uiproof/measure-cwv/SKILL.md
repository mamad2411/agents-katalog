---
name: measure-cwv
description: Measure Core Web Vitals (LCP, INP, CLS) on a live page using PerformanceObserver injection. Returns metrics + thresholds verdict per web.dev good/needs-improvement/poor bands. Chromium-only — Firefox and WebKit ship partial PerformanceObserver coverage.
---

# /measure-cwv

Single-backend skill. Calls **`measure_cwv`** on the rolepod-uiproof
MCP server. No fallback (D-024).

## When to use

- Verifying that a page meets the Core Web Vitals targets for a UX change.
- Comparing LCP / INP / CLS before vs after a UI change.
- Establishing a CWV baseline for a landing page.
- Running a CWV check inside a Verify-phase flow alongside `/audit-a11y` and `/check-errors`.

## When NOT to use

- Backend latency or server-side p95/p99 timing — that is the parent rolepod's
  `rolepod-builder` agent territory.
- Bundle size / build-output inspection — same.
- Synthetic load tests (k6, Locust) — same.
- Firefox or WebKit targets — the underlying PerformanceObserver entry
  types are chromium-specific; the tool refuses other browsers with
  `cwv_unsupported_browser`.

## Inputs

- `url` — URL to measure.
- `viewport` — optional `{ width, height }`.
- `emulate.network_throttle` — one of `offline | slow-3g | fast-3g | slow-4g | fast-4g | no-throttling`.
- `emulate.cpu_throttle` — 1 (none) to 20 (very slow). Chromium only.
- `observe_ms` — observation window after load. Default 5000ms.
- `interactions[]` — optional steps to elicit INP samples. Each step is
  `{ kind: "click", query }`, `{ kind: "type", query, text }`,
  `{ kind: "key", key }`, or `{ kind: "scroll", direction, amount? }`.
- `thresholds` — overrides for `lcp_ms` (2500), `inp_ms` (200), `cls` (0.1).

## Outputs

- `run_id` — folder under the run root (see Evidence routing).
- `metrics` — `{ lcp_ms, inp_ms, cls }`.
- `verdict` — per-metric `good | needs-improvement | poor | unmeasured`. INP
  is `unmeasured` when no interactions were driven.
- `status` — `pass` (all good) | `warn` (any needs-improvement) | `fail` (any poor).
- `thresholds` — the effective thresholds used.
- `report_path` — path to `cwv.json` with full samples.

## Process

1. Build `measure_cwv` input from the user's intent (URL, optional
   throttle, optional interactions).
2. Call the tool.
3. Surface the three metrics + verdict inline. Reference the report path
   for the full sample list.

## Evidence routing

Run artifacts are saved under:

- **Standalone:** `.rolepod-uiproof/artifacts/measure_cwv_<ts>_<uuid>/`
- **With `rolepod` parent** (detected via the marker file `<git-root>/.rolepod/parent-active` written by the parent's SessionStart hook): `<git-root>/.rolepod/evidence/<ts>-rolepod-uiproof-measure-cwv/`

Either way the run directory contains a `manifest.json` per Extension Protocol v1 so the parent's `check-work` skill can aggregate the result into the verify report. Standalone users can read the manifest themselves — same shape.

## If the tool is unavailable

Surface plainly:

> The `/measure-cwv` skill needs the **rolepod-uiproof** MCP server, which is
> not currently available. Confirm the plugin is installed and try again.

Do not attempt another backend (D-024).

## Examples

### Plain LCP / CLS check on a landing page

```json
{
  "url": "https://example.com",
  "observe_ms": 5000
}
```

INP will be reported as `unmeasured` — no interactions were driven.

### Eliciting an INP sample after a click

```json
{
  "url": "https://example.com/app",
  "observe_ms": 3000,
  "interactions": [
    { "kind": "click", "query": "Open menu" }
  ]
}
```

### Throttled measurement (slow 4G, 4x CPU)

```json
{
  "url": "https://example.com",
  "emulate": { "network_throttle": "slow-4g", "cpu_throttle": 4 },
  "observe_ms": 7000
}
```
