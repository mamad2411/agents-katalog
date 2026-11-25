---
name: architect-propose
description: Propose and create a new Architect track for an initialized project, including its spec, plan, metadata, and registry entry. Use when the user asks to add, plan, or propose a new feature, bug fix, chore, refactor, docs, or test track.
---

# Architect Propose

Create one proposal track from approved specification and plan artifacts. Follow `references/propose-track-protocol.md` as the source of truth.

## Hard Boundaries

- Require initialized core Architect context.
- Do not create a track before both spec and plan approvals.
- Keep writes and links under safe `architect/` paths.
- Do not let unrelated track status block an independent proposal; only collisions may block creation.
- Commit only when explicitly requested in the current conversation.

## Run

1. Read `references/propose-track-protocol.md` and core project context.
2. Establish description and inferred track type.
3. Draft, present, revise, and approve `spec.md`.
4. Ask for Task or Sub-task status granularity, default to Sub-task, then draft, present, revise, and approve `plan.md` from the project workflow.
5. Recover management paths when needed, generate a safe ID, and run collision checks.
6. Create artifacts, register the track, and report next steps without starting implementation.
