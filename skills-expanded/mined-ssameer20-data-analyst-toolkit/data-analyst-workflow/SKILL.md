---
name: data-analyst-workflow
description: Use when coordinating an end-to-end data analysis workflow, or when a request spans data cleaning, data quality, feature engineering, SQL, or business intelligence reporting.
---

# Data Analyst Workflow

Use this skill to coordinate data-analysis requests across the specialist skills. **Do not repeat their detailed procedures here or handle their domain work from this file.** Before carrying out a phase, open and follow the linked specialist skill for that phase.

## Route the request

- Dataset cleaning or transformation: [data-cleaning](../data-cleaning/SKILL.md)
- Data-quality rules, audit, or remediation: [data-quality](../data-quality/SKILL.md)
- Derived analytical or machine-learning fields: [feature-engineering](../feature-engineering/SKILL.md)
- SQL writing, explanation, optimization, or debugging: [sql-expert](../sql-expert/SKILL.md)
- BI platform, dashboard, KPI, visualization, or report deliverable: [bi-expert](../bi-expert/SKILL.md)

For a focused request, load only the matching skill. For a broad request, load each relevant skill and coordinate the work in this order as applicable:

1. Assess data quality.
2. Clean or transform the data.
3. Engineer features.
4. Query or analyze using the requested tool.
5. Prepare business intelligence reporting in the requested platform and deliverable format.
6. Validate that assumptions, grain, and metrics remain consistent across the results.

Skip irrelevant phases. Carry decisions and assumptions forward between skills, and present one coherent result rather than separate, repetitive instructions. Each specialist skill owns its detailed workflow, safety requirements, and output guidance.

## Privacy baseline

- Use only the data and context the user explicitly provides for the requested analysis. Do not solicit unrelated personal or confidential information.
- Do not solicit or process payment-card data subject to PCI DSS, protected health information, government identifiers, or authentication credentials and secrets. If supplied data contains these fields, ask the user to remove or mask them before analysis.
- Process other sensitive or special-category personal data only when it is strictly necessary for the stated task, legally adequate consent is confirmed, and the user was explicitly informed before providing it. Otherwise, ask the user to remove or mask it.
- Avoid reproducing personal or confidential values in responses.
