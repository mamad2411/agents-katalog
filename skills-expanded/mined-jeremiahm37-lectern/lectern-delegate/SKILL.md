---
name: lectern-delegate
description: "Delegated build: you plan a substantial change and review the result; a cheaper worker agent builds it as a Lectern task in its own worktree. Use for multi-file features, migrations and refactors when Delegated builds is ON. Skip trivial edits and single-agent requests."
---

# Delegated build for Lectern

You are the lead. Keep for yourself what your judgment is worth paying for:
scope, design, acceptance criteria, material risk and the final review. Hand
the volume of the implementation, and the discovery, testing and debugging it
needs, to the worker.

The workflow is adapted from ethanplusai/astra-flash-orchestrator, whose
original skill, references and templates are unmodified in `upstream/` (MIT).
What differs is the transport: the worker is not a native subagent but a
**Lectern task**, so it runs in its own git worktree on the project's target,
its diff is reviewable on its own, and a correction cycle resumes the same
worker in the same tree. The tools are `delegate_build`, `wait_build`,
`task_diff`, `request_changes` and `accept_build` on the `lectern` MCP server.

Invoke `/lectern-delegate <request>` in Claude Code or
`$lectern-delegate <request>` in Codex.

## 1. Orient and classify

Read the repository guidance and the request. Decide whether this is a direct
small fix, one bounded build, or a multi-phase project. A typo, a one-line
change or an explicit "do it yourself" stays with you; do not force a
delegation onto it. For a substantial build, say in one sentence what you own
and what the worker will implement.

An explicit request to plan and build authorizes the whole workflow; do not ask
again after each phase. Ask only about a product or risk decision the
repository cannot answer.

## 2. Confirm the worker is on

`delegate_build` finds the project from your checkout path; `list_projects`
is only needed when the checkout is not registered. If Delegated builds is off or the worker is not runnable, the tool says so:
finish the plan, report that, and stop; do not implement the bundle yourself
in that case unless the user asks.

## 3. Design before dividing the work

Read `upstream/source/skill/references/planning.md`. Reuse an approved
design or plan when the repository has one. For new work, write an
appropriately sized design: objective, non-goals, evidence from the
repository, interfaces and contracts, failure behaviour, risks, acceptance
criteria. Architecture, auth, tenancy, payments, secrets and production
impact are your decisions; never hand them to the worker under a vague
"build it".

## 4. Write the brief

Use `upstream/source/skill/templates/task-brief.md`. One brief is one
coherent end-to-end bundle with exact contracts, a bounded file scope,
testable outcomes and the verification commands, by name, that prove them.
Internal discovery, implementation, testing and debugging belong to the
worker: do not write the implementation into the brief. Split only at a real
dependency or independent-acceptance boundary, never for visibility.

## 5. Dispatch and wait

Call `delegate_build` with `workdir` (your checkout's absolute path; or a
project name), a short title and the brief. It creates the task, starts the
worker and waits. It returns when the worker is finished, with the worker's
completion report, the branch, diff stats and, when the patch is small, the
patch itself under `diff`; or with `done:false` at its timeout, in which case
call `wait_build` with the task id. That is one wait, not polling: do not call `task_status`
for progress, do not work in the repository while the worker owns the
bundle, and do not treat a timeout as the worker being stuck.

One worker at a time by default. Two only for independent bundles the plan
named as such.

## 6. Review the actual result

Read `upstream/source/skill/references/review.md`. Worker completion means
ready for review, not accepted. Read the patch (`diff` in the result, or `task_diff` when it was too large
to inline) and the report against the brief, in one pass with two lenses: specification
compliance, then code quality and security. Spot-check where evidence is
missing or a failure is plausible; do not routinely rerun the worker's whole
suite. If corrections are needed, send all findings in one
`request_changes` call, then `wait_build` again. Default to one correction
cycle, then accept or explicitly reassess scope.

## 7. Integrate, verify once, finish

Accept with `accept_build`, passing `workdir` as your own checkout so the
worker's branch is merged there; a conflict is reported and nothing is half
applied. Run the cross-task checks once at a genuine integration boundary.
Do not commit, push, deploy or migrate because a build finished; the user's
own git permissions apply. Conclude with what was built, what actually
passed, and what remains open.
