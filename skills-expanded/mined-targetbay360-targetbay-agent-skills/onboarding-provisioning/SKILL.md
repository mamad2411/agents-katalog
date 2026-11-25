---
name: onboarding-provisioning
description: Use when an approved onboarding blueprint needs to become real configuration in TargetBay — the segments, journeys, templates, review triggers, loyalty configuration and onsite placements it describes. Dry-runs every resource first and shows what would be created or changed and how many people each can reach, applies only what a human approved, verifies what was created against what was approved, and stops before anything can reach a real person.
license: MIT
metadata:
  targetbay.display_name: Onboarding Provisioning
  targetbay.version: "0.2.0"
  targetbay.category: provisioning
  targetbay.requires: onboarding.store_context, onboarding.provisioning, onboarding.activation
  targetbay.composes: onboarding-blueprint
  targetbay.risk_level: high_impact
  targetbay.execution_mode: execute_with_approval
  targetbay.status: foundation
---

# Onboarding Provisioning

## Purpose

Build what an approved blueprint describes, exactly and once, and stop before anything goes live.

Onboarding is the workflow most likely to be re-run after a partial failure, and the one where a single
careless approval could activate a dozen irreversible things at once. This skill exists to make both of
those safe: every resource is idempotent, and creating is never the same act as activating.

## When to Use

- An onboarding blueprint has been approved and the resources it describes need creating
- A previous provisioning run failed partway and needs completing
- Verifying that what exists in TargetBay matches what was approved

## When Not to Use

- No blueprint has been approved. Use [onboarding-blueprint](../onboarding-blueprint/SKILL.md);
  provisioning does not decide what should exist.
- The store has an established programme and configuration is being changed rather than created. That is
  a `destructive` change to something somebody built, with its own approval (S6).
- Only activation is wanted. Activation is a separate gate and is never batched (S2, S3).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| The approved blueprint | The only source of what should be created | Blocked |
| Current coverage per product | Confirms nothing changed since the blueprint was approved (G5) | Blocked; a stale blueprint may duplicate or conflict |
| Provisioning capability status | Determines whether anything can be created at all | Blocked; degrade to a build checklist |
| Audience size per resource | Required in the approval request (S4) | Partial; state which sizes are unknown |
| The approved contact budget | Re-checked against what was actually built (X8) | Partial; flag that the check could not run |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `onboarding.store_context` | Current coverage, audience sizes, consent state before creating anything |
| `onboarding.provisioning` | Dry run, apply and verify the resource set |
| `onboarding.activation` | Moving an approved resource from draft to live, one at a time |

## Decision Process

```
1. Re-read coverage              ← confirm nothing changed since approval
2. Translate to resources        ← each with a stable reference, each idempotent
3. Dry run                       ← per-resource diff: create, update, no change, conflict
4. Compute blast radius          ← audience per resource, and weekly contact per customer (X8)
5. Stop on any conflict          ← never overwrite what somebody already built (S6)
6. Approve the resource set      ← as a mutation, with the numbers shown
7. Apply                         ← same idempotency key, drafts only
8. Verify                        ← what exists against what was approved
9. Activate                      ← separately, one resource at a time, each approved on its own
```

Steps 7 and 9 are deliberately different acts. A single call that creates and activates would leave the
approval gate in step 9 with nothing to gate.

## Decision Rules

Binding: [../../rules/safety-rules.md](../../rules/safety-rules.md),
[../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/contact-ownership-rules.md](../../rules/contact-ownership-rules.md),
[../../rules/sequencing-rules.md](../../rules/sequencing-rules.md).

- **Create drafts. Never create and activate in one step** (S2), even when the operator asks for it.
- **Every resource carries a stable reference** so a re-run updates in place rather than duplicating.
  Onboarding is re-run after partial failure more often than any other workflow.
- **Dry run before every apply**, including a re-run. The diff is what the approval is given on.
- **A conflict stops the run** (S6).
- **Show the blast radius before asking** (S4): what will be created, how many people each resource can
  reach, and the maximum weekly contact per customer once it is live.
- **Re-check the contact budget against what was actually built** (X8). If the built set produces a
  different number than the approved blueprint stated, stop and re-approve before activating.
- **Activation is per resource, never batched** (S3, S5), with the recipient count stated each time.
- **Nothing activates before its dependencies verify** (SQ3). A journey activates after its segment exists
  and has been confirmed to hold who it should.
- **Report what actually happened** (S10). A resource that was created is not live, and a plan that was
  approved was not thereby executed.
- **The first send to an imported list is its own approval**, with the ramp and recipient count stated
  (S7, S14).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Re-read coverage and consent; confirm nothing changed since approval | `read_only` |
| PLAN | Translate blueprint steps into resource declarations with stable references | `plan` |
| PREVIEW | Dry run; present per-resource diff, audience sizes and aggregate contact load | `plan` |
| VALIDATE | Run the checks below; stop on any conflict | `plan` |
| APPROVE | Human approves the resource set | — |
| EXECUTE | Apply with the same idempotency key; drafts only | `mutation` |
| VERIFY | Re-read what was created and diff it against what was approved | `read_only` |
| — | **Activate a resource** | `high_impact`, **explicit, one at a time** |
| MEASURE | Confirm each activated resource behaves as the blueprint expected before the next activates | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the resource set with each item's
stable reference and owning product; the dry-run diff classifying every resource as create, update, no
change or conflict; audience size per resource and the maximum weekly contact per customer the set would
produce; what was applied and what was not, by reference; the verification diff of created against
approved; and the explicit list of what remains in draft awaiting its own activation approval.

## Validation

- [ ] Coverage re-read; the blueprint is still current (G5)
- [ ] Every resource carries a stable reference and is safe to re-apply
- [ ] Dry run completed and its diff presented before approval
- [ ] No conflict left unresolved by a human (S6)
- [ ] Audience size stated per resource, or explicitly unknown (S4)
- [ ] Maximum weekly contact per customer recomputed from the built set and matched against the approved figure (X8)
- [ ] Nothing activated as part of the apply (S2)
- [ ] Verification diff run and reported, including any divergence (S10)
- [ ] Every activation approved individually, with its recipient count (S3, S5)
- [ ] No resource activated ahead of a dependency that has not verified (SQ3)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Re-read coverage, dry run, verify | `read_only` / `plan` | None |
| Create the resource set as drafts | `mutation` | Preview the diff and the numbers, then confirm |
| **Activate a journey, trigger or offer** | `high_impact` | **Explicit, per resource**, recipient count stated |
| **First send to an imported list** | `high_impact` | **Explicit**, with the ramp-up plan and recipient count |
| **Replace existing configuration** | `destructive` | **Explicit**, as its own finding, never folded into the apply (S6) |

"Approve the whole launch" is never accepted. Twelve resources are twelve approvals, or the plan is staged
so the first one runs, is measured, and informs the rest (S3).

## Examples

**"The blueprint's approved — build it."**
Fourteen resources across three products. The dry run reports eleven creates, two no-changes from an
earlier partial run, and one conflict with an existing welcome automation the store built before
migrating. The run stops on the conflict, reports it as its own finding, and proceeds with thirteen after
the operator decides to keep the existing automation. Everything is created as drafts. The verification
diff matches. Nothing is live, and the result says exactly that, listing the thirteen drafts awaiting
individual activation.

**"That failed halfway — run it again."**
The same idempotency key and the same stable references are reused. The dry run reports no change for the
seven resources that already exist and create for the six that do not. Nothing is duplicated, and the
approval is asked on the six.

## Failure Handling

| Situation | Response |
|---|---|
| `onboarding.provisioning` unavailable | **Blocked** for execution. Degrade to a build checklist: the exact resource set, in order, for a human to create. Say plainly that nothing was created |
| Dry run reports a conflict | **Stop.** Report what exists, who it reaches, and what replacing it would cost. Never overwrite (S6) |
| Apply partially succeeded | **Partial.** Report which references exist and which do not. A re-run is safe (S10) |
| Verification diverges from approved | **Stop.** Report the divergence. Do not activate anything until it is resolved |
| Contact budget differs from the approved figure | **Stop.** Re-enter approval with the new number (X8) |
| Audience size unavailable for a resource | Report it as unknown in the approval request. Never estimate a number a human is about to approve on (S4) |
| Coverage changed since the blueprint was approved | **Blocked.** Approval was scoped to what was described (S9); return to the blueprint |

Degraded outcomes set `status` and populate `unmet_requirements`. This skill reports what happened rather
than what was intended.
