---
name: session-summary
description: Use when the user asks where a task stands, requests only remaining work, wants a checkpoint or handoff, or wants a closeout execution prompt from the full task history
---

# Session Summary Checkpoint

Assess the complete current Codex task. Treat this as an anytime, evidence-based checkpoint: assume work remains unless evidence proves that no agreed work remains. Do not execute proposed work.

## Mode and safety

- With no arguments, run read-only checkpoint mode.
- If the first argument is `handoff`, run lightweight handoff mode; remaining arguments are optional focus text.
- If the first argument is `remaining`, run read-only remaining-work mode; remaining arguments are optional focus text.
- If the first argument is `closeout`, run closeout-prompt mode; remaining arguments are optional focus text.
- Treat every other argument, including unknown mode-like text, as optional focus text in read-only checkpoint mode. Focus narrows emphasis but must not exclude material session information.
- In checkpoint mode, make no file changes and do not update trackers, memory, commits, deployments, messages, or external systems.
- In remaining-work mode, write nothing, change nothing, and return only the six remaining-work sections below. Do not generate or execute an implementation prompt.
- In handoff mode, write only the one handoff file described below. Do not update trackers, memory, commits, deployments, messages, or external systems.
- In closeout-prompt mode, write exactly one closeout artifact and return its paste-ready prompt; do not execute the prompt or update trackers, memory, commits, deployments, messages, or external systems.
- Never reproduce secret values from messages or tool output. Mention only the safe credential location when it is material.
- For every assessment-only Git command in every mode, set `GIT_OPTIONAL_LOCKS=0` or use `git --no-optional-locks` so inspection does not create or refresh repository locks. If a lock or other residue already exists, report it; do not create, remove, or repair it during assessment.

## Establish coverage before assessment

Resolve one complete transcript before drawing conclusions. Use this resolution order exactly:

1. When Codex exposes an exact current task or thread ID, use it as a hard branch. Probe candidate files' `session_meta.payload.id` and only relevant metadata (working directory or task identity); do not read transcript records yet. If an exposed exact ID yields anything other than exactly one candidate, stop log discovery and use limited loaded-conversation/compaction coverage. Do not search global logs for that ID, the current prompt, nonce, or marker after exact-ID failure.
2. Only when no exact ID is exposed, use the no-ID fallback. Build a plausible candidate set with filename-only matching and fields-only `session_meta`/CWD/task-identity probes. If metadata leaves multiple plausible candidates, use a non-printing path-only search for one distinctive recent user message from the loaded conversation, scoped specifically to response_item user-role records in those metadata-confirmed candidates. The search may return matching file paths only; it must not print, sample, or match against assistant, tool, or other record content. Only after that search leaves exactly one path may you read transcript records. A sole metadata-confirmed candidate may be read without the path-only search.
3. If metadata leaves zero candidates, stop log discovery and use the loaded conversation plus compaction summaries. If the path-only search leaves zero or multiple matches, stop log discovery and use the same limited coverage. Never open, print, head, tail, cat, or sample unconfirmed candidate JSONL content; never merge candidates or infer missing transcript content.
4. Report the coverage limitation visibly. Never silently claim full-session coverage.

When candidate resolution stops with zero or multiple matches, include this sentence shape in `## Coverage`: `Coverage is limited: <count> candidates remain ambiguous after <zero-or-multiple> path matches; no candidate transcript was opened, printed, merged, or inferred.`

For a confirmed Codex rollout log only, extract material `turn_context`, `event_msg`, and `response_item` records; exclude catalog, non-conversation, and tool-noise record contents unless they materially changed execution. Never quote, reproduce, summarize, or name excluded content; if material, say only `excluded non-conversation records`. Preserve legitimate user-message evidence. Use [the Codex log-format reference](references/codex-log-format.md) for record details and a safe fallback.

For a large confirmed log, inspect it in bounded chunks and preserve user corrections, tool evidence, failures, rejected approaches, and the exact stopping point. If coverage is limited, mark every conclusion that depends on the gap as limited rather than guessing.

## Analyze evidence and use delegation proportionately

Treat user requests and corrections as the authoritative source for objectives and preferences. Treat tool output, file inspection, tests, and live checks as evidence. Classify each material claim as `DISCUSSED`, `PLANNED`, `ATTEMPTED`, `COMPLETED`, or `VERIFIED`; implementation alone is not verified, deployed, or live-witnessed.

Analyze short tasks directly; do not delegate when coordination cost exceeds the benefit. For a short task with no useful concurrency, state in `## Execution Strategy` that no subagents and no parallel work are recommended, and name direct primary-model synthesis. For long tasks, when the runtime supports agents, delegate these independent, bounded extractions to cheaper agents when available:

1. chronology and objectives;
2. deliverables and verification evidence;
3. failures, blockers, decisions, and rejected alternatives.

The primary model must reconcile contradictions, determine the status, identify scope drift, and write the assessment and recommendations. Keep dependent decisions sequential, recommend parallelism only for genuinely independent work, and do not recommend a subagent for trivial edits.

When a long task contains three independent material transcript slices, the assessment must recommend bounded lower-cost parallel extraction and primary-model centralized reconciliation or synthesis. If the current runtime cannot run agents, recommend that routing for the next capable runtime; do not conclude that no subagents are necessary merely because the input is regular or already partitioned.

## Status definitions

- `ON TRACK`: agreed work remains, but evidence shows progress and no material threat to the current path.
- `AT RISK`: agreed work remains and a material uncertainty, dependency, gap, or drift threatens progress or outcome.
- `BLOCKED`: a material dependency, required decision, access constraint, or failure currently prevents the next meaningful action.
- `COMPLETE`: evidence shows every agreed objective is completed and verified as appropriate, and no agreed work remains. Conversation ending, an implementation claim, or an unverified test is never enough.

## Output recipe

Write the following headings in exactly this order. Each required label must be a Markdown ATX level-two heading exactly as shown below: every heading line starts with `## `, never a bold substitute. Use `None — <reason>` whenever a section has no applicable content. Keep it compact enough to scan, but include exact paths, commands, identifiers, evidence, and stopping points where material.

## Coverage

State session/task identity, transcript source, time span when available, whether full coverage was established, and all known gaps.
When the complete supplied loaded-conversation fixture was assessed and no transcript log applies, include: `Full coverage of the supplied fixture was established.` Do not use this sentence for partial fixture evidence.

## Current Position

State exactly one of `ON TRACK`, `AT RISK`, `BLOCKED`, or `COMPLETE`, with a short evidence-based explanation.

## Objectives

State the original objective, current objective, user corrections, and accepted or suspected scope changes.

## Accomplished and Verified

List outcomes with their `COMPLETED` or `VERIFIED` state, locations, and supporting evidence. Separate completed-but-unverified work from verified work.

## In Progress

State each started but unfinished item, its state, and its exact stopping point.

## Not Done

List planned, deferred, rejected, or not-started work and the reason each remains undone.

## Issues, Risks, and Blockers

Separate resolved issues, active blockers, dependencies, risks, failed attempts, and approaches rejected with evidence.

## Decisions and Assumptions

Record decisions and rationale, rejected alternatives, and assumptions still needing validation.

## Insights

Capture non-obvious findings, patterns, user preferences demonstrated in the task, and implications.

## Recommendations

Provide prioritized advice distinct from decisions already made.

## Execution Strategy

Recommend only useful subagents, parallel work, loops, workflows, skills, model routing, approval gates, and stop conditions. Distinguish independent parallel work from sequential dependencies.

For that long-task case, the Execution Strategy must state the bounded extraction scopes, parallel routing, lower-cost model choice, primary-model reconciliation or synthesis, and the current-runtime or next-capable-runtime boundary.

## Open Questions

Include only questions whose answers materially affect progress.

## Potential Next Steps

Give a short ordered set of continuation options.

## Recommended Next Move

Name exactly one concrete immediate action, including required arrival verification or evidence when relevant.

## Continue or Restart

Recommend continuing in the current chat or restarting, based on remaining work, context size, task cohesion, coverage, and handoff quality.

## Remaining-work mode

When invoked as `session-summary remaining [optional focus]`, apply the same transcript-coverage, evidence-state, privacy, and proportional-analysis rules, but return only unfinished or decision-relevant material. Write nothing and change nothing. Do not create an artifact, generate an implementation prompt, or execute any proposed work.

Use exactly these headings in this order, with `None — <reason>` when empty:

## Remaining Work

List agreed unfinished work in dependency order with state, stopping point, owner boundary, acceptance check, and evidence needed. Do not repeat completed work except when a short verified prerequisite is essential to understand an unfinished item.

## Bugs and Blockers

List reproducible defects, active blockers, dependencies, risks, failed attempts, and the exact unblock or diagnostic action when known.

## Improvements

List small directly related improvements separately from broader optional enhancements. Do not silently convert suggestions into agreed scope.

## Insights

State non-obvious findings and implications that materially affect the remaining work.

## Recommendations

Give prioritized advice for closing or de-risking the remaining work, without turning the response into an execution prompt.

## Decisions Needed

List only unresolved decisions that materially affect progress, including the owner, options or tradeoff, and the latest safe decision point. State coverage limitations inline where they weaken an item; do not add extra sections.

## Lightweight handoff mode

When invoked as `session-summary handoff [optional focus]`, produce the same assessment and save it as one concise Markdown handoff. Determine `<project-root>` from the confirmed current project. Write to `<project-root>/docs/handoff/SESSION-SUMMARY-<YYYY-MM-DD>-<slug>.md`; if no project applies, write to `~/projects/.claude/handoffs/`. Never overwrite an existing artifact. Try the unsuffixed base filename first, then `-<HHMM>`, then `-<HHMM>-2`, `-<HHMM>-3`, and so on until the candidate filename is unused. Create exactly one artifact at the selected unused path.

The saved handoff must contain the assessment plus exact project paths, relevant commands, identifiers, verification instructions, and a warning for destructive, external, approval-gated, or unresolved actions. Then return one paste-ready restart prompt that names the handoff file, states the objective, asks the arriving agent to verify current state before editing, and names the first proposed action. Label it `session-summary handoff`.

Do not create any other artifact in handoff mode.

## Closeout-prompt mode

Before creating the closeout artifact, perform the same remaining-work assessment defined above and use it as the source queue. Do not return that intermediate assessment separately.

When invoked as `session-summary closeout [optional focus]`, use the same transcript-coverage, evidence-state, privacy, and proportional-delegation rules above, but assess only what remains and how to close it. Determine `<project-root>` from the confirmed current project. Write exactly one Markdown artifact to `<project-root>/docs/handoff/SESSION-CLOSEOUT-<YYYY-MM-DD>-<slug>.md`; if no project applies, write to `~/projects/.claude/handoffs/`. Never overwrite an existing artifact. Try the unsuffixed base filename first, then `-<HHMM>`, then `-<HHMM>-2`, `-<HHMM>-3`, and so on until the candidate filename is unused. Create exactly one artifact at the selected unused path. Then repeat the complete paste-ready prompt in chat. Create no other file and perform no action proposed by the prompt.

Classify each queue item as `[REQUIRED]`, `[INCLUDED]`, or `[OPTIONAL]`: agreed work, defects, verification, directly affected documentation, and delivery closure are required; small adjacent work demonstrably necessary to close or de-risk a required item may be included; broader suggestions remain optional and outside execution scope until accepted. Give each actionable item a stable ID, priority, dependency, `[AUTO]` or `[GATED]` tag, exact stopping point, `Done when` acceptance check, and required evidence. `[AUTO]` means reversible and already authorized in scope. `[GATED]` means credentials, destructive cleanup, spending, publication or external messages, scope expansion, or an authorization not already supplied. Do not turn every recommendation into work.

Write these headings in exactly this order. Each is a Markdown ATX level-two heading. Use `None — <reason>` when empty.

## Coverage

State task identity, transcript source, time span when available, whether full coverage was established, and the gaps that limit the queue.

## Closeout Objective

State the outcome that must be true after execution, including agreed delivery, verification, documentation, integration, repository cleanliness, and deployment only when it is actually in scope.

## Verified Baseline

Include only completed facts the execution prompt depends on. Label each `VERIFIED`, `COMPLETED`, `USER-STATED`, or `ASSUMED`; give the exact evidence or arrival check. Do not narrate unrelated completed work.

## Remaining Work Queue

List the stable-ID queue in dependency order with classification, gate, priority, owner or writer boundary, exact path or system, stopping point, `Done when`, and evidence requirement. If no agreed implementation remains, keep documentation, integration, cleanliness, and final verification work here; do not invent features.

## Bugs, Risks, and Blockers

Separate reproducible defects, active blockers, dependencies, risks, failed attempts, ownership conflicts, and unknowns. Give the exact unblock or diagnostic action when known.

## Improvements and Recommendations

Separate `[INCLUDED]` closeout improvements from `[OPTIONAL]` future recommendations. Explain why each included improvement is necessary and why each optional recommendation is not part of this execution scope.

## Dependencies and Execution Strategy

Show the critical path, safe parallel waves, sequential joins, controller/writer ownership, useful skills and tools, lower-cost bounded extraction or worker tasks, primary-model reconciliation, verification loops, stop conditions, and runtime limits. Optimize for elapsed time without creating competing writers or bypassing evidence.

## Approval Gates

List only unresolved gates. A prior explicit user instruction to commit, push, create or update a PR, merge, or deploy counts as authorization for that named action, but never as authorization to bypass branch protection, required review, credentials, destructive cleanup, or missing deployment infrastructure.

## Definition of Done

Define observable project-level closure: all `[REQUIRED]` and accepted `[INCLUDED]` items verified; relevant tests, lint, build, security, and acceptance checks pass; affected documentation and canonical task/status surfaces agree; intended changes are in logical commits, pushed, reviewed, checked, and merged; the worktree is clean without deleting unrelated user work; merged and deployed SHAs are recorded separately when deployment is in scope; optional work is explicitly deferred.

## Closeout Prompt

Begin the copy-ready prompt with `Read the closeout artifact at <absolute-path>.` using the selected artifact's fully resolved absolute path. Repeat that same absolute path in the chat prompt.

Return one copy-ready prompt that references the artifact by absolute path and charges the next agent as the closeout controller. The prompt must require all of the following:

1. Read applicable repository instructions, the artifact, plans, handoffs, documentation, and canonical task/status sources. Treat the closeout artifact as potentially stale until verified. Inspect the exact repository, branch, HEAD, remotes, worktrees, dirty files, active owners, PRs, checks, deployment state, and task state before editing.
2. Reconcile the artifact into a dependency-aware queue and work the critical path first. Use all safe, relevant, in-scope means available: appropriate skills, tools, subagents, parallel work, workflows, tests, and lower-cost models. Parallelize only independent work. Maintain one controller and one writer per repository or shared artifact; keep integration and contradiction resolution with the primary controller.
3. Complete every `[REQUIRED]` and accepted `[INCLUDED]` item to its `Done when` check. Repair directly related defects and small de-risking improvements. Leave `[OPTIONAL]` recommendations unimplemented unless separately authorized.
4. Continue the implement-test-verify-reassess loop until the queue is empty or a genuine external blocker prevents progress. Do not report `COMPLETE` because time, context, or budget is running low. On a blocker, exhaust safe in-scope alternatives, preserve exact evidence, and report the precise unblock action.
5. Never expose secrets or bypass authentication, required review, CI, branch protection, security controls, or user-owned changes. Stop at unresolved `[GATED]` items.
6. Run proportionate targeted and full verification, resolve actionable review feedback, and bind evidence to the exact commit. Reassess for regressions and newly revealed required work after each integration wave.
7. Update every documentation and state surface invalidated by the work, including applicable README, project and architecture docs, operational/deployment docs, changelog or release notes, governance instructions, decision/status files, and canonical task trackers. Avoid shadow state that exists only in the closeout artifact.
8. Clean the repository safely: preserve unrelated dirty or untracked work; remove only known generated or temporary artifacts; stage only intended paths; create logical commits; push; open or update the PR; satisfy checks and required reviews; merge using the repository's protections; then verify the merged SHA, remote state, and clean working tree. Do not delete branches or worktrees merely for appearance.
9. Merged is not deployed. Deploy only when deployment is part of the agreed scope and a real target, documented procedure, credential boundary, rollback, and live acceptance check exist. Verify the exact deployed SHA and live behavior separately; otherwise report `merged, not deployed`.
10. Return a final closeout report with queue disposition, blockers, tests and checks, commits, PR, merged SHA, documentation updated, repository cleanliness, deployment and live-witness state, canonical tracker reconciliation, and optional recommendations deliberately left for later.
