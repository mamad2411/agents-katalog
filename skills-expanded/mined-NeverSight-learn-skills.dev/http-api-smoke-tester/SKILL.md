---
name: http-api-smoke-tester
description: Run a vendor-neutral HTTP API smoke test plan (requests + assertions) and emit a compact pass/fail report.
---

## When to invoke
- You need a quick, repeatable smoke test for an HTTP API environment (dev/staging/prod).
- You want a lightweight alternative to full integration tests.
- You want machine-readable pass/fail output for CI.

## Inputs needed
- A JSON test plan file with:
  - `base_url`: string
  - `steps`: list of HTTP request steps with assertions
- Optional headers (e.g., auth token) inside the plan.

## Workflow
1. Read and validate the plan schema.
2. For each step:
   - Build the request URL from `base_url` + `path`.
   - Send the HTTP request.
   - Capture status, headers, body (truncated for reporting).
   - Evaluate assertions:
     - status code equals
     - JSON path exists / equals
     - header equals / contains
     - body contains substring
3. Emit a JSON report:
   - overall pass/fail
   - per-step results, assertion failures, timing

## Output format
A JSON object written to stdout:
- `passed`: boolean
- `summary`: counts and total time
- `steps`: list with `name`, `passed`, `status`, `duration_ms`, `failures`

## Guardrails
- Vendor-neutral: uses standard HTTP concepts and a plain JSON plan.
- Do not log secrets: redact `Authorization` and `X-Api-Key` header values in output.
- Limit response body captured in the report (default 2000 chars).

## Reference code
- `http_api_smoke_tester.py`
