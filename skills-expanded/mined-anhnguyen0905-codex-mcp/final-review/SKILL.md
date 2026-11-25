---
name: final-review
description: Run the final review, improvement gate, and retro.
---

# Final review (embed into Codex prompts)

**Helpers**: required — requirements-coverage.mjs, project-context.mjs, session-cost.mjs, flow-state.mjs (scripts/flow-state.mjs; helper rule: missing or non-zero means stop and tell the user to reinstall the plugin).

## Phase 5 — Review (final)

8. **After the last task**: `flow-state advance` moves `execution → review`; repeat after improvement tasks (only place `phase: review` is written)
   and set `wave -`, then do a dual review — Claude's pass PLUS required
   `mcp__codex__codex_review`. Review the baseline-to-working-tree diff with
   `git diff runBaselineRef` (the one-argument form), taking `runBaselineRef` from
   `.codex-flow/STATE.md`; never use a resume-point ref for final review. This includes
   checkpoint/merge commits plus staged and unstaged changes. Also inspect untracked files from
   `git status --porcelain`. When `dirtyBaseline` names `baseline-dirty.patch`, subtract the
   run-start hunks and untracked paths recorded in that manifest when attributing run changes;
   report them as pre-existing instead. Compare current failures against the original
   `knownRed` list from STATE.md; only failures absent from that run-start list are new. The step-4
   rule for a failed, timed-out, or `partial` `codex_review` applies here too. Compare the final
   findings per the review-dual comparison protocol, verify every finding, and append non-blocking
   suggestions from BOTH reviews to `.codex-flow/IMPROVEMENTS.md`. Route verified CRITICAL/HIGH
   findings to the relevant Phase-4 IMPLEMENTATION `sessionId` through the same
   `mcp__codex__codex_continue` fix/re-review loop; repeat up to 3 rounds before delivery. Run the
   full test suite, AND verify the feature end-to-end by exercising the changed behavior (run the
   app/flow, not only unit tests). Re-run
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/requirements-coverage.mjs" --requirements .codex-flow/REQUIREMENTS.md --tasks .codex-flow/TASKS.md --plan .codex-flow/PLAN.md`;
   Walk the effective
   REQUIREMENTS.md set ID-by-ID, reporting met/not-met with evidence (test name, file, or
   demonstrated behavior); any not-met ID blocks completion. Then summarize the delivered change,
   remaining risks, and suggest a commit message. With per-task checkpoint commits, offer to squash
   the `wip(codex-flow)` commits into one clean commit (or keep them — user's call). Do not commit
   or squash unless the user asks. Record the final comparison in the report dir's `reviews.md` per
   `codex-flow:session-report`, and once in the Decision log using the non-task event-block schema
   from `codex-flow:plan-architecture`. When any Decision-log block of this run records a contract
   deviation under `Contracts touched` or a Decision naming an architecture change, run
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/project-context.mjs" --refresh` and show the user the
   resulting `.codex-flow/PROJECT.md` diff for confirmation (owner notes survive a refresh).
9. **Improvement decision gate**: run it per `codex-flow:review-dual`, which carries the whole gate
   (pending-entry definition, the missing-ledger "no improvements" case, slicing approved items into
   `.codex-flow/TASKS.md` with `(approved: T<n>)` / `(declined)` ledger markers, and the no-re-trigger
   rule for gate-spawned tasks). Before appending any approved task, FIRST run `flow-state improvement-gate`. Slice
   approved items into new tasks appended to `.codex-flow/TASKS.md`.
   Run the impact analysis, the coverage lint with `--plan .codex-flow/PLAN.md`, and backlog sanity
   checks, then get backlog re-approval;
   only afterward run `flow-state approve backlog` then `flow-state advance` before scheduling the new tasks, which run
   through the normal Phase 4 → Phase 5 loop. Before the final completion `flow-state advance`, append one ledger line per `codex-flow:run-ledger`.
   After the improvement decision gate has fully resolved — all approved improvement tasks have
   been executed and reviewed, or no improvements are pending — and just before delivering the
   final summary, generate `cost.md` from the project root per `codex-flow:session-report`. Read
   `<session-start ISO>` from PLAN.md's recorded `- Session start: <ISO 8601>` line, falling back to
   the report-dir timestamp in local time, and run:
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/session-cost.mjs" --since "<session-start ISO>" --session <task session ids…> --session <review session ids…>`
   using every task `- Session:` id and every `Codex review session:` id recorded in `reviews.md`;
   use `--cwd <project root>` only when no session id exists.
   Embed its output in `cost.md`; always include the Claude
   qualitative section, never fabricate numbers, and never embed raw stderr.
   Generate `SUMMARY.md` in the report dir per `codex-flow:session-report` and mention both
   reports in the final delivery summary. Only after the improvement gate and all final review, requirement,
   cost, report, and delivery gates complete, run `flow-state advance` until `phase: complete`
   (twice when improvement tasks returned the run to `execution`).
10. **Retro**: per `codex-flow:skill-selection` Step 8, if the flow produced reusable domain
   knowledge no indexed skill covers, offer to save it as a new skill in the local library and
   rebuild the index.
