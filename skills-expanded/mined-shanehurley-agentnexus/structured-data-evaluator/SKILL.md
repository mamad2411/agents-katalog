---
name: structured-data-evaluator
description: Interpret measurements, CSV, or logs after deterministic calculation. Use for lab data evaluation. Do not perform mental math, parse raw files in the same step as interpretation, or emit charts directly.
---

# Structured Data Evaluator

ADR 0002 stage: **evaluation only**.

Inputs: already-extracted tables plus deterministic calc outputs.  
Outputs: evaluation packet (trends, anomalies, pass/fail vs limits) with claim tags.  
Next: `visualization-specifier` for chart/table-ready specs.

Forbidden: mixing parse/calc/interpret/chart in one LLM call; inventing measurements.
