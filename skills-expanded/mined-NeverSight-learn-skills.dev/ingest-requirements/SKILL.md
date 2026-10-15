---
name: ingest-requirements
description: "Read the source requirements documents and produce the register: one numbered, traceable requirement per line, with its provenance, classification and open questions."
disable-model-invocation: true
---

# Ingest Requirements

Turn signed documents into the **register**: `docs/delivery/requirements.md`, the flat, numbered list of everything the contract says must be true.

The register is the chain's **traceability spine**. Every story published later cites the requirement IDs it delivers, which makes two questions answerable at any moment: *is all of the contracted scope in the backlog?* and *is anything in the backlog outside the contract?* Neither question can be answered from a backlog alone, which is why this step exists and why skipping it costs more later than it saves now.

Read `docs/agents/backlog-conventions.md` first for the requirement ID convention. If it is not there, tell the user to run `/setup-delivery`.

## Process

### 1. Read every source document, completely

The user passes paths or URLs: a BRD, an SOW, an RFP response, a build spec, a signed change request, a slide deck that got agreed in a meeting. Read all of them, end to end, before writing a line.

Reach for the format skills where the source needs one: `docx` for `.docx`, `pptx` for `.pptx`. A PDF reads directly.

**Contract documents outrank technical ones.** Where an SOW and a build spec disagree, the SOW is what was signed and the build spec is what somebody intended. Record both and flag the conflict; do not silently prefer the one that is easier to build.

### 2. Extract atomically

One requirement per row. A row that contains "and" is usually two rows.

Keep the source's own IDs where it has them (`BE-12`, `FR-3.1`): they are what the client will quote back at you in a scope dispute, and a register that renumbers them is worthless in exactly the moment it is needed. Mint IDs only for requirements the source states in prose without numbering, and mark those as minted.

Every row carries its **provenance**: the document and section it came from. A requirement whose provenance you cannot name is a requirement you inferred, and it goes in the Inferred table, not the register.

### 3. Classify

Each requirement gets:

- **Type**: `functional`, `non-functional`, `constraint`, `integration`, or `compliance`. Non-functional and compliance requirements are the ones that get dropped, because they belong to no screen and no user journey. Naming the type is what stops that.
- **Priority**: MoSCoW, from the source where it says so and from the user where it does not.
- **Phase**: which contracted phase owns it.

### 4. Hunt the gaps

This is the step that earns the skill, and the one an agent will rush past. The completion criterion is not "the documents are transcribed"; it is **every requirement accounted for, and every silence named**.

Read for what the documents do not say:

- **Unhappy paths.** The document specifies the sign-in; find where it specifies sign-out, password recovery, session expiry, lockout, and deactivation. It usually does not.
- **The other end of every flow.** Where a document specifies a request, find where it specifies the response reaching the person who made it, and the screen that shows it.
- **Stopping.** Cancellation, refund, reversal, shift handover, offboarding. Documents describe systems being used, rarely systems being left.
- **Failure.** Connectivity loss, retry, double submission, partial success, reconciliation.
- **Non-functional silence.** Volume, latency, retention, residency, availability, audit.

Each gap is a **question**, not a requirement. Requirements come from documents; a gap becomes a requirement only when a human answers it. Write it in Open questions with the concrete consequence of leaving it unanswered.

Then look the other way, for **contradictions**: two sections that cannot both be true, a term used with two meanings, a figure quoted twice differently. These cost more than gaps because they read as agreement.

### 5. Write the register

Write `docs/delivery/requirements.md` using the template below.

### 6. Walk the user through it

Present, in this order: the count by type and phase, the contradictions, then the open questions ranked by what they block. Ask them to confirm the MoSCoW and phase columns, which are the two you guessed at most.

That is the whole report. The register itself stays on disk: a three-hundred-row table pasted into the terminal buries the handful of lines the user has to answer.

Do not proceed to the backlog until the contradictions are resolved. An unresolved contradiction becomes two stories that undo each other.

<register-template>

# Requirement register

Sources, with the version or date of each, and which is contractually binding.

## Requirements

| ID | Requirement | Type | Priority | Phase | Source |
|---|---|---|---|---|---|
| BE-12 | The audit log is tamper-evident. | non-functional | Must | 1 | BRD §7.4 |

One line each, stated as a condition that is either true or false of the delivered system. "Support wallets" is not a requirement; "a company can hold a pre-funded wallet balance that debits on each authorised transaction" is.

## Open questions

| # | Question | Blocks | Asked of | Answer |
|---|---|---|---|---|

What the documents do not settle, what it holds up, and who owes the answer. This table is worked down over the engagement; it is not a snapshot.

## Contradictions

Where two sources disagree, both readings, and which document governs.

## Inferred

Requirements no document states, that the system plainly needs. Kept apart from the register because they are **not contracted**, and shipping them without agreement is unbilled scope. Each one is a question for the client before it becomes a requirement.

## Out of scope

What the documents explicitly exclude. As load-bearing as the register itself: this is what you point at when it is asked for in month four.

</register-template>

## Done when

- Every requirement in every source document appears exactly once, with its provenance.
- Source-assigned IDs are preserved unrenumbered; minted IDs are marked as minted.
- Every requirement has a type, a priority and a phase.
- Each of the five gap classes in step 4 was searched for by name, and the search is visible in Open questions or was reported as clean.
- Contradictions are named with both readings.
- Inferred requirements are outside the register, not inside it.

## Hand off

`docs/delivery/requirements.md` is written. Tell the user: **`/shape-backlog`** next, and to run it in this same session while the documents are still in context, since the two steps read the same material at different altitudes.
