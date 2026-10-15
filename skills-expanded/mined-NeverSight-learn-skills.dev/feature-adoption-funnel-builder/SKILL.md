---
name: feature-adoption-funnel-builder
description: Builds vendor-neutral feature adoption funnels from event logs to quantify conversion, drop-off, and time-to-adopt.
---

## When to invoke
- You have product event logs and need a funnel for a feature (e.g., viewed -> started -> completed).
- You want per-step conversion and median time between steps.

## Inputs needed
- `--events`: CSV containing at least `user_id`, `event_name`, `timestamp` (ISO8601).
- `--steps`: Comma-separated ordered event names defining the funnel.
- Optional: `--window-days`: Max time window from first step to count subsequent steps.
- Optional: `--out`: Path to write funnel JSON.

## Workflow
1. Load events.
2. For each user, find the first occurrence timestamp for each funnel step after the prior step.
3. Count users reaching each step.
4. Compute step-to-step conversion and median time deltas.

## Output format
JSON:
- `steps`: list of step names
- `counts`: users per step
- `conversions`: per-step conversion rates
- `median_step_time_seconds`: median time between steps

## Guardrails
- Use first-occurrence per user per step to avoid double-counting.
- Do not infer missing events.
- Vendor-neutral: no assumptions about event source.

## Reference code
Use `feature_adoption_funnel_builder.py`.
