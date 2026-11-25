---
name: pitch-agent
description: Coordinate a first-draft investment banking pitch workflow in Codex using the imported financial-services skills. Use when the user wants a new valuation workbook and pitch deck for a target plus situation, with explicit sequencing, artifact contracts, and review gates.
---

# Pitch Agent Coordinator

Use this coordinator for a first-draft client pitch. Do not use it for editing an existing deck only.

Before running:

- read [`references/workers.md`](./references/workers.md)
- read [`../finance-modeling-office-pro/references/source-inventory.md`](../finance-modeling-office-pro/references/source-inventory.md) for provenance if needed
- reuse the `model-builder` coordinator pattern for the workbook phase

## Inputs

Minimum inputs:

- target company or ticker
- one-line strategic situation

Optional inputs:

- explicit comp set
- precedent preferences
- required template deck path
- whether an illustrative sponsor case is required

## Output Contract

Primary artifacts:

- `./out/model.xlsx`
- `./out/pitch-<target>.pptx`
- `./out/pitch-review.md`

Supporting scratch files are allowed under:

- `./out/tmp/pitch-agent/`

## Coordinator Flow

1. Scope the pitch ask.
2. Research comps and precedents.
3. Build and verify the valuation workbook.
4. Build the pitch deck.
5. Run review gates and stop for banker approval.

## Phase 1: Scope The Pitch Ask

Create:

- `./out/tmp/pitch-agent/scope.md`

It should define:

- target
- situation
- sector framing
- expected deliverables
- whether the deck must use a specific template

## Phase 2: Research Comps And Precedents

Use:

- `sector-overview`
- `comps-analysis`

Create:

- `./out/tmp/pitch-agent/research-pack.md`

The pack should capture:

- trading comps list
- precedent transactions list
- metric definitions
- sector framing notes
- unsourced gaps

If delegation is available and explicitly authorized, this phase maps to the `pitch-researcher` worker.

## Phase 3: Build And Verify The Valuation Workbook

This phase should follow the `model-builder` coordinator pattern, but constrained to the pitch deliverable.

Use:

- `dcf-model`
- `lbo-model` when the sponsor case is requested
- `3-statement-model`
- `audit-xls`
- `xlsx-author`

Produce:

- `./out/model.xlsx`
- workbook verification results folded into `./out/pitch-review.md`

If delegation is available and explicitly authorized, this phase maps to the `pitch-modeler` worker for structured calculations and to the write-capable deck-writer phase for final workbook materialization.

## Phase 4: Build The Pitch Deck

Use:

- `pitch-deck`
- `pptx-author`
- `ib-check-deck`

Produce:

- `./out/pitch-<target>.pptx`

Rules:

- every number on the deck traces back to the workbook
- footnotes and dates must be consistent
- if the workbook changed materially after review, rerun deck QC

If delegation is available and explicitly authorized, this phase maps to the `pitch-deck-writer` worker and owns the write scope.

## Phase 5: Review Gates

Stop twice:

1. after the workbook is built and verified
2. after the deck is generated and QC is complete

Write:

- `./out/pitch-review.md`

That file must state:

- target and situation
- workbook path
- deck path
- what was verified
- any unresolved sourcing or template issues

Do not proceed to client-facing distribution or outreach from this coordinator.
