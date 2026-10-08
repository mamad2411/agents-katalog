---
name: save-as
description: "Use when the conversation has converged and a written spec is needed — pure synthesis of what was already discussed, no new questions."
disable-model-invocation: true
---

# Save As

The conversation is the source document; the spec is its export. Combine what the user decided with what the codebase reveals and write it down as a spec (a PRD, if you prefer that label). The moment has passed for asking questions — this is a synthesis step. A decision that turns out to have never been discussed goes into Open Questions at the end of the spec, untouched by you.

## Process

1. **Ground the spec in the repo.** If the codebase hasn't been surveyed yet, do that now. Write with the project's domain glossary vocabulary and honor any ADRs in the affected area.

2. **Choose the testing seams.** Favor the seams the codebase already has over inventing new ones, pick the highest available, and keep the count minimal — one is the ideal. Get the user's confirmation that these are the seams they expect to be tested at.

3. **Draft and publish the spec** from the template below into the project's issue tracker, applying the `ready-for-agent` label — **publish only after the user approves the drafted spec** (writing to a shared tracker is an external action; Iron Law 4). No extra triage pass needed.

4. **Pin the Constraints.** Every non-negotiable the implementation must respect — quality floors, performance and security limits, hard prohibitions — lands in the Constraints section. Execution and review will treat this section as binding material; a floor agreed here cannot be negotiated down later.

5. **Attach Acceptance Criteria** (see the template section) covering every requirement — exactly one criterion per requirement, each phrased so it can genuinely FAIL against shipped code. "The code should be good" cannot fail, so it is prose wearing a criterion's clothes: rewrite it or cut it. This section is the upstream gate — downstream verification proves behavior, never intent, so a spec that reaches decomposition without executable acceptance criteria can ship the wrong thing with every test green. Required for class `loop`; for `full` it is recommended without being enforced.

6. **Attack your own spec before anyone else does.** Run the adversarial self-review below, then publish. Translating conversation into document is precisely where new ambiguity creeps in, and this review runs while the reasoning is still in context — the one moment synthesis drift is cheap to see and cheap to fix.

## Acceptance Criteria

A numbered list. Each item:

- Maps 1:1 to a requirement or user story in this spec (traceable, cite the story number).
- Is phrased as a falsifiable assertion — a condition that can be checked to be TRUE or FALSE against the delivered work, never a value statement.
- Carries its check method: automated test, browser check with real data, or explicit human verification.

## Adversarial self-review

Before publishing, read the spec against itself and the codebase and report (then fix) every finding:

- **Ambiguity** — any sentence two implementers could read differently (named examples, vague quantifiers, undefined terms against the project's glossary).
- **Contradiction** — any two sections that cannot both hold (a Constraint that defeats a User Story, an Acceptance Criterion the Solution cannot produce).
- **Hidden assumption** — anything the spec depends on but never states (existing behavior, environment, data shape); surface it into Constraints or Open Questions.
- **Untestable criteria** — any Acceptance Criterion that cannot genuinely fail; rewrite it until it can, or move the intent to Open Questions.

Findings are fixed in the spec before publishing — publishing with a known unreviewed finding is the "it's fine trust me" of specs.

<spec-template>

## Problem Statement

The problem the user is facing, from the user's perspective.

## Solution

The solution, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each in the format:

1. As a <actor>, I want a <feature>, so that <benefit>

This list should be extremely extensive and cover all aspects of the feature.

## Decisions Already Made

Every decision already made, recorded as a list. Typical contents:

- Modules to build or modify
- Interfaces of those modules that change
- Clarifications the developer gave along the way
- Architectural choices
- Schema changes
- API contracts
- Interaction details

Do NOT include specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts.

## Testing Decisions

How testing will work, recorded as a list:

- What counts as a good test here (external behavior only, never implementation details)
- The modules that will be tested
- Prior art (similar types of tests already in the codebase)

## Constraints

Non-negotiable rules binding execution: quality floors, runtime/target limits, accessibility needs, specific prohibitions.

## Acceptance Criteria

Numbered, falsifiable assertions — one per requirement (cite the user-story number), each carrying its check method (automated test / browser with real data / human verification). A criterion that cannot fail is prose, not a criterion.

## Out of Scope

Things that are out of scope for this spec.

## Open Questions

Decisions that were never discussed — do not fill in speculative answers.

</spec-template>
