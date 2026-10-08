---
name: spade-plan
description: Write a SPADE Plan from a locked Scope and take it to approval. Use when a Scope exists and someone says "plan this", "generate a plan", "break this down", "approve the plan", "review the plan", or when an issue is in Scoped or Approval status. Invoked by /spade at the Plan and Deliver levels.
---

## Mode Resolution

Read `.spade/config` if it exists and resolve `mode:` per `references/FRAMEWORK.md` § Operating modes.
With no config, work as `local`.

# SPADE Plan

Turn a locked Scope into a Plan a human can approve in a few minutes, then record the approval (`references/FRAMEWORK.md` § Plan and § Approve).
Done means: `.spade/plans/<scope-key>.md` exists in the format below with an approval line, and in `linear` mode the Plan is posted on the Scope issue and the issue is in Delivering.

The Plan is for the human who approves it, not a script for the agent that delivers it.
Put effort into the approach, the forks you rejected, and the risks; keep tasks to one line each.

## Before writing

- Read the Scope. If it is missing intent, checkable acceptance criteria, or constraints, stop and send it back to `/spade-scope`.
- Read ARCHITECTURE.md, PATTERNS.md, and ANTI-PATTERNS.md, and look at the code the Scope touches.
- Read active entries in `.spade/learnings/` (not `private/` unless the human opts in) whose tags or `scope_ref` match the work, and use the ones that apply. Say which ones you used.

## The Plan

Use the format in `references/FRAMEWORK.md` § Plan.

- **Approach.** What will be built and how, the patterns and libraries it uses, and the forks you rejected, each with the reason it lost.
- **Risks.** Assumptions that could be wrong and what changes if they are. Name any conflict with ARCHITECTURE.md or ANTI-PATTERNS.md here; a conflict needs the human's explicit approval.
- **Tasks.** Checkbox lines in delivery order, each an outcome with "done when" and "verify with". Prefer vertical slices a user, caller, or operator can observe; a preparatory task says what it enables. Mark work that needs a human with `(human)`, for example a stakeholder decision, access only a person has, or a physical check.
- **Bundles.** Only when more than one PR is genuinely better: independent tasks with no shared files, where separate review or revert is worth it.

If the Plan exceeds `autonomy.size_ceiling` in `.spade/config` (default 7 tasks or 12 changed files), say so; under `/spade` that is a tripwire.

Apply `/unslop` to the prose, then write the file to `.spade/plans/<scope-key>.md`, where `<scope-key>` is the tracker id or the local Scope slug, and move the Scope to Approval (issue status, or `status: approval` in a local Scope file).
When pandoc is installed, render it with `spade-render <file>` and give the `file://` link.

## Approval

When `/spade` invokes this skill, stop after writing the Plan: `/spade` runs the review first and then either asks for approval as below (Plan level) or records its own (Deliver level).

Otherwise, show the Plan and ask through `{{SPADE_ASK_USER}}`: *Approve*, *Approve with notes*, *Revise*, or *Reject*.
Before asking, give your own one-line read on each of: architecture fit, gaps, assumptions, task breakdown.
When this skill runs on its own, offer `/spade-review` first and recommend it if the change touches architecture, security, or cross-system boundaries; under `/spade` the review has already run.

- **Approve** (with or without notes): add `Approved by <name>, <date>.` under the Scope line, plus any notes. In `linear` mode post the Plan as a comment on the Scope issue and move it to Delivering; in `local` mode set the Scope file's `status:` to `delivering`.
- **Revise**: take the human's feedback, rewrite the Plan, and ask again.
- **Reject**: record the reason in the Plan's Halts section, move the Scope back to Scoped (the issue in `linear` mode, `status: scoped` in a local Scope file), and stop.

Do not start delivery before approval.

## Finish

End with the run summary (`references/FRAMEWORK.md` § Run summary).
Under Blocked on me, say whether the Plan is waiting for approval; after approval, the next step is `/spade` to deliver.
