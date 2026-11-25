---
name: create-adr
description: Create an Architectural Decision Record (ADR) for this project. Use when the user asks to document a decision, create an ADR, record an architectural decision, or write a decision record. Triggers on phrases like "ADR", "architectural decision", "decision record", "document this decision", or "record why we chose X over Y".
allowed-tools: Read, Write, Glob, Grep, Bash
model: sonnet
version: 1.0
---

# Create Architectural Decision Record

Produce an ADR document that captures the *why* of an architectural decision in a form that is both machine-parseable and human-readable.

## When this skill applies

Use this skill whenever the user wants to:
- Create a new ADR for a decision being made now.
- Convert a discussion (from the current conversation or a linked issue/PR) into a formal ADR.
- Document an already-made decision retroactively.

Do **not** use this skill for:
- Generic design docs, RFCs, or proposals (ADRs are narrower: one decision, one document).
- Editing an existing ADR's `Status` field — that is a trivial edit, not a new document.

## Required inputs

An ADR cannot be generated without all of the following:

1. **Decision Title** — short noun phrase (e.g. "State management library selection").
2. **Context** — the problem, constraints, and environment that forced the decision.
3. **Decision** — what was chosen.
4. **Alternatives** — at least one alternative considered, with why it was rejected.
5. **Deciders** — who decided (individual, team, or "BSD-layouter team").

### How to gather them

Follow this procedure *in order*. Do not skip ahead.

1. **Scan the current conversation first.** If the user has already discussed a decision, extract candidate values for each field. Do not fabricate — if something is not stated, treat it as missing.
2. **Present what you extracted** back to the user: "Here is what I inferred: 1. Title: ... 2. Context: ... — is this correct, and what is missing?"
3. **For any field still missing, ask one question at a time.** Do not bundle questions. Do not proceed to drafting until every required input is confirmed.
4. Only once all five are confirmed, generate the file.

If the user insists on generating the ADR with missing fields, do so but leave missing sections as `[TODO: ...]` placeholders and list every placeholder explicitly at the end.

## Where to save the file

All ADRs for this project live in:

```
docs/architecture-decisions/adr-NNN-<title-slug>.md
```

`NNN` is a 3-digit zero-padded sequence number (001, 002, ...).

### Determining the next number

Before writing, find the highest existing number:

```bash
ls docs/architecture-decisions/ | grep -E '^adr-[0-9]+-' | sort | tail -1
```

If the directory is empty, start at `001`. Increment by 1 for each new ADR.

If two collaborators add an ADR in parallel branches, a number collision is possible. Mention this caveat to the user on creation.

### Slugifying the title

1. Lowercase everything.
2. Replace any run of non-alphanumeric characters with a single hyphen.
3. Strip leading and trailing hyphens.
4. Cap at 60 characters (cut at the last hyphen boundary before the limit).

Example: "TanStack Router over React Router" becomes tanstack-router-over-react-router.

## Document format

Do not use YAML front matter in the ADR itself. Use inline bold fields at the top.

Generate the file with exactly this structure:

# ADR-NNN: <Decision Title>

**Status:** Proposed
**Date:** <YYYY-MM>
**Deciders:** <Names or team>
**Related:** <Links to other ADRs, PRs, or issues -- or "None">

## Context

<Problem statement, constraints, and environmental factors that forced this decision.
Write in present tense. Name specific libraries, versions, and constraints where relevant.>

## Decision

<The chosen solution as a declarative sentence, followed by the rationale.
Do not restate the context here.>

## Consequences

### Positive

- <Beneficial outcome>

### Negative

- <Trade-off or limitation introduced>

## Alternatives Considered

### <Alternative Name>

- **Description**: <Brief technical description>
- **Rejection Reason**: <Specific reason -- not "worse overall">

## Implementation Notes

- <Key implementation or migration considerations>

## References

- <Related ADRs as relative markdown links>
- <External docs or standards referenced>

## Writing rules

- **Precise language.** Prefer "X imports Y at build time" over "X uses Y".
- **Status is always Proposed on creation.** Do not set Accepted -- that is a human review outcome.
- **Date format is YYYY-MM.** Not YYYY-MM-DD.
- **At least one alternative is required.** "Status quo" and "do nothing" are legitimate alternatives.
- **Both positive and negative consequences must be filled.** A section with only positives is incomplete.
- **Do not invent references or PR numbers.** Write "None" if not provided.

## After creating the file

1. Show the full path of the created file.
2. List any [TODO: ...] placeholders that remain.
3. Remind the user to flip Status to Accepted once the decision is confirmed.

Do not commit or push unless the user explicitly asks.
