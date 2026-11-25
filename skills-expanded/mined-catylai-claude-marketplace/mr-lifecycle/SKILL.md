---
name: mr-lifecycle
description: "Takes a GitLab merge request from open to merged with glab, following project policy. Use when opening an MR, fixing its pipeline, answering discussions, rebasing or merging. Not for posting a code review (use review-transport); not for pipeline YAML (use gitlab-ci-authoring)."
when_to_use: "open a merge request, why is my pipeline failing, wait for CI on GitLab, address MR comments, resolve MR discussions, mark MR ready, rebase the MR, merge this MR"
allowed-tools: Bash(glab auth status), Bash(glab repo view *), Bash(glab mr view *), Bash(glab ci status *), Bash(glab ci get *), Bash(glab ci trace *), Bash(git status *), Bash(git branch --show-current), Read, Grep, Glob
license: MIT
---

# mr-lifecycle

A merge request moves through a few states: unopened, draft, pipeline red, discussions open,
mergeable, merged. Each section below is the next command for one state. Merge method, approval
rules and protected branches belong to the project, so read them rather than assuming.

Run `glab auth status` first; an auth failure otherwise surfaces as a confusing 404. Outside a
checkout, add `--repo <group>/<project>` to every `glab mr` and `glab ci` call. `glab api` has no
`--repo`: in its paths, `:id` is the checkout's project, and another project is written URL-encoded
(`projects/<group>%2F<project>/...`). Write the MR's IID (the `!123` number, not the global id)
literally into each command, because shell variables do not survive between Bash calls.

## Open

```bash
glab repo view --output json --jq '.default_branch'   # the target; do not assume main
git push --set-upstream origin HEAD
```

If the project has a template in `.gitlab/merge_request_templates/`, pass `--template <name>`.
Otherwise the description says what changed and why, plus how it was verified. Write it to a file,
which avoids quoting trouble:

```bash
glab mr create --target-branch <default-branch> --title "<type>(<KEY>): <description>" \
  --description-file <path> --remove-source-branch --yes
```

`--yes` skips the confirmation prompt, which otherwise waits forever without a terminal. Take the
title shape from `issue-tracker-core:branch-and-title-conventions` when it is installed:
`<type>(<KEY>): <description>`, with the key taken from a `<prefix>/<KEY>-<summary>` branch. With no
key, write `<type>(<component>): <description>` or `<type>: <description>` per
`dev-standards:commit-standards`. Use a key only when the tracker or the user supplied it. Add
`--draft` when the work is incomplete; `glab mr update <iid> --ready` flips it later (and `--draft`
flips it back).

## Read state

```bash
glab mr view <iid> --output json --jq '{state, draft, detailed_merge_status, has_conflicts, sha, web_url}'
glab api "projects/:id/merge_requests/<iid>/approvals" --jq '{approved, approvals_left, user_can_approve}'
```

`detailed_merge_status` answers "why is the merge button not green" in one string: `mergeable`,
`not_approved`, `ci_still_running`, `ci_must_pass`, `discussions_not_resolved`, `conflict`,
`need_rebase`, `draft_status`, among others. `sha` is the head commit, which the merge pins below.

## Wait on the pipeline

Use glab's blocking form rather than a sleep loop, and run it with the Bash tool's
`run_in_background: true`, since a pipeline usually outlasts the tool's timeout:

```bash
glab ci status --wait
```

When it ends red, read the failing job before changing anything:

```bash
glab ci get --merge-request <iid> --status failed --with-job-details
glab ci trace <job-id>
```

Pass `glab ci trace` a job id; without one it opens an interactive picker that hangs without a
terminal. Reproduce the failure locally before pushing a guess, because each attempt costs a
pipeline. Retry (`glab ci retry <job-id>`) only when you have a reason to think the job was flaky,
and state that reason. A `manual` job is waiting, not failing; `glab ci trigger <job-id>` starts it.
A pipeline that never appeared is a `rules:` or YAML problem: see `gitlab-ci-authoring`.

## Address review feedback

```bash
glab mr view <iid> --unresolved
glab api "projects/:id/merge_requests/<iid>/discussions" --paginate \
  | jq -s 'flatten(1) | map(select(.notes[0].resolvable and (.notes[0].resolved | not))
      | {id, path: .notes[0].position.new_path, line: .notes[0].position.new_line,
         author: .notes[0].author.username, body: .notes[0].body})'
```

Reply in the discussion's own thread, so the answer stays attached to the line, then resolve the
ones you addressed once the fix is pushed:

```bash
glab mr note create <iid> --reply <discussion-id> -m 'Fixed in <sha>: <one line on what changed>.'
glab mr note resolve <iid> <discussion-id>
```

`glab mr note resolve` is marked experimental. If it is missing or fails, the API does the same:
`glab api --method PUT "projects/:id/merge_requests/<iid>/discussions/<discussion-id>" -f resolved=true`.

If you disagree with a note, reply with your reason and leave the discussion open for its author.
Leave code you believe is correct as it is. A push alone does not re-request review:
`glab mr update <iid> --reviewer +<username>` adds one (without `+`, the list is replaced).

## Rebase

```bash
glab mr rebase <iid>
```

The rebase runs on the server. glab waits until GitLab reports it finished and exits non-zero with
GitLab's message when it fails, a conflict included. The branch was rewritten remotely, so bring
your local copy in line with `git pull --rebase` before committing again.
`dev-guardrails:session-sync` relies on this behaviour.

## Merge

Merging is outward-facing and hard to undo. Show the user the state below and get an explicit yes
first.

```bash
glab repo view --output json --jq '{merge_method, squash_option, only_allow_merge_if_pipeline_succeeds, only_allow_merge_if_all_discussions_are_resolved}'
glab mr view <iid> --output json --jq '{detailed_merge_status, sha}'
```

Merge only when `detailed_merge_status` is `mergeable`. `merge_method` is `merge`, `rebase_merge`
or `ff`; the last two reject a source branch that is behind, with an error that reads like a
permissions problem, so rebase first. Pass `--squash` only when `squash_option` allows it. Pin the
`sha` you checked, so a push between the check and the merge makes the merge fail instead of
shipping unreviewed code:

```bash
glab mr merge <iid> --sha <sha> --remove-source-branch --auto-merge=false --yes
```

`glab mr merge` turns on auto-merge by default, so without `--auto-merge=false` a running pipeline
makes the command return 0 with nothing merged yet. Leave auto-merge on only when the user asks for
it and the MR is already approved.

## Verify

```bash
glab mr view <iid> --output json --jq '{state, merged_at, merge_commit_sha, squash_commit_sha}'
```

`state` should be `merged`. `opened` with `detailed_merge_status: "ci_still_running"` means
auto-merge is armed, not that the merge failed. A command that exits 0 is not proof that the MR
landed.

## Without glab

On the web, or anywhere without a shell, use a GitLab MCP server if one is connected, following the
same steps and the same confirmation before merging. Otherwise work from what the user pastes (the
MR page, a job log) and give them the commands above to run.
