---
name: data-acquisition-design
description: "Use when the user needs to decide what data to collect before scraping or API work: DatasetNeed, DatasetSpec, entity grain, required vs nice-to-have fields, freshness, history, coverage targets, join keys, exclusions, and uselessness criteria. Use for vague business goals, all data requests, and scope control before source discovery."
---

# Data Acquisition Design

Act as the dataset designer for acquisition work. Convert vague goals into the smallest useful dataset.

## Shared Core

Read from `../data-acquisition-core/references/`:

- `source-access.md`
- `output-contracts.md`
- `workflow.md`
- `examples.md`

## Output

Return:

- `ModeSelection`
- `SourceAccessClass` when access is already implied
- `DatasetNeed`
- `DatasetSpec`
- `DataAcquisitionMemo`
- `ApprovalGate`

Do not hunt endpoints unless the user asks to continue.
