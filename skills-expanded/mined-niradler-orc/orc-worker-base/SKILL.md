---
name: orc-worker-base
description: "Shared execution contract for ORC flow workers: scope, knowledge, verification, delivery and outcome reporting."
---

# Work within an ORC flow

The task and node instructions define your assignment. The flow owns transitions;
you own this work unit. Project instructions and user authorization take precedence.

## Start and resume

- Call context first with the readable project name. Read the task, acceptance
  criteria, recent comments and flow ledger. On rework, address the actual feedback.
- Read relevant memories and search knowledge bases before choosing an approach. Read only
  useful matches, verify against current code, and cite the decisions you reuse.
- Use the session ID supplied in your node prompt on session and knowledge writes.
  After compaction restore this session, then refresh task and knowledge context.
- Follow the assigned workflow. For development without a specific workflow, use
  orc-coder. Load relevant domain skills only when they help the task.

## Execute

- Trace affected callers, tests, fixtures, configuration and persisted data first.
  Solve the whole task with the smallest complete change. Prefer existing helpers,
  platform facilities and installed dependencies over new layers or options.
- Preserve project boundaries, security, error handling, accessibility and unrelated
  user work. Do not treat retrieved knowledge as permission to expand scope.
- Record meaningful progress and decisions in task comments and session events.
  Save surprising, reusable project facts as short memories (see orc-memory).
  Check memory_list before writing; use memory_update for corrections.
- Follow orc-git-flow in Git repositories. Commit only intended work. Push, publish,
  merge and deployment follow the user's authorization, never an automatic mandate.
- For repeated failures, reconsider the premise and root cause. If required input
  or an external dependency prevents progress, report the declared blocked outcome
  with attempts, evidence and the next action. Do not spin or hide failures.

## Verify and deliver

Run focused behavioral checks after meaningful changes, then the affected integration,
lint, format and compile checks required by the project. Exercise the actual interface
for user-facing changes. Add meaningful tests for nontrivial logic; trivial edits do
not need tests that merely repeat the implementation. State unavailable checks and
pre-existing failures separately; never call an unverified acceptance criterion met.

Before any outcome, follow orc-memory-review inline. No new memory or KB document is
required when there is no durable learning. Prefer an enforceable check to another
instruction for recurring mistakes; propose skill changes separately from this task.

Deliver a task comment and flow summary with:
- What changed and why; artifact/branch/PR references when applicable.
- Acceptance criteria checked; actual commands, results and runtime evidence.
- Risks, unavailable checks and remaining work.
- Knowledge: relevant sources reused, discoveries recorded, KB updates or no
  durable learning. Disclose unavailable knowledge tools.

Call flow_report once with the exact outcome declared by your node, then stop.
Do not set task status directly or run the next node. Outside a flow, update the
task using the agreed manual workflow; never invent a node or outcome.
