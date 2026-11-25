---
name: codex-automation-audit
description: Audit recent Codex automation and personal skill runs, compare task behavior with prompts and local docs, then prepare numbered patch-ready recommendations without changing files during the scheduled run.
---

# Codex Automation Audit

## Goal

Review Codex automation and personal skill tasks from the previous seven complete days. Find repeated corrections, edited approvals, rejected steps, and manual steering. Map each issue to its current automation, skill, or named Markdown owner.

The scheduled audit is read-only and recommendation-only. A later reply may patch only approved recommendation numbers.

## Schedule context

Use the seven full calendar days before the run date in the automation's timezone. Exclude the current day. A Thursday run covers the prior Thursday through Wednesday.

## Primary sources

1. Automation definitions under `${CODEX_HOME:-$HOME/.codex}/automations/*/automation.toml`
2. Automation memories and runbooks under `${CODEX_HOME:-$HOME/.codex}/automations/**`
3. Codex task tools such as `list_threads` and `read_thread`
4. Markdown files named by automation prompts or skills
5. Personal skill folders under `${CODEX_HOME:-$HOME/.codex}/skills`
6. Manual Codex tasks where a personal skill was used or clearly followed

## Task tool fallback

Try `list_threads` once and each needed `read_thread` once. Stop a call after 60 seconds. If needed, use matching files under `${CODEX_HOME:-$HOME/.codex}/sessions/YYYY/MM/DD/` and use summaries only as a map. Report partial live-task coverage. Direct task text outranks summaries. The same privacy limits apply.

## Task scope

Include scheduled and direct runs, heartbeats, linked child or follow-up tasks, manual skill use, and the prior weekly audit. A task is linked by title, URL, workspace, or direct reference.

## Audit workflow

1. Read current automation definitions before judging a run.
2. Map tasks to their automation or personal skill and find user interventions.
3. Read the owning prompt, skill, and named Markdown files.
4. Find stale, mixed, duplicate, slow, unsafe, or unproved steps.
5. Treat memory as evidence, not the only truth.
6. Keep each workflow's privacy and no-send limits. Do not read private lead rows, raw transcripts, PDFs, workbooks, archives, credentials, or client exports unless the user asks for that exact needed file.
7. Patch the skill or named doc when it owns the behavior. Patch the launcher only when it owns the problem.

## Recommendation bar

Inspect the current prompt, owning skill, and named docs before drafting a patch. Use this order:

1. Delete a stale, duplicate, conflicting, or unneeded instruction.
2. Simplify or merge an existing instruction.
3. Replace one existing instruction when deletion would remove needed behavior.
4. Add a new instruction only when no current instruction can safely own the behavior.

For a repeated portrait-quality issue, find the current portrait gate first. Do not add a second gate when one can be removed or changed.

Label every recommendation `Change type: Delete`, `Simplify`, `Replace`, or `Add`. An `Add` must state why existing text cannot be changed.

Recommend a change after two matching corrections. One is enough for a risky action, wrong person or source, privacy problem, destructive change, failed run, or large waste. Independent improvements need proof, useful impact, and low risk.

Every patch-ready item needs a `Safety test` covering the failure, one core behavior, and one safety boundary. A deletion must name its rollback trigger.

When two sources conflict, keep one owner of truth and delete the duplicate. Do not add the same rule to many files.

## Scheduled output

Keep the report in the Codex task unless the user asks for a file. Start with a short summary, then one section per automation or skill.

Each section names reviewed tasks, repeated changes, proof, root cause, and file owner. Each recommendation includes `Existing rule checked`, exact target and patch, `Change type`, expected result, `Safety test`, confidence, and status. Separate fixes from independent improvements.

Number every recommendation as `R1`, `R2`, `R3`, and so on.

For patch-ready items, give exact target paths and exact replacement or added text. Keep each change small.

End with: `Reply with specific recommendation numbers, or approve all, and I will patch only the approved items.`

## Approval and patch mode

Patch only approved numbers. `approve all` covers every patch-ready item in the latest audit plus any other item clearly approved. Ask one short question if approval is unclear.

Re-read each target. Keep unrelated changes. Use small edits only in approved prompts, skills, or named Markdown files. Rewrite a full prompt only when the approved recommendation proves it is broken and gives the new shape.

Run the `Safety test`, existing validators, and scenario cases. Re-read the diff. If a core behavior or safety boundary fails, revert only that patch and report it.

Use Git history instead of dated backup folders. Record the current commit when available. For an unversioned target, keep the reverse patch in the task until tests pass.

Report changed files, behavior, tests, rollbacks, and blocked approved items.

## Safety rules

- Scheduled runs only read and recommend.
- Approved replies edit only approved prompts, skills, or named Markdown files.
- Never send an external message, change a live app, deploy, or touch an unrelated repo without a separate clear request.
