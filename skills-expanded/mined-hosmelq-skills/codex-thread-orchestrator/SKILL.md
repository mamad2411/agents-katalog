---
name: codex-thread-orchestrator
description: >-
  Route work from a user-started parent Codex task to visible child tasks using
  compact durable state, proactive callbacks, independent review, reuse, and
  compaction recovery.
---

# Codex Thread Orchestrator

Activate `$durable-workflow-control` first; it owns generic goals, evidence,
budgets, blockers, verification, and closure. This extension adds visible-task
identity, routing, reuse, compact messages, and recovery.

Read [references/protocol.md](references/protocol.md) before creating a child.
Discover applicable `AGENTS.md`, skills, and operations from the live runtime;
never hardcode projects, frameworks, or unavailable tools.

## Restrict The Parent

The parent only maintains coordination state, operates visible tasks, validates
callbacks, routes transitions and review, and answers from durable state.

It never reads project code, investigates, implements, runs project commands or
tests, edits deliverables, or polls.

## Keep State And Messages Small

Use the protocol layout. The parent owns root files; each child owns its compact
file. Persist stable facts and the review recipe once. Keep decisions and brief
evidence references in state; open detailed task artifacts only when needed.
Keep follow-ups to delivery, callback, supersession, and the change.

## Route Visible Tasks

Create project-local visible tasks only on explicit request and follow the
protocol's project selection and model lanes. Route by responsibility and risk,
not project or framework; split oversized work before raising effort. Every
Locator, Scout, Worker, Smart worker, researcher, implementer, and reviewer is a
parent-created visible task. Never use subagents; children cannot create tasks.

After dispatch, end without waiting. Children attempt one minimal callback and
leave a short final pointing to their state file.

Review implementation with the same implementer/reviewer until approval.
Accept routine research, inventories, trackers, and deterministic evidence
without review unless requested or risky/ambiguous.

## Recover After Compaction

The installed `SessionStart(compact)` hook immediately injects the exact parent
control or visible-child state path before resumed reasoning/tools. Parent
recovery uses the permanent `parent` marker, never `active`.
