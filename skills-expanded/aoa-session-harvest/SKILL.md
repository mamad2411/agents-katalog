---
name: aoa-session-harvest
description: "Use only when a literal ref to a closed/reviewed session packet is supplied, to extract, classify, propose promotion or branching, or identify an automation opportunity. Missing, live, or unreviewed evidence must fail closed without inventing a ref. Natural closeout preservation belongs to aoa-memo-writeback. Do not use for generic summaries, progression, direct owner writes, scheduling, mutation, or telemetry authority."
---

# aoa-session-harvest

## Intent

Metabolize reviewed experience without collapsing extraction, object
classification, promotion, route choice, and automation readiness into one
generic candidate label. Destination owners retain all acceptance authority.

## Trigger boundary

Use this skill when:

- an explicitly reviewed, bounded session/evidence packet contains reusable
  units, an isolated unit needs owner or promotion judgment, several next routes
  must remain visible, or a repeated manual route needs automation triage
- the same extraction or promotion is explicitly requested from live,
  unreviewed, or unbounded material and the only valid result is
  `blocked_unreviewed_evidence` before a mode loads

Do not use this skill when:

- the request is generic summarization, progression scoring, memo writeback,
  runtime repair, or direct owner writing, promotion, scheduling, delegation,
  or mutation
- the request starts from ordinary work/closeout evidence and asks whether a
  bounded lesson should be preserved for future owner work; that first
  writeback judgment belongs to `aoa-memo-writeback`, even if the answer might
  later resemble a candidate classification

## Inputs

- reviewed evidence boundary and at least one literal supplied ref,
  closure/review posture, one mode intent,
  relevant owner constraints, risks, effects, and optional checkpoint/handoff
  hints that have not yet been trusted; or an attempted live/unreviewed input
  used only to return the pre-mode block

## Outputs

- one typed session-local result from `references/contract.yaml`, with evidence
  refs, owner hints, rejected nearest route, effect `none`, stop line, and
  destination-owner review requirement; or `blocked_unreviewed_evidence`

## Procedure

| Mode | Use when | Reference |
|---|---|---|
| `extract` | Reusable units and unresolved residue have not been isolated. | `references/extract.md` |
| `classify` | One unit needs its object kind, owner, and next artifact classified. | `references/classify.md` |
| `promote` | Exactly one isolated repeated quest-shaped unit needs a final promotion verdict. | `references/promote.md` |
| `branch` | Several materially different continuations must stay visible. | `references/branch.md` |
| `automation-opportunity` | A repeated manual route needs readiness and highest-honest-mode classification. | `references/automation-opportunity.md` |

### Mode: extract

Read and follow `references/extract.md`.

### Mode: classify

Read and follow `references/classify.md`.

### Mode: promote

Read and follow `references/promote.md`.

### Mode: branch

Read and follow `references/branch.md`.

### Mode: automation-opportunity

Read and follow `references/automation-opportunity.md`.

1. Read `references/contract.yaml`. Confirm that the request or supplied packet
   contains at least one literal evidence ref; never infer, normalize, or mint
   a missing packet/session identifier. Then inspect only enough of that exact
   evidence boundary to verify explicit review/closure.
2. If a literal ref, review/closure, or a bounded evidence source is missing,
   return
   `blocked_unreviewed_evidence` without loading any mode reference.
3. Choose exactly one mode and read only its reference to EOF.
4. Execute exactly one mode. Later modes are typed handoffs and require a new
   selection; they are not an automatic pipeline.

## Contracts

- candidates and refs remain session-local until an owner accepts a handoff
- extraction, classification, promotion, automation, execution, progression,
  telemetry, and durable owner writes are separate effects
- hints, receipts, counts, and route cards never become evidence or authority
  merely by appearing in a reviewed packet
- technique records may explain lineage but are not runtime dependencies

## Risks and anti-patterns

- mining a live transcript, universalizing one success, or turning themes and
  frustration into reusable units
- inventing or normalizing a packet/session ref that was not literally supplied
- forcing every repeated unit into a skill or every automation candidate into
  a scheduler/playbook
- treating quest, receipt, progression, stats, routing, KAG, or owner state as
  procedure output

## Verification

- trace every result to reviewed refs and disposition stale/cross-session hints
- confirm one mode, typed output, owner, rejected nearest target, effects, and
  stop line
- confirm no owner file, quest, memory, route, KAG, telemetry, schedule, or
  runtime state changed

## Adaptation points

Sessions supply reviewed packets and evidence boundaries. Destination owners
supply intake, promotion, automation, progression, and artifact contracts.
