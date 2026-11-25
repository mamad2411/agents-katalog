---
name: issue-batch-followup
description: Use when a human is reviewing a single issue branch produced by issue-batch-sdd, requests changes, approves the issue, or asks to open a GitHub or Gitee pull request from issue-sdd artifacts.
---

# Issue Batch Followup

Continue one `issue-batch-sdd` issue after `DONE_FOR_HUMAN_REVIEW`: read the issue artifacts, handle human review feedback on the existing issue branch, update the artifacts, and create a GitHub or Gitee pull request only after explicit human approval.

## Scope

Use this skill for a single issue branch that came from `issue-batch-sdd`.

Do not use this skill for:

- starting a new issue batch
- implementing unrelated issues
- opening pull requests for branches not produced by `issue-batch-sdd`
- platforms other than GitHub or Gitee

**Required background:** This skill reuses `issue-batch-sdd`'s artifact layout, branch rules, artifact-commit rules, and the canonical status lifecycle — see that skill for definitions. The handoff point is `DONE_FOR_HUMAN_REVIEW`.

## Core Rules

- Handle exactly one issue at a time.
- Work on the existing issue branch. Do not create a new followup branch unless the human explicitly asks.
- Treat human feedback as authoritative but keep it inside the selected issue scope.
- Do not commit `.agents/issue-sdd/` artifacts; artifact content may only be summarized or copied into the pull request description.
- Do not create a pull request until the human explicitly approves the issue or asks to open the PR/MR (see [Human Approval Gate](#human-approval-gate)).
- Remote issue and PR operations are supported only on GitHub and Gitee: use `gh` CLI for GitHub and the Gitee MCP tools for Gitee.

## Inputs

Find the issue from one or more user-provided hints:

- issue id or title
- issue artifact path
- branch name
- batch directory
- remote issue URL

Resolve in this order:

1. Match the hints against `.agents/issue-sdd/*/progress.md` (the Status table carries a `Branch` column). If exactly one issue matches, use it.
2. If no hint matches, use the current branch name as the input and resolve it against `progress.md`.
3. If multiple candidates match and the current branch cannot disambiguate, ask the human to confirm the branch or batch directory before proceeding.

To list candidate issues, prefer running the listing script `scripts/list-issues.sh` instead of reading each `progress.md`. It prints `<batch>\t<progress row>` for each issue row that has a branch.

## Artifact Contract

The artifact layout is defined by `issue-batch-sdd` (see its Batch Artifacts section); this skill does not redefine it.

Read the useful files for the selected issue before changing code, especially the issue directory's `brief.md`, `implementer-report.md`, `reviewer-report.md`, and `decision-needed.md` if present.

This skill additionally creates/updates two files in the issue directory, kept concise and factual:

- `followup-report.md` — create/update during this skill
- `pr-body.md` — create/update before PR/MR creation

### `followup-report.md`

```text
# Followup Report

## Human Feedback

- <date/time>: <change requests or approval message>

## Followup Changes

("None changed" if approved without change requests)

### Assessment

- In scope: <yes/no>
- Reason: <why this is in or out of scope>
- Decision needed: <yes/no and what>

### Changes Made

- <what changed and files touched>

### Verification

- <tests: pass | fail | not run>

### Remaining Risk

- <risk or "None known">

## Approval

- Status: <approved/rejected>
- Approved by: <human name or "user">
- Approval note: <approval summary>
```

### `pr-body.md`

Use this file as the source for the PR/MR body. It is the public version of the artifacts.

```text
## Issue

<remote issue reference if available>

## Summary

- <implementation summary>

## Verification

- `<command>`: <result>

## Risks

- <risk or "None known">
```

Do not paste private scratch notes, chain-of-thought, unrelated logs, or raw `.agents` file dumps into the PR body.

## Workflow

1. **Identify one issue.** Confirm the issue id/title, branch, and artifact directory.
2. **Check status, then switch to the issue branch.** Do not overwrite unrelated user changes.
3. **Read artifacts.** Read the issue brief, implementation report, reviewer report, decision note if present, and relevant batch files.
4. **Classify the human feedback** and note it in `followup-report.md`:
   - If in scope and actionable, implement it.
   - If unclear, ask one focused question.
   - If it changes product behavior, permissions, storage, schema, audit semantics, or issue scope, ask the human for confirmation.
   - If it is a new issue, recommend creating a separate issue instead of expanding this branch.
   - If it is an approval, go to step 8.
5. **Make requested changes.** Use the repo's normal development and test practices.
6. **Verify.** Run the smallest relevant checks that prove the followup. Broaden verification if shared behavior changed.
7. **Wait for approval.** If the human has not approved, report that the branch is ready for another human review.
8. **Commit code changes when appropriate.** Commit only intended repository changes; keep `.agents/issue-sdd/` uncommitted.
9. **Update artifacts.** Update `followup-report.md` and `progress.md`.
10. **Prepare PR/MR body.** Write `pr-body.md` from the public artifact summary.
11. **Create PR/MR only after explicit approval.** Push the issue branch if needed, then use the platform-specific path below.

## Status Updates

The canonical status lifecycle is defined by `issue-batch-sdd` (see its Statuses section); this skill does not redefine it. It transitions the selected issue through the post-review statuses: `HUMAN_CHANGES_REQUESTED`, `FOLLOWUP_IN_PROGRESS`, `APPROVED_BY_HUMAN`, `PR_OPENED`, or `FOLLOWUP_BLOCKED`.

Update the selected issue row in `progress.md` when useful, and append a timestamped ledger entry for each meaningful transition.

## Git Operation Contract

Before committing or pushing:

- inspect the worktree status
- stage only intended repository files
- leave `.agents/issue-sdd/` unstaged
- do not delete or rewrite human changes unrelated to the issue
- use the existing repository commit style if one is obvious

Before PR/MR creation:

- ensure the issue branch has the intended commits
- push the issue branch to the matching GitHub or Gitee remote if it is not already pushed
- confirm the PR/MR body comes from `pr-body.md`, not from raw artifact dumps

### GitHub Path

Use this path when the target repository remote is GitHub.

1. Inspect remotes and branch.
2. Determine the base branch from `triage.md`, the current branch's upstream, or the repository default from `gh repo view`.
3. Determine issue association:
   - If the source issue is in the same GitHub repository, include `Refs #<number>` in `pr-body.md`.
   - If the human explicitly wants auto-close behavior, use `Closes #<number>` or `Fixes #<number>`.
4. Create the PR:

```bash
gh pr create --base <base-branch> --head <issue-branch> --title "<title>" --body-file <path-to-pr-body.md>
```

If `gh` is not authenticated or the repository is not on GitHub, stop and report the blocker.

### Gitee Path

Use this path when the target repository remote is Gitee.

1. Identify `owner`, `repo`, current branch, target base branch, and issue number if available.
2. Use the Gitee MCP `create_pull` tool (service `mcp_gitee`), not raw HTTP calls.
3. Set:
   - `owner`: repository owner path
   - `repo`: repository path
   - `base`: target branch
   - `head`: issue branch, or `namespace:branch` if needed
   - `title`: concise issue title
   - `body`: contents of `pr-body.md`
   - `issue`: source issue number when the source is a Gitee issue and the MCP field applies

Also include the issue reference in the body so the association remains visible even if platform linking behavior differs.

### Unknown Platform

If the repository platform cannot be identified as GitHub or Gitee, stop and ask the human what to do.

## Human Approval Gate

Explicit approval examples:

- "approved, open the PR"
- "looks good, create the MR"
- "审核通过，帮我提 PR"
- "可以提交到 Gitee"

Not approval:

- "run tests"
- "looks closer"
- "fix this last thing"
- "what would the PR say?"

When in doubt, ask before creating the PR/MR.

## Red Flags

Stop and ask for human direction if:

- multiple issue artifact directories match
- the current branch does not match the selected issue
- there are unrelated uncommitted changes
- human feedback expands beyond the issue brief
- followup requires schema, permission, audit, migration, or storage changes not already specified
- verification cannot run for environmental reasons
- the remote is not GitHub or Gitee
- platform auth is missing
- the human asks to commit `.agents/issue-sdd/`

## Summary

When PR/MR is created, report:

- PR/MR URL or number
- linked issue reference
- verification summary
- any residual risk
