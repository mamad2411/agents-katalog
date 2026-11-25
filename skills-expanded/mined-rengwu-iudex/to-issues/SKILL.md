---
name: to-issues
description: Break a plan, spec, or PRD into independently-grabbable iudex tickets using tracer-bullet vertical slices, and register them in the iudex queue with their dependencies. Use when the user wants to convert a plan into tickets, create implementation tickets, or break down work into the iudex queue.
---

# To Issues

Break a plan into independently-grabbable iudex tickets using vertical slices (tracer bullets). The iudex queue is the tracker: each slice becomes a `t<id>.md` brief in `.iudex/queue/`, registered with `iudex queue`. Blocking relationships between slices map directly onto iudex dependencies (`--deps`).

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user points at a PRD (e.g. `.context/prd/<slug>.md`), read it in full. Read the domain glossary — every top-level `*.md` in `.context/` — so ticket titles and descriptions use the project's vocabulary, and respect ADRs in `.context/adr/` for the area you're touching.

If the source is a PRD, make sure every requirement has a stable id first: list them
with `grep -nE '^#{1,6} +REQ-' .context/prd/<slug>.md`. If any heading still reads
`REQ-?`, assign ids using the to-prd skill's numbering rule (file-scoped: highest
existing `REQ-<n>` in this file + 1, in order of appearance, never renumbering existing
ids), then re-run the grep to confirm no `REQ-?` remains. Reference those `REQ-N` ids
when you slice, so each ticket traces back to the requirements it satisfies.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code.

### 3. Draft vertical slices

Break the plan into **tracer bullet** tickets. Each ticket is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

Slices may be 'HITL' or 'AFK'. HITL slices require human interaction, such as an architectural decision or a design review. AFK slices can be implemented and merged without human interaction. Prefer AFK over HITL where possible. (iudex itself doesn't track HITL/AFK — every ticket passes through the same human-qa gate — so note it in the brief prose to guide how the human drives `activate`/`human-qa`.)

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
</vertical-slice-rules>

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Type**: HITL / AFK
- **Blocked by**: which other slices (if any) must complete first
- **Requirements covered**: which PRD requirements (`REQ-N` ids) this slice satisfies, if the source is a PRD

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?
- Are the correct slices marked as HITL and AFK?

Iterate until the user approves the breakdown.

### 5. Register the tickets in the iudex queue

Publish the approved slices **in dependency order — blockers first** — so every blocker already has a real ticket id by the time a dependent references it. iudex requires deps to be pre-registered, and `iudex next-ticket-id` returns "highest *registered* id + 1", so you must complete the full register step for one ticket before computing the id for the next.

For each slice, in order:

1. **Get the id:** `id=$(iudex next-ticket-id)`
2. **Author the brief:** write the ticket body to `.iudex/queue/t$id.md` using the template below. The **first line must be an H1 title** — `# <short descriptive title>` (the slice's Title from step 4, no `tN:` prefix — the id is shown separately). The GUI reads a ticket's title from the brief's first `# ` heading, so a brief without one shows no title in the Tickets, Agents, and Review views. Use a single `#` — section headings inside the brief are `##` or deeper.
3. **Register it (with deps):** `iudex queue t$id --deps t<blocker-ids>` (comma-separated blocker ids; omit `--deps` entirely if the slice has none).

**Do not put status or dependencies inside the `t<id>.md` file.** iudex's event log is the single source of truth — dependencies live ONLY in the `iudex queue --deps` command. You may mention blockers in the brief's prose for a human reader, but the canonical dependency edge is the registered queue event. The markdown carries the spec, nothing else.

After registering, run `iudex status` to show the user the queued tickets (each annotated `ready` or `blocked by`).

<ticket-template>
# <short descriptive title>

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

Avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it here and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Notes

- Type: HITL / AFK (and why, if HITL).
- Blockers (for the human reader): tN, tM — registered canonically via `iudex queue --deps`.
- Requirements covered (for the human reader): `REQ-N`, `REQ-M` from the source PRD. This is prose traceability for now; a canonical requirement→ticket link (`iudex queue --satisfies`) is planned but not yet available.
- Reference to the source PRD under `.context/prd/` if applicable.
</ticket-template>
