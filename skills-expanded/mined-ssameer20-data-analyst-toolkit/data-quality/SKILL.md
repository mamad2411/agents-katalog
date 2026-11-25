---
name: data-quality
description: Use when auditing data quality, defining validation rules, measuring defects, prioritizing data issues, or recommending remediation.
---

# Data Quality

Create evidence-based data-quality assessments that make defects measurable, explain their impact, and identify practical next actions.

## Workflow
1. Clarify the dataset's grain, critical fields, business definitions, expected ranges and relationships, and the decision or report at risk.
2. Check for duplicate business keys, referential-integrity failures, missing critical values, invalid ranges or formats, inconsistent mappings, invalid dates, cross-field contradictions, and reconciliation differences.
3. For each rule, state its definition, affected fields, and business impact. Provide validation logic in the requested tool or SQL dialect.
4. Quantify affected rows and rates when data is available. State the denominator and treatment of nulls; never invent counts or results.
5. Prioritize by business impact, scope, reporting risk, and fix feasibility. Clearly label root-cause explanations as hypotheses.
6. Recommend a specific fix and owner/action. Separate safe normalization from decisions that require business approval.

## Report format
Use a concise table with: rule/defect, definition and impact, validation logic, count and rate, severity, root-cause hypothesis, and recommended action. Omit unavailable measurements rather than estimating them.

## Correctness and privacy
- Use only supplied data, schema, and business rules. Distinguish observed facts from assumptions and recommendations.
- Avoid repeating personal or confidential values; suggest masking sensitive fields before sharing.
- Do not solicit or process payment-card data subject to PCI DSS, protected health information, government identifiers, or authentication credentials and secrets. If supplied data contains these fields, ask the user to remove or mask them before analysis. Process other sensitive or special-category personal data only when strictly necessary for the task, legally adequate consent is confirmed, and the user was explicitly informed before providing it; otherwise ask for removal or masking.
- Do not claim to execute checks or modify source data unless an execution tool is actually available.
