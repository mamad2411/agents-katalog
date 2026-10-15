---
name: lighthouse-auditor
description: Run Lighthouse CLI audits for websites and web applications from environment setup through result interpretation. Use when the user wants to audit performance, accessibility, SEO, best practices, PWA readiness, Core Web Vitals, Lighthouse CI, batch URL scans, localhost pages, or production pages. Trigger this skill for Lighthouse setup and troubleshooting in Linux or WSL, browser launcher failures such as "Cannot find Chrome" or "ECONNREFUSED 127.0.0.1", Chrome or Chromium detection issues, PageSpeed-style analysis requests, or any request to generate Lighthouse HTML and JSON reports with actionable recommendations.
---

# Lighthouse Auditor

## Overview

Use this skill to handle Lighthouse work end to end: verify the environment, fix browser-launch problems, run the right audit profile, and turn raw reports into prioritized recommendations.

## Core Workflow

1. Identify the audit scope.
2. Prepare the execution environment.
3. Choose the right audit profile.
4. Run the audit and save HTML plus JSON output.
5. Summarize scores, metrics, opportunities, and next actions.

## 1. Identify the Audit Scope

Collect the minimum missing context before touching the environment:

- Target URL or URLs.
- Localhost, staging, or production.
- Mobile, desktop, or both.
- One-off run, comparison, or batch audit.
- Manual analysis or CI/CD integration.

If the user does not specify, default to one single-URL audit with one run for `mobile` and one run for `desktop`.

## 2. Prepare the Execution Environment

Start with:

```bash
bash scripts/ensure_lighthouse_env.sh --check
bash scripts/clean_lighthouse_temp.sh
```

If you need shell exports for a raw Lighthouse command, use:

```bash
eval "$(bash scripts/ensure_lighthouse_env.sh --print-shell)"
```

Then act on the result:

- If the global `lighthouse` binary is missing and `npm` is available, install it with `npm install -g lighthouse`, or use `npx --yes lighthouse` for a one-off run.
- If Node.js or npm is missing, install Node.js 18+ LTS before continuing.
- If the environment is WSL, prefer a Linux-native browser. Do not point Lighthouse to a Windows Chrome binary under `/mnt/c/...`.
- In WSL, prefer `/usr/bin/google-chrome-stable` over Chromium. If Chrome Stable is missing, install it before trying to debug launcher failures.
- In WSL, `CHROME_PATH` alone is not always enough. `chrome-launcher` may also require a valid Windows Local Temp path in `PATH`. Use `ensure_lighthouse_env.sh --print-shell` or the bundled wrapper so that fix is applied automatically.
- If the user wants the agent to install missing dependencies directly, rerun `scripts/ensure_lighthouse_env.sh` with `--install-lighthouse`, `--install-browser`, or `--install-all`.
- If browser launch fails with `Cannot find Chrome`, `ECONNREFUSED 127.0.0.1`, or similar launcher errors, read [references/wsl-chrome-fix.md](./references/wsl-chrome-fix.md) and apply it exactly.
- Do not declare Lighthouse blocked in WSL until you have tried the explicit fallback sequence from `references/wsl-chrome-fix.md`, including the exact raw Lighthouse command with `--chrome-flags="--headless --no-sandbox --disable-gpu"` after exporting the environment fix.

When installation needs network access, `sudo`, or package-manager changes, ask for approval and state exactly what will be installed.

## 3. Choose the Right Audit Profile

Use these defaults unless the user asks for something else:

- Quick manual review: `1` run.
- Baseline or stakeholder report: `3` runs and compare patterns instead of trusting one noisy result.
- Default device scope: run both `mobile` and `desktop`.
- Mobile audit: default Lighthouse behavior.
- Desktop audit: `--preset=desktop`.
- Local development server: `--throttling-method=provided`.
- CI or headless Linux: `--chrome-flags="--headless --no-sandbox --disable-dev-shm-usage"`.
- WSL launcher-sensitive environment: `--chrome-flags="--headless --no-sandbox --disable-gpu"`.

For advanced settings, budgets, and custom configs, read [references/config-and-budgets.md](./references/config-and-budgets.md).

## 4. Run the Audit

Prefer the bundled wrapper for repeatable work:

```bash
bash scripts/run_lighthouse_audit.sh https://example.com
```

By default, the wrapper creates `./lighthouse-audit-results` in the current working directory, so reports stay inside the project where the audit was executed.
By default, it generates separate report pairs for `mobile` and `desktop`.
In WSL, it also cleans temporary Chrome/Lighthouse profile directories automatically so only the final reports remain in the project.
The wrapper prefers the global `lighthouse` binary, but if it is missing and `npx` is available it can fall back to `npx --yes lighthouse`.
If a previous failed run already left stray folders in the project root, run `bash scripts/clean_lighthouse_temp.sh` before or after the audit.

Common variations:

```bash
# Desktop
bash scripts/run_lighthouse_audit.sh https://example.com --preset desktop

# Mobile only
bash scripts/run_lighthouse_audit.sh https://example.com --preset mobile

# Local dev server
bash scripts/run_lighthouse_audit.sh http://localhost:3000 --throttling-method provided

# Three-run comparison
bash scripts/run_lighthouse_audit.sh https://example.com --runs 3

# Only performance
bash scripts/run_lighthouse_audit.sh https://example.com --only-categories performance
```

Use raw `lighthouse` commands only when a wrapper script would get in the way of a very custom case.
In WSL, prefer the wrapper even more strongly because it injects the launcher-specific environment fix automatically.

If you need to prove whether raw Lighthouse works in WSL, use this exact sequence before concluding the environment is blocked:

```bash
eval "$(bash scripts/ensure_lighthouse_env.sh --print-shell)"
lighthouse https://example.com --chrome-flags="--headless --no-sandbox --disable-gpu"
```

If the global binary is not installed but `npx` is available, run the same fallback with:

```bash
eval "$(bash scripts/ensure_lighthouse_env.sh --print-shell)"
npx --yes lighthouse https://example.com --chrome-flags="--headless --no-sandbox --disable-gpu"
```

After any raw fallback attempt in WSL, run:

```bash
bash scripts/clean_lighthouse_temp.sh
```

If those exact sequences still fail, report the exact stderr and classify it as an environment/runtime issue.

Always save both HTML and JSON output so the report can be opened visually and analyzed programmatically. When running both device profiles, keep the output sets separate and compare them explicitly.

## 5. Summarize and Explain Results

After a run completes, summarize the JSON report with:

```bash
python3 scripts/summarize_lighthouse_report.py path/to/report.report.json
```

Present the results in this order:

1. Audit scope and command profile used.
2. Category scores.
3. Core Web Vitals and related timing metrics.
4. Top three opportunities by estimated savings.
5. Critical diagnostics or failing audits.
6. Prioritized next actions.

Use [references/interpreting-results.md](./references/interpreting-results.md) when you need symptom-to-root-cause guidance or more detailed remediation ideas.

## Batch and CI/CD Work

For multiple URLs, read [references/batch-analysis.md](./references/batch-analysis.md).

For GitHub Actions, GitLab CI, or Lighthouse CI, read [references/ci-cd.md](./references/ci-cd.md).

When running many URLs:

- Keep concurrency modest to avoid distorting scores.
- Reuse the same Chrome flags across the whole batch.
- Compare medians or repeated patterns, not a single best run.

## Reporting Standard

A complete answer should normally include:

- What was audited and under which profile.
- The generated report locations.
- Category scores with a short interpretation.
- Core Web Vitals with threshold context.
- The biggest performance opportunities.
- The most likely root causes.
- A short, prioritized action plan.

## Resources

- `scripts/ensure_lighthouse_env.sh`: Check and optionally install Lighthouse plus a usable browser, with WSL-specific Chrome handling.
- `scripts/clean_lighthouse_temp.sh`: Remove stray Chrome/Lighthouse temp directories that may be materialized in the project root by WSL launcher failures.
- `scripts/run_lighthouse_audit.sh`: Run a single or repeated audit with sensible defaults and stable output naming.
- `scripts/summarize_lighthouse_report.py`: Extract scores, metrics, opportunities, and failing audits from a Lighthouse JSON report.
- [references/wsl-chrome-fix.md](./references/wsl-chrome-fix.md): Exact recovery steps for WSL Chrome launcher failures.
- [references/interpreting-results.md](./references/interpreting-results.md): Read and explain Lighthouse output.
- [references/config-and-budgets.md](./references/config-and-budgets.md): Advanced config files and performance budgets.
- [references/batch-analysis.md](./references/batch-analysis.md): Batch auditing patterns and comparisons.
- [references/ci-cd.md](./references/ci-cd.md): GitHub Actions, GitLab CI, and Lighthouse CI templates.
