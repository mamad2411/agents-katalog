---
name: pr-lifecycle
description: "Takes a GitHub pull request from open to merged with gh, following repository policy. Use when opening a PR, fixing its checks, answering review threads, updating its branch or merging. Not for posting a code review (use review-transport); not for issues (use github-issues:issue-lifecycle-github)."
when_to_use: "open a PR, why are my checks failing, wait for CI, address review comments, resolve review threads, update the PR branch, merge this PR"
allowed-tools: Bash(gh auth status), Bash(gh repo view *), Bash(gh pr view *), Bash(gh pr checks *), Bash(gh pr diff *), Bash(gh run list *), Bash(gh run view *), Bash(git status *), Bash(git branch --show-current), Read, Grep, Glob
license: MIT
---

# pr-lifecycle

A pull request moves through a few states: unopened, draft, checks red, feedback open, mergeable,
merged. Each section below is the next command for one state. Merge strategy, required checks and
branch protection belong to the repository, so read them rather than assuming.

Run `gh auth status` first; an auth failure otherwise surfaces as a confusing 404. The `gh` login is
for interactive, user-scoped work like this. For an unattended run, mint the org GitHub App token
instead (see `dev-standards:secrets-management`, "GitHub access"), and never run `gh auth login`
or `gh auth refresh` from an agent session. Outside a
checkout, add `--repo <owner>/<repo>` to every `gh` call. In `gh api` paths, `{owner}` and `{repo}`
are filled in from the current checkout, so no shell variables are needed. Shell variables do not
survive between Bash calls anyway.

## Open

```bash
gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'   # the base; do not assume main
git push --set-upstream origin HEAD
```

If the repository has a template (`.github/pull_request_template.md` or
`.github/PULL_REQUEST_TEMPLATE/`), fill it in. Otherwise the body says what changed and why, plus how
it was verified. Write it to a file and pass `--body-file`, which avoids quoting trouble:

```bash
gh pr create --base <default-branch> --title "<type>(<KEY>): <description>" --body-file <path>
```

Take the title shape from `issue-tracker-core:branch-and-title-conventions` when it is installed:
`<type>(<KEY>): <description>`, with the key taken from a `<prefix>/<KEY>-<summary>` branch. With no
key, write `<type>(<component>): <description>` or `<type>: <description>` per
`dev-standards:commit-standards`. Use a key only when the tracker or the user supplied it. For a
GitHub issue, put `Fixes #<n>` in the body so the merge closes it. Add `--draft` when the work is
incomplete; `gh pr ready` flips it later.

## Read state

```bash
gh pr view --json number,state,isDraft,mergeable,mergeStateStatus,reviewDecision,headRefOid,url
gh pr checks --json name,bucket,link --jq '.[] | select(.bucket != "pass" and .bucket != "skipping")'
```

`mergeable` answers "does it conflict". `mergeStateStatus` answers "would the merge button be green"
(`CLEAN`, `BLOCKED`, `BEHIND`, `DIRTY`, `UNSTABLE`). A PR can be `MERGEABLE` and `BLOCKED` at once.
Filter checks on `bucket` (`pass`, `fail`, `pending`, `skipping`, `cancel`) rather than `state`: raw
states include `SKIPPED`, `NEUTRAL`, `ERROR` and `TIMED_OUT`, and filtering on `SUCCESS`/`FAILURE`
gets both directions wrong.

## Wait on CI

Use gh's blocking watcher rather than a sleep loop. Run it with the Bash tool's
`run_in_background: true`: a build usually outlasts the tool's timeout, and a backgrounded command
notifies you when it exits.

```bash
gh pr checks --watch --fail-fast
```

It refreshes every 10 seconds (`--interval <s>` changes that) and exits non-zero once a check fails.
Add `--required` to wait only on the checks branch protection requires. Without `--watch`, exit code
8 means checks are still pending. When a check fails, read the failure before changing anything:

```bash
gh pr checks --json name,bucket,link --jq '.[] | select(.bucket == "fail")'
gh run view <run-id> --log-failed
```

Reproduce the failure locally before pushing a guess, because each CI attempt costs a push. Re-run
(`gh run rerun <run-id> --failed`) only when you have a reason to think it was flaky, and state that
reason. Re-running without one is how a real failure gets merged.

## Address review feedback

Inline comments come from a different endpoint than `gh pr view`:

```bash
gh api "repos/{owner}/{repo}/pulls/<n>/comments" --paginate \
  --jq '.[] | {id, path, line: (.line // .original_line), user: .user.login, body}'
```

`line` is null on a comment whose code has since changed; `original_line` still places it. Reply
in the comment's own thread, so the answer stays attached to the line:

```bash
gh api --method POST "repos/{owner}/{repo}/pulls/<n>/comments/<comment-id>/replies" \
  -f body='Fixed in <sha>: <one line on what changed>.'
```

REST cannot resolve a thread. GraphQL can. List the threads, then resolve the ones you addressed:

```bash
gh api graphql -F owner='{owner}' -F name='{repo}' -F n=<n> -f query='
  query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){
    reviewThreads(first:100){nodes{id isResolved comments(first:1){nodes{databaseId path body}}}}}}}'
gh api graphql -f id=<thread-id> -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}'
```

If you disagree with a comment, reply with your reason and leave the thread open for the reviewer.
Leave code you believe is correct as it is. A push alone does not re-request review; run
`gh pr edit <n> --add-reviewer <login>`.

## Update the branch

```bash
gh pr update-branch <n> --rebase
```

Without `--rebase`, GitHub merges the base into the branch. With it, the branch is rewritten on the
server, so bring your local copy back in line with `git pull --rebase` before committing again.
`dev-guardrails:session-sync` relies on this command and flag.

## Merge

Merging is outward-facing and hard to undo. Show the user the state below and get an explicit yes
first.

```bash
gh repo view --json mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed
gh pr view <n> --json reviewDecision,mergeStateStatus,headRefOid
```

Merge only when `reviewDecision` is `APPROVED` (or the repository requires no review) and
`mergeStateStatus` is `CLEAN`. Choose a strategy the repository allows: GitHub rejects a disallowed
one with an error that looks like a permissions problem. Pin the head you checked, so a push that
lands between the check and the merge makes the merge fail instead of shipping unreviewed code:

```bash
gh pr merge <n> --squash --delete-branch --match-head-commit <headRefOid>
```

Pass `--auto` in place of an immediate merge only when the PR is approved and you have read which
checks are required: auto-merge waits only for what branch protection requires. When the base
branch requires a merge queue, no strategy flag is needed and `gh pr merge` adds the PR to the queue.
Use `--admin`, which bypasses protection and the queue, only when the user explicitly asks for a
bypass.

## Verify

```bash
gh pr view <n> --json state,mergedAt,mergeCommit --jq '{state, mergedAt, sha: .mergeCommit.oid}'
```

`state` should be `MERGED` (or the PR should show as queued). A command that exits 0 is not proof
that the PR landed.

## Without gh

On the web, or anywhere without a shell, use the GitHub MCP server if it is connected:

| Step | MCP tool |
| --- | --- |
| Open | `create_pull_request` |
| Read state and checks | `pull_request_read` |
| Reply to or resolve a thread | `add_reply_to_pull_request_comment`, `resolve_review_thread` |
| Update the branch | `update_pull_request_branch` (check whether it offers rebase; the REST form merges) |
| Merge | `merge_pull_request` or `enable_pr_auto_merge`, after the same user confirmation |
| Failing job logs | `get_job_logs` |

With neither a shell nor the MCP server, give the user the commands above to run themselves.
