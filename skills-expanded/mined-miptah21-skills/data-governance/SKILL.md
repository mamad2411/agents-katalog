---
name: data-governance
description: |
  Specialized skill for data contracts, access controls, compliance, and PII handling.
  Use when: implementing RBAC/RLS policies, defining data contracts between producers and consumers, handling PII/PHI masking, GDPR/CCPA compliance, or managing data ownership.
  Do NOT use for dbt model documentation — use `documenting-dbt-models` instead.
  Do NOT use for data lineage tracing — use `tracing-upstream-lineage` or `tracing-downstream-lineage` instead.
metadata:
  author: dataops-agent
  version: "2.0.0"
---

# Automated Data Governance

Data contracts, access controls, and compliance. For dbt documentation, use `documenting-dbt-models`. For lineage tracing, use `tracing-upstream-lineage` / `tracing-downstream-lineage`.

## When to Apply
Use this skill when:
- Defining or enforcing Data Contracts between producers and consumers
- Implementing Role-Based Access Control (RBAC) or Row-Level Security (RLS)
- Handling PII/PHI masking and compliance (GDPR, CCPA)
- Establishing data ownership and stewardship policies
- Code-driven governance rules (SQL grants, policies-as-code)

## Scope Boundaries

| Task | Correct Skill |
|------|--------------|
| "Add descriptions to dbt schema.yml" | `documenting-dbt-models` |
| "What feeds this table?" | `tracing-upstream-lineage` |
| "Set up RBAC for Snowflake" | **this skill** ✅ |
| "Create a data contract for this API" | **this skill** ✅ |
| "Mask PII columns" | **this skill** ✅ |

## Best Practices
1. **Code-Driven Governance**: Treat governance rules, access policies, and data contracts as code.
2. **Clear Ownership**: Every data asset must have an explicit owner defined in metadata.
3. **Least Privilege**: Apply strict access controls and dynamic data masking for sensitive information.
4. **Transparent Lineage**: Ensure all transformations are documented so consumers understand data provenance.

## Execution Pattern
1. Review the current schema, architecture, or policy requirements.
2. Generate the required configuration (YAML data contracts, SQL grants for RBAC, masking policies).
3. Explain how the solution enforces governance without blocking engineering velocity.
