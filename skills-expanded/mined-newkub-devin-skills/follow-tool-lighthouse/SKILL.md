---
name: follow-tool-lighthouse
description: Audit a single web page with Lighthouse CLI — performance, accessibility, SEO, best-practices
argument-hint: "<url> [options]"
related:
  - follow-tool-unlighthouse
  - use-chrome-devtools
  - deep-review-codebase
  - run-dev
  - report
---

## Goal

Audit one web page reproducibly with the Lighthouse CLI — performance, accessibility, SEO, best-practices — with structured output for review/report

## Scope

Use for auditing a single page/specific route directly with the `lighthouse` CLI

- Boundary: site-wide crawl of every route → `/follow-tool-unlighthouse`; E2E user-flow assertions → `/follow-tool-playwright`; Lighthouse in a CI workflow → `/follow-tool-github-actions`; auditing in an open browser without the CLI (a11y/SEO/best-practices/agentic — not perf) → `lighthouse_audit` in `chrome-devtools-mcp` per `/use-chrome-devtools`
- Latest: `lighthouse@13.5.0` (verified 2026-09-28) — categories added `agentic-browsing` in v13
- Requires Chrome/Chromium ≥ v66 on the machine — or specify it via the `CHROME_PATH` env var

## Execute

### 1. Verify Environment

> Goal: lighthouse and Chrome ready to use

1. `lighthouse --version` — if missing → `bunx lighthouse@latest` or `bun add -g lighthouse`
2. Check Chrome: auto-detects Chrome Stable/Canary — or set the `CHROME_PATH=<path-to-chrome>` env var
3. For a dev URL → start the server first with `/run-dev`

### 2. Run Audit

> Goal: get a report for the desired categories

```bash
# full audit of every category — HTML report
bunx lighthouse <url> --output html --output-path ./reports/lh.html --view

# performance only — JSON stdout for further parsing
bunx lighthouse <url> --only-categories performance --output json --output-path stdout

# desktop profile (not just --form-factor=desktop — use the preset)
bunx lighthouse <url> --preset desktop

# specific mobile emulation
bunx lighthouse <url> --form-factor mobile --screenEmulation.width=360 --screenEmulation.height=640
```

Available categories: `accessibility`, `best-practices`, `performance`, `seo`, `agentic-browsing` (new in v13)
Presets: `perf`, `experimental`, `desktop`

### 3. Control Measurement

> Goal: stable results matching production-like conditions

1. `--throttling-method simulate` (default) for repeatable numbers; `devtools` when you need real-network throttling
2. Tune `--throttling.rttMs`, `throughputKbps` when simulating a specific network
3. `--max-wait-for-load <ms>` for slow-loading SPAs
4. `--blocked-url-patterns` cuts third-party noise (analytics, ads) out of the result
5. `--disable-storage-reset` when auditing a cached/logged-in state
6. For high reproducibility → run 3-5 times and take the median (Lighthouse variance is high)

### 4. Two-Phase Runs

> Goal: debug or re-audit without re-collecting the trace

```bash
bunx lighthouse <url> -G            # gather artifacts → ./latest-run/
bunx lighthouse <url> -A            # audit from stored artifacts
bunx lighthouse <url> -GA           # gather + audit
```

### 5. Parse And Report

> Goal: scores + opportunities as actionable findings

1. Use `--output json`, then read `categories.*.score` (0-1 → x100) and `audits` with `score < 0.9`
2. Focus on `audits` carrying `details.overallSavingsMs`/`overallSavingsBytes` — clear estimated impact
3. `--list-all-audits` shows all audit IDs when you need targeted `--only-audits`/`--skip-audits`
4. Report via the `/report` table: No., Category, Score, Top findings (with savings), Recommendation

## Rules

- JSON output for automation/parsing; HTML for human review — `--output` accepts multiple values
- `--preset desktop` isn't just `--form-factor desktop` — the preset adjusts throttling/emulation more completely
- Lighthouse scores vary between runs (variance) — don't conclude from a single run, use the median of several
- Authenticated pages → launch Chrome with a logged-in profile via `--chrome-flags`/`--port`, or use `--disable-storage-reset`
- Don't audit production third-party sites you have no rights to
- Use /follow-tool-unlighthouse when site-wide is needed; /deep-review-codebase when going deeper than scores

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- A Lighthouse report (html/json/csv) per specified URL with scores for every selected category
- Findings with estimated savings for follow-up fixes
