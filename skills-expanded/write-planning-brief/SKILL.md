---
name: write-planning-brief
description: Distill a completed planning discussion and its cited evidence into a durable, plan-ready local brief without reopening the interview. Use at the end of talk-it-through or when a conversation must become reliable input for write-a-prd or to-plan.
---

# Write Planning Brief

Write a durable source document from the current planning conversation and any supplied decision,
research, prototype, or design artifacts. Do not interview the user and do not implement or create
plan tasks. When information is missing, preserve the gap and mark the brief `More decisions
required` rather than inventing an answer.

## Source and output

Accept an optional topic, source paths, and output path. Verify repository-state claims against disk
and reference authoritative artifacts by path or URL instead of duplicating them.

Choose the output path in this order:

1. a path supplied by the caller;
2. the repository's established decision/planning-document convention;
3. `plans/decisions/<topic-slug>.md` when `plans/` exists;
4. `docs/planning/<topic-slug>.md` otherwise.

Create parent directories when needed. If a brief for the same topic already exists, update that
file after reading it; do not create competing sources of truth. Never overwrite a different topic.

## Distillation rule

Capture every durable requirement, decision, constraint, non-goal, evidence pointer, and unresolved
checkpoint needed by a fresh planner. Do not copy the transcript, exploratory chatter, temporary
misunderstandings, raw research output, or repository search output. Preserve an important rejected
alternative only when its rationale prevents a future agent from reopening or reversing a material
decision accidentally.

Distinguish verified facts, user decisions, recommendations the user accepted, and unresolved
uncertainty. Do not present an agent recommendation as a user decision.

## Readiness gate

Use exactly one planning status:

- `Ready for planning`: observable behavior, boundaries, material scenarios, dependencies, testing
  decisions, and acceptance proof are sufficient for safe vertical slicing, with no blocking
  unresolved checkpoint.
- `More decisions required`: any missing decision could materially change behavior, architecture,
  risk, proof, or task boundaries.

A nonblocking future enhancement can remain out of scope without preventing readiness. A factual
unknown that controls implementation or acceptance is blocking.

## Required document

Write this structure, omitting only optional subsections explicitly marked optional:

```markdown
# <Topic>

## Planning status
Ready for planning | More decisions required

<One sentence explaining the readiness verdict.>

## Problem and destination
<Problem from the affected actor's perspective and what reaching the destination means.>

## Current state
<Relevant verified behavior, constraints, and source pointers.>

## Target behavior
<Observable resulting behavior.>

## Actors and permissions
<Actors, ownership, authorization, and relevant trust boundaries, or "No special permissions".>

## Scenarios
### Happy path
### Repeat use and idempotency
### Failure and retry
### Cancellation, resume, and cleanup
### Relevant edge cases

Use `Not applicable — <reason>` where a scenario genuinely cannot occur.

## Decisions
### <Decision name>
- **Decision**: <settled choice>
- **Reason**: <why>
- **Important alternatives**: <only durable rejected alternatives, or "None recorded">
- **Consequences**: <constraints this creates for planning>

## Domain language
<Precise terms whose meaning matters, or "No new domain terms".>

## State and external dependencies
<Persisted state, ownership, migrations, integrations, compatibility, and failure policies.>

## Interfaces and seams
<Important product, module, service, platform, or provider boundaries and invariants.>

## Testing decisions
- **Observable behaviors**: <what proof must demonstrate>
- **Primary seams**: <highest stable test boundary for each behavior group>
- **Existing precedent**: <test pattern/path pointer, or "To be discovered during planning">
- **Highest-level proof**: <integration/journey/provider proof>
- **Manual proof**: <steps and why automation is impossible, or "None expected">

## Security and data checkpoints
<Required trust-boundary or destructive/persistent-data confirmations, or "None identified">.

## Out of scope
<Explicit non-goals.>

## Research evidence
- [<artifact or primary source>](<path-or-url>) — <decision-relevant conclusion>

Use `No external research required` when applicable.

## Unresolved checkpoints
- <question, why it matters, and natural next evidence/decision step>

Use `None` only when every planning-blocking decision is settled.

## Planning constraints
<Dependencies, ordering, rollout, compatibility, and independently verifiable slicing constraints.>

## Source coverage
<List the conversation, decision docs, research artifacts, prototypes, and design comparisons used.>
```

## Coverage audit

Before returning, verify:

- every settled material decision from the session appears once;
- contradictions are resolved or listed under Unresolved checkpoints;
- research claims have claim-level citations or artifact pointers;
- design alternatives do not obscure which design was selected;
- testing decisions discussed in the session are present in the document;
- the readiness status agrees with Unresolved checkpoints;
- no secrets, credentials, private data, raw prompts, or transcript dumps are present; and
- a fresh `to-plan` invocation would not need the original conversation to understand scope and
  acceptance proof.

Return the path, planning status, unresolved checkpoint count, and one recommended next command:
`/skill:write-a-prd <path>` when a product-facing PRD is useful, otherwise `/skill:to-plan <path>`.
