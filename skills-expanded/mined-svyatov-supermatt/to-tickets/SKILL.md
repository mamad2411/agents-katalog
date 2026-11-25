---
name: to-tickets
description: Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker (edges as text in one file per ticket locally, or native blocking links on a real tracker).
disable-model-invocation: true
argument-hint: "[spec path, issue identifier, or URL]"
license: MIT
---

# To Tickets

Break a plan, spec, or conversation into a set of **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it.

Read `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`. If either is missing or unreadable, stop and tell the user to run `/setup-supermatt-skills` in Claude linked installs or Cursor, `/supermatt:setup-supermatt-skills` from the Claude plugin, `$setup-supermatt-skills` in Codex, or `/skill:setup-supermatt-skills` in OMP. Resume only after both required docs exist and have been read.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, a tracker identifier or URL) as an argument, fetch it and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, spawn a fresh read-only exploration subagent, so the file contents stay out of this context. Have it return a summary: the current state of the code in the area, the glossary terms and ADRs that apply, and prefactor candidates. If no independent context is available, explore it yourself and report that gap. Ticket titles and descriptions should use the project's domain glossary vocabulary and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first

</vertical-slice-rules>

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. List only direct blockers: drop an edge another blocker already implies, so a final ticket names only the tickets nothing else depends on. A ticket with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand-contract**. It takes three kinds of ticket. The expand ticket adds the new form beside the old so nothing breaks. Each migrate ticket moves one batch of call sites over, sized by blast radius (per package, per directory) and blocked by the expand; CI stays green batch to batch because the old form still exists. The contract ticket deletes the old form once no caller remains, blocked by every migrate batch. Every ticket must pass the repository's full required gate independently; if a batch cannot, reshape or combine it until it can before publishing.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **What it delivers**: the end-to-end behaviour this ticket makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?

Iterate until the user approves the breakdown.

### 5. Publish the tickets to the configured tracker

Publish the approved tickets. **How** depends on the tracker `/setup-supermatt-skills` configured; the tickets are the same either way, only the shape of the blocking edges changes:

- **Local files** → write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first). Each file's `Blocked by:` line lists the numbers it depends on. Use the per-ticket file template below: one ticket per file, never a single combined file. Set `Status:` to the configured value for the canonical `ready-for-agent` role.
- **A real issue tracker (GitHub, Linear, ...)** → publish one issue per ticket in dependency order (blockers first) so each ticket's blocking edges can reference real identifiers. Use the platform's native blocking relationship where it has one (the **Blocking** operation in `docs/agents/issue-tracker.md`); otherwise put the tracker's `Blocked by:` fallback line at the top of each ticket's body. Apply the configured label for the canonical `ready-for-agent` role; the tickets are agent-grabbable by construction. A label override must still map to that canonical role in `triage-labels.md`.

Preserve an exact `## Parent` reference to the source spec in every child, including local files. Use the tracker's canonical issue reference or a usable Markdown path/link to the local spec. When both the source spec and the published ticket are GitHub issues, also attach the ticket to the spec as a native sub-issue using [Attach a spec ticket](../setup-supermatt-skills/issue-tracker-github.md#attach-a-spec-ticket). On Linear create the children in the configured project and default team, set the native parent to the source Linear spec, and verify the parent and native blocking relations before removing the spec's readiness. If a Linear operation fails, report the partial publication with the identifiers already created. Reconcile those tickets before retrying. For a tracker without native parent links, keep the text reference. Parentage adds no blocking edge.

If the source was a spec carrying the canonical `ready-for-agent` role, remove that readiness using the configured label or local `Status:` field: its tickets are now the work, and the spec stays open as their parent. Leave the parent otherwise untouched.

Then stop. Tell the user to run `/implement` in Claude linked installs or Cursor, `/supermatt:implement` from the Claude plugin, `$implement` in Codex, or `/skill:implement` in OMP on a **frontier** ticket (one whose blockers are all satisfied under the configured tracker's rules) in a fresh context, one ticket per session.

<local-ticket-template>

# <NN>: <Ticket title>

Status: <configured ready-for-agent value>
Blocked by: <NN, NN> (omit this line when nothing blocks it)

**What to build:** the end-to-end behaviour this ticket makes work, from the user's perspective, not a layer-by-layer implementation list.

**Seams:** the seams under test for this ticket: every seam from the spec's Testing Decisions that one of its acceptance criteria crosses (omit when there is no spec).

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

## Parent

A Markdown path/link to the source spec (omit when there is no source spec).

</local-ticket-template>

<issue-template>

Blocked by: #<n>, #<n> (only where the tracker has no native blocking; omit it when nothing blocks the ticket)

## Parent

The exact issue reference or Markdown path/link to the source spec (omit when there is no source spec).

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective, not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Seams

The seams under test for this ticket: every seam from the parent spec's Testing Decisions that one of its acceptance criteria crosses (omit this section when there is no spec).

</issue-template>

In either form, avoid specific file paths or code snippets: they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype, citing its `prototype/<name>` branch. Trim to the decision-rich parts, not a working demo, just the important bits.

For a spec with an approved `## Migration map`, every affected ticket must link that authoritative section and identify its assigned move rows and path-contract updates, including exact paths where needed. These references are requirements for a fresh implementation session, and are a conditional exception to the source-path rule above. Preserve the map's contracts rather than replacing them with a summary.
