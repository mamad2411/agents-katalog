# /sermon-evaluate-srcs — Manual SRCS Evaluation

Manually trigger SRCS evaluation on research outputs.

## Usage
```
/sermon-evaluate-srcs
```

## Process
1. Read state.yaml to get sermon output directory
2. Verify research output files exist in research-package/
3. Dispatch @unified-srcs-evaluator to evaluate all claims
4. Use `_sermon_lib.calculate_srcs_score()` for score computation
5. Generate srcs-summary.json and confidence-report.md
6. Display summary with flagged low-confidence claims

## Output
- `srcs-summary.json` — Machine-readable scores
- `confidence-report.md` — Human-readable report (via `_sermon_lib.format_srcs_report()`)
