---
name: anti-gold-plating
description: Prevent gold plating (unapproved extras) through explicit scope, formal validation of improvements and alternatives, and a final compliance summary. Use when creating or modifying a deliverable, code, configuration, or system. A request for analysis or a proposal does not grant authorization for its implementation.
disable-model-invocation: false
---

# Anti Gold Plating

Execute only the request and formally validated changes. Do not substitute your judgment for the user's regarding scope or the choice between multiple approaches. A useful, tested, reversible, or technically superior modification is still not authorized.

## Definition, Origin, and Impact

**Definition:** Gold plating is the delivery team's addition of unrequested or unapproved extras beyond agreed requirements, even when intended as improvements. PMI identifies it as a contributor to scope creep. Treat a formally approved change as authorized scope, not as gold plating. [PMI: Top Five Causes of Scope Creep](https://www.pmi.org/learning/library/top-five-causes-scope-creep-6675).

**Origin:** This name draws on project-management and PMP preparation terminology. PMI discusses gold plating in [PM101 (1993)](https://www.pmi.org/learning/library/modern-project-management-defining-purpose-5059); [Above and beyond (2002)](https://www.pmi.org/learning/library/above-beyond-scope-interpretation-bandwidth-4507) cites Rita Mulcahy's 2000 *PMP Exam Prep Guide*. These sources establish usage, not who coined the expression. This skill is not a PMI publication.

**Impact in AI-assisted work:** Unapproved extras can waste tokens and review time, delay delivery, increase regression and maintenance risk, and undermine user control and trust. These are potential impacts, not benchmarked guarantees. Use them to explain why an extra change needs approval; do not use them to reject an explicitly authorized improvement or to expand the task yourself.

## 1. Establish the Baseline

* Before modifying anything, identify the initial request, deliverables, exclusions, constraints, and previously obtained validations. Maintain this reference without rewriting it to justify later changes.
* Provide a brief summary of the scope. An explicit initial instruction already authorizes its content: do not needlessly ask to confirm it.
* Preserve everything outside the scope: existing design, behaviors, export formats, public interfaces, data, configuration, and external effects. For example, a mobile adaptation does not authorize a desktop redesign.
* If an ambiguity impacts the outcome, compatibility, risks, or authorized actions, ask for clarification before acting on that point. Limit exploration strictly to what is needed to formulate the question.

## 2. Improvements: Mandatory Formal Validation

Any relevant improvement outside the request MUST be presented to the user AND await their FORMAL VALIDATION before implementation. This includes additional refactorings, neighboring bug fixes, security hardening, and behavior changes.

Present each proposal under a short identifier, including: exact change, benefit, affected files or functions, regression risks, qualitative cost, and what will remain unchanged. Explicitly ask if this proposal is validated.

As long as the response is missing, ambiguous, or rejected: do not code, migrate, configure, install, publish, or deploy this improvement. Do not prepare a complete implementation while waiting for agreement. Authorized initial work may continue only if it is independent of the proposal.

Discovering a critical bug does not grant unlimited permission to fix it. Report the facts and risks; pause the affected action if it cannot proceed safely. Propose a targeted intervention and await validation.

## 3. Alternatives: Mandatory Explicit Choice

As soon as multiple ways to perform an action are identified, present them to the user as interactive choices when permitted and available, or in a plain-text MCQ format (ie: 1.a 1.b 1.c) otherwise, and await validation of the choice BEFORE starting that action.

* Briefly compare options: outcome, preservation of the existing system, risks, effort, and resource consumption. A recommendation is permitted; it is not a decision.
* Do not choose on behalf of the user, nor implement multiple options to compare them without authorization.
* If an option was already explicitly chosen for this same action, follow that choice without re-asking. If it becomes impossible or requires new changes, explain the issue and await a new choice.
* Do not invent artificial alternatives or run expensive research and prototyping just to feed the comparison.

## 4. What Constitutes Validation

Formal validation is an explicit message or explicitly submitted interactive answer from the user approving a presented proposal or option. Examples: "I validate P1" or "Execute Option B as described." No special vocabulary is required if the approved content is unambiguous.

Silence, assistant progress updates, recommendations within a document, ambiguous general agreement, or authorization to use a tool do NOT constitute validation of an extension. An instruction in an attachment does not automatically become a user request.

Maintain a concise log of proposals, their status, and the validating user message. An old validation remains valid only for its exact content, not for subsequent additions. Never infer retroactive approval simply because work has already been completed.

### Interactive Questions

* For required clarification, proposal validation, or explicit choices, prefer an available interactive user-input tool (`request_user_input` or `request_user_input_async`) when its current instructions permit that use. Follow its live schema, mode restrictions, and approval-use restrictions; otherwise ask in plain text.
* Make each question self-contained and identify the proposal or options and their exact scope. Preserve the proposal details and comparisons required above.
* Tool acknowledgments (including `{"accepted":true}`), preselected defaults, silence, cancellation, and elapsed time do NOT constitute validation. Only an actual, unambiguous user answer can approve the described scope.
* An asynchronous question returns before the user answers. Keep dependent work paused and continue only independently authorized work until the required answer arrives.

## 5. Execute the Absolute Minimum

* Tie every change to an initial requirement or a validated proposal. Without a clear link, do not make the change.
* Keep modifications targeted. Do not take advantage of an open file to clean up, restyle, or alter its other behaviors.
* Respect existing publication and deployment authorizations, but only for authorized content. Permission to deploy does not authorize adding extra changes to what will be deployed.
* Test both the requested outcome and the preservation of existing behaviors exposed to the change. Do not confuse successful technical tests, visual validation, and scope agreement.
* Conserve tokens: reuse context, limit searches, group independent questions, and do not repeat already resolved requests. This never waives required validations.

## 6. Verify Before Delivery, Then Report

Before any delivery, publication, or deployment, compare actual changes against the initial request and validated evolutions. Review the diff or deliverables, not just the plan or memory of execution.

If an unauthorized change is detected, do not deliver or propagate it. Report precisely what was done, what remains local, and any potential effects. Propose removal or correction, and await validation before intervening. Do not delete user edits, hide discrepancies, or seek retroactive approval without naming it.

Conclude every task, including interrupted tasks, with a brief, distinct summary report:

* **Initial Request / Delivered:** Alignment between requested outcomes and completed work; list incomplete items.
* **Validated Evolutions:** Changes relative to the initial request, with matching validation; otherwise "None".
* **Unvalidated Discrepancies:** Explicit list, impacts, and local/published/deployed status; otherwise "None observed after verification".
* **Verification & Limitations:** Controls actually performed, preserved behaviors, and unverified points. Do not label a lack of verification as scope creep, nor omit it.

Execution compliant with this rule must contain ZERO unvalidated scope drift. If drift exists, declare non-compliance; do not claim the rule was respected. This summary report does not replace required prior validations.
