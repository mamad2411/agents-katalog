---
name: issue-lifecycle-github
description: "Runs issue-tracker-core's pre-work gate and comment trail on GitHub with gh or GitHub MCP tools: fetch, create, assign, move, comment on, close, reopen. Use when working a GitHub issue. Not for labels, parents or sweeps (use backlog-hygiene-github); not for PRs (use github-workflow:pr-lifecycle)."
allowed-tools: Bash(gh auth status), Bash(gh issue view *), Bash(gh issue list *), Bash(git branch --show-current), Bash(printenv CLAUDE_TICKET_PATTERN)
license: MIT
---

# Issue Lifecycle on GitHub

The rules live in `issue-tracker-core`: `pre-work-gate` (the four properties, the scope check and
the summary line) and `tracker-discipline` (the seven states, dedupe, parenting and the comment
templates). This skill supplies the GitHub calls that carry them out. Reads are pre-approved;
every write (edit, comment, create, close) asks first.

## Access

Use the first that works:

1. **gh.** `gh auth status` must report an account for the repository's host. Outside a checkout,
   add `--repo <owner>/<repo>` to every `gh issue` command; in `gh api` paths, `{owner}` and
   `{repo}` are filled in from the checkout.
2. **GitHub MCP tools** (the GitHub MCP server or the claude.ai GitHub connector), when `gh` is
   missing or unauthenticated, as on the web. The mapping is under [Without gh](#without-gh).
3. **Neither:** use the core's "Work from a pasted issue" path, and print each `gh` command below
   for the user to run.

Shell variables do not survive between Bash calls. Write issue numbers literally into each
command, or chain dependent steps inside one call.

Newer `gh` releases add `--parent`, `--type` and `--blocked-by`. If `gh issue edit --help` does
not list `--parent`, use the fallbacks noted below. Versions are in
[references/gh-versions.md](references/gh-versions.md).

## Settings

Read the `## Issue tracker` section of the project's `CLAUDE.md`, as the core describes. The
GitHub values (ticket pattern `GH-[0-9]+` or `[0-9]+`, and a status mapping on `status:` labels)
are filled in in [references/issue-tracker-section.md](references/issue-tracker-section.md). The
examples below assume that recommended mapping.

## Step 1: Find the issue number

Run `git branch --show-current` and match the Ticket pattern. With `GH-[0-9]+`, the branch
`fix/GH-123-retry-worker` names issue `#123`. No match: follow the core's search order (the
user's message, then this session), then ask.

## Step 2: Fetch, then print the summary

```bash
gh issue view 123 --json number,title,state,stateReason,assignees,labels,milestone,issueType,parent,url,body
gh issue view 123 --comments
```

The comment thread is part of the scope check; an earlier scope negotiation lives there. If `gh`
rejects `issueType` or `parent` as unknown fields (an older release), drop them and read the parent
with `gh api repos/{owner}/{repo}/issues/123 --jq .parent_issue_url` (null means no parent).

A non-zero exit means the issue does not exist or this is the wrong repository. Ask which issue the
work belongs to rather than creating one to make the gate pass.

Map the labels (or board status) to a core state through the Status mapping and print the core's
summary line, for example `State: in-progress (status:in-progress)`.

## Step 3: Repair gate failures

| Property | Repair |
|---|---|
| Assigned | `gh issue edit 123 --add-assignee @me` |
| Workable | `gh issue edit 123 --remove-label "status:ready" --add-label "status:in-progress"`, one command so the issue never carries two status labels or none. When a board carries state, use `projects-v2`. |
| Parented | `gh issue edit 123 --parent 40`, or `--milestone "<title>"` when the Parent mechanism is milestone. Finding a candidate parent: `backlog-hygiene-github`. |

Then post the start comment (Step 6).

## Step 4: Create an issue

Run the core's dedupe check first. Search on the symptom, not your intended title:

```bash
gh issue list --state open --search "timeout sign-in" --json number,title,labels --limit 20
gh issue list --state closed --search "timeout sign-in reason:completed" --json number,title --limit 20
```

The second search is for regressions. Record `NEW`, `DUPLICATE → #<n>` or `UNCHECKED`. On a
duplicate, comment on the existing issue instead of creating.

For `NEW`, set assignee, state and parent in the create call itself:

```bash
gh issue create --title "Retry transient upstream failures in the ingestion worker" \
  --assignee @me --label "status:in-progress" --type Bug --parent 40 --body-file - <<'BODY'
## Problem
The ingestion worker aborts the batch on the first transient upstream 503.

## Acceptance
- Transient 5xx responses are retried with bounded backoff.
- A permanently failing record is quarantined, not retried forever.
BODY
```

- `--type` only when the organization defines issue types; otherwise add a `type:` label
  (`backlog-hygiene-github` explains which).
- `--milestone "<title>"` instead of, or as well as, `--parent` when the Parent mechanism says so.
- Without `--parent` support: create without it, read the number from the URL `gh` prints, and
  attach it in the next call per `backlog-hygiene-github`.

Read it back: `gh issue view <n> --json number,assignees,labels,issueType,parent,milestone`.

## Step 5: Branch and pull request

The branch and title shape belong to `issue-tracker-core:branch-and-title-conventions`, and
opening the pull request to `github-workflow:pr-lifecycle`. The one GitHub rule this skill adds:
the pull request body carries `Fixes #123` (the `#` form, never `Fixes GH-123`) so the merge closes
the issue. That works only when the pull request targets the default branch. Details are in
[references/issue-tracker-section.md](references/issue-tracker-section.md).

## Step 6: Comment trail

Use the core's start, handoff and finish templates. `--body-file -` reads the comment from stdin,
so multi-line text needs no shell quoting:

```bash
gh issue comment 123 --body-file - <<'BODY'
**Start**
Branch: `fix/GH-123-retry-worker`. Plan: wrap the upstream client in a bounded retry.
Differs from the description: the worker does not yet tell transient from permanent failures.
BODY
```

**Blocked or paused.** The core sends blocked work back to `ready` or `parked`. On GitHub, record
the blocker as a native dependency where available, together with the state move:

```bash
gh issue edit 123 --remove-label "status:in-progress" --add-label "status:ready" --add-blocked-by 118
```

Then post the handoff comment naming the blocker. Without `--add-blocked-by`, the comment alone
carries the blocker. A repo that wants a filterable facet adds the `blocked` label described in
`backlog-hygiene-github`, alongside the status label.

`gh issue comment` prints only the comment URL, so read it back:
`gh issue view 123 --json comments --jq '.comments[-1] | {author: .author.login, createdAt}'`.

## Step 7: Close and reopen

Prefer the merge closing the issue through `Fixes #123`. Close by hand only when no code change
is behind it, and pass `--reason` every time, because the reason is the only place GitHub separates
finished from abandoned:

| Core state | Command |
|---|---|
| `done` | `gh issue close 123 --reason completed --comment "Shipped in #131."` |
| `declined` | `gh issue close 123 --reason "not planned" --comment "<why>"` |
| `declined` (duplicate) | `gh issue close 123 --duplicate-of 77` |
| `parked` | Stays open: swap to `status:parked` and comment the revisit condition. |

Reading back, `stateReason` maps `COMPLETED` to `done`, and `NOT_PLANNED` or `DUPLICATE` to
`declined`. A closed issue's state wins over any `status:` label left on it; there is no
`status:done` label to maintain.

Reopening retracts the close, so replace whatever `status:` label the issue still carries:

```bash
gh issue reopen 123 --comment "Reopening: the retry bound applies per call, not per batch."
gh issue edit 123 --remove-label "status:in-review" --add-label "status:in-progress"
```

A reopened issue can get a second branch against the same key (`fix/GH-123-bound-per-batch`).

## Without gh

GitHub MCP tool names (the prefix depends on how the server is registered):

| Step | Tool and arguments |
|---|---|
| Fetch, comments, parent | `issue_read` with `method` `get`, `get_comments` or `get_parent` |
| Dedupe search | `search_issues` |
| Create with parent | `issue_write` `method: create` with `parent_issue_number`, `assignees`, `labels`, `type` |
| Assign, relabel, set type | `issue_write` `method: update`. `labels` and `assignees` replace the whole set, so read the current values and send the full list. |
| Comment | `add_issue_comment` |
| Close | `issue_write` `method: update`, `state: closed`, `state_reason` `completed`, `not_planned` or `duplicate` (with `duplicate_of`) |
| Issue types available | `list_issue_types` |

The MCP server has no dependency tool, so record a blocker in the handoff comment. With no tool
at all, print the `gh` commands and say nothing is recorded until the user confirms.

## Examples

<example>
Branch `fix/GH-123-retry-worker`; the user asks to add retry logic to the ingestion worker.
`gh issue view 123` returns an open issue assigned to the user, labelled `status:ready`, parent #40.
Print the summary with `Gate: PASS` after moving it: `gh issue edit 123 --remove-label
"status:ready" --add-label "status:in-progress"`, then post the start comment.
</example>

<example>
Asked to file "export times out for large orgs". `gh issue list --state open --search "export
timeout"` finds #77 "CSV export slow above 10k rows". Report `DUPLICATE → #77`, and comment on #77
with the new symptom. Create nothing unless the user says it is a different problem.
</example>

<example>
Mid-work on #123, the fix turns out to need the schema change tracked in #118.
Run `gh issue edit 123 --remove-label "status:in-progress" --add-label "status:ready"
--add-blocked-by 118`, then post the handoff comment with "Blocker: #118 (schema migration), owned
by the data team". The issue now claims `ready` with a recorded blocker, not `in-progress`.
</example>

## Common failures

| Symptom | Cause | Repair |
|---|---|---|
| `Could not resolve to an Issue` | Wrong repository context, or the number is in another repo. | Add `--repo <owner>/<repo>`. |
| Gate finds no key on a correctly named branch | Ticket pattern still the core default, which never matches a GitHub key. | Set the row per `references/issue-tracker-section.md`. |
| Merged pull request did not close the issue | `Fixes GH-123` instead of `Fixes #123`, or the target was not the default branch. | Close by hand with `--reason completed`. |
| `unknown flag: --parent` or unknown JSON field `parent` | `gh` older than the sub-issue flags. | Use the REST fallback in `backlog-hygiene-github`. |

## Verify

After each write, read the issue back with `gh issue view 123 --json assignees,labels,state,stateReason,parent`
(or `issue_read`) and check it against the core's Verify list: the state maps to the core state you
intended, exactly one `status:` label on an open issue, the parent exists and is open, and the
comment is on the issue. From pasted data, confirm the user has applied the printed commands.
