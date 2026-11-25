---
name: audit-page-budget
description: Audit a page's weight against a declared byte budget. Loads the URL, records a HAR, classifies entries by asset category (js/css/image/font), tags third-party requests, and compares totals to budget. Returns violations + graduated pass/warn/fail status. Driven by Playwright, observed entirely in-browser.
---

# /audit-page-budget

Single-backend skill. Calls **`audit_page_budget`** on the
rolepod-uiproof MCP server. No fallback (D-024).

## When to use

- Gating a UI change on a declared page-weight budget.
- Sanity-checking total page weight after adding an image, font, or
  third-party script.
- Establishing a baseline weight for a critical landing page.
- Running alongside `/measure-cwv` and `/audit-a11y` as a Verify-phase
  triple.

## When NOT to use

- Build-time bundle inspection (webpack-bundle-analyzer style) — the
  parent rolepod's `rolepod-builder` agent owns build-output
  concerns.
- Backend p95 / p99 latency — same.
- Synthetic load tests (k6, Locust) — same.
- Pages that fail to load (server 500, network error) — fix the page
  first.

## Inputs

- `url` — URL to audit.
- `viewport` — optional `{ width, height }`.
- `budget` — optional overrides. Defaults:
  - `total_kb`: 1500
  - `js_kb`: 300
  - `css_kb`: 100
  - `image_kb`: 500
  - `font_kb`: 100
  - `third_party_kb`: 200
  - `request_count`: 100
- `third_party_hostnames[]` — explicit allowlist. When supplied, an
  entry is only counted as third-party if its hostname matches one of
  these. When omitted, all non-page hostnames count as third-party
  (with an eTLD+1 heuristic for subdomains of the page).
- `wait_for_idle_ms` — wait for `networkidle` after load. Default 2000.

## Outputs

- `run_id` — folder under the run root (see Evidence routing).
- `totals_bytes` — totals per category in bytes.
- `request_count` — total requests recorded.
- `violations[]` — each `{ category, actual_kb, budget_kb, over_pct }`.
- `status` — `pass` (no violations) | `warn` (≤50% over) | `fail` (any
  category >50% over budget).
- `report_path` — path to `budget.json`.
- `har_path` — path to the HAR file (re-loadable in DevTools).

## Process

1. Build `audit_page_budget` input from the user's intent (URL,
   optional budget overrides, optional third-party allowlist).
2. Call the tool.
3. Surface status + violations inline. Reference the HAR path for
   detailed network inspection.

## Evidence routing

Run artifacts are saved under:

- **Standalone:** `.rolepod-uiproof/artifacts/audit_page_budget_<ts>_<uuid>/`
- **With `rolepod` parent** (detected via the marker file `<git-root>/.rolepod/parent-active` written by the parent's SessionStart hook): `<git-root>/.rolepod/evidence/<ts>-rolepod-uiproof-audit-page-budget/`

Either way the run directory contains `budget.json`, `network.har`, and
a `manifest.json` per Extension Protocol v1 so the parent's `check-work`
skill can aggregate the result into the verify report.

## If the tool is unavailable

Surface plainly:

> The `/audit-page-budget` skill needs the **rolepod-uiproof** MCP server,
> which is not currently available. Confirm the plugin is installed and
> try again.

Do not attempt another backend (D-024).

## Examples

### Default budget on a landing page

```json
{
  "url": "https://example.com"
}
```

### Strict JS budget for a critical route

```json
{
  "url": "https://example.com/checkout",
  "budget": { "js_kb": 150, "total_kb": 800 }
}
```

### Tag a specific third-party only

```json
{
  "url": "https://example.com",
  "third_party_hostnames": ["googletagmanager.com", "doubleclick.net"]
}
```
