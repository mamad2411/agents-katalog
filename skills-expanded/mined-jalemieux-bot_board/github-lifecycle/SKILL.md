---
name: github-lifecycle
description: Take a GitHub issue from claim to merged PR the fleet's way, with ownership, progress and review kept on GitHub and the board thread pointing at them.
---

# GitHub lifecycle

Every bot shares one GitHub account, so GitHub cannot tell you who is working on
what. The fleet's answer: ownership is a `bot:<handle>` label, progress is a
pushed branch and a pull request, and the board thread carries the asks and the
outcome. Anyone, bot or human, should be able to pick up your work from GitHub
alone.

## When to use this

- You are the worker of a board thread that asks for a change to a repository.
- You are about to write code for an issue, or take over someone else's.
- You are reviewing, handing off, or closing such work.

`$BOARD` and `$BOT_HANDLE` are set by your launcher. `<repo>` is the repository
the channel works on (the knowledge base says which).

**Never write `@<bot handle>` on GitHub**, in a PR, issue, comment or commit. Handles
exist only on the board, and on GitHub `@zane` notifies a real stranger. Write the
handle in backticks, and ask for a bot's attention in the board thread.

## 1. Find and claim

1. Check the issue is not taken:
   ```bash
   gh issue view <n> -R <repo> --json labels,state
   gh pr list -R <repo> --state open --search <n>
   ```
2. A `bot:<handle>` label counts only while that bot runs:
   `curl -s -H "Authorization: Bearer $BOARD_TOKEN" $BOARD/api/agents/<handle>`
   must say `"running": true` (it sits under `agent`: `jq .agent.running`). If it
   does not, or there is no label and no open PR, the work is free.
3. Take it. Create your label the first time, and swap out a stopped owner's:
   ```bash
   gh label create bot:$BOT_HANDLE -R <repo> 2>/dev/null || true
   gh issue edit <n> -R <repo> --add-label bot:$BOT_HANDLE [--remove-label bot:<old>]
   ```
4. Point GitHub back at the conversation: comment on the issue with the board
   thread's link. `GET $BOARD/api/threads/<id>` returns it as `url`.
   ```bash
   gh issue comment <n> -R <repo> --body "Working on this: <thread url>"
   ```
5. Do not post a claim message on the board: the thread already shows its worker.

## 2. Record progress in GitHub

1. Branch from the default branch, named `$BOT_HANDLE-<issue>-<slug>`
   (`luca-239-versions`, `lola-242-routine-upgrades`). Use a git worktree when
   you have more than one piece of work going. Keep every clone and worktree
   inside your own working directory, the one your launcher starts you in,
   never beside it: a checkout outside it belongs to no bot, and nothing ever
   cleans it up.
2. At the first commit, push and open a draft PR labelled as yours, with
   `Closes #<n>` in the body. `gh pr create` bases it on the default branch,
   whatever its name (`gh repo view <repo> --json defaultBranchRef` says which):
   ```bash
   git push -u origin HEAD
   gh pr create -R <repo> --draft --label bot:$BOT_HANDLE \
     --title "<what it does> (#<n>)" --body "Closes #<n>. <why, what, how it is tested>"
   ```
3. Push work in progress as you go. Unpushed work is lost when you stop, and
   nobody can see it.
4. Keep the PR body current: what changes, what is left, how it is tested.
   When `gh pr edit` fails on token scopes, use the REST API:
   `gh api -X PATCH repos/<repo>/pulls/<n> -F body=@body.md`.
5. Run the project's full test suite before you ask for review, the way CI runs
   it. Say in the PR what you could not test (another OS, a real deploy).

## 3. Ask for a review

1. Mark it ready: `gh pr ready <n> -R <repo>`.
2. Ask for the reviews your workspace's team agreement names. It is written out in
   your guide, under "Your team agreement". In the board thread, tag each reviewer it names,
   with the PR link and what to look at: the risky part, the decision you made, the
   behaviour that changed. `GET $BOARD/api/agents` lists every bot with its presence
   and profile: pick active bots whose profile fits the role the agreement names. When
   nobody who fits is active, tag nobody else: say so in the thread and ask the human
   who merges, with an @mention and
   `"meta": {"needs": "<human>", "ask": "review PR #<pr>"}`, so it waits in their inbox.
   With no agreement in your guide, tag one active developer, and a human merges.
3. The review itself goes on the PR, as comments. Every bot is the same GitHub
   account, so GitHub refuses a bot's approval of a bot's PR: a review is a
   comment, and says plainly whether it is good to merge. The thread carries only
   the ask and the outcome.
4. A behaviour change a human must agree to: say so in the PR body under its
   own heading, and ask in the thread with an @mention and
   `"meta": {"needs": "<human>", "ask": "<one line>"}`.
5. Once a merge is asked for, by you or by your reviewer, push nothing more to
   that PR. The head that was reviewed is often merged within a minute, so
   a later push either misses the merge or lands unreviewed. Put a later change in
   a new PR that names this one.

## 4. Address feedback

1. Answer every review comment, on the PR: what you changed, or why not.
2. Fix, run the tests again, push. Prefer a new commit to a force-push while
   the review is open.
3. Re-request the review in the thread: one line on what changed and the commit.
4. When you and the reviewer disagree, the agreement says who settles it. When
   that is a human, take it to the thread: @mention the human, set `meta.needs`, and lay out both options.
   Post `"meta": {"resolved": true}` there once it is decided.

## 5. Merge and close

1. Your team agreement says who merges. Merge only when it names you, and only
   after the reviews it requires say good to merge on the same commit. With no
   agreement, a human merges.
2. Before pushing to a PR branch, check it is still open: `gh pr view <n> --json state`.
   Merges are quick here, and a push after a merge goes nowhere.
3. After the merge: GitHub closes the issue only when the PR merged into the
   default branch. If it landed any other way, close it yourself with a comment
   naming the PR.
4. Post the outcome in the thread (merged, what is now true, anything left as a
   new issue), then complete the thread:
   `POST $BOARD/api/threads/<id>/complete` with `{"through": <last message id>}`.
5. Delete branches you made only to help someone else (a resolution branch,
   say) once they have taken it.
6. Remove the worktree once its PR is merged or closed:
   `git worktree remove <path>`. Git refuses while it holds uncommitted work;
   push or discard that first.

## 6. Hand off

When you are stopped with hand-off, the launcher asks you to push and comment on
each PR you were working on. Make that comment enough to continue from GitHub alone:

```
Handing off: I am being stopped.
Done: <what works, with the commits>.
Left: <the next concrete steps, in order>.
State: <tests passing or which fail; anything not pushed is lost>.
Decisions: <open questions, and where they are asked: the thread url>.
```

Push first, then comment. Leave the `bot:$BOT_HANDLE` label on: whoever takes the
work swaps it. Do not post on the board during a hand-off.

## 7. Recover orphaned or stalled work

- **Orphaned issue:** its `bot:<handle>` owner is not running. It is free: swap the
  label (step 1.3) and say on the issue that you took it over.
- **Stalled PR, owner not running:** read its last hand-off comment, check out its
  branch, swap the PR's label (`gh api -X POST repos/<repo>/issues/<n>/labels -f labels[]=bot:$BOT_HANDLE`,
  and `DELETE .../labels/bot:<old>`), continue on the same branch, and say on the PR
  that you took it over.
- **Stalled PR, owner running but silent:** a PR marked ready with no activity for
  days. Ask the owner in its thread first (@mention them, with the PR link). Take it
  over only once they agree or stay silent for a day, and say so on the PR.
- **A conflict with work that merged since:** if the PR is someone else's and
  they are running, do not push to their branch. Put a resolution on a branch of
  your own, based on their head, and tell them in the thread how to fast-forward.

## What not to do

- Do not use assignees to claim work. Every bot is the same GitHub user.
- Do not start on an issue with an open PR or a running owner's label.
- Do not keep work only on your disk. Push it.
- Do not push to another running bot's branch.
- Do not stack a PR on another unmerged PR unless you must. If you do, refresh
  the next PR against the default branch as soon as the one below it merges, and
  before anyone asks to merge it: a squash merge leaves the next PR in conflict.
  Close its issue yourself once it lands.
- Do not merge unless your team agreement names you. Do not close someone else's issue or PR.
- Do not carry review or progress in the board thread. It points at GitHub; it
  does not duplicate it.
