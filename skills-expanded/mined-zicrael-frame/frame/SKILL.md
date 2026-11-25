---
name: frame
description: Apply FRAME (Foundation, Research, Align, Materialize, Evaluate) to software engineering work - implementing, changing, debugging, or refactoring code, and investigating how a system behaves when the answer has to be established rather than recalled. Establish the requested outcome and the existing behaviour, resolve uncertainty that could change the solution, and verify the deliverable against what was asked.
---

# FRAME

Consideration before Implementation.

FRAME guides engineering judgment. The requested outcome determines the work; uncertainty and verification needs determine the effort and the participants.

## Scale the work to the deliverable

Deliver what was asked for, at the depth that request needs.

| Request | What completing it means |
| --- | --- |
| A change whose cause and approach are already clear | Understand it, implement it, verify it. No investigation is owed. |
| A question, diagnosis, or comparison | Findings with their evidence, and a recommendation where the evidence supports one. No code is owed. |
| A request to fix a defect whose cause is not established | Establish the cause, then the implementation and its checks. |
| A broad improvement request | Enough investigation and implementation to reach the outcome it asks for. |

The requested deliverable decides what you are authorised to do; the evidence available decides how much investigation that takes. A request to explain a failure is satisfied by a supported explanation and does not authorise a fix. A request to fix one is not satisfied until the fix is implemented and verified, however little investigation the cause turned out to need. "Fix this" does not imply deep research, and a serious-sounding task does not imply more process: effort grows because a question is unresolved or a consequence is unverified.

The plan you start with stays revisable. When evidence shows that reaching the requested outcome needs related work — a consumer the change breaks, a contract it violates, a defect the fix exposes — that work belongs to the task, within the authority the request already grants; a genuinely optional improvement does not.

The requested outcome itself holds unless the user changes it. Correct your understanding and your solution as evidence arrives; never quietly weaken a requirement so that a candidate can pass.

A follow-up inherits the understanding already established. Revisit only the outcome, constraints, or decisions the new information actually affects.

## The five responsibilities

These are responsibilities, not conversations, documents, or rigidly ordered passes. Foundation and Evaluate apply to every task. Research and Align can each take a sentence when the approach is already clear.

### F — Foundation

Establish the requested outcome, the explicit constraints, and the existing behaviour that bears on them. Locate what the task actually depends on — the code, its consumers, the tests, the documentation — and work from those sources rather than from filenames or recollection. Stop expanding once the affected behaviour and its credible impact are understood.

Identify the behaviour and contracts that have to survive, including the ones the request never mentions. Distinguish intended behaviour from defects and from incidental implementation detail: preserving behaviour does not mean preserving internal structure. If the change as requested would not achieve the outcome as requested, say so before implementing it.

Where the request is broad, bound it with the outcome it names and the findings you actually have: investigate enough to know what achieving that outcome requires, and treat an unrelated problem you happen to discover as information rather than as authorisation to repair it. Where the outcome admits several readings — "maintainable" and "faster" are the usual ones — say which one you are working to, so the user can correct it before the work is done rather than after.

### R — Research

Resolve the uncertainty that could change the solution. Anything else can be settled while implementing or checked during Evaluate.

- For a defect, establish a cause supported by a reproduction, the code, logs, or traces. Where reproduction is unavailable, state the evidence you have and the uncertainty that remains instead of presenting a guess as a diagnosis.
- Verify the assumptions the approach depends on against the code, a focused experiment, or authoritative documentation for the version actually in use. Existing usage elsewhere does not prove that a proposed variation is supported.
- Investigate dependencies and consumers where evidence indicates the change reaches them.
- Compare approaches when the difference between them would change what you do, and not otherwise.

Research produces usable evidence: what is established, where it can be seen, what remains uncertain, and a recommendation when one is warranted. Where findings are the deliverable, this is the substance of the task rather than a preliminary to it.

When an attempt fails, investigate the failure before replacing the approach; a fix aimed at a misdiagnosed cause looks like progress. Check whether the reason it failed also rules out the alternative you were about to adopt. When the same kind of failure returns, reassess the diagnosis rather than trying the next variation of the fix.

Carry established evidence forward, and keep the reason each rejected alternative was rejected — a rejected approach comes back into scope when that reason no longer holds, and difficulty alone does not remove it. Before another attempt, name the question it would answer; a variation with no question behind it is not investigation.

### A — Align

Decide how to proceed. Test the approach against the implementation context you actually found, accept its trade-offs, and identify the changes and integration points. This is an engineering decision, not a human approval gate; a local choice can be a sentence.

When research came from a helper, check its evidence and the consequential assumptions the decision rests on against the sources, rather than adopting a summary. A recommendation the code contradicts can be rejected.

Involve the user when progress needs authority or information you do not have: a new dependency, a behaviour change, a migration, a cost beyond what the request grants, or constraints that contradict each other. A failed approach on its own is a reason to investigate further, not to escalate.

### M — Materialize

Implement the simplest solution that satisfies the established outcome and contracts, following the project's conventions. Cover the input domain the contract admits, not only the examples in the request. Include the related work the outcome requires; leave out unrelated cleanup and speculative capability.

Preserve required behaviour while correcting the defects the task covers. Simplify internal structure where that helps. If implementation disproves an assumption or shows the approach unsuitable, return to the investigation rather than stacking workarounds.

### E — Evaluate

Assess whether the deliverable satisfies the original request. That includes required work left undone, not only behaviour the change broke.

Use the evidence the task admits, and choose the checks most likely to expose a consequential problem rather than working through every kind of check available. A small change whose effects are visibly contained can be settled by running the relevant tests and confirming the changed behaviour; the depth below is what a consequential change earns.

Run the tests and project checks the repository actually provides. Exercise changed behaviour through its real consumers, at integration, boundary, and failure states. Inspect the source where a test would not reach, and look at the rendered result for presentation changes. Establish expected results independently: a check that reuses the implementation's own logic cannot detect that logic being wrong.

Review the diff for unintended behaviour changes, unnecessary scope, and coverage that was removed or weakened. A fallback has to meet its contract or make the failure visible. An interrupted or blocked check establishes nothing — report it as blocked, and name the material behaviour that remains unverified rather than letting passing checks imply more than they cover. Separate failures you introduced from ones already present.

Where findings are the deliverable, Evaluate assesses the findings: whether they answer what was asked, and whether their evidence actually supports them.

## Participants

Start with one accountable lead carrying all five responsibilities. It holds the requested outcome throughout, owns the implementation decisions and the integration, and answers for the result. Add a helper when it has a concrete contribution that justifies the handoff and the context it has to rebuild.

The common arrangements:

| Arrangement | When it fits |
| --- | --- |
| One agent carrying FRAME | The lead can understand, perform, and meaningfully verify the work itself. |
| FRAM lead, independent E | A separate assessment could expose consequential mistakes, omissions, or unsupported assumptions. |
| FR researcher, AM lead, E validator | A substantial investigation benefits from its own context, and the implementation also benefits from independent assessment. |

The letters show where the effort falls, not where accountability moves: a researcher investigates assigned questions within the lead's outcome, and a validator assesses against it. The lead evaluates its own work in every arrangement — an independent validator adds a second assessment rather than replacing the lead's.

Research and validation are separate choices, and either helper can be used without the other; a lead and a researcher, with the lead evaluating, is as valid as the rows above. Decide on uncertainty, consequences, the value of an independent check, and whether the work separates usefully. Task size and file count do not decide it. The arrangement can change as evidence develops, and choosing one should stay a quick judgment rather than becoming a project of its own.

Research assignments go to `frame-researcher` and validation assignments to `frame-validator`, resolved as the host exposes them, including any plugin namespacing. A helper carries out the assignment it was given: it writes no production code, does not restart FRAME, and does not delegate further. Reuse the same helper for a related follow-up rather than starting another. Where the helper a responsibility calls for is unavailable, carry that responsibility yourself and report the verification you actually performed. Read [references/delegation.md](references/delegation.md) before the first handoff.

Each additional agent has to justify the handoff and the context it rebuilds. More agents do not automatically make the work better, so do not treat adding one as a mark of thoroughness.

## Correction

Evaluation results, whether your own or a helper's, re-enter the work where their cause lies.

| Result | Next action |
| --- | --- |
| Implementation defect, or required work omitted | Repair it and recheck the behaviour the repair affects. |
| Invalid assumption or unsuitable approach | Revisit the relevant investigation and the decision built on it. |
| The requested outcome was misunderstood | Correct the understanding against the original request; ask the user only when the information is genuinely unavailable to you. |
| Missing evidence | Run the smallest practical check that resolves the uncertainty. |
| A finding the evidence does not support | Weigh that evidence before changing anything. |
| An optional improvement | Keep it out of what completion requires. |

Send back only the finding or question that needs resolving. One finding does not restart the task, and a finding does not have to travel through Research to be fixed.

Before reporting completion, account for the material findings you or a helper produced. Reporting an actionable required defect as a residual issue does not repair it. A finding you are not acting on needs its reason stated — unsupported by evidence, outside the requested outcome, or blocked — and a blocked required repair means the task is incomplete.

Continue while necessary work remains and the evidence supports a useful next action: a concrete unresolved risk, a question worth answering, or a check that has not run. When progress depends on information or authority you do not have, or when investigation has stopped producing evidence, report the concrete blocker instead of circling. Completion rests on satisfying the request with adequate evidence, not on agents agreeing with each other.

## Communication

Keep routine process internal and do not narrate the five responsibilities. Explain consequential decisions, changed assumptions, accepted trade-offs, and blockers when they matter to the user. Finish with the result, the checks that support it, and the limitations that remain.
