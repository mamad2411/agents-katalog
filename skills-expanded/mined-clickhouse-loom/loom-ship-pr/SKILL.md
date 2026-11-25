---
name: loom-ship-pr
description: Opens and lands a Loom PR — signed-off commits, a public body from the template, a fresh review at every push alongside CI, a CI gate on gh's JSON, and a squash merge on green. Use when asked to open, update, land or merge a PR. Comments on it — loom-address-review; a red check — loom-investigate-ci.
argument-hint: "[pr-number]"
metadata:
  internal: true
---

# Shipping a Loom pull request

## 1. Commit

```bash
git add <paths>              # name them; never `git add -A` over untracked scratch files
git commit -s -m "<what is now true>" -m "<why>"
```

The subject says what is now true, as `git log` reads it. Sign-off (`-s`) is required (DCO).

## 2. Body

Fill `.github/PULL_REQUEST_TEMPLATE.md` in order: linked issues, changelog category, changelog entry, Why, Scope and risk, Compatibility/rollout/rollback, Tests, AI assistance, checklist. Write it to a file and pass `--body-file`. Where `gh pr edit` fails on the retired Projects (classic) API (older `gh` releases), update the body with `gh api -X PATCH repos/ClickHouse/loom/pulls/<n> -F body=@<body file>`.

The body is public. It carries:

- the why, the design for a material change, alternatives and their cost;
- every op or field added, changed or removed, and operator steps (or "none");
- what you ran and what it showed, with the command that reproduces a measurement.

It never carries other products' names or comparative framing, host names, internal namespaces or repository names of a deployment, people, wall-clock times, production row counts or incident timelines. Evidence from a live deployment goes to the conversation with the requester, not into the PR.

Write it in the `loom-writing` voice and run `python3 .claude/skills/loom-writing/scripts/check_prose.py <body file>` before every `gh pr create` or `gh pr edit`. Link the issue it fixes with `Closes: <full issue URL>`.

One concern per PR, and the title matches every part of it: a feature, an example and a release-process change are three PRs. A large task is a few PRs grouped by concern, not one per file: each needs its own CI run and review.

## 3. Push and open

```bash
git push -u origin HEAD
gh pr create --base main --title "<subject>" --body-file /path/to/body.md
```

CI runs on PRs into `main` or a `release/X.Y` line (and pushes to them). Retarget a stacked PR (`gh pr edit <n> --base main`) before pushing its next real change or required rebase. A base edit alone does not trigger the default `pull_request` events: `opened`, `synchronize` or `reopened`. A PR with a merge conflict gets none, silently. After every push:

```bash
gh pr view <n> --json mergeable --jq .mergeable     # CONFLICTING: rebase on origin/main now, or CI never starts
```

## 4. Review at the push

Start the review the moment the push lands; CI runs in parallel. In Claude Code, launch a fresh `loom-reviewer` subagent in the background with the PR number and head sha; elsewhere run the `loom-review` skill in a new session. A reviewer that saw an earlier head carries its conclusions forward, so every head gets a new one.

Work the findings with `loom-address-review`: fix every confirmed one, nits included, or answer why not; push; review again. The loop ends when a fresh reviewer returns no findings on the head and CI is green. An "approve" that still lists nits is not the end.

## 5. Read CI

Right after a push the new head has no checks for a few seconds (the previous head's runs are cancelled), and `gh pr checks --watch` returns at once on an empty list. Wait for the head's checks to appear first, for at most five minutes; none by then means a conflict or a workflow that did not start (`loom-investigate-ci`):

```bash
for _ in $(seq 20); do [ "$(gh pr view <n> --json headRefOid,statusCheckRollup --jq "(.headRefOid == \"$(git rev-parse HEAD)\") and (.statusCheckRollup | length > 0)")" = true ] && break; sleep 15; done
gh pr checks <n> --watch --fail-fast      # a CI round trip outlasts a foreground call: run it in the background
gh pr view <n> --json statusCheckRollup --jq '.statusCheckRollup[] | "\((.conclusion // "") as $c | if $c == "" then (.state // .status) else $c end)\t\(.name // .context)"'
gh pr view <n> --json statusCheckRollup --jq '.statusCheckRollup | length > 0 and all(.[];
  (.status // "COMPLETED") == "COMPLETED" and ((.conclusion // .state) | IN("SUCCESS", "SKIPPED", "NEUTRAL")))'   # true = green
```

Gate on `jq`'s `all(...)` (an empty rollup is not green; a commit-status entry has `state` where a check run has `status` and `conclusion`) and print the table; do not gate on `grep -v` over text output, whose exit code inverts on some grep implementations. A red job: `loom-investigate-ci`.

## 6. Merge

Only when the gate above prints `true`, the review has no open finding and the requester approved merging. Read the title and body once more first: the squash merge copies them into `main`'s history, where they cannot be edited. They describe the final diff (not the first push), and carry nothing internal.

```bash
gh pr merge <n> --squash
git push origin --delete <branch>   # the repository keeps merged branches
```

`--delete-branch` would check out and pull `main` in this linked worktree, which `main`'s shared ref forbids, and fails after the merge when `main` is checked out elsewhere.

- Squash-merge always. Never merge another author's PR for them.
- If another PR merged after your last green run and yours adds files the whole-tree gates scan (any `.py`, `.md`, test or doc), rebase on it (`git fetch origin main && git rebase origin/main && git push --force-with-lease`, which asks for approval; `--force`, `-f` and `+ref` are denied) and wait for green again: two PRs green alone can be red together.
- Two open PRs that bump the plugin to the same version: the second ships nothing. Re-bump before merging.

## 7. After the merge

Remove the private ClickHouse (`docker rm -f <your container>`), then the worktree and its branch. If this session is inside the worktree (entered with `EnterWorktree` or `--worktree`, or resumed into it), leave with `ExitWorktree` (`action: "remove"`, and `discard_changes: true`, since a squash merge leaves the branch's commits off `main`): while inside, commands aimed at the primary checkout are refused. Then, from the primary checkout: `git worktree remove <worktree>` if it is still there, and `git branch -D <branch>`. Deploying is a separate, explicit step (`loom-deploy`).
