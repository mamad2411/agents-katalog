---
name: nested-agent-control
description: Control nested single-job subagents without overrunning thread capacity. Use when the user asks for nested agents, subagents, bug-factory style one-agent-one-job delegation, review coordinators, multi-agent build/review/proof loops, or when prior agent loops hit thread limits and need disciplined orchestration.
---

# Nested Agent Control

Use this skill to make subagents add correctness without stalling the lane. The lead agent remains the orchestrator, integrator, final reviewer, and owner of the next action.

## First Move

State the control header before spawning:

`NESTED AGENT CONTROL: budget=<medium|high|xhigh> | mode=<solo|single-coordinator|sequential-review|parallel-workers> | active_limit=<n> | stop_gate=<condition>`

Then write a short agent ledger:

```text
Agent ledger:
- Local lead: <blocking task owned locally>
- Active coordinators: 0/1
- Active workers/reviewers: 0/<limit>
- Must close before next wave: <agent ids or none>
```

Never delegate the immediate blocking task if local execution is faster and safer. Use subagents for bounded sidecar work, independent file edits, fresh review lenses, or proof checks.

## Capacity Rules

- Run at most one nested coordinator at a time.
- Do not run two coordinators that both need to spawn children.
- Close completed agents immediately before starting the next wave.
- If a coordinator reports `agent thread limit reached`, close completed agents and retry with sequential single-lens reviewers.
- Prefer three parallel leaf reviewers only when no other agents are open.
- Prefer sequential reviewers when the thread is already busy.
- Do not keep completed agents open for “maybe later” context.

## One-Agent-One-Job

Assign one job per agent:

- `confirm`: reproduce or validate the issue.
- `plan`: design the fix.
- `build-test`: edit exactly one test file.
- `build-prod`: edit exactly one production file.
- `test`: run focused verification only.
- `blast-radius`: find missed callers/siblings.
- `patch-or-fix`: classify root-cause fix vs patch.
- `zoom-out`: check architecture and ownership fit.
- `verify`: gather live/browser/canary proof.

Never ask one agent to both build and review, or to edit more than its assigned file set.

## Dispatch Patterns

Use `parallel-workers` only for disjoint write sets:

```text
Worker A: edit exactly <test file>. Do not touch production.
Worker B: edit exactly <production file>. Do not touch tests.
Worker C: edit exactly <proof doc>. Do not touch runtime.
```

Use `single-coordinator` for complex review, but require it to spawn nested leaf reviewers:

```text
You are a review coordinator. Coordinate only. Spawn three nested single-job reviewers:
1. blast-radius
2. patch-or-fix
3. zoom-out
Return READY only if all three finish with no HIGH findings.
Return BLOCKING if any reviewer fails to spawn, reports HIGH, or lacks evidence.
Do not edit files, commit, or create PRs.
```

Use `sequential-review` when thread capacity is tight:

```text
Run exactly one reviewer now: <blast-radius|patch-or-fix|zoom-out>.
Close it after completion.
Then run the next lens with a fresh agent.
```

## Prompt Template

Use this as the default coordinator prompt:

```text
You are a nested coordinator for <issue/task>. One agent, one job: coordinate <review/build/proof> only.
Work in <absolute worktree>. Do not edit files unless explicitly assigned.

You must spawn nested single-job subagents. No nested agent may do more than one job.

Context:
- Branch/head: <branch> at <sha>
- Goal: <goal>
- Known changes: <short file list and behavior>
- Required evidence: <tests/canary/browser/proof gate>

Nested jobs:
1. <lens/job A>: <exact question/output>
2. <lens/job B>: <exact question/output>
3. <lens/job C>: <exact question/output>

Coordinator rules:
- Wait for all required jobs.
- Return READY only if every required job completed and no HIGH findings remain.
- Return BLOCKING on spawn failure, missing evidence, thread-limit failure, or any HIGH.
- Include exact SHA reviewed, receipts, and required follow-up.
- Do not commit, push, create PRs, or mutate unrelated files.
```

## Stop Gates

Stop and report instead of continuing when:

- A nested agent cannot spawn and the task requires nested receipts.
- A reviewer returns HIGH.
- A worker touches files outside its assigned scope.
- A proof/canary/browser check is missing after a code change.
- A coordinator cannot prove exact SHA/worktree reviewed.
- The lead cannot distinguish source proof from runtime proof.

## When Subagents Add Value

Use nested agents for:

- High-risk correctness: data integrity, payments, inventory, auth, tenant boundaries.
- Fresh review after a fix bounced once.
- Multiple independent file-scoped edits.
- Proof-heavy lanes where source tests and runtime proof are separate.

Keep work local for:

- Tiny mechanical edits.
- One-file fixes where review can happen after the patch.
- Urgent blocking work.
- Any task where spawning agents would consume more time than the verification itself.

## Final Handoff

Before calling work ready, summarize:

```text
Agent receipts:
- <agent id/name>: <job> -> <READY|BLOCKING|changed files|tests>

Local proof:
- <commands and results>

Open blockers:
- <none or exact blockers>
```
