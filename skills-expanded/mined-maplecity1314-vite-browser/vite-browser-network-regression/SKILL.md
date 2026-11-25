---
name: vite-browser-network-regression
description: >-
  Focused workflow for API/data regressions in Vite apps using vite-browser
  network inspection. Make sure to use this skill whenever users mention any of:
  wrong data, missing data, empty data, empty response, incorrect payload, API
  error, fetch failed, request failed, 401, 403, 404, 500, 4xx, 5xx, status
  code, CORS error, CORS blocked, authentication failed, auth issue, cookie
  issue, session expired, inconsistent data, intermittent API, network timeout,
  or the data is incorrect.
---

# vite-browser-network-regression

Use this skill to isolate request/response regressions quickly.

## Workflow

1. Open page and reproduce action.
2. List network traffic and identify suspicious entries (4xx/5xx/FAIL/slow).
3. Inspect target request in detail.
4. Correlate with UI state and console errors.
5. If the request failure appears only after a hot update or reload loop, switch to `vite-browser-runtime-diagnostics`.

## Commands

```bash
vite-browser open <url>
vite-browser errors --mapped
vite-browser logs
vite-browser network
vite-browser network <idx>
vite-browser eval '<state-probe>'
vite-browser screenshot
```

## Analysis checklist

For each failed/suspicious request:

1. URL and method correct?
2. Status and response body expected?
3. Request headers/body complete?
4. CORS/auth/cookie mismatch?
5. UI state consistent with response?
6. Did the failure start only after a recent HMR update?

## Output format

Always include:

1. Failing request index and endpoint
2. Concrete mismatch (request or response)
3. Likely ownership (frontend request build vs backend response)
4. Confidence: `high`, `medium`, or `low`
5. Exact re-test command sequence

## When to switch skills

If diagnosis reveals the root cause is actually:
- HMR/runtime issue (failure only after hot update, module errors) → switch to `vite-browser-runtime-diagnostics`
- Component state or framework-specific issue → switch to `vite-browser-core-debug`
- Need final pre-release validation → switch to `vite-browser-release-smoke`
