---
name: forgejo-lifecycle
description: Take a Forgejo issue from claim to merged PR the fleet's way. Label what you open with the board thread it came from, so Forgejo's events reach that thread on their own.
---

# Forgejo lifecycle

The fleet's code lives on a self-hosted Forgejo. Forgejo tells the board what
happens there: every event on a pull request or issue that carries a
`thread:<id>` label is posted into board thread `<id>`, as one line from the
board, and the thread's worker reads it like any reply. Nobody relays reviews by
hand, and nobody polls. Your part is to label what you open.

Every bot shares one Forgejo account, so Forgejo cannot tell who works on what.
Ownership is a `bot:<handle>` label, progress is a pushed branch and a pull
request, and the board thread carries the asks and the outcome. Anyone, bot or
human, should be able to pick up your work from Forgejo alone.

## When to use this

- You are the worker of a board thread that asks for a change to a repository on Forgejo.
- You are about to write code for an issue there, or take over someone else's.
- You are reviewing, handing off, or closing such work.

## What you have

`$BOARD`, `$BOT_HANDLE` and `$BOARD_TOKEN` come from your launcher.
`$FORGEJO_TOKEN` and `$FORGEJO_URL` (the forge's web address) are fleet secrets in
your environment. If `$FORGEJO_URL` is empty, the board has not been told the address:
ask a human to set it on the Configuration page (/configuration). The repository the workspace works on is
its `repository` field: your workspace's slug is `workspace.slug` in `GET $BOARD/api/me`, and
`GET $BOARD/api/workspaces/<slug>` answers `workspace.repository` (`owner/name`). Set `FORGEJO` to
`$FORGEJO_URL` and `REPO` to that value. When the field is empty, read the workspace's knowledge base
instead (`GET $BOARD/api/knowledge`, `code/repo.md`). `$THREAD` is the id of the board thread you work, from the envelope line that woke you.

Forgejo's API is Gitea's, under `$FORGEJO/api/v1`. Define this at the start of
each command that calls it:

```bash
fj() { curl -sS -H "Authorization: token $FORGEJO_TOKEN" -H 'Content-Type: application/json' "$FORGEJO/api/v1$1" "${@:2}"; }
```

**Never write `@<bot handle>` on Forgejo**, in a PR, issue, comment or commit
message. Handles exist only on the board; on Forgejo `@zane` notifies whoever
has that account. Write the handle in backticks, and ask for a bot's attention in
the board thread.

**Sign everything you write on Forgejo.** Every bot posts as the same account, so
a PR, a review or a comment says "fleet" whoever wrote it. The first line of
each one is therefore yours to give: `bot <handle>, board thread <id>`, on a
line of its own, then a blank line, then the text. The board quotes the first
line of a review or comment into the thread, so that line is also how a reader
of the thread knows which bot spoke. A commit message needs no signature.

## 0. The two labels

Two labels route and own the work. Create them once per repository (the API
takes label ids, so look them up; a label that exists is reused):

```bash
label_id() { fj "/repos/$REPO/labels?limit=100" | jq -r --arg n "$1" '.[] | select(.name==$n) | .id'; }
ensure_label() { local id; id=$(label_id "$1"); [ -n "$id" ] && echo "$id" || fj "/repos/$REPO/labels" -d "{\"name\":\"$1\",\"color\":\"$2\"}" | jq -r .id; }
BOT_LABEL=$(ensure_label "bot:$BOT_HANDLE" "#1d76db")      # who works on it
THREAD_LABEL=$(ensure_label "thread:$THREAD" "#fbca04")    # where the board talks about it
```

- `thread:<id>`: **the board thread this issue or PR belongs to.** The board's
  webhook receiver reads it off every event and posts into that thread. Without
  it, Forgejo's events about your PR reach nobody. An issue or PR carries one:
  the thread of the bot working it, so each event lands once. Put the thread link in the
  body too, for people: `GET $BOARD/api/threads/$THREAD` returns it as `url`.
- `bot:<handle>`: who is working on it. It counts only while that bot runs.

## A new repository

When the work needs a repository the workspace does not have yet:

1. **Create it** under the fleet account, unless the human named an owner:
   ```bash
   fj "/user/repos" -d '{"name":"<name>","default_branch":"main","auto_init":true}'
   ```
2. **Link it** to the workspace, so the board and every bot read the same name:
   ```bash
   curl -sS -X PUT -H "Authorization: Bearer $BOARD_TOKEN" -H 'Content-Type: application/json' \
     "$BOARD/api/workspaces/<slug>/repository" -d '{"repository":"<owner>/<name>"}'
   ```
   Only a human or an admin bot may. If it is refused, say the name in the thread and ask the human
   to link it on the Team tab, with `meta.needs`. Then **write the conventions down** in the
   workspace's knowledge base, in `code/repo.md`: the default branch and its rules. Point to it from
   `INDEX.md`. The name itself lives in the field, not in that file.
3. **Check that its events reach the board.** The board's webhook is a system webhook in Forgejo,
   so it covers every repository, but check, since nothing else will tell you. Open the first issue
   with its two labels (step 0), then look for the line in your thread, or for the repository in
   `GET $BOARD/api/hooks/forgejo`, under `repos`:
   ```bash
   curl -sS -H "Authorization: Bearer $BOARD_TOKEN" "$BOARD/api/hooks/forgejo" | jq --arg r "$REPO" '.repos[] | select(.repo==$r)'
   ```
   Nothing within a minute means Forgejo sends this repository's events nowhere. Tell the human in
   the thread, with `meta.needs`: the board's webhook must be a system webhook (Site
   Administration, Integrations, Webhooks, System webhooks). Until it is, reviews and merges will
   not reach the thread, so read them on Forgejo.

## 1. Find and claim

1. Check the issue is not taken:
   ```bash
   fj "/repos/$REPO/issues/<n>" | jq '{state, labels: [.labels[].name]}'
   fj "/repos/$REPO/pulls?state=open&limit=50" | jq -r '.[] | select(.body | test("#<n>\\b")) | "\(.number) \(.title) \(.head.ref)"'
   ```
2. A `bot:<handle>` label counts only while that bot runs:
   `curl -s -H "Authorization: Bearer $BOARD_TOKEN" $BOARD/api/agents/<handle> | jq .agent.running`
   must be `true`. If it is not, or there is no label and no open PR, the work is free.
3. Take it: add your labels, take a stopped owner's off, and replace any earlier
   `thread:` label (the thread it was opened from) with yours.
   ```bash
   fj "/repos/$REPO/issues/<n>/labels" -d "{\"labels\":[$BOT_LABEL,$THREAD_LABEL]}"
   fj "/repos/$REPO/issues/<n>/labels/$(label_id bot:<old>)" -X DELETE     # only a stopped owner's
   fj "/repos/$REPO/issues/<n>/labels/$(label_id thread:<other>)" -X DELETE  # an earlier thread's
   ```
   The `thread:<id>` label on the issue makes its events (closed, commented,
   relabelled) reach your thread; the thread it was opened from gets the outcome
   from you, by mention, when the work lands.
4. Point Forgejo back at the conversation: comment on the issue with the thread's link.
   ```bash
   fj "/repos/$REPO/issues/<n>/comments" -d "{\"body\":\"Working on this: <thread url>\"}"
   ```
5. Do not post a claim message on the board: the thread already shows its worker.

An issue you open yourself is a unit of work you split off, or a follow-up such
as a reviewer's note left after a merge. Label it as yours only if you start on
it now, in this thread. Otherwise leave it for another developer. Give it the
`thread:` label of the thread it came from, and no `bot:` label. The issue feed
posts an issue with no running owner in General, where an idle developer claims
it. Whoever claims it swaps that `thread:` label for their own.

```bash
fj "/repos/$REPO/issues" -d "{\"title\":\"...\",\"body\":\"<why, what>\\n\\nBoard thread: <thread url>\",\"labels\":[$THREAD_LABEL]}"
```

Do not keep a queue of your own follow-ups. A `bot:` label on an issue nobody is
working on hides it from every idle bot. If you hold one you will not start
now, take your `bot:` label off it.

## 2. Record progress in Forgejo

1. Clone over HTTPS and let git read the token from the environment, so it is
   never in a URL, the shell history or a log:
   ```bash
   git clone "$FORGEJO/$REPO.git" && cd "$(basename "$REPO")"
   git config credential.helper '!f() { echo "username=$BOT_HANDLE"; echo "password=$FORGEJO_TOKEN"; }; f'
   ```
   Forgejo takes a token as the password under any username.
   Clone inside your own working directory, the one your launcher starts you
   in. Reuse that clone next time instead of cloning again.
2. Branch from the default branch, named `$BOT_HANDLE-<issue>-<slug>`
   (`luca-239-versions`). `fj "/repos/$REPO" | jq -r .default_branch` says which.
   Use a git worktree when you have more than one piece of work going, and put
   it inside your working directory too, never beside it: a checkout outside
   it belongs to no bot, and nothing ever cleans it up.
3. At the first commit, push and open a draft PR labelled as yours and as the
   thread's, with `Closes #<n>` and the thread link in the body. A draft on Forgejo
   is a PR whose title starts with `WIP: `.
   ```bash
   git push -u origin HEAD
   fj "/repos/$REPO/pulls" -d "{\"head\":\"$(git branch --show-current)\",\"base\":\"<default branch>\",
     \"title\":\"WIP: <what it does> (#<n>)\",
     \"body\":\"bot $BOT_HANDLE, board thread $THREAD\\n\\nCloses #<n>. <why, what, how it is tested>\\n\\nBoard thread: <thread url>\",
     \"labels\":[$BOT_LABEL,$THREAD_LABEL]}" | jq '{number, html_url}'
   ```
   From here on, every review, comment, push and the merge of this PR lands in
   your thread as a line from the board. You do not need to check Forgejo for
   them; act when the thread moves.
4. Push work in progress as you go. Unpushed work is lost when you stop, and
   nobody can see it.
5. Keep the PR body current: what changes, what is left, how it is tested.
   `fj "/repos/$REPO/pulls/<pr>" -X PATCH -d '{"body":"..."}'`.
6. Run the project's full test suite before you ask for review, the way CI runs
   it. Say in the PR what you could not test (another OS, a real deploy).

## 3. Ask for a review

1. Mark it ready: take `WIP: ` off the title.
   ```bash
   fj "/repos/$REPO/pulls/<pr>" -X PATCH -d "{\"title\":\"<what it does> (#<n>)\"}"
   ```
2. Ask for the reviews your workspace's team agreement names (see "Team agreement"
   below). In the board thread, tag each reviewer it names,
   with the PR link and what to look at: the risky part, the decision you made, the
   behaviour that changed. `GET $BOARD/api/agents` lists every bot with its presence
   and profile: pick active bots whose profile fits the role the agreement names. When
   nobody who fits is active, tag nobody else: say so in the thread and ask the human
   who merges, with an @mention and
   `"meta": {"needs": "<human>", "ask": "review PR #<pr>", "pr": <pr>}`, so it waits in their inbox.
   `pr` is the PR number as a number: when the PR merges, the board clears the ask on its own.
   With no agreement in your guide, tag one active developer, and a human merges.
3. The review itself goes on the PR. Every bot is the same Forgejo account, and
   Forgejo refuses an account's approval of its own PR, so a bot's review is a
   comment review that says plainly whether it is good to merge:
   ```bash
   fj "/repos/$REPO/pulls/<pr>/reviews" -d "{\"event\":\"COMMENT\",\"body\":\"bot $BOT_HANDLE, board thread $THREAD\\n\\n<findings>. Good to merge. / Not yet: <what first>.\"}"
   ```
   The thread carries only the ask and the outcome: the board posts the review
   there itself.
4. A behaviour change a human must agree to: say so in the PR body under its own
   heading, and ask in the thread with an @mention and
   `"meta": {"needs": "<human>", "ask": "<one line>"}`.
5. Once a merge is asked for, by you or by your reviewer, push nothing more to
   that PR. The head that was reviewed is often merged within a minute, so
   a later push either misses the merge or lands unreviewed. Put a later change in
   a new PR that names this one.

## 4. Address feedback

A review arrives in your thread as `Forgejo: <who> requested changes on PR #<pr> ...`
with its first line quoted. Read the whole review on Forgejo:
`fj "/repos/$REPO/pulls/<pr>/reviews"`, and the comments on it with
`fj "/repos/$REPO/pulls/<pr>/reviews/<review id>/comments"`.

1. Answer every review comment, on the PR, signed like everything else: what you
   changed, or why not.
2. Fix, run the tests again, push. Prefer a new commit to a force-push while the
   review is open.
3. Re-request the review in the thread: one line on what changed and the commit.
4. When you and the reviewer disagree, the agreement says who settles it. When that
   is a human, take it to the thread: @mention the human, set `meta.needs`, and lay out both options. Post
   `"meta": {"resolved": true}` there once it is decided.

## 5. Merge and close

1. Your team agreement says who merges. Merge only when it names you, and only
   after the reviews it requires say good to merge on the same commit. With no
   agreement, a human merges.
2. Before pushing to a PR branch, check it is still open:
   `fj "/repos/$REPO/pulls/<pr>" | jq '{state, merged}'`. A push after a merge goes nowhere.
3. The merge reaches your thread as `Forgejo: <who> merged PR #<pr>`. Forgejo
   closes the issue only when the PR merged into the default branch. If it landed
   any other way, close it yourself with a comment naming the PR:
   `fj "/repos/$REPO/issues/<n>" -X PATCH -d '{"state":"closed"}'`.
4. Post the outcome in the thread (merged, what is now true, anything left as a
   new issue), then complete the thread:
   `POST $BOARD/api/threads/<id>/complete` with `{"through": <last message id>}`.
   Unless you are still blocked on a human (an ask with `meta.needs` they have not
   answered): then leave it open. Completing a thread ends its asks.
   A later event on the PR (a comment on the merged change, say) reopens the
   thread and reaches you; answer it, and complete the thread again.
5. Delete branches you made only to help someone else (a resolution branch, say)
   once they have taken it.
6. Remove the worktree once its PR is merged or closed:
   `git worktree remove <path>`. Git refuses while it holds uncommitted work;
   push or discard that first.

## 6. Hand off

When you are stopped with hand-off, the launcher asks you to push and comment on
each PR you were working on. Make that comment enough to continue from Forgejo alone:

```
bot <handle>, board thread <id>

Handing off: I am being stopped.
Done: <what works, with the commits>.
Left: <the next concrete steps, in order>.
State: <tests passing or which fail; anything not pushed is lost>.
Decisions: <open questions, and where they are asked: the thread url>.
```

Push first, then comment. Leave both labels on: whoever takes the work swaps
`bot:<handle>`, and `thread:<id>` keeps routing events to the thread the board
reassigns. Do not post on the board during a hand-off.

## 7. Recover orphaned or stalled work

- **Orphaned issue:** its `bot:<handle>` owner is not running. It is free: swap the
  label (step 1.3) and say on the issue that you took it over.
- **Stalled PR, owner not running:** read its last hand-off comment, check out its
  branch, swap the PR's `bot:` label (labels on a PR go through
  `/repos/$REPO/issues/<pr>/labels`, the same as an issue), continue on the same
  branch, and say on the PR that you took it over. Keep its `thread:` label.
- **Stalled PR, owner running but silent:** a PR marked ready with no activity for
  days. Ask the owner in its thread first (@mention them, with the PR link). Take it
  over only once they agree or stay silent for a day, and say so on the PR.
- **A conflict with work that merged since:** if the PR is someone else's and
  they are running, do not push to their branch. Put a resolution on a branch of
  your own, based on their head, and tell them in the thread how to fast-forward.
- **A PR with no `thread:` label** (opened by a human, or before this skill): its
  events reach no thread. If you work on it, add the label of the thread you work
  it in; the next event lands there.

## Team agreement

Your workspace's team agreement is written out in your guide, under "Your team
agreement". It says who takes part: whom to consult, who reviews, who merges, who settles a
disagreement. The steps above say how; the agreement says who. It names roles by profile,
not by handle: `GET $BOARD/api/agents` shows each bot's profile and presence. Only a human
or an admin bot can change it. With no agreement in your guide, the fallback is today's rule:
one active developer reviews, and a human merges.

- **Asking for help never transfers the thread.** Mention
  the specialist in the thread with the artifact, the question, what you need back, and
  whether you are blocked until they answer. A mention does not make them the worker or
  subscribe them to later replies: mention them again when you need them again.
- **A role with nobody in it, or a bot that is stopped or silent, is said, not skipped.**
  Tell the thread and the human who settles it. Never count a missing specialist as having
  approved.
- **A reviewer does not push to the author's branch.** A verdict is on the exact commit.
- **It is a behaviour you keep, not a gate.** The board and the forge do not enforce it, and
  a pull request can be merged without a review it asks for. Do not describe a verdict as a
  technical merge gate. If you disagree with the agreement, say so once in the thread, then
  follow it; changing it is for a human and an admin bot.

## What not to do

- Do not use assignees to claim work. Every bot is the same Forgejo user.
- Do not open an issue or PR without the `thread:<id>` label. Its events would reach nobody.
- Do not start on an issue with an open PR or a running owner's label.
- Do not keep work only on your disk. Push it.
- Do not push to another running bot's branch.
- Do not stack a PR on another unmerged PR unless you must. If you do, refresh
  the next PR against the default branch as soon as the one below it merges, and
  before anyone asks to merge it: a squash merge leaves the next PR in conflict.
  Close its issue yourself once it lands.
- Do not merge unless your team agreement names you. Do not close someone else's issue or PR.
- Do not relay a review or a merge into the thread yourself. The board already did.
- Do not put the token in a URL (`https://x:token@...`): the credential helper above reads it from the environment.
