---
name: thirdshift-to-spec
description: "Turn the current session into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already settled. For an Architecture review or Security fix publishing."
disable-model-invocation: false
---

This skill takes the current session context and codebase understanding and produces a spec. Nobody is there to interview or to ask; just synthesize what you already know.

The issue tracker and triage label vocabulary should have been provided to you. If `docs/agents/issue-tracker.md` is missing, fall back to `gh issue create`. If `docs/agents/triage-labels.md` is missing, use the label names as written here, creating a label the tracker lacks (`gh label create`).

The spec is all this skill writes. Write nothing to the repository: no spec file, commits or branches. A `GLOSSARY.md` or ADR change the spec needs is work for one of its tickets.

For **Security fix publishing**, the Session prompt overrides the template: keep the Spec terse, saying only what the fix changes and linking the private record. Keep all finding evidence in that record. On a private repository, use the finding's existing issue as the Spec and preserve its body and evidence; publish its Tickets with `thirdshift-to-tickets`.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Sketch out the seams at which the feature will be tested. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

Decide the seams yourself and record them, with the reason for each, under Testing Decisions.

3. Write the spec using the template below, then publish it to the project issue tracker. Apply the `needs-triage` triage label and no other: thirdshift marks the spec ready once the session has ended and the plan passes its checks.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made, each with its reason. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made, each with its reason. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- The seams the feature will be tested at
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
