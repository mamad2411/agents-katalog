---
name: branch-review-before-pr
version: 2.0.0
description: |
  Gate a branch before it becomes a PR — catch the STRUCTURAL defects tests miss, not style: read the
  full diff against the default base, run a two-pass checklist (blocking pass first — unsafe queries,
  race conditions, trust-boundary and auth mistakes, conditional side effects — then the non-blocking
  remainder), and verify each candidate against surrounding code before reporting. Stays read-only and
  reports blocking-first; only becomes mutating after you explicitly approve a specific fix per issue —
  never batches decisions or auto-fixes. Use as the branch gate right before shipping or opening a PR.
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
  - Edit
  - Write
argument-hint: "[review focus or branch risk hint]"
arguments:
  - request
when_to_use: |
  Use when the user asks for a pre-PR review, when a ship workflow needs a blocking branch gate, or
  when a PR draft needs a fast structural audit. Examples: "/branch-review-before-pr", "review this
  branch before PR", "check for blocking issues before I ship". Do NOT use for a whole-repository
  launch sweep (that's go-live-audit), for the deep forked bug hunt (that's find-bugs), or for
  style-only nitpicks — this gate is scoped to the branch diff and reports structural risk, not preference.
effort: high
---

<EXTREMELY-IMPORTANT>
This skill is review-first and only becomes mutating after explicit user approval.

Non-negotiable rules:
1. Read the full diff before reporting any issue.
2. Load and respect `checklist.md`, including suppressions.
3. Stay scoped to the diff against the review base.
4. Stay read-only unless the user explicitly picks "Fix it now" for a blocking issue.
5. Keep findings terse, evidenced, and specific.
</EXTREMELY-IMPORTANT>

# Branch Review Before PR

## Inputs

- `$request`: Optional focus area, branch risk hint, or review scope clarification

## Goal

Review the current branch against the default base and:

- find structural defects that survive context checks
- separate blocking issues from non-blocking issues
- ask the user how to handle each blocking issue
- optionally apply only the fixes the user explicitly approves

## Step 0: Resolve the review base

Determine:

- the current branch
- the default review base, usually `origin/main` or `origin/master`
- whether the user wants full-branch review or a narrower scope

If the current branch is already the base branch, or there is no diff, stop and say so clearly.

**Success criteria**: There is an explicit diff base and actual branch delta to review.

## Step 1: Load the checklist and diff surface

Read:

- `checklist.md`
- the full diff against the base branch
- changed-file list when the diff is large

Rules:

- do not review from `--stat` alone
- do not report checklist items that are suppressed
- when the diff is large, read changed files individually with enough surrounding context to verify claims

**Success criteria**: The checklist is loaded and every changed file that matters has been read.

## Step 2: Run the two-pass review

Pass 1 is blocking-only:

- query and data safety
- race conditions and concurrency
- auth and trust boundaries

Pass 2 is non-blocking:

- all remaining checklist categories

For each candidate issue, verify:

- it is actually in scope
- it is not already fixed elsewhere in the diff
- surrounding code does not already mitigate it

**Success criteria**: All meaningful checklist categories were evaluated and false positives were filtered out.

## Step 3: Report all findings

Always report the full result set:

- blocking issues first
- then non-blocking issues
- explicit clean result if none were found

Use this structure:

```text
Branch Review: N issues (X critical, Y informational)

CRITICAL (blocking):
- [file:line] Problem description
  Fix: suggested fix

Issues (non-blocking):
- [file:line] Problem description
  Fix: suggested fix
```

**Success criteria**: The user can tell immediately whether the branch is blocked and why.

## Step 4: Handle blocking issues one by one

For each blocking issue, use a separate `AskUserQuestion` with:

- the issue and location
- the recommended fix
- these options:
  - `Fix it now`
  - `Acknowledge`
  - `False positive`

If the user chooses:

- `Fix it now`: apply only the approved fix
- `Acknowledge`: leave code unchanged and record the acceptance
- `False positive`: leave code unchanged and note the dismissal

Do not batch multiple blocking issues into one question.

**Success criteria**: Each blocking issue has an explicit user decision.

## Step 5: Apply approved fixes only

When the user chooses `Fix it now`:

- make the smallest correct code change
- keep changes scoped to the approved issue
- do not commit, push, or create a PR
- summarize what changed after the fixes are applied

If the user only acknowledges or dismisses issues, make no edits.

**Success criteria**: Only explicitly approved fixes were applied.

## When To Load References

- `checklist.md`
  Use for the detailed review matrix, suppressions, and issue categories.

## Guardrails

- Do not add `disable-model-invocation`; this skill must remain usable inside PR/ship workflows.
- Do not review unchanged files beyond what is needed to verify context.
- Do not report style preferences as issues.
- Do not fix anything unless the user explicitly approved that issue.
- Do not commit, push, or open a PR from this skill.

## Output Contract

Report:

1. the review base and branch scope
2. blocking findings
3. non-blocking findings
4. per-blocker user decisions if questions were asked
5. any fixes actually applied
