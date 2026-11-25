---
name: github-issue-manager-catalex
description: Select, start, and complete Catalex development work from GitHub Issues using issue-only status labels, priorities, native sub-issues, and approval-gated completion commits. Use when the user requests GitHub issue task management or project instructions require it; a passing mention of GitHub is not enough.
---

# GitHub Issue Manager for Catalex

Use GitHub Issues as the task record; do not require GitHub Projects. Project instructions define implementation checks, branches, versions, and tags. Keep those commands out of this skill.

## Issue repository

Read applicable project instructions and `.githubissues.json` at the code repository root:

```json
{"issueRepository":"OWNER/REPO"}
```

The issue repository may differ from the code repository. Never infer it from the code remote when the user named a separate task repository. Verify the exact repository with `gh repo view` or an equivalent connected GitHub tool before selecting or changing issues. Keep authentication out of the config.

If the config is missing, use an exact issue repository already supplied for this project to create it and continue. Otherwise ask for the `OWNER/REPO` or issue-repository URL, verify access, and create the config. Do not select work from an ambiguous or inaccessible repository. Setup, lookup, and discussion do not themselves authorize implementation, status changes, or commits.

Prefer `gh` for the full workflow because it supports labels, native sub-issues, close reasons, and efficient search. A connected GitHub tool is acceptable when it supports the same operation. If authentication or a required mutation is unavailable, finish read-only preparation and report the missing access before changing task state.

## Issue-only states and priority

| GitHub issue | Meaning | Automatic selection |
| --- | --- | --- |
| Open with `in progress` | Active | First |
| Open without `in progress` or `wontfix` | Queued | After active work |
| Open with `wontfix` | Deferred | Never |
| Closed with completed reason | Finished | Never |
| Other closed issue | Closed/canceled | Never |

`wontfix` is this workflow's deferred label. Do not close or reopen issues merely to represent queue status. Treat conflicting `in progress` and `wontfix` labels as an inconsistency to resolve before selecting that issue.

Among queued issues, use `priority: urgent`, then `priority: high`, then `priority: medium`, then no priority label (normal). Keep at most one priority label. Active work takes precedence over every queued priority. Within a tier, use oldest GitHub `createdAt`, breaking exact ties by issue number. The migrated open issues were deliberately recreated after the completed archive, so creation order is the queue order. Do not use issue update time.

## Target routing

Read `targets` from `.githubissues.json`, which maps target labels to
`workspace` paths and expected `branch` names.

- Use the issue's own target label, falling back to its parent's.
- If the user specifies a target, filter top-level issues by that label
  before automatic task selection. Keep the existing selection rules
  otherwise.
- Work in the mapped workspace, follow its AGENTS.md, and verify its
  current branch matches the configured branch. Ask if the mapping is
  unresolved or the branch differs. Do not automatically create workspaces
  or switch branches, except for the approved integration worktree below.

## Select and start work

Continue an established active issue. For an explicitly named issue, fetch it directly and confirm it belongs to the configured repository. Otherwise, restrict every automatic selection query to parentless issues with `no:parent-issue`, querying open `in progress` issues server-side first. Only if none qualifies, query queued urgent, high, medium, and normal tiers in that order. Use the tested commands and pagination guidance in [references/search.md](references/search.md). Do not fetch the full closed archive or scan every issue to discover labels.

Inspect a short-listed top-level issue's labels before choosing it. After selecting it, inspect its direct children and follow the subissue flow, applying the existing active-first and priority ordering independently within that parent. For an explicitly named or established active child, confirm its parent is neither deferred nor closed before starting it. If no issue qualifies, report deferred work or that the queue is empty. Before implementation, read the selected issue's full body, comments, parent, direct children, and relevant source links. Keep imported Linear provenance intact.

When work actually starts, add `in progress` to the selected queued issue. If starting a child under a queued parent, mark the parent `in progress` too. Preserve priority, target, and other descriptive labels, including at completion. Add comments only for material implementation notes, blockers, verification, or follow-up context.

## Native sub-issues

Keep one level of subissues for this workflow, even though GitHub supports deeper nesting. Additional work on a child becomes a sibling under its parent. Create or link native sub-issues with `gh issue create --parent` or `gh issue edit --parent`; a text link alone is insufficient.

If a child is added after a previously childless parent's original task is complete but uncommitted, create an `Initial subissue` under the parent. Mark it `in progress`, summarize the original task and relevant parent comments, and finish it through the subissue gate.

Before a parent's completion gate, fetch all direct children and confirm the result is complete. Apply the same active-first and priority ordering to eligible children. If one qualifies, keep the parent `in progress` and ask exactly:

`Continue working on subissue <identifier> "<title>"? Reply yes or no.`

On yes, read its full details and mark it `in progress` as work starts. On no, wait. Other replies do not authorize starting it. If no child qualifies, proceed to the parent gate; mention deferred children without calling them complete. Do not close a parent while a selectable child remains.

## Finish work

Complete implementation and applicable checks before asking for completion approval. Track the active issue, parent, approval, version choice, applied version, issue updates, commit, and tag so retries do not duplicate work. Use project instructions for checks and version commands; never invent or skip required checks. Stage only task changes and preserve unrelated work. Keep the issue as the historical record. Do not push commits or tags unless requested.

Include each completed issue's qualified reference in the commit body, for example: `Catalex-app/Catalex-tasks#338`. One approved commit may cover related issues; do not create empty completion commits for changes already committed.

Keep the issue open with `in progress` until the selected completion path succeeds. Preparatory commits may be needed for integration, but do not push the destination branch or create release tags before verification passes. On failure, fix within the approved scope and rerun affected checks.

### Parent or standalone task

After checking children, ask these questions in order, skipping any already answered:

1. "Finish this task and commit? Reply yes or no."
2. "Keep it on the current branch or merge? Reply keep or name the destination branch."
3. Only when merging into main: "Bump the version? Reply no bump, patch, minor, or major."

On no to completion, keep the issue in progress. Otherwise, follow the selected completion path. Merges into other branches do not bump versions or create release tags.

An approved merge includes pushing the verified result. Publishing a draft release requires separate approval.

- Without merging: run the required checks, full build, and packaging, including completed child changes; then commit and close. Do not bump, tag, or push.
- With merging: review the full changes against the latest destination branch, clarify unexpected scope, and prepare the merge in a temporary worktree. Commit source changes first if necessary, keeping the issue open. For an approved bump into main, compute it once from the latest main version and update the changelog before running the required checks, full build, and packaging on the merged result. Without a bump, leave versions unchanged.
- Before completion, recheck direct children using the existing subissue rules. Before pushing, recheck the remote destination branch. If it has advanced, integrate it and repeat verification; if this changes the approved version choice, clarify before continuing. Never force-push the destination branch.
- After successful verification, push the verified commit to the destination branch and, if bumped, its annotated release tag. Without a bump, create no tag. For a release, confirm the tag workflow prepares the draft successfully.
- Close the issue only after the selected path succeeds.

Use `gh issue close --reason completed` and remove only `in progress`, preserving priority, target, and descriptive labels. Do not rely on commit-message auto-closing, especially when the task repository differs from the code repository.

After completion, ask exactly: `Move on to the next task? Reply yes or no.` On yes, select the next task; on no, wait.

### Subissue

State the parent before asking:

`Note: <identifier> "<title>" is a subissue of <parent identifier> "<parent title>".`

Ask exactly:

`Mark this subissue finished and create a git commit? Reply yes or no.`

On no, keep it `in progress` and wait. For other replies, repeat the gate unless the user explicitly changes the workflow. On yes:

1. Do not request a version choice, bump, or tag.
2. Run required non-build checks, tests, rendered UI checks, and harness checks; defer production builds to parent completion.
3. Commit the completed changes, then remove the child's `in progress` label and close it with reason `completed`.
4. Return to the parent and fetch its children again. If another qualifies, ask exactly: `Continue working on next subissue <identifier> "<title>"? Reply yes or no.` On yes, start it; on no, keep the parent `in progress` and wait. Otherwise, report deferred work and ask the parent completion gate.

## Recover from uncertain results

Retain approval through routine retries; ask again only if scope or version choice materially changes. Inspect commits, remote branches, tags, workflow runs, and issue state before resuming unfinished steps. Do not duplicate commits, recompute the approved bump, or rewrite release tags. Keep the issue open on failure; if pushing succeeded but the issue update failed, retry that update without undoing pushed work. Do not claim completion or advance while required steps remain unfinished.
