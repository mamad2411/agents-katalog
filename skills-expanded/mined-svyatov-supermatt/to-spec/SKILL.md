---
name: to-spec
description: "Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed."
disable-model-invocation: true
argument-hint: "[wayfinder map or issue reference]"
license: MIT
---

This skill takes the current conversation context and codebase understanding and produces a spec. Synthesize what you already know instead of re-grilling the idea: you ask the user only the seam check in step 2 and any step 4 finding that needs a decision.

Read `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md` first. If either is missing or unreadable, stop and tell the user to run `/setup-supermatt-skills` in Claude linked installs or Cursor, `/supermatt:setup-supermatt-skills` from the Claude plugin, `$setup-supermatt-skills` in Codex, or `/skill:setup-supermatt-skills` in OMP. Resume only after both required docs exist and have been read.

If the user passes a reference, fetch it with the tracker doc's **Read an issue** command. For a `wayfinder` map, the decisions live in one of two places. When the map names a written destination (a spec or ADRs a ticket already assembled), read that destination: it is the decision record, and you fetch a linked ticket only where the destination is silent. Otherwise fetch every ticket its **Decisions so far** section links: those tickets hold the decisions the spec collapses into a plan.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better: the ideal number is one.

Check with the user that these seams match their expectations.

3. Write the spec using the template below. Don't publish it yet.

4. Check the draft in a fresh context. This context wrote the spec, so it shares the spec's blind spots. Spawn one sub-agent with the draft, repo access, and the authoritative destination and fetched decision records from the map. Where records are passed as retrievable references instead of full text, include the tracker instructions needed to fetch them. Give it this brief: "Report: (a) places where the spec contradicts itself, or a user story conflicts with an implementation decision or Out of Scope; (b) implementation decisions that the current codebase cannot support as written, citing the file; (c) user stories that no implementation or testing decision covers; (d) when the spec came from a decision record (a map's destination or tickets), decisions that contradict it or settle what it never settled. Quote the spec line for each finding. Under 300 words."

If subagents are unavailable, use a fresh session with the same draft, repo access, authoritative decision records or retrievable references and tracker instructions, and brief where possible. Otherwise review the draft yourself and disclose the lack of independent review before publishing.

Fix the findings that have one clear fix. A finding that needs a decision goes to the user before you publish.

5. Publish the spec to the project issue tracker. Apply the configured `ready-for-agent` role (a label on hosted trackers, `Status:` locally): it needs no further triage.

When the spec came from a `wayfinder` map, start its body with `## Parent` and the map's canonical reference (`#<number>` on GitHub, `TEAM-123` or its URL on Linear, a Markdown path/link locally). On Linear also set the map as the native parent. After publishing, comment the spec's link on the map and close the map as completed: the spec is its destination.

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

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

When a provider and consumer evolve or deploy independently, name one authoritative contract, its owner, and how each side will be checked against it. Include actual serialization and consumer fixtures in the testing decision, with relevant error, null, mock, and feature-flag paths. For components changed and built atomically, an existing shared type can be that contract; require an additional schema or generator only for a concrete gap.

Name modules and their interfaces, not source file paths or code snippets: those go stale fast. Two kinds of path are durable and belong in the spec: a document the spec builds on (a behavioural spec, an ADR), and the existing tests named as prior art.

For an approved file-migration map, preserve its exact source and destination paths and all preserved path contracts in a dedicated `## Migration map` section. These are requirements, not optional implementation details; carry the complete approved map into the published spec so tickets and fresh implementation sessions can retrieve it. This is a conditional exception to the source-path rule above.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype, citing its `prototype/<name>` branch. Trim to the decision-rich parts, not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- The seams under test, as agreed with the user in step 2
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
