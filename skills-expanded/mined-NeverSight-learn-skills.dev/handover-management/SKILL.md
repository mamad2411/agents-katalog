---
name: handover-management
description: This skill should be used when preparing, validating, or executing inter-phase handovers in the waterfall lifecycle. Covers artefact inventory, open items log, risk register transfer, phase transition readiness checklist, and formal handover sign-off.
---

# Handover Management

## Purpose

Structured inter-phase handover process for the waterfall lifecycle. Governs artefact inventory, open items log, risk register transfer, phase transition readiness checklist, and formal handover sign-off. Ensures continuity between phases without losing context or leaving unresolved items.

The handover is the formal transfer of accountability from one phase team to the next. It is not a rubber stamp — it is a governance record that every artefact, register item, and open decision has been explicitly accounted for.

## When to Use

- Preparing the handover package for any phase gate (Gate A through Gate H)
- Reviewing completeness of handover artefacts before gate submission
- Transferring open register items (risks, assumptions, clarifications, dependencies) from one phase to the next
- Obtaining formal handover sign-off from the current phase lead
- Any time phase transition readiness is being assessed

## Instructions

### Step 1: Identify the Gate and Artefact Set

Determine the gate label (A–H) and the corresponding mandatory artefact list from `references/gate-criteria-reference.md`.

For Gate C (Phase 3 → Phase 4), the mandatory set is:
- `hld.md`
- `lld.md`
- `interface-specifications.md`
- `adr-set/` (directory with at least 1 ADR file)
- `control-matrix.md`
- `test-design-package.md`
- `operational-design-package.md`
- `security-design-review.md`
- `ai-control-design-note.md`
- `design-approval-pack.md`
- `assumption-register.md` (updated with Phase 3 assumptions)
- `clarification-log.md` (updated, all blocking design items resolved or tracked)

For Gate B (Phase 2 → Phase 3), refer to `references/handover-checklist.md` Section 2.

### Step 2: Conduct Artefact Inventory

For each mandatory artefact:
- Check it exists in `.waterfall-lifecycle/artefacts/phase-N/`
- Check it contains no unfilled `{{variable}}` placeholder tokens
- Check it has been reviewed (not in draft status)
- Record status: `complete` / `incomplete` / `missing`

An artefact with placeholders is `incomplete`, not `complete`. Gate cannot proceed with any `incomplete` or `missing` artefacts.

### Step 3: Transfer Open Register Items

Review the following 5 register types from the current phase:
- Risk register
- Assumption register
- Clarification log
- Dependency log
- Evidence index

For each open item:
- Add a `transition_note` explaining why it was not resolved in the current phase
- Assign or confirm an owner for the next phase
- Copy the item to the next phase's register, preserving the original ID and history
- Document the transfer count per register type

### Step 4: Complete the Phase Transition Readiness Checklist

Assess against the 8 exit criteria for the current gate (see `references/handover-checklist.md`). Record pass/fail per criterion. Any `fail` result is a blocker — the handover package cannot be submitted until the blocker is resolved or formally waived.

### Step 5: Obtain Formal Sign-off

The designated sign-off authority must review and sign the gate approval pack.

For Gate C: Architecture Lead + Solution Architect.
For Gate B: Requirements Lead + Business Owner.

Sign-off requirements:
- All exit criteria are `pass`
- No CRITICAL open items without explicit carry-forward approval
- All mandatory artefacts have status `complete`

Sign-off must happen before gate submission — it cannot be retroactive.

### Step 6: Generate Handover Summary

Produce a handover summary document covering:
- Artefacts handed over (status: complete / incomplete per artefact)
- Open items transferred (count by register type)
- Transition decisions (anything deferred, with reason and owner)
- Sign-off record (authority name, date, method of confirmation)

File the handover summary in `.waterfall-lifecycle/gate-reports/` before Phase N+1 begins.

## Key Principles

1. **No artefact left behind** — every mandatory artefact must be accounted for: either present and complete, or explicitly deferred with a documented reason and named owner.
2. **Open items travel forward** — unresolved risks, assumptions, and clarifications transfer to the next phase register with transition notes; they do not disappear between phases.
3. **Placeholders are blockers** — any artefact with unfilled `{{variable}}` tokens is not complete; the gate cannot pass until placeholders are resolved.
4. **Sign-off is binding** — formal sign-off on the gate pack is the governance record; it cannot be retroactive and must occur before gate submission.
5. **Phase N+1 acknowledgement** — the receiving phase PM must explicitly acknowledge inherited open items before Phase N+1 work begins; inherited items are not surprises, they are documented transfers.

## Reference Materials

- `references/handover-checklist.md` — per-gate artefact checklists and transition readiness criteria
- `references/gate-criteria-reference.md` — gate pass/fail criteria for all gates
- `references/lifecycle-overview.md` — full phase boundary definitions

## Quality Checks

- All mandatory artefacts for the gate are present and have status `complete`
- Zero unfilled `{{variable}}` placeholder tokens in any artefact
- The 5 transfer register types (risk, assumption, clarification, dependency, evidence index) have been reviewed and open items transferred to the next phase
- Exit criteria checklist is 100% pass before gate submission is requested
- Sign-off authority has reviewed and signed the gate approval pack (not just been listed)
- Handover summary is produced and filed before Phase N+1 begins
