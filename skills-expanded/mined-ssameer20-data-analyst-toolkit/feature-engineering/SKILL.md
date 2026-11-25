---
name: feature-engineering
description: Use when designing, creating, transforming, selecting, or validating analytical or machine-learning features from raw data.
---

# Feature Engineering

Design useful, reproducible features that match the analytical objective and data grain, without introducing leakage or unsupported assumptions.

## Workflow
1. Clarify the task (prediction, segmentation, forecasting, or descriptive analysis), target or outcome if any, prediction/measurement time, row grain, available fields, and implementation tool.
2. Inspect actual schema and representative data. Identify keys, time coverage, missingness, category cardinality, and source/availability timing for candidate fields.
3. Propose features with their business meaning, formula, input columns, output type, and level of aggregation. Make assumptions explicit; do not invent columns or business definitions.
4. Choose transformations appropriate to the data and requested tool, such as date parts, durations, ratios, grouped aggregates, categorical encoding, or numeric scaling. Define null, zero, invalid-value, and unseen-category handling.
5. Prevent leakage: exclude target-derived or post-outcome information, use only data available at the prediction time, and compute learned transformations using training data only.
6. Recommend validation that respects the problem structure, such as time-based splits for temporal prediction or group-based splits when entities recur. Fit transformations within each training fold when evaluating models.
7. Provide reproducible code or a clear implementation plan and validate ranges, null handling, row grain, key cardinality, and before/after counts.

## Correctness and privacy
- Separate observed facts, assumptions, and recommendations; do not claim to execute code unless an execution tool is available.
- Preserve source data and document transformations so results are auditable and reproducible.
- Avoid exposing personal or confidential values; never request passwords or API keys.
- Do not solicit or process payment-card data subject to PCI DSS, protected health information, government identifiers, or authentication credentials and secrets. If supplied data contains these fields, ask the user to remove or mask them before analysis. Process other sensitive or special-category personal data only when strictly necessary for the task, legally adequate consent is confirmed, and the user was explicitly informed before providing it; otherwise ask for removal or masking.
