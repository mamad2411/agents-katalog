---
name: customer-journey-gap-analyzer
description: Analyze a CSV of funnel stages and drop-offs to identify the biggest customer journey gaps and suggest prioritized experiments (vendor-neutral).
---

## When to invoke
- You have funnel/journey stage metrics and need to find the largest drop-offs.
- You want a simple prioritization framework for improvement ideas.
- You need a quick report for product, growth, or CX teams.

## Inputs needed
- A CSV with at least these columns:
  - `stage`
  - `entered` (count entering stage)
  - `completed` (count completing stage)
- Optional columns:
  - `avg_time_seconds`
  - `notes`

## Workflow
1. Load CSV and validate numeric columns.
2. Compute per-stage conversion rate: \\(completed/entered\\).
3. Compute drop-off count and drop-off rate.
4. Rank stages by impact using a simple score:
   - volume-weighted drop-off: \\(entered - completed\\)
   - plus penalty for very low conversion.
5. Generate recommended experiments based on common patterns:
   - clarify value proposition
   - reduce form friction
   - improve error messaging
   - add trust/privacy cues
6. Output a JSON report.

## Output format
JSON to stdout:
- `stages`: metrics per stage
- `top_gaps`: ranked list with suggested experiments
- `summary`: overall conversion (first entered to last completed)

## Guardrails
- Vendor-neutral: generic funnel analytics; no platform-specific assumptions.
- Recommendations are templates; validate with user research.

## Reference code
- `customer_journey_gap_analyzer.py`
