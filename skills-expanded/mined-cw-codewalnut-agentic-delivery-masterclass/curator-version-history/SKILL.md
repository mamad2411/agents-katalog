---
name: curator-version-history
description: Use when an authentic owner decision must be appended as accepted, rejected, or superseded learning history.
---

# Maintain governed decision history

## Inputs
Exact proposal version, authentic authority decision, prior history, destination version, effective/review dates, conflicts, and replacement links.

## Procedure
1. Verify the decision actor controls the destination and decided the exact proposal version.
2. Append an event; preserve every prior proposed, accepted, rejected, and superseded state.
3. For acceptance, assign the destination version plus effective and review dates.
4. For rejection, retain rationale and evidence boundary.
5. For supersession, link old and new records and end the old effect without deleting its text.
6. Recompute the active record from append-only events and report unresolved conflicts.

## Output
An append-only history event, active-version pointer, dates, actor, rationale, and supersession links.

## Stop condition
Stop when authority is unverified, the decision targets different bytes, dates conflict, history is missing, or a proposal is merely being relabelled as decided.
