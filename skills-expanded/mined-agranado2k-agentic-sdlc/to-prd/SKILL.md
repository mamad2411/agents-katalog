---
name: to-prd
description: Turn the current conversation context into a PRD and publish it to the project issue tracker. Use when user wants to create a PRD from the current context.
allowed-tools: Read, Grep, Glob, Bash, Write, Skill
metadata:
  phase: planner
---

This skill takes the current conversation context and codebase understanding and produces a PRD. Do NOT interview the user — just synthesize what you already know. The one exception is the one question below, asked before anything else when the conversation was never grilled. (If the requirements are not settled yet, that is `/grill-me` or `/grill-with-docs`, not this.)

## A factory project defers, before any other step

First of all — before the grilling question below, and before you explore the repo — open [FACTORY.md](FACTORY.md) and run its check, `factory_deferral factory-prd`. `defer` ends the run at its hand-off; `missing` is said once; `none` changes nothing.

## Before you start

- **An ungrilled conversation.** Before any step of the process, read this conversation for a grilling session — a `/grill-me` or `/grill-with-docs` run that settled the plan one question at a time. Only such a run counts as grilled; an interview of the same shape held by hand does not, and asking costs one line. When it holds no grilling session, open by asking the user one question, and only one: run `/grill-me` first? Where the project has a glossary (`docs/domain-glossary.md`) and decision records (`docs/adr/`), name `/grill-with-docs` instead — it challenges the plan against both. **Yes** runs that skill; when it ends, hand back to this skill and synthesize from step 1. A run with nobody to answer — spawned by another session, or unattended — takes the No path without asking. **No** writes the PRD as this skill always has, and lists under Open Issues each point you would otherwise have guessed, in that section's three-line shape, so a later session sees the guess instead of inheriting it as a decision. The check reads the conversation only, never the trace: the trace records grill decisions, but no skill reads it to decide anything (the kit's ADR-0008). Beyond this one question the skill still never interviews (the kit's ADR-0012).
- **The tracker.** Publish to whatever issue tracker the project uses; the root `AGENTS.md` or `constitution/local-workflow.md` names it. If neither does, ask once and then record the answer there rather than in this file.
- **The autonomy label.** Shared invariant §6: every ticket carries an explicit autonomy label, and ambiguity resolves to human-in-the-loop. This kit's mechanism is a single `ready-for-agent` label — its presence means an agent may take the work solo, its absence means a human stays in the loop. There is no literal `HITL` label; absence *is* the signal.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use `docs/domain-glossary.md` vocabulary throughout the PRD, and respect the decision records in `docs/adr/` that cover the area you're touching.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can.

Check with the user that these seams match their expectations.

3. Write the PRD using the template below, then **reread it as a stranger.** The PRD is read by sessions that hold none of this conversation (shared invariant §4). Whatever you would tell a teammate before they read it belongs in the Objective and the Problem Statement, not in your head; if a section only makes sense with the chat open, it is not finished.

4. Publish it to the project issue tracker with the `ready-for-agent` label if the work is mechanical with a checkable definition of done — no additional triage needed. Then record the publish, once the tracker has given it a number: `sh scripts/trace.sh emit kind=prd.write subject=prd:#<issue> outcome=published data.label='<ready-for-agent, or none>' reason='<the Objective, one line>' || :`. The trace is written here and never read (the kit's ADR-0008); unconfigured, the call is a silent no-op.

<prd-template>

## Objective

The objective is one sentence, in plain language and the glossary's vocabulary, that any stakeholder understands: what this changes and for whom. It is the line every ticket opens with for context and the name the change goes by, so it is the first line of the PRD, before the problem is explained.

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A numbered list of user stories, one story per distinct actor goal. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

A story is kept as the *why* — who wants this and what it buys them — not as the list of everything the feature does: that list is the Requirements section's job. Two stories with the same actor and the same goal are one story; every requirement serves at least one story, and a requirement that serves none is either a missing story or a requirement nobody asked for.

## Scenarios

Each scenario is a **use case**: `UC<n> — <name>`, numbered from 1 within the PRD, then `Actor:` — who drives it — and `Goal:` — what they have when it ends; a numbered **main flow**, the walkthrough of the finished system in use — actor, action, what they see — step by step, with concrete names rather than placeholders; and `Extensions:`, each one numbered from the step it branches from — `2a` is the first branch off step 2, `2b` the second — holding the refusal, the missing input, the second path a main flow walks past. One per major story, and always where the story is abstract.

<scenario-example>
**UC1 — Check a balance after a transfer.** Actor: Ana, who holds a current and a savings account. Goal: know what she can spend today.
1. Ana opens the account screen and sees the balance of both her accounts.
2. Ana's transfer of 200 to Bo settles, and the screen shows her new balance.

Extensions:
- 2a. The balance service does not answer: the screen shows the last balance it read, and when.
</scenario-example>

Each main flow is a walkthrough a session can replay: `/to-tickets` reads each use case's main flow as a candidate tracer bullet, and an extension's requirements go to the slice that builds its step — so a use case that cannot be walked through is a story the PRD has not finished thinking about. A PRD written before use cases keeps its walkthrough scenarios as written; nothing rewrites or refuses them.

## Requirements

The exhaustive list of what the finished feature does: one observable behavior per line — a behavior a test can fail — each carrying an id `R<n>`, numbered from 1 within the PRD. Tickets, tests and the review cite a requirement by its id, so an id once published is not renumbered. Write each line in EARS-lite, one of five forms:

- `The <system> SHALL <behavior>` — always true.
- `WHEN <trigger>, the <system> SHALL <behavior>` — an event.
- `WHILE <state>, the <system> SHALL <behavior>` — a state that holds.
- `IF <condition>, THEN the <system> SHALL <behavior>` — an unwanted case and its handling.
- `WHERE <feature>, the <system> SHALL <behavior>` — an optional feature present.

<requirement-example>
R1. The account screen SHALL show the balance of every account the customer holds. [UC1 1]
R2. WHEN a transfer settles, the account screen SHALL show the new balance within 5 seconds. [UC1 2]
R3. IF the balance service does not answer, THEN the account screen SHALL show the last known balance with the time it was read. [UC1 2a]
R4. The account screen SHALL show a balance to two decimal places.
</requirement-example>

A line that bundles two behaviors is two requirements; a line no test could fail — "the screen SHALL be intuitive" — is a quality word, and the Testing Decisions rule applies to it: a number, or dropped.

**A requirement a step checks ends with those steps in brackets**, the use case and its step: `[UC1 2a]`, or `[UC1 1, 2]` for more than one — so each requirement traces to the flow that needs it, and an unwanted case no extension holds is a branch the scenarios missed. A requirement no step reaches — a format, a limit, a schema rule — carries no brackets, and that is allowed. The brackets are never part of the id: the coverage check reads the id alone.

**Where a living spec exists for the area** — `docs/specs/<area>.md`, the area's current requirements — **write the requirements as deltas against it** (the kit's ADR-0012 clause 8), each line spelled with its area-qualified id, `<area>/R<n>.`, so that the PRD, a ticket's `Covers:` line and the test that holds the requirement all cite the same string:

- `### ADDED` — a new requirement, under the next free id: one past the highest number the living spec has used, its requirement lines and its tombstones both, because an id is never reused.
- `### MODIFIED` — an existing requirement, its whole new text restated under the id it already has, never a list of the words that changed.
- `### REMOVED` — the id, and why it goes.

Only the headings the PRD needs appear: everything the living spec holds outside a delta is unchanged by construction. A REMOVED line is still a requirement line — a ticket covers it, and delivering it replaces the line in the living spec with its tombstone, `~~R<n>.~~ Removed by #<PRD>: <why>`, which no test needs to name (`/implement` step 4). **Where no living spec exists for the area**, write plain `R<n>.` lines numbered from 1, and name the area once, on a line `Area: <area>` above them — one lowercase token, `[a-z][a-z0-9-]*`; the first ticket that covers one creates `docs/specs/<area>.md`, keeping the PRD's numbers. A PRD that names no area keeps no living spec: its ids live and die with it.

<requirement-delta-example>
### ADDED
billing/R7. WHEN an invoice is reissued, the account screen SHALL show the original's number beside the new one.

### MODIFIED
billing/R2. WHEN a transfer settles, the account screen SHALL show the new balance within 2 seconds.

### REMOVED
billing/R4. Removed: the paper statement it described is no longer sent.
</requirement-delta-example>

## Implementation Decisions

Record a decision here when the **penalty for being wrong** is high — an interface, a storage shape, a seam, a module boundary: anything expensive to reverse once sessions have built on it. A decision that is cheap to change later belongs to the implementing session, not the PRD; pinning it here writes the implementation during design. The file-path rule below is one consequence of this.

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)
- Every quality word in this PRD — fast, small, robust, responsive — restated as a number a test can assert, or dropped

## Alternatives Considered

A few brief lines per strong alternative the conversation rejected, and why it lost. Only the ones a later session would plausibly propose again — not every idea. A decision that outlives this feature is already recorded in `docs/adr/` (by `/grill-with-docs` or `/design-brief`, after a human yes) and is linked from here, not repeated; one that is not yet recorded is an Open Issue, not an alternative.

## Out of Scope

One line per item, each with its reason, and each marked *later* (deferred — say what would reopen it) or *never* (rejected). A bare list makes a fresh session guess which is which.

## Open Issues

Anything the conversation left unresolved, each as three lines: the problem, the options seen, and the immediate next step — a `/prototype` spike, a `planner` ticket, or a question to a named person (which, if the answer shapes tickets, `/to-tickets` writes as a ticket with no label, so a human answers it). When one is resolved, move it out of here and into Implementation Decisions (or a decision record); the tracker keeps the history. An open issue whose answer would shape tickets becomes the first ticket `/to-tickets` writes, and blocks the ones it shapes — see its open-issue gate.

## Further Notes

Any further notes about the feature.

</prd-template>

Alternatives Considered and Open Issues are **omitted when empty** — never written as "none" or "N/A". A section is a menu item, not a form field.

## What happens next

A PRD that spans more than one context window goes through `/to-tickets` before any code is written (shared invariant §1). One that fits a single window can go straight to `/implement`.

---

*Adapted from `engineering/to-prd` in [mattpocock/skills](https://github.com/mattpocock/skills) — MIT, see `.agents/skills/LICENSE-mattpocock-skills.md`. Upstream expects a separate setup skill to have supplied the tracker and label vocabulary; here that vocabulary is the kit's own autonomy-label mechanism. The Objective, Scenarios, Alternatives Considered and Open Issues sections and the penalty-for-being-wrong filter follow Michael Lynch's [How to Write an Effective Software Design Document](https://refactoringenglish.com/excerpts/write-an-effective-design-doc); the stranger reread and the later/never split are the kit's own extension of it. The Scenarios' use-case shape — an actor, a goal, a main flow and extensions numbered from their step — follows Alistair Cockburn's *Writing Effective Use Cases*.*
