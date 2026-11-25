---
name: first-tree-write
version: 0.16.2-local.1
cliCompat:
  first-tree: ">=0.5.16 <0.6.0"
description: Source-driven Context Tree write workflow for managed and BYO consumers. BYO always requires the exact SCOPE-routed read snapshot and a new user confirmation of the precise Team/source/targets/mutation plan before any Tree mutation. If no source artifact is available, there is no write task.
---

# First Tree Write — Local Context

## Purpose and authority

Reflect a concrete source artifact into the current Agent's private Local
Context. This payload is the managed Local variant of `first-tree-write`; its
public name and routing description intentionally match the Remote payload.

Local Context is not Team-approved truth and has no Git, forge, PR/MR,
Reviewer, Audit, Seed, Cloud Tree IO, or Web workflow. Any current Chat, human
decision, design document, PR/MR, Issue, meeting note, or other inspectable
material can be a source. Never manufacture organization facts from model
memory. The generated Context Tree Policy remains the content-model baseline.

## Source gate and Double Test

Write only when the source establishes or changes a durable decision,
constraint, ownership fact, or cross-domain relationship. It must both matter
to future choices and remain true if the triggering implementation is
rewritten. Implementation detail, refactors, request shapes, fixtures, build
configuration, and one-off fixes stay in their source system.

If nothing passes, write nothing and explain why.

## Workflow

1. Identify the exact source, smallest existing target, parent, relevant
   normal `soft_links`, and ownership-adjacent member content. New top-level
   domains, `owners` changes, and `decisionLocksCode` changes still require
   explicit human-owner authority.

2. Run:

   ```text
   <firstTreeInvocation> --json tree local resolve --ensure --intent write
   ```

   Use only the returned `data.path`. The guard accepts no caller path and
   rechecks runtime identity, fixed containment, limits, latch, and Server
   binding. `repairOnly: true` means the live Tree is invalid: repair existing
   mechanically provable content before any expansion. If correct business
   content cannot be determined from the files and source, stop and ask a
   human; do not delete or invent facts just to pass validation.

3. Read the source and surrounding live Tree. Then edit the live root directly
   with native file tools. Do not create a lock, snapshot, candidate,
   fingerprint, worktree, journal, rollback state, approval diff, commit, or
   PR/MR. Local V0 accepts last-write-wins and moving reads.

4. Immediately re-read every changed node and perform the semantic checklist:

   - source-system boundary and Double Test;
   - current-state What and surviving Why;
   - Who only in `owners` frontmatter or member content;
   - correct normal/archive/member content class;
   - smallest edit and one canonical home, with no duplicate truth;
   - no implementation walkthrough, delivery history, PR reference, or future
     work in normal content;
   - no unauthorized owner, top-level domain, or `decisionLocksCode` change.

5. Run the full mechanical gate:

   ```text
   <firstTreeInvocation> tree verify --tree-path "<live-root>"
   ```

   A non-zero result means the write is unfinished. Continue repairing and
   verifying, or report failure without citing the change or claiming success.

6. Re-run the guard after the successful verification:

   ```text
   <firstTreeInvocation> --json tree local resolve --ensure --intent write
   ```

   It must still return the same live root with `verified: true` and without
   `repairOnly`. Bound, frozen, invalid, unknown, corrupt, mismatched, or
   unreadable state stops completion. A newly observed remote binding freezes
   the Local files in place; never upload, merge, or continue using them.

## Failure and concurrency boundary

Concurrent Chats may overwrite one another or leave a temporary invalid Tree;
a crashed writer may leave partial edits. There is no automatic rollback.
Every writer is responsible for the full live Tree it sees at completion, and
every later reader verifies again before use. Do not claim transaction safety,
stable snapshots, conflict detection, or durable Local history.
