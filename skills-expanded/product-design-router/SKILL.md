---
name: product-design-router
description: Diagnose the highest-risk unknown in product design or independent product-building work, establish decision ownership, and compose the smallest useful skill loop. Use when the user is unsure what work should happen next, has mixed artifacts from different stages or surfaces, or wants to avoid mechanically following a lifecycle. Do not use to replace a clearly requested specialist skill.
---

# Product Design Router

Route by uncertainty, not by lifecycle stage.

## Start from what exists

Inspect the supplied brief, research, prototype, code, analytics, feedback, constraints, and decision records. Do not require discovery artifacts merely because they traditionally come first. If the user has already named a concrete specialist task, preserve that intent and invoke that skill directly unless a missing decision would make the work misleading or unsafe.

## Establish the collaboration and decision spine

Before choosing a skill, make the smallest shared working state explicit:

- the current working artifact or source of truth, including its version when relevant;
- the product decision and the person accountable for making or approving it;
- the people and agents contributing evidence, generation, critique, or implementation;
- the working surface where the uncertainty can best become observable: source evidence, canvas, prototype, code, or a live product signal;
- what AI may propose or execute and what requires human review or approval.

Do not invent an organization chart. One person may own several responsibilities in an independent-builder context. Record only the ownership and authority boundaries needed for the current decision.

## Diagnose the decision

1. Name the product decision the user is trying to make.
2. Separate known evidence, inference, assumption, preference, and confirmed decision.
3. Identify the unknown most likely to cause failure or expensive rework:
   - `Value`: wrong user, buyer, problem, outcome, or alternative;
   - `Meaning & Structure`: incoherent objects, relationships, states, rules, IA, or permissions;
   - `Experience & Judgment`: unclear interaction, content, usability, accessibility, or quality bar;
   - `Feasibility & Reliability`: implementation, performance, safety, recovery, or operational risk;
   - `Adoption & Market`: weak positioning, channel, activation, pricing, retention, or distribution;
   - `Learning & Governance`: missing instrumentation, interpretation, provenance, approval, or decision memory.
4. Prefer the unknown whose answer would most change the product, not the one with the easiest artifact.
5. Choose the working surface that exposes the unknown most directly. Do not default to a canvas, document, prototype, or code merely because it is convenient or fast.
6. Propose the smallest loop that can produce credible evidence. Usually select one primary skill and at most two supporting skills.
7. Assign only the collaboration needed for that loop: who supplies context, who creates or changes the artifact, who evaluates it, and who owns the decision.
8. Define an exit condition: what evidence would support, reject, or reframe the current decision.

Use [references/CAPABILITY-NETWORK.md](references/CAPABILITY-NETWORK.md) only when choosing among multiple nodes or composing a cross-node loop.

## Output

```markdown
## Entry state
- Working artifact / source of truth:
- Current working surface:

## Decision now

## Highest-risk unknown
- Node:
- Why now:
- Evidence already available:
- Missing evidence:

## Collaboration & decision spine
- Decision owner:
- Contributors and agents:
- AI may:
- Human review / approval:

## Smallest useful loop
1. Primary skill — question it should answer
2. Optional supporting skill — only if required

## Exit condition

## After the loop
- Update:
- Next unknown, if any:
```

## Boundaries

- Do not present a complete skill catalog when one next action is enough.
- Do not treat a polished PRD, mock, prototype, or codebase as proof that upstream decisions are settled.
- Do not invent research, analytics, constraints, or user consent.
- Do not optimize for artifact completion; optimize for evidence that can change a decision.
- Do not treat a shared canvas or real-time generation as shared understanding; make the decision, evidence, and owner explicit.
- Do not assign AI final authority over ambiguous, high-impact, or irreversible product decisions.
- High-risk legal, medical, financial, security, privacy, or irreversible decisions require the relevant specialist review and human approval.
- Designer and Builder profiles adjust default emphasis only; they never force a fixed sequence.

The route is complete when the user can see why this unknown matters now, where the work should happen, which minimal capability to invoke, who owns the decision, and what new evidence will end the loop.
