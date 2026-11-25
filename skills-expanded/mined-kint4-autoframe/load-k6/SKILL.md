---
name: load-k6
description: Generate a k6 load test script with ramp-up stages and pass/fail thresholds. Use when the user runs /load-k6 or asks for a load or performance test.
---

# /load-k6 — Generate a k6 Load Test

**Type:** Load
**Description:** Generates a k6 load test script for a described scenario, with real ramp-up/sustain/ramp-down stages, thresholds, and a readable report.

---

## Input Format

The user describes the scenario:
- The endpoint or flow to load test
- Expected/target traffic (concurrent users)
- Performance goals (acceptable latency, error rate)

If targets aren't given, use Autoframe defaults: 50 ramp-up → 100 sustained, p95 < 500ms, error rate < 1%.

## Output Format

A k6 script at `performance/load/[scenario].load.js` following the k6 conventions in CLAUDE.md:
- `options.stages`: ramp up, sustained load, ramp down — **real numbers, never placeholders**
- `options.thresholds`: p95 response time and error rate
- `__ENV.BASE_URL` for the base URL — never hardcoded
- `check()` assertions and a `sleep()` per iteration

## Step-by-Step Instructions

1. Read the k6 conventions in CLAUDE.md.
2. **Confirm the target URL is not production.** If it is, require explicit user confirmation before generating or running.
3. **Check the target path is HTTP-reachable.** Single-page apps route paths like
   `/inventory.html` client-side — a raw `http.get` to them returns 404. For SPAs,
   target the document root or real API endpoints instead. Verify with one request
   (`curl -o /dev/null -w "%{http_code}"`) before generating the script.
4. Translate the scenario into concrete stages and thresholds (use defaults if unspecified).
5. Write the script:
   - `import http from 'k6/http'` and `{ check, sleep } from 'k6'`.
   - `export const options` with `stages` (real durations/targets) and `thresholds`.
   - `export default function ()` that hits `${__ENV.BASE_URL}/[path]`, runs `check()`s, and `sleep(1)`.
6. Use kebab-case + `.load.js` suffix.
7. Save to `performance/load/[scenario].load.js`.
8. Tell the user how to run it: `BASE_URL=... k6 run performance/load/[scenario].load.js` (or via the `load.yml` workflow).

## Rules

- Never use placeholder text like `[ramp-up]` in stage targets — always real numbers.
- Always use `__ENV.BASE_URL`; never hardcode URLs.
- Always define ramp up, sustained, ramp down stages and both thresholds.
- Never run against production without explicit user confirmation.
- k6 scripts are JavaScript (the one exception to the TypeScript rule).
