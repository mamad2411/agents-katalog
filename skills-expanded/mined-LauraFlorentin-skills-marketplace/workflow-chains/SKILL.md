---
name: workflow-chains
description: Coordinate multi-stage M&A workflows across screening, diligence, marketing, bidding, synergy analysis, and integration planning. Use when a user asks for an end-to-end deal process, multiple connected deliverables, parallel workstreams, stage gates, owners, dependencies, or an auditable transaction workflow.
---

# Workflow Chains

Sequence the plugin's specialist skills while preserving deal-team review, source provenance, confidentiality, and professional judgment. Automation speed depends on document quality, access, scope, and approval latency; do not promise fixed time compression.

## Control plane

For every chain, define:

- transaction, side, phase, decision, deadline, and materiality;
- source documents and approved data boundaries;
- workstream owner, reviewer, and approval gate;
- input and output schema for each step;
- dependencies, parallel-safe tasks, and stop conditions;
- version, timestamp, source citations, and unresolved questions for each deliverable.

Do not distribute confidential outputs, contact counterparties, modify a VDR, submit a filing, or send a bid without explicit authorization and the required human approval.

## Common chains

### Opportunity to preliminary bid

```text
CIM and source intake
  → deal screening and financial normalization
  → independent valuation scenarios
  → regulatory and financing issue scan
  → investment-committee review
  → IOI draft and authorized submission
```

### VDR opening to initial red flags

```text
VDR inventory and permission check
  → document classification and missing-item log
  → parallel financial, legal, regulatory, and commercial issue spotting
  → contradiction and source reconciliation
  → specialist and counsel review
  → prioritized red-flag report and diligence plan
```

### Synergy thesis to integration plan

```text
independent synergy map
  → costs-to-achieve, timing, dependency, and confidence model
  → operating-model and workstream design
  → Day 1, first 100 days, and value-capture milestones
  → functional-owner validation
  → board or steering-committee plan
```

Adapt the chain to the deal. Run steps in parallel only when they do not depend on one another and when data-access controls permit it.

## Stage gates

At each transition:

1. validate source completeness and permissions;
2. reconcile numbers, entities, dates, currencies, and defined terms;
3. separate verified fact, management representation, estimate, and open question;
4. require the named reviewer for legal, regulatory, tax, accounting, valuation, employment, data, or other specialist conclusions;
5. log approval, requested revision, or stop reason.

Stop the chain on missing authority, material conflicting evidence, suspected data leakage, unsupported legal or regulatory conclusion, failed validation, or a change in deal scope.

## Status output

Return:

| Stage | Owner | Inputs | Status | Evidence / version | Gate | Next dependency |
|---|---|---|---|---|---|---|

Follow with critical path, parallel workstreams, decisions due, material risks, missing evidence, and the exact human approvals required next.
