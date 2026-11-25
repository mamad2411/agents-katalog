---
name: library-health-report
description: "Audits accessible components, styles, and variables for naming, duplication, documentation, and structural health. Use for a scoped library review; include usage or publication findings only when the required library or analytics context is explicitly available."
---

# Library Health Report

## Capability Mode

`Review accessible library evidence`. Do not assume access to organization-wide libraries, publication settings, usage analytics, subscriber data, or admin controls.

## Scope

- Default to the current file, page, or selected library assets.
- Expand to a published library only when that context is available.
- Treat usage claims as unknown unless usage data is supplied or accessible.

## Workflow

1. Inventory in-scope components, component sets, styles, and variables.
2. Check naming, grouping, descriptions, variants, properties, modes, and token semantics.
3. Identify exact duplicates and evidence-backed near-duplicates.
4. Flag undocumented, deprecated, detached, or structurally inconsistent assets.
5. Prioritize findings by user impact, maintenance cost, and migration risk.
6. Separate direct file findings from analytics- or admin-dependent recommendations.

## Guardrails

- Do not label an asset unused without usage evidence.
- Do not claim publication or subscriber status without access.
- Do not delete, unpublish, or rename assets during a report-only review.
- Preserve documented exceptions.

## Output Contract

Return scope and coverage, findings by severity, affected asset names, evidence, recommended action, dependencies, and unavailable data that would improve confidence.
