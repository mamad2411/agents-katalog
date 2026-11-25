---
name: load-testing
description: Designs a k6 load test with realistic traffic, explicit thresholds and a clear pass or fail result, and reads the numbers back to you.
---

# Load testing with k6

A load test needs a question, a traffic model and thresholds written down first.

## Steps

1. Ask or infer: which endpoints, expected peak requests per second, and the targets (for example p95 under 400 ms, errors under 1 percent). Never test production or a shared environment without explicit approval; use a staging copy with realistic data volume.
2. Build the traffic mix from access logs or analytics: weights per endpoint, think time between steps, and a login or token flow that is done once per virtual user, not per request.
3. Write the script in `tests/load/<name>.js`:
   - `scenarios` using `ramping-arrival-rate` so the load is a request rate, not a user count
   - stages: warm up, ramp, hold at peak for at least five minutes, ramp down
   - `thresholds` for `http_req_duration{p(95)}`, `http_req_failed` and per-endpoint tags
   - `check()` on status and a field of the body, since a fast 500 is not a pass
4. Run a short smoke pass (1 virtual user, 30 seconds) to validate the script before the real run.
5. Run the full test. Watch for the knee: where latency climbs faster than load.
6. Repeat once for stability, then a stress run above peak to find the breaking point.

## Rules

- Never hard-code secrets in the script; read from `__ENV`.
- Do not include warm-up in thresholds.
- Never point it at third-party services.

## Report

Pass or fail per threshold, p50, p95 and p99, error rate, the first bottleneck seen, and the safe rate you recommend.
