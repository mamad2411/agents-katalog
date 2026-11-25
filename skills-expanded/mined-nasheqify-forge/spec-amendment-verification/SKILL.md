---
name: spec-amendment-verification
description: >
  Read-only cross-spec verification after spec amendments.
  Checks whether the changes are consistent with the referenced
  specs.
  Triggers when a spec amendment lands and cross-spec consistency must be checked read-only (build verify, conditional); NOT for full spec quality review (use spec_board).
status: active
verification_tier: 1
evidence_layout: per_finding
relevant_for: ["main-code-agent"]
invocation:
  primary: workflow-step
  secondary: [sub-skill]
disable-model-invocation: false
uses: [_protocols/evidence-pointer-schema]
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: spec-amendment-verification

Read-only verification of spec amendments for cross-spec
consistency. Lightweight alternative to a board review. No fixes,
only findings.

---

## Trigger

Buddy dispatches this skill on one of the existing caller paths:

1. MCA return contains `SPEC_VERIFICATION: NEEDED` (original
   trigger — code-side amendment).
2. Architect-amendment integration completes per
   `_protocols/spec-amendment-discipline.md` §Dispatch shape (Buddy
   has just integrated `mode=spec_amendment` prose into the target
   spec(s) and bumped `spec_version`).
3. `retroactive_spec_update/verify-and-commit.md` Phase 4 reaches cross-spec
   verification after integration.

One of these caller paths must apply. Sweep context is not a new trigger.

---

## Input

Buddy passes:
- `changed_files`: the caller's integrated changed-spec set; map the retro
  caller's `changed_specs` to this existing input.
- `change_summary`: per-item status of what changed. Source:
  - MCA-trigger: MCA return's per-item status block.
  - Architect-trigger: the architect's returned edit-list (cross-ref
    sweep per `agents/brief-architect.md` Required Output
    `mode=spec_amendment`).
  - Retro-trigger: integrated findings/change summary from
    `retroactive_spec_update/walkthrough.md` Phase 2 + 2b.
- `task_context` (optional): existing task/wave/item or run metadata.
  When absent, the supplied changed-spec scope provides traceability;
  do not invent a task or run identifier.

When a sweep was authored, include its existing edit-list and application
observations. Consume that context under
`_protocols/spec-amendment-discipline-reconcile.md` §Bounded amendment sweep;
MCA and retro callers need not invent an absent sweep. When
`_protocols/spec-amendment-discipline-reconcile.md` §Independent
references of a changed clause applies, include its entries; their
absence is an issue of the `Independent references` row.

## Agent

Agent type: `spec-verification` (read-only — spec-side mirror of
`code-verification`). Defined in `agents/spec-verification.md`,
dispatched standalone with `disallowedTools`; assembled with
`agents/_protocols/reviewer-base.md` if run as a board seat.

## Process

### 1. SCOPE (determined autonomously)

Read `docs/specs/SPEC-MAP.md` as an entry point. Independently inspect
changed specs, directly referenced specs and demonstrated affected
producer/consumer dependencies using the boundary in
`_protocols/spec-amendment-discipline-reconcile.md` §Bounded amendment sweep.
Neither the map nor the caller's inventory is a scope whitelist.

### 2. READ

Read all specs in the verification scope. For large specs: the
sections that contain cross-references (interface tables, import
lists, type definitions, message-channel lists such as NATS subjects, consumer configs).
For the `Independent references` row, also the references it finds
under the test tree.

### 3. CHECK

For every changed spec, against every referenced spec:

| Check | What |
|-------|------|
| **Contract** | Signatures, return types, parameter lists consistent? |
| **Naming** | Names for the same live contract agree where required; distinguish historical names, valid contextual examples and unrelated entities. |
| **Types** | Enum values, literal types, schema models (e.g. Pydantic) aligned? |
| **References** | Section numbers, line refs, version tags up to date? |
| **Messaging** | Channel or subject names (e.g. NATS), consumer configs, event payloads consistent? |
| **Locks** | Lock namespaces, advisory-lock signatures aligned? |
| **Mechanism cells** | Amendment touches a state carrier → the owning spec's `§Mechanism-Lifecycle` matrix was edited in the same change (no second model in a log), no cell is empty, every cell is placed per the plan (`task-N` cells have their owning task `blocked_by`-wired), every cross-spec pointer resolves to the owning section (`skills/_protocols/mechanism-model.md`) |
| **Derived-state routes** | Amendment touches an "X changes only via Y" invariant → every input-changing operation (withdraw, processing / meaning successor, scope move, replacement field edits, cross-principal acts) is a matrix column with a guard or a stated unreachability reason (`skills/spec_board/checklist-and-dispatch.md` §4b) |
| **Fix values** | A new validator / rule taken from a review finding or ruling agrees with every spec that produces or consumes the field, and names the contract-owner spec |
| **Supplied sweep** | Perform the verifier responsibilities in `_protocols/spec-amendment-discipline-reconcile.md` §Bounded amendment sweep against actual applied consumers and protected text. |
| **Independent references** | The amendment changes what a clause requires → find the references that encode it yourself: those the spec and its test plan name, and the test tree searched for the identifiers the clause had before the amendment. Compare them with the edit-list entries (`_protocols/spec-amendment-discipline-reconcile.md` §Independent references of a changed clause). An issue: no entries where a reference encodes a changed clause, a reference missing from them, an `unchanged` reason the change does reach. No reference found: not applicable, with the search in Notes. |

No completeness check on the spec itself — only cross-spec
consistency of the changed places and the completeness of the
amendment's own entries the rows above name.

### 4. RETURN

```
VERIFICATION-RESULT:
  Scope: [N changed specs, M cross-refs checked]
  Status: PASS | ISSUES_FOUND
  Issues:
    - [Spec-A §X ↔ Spec-B §Y]: description of the inconsistency
  Notes:
    - [observations that aren't issues but are relevant]
```

For supplied sweep context, include checked outcomes and comparison
evidence in Notes; put unmet required outcomes or comparisons in Issues,
as defined by the amendment protocol. Retain the existing result format.

On `PASS`: Buddy logs and moves on.
On `ISSUES_FOUND`: Buddy escalates to the user with the issue
list. Buddy does NOT fix autonomously — the user decides whether
a fix is needed or acceptable.

## Contract

### INPUT
- **Required:** changed_files — the caller's integrated changed-spec set;
  map the retro caller's `changed_specs` to this existing input.
- **Required:** change_summary — the caller's per-item status, returned
  amendment edit-list or integrated retro findings/change summary.
- **Optional:** task_context — existing task/wave/item or run metadata.
  Without it, the supplied changed-spec scope provides traceability; do
  not invent a task or run identifier.
- **Required:** a caller path from §Trigger.
- **Context:** `docs/specs/SPEC-MAP.md` — the agent determines
  the scope autonomously.
- **Conditional context:** authored sweep edit-list and application
  observations, per §Input.

### OUTPUT
**DELIVERS:**
- Verification result: PASS or ISSUES_FOUND.
- Scope documentation (N changed specs, M cross-refs checked).
- On ISSUES_FOUND: issue list with spec references (Spec-A §X ↔
  Spec-B §Y).
- Notes: observations that are not issues but are relevant.

**DOES NOT DELIVER:**
- No fixes — read-only, only findings.
- No completeness check — only cross-spec consistency of the
  changed places, beyond the amendment's own entries the §3 rows name.
- No pre-amendment review — this is POST-amendment.

**ENABLES:**
- Build verify: cross-spec consistency after spec amendments.
- User decision: issue list as a basis for the fix decision.
- Fix routing: issues show which consumer specs are affected.

### DONE
- SPEC-MAP read and the verification scope determined
  autonomously.
- All specs in scope read (interface points).
- Applicable §Process, 3. CHECK rows completed; non-applicable checks
  and unavailable required evidence are explicit.
- Verification result returned: PASS or ISSUES_FOUND.

### FAIL
- **Retry:** not foreseen — verification is a single pass.
- **Escalate:** ISSUES_FOUND → Buddy escalates to the user with
  the issue list (Buddy does NOT fix autonomously).
- **Abort:** not foreseen.

## Boundary

- No spec review → `spec_board` (amendment-verification is
  POST-amendment, not pre).
- No code review → `code_review_board`.
- No completeness check on a spec → `spec_board` §Completeness.
- No pre-amendment cross-spec coherence →
  `architecture_coherence_review`.
- Read-only: Buddy does not fix here, only verifies.

## Anti-patterns

- **NOT** run amendment verification without first listing all
  changed specs. INSTEAD: `git diff --stat` + an explicit scan
  for amendment markers. Because: missed amendments =
  unverified changes.
- **NOT** fix yourself when issues are found. INSTEAD escalate
  to the user with the issue list. Because: amendment
  verification is read-only — otherwise role conflict.
- **NOT** push cross-spec consistency off as "the board's job".
  INSTEAD check it here, that's the main purpose. Because: the
  board checks single-spec quality, not cross-spec effects of
  amendments.
