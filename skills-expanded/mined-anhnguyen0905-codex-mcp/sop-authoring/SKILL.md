---
name: sop-authoring
description: Write standard operating procedures, process docs, work instructions and checklists a new hire can execute unaided — SOP template with trigger, prerequisites, numbered single-action steps, decision points, expected result per step, escalation path, named owner and review date; SOP vs runbook vs policy; writing for the least experienced reader; screenshots and exact commands instead of prose; versioning and change log; testing an SOP by having someone unfamiliar run it; stale steps, implicit knowledge, unowned documents.
---

# SOP Authoring (procedures a new hire can execute unaided)

## The executable-SOP contract

An SOP is executable when a competent newcomer with the stated access completes it correctly without
asking anyone. That needs nine elements:

```
Title             the outcome as a task ("Refund a duplicate charge")
Trigger           the exact event or condition that starts this procedure
Prerequisites     access, permissions, tools, credentials, inputs, approvals needed BEFORE step 1
Steps             numbered, ONE action each, imperative, with the exact UI path or command
Expected result   per step: what the reader should see if it worked
Decision points   explicit branches — "If X → go to 7. If Y → go to 12."
Definition of done the observable end state, plus what to record and where
Escalation        who to contact, on which channel, within what time, when a step fails
Owner + dates     named owner (role and person), version, last reviewed, next review date
```

Missing any one turns the document into a reminder for people who already know the process.

## SOP vs runbook vs policy

```
Policy   WHAT must and must not happen, and why — the rule. No steps. Changes rarely.
SOP      HOW a recurring, planned task is performed correctly and repeatably.
Runbook  HOW to respond to a failure or incident — diagnosis-first, branch-heavy, written for
         pressure: symptoms, checks, mitigations, rollback, comms.
```

Do not blend them: a policy stuffed with clicks goes stale on the next UI change, and an SOP that
argues rationale buries its own steps. Cross-reference instead.

## Write for the least experienced reader

Assume no tribal knowledge. Expand every acronym on first use. Name the exact menu, button, table,
queue or environment — never "the usual dashboard". Give the literal command with placeholders marked
and the source of real values named. State what NOT to do wherever a plausible wrong action is
destructive. Never write "obviously", "simply" or "just".

```
Weak:   "Verify the payment went through in the admin panel and update the ticket."
Strong: 4. Open Admin → Payments → search the charge ID from step 2.
           Expected: status reads SETTLED and the amount matches the ticket.
           If PENDING, wait 10 minutes and repeat step 4 once.
           If still PENDING, escalate (see Escalation) — do NOT issue a second refund.
```

Use a screenshot only where something is visually ambiguous, annotated on the exact control and
date-stamped so staleness is visible; a copyable command block for anything CLI-driven, never prose
describing what to type; a table for lookups (codes, tiers, routing). Keep the why short and separate
from the steps.

## Versioning, change log, and testing

Keep the SOP in version control or a system with real history. Every change records date, author, what
changed and why; bump a version the reader can quote when reporting a problem; set a next-review date,
because readers trust a stale SOP exactly as much as a correct one. Deprecate rather than delete and
point the old title at the replacement.

Proofreading is not testing. The only valid test is a dry run by someone who has never done the task,
following the text literally while the author watches silently and logs every question, pause and
improvisation — each is a defect in the document, not in the tester. Fix, then re-test with a second
person. For destructive tasks, run against a sandbox or a reversible target first.

## Failure modes

- **Stale steps**: tool or vendor changed, SOP still describes the old flow; readers quietly work
  around it and stop reporting the drift.
- **Implicit knowledge**: "check the usual sheet", unnamed systems, unstated approvals.
- **Multi-action steps**: four actions in one number, so partial completion is invisible and the
  procedure cannot be resumed.
- **No expected result**: success is indistinguishable from silent failure, so the reader continues.
- **No escalation path**: on the first anomaly the reader guesses, improvises, or stalls.
- **No owner**: nobody is accountable for accuracy, so nothing is ever updated.
- **Decision points buried in prose**, so readers take the wrong branch.
- **Untested**: reviewed only by experts, who mentally fill the gaps a newcomer falls into.

## Reviewer checklist

- [ ] Trigger and prerequisites stated before step 1
- [ ] Every step is one imperative action with an exact path, command or field name
- [ ] Every step states its expected result; failure branches explicit and numbered
- [ ] Definition of done names the end state and what must be recorded, where
- [ ] Escalation names a person or role, a channel, and a time bound
- [ ] Named owner, version, last-reviewed and next-review dates present
- [ ] No unexpanded acronyms, no "simply", no unnamed systems or sheets
- [ ] Screenshots annotated and dated; commands copyable with placeholders marked
- [ ] Change log updated; dry run by an unfamiliar person recorded, with the fixes it produced
- [ ] Correctly typed as SOP (not policy or runbook), cross-referencing instead of blending

## Provenance

Standard operating-procedure and technical-documentation practice (single-action steps, expected
results, explicit escalation, named ownership, review cycles, walkthrough testing with a naive user).
The nine-element contract and the SOP/runbook/policy split as stated here are **derived, unverified**
working conventions, not a citable standard. Every interval or number adopted from this file — review
cadence, retry counts, wait times, escalation windows — must be replaced with the project's own
measured values and its compliance requirements before being treated as a target.
