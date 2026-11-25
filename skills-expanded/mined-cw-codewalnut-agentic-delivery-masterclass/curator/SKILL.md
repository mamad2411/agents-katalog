---
name: curator
description: Use when delivery findings should improve the next change.
version: 1.0.0
---
# Curate evidence-backed learning

## Purpose and boundary
Place verified learning in the correct governed home. Do not copy private evidence, silently change policy, or universalize one local solution.

## Inputs
Review/test evidence, defects and surprises, current skill/domain versions, provenance, maintainers, domain owners, and contribution rules.

## Steps
1. State the finding and its evidence without confidential payloads.
2. Classify it: reusable method, domain fact/decision, product defect, or local implementation note.
3. Choose one home: skill for portable questions/process; domain for approved business meaning; backlog for a product change; local note for implementation detail.
4. Draft the smallest update with status `proposed`, owner, source, effective date, and conflicts.
5. Review for overfitting, privacy, safety, compatibility, and whether one counterexample would invalidate the rule.
6. Obtain the correct approval. Mark `accepted` only after owner decision; retain rejected/superseded history.
7. Define a next-use check and review date, then observe whether the change reduces missed decisions or rework.

## Outputs
Curated learning record, proposed/accepted update, owner, version, provenance, conflict status, review date, and next-use measure.

## Stop gates
Stop for private content, absent evidence, unknown owner, unresolved contradiction, universal claims from one case, or an update that changes approved policy without product authority.

## Example
Finding: simultaneous valid cancellation requests can duplicate side effects if transition and event publication are separate. Reusable skill update: always ask which side effects must occur once under concurrency. Domain remains: only `placed` and `confirmed` are cancellable. Product proposal: evaluate a transactional outbox. These are three different records and owners.

## Quality check
Method and business facts remain separate; proposal is not adoption; provenance is safe; a later work item can test whether the learning helped.
