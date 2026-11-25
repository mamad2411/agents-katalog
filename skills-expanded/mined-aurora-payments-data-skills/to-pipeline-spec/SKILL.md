---
name: to-pipeline-spec
description: Turn the current conversation into a pipeline spec covering source-to-target mapping, grain and acceptance corridors, then publish it to the project issue tracker. No interview, just synthesis of what you've already discussed.
disable-model-invocation: true
---

This skill takes the current conversation context, codebase understanding, and data understanding and produces a pipeline spec (you may know this document as a PRD, or its core as a source-to-target mapping). Do NOT interview the user; just synthesize what you already know.

The issue tracker and triage label vocabulary should have been provided to you. Run `/setup-data-skills` if not.

## Process

1. Explore the repo AND the data to understand the current state, if you haven't already. For every source the spec touches, verify the schema against the warehouse catalog (`INFORMATION_SCHEMA` or the platform equivalent) and profile a sample of real rows, because a column you assumed but never checked is the cheapest spec bug to catch here and the most expensive to catch after publish. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Sketch out the seams at which you're going to validate the work. In a pipeline, a **seam** is a model boundary: a table or view that the tests and reconciliation queries read. Existing model boundaries should be preferred to new ones. Use the highest seam possible, validating the mart the consumer reads rather than every intermediate step. If new model boundaries are needed, propose them at the highest point you can. The fewer seams across the pipeline, the better - the ideal number is one.

For each seam, pin three things: the **grain** (what one row means, and the unique key that enforces it), the **oracle** (the independent number the output must reconcile against, such as source-system totals, the legacy report being replaced, or an operational count), and the **tolerance** (exact match, or an explicit corridor with separate warn and error thresholds).

Check with the user that the seams, and each seam's grain, oracle and tolerance, match their expectations.

3. Write the spec using the template below, then publish it to the project issue tracker. Apply the `ready-for-agent` triage label - no need for additional triage.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a revenue analyst, I want daily order volume by sales channel, so that I can spot channel-mix shifts the day they happen
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Source-to-Target Mapping

The blueprint for the transformation work. Start with a one-paragraph, technology-independent sketch of the flow from sources to targets. Then, for every target model:

- **Grain**: what one row means, and the unique key that enforces it
- **Mapping table**: one row per target field, giving the source field(s), types on both sides, the transformation rule in plain English plus the formula where one exists, allowed values and what they mean (semantics, not labels), and cardinality (1:1, split, or coalesce, where a coalesced field needs a reconciliation rule for when its sources disagree)
- **Sample values**: 3-5 per nontrivial mapping, including at least one problem sample: a NULL, a duplicate, or a malformed value actually present in the source
- **Consumers**: the registered downstream surfaces of the target model (dashboards, notebooks, exports) from the consumer registry. A target with a registered dashboard carries the freshness contract: the source-anchored freshness fields (latest business period, source load time) appear as mapped columns like any other

This is the one section where source tables, target models, and formulas appear by name, since the mapping is worthless without them.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The models that will be built/modified, and which layer each lives in (staging, intermediate, mart)
- Materialization and incremental strategy: merge versus partition overwrite, the unique key, and the lookback window for late-arriving rows
- Partitioning and the unit of reprocessing: the partition, not the row, is the atomic unit of state
- Schema contracts on models that consumers read: enforced column names and types
- Backfill and idempotency semantics: what re-running any slice of history does, and why it is safe
- Handling of late-arriving data and source schema drift
- Architectural decisions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly. Model and table names are not file paths; they are domain vocabulary, and the mapping section depends on them.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (a transformation query, a window-function dedup, a schema contract, a type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts: not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test model outputs at the seams, not intermediate steps)
- Which tests are unit tests (fixed rows in, expected rows out, testing logic and running without live data) and which are data tests (assertions against live data, testing quality)
- The acceptance corridor for each data test: the failure counts at which it warns and at which it errors
- Freshness expectations per source: how stale the data may be before a warning, and before an error
- Where a target feeds a registered dashboard: the source-anchored freshness columns the target must expose. Freshness is reportable; the surface shows it, so the mart carries it
- The reconciliation plan for each seam: which comparison proves the oracle number (row counts, column aggregates, or row-by-row classification into identical/modified/added/removed) and at what tolerance
- Whether the publish is gated: write to an audit branch or staging dataset, validate, then promote atomically, or validate in place
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
