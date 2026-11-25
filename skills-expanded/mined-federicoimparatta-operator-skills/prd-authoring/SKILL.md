---
name: prd-authoring
description: Use this skill when the user asks to write, draft, structure, or revise a Product Requirements Document. Trigger phrases include "write a PRD", "draft a product spec", "turn this into a PRD", "PRD for X", "escribir un PRD", "spec this feature", "product brief". Produces a PRD as a hypothesis, not a spec. Scales sections to the maturity of the feature. Works in English and Rioplatense Spanish.
---

# prd-authoring

> **Anchor:** A PRD is a hypothesis, not a spec. Reduce uncertainty, not scope.

## When to use

Use this skill when the user needs to write or restructure a product requirements document for a feature, surface, or initiative. Works for:

- A new feature that needs alignment before build.
- An existing feature that needs a retroactive PRD for handoff or audit.
- A discovery-stage concept that needs to be reduced to a testable hypothesis.

Do not use when:

- The user is proposing a feature pre-scoping. Use `feature-proposal` instead.
- The user is scoping delivery work (time, phases, commercial). Use `proposal-scoping`.
- The user is triaging existing tickets. Use `ticket-triage`.

## Philosophy

A PRD is a hypothesis under uncertainty. It is a bet, placed in writing, with kill criteria and instrumentation that will tell you whether the bet paid off. Treating it as a contract for engineering is a category error. Treating it as a creative document is a cost the team pays for months.

Five concepts from the handbook apply directly. **Output vs outcomes:** write what should change in user behavior or system state, not what the team will produce. **Product as a portfolio of bets:** the PRD names the bet and its size. **Reduce uncertainty, not scope:** the shortest PRD is not the best; the PRD that kills the riskiest unknown first is. **PM as anthropologist:** the problem statement comes from observation, not invention. **Discovery is a practice:** the PRD carries evidence of what has already been validated and what has not.

## Voice rules (apply to all outputs)

- No buzzwords: leverage, empower, synergy, resonate, tapestry, delve, elevate, captivate, explore, dynamic, testament.
- No em dashes.
- No filler openings.
- Decision-oriented over descriptive.
- High-context, no overexplaining.
- Standard sentence case for formal outputs.
- ES outputs match the register of the handbook: direct, self-aware, no reverence for process, comfortable naming failure.
- EN outputs use direct US business register. Do not soften bluntness into corporate-speak.
- Language switches based on audience, not author.

## Bilingual handling

- **ES.** Rioplatense register. Vos over tú. Keep technical terms in English where that is standard in industry use: PRD, backlog, sprint, stakeholder, rollout, feature flag, AB test, KPI. Do not translate those to Spanish equivalents that no one uses in meetings.
- **EN.** Direct US business register. Short sentences. No British spelling unless the target audience is UK or AU.
- Choose the language of the audience that will read the document, not the language the user types in. Ask once if ambiguous.

## Method

### Step 1. Classify the feature by maturity

Pick one. This decides which template to use.

| Maturity | Signals | Template |
|---|---|---|
| Discovery | Problem is not yet confirmed. No user interviews. No data. | `prd-lean` |
| Shaping | Problem confirmed. Solution space open. Some data. | `prd-lean` |
| Build | Solution committed. Dependencies mapped. Timeline real. | `prd-full` |
| Post-hoc | Feature shipped. PRD written for handoff or audit. | `prd-full` |

When in doubt, use `prd-lean`. Full PRDs written too early are expensive fiction.

### Step 2. Write the problem before anything else

Do not open the document with scope. Open it with the problem.

The problem statement answers four questions:

1. **Who feels it.** A specific user type, not "users" or "customers".
2. **When they feel it.** A moment in the product, a frequency, or a trigger.
3. **What they do today.** The current workaround, detour, or resignation.
4. **What that costs.** Time, revenue, churn, support load, or a strategic gap.

If you cannot answer all four, the PRD is not ready. Flag the gaps instead of guessing.

### Step 3. State the hypothesis

Format:

> If we ship **X** for **user Y**, we expect **metric Z** to move by **roughly W**, because **reason R**.

This forces scope, audience, metric, magnitude, and causal logic into one sentence. If the sentence is vague, the PRD is vague.

### Step 4. Define scope by exclusion

Write three lists:

- **In.** What we are committing to build now.
- **Out.** What we are choosing not to build now, and why.
- **Not ever.** What we believe is wrong for this feature, not just deprioritized.

The **Out** list is the most important. It is where teams lose months.

### Step 5. Write acceptance criteria in user-observable terms

Each criterion is something a user or another system could verify without access to the codebase. "User receives an email within 5 minutes of event X" is a criterion. "The queue retries twice on failure" is a system note, not an acceptance criterion.

### Step 6. Name the instrumentation before the build

Before the feature ships, define:

- Which events fire.
- Which property shape they carry.
- Which funnel they roll up into.
- Which dashboard they populate.
- Who owns that dashboard.

If the PRD does not name these, you will not know whether the bet paid off. Cross-reference `analytics-instrumentation` if the taxonomy does not yet exist.

### Step 7. Name the kill criteria

A PRD without kill criteria is a one-way door. Write:

- What result or signal would cause us to roll back.
- What result or signal would cause us to pause and rethink.
- How long we wait before checking.

### Step 8. List the open questions

Every non-trivial PRD has open questions. Write them down with an owner and a deadline. Do not bury them in slack threads.

### Step 9. Read the PRD as a stranger

Before handing off, read it as someone who was not in the conversation. If a sentence only makes sense with prior context, fix it or move it to a linked appendix.

## Templates

- `templates/en/prd-lean.md`: discovery and shaping stage.
- `templates/en/prd-full.md`: build and post-hoc stage.
- `templates/es/prd-lean.md`: etapa de discovery y shaping.
- `templates/es/prd-full.md`: etapa de build y post-hoc.

## Related skills

- `feature-proposal`: use it first when the feature is a pre-scoping bet, not a committed build.
- `proposal-scoping`: use it when scoping delivery work (time, phases, commercial), not product behavior.
- `analytics-instrumentation`: cross-reference it to build the instrumentation section when the taxonomy does not yet exist.
- `ticket-triage`: use it when the work is triaging existing tickets rather than writing a spec.

## Anti-patterns

This skill must never produce:

- A PRD that opens with a solution or a screen.
- A PRD that lists features without naming the problem they solve.
- A PRD that has no instrumentation section.
- A PRD that uses "users" or "customers" as the only audience descriptor.
- A PRD that treats engineering estimates as commitments before scope is settled.
- A PRD that hides open questions inside meeting notes instead of surfacing them.
- A PRD written in the style of a press release when the audience is internal.
- A PRD with acceptance criteria that require reading the codebase.
- A PRD that mixes English and Spanish inconsistently within a single section.
- A PRD that cites "industry best practice" without a concrete internal reason.

## Checklist before delivery

- [ ] Problem statement answers the four questions in step 2.
- [ ] Hypothesis is a single sentence in the step 3 format.
- [ ] **Out** list has at least three items.
- [ ] Acceptance criteria are user-observable.
- [ ] Instrumentation section names events, properties, and an owner.
- [ ] Kill criteria are concrete and time-bounded.
- [ ] Open questions each have an owner and a deadline.
- [ ] No buzzwords from the voice rules appear anywhere.
- [ ] Document reads cleanly to a stranger who was not in prior meetings.
