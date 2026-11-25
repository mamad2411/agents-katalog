---
name: plugin-widget-recommender
description: "Recommends plugin or widget categories for a concrete Figma workflow and audits supplied plugin usage against a supplied approval policy. Use when the user needs tool-selection guidance or a policy comparison; verify current marketplace availability and do not assume access to file-level plugin history or organization admin data."
---

# Plugin Widget Recommender

## Capability Mode

`Recommend or audit supplied evidence`. Do not install, approve, disable, or configure plugins or widgets. Do not claim live marketplace, file-history, organization-policy, or admin visibility unless that context is explicitly available.

## Required Inputs

- A concrete workflow problem.
- For named product recommendations: current marketplace evidence or browsing access.
- For policy audits: the observed plugin/widget list and the organization-approved list.

When evidence is missing, recommend tool categories and verification criteria rather than asserting specific current products or compliance status.

## Workflow

1. Restate the workflow need and constraints.
2. Decide whether the task is category guidance, current-product research, or policy comparison.
3. For category guidance, recommend the smallest useful tool category and evaluation criteria.
4. For current-product research, verify availability, publisher, maintenance, permissions, pricing, and organization eligibility before naming options.
5. For policy comparison, compare only the supplied observed list against the supplied approved list; mark unknowns instead of inferring usage.
6. Explain the fit, risks, and required verification for each result.

## Guardrails

- Do not infer which plugins or widgets have been used from ordinary canvas content.
- Do not describe a product as verified, highly rated, approved, or available without current evidence.
- Do not install or change organization settings.
- Prefer native Figma capabilities when they already solve the workflow adequately.

## Output Contract

For recommendations, return a short ranked list with `option or category`, `best for`, `evidence`, `risks`, and `verify before adoption`.

For audits, return `plugin/widget`, `observed evidence`, `policy status`, and `required action`.