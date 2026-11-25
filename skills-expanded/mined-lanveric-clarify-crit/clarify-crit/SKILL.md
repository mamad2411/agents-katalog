---
name: clarify-crit
version: 1.2.1
description: Refines complex, incomplete, ambiguous, conflicted, or high-consequence requests using Context, Role, Interview, and Task. Use when the user invokes CRIT or Clarify, asks for a request or prompt to be clarified, or when unresolved material uncertainty could change the deliverable, method, risk, cost, approval, or success criteria. Do not activate automatically for straightforward work that can be completed safely with supplied context or conventional defaults.
---

# Clarify (CRIT)

Clarify improves uncertain requests through the **CRIT** method — **Context, Role, Interview, and Task**.

## Governing principle

Use the least interaction and least visible structure required to remove material uncertainty and produce a correct, executable result.

CRIT must reduce total interaction cost. It should not turn ordinary work into a visible framework exercise.

## Activation

Use CRIT when the user explicitly invokes it by name (`CRIT` or `Clarify`).

Activate it automatically only when both conditions are true:

1. unresolved material uncertainty exists; and
2. resolving that uncertainty is likely to improve the result enough to justify the interaction.

Complexity alone is not sufficient. Do not activate automatically for factual questions, translations, simple calculations, straightforward rewrites, casual conversation, or complete requests that can be executed safely as written.

When explicitly invoked for a simple request, apply CRIT lightly and avoid unnecessary structure.

## Core rules

1. **Reuse context first.** Do not ask for information already present in the conversation, supplied files, instructions, accessible tools, or connected sources.
2. **Resolve only material uncertainty.** A detail is material only when it could change the deliverable, method, risk, cost, approval, or success criteria.
3. **Aim for zero questions.** Ask one when possible. Use up to three in a bounded clarification turn and four only for high-stakes or formal discovery.
4. **Resolve foreseeable blockers together.** Use another clarification turn only when the user's answer introduces a new material dependency.
5. **Route unknowns efficiently.** Reuse, research, ask, default, or ignore. Do not convert every unknown into a user question.
6. **Keep the reasoning non-visible by default.** Do not narrate request classification, role selection, hypothetical interpretations, or internal framework steps unless the user needs that information.
7. **Preserve intent.** Improve the route to the user's stated outcome without replacing it with a larger or different project.
8. **Use reversible defaults.** Proceed when a conventional, low-risk choice can keep the work moving. State it only when consequential.
9. **Display a brief only when useful.** A visible brief is required for handoff, prompt-only work, approval, formal specification, or when it has independent value. Otherwise refine internally and execute directly.
10. **Avoid ceremonial text.** Omit generic praise, framework announcements, repeated permission requests, and non-functional closings.

## Decision procedure

### 1. Determine the request state

- **Clear:** executable with supplied context or safe defaults.
- **Ambiguous:** multiple plausible interpretations would materially change the result.
- **Incomplete:** the objective is known, but an essential constraint, preference, fact, or approval is missing.
- **Undefined:** the objective itself needs discovery or narrowing.
- **Conflicted:** supplied requirements cannot all be satisfied together.

When ambiguity is uncertain, compare two plausible interpretations internally. Clarification is material only if they would lead to meaningfully different outputs, methods, risks, costs, approvals, or success criteria.

For conflicted requests, identify the smallest incompatible requirement pair and ask for the governing priority or propose the safest trade-off.

### 2. Route each material unknown

Use the first suitable route:

- **Reuse:** retrieve the answer from available context or an explicitly accessible source.
- **Research:** verify a material external fact when reliable tools or sources are available and the value of verification exceeds the retrieval cost.
- **Ask:** only the user can supply the preference, approval, inaccessible private fact, or value judgment.
- **Default:** use a low-risk, reversible convention that preserves the objective.
- **Ignore:** the detail does not materially affect the result.

Do not ask the user to research facts that accessible sources can verify more reliably.

### 3. Select the least intervention

Use modes internally only; do not announce them unless useful.

- **Quick:** clear or lightly incomplete; usually no question.
- **Standard:** bounded ambiguity or several important constraints; resolve blockers in one turn using no more than three critical questions.
- **Deep:** high-stakes, architectural, strategic, research-heavy, multi-phase, or formally exploratory; use no more than four critical questions per turn.

Deep mode permits more reasoning, not more visible ceremony.

### 4. Use roles sparingly

Select one primary professional perspective internally. Add another only when a distinct discipline materially changes the method or risk assessment.

Show a role only when it improves handoff, explains a method, or identifies a meaningful professional boundary. Do not invent expert panels or narrate fictional debate.

### 5. Ask response-efficient questions

Ask only questions whose answers could change scope, method, deliverables, safety, cost, approval, or success criteria.

- Combine related decisions.
- Resolve all currently foreseeable blockers in one turn where possible.
- Offer a recommended default when it reduces effort without concealing risk.
- Use the smallest set of meaningfully distinct options that covers the decision; two to four is usually sufficient.
- Use a bounded open question when the option space is not genuinely closed.
- Defer improvement-only questions unless deeper discovery was requested.
- Never repeat a resolved question.

### 6. Pause or proceed

Pause only when:

- an unanswered issue materially blocks safe or correct execution;
- approval or authorisation is required;
- requirements remain materially conflicted; or
- proceeding would require a consequential unsupported assumption.

Otherwise proceed using stated low-risk defaults. Do not create confirmation loops.

## Outcome selection

Choose the smallest useful outcome:

### Direct execution

Refine internally and perform the task when the same model can execute it safely and a visible brief would add no independent value.

Expose only consequential assumptions, limitations, or unresolved dependencies.

### Visible execution brief

Produce a self-contained brief when:

- the user requested a prompt or specification;
- another person or model will execute the work;
- approval is needed before execution;
- the brief is itself a deliverable; or
- the task is complex enough that a reviewable specification has independent value.

### Provisional brief with blocker

When execution is blocked, show:

1. the smallest decision needed;
2. a recommended default when appropriate; and
3. a provisional brief containing everything already established.

Do not ask the user to restate resolved information.

## Execution brief contract

Include only fields that add distinct execution value:

- **Objective**
- **Deliverables**
- **Requirements and constraints**
- **Success criteria**
- **Output format**, when not obvious
- **Assumptions/defaults**, when consequential
- **Risks or dependencies**, when material
- **Out of scope**, when scope drift is likely

A portable brief must contain every execution-critical fact or explicitly identify an accessible source. Avoid phrases such as `as discussed`, `the file above`, or `use what we decided earlier`.

Do not duplicate the same information in separate Context and Task reports.

## Runtime quality gate

Before responding, silently check:

1. **Intent:** Does the result preserve the user's actual objective?
2. **Uncertainty:** Could any unresolved interpretation materially change the result?
3. **Routing:** Can each proposed question instead be answered by reuse, research, a safe default, or omission?
4. **Interaction:** Are all foreseeable blockers handled in the current turn?
5. **Visibility:** Does every visible heading and sentence help the user decide, approve, hand off, or execute?
6. **Portability:** When a brief is shown, can another capable model execute it without prior conversation?
7. **Action:** Is the next required action unambiguous?

## Conditional references

The core procedure above is sufficient for ordinary use. Consult references only when needed:

- [`references/response-patterns.md`](references/response-patterns.md) when a visible response structure is useful but unclear;
- [`references/examples-and-edge-cases.md`](references/examples-and-edge-cases.md) for unusual, mixed, or difficult request states;
- [`references/failure-modes.md`](references/failure-modes.md) when reviewing or correcting behavioural drift.

Do not load every reference by default.
