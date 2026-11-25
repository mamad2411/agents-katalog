---
name: write-a-prd
description: Convert a plan-ready planning brief or completed conversation into a durable PRD while preserving behavioral scenarios, implementation decisions, testing seams, acceptance proof, research evidence, non-goals, and unresolved checkpoints. Use after talk-it-through when a product-facing PRD is useful before to-plan.
---

# Write a PRD

Transform settled planning evidence into a product and implementation specification that a fresh
`to-plan` session can use without the original conversation. Do not reopen the interview and do not
invent missing decisions.

## Source

Prefer a `write-planning-brief` artifact passed as an argument. Otherwise use a supplied decision
document or the current completed planning conversation. Read referenced research, design, domain,
or decision artifacts only where the PRD depends on them. Verify current-state claims against the
repository when material.

If the source is marked `More decisions required`, produce a draft PRD that preserves every
unresolved checkpoint and mark it `Not ready for to-plan`. Do not hide uncertainty inside prose.

## Output

Accept an optional output path. Otherwise use the repository's established PRD convention, then
`plans/prds/<topic-slug>.md` when `plans/` exists, or `docs/prds/<topic-slug>.md` otherwise. Update an
existing PRD for the same topic rather than creating a competing source of truth.

Write prose through `write-well` after the factual structure is complete. Style work must not remove
requirements, qualifications, citations, or uncertainty.

## Required PRD

```markdown
# <Feature>

## PRD status
Ready for to-plan | Not ready for to-plan

## Problem statement
<The affected actor's problem and consequences.>

## Solution
<The resulting capability from the user's perspective.>

## Current state and constraints
<Relevant verified behavior, compatibility, policy, and environmental constraints.>

## User stories
<Numbered user stories covering every material actor and behavior without duplicative filler.>

## Behavioral requirements
### Happy path
### Repeat use and idempotency
### Failure and retry
### Cancellation, resume, and cleanup
### Permissions and trust boundaries
### Relevant edge cases

## Acceptance criteria
- <Observable criterion with an identifiable proof method>

## Implementation decisions
For each settled material decision:
- **Decision**: <contract, schema, interaction, module boundary, or policy>
- **Reason**: <decision-relevant rationale>
- **Important alternatives**: <durable rejected alternatives and decisive reason, or `None recorded`>
- **Consequences**: <constraint inherited by planning>

## Domain language
<Precise project-specific terms whose meaning constrains the work, or `No new domain terms`.>

Avoid volatile file paths and implementation snippets unless a decision cannot be represented
accurately without a small state-machine, schema, reducer, or type shape.

## Testing decisions
- **Behavioral test standard**: <public behavior rather than implementation detail>
- **Primary seams**: <highest stable seam for each behavior group>
- **Existing precedent**: <repository pattern or source pointer>
- **Highest-level proof**: <assembled journey, integration, provider, or platform proof>
- **Manual proof**: <only what cannot be automated, with reason and failure signal>

## State, data, and external dependencies
<Persistence, ownership, migration, integration, rollout, compatibility, and failure policies.>

## Security and human checkpoints
<Trust-boundary, destructive-data, or unavoidable manual decisions, or `None`.>

## Out of scope
<Explicit non-goals and adjacent behavior deliberately excluded.>

## Research evidence
- [<artifact or primary source>](<path-or-url>) — <decision-relevant conclusion>

Use `No external research required` when applicable.

## Unresolved checkpoints
<Question, consequence, and next decision/evidence step, or `None`.>

## Planning constraints
<Task dependencies, ordering, slicing, rollout, and compatibility constraints inherited by `to-plan`.>

## Further notes
<Only durable information not represented above.>

## Source coverage
<Planning brief and authoritative artifacts used.>
```

## Coverage and readiness audit

Before returning, compare the PRD against the planning brief or conversation and verify:

- every target behavior and actor is represented;
- happy, repeat, failure, cancellation, resume, cleanup, and edge scenarios are included or marked
  not applicable with a reason;
- every settled material decision, important rejected alternative, domain term, planning constraint,
  and explicit non-goal survived the transformation;
- testing decisions and highest-level acceptance proof are explicit;
- research-dependent claims retain claim-level citations or artifact links;
- security, destructive-data, compatibility, and rollout constraints are not softened;
- unresolved checkpoints are preserved rather than silently answered;
- user stories add coverage rather than repetitive volume; and
- source coverage is complete enough that `to-plan` does not need the original conversation.

Mark `Ready for to-plan` only when no unresolved checkpoint could change behavior, architecture,
risk, proof, or task boundaries. Return the PRD path, status, unresolved checkpoint count, and
`/skill:to-plan <prd-path>` when ready.
