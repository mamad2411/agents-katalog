---
name: data-acquisition-core
description: Shared core for the data acquisition skill tree. Use when a data acquisition task needs source access classification, output contracts, compliance boundaries, feasibility scorecards, probing standards, pipeline quality standards, or shared references used by sibling data-acquisition skills. Do not use alone for ordinary browsing or non-data tasks.
---

# Data Acquisition Core

Use this as the shared contract package for the data acquisition skill tree. Keep shared definitions here so sibling skills do not drift.

## Core References

Load only what the active task needs:

- `references/source-access.md`: access classes, owned-session rules, secret handling, publishability.
- `references/output-contracts.md`: ModeSelection, SourceAccessClass, DatasetNeed, DatasetSpec, ProbeResults, FeasibilityScorecard, PipelineQualityPlan, PipelinePlan, ApprovalGate.
- `references/compliance-boundaries.md`: allowed and disallowed behaviors.
- `references/workflow.md`: end-to-end acquisition workflow.
- `references/modes.md`: mode ladder and output shapes.
- `references/probing.md`: tiny probes, headers, pagination, limits.
- `references/feasibility-scoring.md`: scoring and Green/Yellow/Red.
- `references/source-strategies.md`: source strategy tradeoffs.
- `references/pattern-library.md`: common API/source archetypes.
- `references/endpoint-discovery.md`: endpoint reverse-engineering.
- `references/playwright-rendered-dom.md`: Patchright warm-session capture, Playwright fallback, and owned-session browser probes.
- `references/execution-adapters.md`: warm-session capture, adapter ladder, and optional Jacob Padilla adapter notes.
- `references/pipeline-engineering.md`: production pipeline design.
- `references/examples.md`: response shapes.

## Rule

Child skills should reference these files instead of duplicating contracts.
