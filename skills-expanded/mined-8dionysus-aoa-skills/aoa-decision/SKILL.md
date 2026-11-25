---
name: aoa-decision
description: Find, record, correct, or supersede a durable repository decision and its derived indexes. Use for prior rationale, a meaningful accepted choice, or decision-source/index drift. Do not use for ordinary documentation, an open choice, current source-authority conflicts, or runtime/generated authority mapping.
---

# aoa-decision

## Intent

Provide one front door for durable decision work without loading three
procedures into every request. Keep owner-authored decision records
authoritative; indexes, retrievers, KAG packets, caches, and session evidence
may locate or contextualize a record but never supply its rationale.

## Trigger boundary

Select this family only after the request fits its frontmatter description.
Treat an undecided option, ordinary documentation edit, current authority map,
or non-decision generated/runtime drift as a different task. Lack of evidence
or write authority never becomes implicit approval.

## Inputs

- one decision intent and the target owner, subject, ID, path, or mismatch
- exact owner routes, records, template, index contract, and effect authority
  for the exact effect, target, and scope
  required by the selected mode

## Outputs

- one typed result from `references/contract.yaml` with owner source, actual
  effects, verification, skipped checks, uncertainty, and stop line

## Procedure

Choose exactly one mode:

| Mode | Select when | Do not select when |
|---|---|---|
| `find` | Existing rationale, status, supersession, or impact is requested. | A write or correction is already known to be required. |
| `record` | A meaningful accepted decision lacks an adequate owner record. | The choice is open, trivial, already recorded, or only needs correction. |
| `correct` | An existing decision record or its derived decision view is stale or wrong. | The task is pure lookup, a current non-decision source-authority conflict, or a genuinely new decision. |

1. Read `references/contract.yaml`, then read the selected mode reference to
   EOF. Do not load another mode or a retired child bundle.
2. Use an exact supplied owner root, decision ID, path, or source surface
   before discovery. Read the owner's route law before any source or generated
   write. If that law defines a disposable or non-VCS owner root, do not probe
   Git; use its named files, builder checks, and direct hashes or comparisons.
3. Use a decision retriever only as an optional narrowing aid. Verify every
   rationale, status, supersession, and owner claim in the authored decision
   record.
4. Execute one mode against one target. A handoff to another mode is a later
   selection, not an implicit continuation.
5. Stop as `blocked_missing_input` before target reads or effects when a
   required owner source, accepted decision field, index contract, builder,
   or effect authority is unavailable.
   For a write, bind authorization to the exact effect, target, and scope. A
   current Operator or human authorization that already matches all three
   satisfies the approval gate without a repeated question; a new or changed
   effect, target, or scope requires fresh authorization.
6. Return the selected mode, exact source refs, result state, actual effects,
   verification, skipped checks, residual uncertainty, and stop line.

### Mode: find

Read and follow `references/find.md`.

### Mode: record

Read and follow `references/record.md`.

### Mode: correct

Read and follow `references/correct.md`.

## Contracts

- Keep one mode and one target active at a time.
- Keep decision acceptance, rationale, and record authority with the named
  owner; this skill structures work but does not make the decision.
- Require explicit current authority for `record` and `correct` effects.
- Rebuild generated decision indexes from owner source; never patch them to
  hide source or builder debt.
- Keep session evidence as optional historical context, never decision truth.
- Keep techniques as optional provenance, never runtime dependencies.

## Risks and anti-patterns

- Loading retired child skills or several mode references.
- Trusting an index title, KAG packet, cache, or session narrative as rationale.
- Recording a trivial diff, inferring rejected options, correcting only a
  generated view, or silently rewriting semantic history.
- Copying a sibling owner's rationale, ID scheme, or template as local law.

## Verification

- Confirm one mode, one target, owner-source grounding, and actual effects.
- Confirm source-first correction and owner-builder use where applicable.
- Distinguish source validity, generated parity, external retrieval freshness,
  and broader architectural correctness.
- Report skipped checks and unresolved owner or federation debt explicitly.

## Adaptation points

Let each repository supply its decision home, ID and status vocabulary,
template, index contract and builder, validation commands, supersession law,
and optional retriever binding.
