---
name: team-backlog
description: Break the PRD into tracer-bullet tickets, vertical slices with acceptance criteria and blocking edges, ordered into .team/03-backlog.md. The playbook of the po role.
---

# Backlog: Tracer-Bullet Tickets

Break the PRD into **tickets**: tracer-bullet vertical slices, each declaring the tickets that block it.

The output is one file: `.team/03-backlog.md`. The backlog is the contract the build and QA stages work from, so it has to be complete enough to start a ticket without reading the whole PRD again.

## Process

### 1. Gather context

Read `.team/02-prd.md` and `.team/01-research.md` if it exists. Work from whatever is already in the conversation too. If the user passes a reference (a spec path or a URL), fetch it and read it in full.

### 2. Explore the codebase (optional)

If this is an existing product, understand the current state of the code before slicing. Ticket titles and descriptions should use the project's domain vocabulary.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change." Prefactoring is its own ticket, first in the order.

### 3. Draft vertical slices

Break the work into **tracer-bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (data, API, UI, tests): vertical, NOT a horizontal slice of one layer.
- A completed slice is demoable or verifiable on its own.
- Each slice is sized to fit in a single fresh context window.
- Any prefactoring is done first.
- A slice delivers end-to-end behavior from the user's perspective, not a layer-by-layer implementation list.

</vertical-slice-rules>

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Do not force it into a tracer bullet; sequence it as **expand–contract**:

1. **Expand**: add the new form beside the old so nothing breaks.
2. **Migrate**: move the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand. The old form still exists, so each batch stays green.
3. **Contract**: delete the old form once no caller remains, in a ticket blocked by every migrate batch.

When even the batches cannot stay green alone, keep the sequence but let them share an integration branch and add a final integrate-and-verify ticket that all of them block. Green is promised only there.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **What it delivers**: the end-to-end behavior this ticket makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?

Iterate until the user approves the breakdown. Do not write the file before approval.

### 5. Write `.team/03-backlog.md`

Write all approved tickets into one file, numbered from `01` in dependency order (blockers first). Each ticket has its acceptance criteria and a `Blocked by:` line using the ticket IDs.

Work the **frontier**: any ticket whose blockers are all done. For a purely sequential chain that means top to bottom.

## Ticket template

Use this shape for every ticket in `.team/03-backlog.md`:

```markdown
# .team/03-backlog.md

Source: `.team/02-prd.md` (and `.team/01-research.md` if present)

## #01 — <Ticket title>

**What to build:** the end-to-end behavior this ticket makes work, from the user's perspective, not a layer-by-layer implementation list.

Blocked by: None (can start immediately)

**Acceptance criteria:**

- [ ] Criterion 1 — observable and testable
- [ ] Criterion 2

## #02 — <Ticket title>

**What to build:** ...

Blocked by: #01

**Acceptance criteria:**

- [ ] Criterion 1
- [ ] Criterion 2
```

For a later ticket with several blockers, write them on one line: `Blocked by: #01, #03`. If a ticket is part of a wide refactor, say so in "What to build" and name the expand, migrate or contract step.

## Acceptance criteria

An acceptance criterion is a behavior, not a task:

- Good: "An invoice with no line items cannot be sent; the form shows an error."
- Bad: "Add validation to the invoice form."

Every criterion must be verifiable by a test, a demo or a measurement. If it cannot be verified, rewrite it or move it to out-of-scope.

## Rules

- Do not use specific file paths or code snippets: they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (a state machine, a reducer, a schema, a type shape), inline it and note that it came from a prototype. Trim to the decision-rich parts, not a working demo.
- One ticket, one slice. If a ticket needs "and then" twice, split it.
- A ticket that cannot be demoed or verified on its own is not a vertical slice; merge it into the slice it serves.
- Order by dependency, not by layer or by who is available.
- Keep the wording in the user's language (Turkish or English), code identifiers in English.

> Adapted from the MIT-licensed upstream ticket-writing skill by Matt Pocock. See THIRD_PARTY_NOTICES.md.
