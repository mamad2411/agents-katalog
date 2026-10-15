---
name: etl-retry-backoff-simulator
description: Simulate retry and exponential backoff strategies against a failure-rate model to estimate expected runtime and cost (vendor-neutral).
---

## When to invoke
- You are tuning retries/backoff for ETL jobs, API ingestion, or batch pipelines.
- You need to compare strategies (fixed delay vs exponential + jitter).
- You want a quick estimate of expected runtime, attempts, and wasted work under failure.

## Inputs needed
- A JSON config with:
  - `attempts_max`
  - `base_delay_seconds`
  - `strategy`: `fixed`, `exponential`, or `exponential_jitter`
  - `failure_probability` per attempt (0..1)
  - `work_seconds_per_attempt` (time spent before a failure/success)
  - `trials` for Monte Carlo simulation

## Workflow
1. Validate config.
2. Run Monte Carlo simulation across `trials`:
   - For each trial, attempt the job up to `attempts_max`.
   - Each attempt succeeds with probability \\(1-p\\).
   - Add work time each attempt; add delay between failed attempts per strategy.
3. Compute summary statistics:
   - success rate
   - expected attempts
   - p50/p90 total duration
   - expected backoff time

## Output format
JSON to stdout:
- `success_rate`
- `expected_attempts`
- `duration_seconds`: p50, p90, mean
- `expected_backoff_seconds`

## Guardrails
- Vendor-neutral: does not assume a specific orchestrator or cloud.
- Model is simplified; use for comparative tuning, not precise capacity planning.

## Reference code
- `etl_retry_backoff_simulator.py`
