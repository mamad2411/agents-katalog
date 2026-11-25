---
name: aoa-engineering-shape
description: Shape one software responsibility boundary through bounded-context, core-boundary, or port-adapter mode. Use when responsibilities, reusable rules, orchestration, or concrete dependencies are entangled and a small owner-aware boundary is needed before implementation. Do not use for source-authority lookup, ordinary edits, test design, or a boundary that is already clear.
---

# aoa-engineering-shape

## Intent

Choose one shaping lens and return the smallest target-bound responsibility
boundary without installing an architecture framework by default.

## Trigger boundary

Use this skill when:

- domain responsibilities are overloaded, stable rules are mixed with glue, or
  a concrete dependency leaks across a meaningful seam

Do not use this skill when:

- the real task is source authority, decision history, verification, an
  ordinary edit, or implementation after the boundary is already explicit

## Inputs

- target system or code slice, target-specific owner surfaces, current responsibilities
- concrete ambiguity, repeated rule, or leaking dependency

## Outputs

- exactly one typed mode result with boundary, interfaces, owner or unresolved
  owner edge, migration edge,
  verification need, unresolved question, and stop line

## Procedure

1. Read `references/contract.yaml` and choose exactly one mode:

   | Mode | Select when | Required procedure |
   |---|---|---|
   | `contexts` | Meanings, responsibilities, owners, or dual postures are overloaded. | `references/contexts.md` |
   | `core` | A stable rule is mixed with loading, rendering, orchestration, or infrastructure. | `references/core.md` |
   | `port-adapter` | A concrete database, API, filesystem, CLI, provider, or runtime detail leaks inward. | `references/port-adapter.md` |

2. Read the selected reference completely. Do not load the other mode
   procedures merely because their vocabulary appears nearby.
3. Bind owner only from a declaration that governs the target slice. An
   unrelated authored surface, sibling route, recent file, or generated index
   cannot supply the target owner. Keep `owner: unresolved` when that binding is
   missing; never borrow a plausible owner.
4. Execute only the selected procedure. If another shaping mode is materially
   necessary, finish the upstream result and hand its typed output to a later
   task-local DAG node instead of blending modes.

## Contracts

- owner facts remain with their owner; this bundle supplies procedure only
- proposed boundaries may continue with an unresolved owner, but cannot claim
  adoption, placement authority, or an owner-specific destination
- one primary responsibility center; cross-relations stay explicit
- errors, fallback, and limits are part of a port contract, not hidden adapter
  behavior
- a proposed boundary is not accepted architecture until its owner adopts it

## Risks and anti-patterns

- generic clean-architecture diagrams without exact local responsibilities
- assigning a target owner from a nearby but unrelated authoritative file
- making directories, frameworks, or current technique names the semantic core
- creating a port with no consumer or a context map for a spelling fix

## Verification

- confirm the selected mode matches the actual pressure
- cite the target-specific responsibility/rule/dependency and the exact owner
  binding, or state that the owner remains unresolved
- state migration compatibility, what remains unresolved, and what this result
  does not authorize

Stop after one reviewable boundary and next-owner question. Do not implement or
multiply abstractions unless the request separately authorizes that effect.

## Adaptation points

Owners provide local vocabulary, interfaces, compatibility windows, and
validation commands. Those facts remain owner data, not forks of this skill.
