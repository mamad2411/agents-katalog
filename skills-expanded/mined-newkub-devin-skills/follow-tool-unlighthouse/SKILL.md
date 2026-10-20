---
name: follow-tool-unlighthouse
description: Set up Unlighthouse for site-wide Lighthouse audits in dev and CI
argument-hint: "[scope]"
related:
  - follow-tool-lighthouse
  - follow-tool-vite
  - follow-tool-playwright
  - follow-test
  - follow-deploy
  - run-profiler
---

## Goal

Set up and use the Unlighthouse CLI to audit the performance, accessibility, and SEO of an entire website

## Scope

Use for projects that want to monitor every web page with Lighthouse, in both development mode and CI/CD

- Boundary: use Unlighthouse for site-wide audits (crawl every route); for a single-page audit use `/follow-tool-lighthouse`; for E2E user-flow assertions use `/follow-tool-playwright`
- Latest: `@unlighthouse/cli@0.18.1` (verified 2026-09-24)
- v0.18.1 breaking change: requires Node.js >= 22.18.0 (engines)

## Execute

### 1. Setup Environment

> Goal: Set the URL to scan

1. Verify Node.js >= 22.18.0 (the requirement of `@unlighthouse/cli@0.18.1`)
2. Set the `APP_URL` environment variable
3. Use the default `http://localhost:3000` for development
4. Configure it in `.env` or the CI environment
5. Confirm the URL is reachable

### 2. Add Package Scripts

> Goal: Add scripts for dev and CI

1. Add `"audit": "bunx unlighthouse --site \${APP_URL:-http://localhost:3000}"`
2. Add `"audit:ci": "bunx unlighthouse-ci --site \${APP_URL:-http://localhost:3000} --budget 75"`
3. Add `"audit:ci:strict": "bunx unlighthouse-ci --site \${APP_URL:-http://localhost:3000} --budget 90 --build-static"`
4. Run `bun run audit` to test
5. See CLI options in 

### 3. Run Development Scan

> Goal: Scan the website in development

1. Run `bun run audit`
2. Open the Web UI at `http://localhost:5678`
3. Use `--debug` for verbose output
4. Use `--no-cache --throttle --samples 3` for accurate results

### 4. Configure Unlighthouse

> Goal: Create a config file when needed

1. Create `unlighthouse.config.ts` at the root
2. Set the `site`, `outputDir`, `scanner` options
3. Configure budgets for performance, accessibility, best-practices, seo
4. See config example in 

### 5. CI Integration

> Goal: Integrate Unlighthouse with CI

1. Add a job running `bun run audit:ci` in GitHub Actions
2. Use `--build-static` to generate an HTML report
3. Upload the `.unlighthouse/` folder for the static report
4. Fail the CI when a score drops below the budget

## Rules

### 1. Usage

- Use `bunx unlighthouse` for development
- Use `bunx unlighthouse-ci` for CI
- No need to install global dependencies

### 2. Environment Variables

- Use `APP_URL` for the site URL
- Define it in `.env` or the CI environment
- Don't hard-code URLs in scripts

### 3. Budgets

- Use `--budget 75` for the standard threshold
- Use `--budget 90` for a strict threshold
- Set per-category budgets when needed

### 4. Reports

- Use `--build-static` for an HTML report
- Use `--reporter json` for machine-readable output
- Upload the report in CI

### 5. Scans

- Use `--no-cache` for a fresh scan
- Use `--throttle` to simulate a real network
- Use `--samples N` for multiple runs

- Use /follow-tool-vite if needed
- Use /follow-tool-playwright if needed
- Use /follow-test if needed
- Use /follow-deploy if needed
- Use /run-profiler if needed

## References

- [CLI reference](references/cli.md)

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Unlighthouse scripts ready to use
- The development scan works
- CI runs the audit automatically
- Budgets are enforceable
- Reports generate in the wanted format

