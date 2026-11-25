---
name: adr-init
description: "Finds the architectural decisions a codebase already embodies and, once you approve the list, writes them to docs/adr/ with an index. Use when adopting ADRs or backfilling partial ADR coverage. Not for one new decision (write that ADR by hand); not for CLAUDE.md (use /init)."
argument-hint: "[optional focus area, e.g. 'auth' or 'storage']"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash(pwd), Bash(git rev-parse *), Agent, Edit(docs/adr/**), AskUserQuestion
license: MIT
---

# Onboard a Repo to Architecture Decision Records

An ADR records one decision that had alternatives: what was chosen, what forced the choice,
and what it costs. This skill finds the decisions a codebase has already made implicitly and
writes them down.

It is **interactive and read-first**. Nothing is written to disk until the Step 3 list is approved.

## Step 1 — Assess current coverage

Focus area from the invocation: `$ARGUMENTS` (empty → whole repository).

Run `pwd` and `git rev-parse --is-inside-work-tree`, then Glob `docs/adr/*.md` and the top-level
directories. Record:

- whether `docs/adr/` and `docs/adr/README.md` exist;
- the **highest** existing ADR number (the largest `NNN` prefix, not the file count: numbers can
  have gaps, and a reused number corrupts the history). New ADRs start at highest + 1, or `001`.

**Without a checkout (web/Cowork):** ask the user to paste the top-level layout, the list of
`docs/adr/` files and the index, and wait. Do not classify coverage or allocate numbers from a
guess: a proposal that duplicates or renumbers existing ADRs is worse than none. On the web,
Step 4 and Step 5 produce file contents for the user to save.

Classify the repo and say which case applies before doing anything else:

- **No `docs/adr/`** → uncovered. Full onboarding.
- **ADR files but no index** → add the index first, then backfill gaps.
- **Some ADRs** → partial. Read every existing ADR and the index before proposing anything, so
  proposals do not overlap or contradict what is recorded.

If the repo is not a git repo, say so and continue: ADRs are just files.

## Step 2 — Extract decisions with Explore agents

Launch read-only `Explore` agents with the `Agent` tool, up to three in parallel, each with a
distinct focus. If a focus area was given, narrow all three to it. Without the Agent tool (web),
do the three passes yourself over what the user pasted.

1. **Structure and boundaries** — module or package layout, service boundaries, the public
   API surface, how the code is decomposed and what that implies.
2. **Dependencies and data** — frameworks and notable version pins, storage engine, schema
   and data-model shape, serialization and transport formats.
3. **Runtime, auth and operations** — how and where it deploys, infrastructure-as-code
   choices, authentication and authorization approach, secrets handling, CI shape.

Ask each agent for **discrete decisions**. A decision is a choice that had a real
alternative and a tradeoff — "we use PostgreSQL rather than a document store" is a decision;
"the code has functions" is not. Each finding must carry:

- a one-line decision statement,
- the evidence (specific files or paths),
- the apparent rationale.

Tell the agents explicitly: document what **is**, do not propose changes.

## Step 3 — Propose, then wait

Consolidate the findings into a numbered candidate list. Present each as
`ADR-NNN: <title> — <one-line summary>` and use `AskUserQuestion` (multi-select) so the user
picks which to record and can edit the framing.

Do not write any file until the set is approved. If the user wants a different cut, merge or
split candidates and present again.

## Step 4 — Write the approved ADRs

Number with three digits, sequentially from the highest existing number + 1 (Step 1). Never
reuse or renumber. One file per decision at `docs/adr/NNN-kebab-title.md`:

```markdown
# ADR-NNN: <short decision title>

**Status:** Accepted

## Context

<the forces at play, reconstructed from the code and the user's input>

## Decision

<the decision as it stands in the code today>

## Consequences

**Good:** <what this buys>

**Tradeoff:** <what it costs, and what becomes awkward>
```

These document existing state, so `Status` is `Accepted` unless the user flags one as still
in progress (`Proposed`) or already replaced (`Superseded by ADR-NNN`).

Where a rationale is inferred rather than evidenced, say so in Context in plain words and
confirm it with the user. Never assert a reason the code cannot support — a confidently
wrong ADR is worse than a missing one.

## Step 5 — Write or update the index

`docs/adr/README.md`, one row per ADR, existing and new:

```markdown
# Architecture Decision Records

Each file records one decision: what was chosen, why, and what it costs.
Change a recorded decision and amend its ADR in the same change.

| # | Title | Status |
|---|-------|--------|
| [ADR-001](001-example-title.md) | Example title | Accepted |
```

The Status column must be honest about the present, not aspirational.

## Step 6 — Propose the CLAUDE.md line

So the repo keeps its ADRs current, propose adding this section to the root `CLAUDE.md` (the section
`project-new` leaves out until ADRs exist), and apply it only on approval:

```markdown
## Architecture and decisions

Architectural decisions live in `docs/adr/` (index: `docs/adr/README.md`). Changing a decision an
ADR records means amending or superseding that ADR in the same change.
```

If specific source paths map to specific ADRs, offer to add that mapping: it is what makes the
ADRs get read. If the section already exists, show the diff and ask before editing.

## Step 7 — Verify

Glob `docs/adr/[0-9][0-9][0-9]-*.md` and read `docs/adr/README.md`. Every ADR file has exactly one
index row, no number appears twice, and every row links to a file that exists. Fix any mismatch
before reporting.

## Step 8 — Summarize

List every file created or changed. Then state the two things that keep coverage alive:

1. Add or amend an ADR in the same change as any architectural decision.
2. Re-run this skill after a large refactor, to catch decisions made since.

## Notes

- Read first, write last. Nothing before Step 3 approval.
- Never fabricate a decision or a rationale. Mark inferences as inferences.
- Continue numbering from existing files; never renumber and never reuse a number.
- A retired decision is superseded, not deleted — the history is the point.
- After onboarding, individual ADRs are written by hand. This skill is for the initial sweep.
