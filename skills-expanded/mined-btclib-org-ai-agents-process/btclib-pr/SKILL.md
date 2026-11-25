---
name: btclib-pr
description: "btclib-pr — from an open pull request to the decision to approve, and to main; every review answered, CI green"
argument-hint: "[--night] [--land] [pull request URLs or numbers]"
---

# From a pull request to main

Take the open pull requests named in $ARGUMENTS, in repositories of
`btclib-org`, to the decision to approve and to `main`, through *What
was raised*, *Answering it*, *Rebase and CI*, *The decision* and
*Landing*. With no argument, start from *The sweep*.

**First read `$PROCESS/process/every-session.md`, whole, before any
command.** It is two directories above this skill's own, so finding it
takes no command; a change to `main` that lands between this read and
the note below goes unnoticed, a window the session accepts.

**Then note where the process stands**, before reading the rest of it:
the session keeps `$PROCESS`'s `HEAD` in a directory of its scratchpad,
for `orchestration.md`'s *The process is re-read when `main` changes
it*. `echo "$PROCESS"` prints the clone's path.

```shell
scratchpad=<the session's scratchpad>
```

```shell
mkdir -p "${scratchpad:?}/orchestrator"
```

```shell
scratchpad=<the session's scratchpad>
```

```shell
git -C "${PROCESS:?}" rev-parse HEAD > "${scratchpad:?}/orchestrator/process.sha"
```

The client loaded this file before that note, so the session reads it
again, whole and once, from `$PROCESS/skills/btclib-pr/SKILL.md`.

**Then read the shared files, whole**: `every-role.md`, `writing.md`,
`local-review.md` and `orchestration.md`, in `$PROCESS/process/`.
`every-role.md`'s opening says what they hold and what this file holds.
What the session writes, and this file, follow `every-session.md`'s
*Write plainly*.

`every-role.md`'s *Where you work* says how the repository is named.

**Which sections are yours**, beyond `every-role.md`'s map:

- **The writer**: *What was raised*, *Answering it*, *Rebase and CI*,
  *Outside contributors*.
- **The reviewer**: *Rebase and CI*'s first bullet, for the delta it
  reads.
- **The orchestrator**: all of this file.

## The sweep

With no argument, list the organization's open pull requests, read from
the API:

```shell
gh search prs --owner btclib-org --state open --limit 200 \
  --json repository,number,title,author,url,isDraft
```

```shell
gh search prs --owner btclib-org --state open --review-requested @me \
  --limit 200 --json url
```

`gh search prs` has no size fields, so each repository with open pull
requests gives their diff balance (`every-role.md`'s *How an issue and a
pull request are named*):

```shell
repo=<owner>/<repo>
gh pr list --repo "${repo:?}" --state open --limit 200 \
  --json number,additions,deletions,changedFiles
```

**Before the table, start the outside contributors' CI.** For every
pull request of an outside contributor (*Whose pull request it is*)
whose head has runs waiting as `action_required`, the session reads
the diff and approves those runs where *Outside contributors* allows
it. Runs started by `pull_request_review_comment` are left out, as
*Outside contributors*' listing says, and never reported as waiting.
A pull request whose diff fails *Outside contributors*' check is
listed with that as what it waits on: its runs are the human's to
approve. The human then reads the table with that CI running or done,
and a session that works the pull request finds its checks already
there.

Show the human one table, grouped:

- outside contributors';
- waiting on the human's review;
- the human's own, with something to do: a review or thread
   unanswered, changes requested, a red or missing check, a conflict
   with its base;
- the agent's: `claude[bot]` in `gh search prs`, `app/claude` in
  `gh pr view`;
- bots';
- the rest: by day, listed and not worked.

Each row is a `PR` link with its diff balance (`every-role.md`'s *How an
issue and a pull request are named*) and what it waits on. A pull
request may wait on one that carries `release-hold`, as *Landing* says,
and this lists the open or merged ones that carry it:

```shell
gh search prs --owner btclib-org --label release-hold --limit 200 \
  --json repository,number,url,state --jq '.[] | select(.state != "closed")'
```

A draft is listed and not worked. Then put one decision
(`every-session.md`'s *When the human has to decide*): which to work,
and in what order, the recommended order first with its reason. In a
repository whose `main` is red, its repair comes first (*Landing*'s
first bullet). Outside contributors' pull requests come next, oldest
first: their author waits on us, and a reply that comes days late can
lose a contributor.

**At night, no decision is put.** Where the human answered this decision
before the night started (`$PROCESS/process/night-mode.md`'s
activation), that answer stands; otherwise every pull request that is
not a draft is worked up to the approval, in the recommended order, a
red `main`'s repair first and outside contributors' pull requests next:
review rounds, rebase and CI, every item of *What was raised* answered.
Each is worked as *Whose pull request it is* says for its case, and goes
on to *The decision*, or to *The human's own pull request*. One whose
approval is not obvious ends as a deferred item (*Where it is not
obvious*), never as "not worked". Where the session cannot push to
another person's branch, its findings are posted as *Another person's
branch* says, and the deferred item names the author as what it waits
on.

## Whose pull request it is

```shell
gh api user --jq .login
```

```shell
n=<n>
repo=<owner>/<repo>
gh pr view "${n:?}" --repo "${repo:?}" --json author,state,isDraft,\
isCrossRepository,maintainerCanModify,headRefName,headRefOid,baseRefName
```

Then `writing.md`'s *Before starting*, on the pull request. Which case
it is:

- **The human's.** The session works it as its author, and ends it at
  *The human's own pull request*.
- **Another person's, on a branch of the repository.** The session
  works it as its reviewer, and changes it as *Another person's branch*
  says.
- **The agent's**, opened by `app/claude` from `claude/issue-<n>`
  (`CONTRIBUTING.md`'s *Working with an LLM*). The session works it as
  another person's on a branch of the repository, not as a bot's. The
  agent cannot push a fix: its workflow pushes the branch once, without
  force, before it opens the pull request, and the review bot's token
  has `contents: read`. So every fix the approval needs is the
  session's own signed commit, added on top: the agent's commit stays as
  it is (`writing.md`'s *Signed and signed off*). The body's `##
  Evidence` gives the gates of the agent's run, on the agent's commit,
  so once the session pushes a fix it updates that section with its own
  runs on the new head. *The decision* leaves the approval to the human.
- **Left by a session that no longer runs**: the shared take-over, the
  branch becoming the writer's own. Where a session still holds it,
  stop.
- **A bot's** — Dependabot, pre-commit.ci. The reviewer checks that the
  diff moves what its title says and nothing else, `uv.lock` apart,
  which *The decision*'s *The reproduced lock* measures, and in which
  direction: Dependabot follows the default branch, so a submodule
  pinned off it is offered a rollback. Its branch is the bot's: where
  it conflicts, the bot's own rebase command brings it up to date, or
  `gh pr update-branch` for a bot with none, as pre-commit.ci is. Never
  a push but the one below.
  Where the update is wrong, close it with the measurement.

  Where the tree's `CONTRIBUTING.md` says an owner commits a hook's
  output to a bot's branch, that commit is signed, signed off, and
  pushed as a fast-forward only, never with any `--force`. The diff then
  moves a second file, and the reviewer checks that it is the hook's
  output: the hook passes on the head. Dependabot stops rebasing a pull
  request once extra commits are pushed to it ([GitHub's
  documentation][dependabot-rebase]). Where it then needs a rebase,
  `@dependabot recreate` drops the commit and puts back Dependabot's own
  title and body, so the commit and the edit below are made again.

  Where a file the `uv-export` hook writes, such as
  `build-constraints.txt`, moves a package that Dependabot's `uv.lock`
  does not move, that commit is the hook's output, which moves only what
  the lock moves. Where the tree's `CONTRIBUTING.md` gives no owner that
  commit, the pull request goes to the human. Once the commit narrows
  the moves, the title and body are edited to name only the moves the
  branch still makes. The body keeps Dependabot's form of each line,
  which *The reproduced lock* reads.

  The order is: the commit is made, the title and body are edited, and
  then the commit is pushed. The review bot runs on a push but not on an
  edit, so its review of the new head reads the edited text. *The
  decision*'s checks and the fresh reviewer come last, on the new head:
  every item there is measured on it, and the `CLEARED` and each ACK of
  *The reviews on GitHub* name it. This edits them, from a file holding
  the new title and one holding the new body:

  ```shell
  n=<n>
  repo=<owner>/<repo>
  title=<title file>
  body=<body file>
  ```

  ```shell
  gh pr edit "${n:?}" --repo "${repo:?}" --title "$(cat "${title:?}")" \
    --body-file "${body:?}"
  ```

- **An outside contributor's**: *Outside contributors*.

## What was raised

Collect everything said on the pull request, from the API. Paginate
where a page comes back full.

- **Reviews**, each with its state, author, body and the commit it
  names: `gh pr view <n> --repo <owner>/<repo> --json reviews`. The
  bot's review from `claude-review.yml` is one of them.

  CodeRabbit's reviews, on every head of the pull request, are printed
  by this, each body after a line naming its review, the commit it
  reviewed and its link. It prints nothing where CodeRabbit left no
  review, and `error` where the read failed:

  ```shell
  repo=<owner>/<repo>
  n=<n>
  : "${repo:?}" "${n:?}"
  { gh api --paginate "repos/${repo:?}/pulls/${n:?}/reviews?per_page=100" ||
      echo '"read-failed"'
  } | jq -r 'if type != "array" then "error"
    else .[] | select(.user.login == "coderabbitai[bot]")
      | "review \(.id) \(.state) \(.commit_id) \(.html_url)", .body, ""
    end'
  ```

- **Review threads**, inline, with whether each is resolved:

  ```shell
  owner=<owner>
  name=<repo>
  n=<n>
  gh api graphql --paginate -F owner="${owner:?}" -F repo="${name:?}" \
    -F n="${n:?}" -f query='
    query($owner: String!, $repo: String!, $n: Int!, $endCursor: String) {
      repository(owner: $owner, name: $repo) {
        pullRequest(number: $n) {
          reviewThreads(first: 100, after: $endCursor) {
            pageInfo { hasNextPage endCursor }
            nodes {
              id isResolved isOutdated path line
              comments(first: 100) {
                totalCount
                nodes { author { login } body url }
              }
            }
          }
        }
      }
    }'
  ```

  A thread whose `totalCount` exceeds its `nodes` is read whole on its
  own.

- **Suggestions**: a fenced `suggestion` block in a thread's comment.
- **Comments** on the pull request itself: `gh pr view <n> --repo
  <owner>/<repo> --json comments`.
- **Checks**: `gh pr checks <n> --repo <owner>/<repo>`.

Every unresolved thread is an item, whoever wrote it, the bot included,
outdated or not. So is a review or comment from anybody but the human
that asks something, where nobody has answered it or it came after the
human's last comment and last push. A resolved thread is done.

**Each finding in a CodeRabbit review body is an item too, on whichever
head the review names, wherever in the body it sits**: under
*Additional comments* on PR btclib-org/ai-agents-process#472, under
*Outside diff range comments* on PR btclib-org/.github#2309, or as a
failed pre-merge check under *Prompt to fix all issues* on PR
btclib-org/btclib-node#2531. The session reads each body the command
above prints, and no command decides what in it is a finding. A review
covers only the commits since CodeRabbit's last one, so a later push
does not repeat an earlier finding. The item is done once the comment
of *Answering it* answers it; until then it holds the landing as an
open thread does, across pushes (*The reviews on GitHub*).

## Answering it

**Each item is re-measured first**, the whole of it, not its cheap
half, then answered one of three ways:

- **accept**: fixed as `writing.md`'s *Committing and rebasing* says,
  and the answer says what changed.
- **decline**: with the measurement that refutes it, or that shows it a
  refinement (below).
- **decision**: a choice the tree does not settle — design, scope, a
  reserved decision. It goes to the human or the maintainer, as
  `every-session.md`'s *When the human has to decide* says.

Each item and its answer go in the findings record
(`orchestration.md`'s *The findings record*).

**A bot's finding, the review bot's, Codex's or CodeRabbit's, takes the
first of these routes that fits**, measured on the head, unless it needs
a decision:

- **declined** where it does not hold: it needs a condition the text
  already rules out, the sentence it calls false is true where the text
  applies it and leads no reader to a wrong step, or it is a matter of
  taste (`REVIEWING.md`'s *The standard an ack is given against*).
- **filed or declined, never accepted, where it is a refinement**, which
  names no defect on any input and no sentence `every-role.md`'s *Which
  prose is worth a round* blocks on, or where `local-review.md`'s *The
  rounds* keeps it off the branch: it adds no text to the branch. A
  defect `local-review.md`'s *The rounds* keeps off the branch, whether
  or not the branch adds it, and a false sentence it keeps off that the
  branch adds, are filed as `every-role.md`'s *Collateral* says, or as a
  line of a known-limits issue where *The rounds* says, and the reply
  names its issue. A refinement of prose is declined with its ground,
  not filed, since `REVIEWING.md`'s *What is filed, and what is not*
  files no prose; any other finding of this route is filed the same way,
  or else declined with its ground. Repeated after the reply, it is
  answered by pointing to the first reply, and resolved.
- **accepted** where it is the branch's own: a defect or a false
  sentence its diff or its pull request body adds, or anything else
  `every-role.md`'s *Collateral* counts as the branch's subject
  (`local-review.md`'s *A pull request's rounds* says how a fix to the
  branch is reviewed). A sentence of the body is weighed as
  `every-role.md`'s *Which prose is worth a round* says, and is fixed by
  editing the body, which the reply names.
- **filed** where it is older than the branch, holding on the file at
  the merge base too, and the branch does not make it materially worse:
  it goes where `every-role.md`'s *Collateral* says, and the reply names
  the issue where one is filed. A line the branch rewrote can carry an
  older limit, so the case is read on the base's file, not the line
  looked for in the diff. `git merge-base` prints `<base>`, the merge
  base with the pull request's base branch, `baseRefName` (*Whose pull
  request it is*), and `git show` the file there. `<path>` is the file's
  path at `<base>`, the old one where
  `git diff --name-status -M <base> <head>` shows a rename:

  ```shell
  wt=<wt>
  baseref=<baseRefName>
  head=<head>
  git -C "${wt:?}" merge-base "origin/${baseref:?}" "${head:?}"
  ```

  ```shell
  wt=<wt>
  base=<base>
  file=<path>
  git -C "${wt:?}" show "${base:?}:${file:?}"
  ```

**A reply to a bot's finding goes through the branch's rounds before it
is posted**, with the route it took, as `local-review.md`'s *A pull
request's rounds* says.

**Every inline `suggestion` that is accepted is applied in the
worktree.** It is not applied with GitHub's button, so that the gates
run on it.

**Every thread gets a reply, and is then resolved.** An accepted one
names the commit that fixes it; a declined one carries its measurement.
A thread waiting on a decision or on the author is replied to and
resolved once that arrives. The reply meets `every-session.md`'s *What
is posted on a forge*. Write the reply to a file of your own, then:

```shell
thread=<thread id>
reply=<reply file>
```

```shell
gh api graphql -F t="${thread:?}" -F b="@${reply:?}" -f query='
  mutation($t: ID!, $b: String!) {
    addPullRequestReviewThreadReply(
      input: {pullRequestReviewThreadId: $t, body: $b}) { comment { url } }
  }'
```

```shell
thread=<thread id>
```

```shell
gh api graphql -F t="${thread:?}" -f query='
  mutation($t: ID!) {
    resolveReviewThread(input: {threadId: $t}) { thread { isResolved } }
  }'
```

A review or comment outside a thread is answered in one comment on the
pull request, which meets `every-session.md`'s *What is posted on a
forge*. For a CodeRabbit review body, that comment links the review and
answers each finding in it.

**Codex's state on the head changes only when Codex reads it again**: a
reply and a resolved thread leave it in findings. A push can start that
read, its summary then naming `New commits` as the trigger. Where its
finding is answered without a push, a comment `@codex review` on the
pull request asks for the read, and the state on the head is waited
for. A finding Codex repeats after the reply is a finding again: fixed,
or answered as a decision, unless the refinement route above answers
it. *The reviews on GitHub* says when the state such findings leave
does not hold the landing.

### Another person's branch

**Where the session can push to the pull request's branch, it makes
every fix the approval needs itself**, blocking findings and nits
alike: every item is answered as *Answering it* says, with no split
between minor and substantial changes.

Before pushing, the session claims the branch (`writing.md`'s *A claim
holds a pull request's branch*) and pushes with the lease of
`writing.md`'s *Committing and rebasing*, on the sha it built on. Where
the branch moved, they are working: stop and ask.

Where the session has no write access to the branch, the findings are
posted to the author as a review comment, and the pull request waits on
them.

## Rebase and CI

- **The reviewer reads the delta** from the sha it last read. A rebase
  goes to a reviewer only where `orchestration.md`'s *A rebase and the
  clearance* sends it. A fresh reviewer's first read is the whole diff
  from its parent.
- **A pull request is rebased onto the default branch only where
  `CONTRIBUTING.md`'s *Landing it* says, or for a retarget.** An outside
  contributor's branch, or the agent's, is never rebased: *Outside
  contributors* brings `main` in by a merge.
- **After a rebase or a merge of `main`, run the gates `writing.md`'s
  *The gates* asks, and push.** Ask the merge the forge will compute,
  locally: `git -C <wt> -c merge.union.driver=false merge-tree
  origin/main <branch>` exits `1` where GitHub will refuse. `gh pr view
  --json mergeable` is a cached value.
- **Wait for the checks on the head just pushed**, in the background, by
  asking until none is pending: `gh pr checks --watch` can return while
  runs are still queued. It asks at the interval, and stops at the
  quota, that `every-session.md`'s *The forge's quota is shared* gives.
  The list covers check runs and commit statuses, pre-commit.ci's among
  them. It must not be empty: right after a push nothing has reported
  yet. The loop gives up after 30 minutes, or once the quota stops it or
  cannot be read; say so where it does.

  Before the loop, read `gh pr view <n> --repo <owner>/<repo> --json
  mergeable,mergeStateStatus`, and read it again where it answers
  `UNKNOWN`, which means not computed yet. `CONFLICTING` (`DIRTY`) is a
  merge with a conflict: no GitHub Actions run starts, and
  pre-commit.ci's status reads `error during mergeable check`, with no
  run to read. Bring the base in as the bullets above say, or, for a
  stacked pull request whose base was amended, as `CONTRIBUTING.md`'s
  *One subject, opened as soon as it is written* says.

  ```shell
  n=<n>
  repo=<owner>/<repo>
  for i in $(seq 16); do
    low=$(gh api rate_limit --jq '.resources | {core, graphql}
      | to_entries[] | select(.value.remaining < 500)
      | "\(.key) \(.value.remaining) reset \(.value.reset | todate)"') ||
      low=unread
    [ -z "$low" ] || break
    [ "$(gh pr checks "${n:?}" --repo "${repo:?}" --json bucket \
      --jq 'length > 0 and all(.[]; .bucket != "pending")')" = true ] &&
      break
    [ "$i" = 16 ] || sleep 120
  done
  case $low in
    '') gh pr checks "${n:?}" --repo "${repo:?}" ;;
    unread) (exit 5) ;;
    *) echo "$low"; (exit 3) ;;
  esac
  ```

  The block's exit code says how the loop ended: `0` all passed, `1` a
  failure or no checks at all, `8` still pending with none failed, `3`
  stopped at the quota, whose lines it prints, `5` stopped where
  `gh api rate_limit` failed; neither `3` nor `5` runs the final
  `gh pr checks`. The loop gave up wherever the output still lists a
  pending check or says `no checks reported`.

  A section that runs this block with a test of its own puts that test
  in place of both the loop's test of the checks and the final `gh pr
  checks`. Unless the quota stops the block, its exit code is the final
  test's.

  **After a close and reopen, a check `gh pr checks` shows as skipped may
  have failed**
  ([ISS 198](https://github.com/btclib-org/ai-agents-process/issues/198)).
  `gh pr checks` shows one run of each check. A workflow that runs on the
  `closed` event and skips its jobs there writes a skipped run of each,
  and that run can be the one shown. This writes the name of each check
  run on the head that has not completed, and of each that started at or
  after the last reopen and concluded neither `SUCCESS`, `SKIPPED` nor
  `NEUTRAL`. On a pull request never reopened it reads every run. It must
  exit `0`:

  ```shell
  owner=<owner>
  name=<repo>
  n=<n>
  red=<red file>
  ```

  ```shell
  gh api graphql --paginate -F owner="${owner:?}" -F repo="${name:?}" \
    -F n="${n:?}" -f query='
    query($owner: String!, $repo: String!, $n: Int!, $endCursor: String) {
      repository(owner: $owner, name: $repo) {
        pullRequest(number: $n) {
          timelineItems(itemTypes: [REOPENED_EVENT], last: 1) {
            nodes { ... on ReopenedEvent { createdAt } }
          }
          commits(last: 1) { nodes { commit { statusCheckRollup {
            contexts(first: 100, after: $endCursor) {
              pageInfo { hasNextPage endCursor }
              nodes { ... on CheckRun { name status conclusion startedAt } }
            }
          } } } }
        }
      }
    }' --jq '.data.repository.pullRequest
    | (.timelineItems.nodes[0].createdAt // "") as $reopened
    | .commits.nodes[0].commit.statusCheckRollup.contexts.nodes[]
    | select(.name and (.status != "COMPLETED" or (.startedAt >= $reopened
      and (.conclusion | IN("SUCCESS", "SKIPPED", "NEUTRAL") | not))))
    | .name' > "${red:?}"
  ```

  A `cancelled` run is not a `failure`.
- **A red check is read before anything is done about it**:
  `gh run view <run id> --repo <owner>/<repo> --log-failed`. Then:
    - **caused by the pull request**: fixed as an accepted item, under
      *Another person's branch* where it is not the human's;
    - **red on the default branch too**, same check
      (`gh run list --repo <owner>/<repo> --branch main --workflow
      <file> --limit 5`): not this pull request's. Find or file its
      issue; its repair comes first (*Landing*'s first bullet). A
      required check holds the pull request. Once the repair has
      landed, close and reopen the pull request, with no push
      (`CONTRIBUTING.md`'s *Landing it* says why):

      ```shell
      n=<n>
      repo=<owner>/<repo>
      ```

      ```shell
      gh pr close "${n:?}" --repo "${repo:?}"
      gh pr reopen "${n:?}" --repo "${repo:?}"
      ```

      The reopen's runs can still test the merge with the old `main`:
      GitHub refreshes `refs/pull/<n>/merge` lazily, and the event
      carries the merge it held, as the second reopen of PR
      btclib-org/btclib#2754 did. A run's log names the merge it tested,
      `Merge <head> into <base>`. `gh run view --log` writes the log,
      and `grep` prints the line that names it:

      ```shell
      repo=<owner>/<repo>
      run=<run id>
      log=<log file>
      ```

      ```shell
      gh run view --repo "${repo:?}" --log "${run:?}" > "${log:?}"
      ```

      ```shell
      grep -m1 'HEAD is now at .* Merge .* into ' <log file>
      ```

      This answers `ahead` or `identical` where `<base>` holds the
      repair:

      ```shell
      gh api --jq .status repos/<owner>/<repo>/compare/<repair sha>...<base>
      ```

      Where it answers anything else, the merge lacks the repair: close
      and reopen again, and read the new runs.

      *The decision* reads the bot's review of the reopen. A check that
      only reports is named in the decision;
    - **not reproducing**: `writing.md`'s *A failure that does not
      reproduce is measured*. One re-run measures it (`gh run rerun <run
      id> --repo <owner>/<repo> --failed`); two different answers are an
      issue, not a green;
    - **never given a runner**: a job cancelled with the annotation `The
      job was not acquired by Runner of type hosted even after multiple
      attempts` never ran, so it is neither a failure nor *not
      reproducing*'s measure. A job's id is its check run's, so the read
      of the run's `jobs` prints the ids of its cancelled jobs, and the
      read of a job's `annotations` prints that job's annotations:

      ```shell
      repo=<owner>/<repo>
      run=<run id>
      gh api --jq '.jobs[] | select(.conclusion == "cancelled") | .id' \
        --paginate "repos/${repo:?}/actions/runs/${run:?}/jobs"
      ```

      ```shell
      repo=<owner>/<repo>
      job=<job id>
      gh api --jq '.[].message' \
        --paginate "repos/${repo:?}/check-runs/${job:?}/annotations"
      ```

      Each job cancelled this way takes up to four re-runs, by the id
      the read of `jobs` prints, each started once the last attempt has
      ended, and the checks are waited for again after each. GitHub
      waits about 15 minutes for a runner before it cancels the job, so
      the attempts are that far apart. `gh run rerun` re-runs the job
      and the jobs that depend on it, and no other failed job of the
      run, which *not reproducing* bounds:

      ```shell
      repo=<owner>/<repo>
      job=<job id>
      ```

      ```shell
      gh run rerun --repo "${repo:?}" --job "${job:?}"
      ```

      On PR btclib-org/btclib-secp256k1#1360 a macOS job of the `test`
      run was cancelled this way on four attempts, and ran on the fifth.
      Where the fourth re-run is cancelled the same way, the wait is
      GitHub's: label the pull request `waits-github`, comment on it
      with the run and the message (`every-session.md`'s *A hold is
      recorded on the issue or pull request*), and report it. The human
      decides what follows;
    - **review quota exhausted**: the log of `Claude review` holds the
      line `api_error_status 429` (match with that, not with
      `api_error_status` alone: the log also echoes the workflow's own
      source) followed by a line such as `You've hit your weekly limit ·
      resets 11am (UTC)`.
      `$PROCESS/skills/btclib-pr/review-quota.md` says how the reset is
      read and what follows, and is read where such a run fails.

- **The reviews on GitHub are answered like any other**, iterating until
  none holds the landing on the current head (*The reviews on GitHub*).

## The reviews on GitHub

Three reviewers read a pull request on GitHub, where the repository has
them: the review bot of `claude-review.yml`, Codex and CodeRabbit. On
the head, each is in one of three states: **ACK**, **findings** or
**absent**. A review still running on the head is in none of them,
whatever an earlier answer on that head says: it is waited for, never
read as absent, and each reviewer's running test is read first.

**A pull request is approved or landed only where none of the three is
in findings, and each that is not absent gave its ACK on the head.**
Codex's state in findings counts as its ACK here where it rests only on
threads that *Answering it*'s refinement route answered and resolved,
and those threads are recorded as the reason of an absence is, below.
An absence does not hold the landing; *The decision* says where the
bot's makes the approval not obvious. Where all three are absent, the
pull request waits for the human: no session approves or lands it
before his word. None of the three is a check the rulesets require. The
reason of each absence is recorded before the approval or the landing:
in the pull request's `## Evidence` where its body is the session's,
otherwise in a comment of the session's own naming the head.

What each command below prints is tested by its value
(`every-session.md`'s *Shell, checkouts and prose*).

**The review bot**, `claude` in `gh pr view`. It is running while a run
of its check on the head has not completed. Every run is read, since
`gh pr checks` shows one of each check, which can be a skipped run a
comment started, and the endpoint's default `filter=latest` hides an
older run behind a newer one. This prints `running`, `done`, or `error`
where the read failed:

```shell
repo=<owner>/<repo>
head=<head>
: "${repo:?}" "${head:?}"
{ gh api --paginate -X GET -F per_page=100 -f filter=all \
    "repos/${repo:?}/commits/${head:?}/check-runs" \
    --jq '.check_runs[] | select(.name == "claude-review / Claude review")
      | .status' || echo read-failed
} | jq -Rrs 'if test("read-failed") then "error"
  elif split("\n") | any(. != "" and . != "completed") then "running"
  else "done" end'
```

Once it prints `done`, of the bot's reviews whose verdict line names the
head, the latest counts. This prints `ack` where that one is
`ACK <head>`, `findings` where it is another verdict, and `none`, which
is absent, where no verdict line names the head:

```shell
n=<n>
repo=<owner>/<repo>
gh pr view "${n:?}" --repo "${repo:?}" --json headRefOid,reviews \
  --jq '.headRefOid as $h
  | [.reviews[] | select(.author.login == "claude")
    | ((.body // "") + "\n" | split("\n")[0])
    | select(test("^(ACK|CHANGES REQUESTED|NACK|NO VERDICT) "
        + $h + "(:|\\s|$)"))]
  | if length == 0 then "none"
    elif last | startswith("ACK ") then "ack" else "findings" end'
```

`skills/btclib-inbox/measure.sh` reads the verdict line the same way in
GraphQL, in its `ack`, but only among the bot's latest reviews, as
`skills/btclib-inbox/SKILL.md` says, where this command reads them all.
A change to this one changes that one too.

Where it is absent, in these cases or another, the pull request is
merged only once the latest fresh reviewer's `CLEARED` also names the
head, or the dedicated reviewer's where the other client is unavailable
(`orchestration.md`'s *Where the other client is unavailable*):

- the bot's run failed with a 429, its quota exhausted, matched as
  *Rebase and CI* says;
- the pull request changes `claude-review.yml`, or a reusable workflow
  that `claude-review.yml` calls by a local path, as
  btclib-org/.github's calls `reusable-claude-review.yml`. The bot
  reviews neither: the action refuses to run where either differs from
  the default branch's copy, and its check fails. Run
  [42404355279](https://github.com/btclib-org/.github/actions/runs/42404355279),
  on PR btclib-org/.github#2116, logs that refusal as `Skipping action
  due to workflow validation`;
- the pull request comes from a fork, `isCrossRepository` being `true`
  in *Whose pull request it is*
  ([ISS 248](https://github.com/btclib-org/ai-agents-process/issues/248)).
  `btclib-org/.github`'s `reusable-claude-review.yml` skips the review
  where `head.repo.full_name` is not the calling repository. No session
  asks for it with an `@claude` comment either: that run is handed the
  credential while it reads the contributor's text. The `CLEARED` stands
  for the bot's ACK, and the pull request is approved as *The decision*
  says and merged as *Merging* says, as any other is.

Where such a pull request lands through the bypass (*The human's own
pull request*), every check but the bot's `Claude review` is green as
well.

The second case's reusable workflows are the ones this lists: each job's
`uses:` in the default branch's `claude-review.yml` that names a local
path, read as YAML, so that a quoted path counts and a comment or a
step's local action does not. It lists nothing where that file calls
none:

```shell
repo=<owner>/<repo>
gh api -H 'Accept: application/vnd.github.raw' \
  "repos/${repo:?}/contents/.github/workflows/claude-review.yml" \
  | uv run --isolated --no-config --no-project --python 3.15 \
    --with pyyaml==6.0.3 python -I -c '
import sys, yaml
for job in yaml.safe_load(sys.stdin)["jobs"].values():
    if str(job.get("uses", "")).startswith("./"):
        print(job["uses"])'
```

**Codex**, `chatgpt-codex-connector`. It keeps one summary comment on
the pull request, whose body carries its state as
`codex-review-state:v1`, and its comment says it reacts with `eyes`
while a review runs. Its findings come as a review with inline threads.
The state's format is the vendor's and undocumented, so a state that is
missing, names another commit or does not parse reads as absent, never
as an ACK. *Answering it* says what moves the state once a finding is
answered. This prints `ack` where the code review on the head completed
with no unresolved finding, `findings` where it completed with one,
`running` while the `eyes` reaction stands or the state on the head has
a status other than `completed` and `failed`, `error` where a read
failed, and `absent` otherwise, as on a `failed` review, which Codex's
usage limit gives. The `eyes` reaction is read on the pull request and
on each of its comments, since Codex's comment does not say which one it
marks. `<head>` is the full `headRefOid`:

```shell
repo=<owner>/<repo>
n=<n>
head=<head>
: "${repo:?}" "${head:?}"
{ gh api --paginate "repos/${repo:?}/issues/${n:?}/comments?per_page=100" \
    --jq '.[] | select(.user.login == "chatgpt-codex-connector[bot]")
      | .body' || echo codex-read-failed
  gh api --paginate "repos/${repo:?}/issues/${n:?}/reactions?per_page=100" \
    --jq '.[] | select(.user.login == "chatgpt-codex-connector[bot]"
      and .content == "eyes") | "codex-eyes"' || echo codex-read-failed
  ids=$(gh api --paginate "repos/${repo:?}/issues/${n:?}/comments" \
    --jq '.[] | select(.reactions.eyes > 0) | .id') || echo codex-read-failed
  for id in $(printf '%s\n' "$ids"); do
    gh api --paginate "repos/${repo:?}/issues/comments/${id}/reactions" \
      --jq '.[] | select(.user.login == "chatgpt-codex-connector[bot]"
        and .content == "eyes") | "codex-eyes"' || echo codex-read-failed
  done
} | jq -Rrs --arg h "${head:?}" '
  ([scan("codex-review-state:v1 (\\{.*\\}) -->") | .[0]] | last
    | try (fromjson | .code_review) catch null) as $c
  | if test("codex-read-failed") then "error"
    elif test("codex-eyes") then "running"
    elif ($c | type) != "object" or $c.commit_sha != $h then "absent"
    elif $c.status == "completed" and $c.has_unresolved_findings == false
      then "ack"
    elif $c.status == "completed" and $c.has_unresolved_findings == true
      then "findings"
    elif $c.status == "completed" or $c.status == "failed" then "absent"
    else "running" end'
```

A review of a push can start minutes after it. So `absent`, read before
the checks on the head have completed (*Rebase and CI*'s wait), is read
again once they have, and that read stands.

**CodeRabbit**, `coderabbitai`, posts no verdict of its own outside a
pilot
([ISS 432](https://github.com/btclib-org/ai-agents-process/issues/432))
that turns its approvals on in btclib-org/ai-agents-process: its
`CodeRabbit` check passes once it has read the head, findings or not.
Until the pilot reports, its states are these, there too. Findings is one of
its threads open, read as *What was raised* reads them, or a finding in
one of its review bodies, on any head of the pull request, that no
comment of *Answering it* answers. Its ACK on the head is a pass of the
latest run of its check whose `details_url` names this pull request,
since another can share the head, with none of its threads open and
every finding in its review bodies answered. It is running while a run
of that check has not completed, and absent otherwise, as where the
check was skipped, its comment saying why (`Review skipped`,
`Reviews paused`).
This prints `ack`, `findings`, `running`, `absent`, or `error` where a
read failed. It reads the check and the threads, not the bodies: its
`ack` is CodeRabbit's ACK only where the session read the bodies, as
*What was raised* says, after every run of that check on the head had
completed, and every finding in them is answered. A read made earlier
can miss a review: on PR btclib-org/ai-agents-process#472, CodeRabbit
posted the review holding its finding 9 seconds before its check
completed:

```shell
repo=<owner>/<repo>
n=<n>
head=<head>
: "${repo:?}" "${head:?}"
{ gh api --paginate -X GET -f check_name=CodeRabbit -f filter=all \
    -F per_page=100 \
    "repos/${repo:?}/commits/${head:?}/check-runs" \
    --jq '.check_runs[] | select(.app.slug == "coderabbitai")
      | "check \(.id) \(.status) \(.conclusion) \(.details_url)"' ||
    echo read-failed
  gh api graphql --paginate -F owner="${repo%%/*}" -F repo="${repo#*/}" \
    -F n="${n:?}" -f query='
    query($owner: String!, $repo: String!, $n: Int!, $endCursor: String) {
      repository(owner: $owner, name: $repo) {
        pullRequest(number: $n) {
          reviewThreads(first: 100, after: $endCursor) {
            pageInfo { hasNextPage endCursor }
            nodes {
              isResolved
              comments(first: 1) { nodes { author { login } } }
            }
          }
        }
      }
    }' --jq '.data.repository.pullRequest.reviewThreads.nodes[]
      | select((.isResolved | not)
        and .comments.nodes[0].author.login == "coderabbitai") | "open"' ||
    echo read-failed
} | jq -Rrs --arg u "/${repo:?}/pull/${n:?}?" '
  (split("\n") | map(select(startswith("check ")) | split(" "))
    | sort_by(.[1] | tonumber)) as $c
  | if test("read-failed") then "error"
    elif any($c[]; .[2] != "completed") then "running"
    elif test("(^|\n)open(\n|$)") then "findings"
    elif [$c[] | select(.[4] + "?" | contains($u))][-1][3] == "success"
      then "ack"
    else "absent" end'
```

## The decision

**The session's approval is the human's** (`every-role.md`'s *Three
roles the process names*). Their standing instruction covers an obvious
approval, as defined below, and nothing else. Every other approval is
theirs to give.

**GitHub refuses an approval from a pull request's author.** On the
human's own pull request the session never approves: *The human's own
pull request* says what it does instead.

**Where `main` is not protected yet, the pull request is held.** In a
repository whose branch protection and rulesets are not applied yet,
*Merging*'s command that writes `<required file>` answers `Branch not
protected` (HTTP 404) and exits `1`. Nothing then requires an approval
or a check, so a merge lands whatever head it is given. The session
neither approves nor merges any pull request there, the human's own
included. It records a hold with `needs-maintainer`
(`every-session.md`'s *When the human has to decide*), protection being
a repository setting. The hold lasts until that command exits `0`, and
the pull request is then decided on its head as this section says.

**The approval is obvious where every item holds**, each measured on the
head `<sha>`. The diff is read once, by two commands that must each
exit `0`:

```shell
n=<n>
repo=<owner>/<repo>
list=<list file>
```

```shell
gh pr diff "${n:?}" --repo "${repo:?}" --name-only > "${list:?}"
```

```shell
n=<n>
repo=<owner>/<repo>
diff=<diff file>
```

```shell
gh pr diff "${n:?}" --repo "${repo:?}" > "${diff:?}"
```

The list omits the old path of a renamed file, so add it from the diff:

```shell
diff=<diff file>
list=<list file>
```

```shell
grep '^rename from ' "${diff:?}" | cut -d' ' -f3- >> "${list:?}"
```

- [ ] the author is not the human: `.author.login` differs from
      `gh api user --jq .login`
- [ ] the author is not the agent: `.author.login` is not `app/claude`.
      Whoever approves the agent's pull request reads every line
      (`CONTRIBUTING.md`'s *Working with an LLM*), so the human decides
- [ ] the latest fresh reviewer's `CLEARED` names `<sha>`, or
      `orchestration.md`'s *A rebase and the clearance*, or
      `local-review.md`'s *A merge of `main` and the clearance*, carries
      it to `<sha>`; where the other client is unavailable, the
      dedicated reviewer's does (`orchestration.md`'s *Where the other
      client is unavailable*)
- [ ] every check passed or was skipped, required or not:
      `gh pr checks <n> --repo <owner>/<repo> --json bucket --jq
      'length > 0 and all(.[]; .bucket == "pass" or .bucket ==
      "skipping")'` answers `true`; *Rebase and CI*'s command that
      writes `<red file>` exits `0`; and `test ! -s <red file>` exits
      `0`. A cancelled check (bucket `cancel`) fails this item until a
      re-run passes; *Rebase and CI*'s *never given a runner* bounds the
      re-runs of a job GitHub never gave a runner.
- [ ] the rule of *The reviews on GitHub* holds on `<sha>`. While the
      bot is out of quota (a 429 with its reset ahead, read as *Rebase
      and CI* says), its review is absent, the checks item fails, and
      the human decides (*Where it is not obvious*); on the human's own
      pull request, *The human's own pull request* says who does. The
      bot's absent review does not stop the approval. On a bot's pull
      request (*A bot's pins*) whose pins change
      `.github/workflows/claude-review.yml`, or a reusable workflow that
      file calls by a local path, the bot's review may be absent, and
      its `Claude review` check may fail while every other check passed
      or was skipped, as the second case *The reviews on GitHub* lists
      allows
- [ ] no review thread is unresolved, every page read (*What was
      raised*). It binds every approval, the human's decision included;
      *Merging* has it for the merge
- [ ] every item of *What was raised* is answered
- [ ] no other reviewer's changes requested stand: `latestReviews`
      holds no `CHANGES_REQUESTED`
- [ ] no item waits on a decision or on the author, and the branch
      takes no decision its issue reserved
- [ ] the repository is not `btclib-org/ai-agents-process`, whose every
      file gives instructions or rules
- [ ] the list holds no file that gives instructions or rules: the
      first command below prints nothing, and the second, where it
      runs, exits `0`
- [ ] every other file in the list is a doc, a test, `pyproject.toml`
      or `uv.lock`, or an exported lock, `.clusterfuzzlite/requirements.txt`
      or `build-constraints.txt` (*The exported lock*, below):
      the third command below prints nothing and exits `1`
- [ ] `pyproject.toml` only moves requirements it already holds to a
      new version, read from the fourth command below
- [ ] the head's `uv.lock`, its `revision` line apart, is what uv
      writes from the base's lock and the versions the body names (*The
      reproduced lock*, below)
- [ ] on a bot's pull request (*A bot's pins*, below), its pin files
      only move pins: the fifth command below prints nothing, and the
      sixth, where it runs, exits `0`
- [ ] a major move of a dependency, a hook or an action has the latest
      fresh reviewer's `CLEARED` answer `local-review.md`'s *The
      verdict*'s item on it, saying that nothing in the notes breaks the
      tree; where the other client is unavailable, the dedicated
      reviewer's does (`orchestration.md`'s *Where the other client is
      unavailable*)

The first prints each file under `.github/` or any `.claude/`, any top-level
`RELEASING.md`, `REPOSITORY.md` or `SECURITY.md`, and any `AGENTS.md`,
`REVIEWING.md`, `GOVERNANCE.md` or `CONTRIBUTING.md`. It exits `1` where
there is none:

```shell
grep -E -e '^\.github/|^(AGENTS|RELEASING|REPOSITORY|SECURITY)\.md$' \
  -e '(^|/)(\.claude/|(AGENTS|REVIEWING|GOVERNANCE|CONTRIBUTING)\.md$)' \
  <list file>
```

The second looks for the readme a package publishes: the `readme` of
`[project]` in the head's `pyproject.toml`. Read the file first. Where
`gh` answers `Not Found`, the tree has none, and the second is skipped:

```shell
gh api -H 'Accept: application/vnd.github.raw' \
  "repos/<owner>/<repo>/contents/pyproject.toml?ref=<sha>" > <toml file>
```

The second prints the readme where the list holds it, and exits `0`
only where it does not:

```shell
toml=<toml file>
list=<list file>
uv run --no-project --python 3.15 python -c 'import sys, tomllib
r = tomllib.load(open(sys.argv[1], "rb"))["project"].get("readme", "")
r = r if isinstance(r, str) else r.get("file", "")
sys.exit(bool(r) and r in open(sys.argv[2]).read().splitlines() and r)' \
  "${toml:?}" "${list:?}"
```

The third prints each file that fails its item, and exits `1` where
none does. The third reads `<export file>`. This writes it empty;
*The exported lock*, below, then fills it where it applies:

```shell
: > <export file>
```

Once *The exported lock*, below, has run where it applies, the third:

```shell
list=<list file>
exported=<export file>
grep -Ev '^(docs|tests)/|\.md$|^(pyproject\.toml|uv\.lock)$' "${list:?}" |
  grep -vxFf "${exported:?}"
```

The fourth prints the diff of `pyproject.toml`:

```shell
awk '/^diff --git /{p = ($(3) == "a/pyproject.toml")} p' <diff file>
```

It writes the third field as `$(3)`, and the fifth writes the line as
`$(0)`: Claude Code replaces a `$` and a digit in a skill with an
argument of the skill.

Any other change in it fails this item, a new requirement included.

**A bot's pins.** On a pull request whose `.author.login`, as `gh pr
view` prints it, is `app/pre-commit-ci` or `app/dependabot`, the pin
files may change too: `.pre-commit-config.yaml`, and each `*.yml`
directly under `.github/workflows/`. The first and third commands then
read the list without them, which this writes, in place of `<list
file>`. Any other path under `.github/` still fails the first:

```shell
list=<list file>
rest=<rest file>
```

```shell
grep -Ev '^(\.pre-commit-config\.yaml|\.github/workflows/[^/]+\.yml)$' \
  "${list:?}" > "${rest:?}"
```

The fifth prints each line a pin file changes that does not read as a
pin, and the header lines of a diff that adds, removes or renames a pin
file, whichever of its two paths is the pin file. A line reads as a pin
where it is a `rev:` line of `.pre-commit-config.yaml`, with its
`# frozen:` comment where it has one, or a workflow's `uses:` line
naming its action at a 40-digit sha, with its `# vX.Y.Z` comment. A
`rev:` line whose value starts with `&`, `*`, `|`, `>` or `!` does not
read as a pin. An action's pins are paired by the line without its sha,
and it prints an action whose pins do not pair:

```shell
awk '/^diff --git /{f = $(3); h = 1
    p = $(0) ~ / [ab]\/\.pre-commit-config\.yaml( |$)/ ||
      $(0) ~ / [ab]\/\.github\/workflows\/[^\/ ]+\.yml( |$)/; next}
  !p {next}
  /^@@/{h = 0; next}
  h && !/^(index |--- |[+][+][+] )/ {print f ": " $(0); next}
  h {next}
  !/^[-+]/ {next}
  {k = substr($(0), 2); d = /^[+]/ ? 1 : -1}
  f ~ /yaml$/ && k ~ /^ *rev: *[^ #&*|>!][^ #]*( *# frozen: [^ ]+)?$/ {next}
  f ~ /yml$/ && k ~ /^ *(- )?uses: *[^ @]+@[0-9a-f]{40} *# *v?[0-9][^ ]*$/ {
    sub(/@.*/, "", k); n[f k] += d; next}
  {print f ": " $(0)}
  END {for (k in n) if (n[k]) print "unpaired: " k}' <diff file>
```

A line can read as a pin and be none, as a `rev:` line inside a hook's
`entry:`. So where the list holds `.pre-commit-config.yaml`, the sixth
parses the file at `<base>` and at `<sha>`. `<base>` is the merge base
*The clone*, below, prints: the diff is taken against it, so a change
`main` made since does not count as the pull request's. These write the
two files, and each must exit `0`. Where one answers `Not Found`, the
pull request adds or removes the file, and the item fails:

```shell
gh api -H 'Accept: application/vnd.github.raw' \
  "repos/<owner>/<repo>/contents/.pre-commit-config.yaml?ref=<base>" \
  > <base yaml>
```

```shell
gh api -H 'Accept: application/vnd.github.raw' \
  "repos/<owner>/<repo>/contents/.pre-commit-config.yaml?ref=<sha>" \
  > <head yaml>
```

The sixth exits `0` only where both files load to a mapping with no key
twice and no value that contains itself, whose `repos` is a list of
mappings, the two are equal once the `rev` of each `repos` entry is
masked, and each entry other than `local` and `meta` has a string `rev`
on both sides. Otherwise it prints why a file fails, each top-level key
whose value differs or that one side lacks, or that the keys are in
another order. Without `--isolated`, uv puts the `.venv` of the working
directory or of a parent, or the one `VIRTUAL_ENV` names, under the
`--with` environment, and runs its `.pth` files even under `-I`:

```shell
base=<base yaml>
head=<head yaml>
uv run --isolated --no-config --no-project --python 3.15 \
  --with pyyaml==6.0.3 python -I -c '
import sys, yaml
MERGE = object()
class L(yaml.SafeLoader):
    def compose_mapping_node(self, anchor):
        node = super().compose_mapping_node(anchor)
        keys = [MERGE if k.tag == "tag:yaml.org,2002:merge" else
                self.construct_object(k, deep=True) for k, _ in node.value]
        if len(set(keys)) != len(keys):
            raise yaml.MarkedYAMLError("a key is repeated", node.start_mark)
        return node
    def construct_document(self, node):
        return self.construct_object(node, deep=True)
def masked(path):
    try:
        d = yaml.load(open(path), L)
    except yaml.YAMLError as e:
        sys.exit(path + ": " + " ".join(str(e).split()))
    if not isinstance(d, dict):
        sys.exit(path + ": not a mapping")
    if not isinstance(d.get("repos"), list):
        sys.exit(path + ": repos is not a list")
    for r in d["repos"]:
        if not isinstance(r, dict):
            sys.exit(path + ": a repos entry is not a mapping")
        if r.get("repo") not in ("local", "meta") and not isinstance(
                r.get("rev"), str):
            sys.exit(path + ": the rev of " + repr(r.get("repo")))
        if "rev" in r:
            r["rev"] = None
    return d
b, h = masked(sys.argv[1]), masked(sys.argv[2])
kb = {repr(k): repr(v) for k, v in b.items()}
kh = {repr(k): repr(v) for k, v in h.items()}
d = [k for k in list(kb) + list(kh) if kb.get(k, "absent") !=
     kh.get(k, "absent")]
for k in dict.fromkeys(d):
    print(k + ": " + kb.get(k, "absent") + " -> " + kh.get(k, "absent"))
if repr(b) != repr(h) and not d:
    print("the keys are in another order")
sys.exit(repr(b) != repr(h))' "${base:?}" "${head:?}"
```

**The clone.** *The exported lock* and *The reproduced lock* run in one
clone of `<sha>`, made once where either applies, before both. The
clone directory is a new one of your own. Shell state does not survive
between calls (`every-role.md`'s *Where you work*), so each command
below takes its values in the same call: a fence that writes has them
in a fence of their own just above it, as section 9 of the
organization's standard says, and a fence that only reads has them at
its head. Fill them in every time. `<base>` is the merge base of `<sha>`
with `baseRefName` (*Whose pull request it is*), which this prints:

```shell
gh api --jq .merge_base_commit.sha \
  repos/<owner>/<repo>/compare/<baseRefName>...<sha>
```

```shell
clone=<clone dir>
```

```shell
git init --quiet "${clone:?}"
```

```shell
clone=<clone dir>
sha=<sha>
base=<base>
repo=<owner>/<repo>
```

```shell
git -C "${clone:?}" fetch --quiet --depth 1 "https://github.com/${repo:?}" \
  "${sha:?}" "${base:?}"
```

```shell
clone=<clone dir>
sha=<sha>
```

```shell
git -C "${clone:?}" checkout --quiet --detach "${sha:?}"
```

**The exported lock.** On a pull request whose `.author.login` is
`app/dependabot`, and whose list holds
`.clusterfuzzlite/requirements.txt` or `build-constraints.txt`, each of
the two the list holds passes the third command where the commands below
regenerate it on `<sha>` and find it byte for byte the same
([ISS 249](https://github.com/btclib-org/ai-agents-process/issues/249)).
They run the `uv-export` hook, which runs `uv export` with the tree's
arguments for each of the two the tree holds, by the command the tree's
`CONTRIBUTING.md` gives an owner (*A bot's*, under *Whose pull request
it is*), in the clone.

Both files are removed first, so that a hook that does not write one
leaves it missing, which the loop that fills `<export file>` reads as a
difference. A tree may hold only one of them:

```shell
clone=<clone dir>
```

```shell
for f in .clusterfuzzlite/requirements.txt build-constraints.txt; do
  rm -f "${clone:?}/${f:?}"
done
```

The hook exits `1` when it writes a file, so its exit code is not
read:

```shell
clone=<clone dir>
```

```shell
env -C "${clone:?}" uv run --locked --only-group lint \
  pre-commit run uv-export --all-files
```

This adds to `<export file>` each of the two that `<sha>` holds and the
hook wrote back byte for byte the same, and exits `0` whichever it adds:

```shell
clone=<clone dir>
sha=<sha>
exported=<export file>
```

```shell
for f in .clusterfuzzlite/requirements.txt build-constraints.txt; do
  if git -C "${clone:?}" cat-file -e "${sha:?}:${f:?}" 2>/dev/null &&
    git -C "${clone:?}" diff --quiet -- "${f:?}"; then
    echo "${f:?}" >> "${exported:?}"
  fi
done
```

**The reproduced lock.** Where the list holds `uv.lock`, the commands
below run in the clone, after *The exported lock* where it applies,
since its hook reads the head's lock. In place of the head's lock they
put the base's, then move each package the pull request's body names to
the version it names. Dependabot names a group's moves one a line,
``Updates `x` from 1.0 to 1.1``, and a single move on the body's first
line, which starts `Bumps [x]` and ends `from 1.0 to 1.1.` The command
below that writes the moves reads both forms. The item holds where the
lock uv writes is the head's, byte for byte, but for the `revision = N`
line at its top, whose number depends on the uv that wrote the lock.
Every other change in the lock, such as a version moved, a package
dropped, an extra emptied, a new requirement or a changed marker, is
then what uv makes of those moves. Run them with a uv the tree's
`[tool.uv]` `required-version` admits, where one is set: uv refuses any
other.

uv resolves what it adds or moves against the index as it is when the
commands run. Where a release came out after the bot wrote its lock,
the two locks can differ: the item then fails, and the human decides.

This writes the moves, one `--upgrade-package` argument a line. It takes
only a package name and a version from each line it reads, so the body
can pass `uv lock` no other argument:

```shell
n=<n>
repo=<owner>/<repo>
moves=<moves file>
```

```shell
gh pr view "${n:?}" --repo "${repo:?}" --json body --jq .body |
  uv run --no-project --python 3.15 python -c 'import re, sys
t = sys.stdin.read()
N, V = r"([A-Za-z0-9][A-Za-z0-9._-]*)", r"([A-Za-z0-9._+!-]+)"
m = re.findall(rf"^Updates `{N}` from \S+ to {V}$", t, re.M) + \
    re.findall(rf"^Bumps \[{N}\]\(\S*\) from \S+ to {V}\.$", t, re.M)
for n, v in sorted(set(m)):
    print(f"--upgrade-package={n}=={v}")' > "${moves:?}"
```

This prints each package the head's lock adds, by name, for the
approval's body (below):

```shell
clone=<clone dir>
base=<base>
git -C "${clone:?}" show "${base:?}:uv.lock" |
  uv run --no-project --python 3.15 python -c 'import sys, tomllib
b = {p["name"] for p in tomllib.loads(sys.stdin.read())["package"]}
h = {p["name"] for p in tomllib.load(open(sys.argv[1], "rb"))["package"]}
for n in sorted(h - b):
    print(n)' "${clone:?}/uv.lock"
```

```shell
clone=<clone dir>
base=<base>
```

```shell
git -C "${clone:?}" show "${base:?}:uv.lock" > "${clone:?}/uv.lock"
```

```shell
clone=<clone dir>
moves=<moves file>
```

```shell
env -C "${clone:?}" uv lock $(cat "${moves:?}")
```

This exits `0` where the lock is the head's, its `revision` line apart:

```shell
clone=<clone dir>
sha=<sha>
git -C "${clone:?}" cat-file -e "${sha:?}:uv.lock" &&
  git -C "${clone:?}" diff --quiet -I '^revision = [0-9]+$' -- uv.lock
```

Then the clone goes:

```shell
clone=<clone dir>
```

```shell
rm -rf "${clone:?}"
```

`local-review.md`'s *The verdict* says what a major move is. Where the
notes show a known problem, its item fails and the human decides (*Where
it is not obvious*).

**Where it is obvious, approve `<sha>`, pinned.** `gh pr review` cannot
pin a commit, so the call is the API's:

```shell
n=<n>
repo=<owner>/<repo>
sha=<sha>
body=<body file>
```

```shell
gh api "repos/${repo:?}/pulls/${n:?}/reviews" -f event=APPROVE \
  -f commit_id="${sha:?}" -F "body=@${body:?}"
```

The body is a one-line summary naming the head it approves, `<sha>`,
then one paragraph: the `CLEARED` it relies on and the rebase case; each
review on GitHub, its ACK as a link, or its absence with its reason,
during a 429 the 429 run as a link; that every check passed or was
skipped, the 429 run apart; each package *The reproduced lock* finds the
head's lock adds; for a major move, the dependency, hook or action and
the notes its `CLEARED` names; and what was not checked.

Then land it, pinned to the same `<sha>` (*Landing*).

**Read the approval back**:

```shell
n=<n>
repo=<owner>/<repo>
login=$(gh api user --jq .login)
gh pr view "${n:?}" --repo "${repo:?}" \
  --json headRefOid,reviewDecision,reviews |
  jq -r --arg l "${login:?}" '.headRefOid, .reviewDecision,
  ([.reviews[] | select(.state == "APPROVED" and .author.login == $l)]
  | last | .commit.oid // "none")'
```

It answers `<sha>`, `APPROVED` and `<sha>`: the last is the commit of
the human's own latest approval, since another reviewer's, CodeRabbit's
or another owner's, can be the last one given. Where the head moved, or
the decision is `CHANGES_REQUESTED`, decide again on the head. Where it
is otherwise not `APPROVED`, the ruleset asks for another approval.
Request it from an owner who is neither the human nor the author and
pushed no commit to the branch, and report whom it waits on. Where
`main` requires a code owner's review and the author is the only code
owner, no other approval meets it, and it lands only through a bypass of
the rule that imposes it. `main` requires that review where either `gh
api` call prints `true` (a 404 from the second is no classic
protection):

```shell
repo=<owner>/<repo>
gh api --paginate "repos/${repo:?}/rules/branches/main" \
  --jq '.[] | select(.type == "pull_request")
    | .parameters.require_code_owner_review | select(.)'
gh api "repos/${repo:?}/branches/main/protection" \
  --jq '.required_pull_request_reviews.require_code_owner_reviews'
```

GitHub reads the owners from the first of `.github/CODEOWNERS`,
`CODEOWNERS` and `docs/CODEOWNERS` it finds; this prints that file on
`main`, nothing where there is none, and the error, exiting `1`, where a
read fails other than with a 404:

```shell
(for p in .github/CODEOWNERS CODEOWNERS docs/CODEOWNERS; do
  u="repos/<owner>/<repo>/contents/$p?ref=main"
  e=$(gh api --silent "$u" 2>&1) &&
    { gh api -H 'Accept: application/vnd.github.raw' "$u"; exit; }
  case $e in *'(HTTP 404)'*) ;; *) echo "$e" >&2; exit 1 ;; esac
done)
```

This prints each ruleset over `main` that imposes the review, with each
of its bypass actors, or with `none`:

```shell
repo=<owner>/<repo>
(set -o pipefail
gh api --paginate "repos/${repo:?}/rules/branches/main" \
  --jq '.[] | select(.type == "pull_request"
    and .parameters.require_code_owner_review) | .ruleset_id' \
  | xargs -I{} gh api "repos/${repo:?}/rulesets/{}" \
    --jq '.id as $r | (.bypass_actors[]?
      | "\($r) \(.actor_type) \(.actor_id) \(.bypass_mode)")
      // "\($r) none"')
```

It waits on a `User` that every ruleset printed names: the author where
the author's id (`gh api users/<login> --jq .id`) is one, another
otherwise. Where classic protection imposes the review, no `User` is
named by every ruleset printed, or a read fails other than with those
404s, hold and ask the human (*Where it is not obvious*).

**Where it is not obvious, the human decides**, as one decision
(`every-session.md`'s *When the human has to decide*). Its context
also gives the head sha and each failed item with its measurement. The
alternatives are: approve, once the thread item holds; ask the author
for changes, naming them, where the session cannot push to the branch;
wait, naming on what or whom; close, where that is an option. Where
only the bot's quota fails the items, the human may run a Claude
review locally. Record it as a hold (`every-session.md`'s *When the
human has to decide*). On "approve", approve as above, with a body
saying it follows the human's decision. At night it is a deferred item
(`orchestration.md`'s *Night mode*).

### The human's own pull request

**Where the human is a bypass actor of an active ruleset, and is the
maintainer (`every-role.md`'s *Three roles the process names*) or runs
`--land` (*Landing*), the session lands it through the bypass, and
requests no owner's review.** It lands once every item above holds but
those on the author, the repository, the files in the list,
`pyproject.toml` and `uv.lock`, a bot's pins and a major move, as
*Landing* qualifies them, the bot's review and its check included or
absent as *The reviews on GitHub* allows. *Landing* gives the command.
`btclib-org/.github`'s `GOVERNANCE.md`, under *How a decision is made*,
decides which repositories give the maintainer the bypass. This command
prints the id of each user an active ruleset gives the bypass in
`pull_request` mode. The human is a bypass actor where it prints the id
`gh api user --jq .id` prints:

```shell
repo=<owner>/<repo>
(set -o pipefail
gh api --paginate "repos/${repo:?}/rulesets" --jq '.[].id' \
  | xargs -I{} gh api "repos/${repo:?}/rulesets/{}" \
    --jq 'select(.enforcement == "active") | .bypass_actors[]?
      | select(.actor_type == "User" and .bypass_mode == "pull_request")
      | .actor_id')
```

Otherwise, `--land` included, another owner decides and `--admin` is
never attempted. Once the same items hold, except the one a 429 fails:

- request the review of every owner but the human who has not approved
  `<sha>`. `btclib-org/.github`'s `GOVERNANCE.md` names the owners, and
  `gh api --paginate "orgs/btclib-org/members?role=admin" --jq
  '.[].login'` lists them:

  ```shell
  n=<n>
  repo=<owner>/<repo>
  login=<login>
  ```

  ```shell
  gh pr edit "${n:?}" --repo "${repo:?}" --add-reviewer "${login:?}"
  ```

- once an owner has approved `<sha>`, the approver merges it, or the
  session does on the human's word (*Merging*);
- report whom it waits on.

After a push, request the review again on the new head (*Landing*).

On a pull request that changes `claude-review.yml`, or a reusable
workflow that file calls by a local path, which the bot does not review
(*The reviews on GitHub*), `--land` does not apply. It lands through the
bypass only where the human is the maintainer and a bypass actor, as
above, and is otherwise merged as *Merging* says.

A pull request whose description says it breaks the live setup, in a
*Breaks* section as
[PR 175](https://github.com/btclib-org/ai-agents-process/pull/175)
has, is put to the human before it lands through the bypass.

## Outside contributors

While the pull request is open, no competing branch is opened for its
issue, which its assignees hold, as the tree's `CONTRIBUTING.md` says
in *Pull requests*. The reviewer reviews it against `REVIEWING.md`. Its
gates run in the sandbox of `writing.md`'s *The gates*, whoever runs
them, and so do the dedicated reviewer's inputs, which the session runs
there for it. Where `orchestration.md`'s *Where the other client is
unavailable* has the body record something, the comment that section
names records it instead.

**It is completed in place where `maintainerCanModify` is `true`**, with
every fix the approval needs, blocking findings and nits alike, as the
bullets below say. Otherwise the orchestrator delivers the findings on
the pull request, warmly and as `every-session.md`'s *What is posted on
a forge* says: the first line thanks them and names what holds the pull
request, what is right comes before what is missing, and a fix of a few
lines is a one-click suggestion. The session then waits. Where a branch
of ours must land first and touches their lines, the maintainer decides
the order, and the contributor is told on their pull request what moved
and how to resolve it. Completing it:

- **Add, never rewrite.** Their commits stay byte for byte. `main`
  comes in by a signed merge, not a rebase, run with hooks off as
  `writing.md`'s *The gates* says. The fixes are a signed commit of ours
  on top, signed off by us.
- **Push to their fork as a fast-forward only**: `git push <fork url>
  HEAD:refs/heads/<their branch>`, never with any `--force`. Before
  every push, `git ls-remote <fork url> refs/heads/<their branch>` must
  still answer the sha you built on; where it moved, they are working,
  and you stop and ask.
- **The same review and decision, then the squash of their pull
  request.** That keeps their authorship; a branch of ours
  cherry-picking them would leave their pull request closed rather than
  merged, and uncredited. Keep their title with the citation; the
  message says what the change does, corrects anything false in their
  commits, and ends with every `Signed-off-by:` line of the commits it
  squashes and a `Co-authored-by:` line for whoever finished it. The
  `Sign-off` job reads the pull request's commits, not the squash, so
  the message carries their trailers onto `main`. After the landing,
  `gh api repos/<owner>/<repo>/commits/<sha> --jq .author.login` is
  theirs.
- **Thank them in a comment of its own**: what their change does, what
  was added and why, in terms they can learn from, and the open issues
  they might take next.
- **The local copy of their branch goes** as `every-role.md`'s *Debris
  goes when its work ends* says.

Both thanks, the findings' first line and the comment of its own, bind
btclib-org only.

**Their sign-off is theirs to add, whether the session completes the
pull request or waits.** A commit of theirs without the trailer is not
ours to fix: a sign-off we add for them is not their attestation. Ask
them, with the findings, and before we push anything to their branch, to
run the command the `Sign-off` check's failure prints and force-push.
The ask warns of the closing and names the closing day the next
paragraph gives.

**A pull request still lacking a sign-off is closed on its closing
day**: the later of the day the tree's `CONTRIBUTING.md` gives in *Pull
requests*, which is what the contributor reads, and seven days after the
pull request's last reopen, so that a reopened pull request's author has
the week to push the trailers. The request the tree's day counts from is
the first comment on the pull request that asks for the trailer and
warns of the closing, by a maintainer, a session or a job; where none
does, it is the session's ask above. Such a comment can be a comment on
the pull request, the body of a review or a comment of a review, which
GitHub serves apart. These list each kind, every page read, with its
time, author and URL on one line and its body on the next, as a JSON
string, so that a body holding a line of that shape adds no entry. The
session reads them all and takes the earliest that asks and warns. A
comment of a review takes its review's time, since GitHub shows the
comments of a pending review only once it is submitted: the third
listing prints the review's id, and the second that review's
`submitted_at`:

```shell
n=<n>
repo=<owner>/<repo>
```

```shell
gh api --paginate "repos/${repo:?}/issues/${n:?}/comments" \
  --jq '.[] | "\(.created_at) \(.user.login) \(.html_url)
\(.body | @json)\n"'
```

```shell
gh api --paginate "repos/${repo:?}/pulls/${n:?}/reviews" \
  --jq '.[] | "\(.submitted_at) \(.user.login) \(.html_url) review \(.id)
\(.body | @json)\n"'
```

```shell
gh api --paginate "repos/${repo:?}/pulls/${n:?}/comments" \
  --jq '.[] | "review \(.pull_request_review_id) \(.user.login) \(.html_url)
\(.body | @json)\n"'
```

This prints the time of the last reopen, and nothing where the pull
request was never reopened:

```shell
gh api graphql -f owner="${repo%%/*}" -f name="${repo#*/}" -F n="${n:?}" \
  -f query='
  query($owner: String!, $name: String!, $n: Int!) {
    repository(owner: $owner, name: $name) {
      pullRequest(number: $n) {
        timelineItems(itemTypes: [REOPENED_EVENT], last: 1) {
          nodes { ... on ReopenedEvent { createdAt } }
        }
      }
    }
  }' --jq '.data.repository.pullRequest.timelineItems.nodes[].createdAt'
```

On the closing day, the session reads the head's commits: the `Sign-off`
check on the head, or, where it did not run, `writing.md`'s *Signed and
signed off*'s script on those commits. Where the check, or the script
where the check did not run, refuses a commit, the session closes the
pull request with a comment, from a file. The comment thanks them, names
the commits refused, links the request, and gives the commands the check
or the script printed. It points to `CONTRIBUTING.md`'s *Pull requests*
for how the pull request comes back, and says that a comment on each
issue it cites, posted next, says who holds that issue:

```shell
comment=<comment file>
```

```shell
gh pr close "${n:?}" --repo "${repo:?}" --comment "$(cat "${comment:?}")"
```

An issue is held by its assignees, as `CONTRIBUTING.md`'s *Pull
requests* says. The issues the pull request cites are those its
`closingIssuesReferences` lists, and any its title or body says it is
for. Each issue sits in the repository its reference names, which may
not be the pull request's: `<issue repo>` is that repository,
`<owner>/<repo>` for a bare `#N`. This prints each issue
`closingIssuesReferences` lists, with its repository:

```shell
gh pr view "${n:?}" --repo "${repo:?}" --json closingIssuesReferences \
  --jq '.closingIssuesReferences[]
    | "\(.repository.owner.login)/\(.repository.name) \(.number)"'
```

For each issue, the session removes the pull request's author from its
assignees:

```shell
irepo=<issue repo>
issue=<issue>
login=<author login>
```

```shell
gh issue edit "${issue:?}" --repo "${irepo:?}" --remove-assignee "${login:?}"
```

This then prints the issue's assignees:

```shell
gh api "repos/${irepo:?}/issues/${issue:?}" --jq '[.assignees[].login]'
```

Where it prints any login, the assignees it prints keep the issue. Where
it prints none, the session looks for the next taker: of the open pull
requests that cite the issue, have a pass of the `Sign-off` check that
counts on their head (*A pass counts only on a head*, below) and have
an author GitHub can assign to the issue, in any repository of the
organization, the same author's included, the one with the earliest
pass that counts. This lists the candidates:

```shell
gh search prs --owner btclib-org --state open "${issue:?} in:title,body" \
  --limit 100 --json url,author \
  --jq '.[] | "\(.author.login) \(.url)"'
```

The search matches the number as a word, so the session reads each
hit's title, body and `closingIssuesReferences`, and keeps the hits
that cite the issue, as `<issue repo>#<issue>`, by the issue's URL, or
as a bare `#<issue>` in `<issue repo>` itself. This prints when the
`Sign-off` check on a hit's head passed, and nothing where it did not or
where the pass does not count. Where a call fails it exits non-zero,
and no taker is chosen until it has exited `0` for each hit:

```shell
pr=<hit url>
```

```shell
info=$(gh pr view "${pr:?}" --json url,headRefOid,baseRefName \
  --jq '(.url | split("/")[3:5] | join("/")), .headRefOid, .baseRefName') &&
  { read -r prepo && read -r sha && read -r base; } <<< "$info" &&
  at=$(gh api --paginate "repos/${prepo:?}/commits/${sha:?}/check-runs" \
    --jq '.check_runs[] | select(.name | test("(^|/ )Sign-off$"))
      | select(.conclusion == "success") | .completed_at') &&
  if [ -n "$at" ]; then
    keep=$(gh api "repos/${prepo:?}/compare/${base:?}...${sha:?}" \
      --jq '(.files | length) < 300 and all(.files[];
        [.filename, .previous_filename // empty]
        | all(.[]; startswith(".github/workflows/") | not))') &&
      if [ "$keep" = true ]; then printf '%s\n' "$at"; fi
  fi
```

A hit that passes is ranked by its first pass that counts on any head it
had (*A pass counts only on a head*, below), so a pull request pushed
again after passing keeps its place. The block above reads the current
head alone. This prints the earliest time a `Sign-off` run passed on a
head that counts, read from every `pull_request` workflow run on the
hit's head branch, from a repository of its head owner, since it was
opened, and nothing where none did. Where a call fails it exits
non-zero, and no taker is chosen until it has exited `0` for each hit
that passes:

```shell
info=$(gh pr view "${pr:?}" \
  --json url,headRefName,headRepositoryOwner,createdAt,baseRefName \
  --jq '(.url | split("/")[3:5] | join("/")), .headRefName,
    .headRepositoryOwner.login, .createdAt, .baseRefName') &&
  { read -r prepo && read -r branch && read -r from && read -r since &&
    read -r base; } <<< "$info" &&
  ids=$(FROM=$from SINCE=$since gh api --paginate -X GET \
    "repos/${prepo:?}/actions/runs" -f event=pull_request \
    -f branch="${branch:?}" -F per_page=100 \
    --jq '.workflow_runs[] | select(.head_repository.owner.login == env.FROM
      and .created_at >= env.SINCE) | .check_suite_id') &&
  passes=$(while read -r id; do
    [ -z "$id" ] || gh api --paginate -X GET -f filter=all \
      "repos/${prepo:?}/check-suites/${id}/check-runs" \
      --jq '.check_runs[] | select(.name | test("(^|/ )Sign-off$"))
        | select(.conclusion == "success")
        | "\(.completed_at) \(.head_sha)"' || exit
  done <<< "$ids") &&
  times=$(while read -r at sha; do
    [ -z "$sha" ] || {
      keep=$(gh api "repos/${prepo:?}/compare/${base:?}...${sha}" \
        --jq '(.files | length) < 300 and all(.files[];
          [.filename, .previous_filename // empty]
          | all(.[]; startswith(".github/workflows/") | not))') || exit
      [ "$keep" != true ] || printf '%s\n' "$at"
    }
  done <<< "$passes") &&
  printf '%s' "$times" | sort | head -n 1
```

**A pass counts only on a head that changes no file under
`.github/workflows/`.** A fork's run uses the workflows of the pull
request's merge commit (*A fork's workflow runs can wait for approval*,
below), so a fork can change a workflow on one head until its
`Sign-off` job passes, then push an honest head over it. The fork names
the job and sets its result, so both blocks also read the files each
passing head changes, from GitHub's compare of the pull request's base
and that head, which reads a head no longer on the branch too. A renamed
file counts under both its names. GitHub caps the files one compare
lists
([*Compare two commits*](https://docs.github.com/en/rest/commits/commits#compare-two-commits)),
so a head whose list reaches the cap counts as changing a workflow. A
pass on such a head neither makes a hit a candidate nor gives it a
time.

The block matches the head's owner, not its repository: once a fork is
deleted, `gh pr view` gives the pull request no head repository, while
its runs still name it.

GitHub caps the runs one query returns
([*List workflow runs for a repository*](https://docs.github.com/en/rest/actions/workflow-runs#list-workflow-runs-for-a-repository)),
and returns them newest first, so a branch name with more `pull_request`
runs than the cap, from any repository, loses its oldest. The runs of
another pull request opened by the same owner from a branch of that name
count too, from the time this one was opened.

GitHub assigns an outside login only to an issue it has commented on, as
`CONTRIBUTING.md`'s *Pull requests* says. This exits `0` where a hit's
author can be assigned to the issue, and exits `1`, printing `User
cannot be assigned to this issue. (HTTP 404)`, where they cannot. Any
other failure, as another HTTP status or no answer, decides nothing, and
no taker is chosen until the call has given one of those two answers for
each hit's author:

```shell
author=<hit author login>
```

```shell
gh api --silent "repos/${irepo:?}/issues/${issue:?}/assignees/${author:?}"
```

The taker is the author of the hit with the earliest first pass among
those for whose author this call exits `0`. The session assigns them,
then reads the issue's assignees back as after the removal:

```shell
taker=<taker login>
```

```shell
gh issue edit "${issue:?}" --repo "${irepo:?}" --add-assignee "${taker:?}"
```

Where the call answers that `404` for every hit's author, the session
assigns no one, and the retry below applies.

**The retry.** Where no taker was assigned, the issue's comment asks
each hit's author who could not be assigned to comment on the issue. On
its next pass over one of their pull requests, the session reads the
issue's assignees as after the removal and, where they hold no login,
looks for the next taker again, as above, and assigns the one it finds.
An assignee is never displaced: once a taker is assigned, a hit that
passed earlier holds nothing, and its author's later comment changes
nothing.

The search returns at most 100 hits, and misses a pull request its index
does not hold yet. Where it finds no taker, the issue stays unassigned
and open to others, so a hit it missed costs that pull request's author
only the assignment, never the issue.

The issue then gets a comment from a file, posted after these edits. It
links the pull request, says it was closed for a missing sign-off, and
says who holds the issue: the assignees that remain, the taker just
assigned, or no one, in which case it is open to others and the comment
carries the retry's ask:

```shell
note=<issue comment file>
```

```shell
gh issue comment "${issue:?}" --repo "${irepo:?}" --body-file "${note:?}"
```

On the contributor's comment asking for a reopen, the session reopens
the pull request in the order `CONTRIBUTING.md`'s *Pull requests* gives.
Where another contributor has been assigned to an issue it cites
meanwhile, the human decides whether it is reopened:

```shell
gh pr reopen "${n:?}" --repo "${repo:?}"
```

Once its `Sign-off` check passes, read as above, the session reads the
assignees of each issue it cites as after the removal. Where they hold
any login, those assignees keep the issue. Otherwise the session looks
for the next taker as above, the reopened pull request among the hits,
and says on the issue who holds it, with a comment from a file as
above, which carries the retry's ask where no taker was assigned.

On a fork's pull request the bot's review does not run, and the
`CLEARED` that *The reviews on GitHub* asks for stands for its ACK.

Where the bot's review does not run on another of their pull requests,
as where `gh pr checks` shows no review, that review is absent (*The
reviews on GitHub*), and the approval is never obvious: it goes to the
human.

**A fork's workflow runs can wait for approval as `action_required`**,
as on PR btclib-org/btclib#2823. This prints the organization's
policy; under `first_time_contributors_new_to_github` only an account
new to GitHub waits:

```shell
gh api orgs/btclib-org/actions/permissions/fork-pr-contributor-approval \
  --jq .approval_policy
```

Under `pull_request`, a fork's run uses the workflows of the pull
request's merge commit, with a read-only `GITHUB_TOKEN` and no other
secret. The session approves the runs once it has read the diff whole
and every file the diff touches is one it can name: a Python module or
test under `src/` or `tests/`, `conftest.py` apart, or prose in
Markdown or reStructuredText, with no component of its path starting
with `.`, and no line of a workflow, an action or `pyproject.toml` of
the base branch names it, a line that is only a comment apart, and no
other open pull request has its head. It says so on the pull request.
Otherwise the human approves them, and the session tells the human
which step stopped it, and, where one did, the file.

Anything else can change what the CI runs: a workflow, a script, test
data, a file a tool reads for what to run or install (`pyproject.toml`,
`uv.lock`, `conftest.py`, `pytest.ini`, `.coveragerc`, Sphinx's
`conf.py`, and more), which the reusable workflows of btclib-org/.github
read without the caller naming them. A list of such files is never
complete, so the check names what passes rather than what stops. A name
matched after code on a line stops it too, a trailing comment included:
the check errs on the side of the human.

These steps, in order, show that every file the diff touches passes:

1. This prints the head, `<head>`, and the base branch, `<base>`. The
   files endpoint takes no sha, so the last step reads them again:

   ```shell
   n=<n>
   repo=<owner>/<repo>
   gh pr view "${n:?}" --repo "${repo:?}" \
     --json headRefOid,baseRefName --jq '.headRefOid, .baseRefName'
   ```

1. This prints a number below 3000. The files endpoint returns at most
   3000 files, so a larger pull request can hide a file that does not
   pass:

   ```shell
   n=<n>
   repo=<owner>/<repo>
   gh pr view "${n:?}" --repo "${repo:?}" \
     --json changedFiles --jq .changedFiles
   ```

1. This exits `0` and writes a file that is not empty.
   `previous_filename` brings in the old name of a renamed file:

   ```shell
   n=<n>
   repo=<owner>/<repo>
   files=<files file>
   ```

   ```shell
   gh api --paginate "repos/${repo:?}/pulls/${n:?}/files" \
     --jq '.[] | .filename, (.previous_filename // empty)' > "${files:?}"
   ```

1. These exit `1`, printing nothing: the first, every file outside the
   names that pass, a path with a component starting with `.` among
   them; the second, a `conftest.py`. One that exits `2` or more could
   not read `<files file>`, and the runs are the human's:

   ```shell
   grep -v -E -e '^(src|tests)/([^./][^/]*/)*[^./][^/]*\.py$' \
     -e '^([^./][^/]*/)*[^./][^/]*\.(md|rst)$' <files file>
   grep -E '(^|/)conftest\.py$' <files file>
   ```

1. No line of a workflow, an action or `pyproject.toml` of the base
   branch names a file the diff touches, a line that is only a comment
   apart. A search or a filter that exits `2` or more failed, and the
   runs are the human's: its silence is no pass. `<hits file>` is a
   path that does not exist before the search, so a redirect that
   fails, which exits `1` without searching, leaves no file, and the
   filter exits `2`.
   The search reads `<base sha>`, the base's commit as GitHub has it,
   not a ref: another session fetching into the same checkout moves
   `FETCH_HEAD` and the remote-tracking refs, never a sha. Where the
   checkout cannot read that commit, the search exits `128`. `git grep`
   reads the commit, not the files on disk, so any checkout of the
   repository does; `git -C` reads a relative `<files file>` from the
   checkout, so it is an absolute path; `-F` takes each path as a
   string, not a pattern, and `-h` leaves the line alone for the
   comment filter.

   This prints `<base sha>`:

   ```shell
   repo=<owner>/<repo>
   base=<base>
   gh api "repos/${repo:?}/commits/${base:?}" --jq .sha
   ```

   This exits `0`:

   ```shell
   checkout=<checkout>
   base=<base>
   ```

   ```shell
   git -C "${checkout:?}" fetch -q origin "${base:?}"
   ```

   This exits `0` or `1`:

   ```shell
   checkout=<checkout>
   files=<files file>
   sha=<base sha>
   hits=<hits file>
   ```

   ```shell
   git -C "${checkout:?}" grep -h -F -f "${files:?}" "${sha:?}" -- \
     .github/workflows/ .github/actions/ pyproject.toml > "${hits:?}"
   ```

   This exits `1`, printing nothing:

   ```shell
   grep -v -E '^[[:space:]]*#' <hits file>
   ```

1. The first step's command prints `<head>` and `<base>` again.

A run waiting on `<head>` is this pull request's only where no other
open pull request has that head: one opened from the same branch
against another base runs the same head on another diff. This prints
`1`, or the runs are the human's:

```shell
repo=<owner>/<repo>
gh pr list --repo "${repo:?}" --state open --limit 200 \
  --json number,headRefOid \
  --jq '[.[] | select(.headRefOid == "<head>")] | length'
```

This lists the runs waiting on `<head>`, every page read, and the POST
to a run's `approve` approves one. It leaves out runs started by
`pull_request_review_comment`, as a review bot's comment starts
`claude-review` on a fork's pull request: GitHub refuses to approve them
with HTTP 403, and the review skips a fork's pull request anyway (*The
reviews on GitHub*). `head_sha` matches only the full sha the first step
prints; an abbreviated one lists nothing:

```shell
repo=<owner>/<repo>
head=<head>
gh api --paginate -X GET "repos/${repo:?}/actions/runs" \
  -f head_sha="${head:?}" -f status=action_required -F per_page=100 \
  --jq '.workflow_runs[] | select(.event != "pull_request_review_comment")
    | {id, name, event}'
```

```shell
repo=<owner>/<repo>
id=<id>
```

```shell
gh api -X POST "repos/${repo:?}/actions/runs/${id:?}/approve"
```

## Merging

**No session and no workflow arms auto-merge.** An armed pull request
merges at a moment nobody reads: a push makes its ACKs stale, a review
with findings can arrive after it was armed, one whose base is not
protected merges at once, and an approving bot could fill the count of
approvals. A pull request found armed is disarmed at once, and the human
is told. This lists the armed ones, and `gh pr merge --disable-auto`
disarms one:

```shell
repo=<owner>/<repo>
gh pr list --repo "${repo:?}" --limit 200 \
  --json number,autoMergeRequest \
  --jq '.[] | select(.autoMergeRequest) | .number'
```

```shell
n=<n>
repo=<owner>/<repo>
```

```shell
gh pr merge "${n:?}" --repo "${repo:?}" --disable-auto
```

**The merge is an explicit act after the approval**: the approver's own,
or a session's on the human's word, which is his approval or *Landing*'s
`--land`. Whoever merges reads these at that moment, on the head, and
merges pinned to it:

- an approval that counts names the head: the read of the reviews below
  prints `approved`, the head and the approvers;
- every required check passed or was skipped;
- the rule of *The reviews on GitHub* holds on the head;
- no review thread is unresolved, read as *What was raised* says
  ([ISS 152](https://github.com/btclib-org/ai-agents-process/issues/152)).

An approval counts where it is the latest review of a person, not a bot,
who is not the author, and names the head, and where GitHub's
`reviewDecision` reads `APPROVED`, which holds a code owner's review
where the tree requires one. *The decision*'s read-back reads only an
approval the session gave; this reads whoever approved. It prints
`approved <head> <logins>`, `not-approved <head> <decision>`, or `error`
where a read failed:

```shell
repo=<owner>/<repo>
n=<n>
: "${repo:?}" "${n:?}"
{ gh pr view "${n:?}" --repo "${repo:?}" \
    --json headRefOid,reviewDecision,author \
    --jq '"pr \(.headRefOid) \(.reviewDecision) \(.author.login)"' ||
    echo read-failed
  gh api --paginate "repos/${repo:?}/pulls/${n:?}/reviews?per_page=100" \
    --jq '.[] | "review \(.state) \(.commit_id) \(.user.type)"
      + " \(.user.login)"' || echo read-failed
} | jq -Rrs '
  . as $in | (split("\n") | map(split(" "))) as $l
  | ([$l[] | select(.[0] == "pr")] | first) as $p
  | [$l[] | select(.[0] == "review")
    | select(.[1] | IN("COMMENTED", "PENDING") | not)]
  | group_by(.[4]) | map(last)
  | [.[] | select(.[1] == "APPROVED" and .[2] == $p[1] and .[3] == "User"
      and .[4] != $p[3]) | .[4]] as $a
  | if ($in | test("read-failed")) or $p == null then "error"
    elif $p[2] == "APPROVED" and ($a | length) > 0
      then "approved \($p[1]) \($a | join(","))"
    else "not-approved \($p[1]) \($p[2])" end'
```

A landing through the bypass (*The human's own pull request*) reads the
same, but for the approval. *The reviews on GitHub* says that none of
them is a required check, so this read is what keeps a merge from one in
findings. *Landing* gives the command, with squash, the only merge
method (`CONTRIBUTING.md`'s *Landing it*).

**The required checks are the branch protection's contexts.** The read
of `required_status_checks` writes them, and `<required file>` must not
be empty. `gh pr checks` then writes each check that passed or was
skipped on the head:

```shell
repo=<owner>/<repo>
required=<required file>
```

```shell
gh api "repos/${repo:?}/branches/main/protection/required_status_checks" \
  --jq '.contexts[]' > "${required:?}"
```

Where it answers `Branch not protected` (HTTP 404) and exits `1`, `main`
has no protection yet: that is not an empty list, and the pull request
is not merged but held, as *The decision* says.

```shell
n=<n>
repo=<owner>/<repo>
green=<green file>
```

```shell
gh pr checks "${n:?}" --repo "${repo:?}" --json name,bucket --jq '.[]
  | select(.bucket == "pass" or .bucket == "skipping") | .name' \
  > "${green:?}"
```

*Rebase and CI*'s command that writes `<red file>` exits `0`. The first
`grep` below prints each required check that has not passed or been
skipped, and the second each one written to `<red file>`. Each exits `1`
where it prints nothing:

```shell
green=<green file>
red=<red file>
required=<required file>
grep -vxFf "${green:?}" "${required:?}"
grep -xFf "${red:?}" "${required:?}"
```

`gh pr checks --required` is not enough: it omits a required check that
has not reported yet.

## Landing

- **Read `main`'s latest push runs** when choosing which pull requests
  to work, and after each landing: `gh run list --repo <owner>/<repo>
  --branch main --event push`. `main` is red where a required check
  failed in the latest run of its workflow. A cancelled check is not a
  failure, and a check that only reports does not count. While `main` is
  red, its repair is the first work, and other pull requests are still
  approved and merged (`CONTRIBUTING.md`'s *Landing it*).
- **`release-hold` holds merges as a publishing tree's `RELEASING.md`
  says in *Release to PyPI*.** Before the session merges a pull request,
  these read the repository and its open or merged pull requests
  carrying the label:

  ```shell
  repo=<owner>/<repo>
  gh api "repos/${repo:?}" --jq .full_name
  ```

  ```shell
  gh api --paginate \
    'repos/<owner>/<repo>/issues?labels=release-hold&state=all&per_page=100' \
    --jq '.[] | select(.pull_request)
      | select(.state == "open" or .pull_request.merged_at != null)
      | "\(.number) \(.state) \(.pull_request.merged_at // "unmerged")"'
  ```

  The first must print `<owner>/<repo>`. The second prints one line per
  hold: the pull request's number, its state, and when it merged or
  `unmerged`. Where it lists a pull request other than the one at hand,
  the one at hand waits until it lists no other, but for the exceptions
  that step gives. Another name from the first, or a nonzero exit of
  either, is an error, and the merge waits until both answer. The read
  and the merge are two calls, and none of the [rules a GitHub ruleset
  offers][rulesets] reads a label, so a label put on between them does
  not stop the merge. That step checks once more, just before the
  release merges, that `main` has not moved. This narrows the gap and
  does not close it, since that check and the release's merge are two
  calls too. The label records the wait, and the waiting pull request
  takes no comment of its own.
- **What gates a merge on GitHub** is the repository's own
  `REPOSITORY.md`, read from `origin/main`: typically an approval from
  somebody other than the author, every review thread resolved, and the
  required status checks. The bot's ACK is a comment, not an approval. A
  push dismisses an approval already given.
- **Where `gh pr merge` refuses, or an approved pull request stays
  `BLOCKED`** (`gh pr view <n> --repo <owner>/<repo> --json
  mergeStateStatus`), read its threads first, with *What was raised*'s
  query, then its checks. Do not explain a block by a ruleset option you
  have not read.
- **Before several pull requests land in one repository, test their
  merge.** CI tested each against the `main` of its own run, and `main`
  does not ask a head to be up to date with it (`CONTRIBUTING.md`'s
  *Landing it*), so two green pull requests can turn `main` red. The set
  is the pull requests about to be merged, and the test comes before the
  first of them is.

  Every run of the test starts here, each repeat below included, because
  fetching a pull request's ref leaves `origin/main` where it was:

  ```shell
  checkout=<checkout>
  ```

  ```shell
  git -C "${checkout:?}" fetch origin
  ```

  The fetch of `refs/pull/<n>/head` is run for each pull request. `<main
  sha>` is the `origin/main` that the fetch of origin above left, pinned
  (`every-role.md`'s *How you establish a fact*), and `<the heads>` are
  their `headRefOid`s, a space between each two:

  ```shell
  checkout=<checkout>
  n=<n>
  ```

  ```shell
  git -C "${checkout:?}" fetch origin "refs/pull/${n:?}/head"
  ```

  ```shell
  checkout=<checkout>
  wt=<wt>
  main=<main sha>
  ```

  ```shell
  git -C "${checkout:?}" worktree add --detach "${wt:?}" "${main:?}"
  ```

  ```shell
  wt=<wt>
  set -- <the heads>
  ```

  ```shell
  git -C "${wt:?}" -c core.hooksPath=/dev/null \
    merge --no-ff --no-commit "$@"
  ```

  With several heads `git merge` ignores `merge=union`, so it needs no
  `merge.union.driver`, and `core.hooksPath` keeps hooks from running on
  what the heads hold. Exit `0` leaves the merge staged and uncommitted.
  The tree's gates run on it whole, as `CONTRIBUTING.md`'s last section
  gives them, under the gate lock with `gate_wait`, and in the sandbox
  of `writing.md`'s *The gates* where any head is an outside
  contributor's. A push to one of the pull requests voids the run.

  **Where the merge exits non-zero, `merge-tree` says why.** This
  exits `1` where `<a>` and `<b>` conflict. It runs on `<main sha>` with
  each head, and on each pair of heads:

  ```shell
  wt=<wt>
  a=<a>
  b=<b>
  git -C "${wt:?}" -c merge.union.driver=false \
    merge-tree --write-tree --name-only "${a:?}" "${b:?}"
  ```

  A head that conflicts with `main` leaves the set and is rebased now.
  Of a pair that conflicts, the repair of a red `main` lands first, then
  the one approved on its head, since a push dismisses that approval,
  then the lower number. The other of the pair leaves the set and is
  rebased once the first has landed. Each rebase goes as
  `orchestration.md`'s *A rebase and the clearance* says. Where a head
  is an outside contributor's or the agent's, `main` comes in by its
  merge, not a rebase (*Rebase and CI*). Where it is an outside
  contributor's, *Outside contributors* says who decides the order.

  Where every run exits `0`, the octopus failed on its own, as it does
  on a file one head renames and another edits. Of the heads that change
  the path its `ERROR:` line names, the last in that order leaves the
  set, and is tested again once the others have landed.

  A head that leaves the set is not merged, and the test runs again on
  what remains. With one head left `git merge` applies `merge=union`, so
  the `merge-tree` of `<main sha>` with that head runs as well.

  **A gate red on the merge and green on `main`** is a clash no merge
  shows. The pull request it names gets the fix, in a new commit through
  `local-review.md`'s *The rounds*, and the test runs again. A gate red
  on `main` too is `main`'s, and *Landing*'s first bullet holds. That
  red can hide a clash on that gate.

  Whatever the outcome, `git -C <wt> merge --abort` ends the merge. It
  exits `128` where an octopus stopped before its last head and left
  nothing to abort. The worktree then goes (`every-role.md`'s *Debris
  goes when its work ends*). Where a fixer left changes, the abort can
  exit `128` too, and the worktree goes with `--force`. Where any head
  is an outside contributor's and a gate has run, no abort runs, and the
  worktree goes with `git -C <checkout> worktree remove --force <wt>`
  (`writing.md`'s *The gates*).

  The test covers those heads on that `main`, and nothing that lands
  from outside the set afterwards.

- **Squash, pinned to the head, once *Merging* holds.** The branch
  carries several commits once review has added any, so the subject and
  the message are written, not inherited:

  ```shell
  n=<n>
  repo=<owner>/<repo>
  head=<the head that lands>
  message=<message>
  ```

  ```shell
  gh pr merge "${n:?}" --repo "${repo:?}" --squash \
    --match-head-commit "${head:?}" \
    --subject "<title> (closes #<issue>) (#${n:?})" --body-file "${message:?}"
  ```

  The subject is the pull request's title with its citation
  (`writing.md`'s *Citations and closing keywords*) and `(#<n>)`, except
  for a batch of ports (`/btclib-iss`'s *Ports of the standard*);
  `--subject` replaces the whole subject. The message says what the
  change does, and keeps every `Signed-off-by:` and `Co-authored-by:`
  line of the commits it squashes. A finding that lives only in the
  commit message is fixed here, with no new round.

  Never land through the bypass (`--admin`, or any other route to it)
  except where *The human's own pull request* says. It merges with no
  approval, even with required checks red. It lands with this, in place
  of the `gh pr merge` above without `--admin`:

  ```shell
  n=<n>
  repo=<owner>/<repo>
  head=<the head that lands>
  message=<message>
  ```

  ```shell
  gh pr merge "${n:?}" --repo "${repo:?}" --squash --admin \
    --match-head-commit "${head:?}" \
    --subject "<title> (closes #<issue>) (#${n:?})" --body-file "${message:?}"
  ```

  **`--land` instructs it**, for the pull requests named with it, or
  opened by `/btclib-iss` for the issues named with it, and no others.
  The human's words in the session, naming the pull requests, count
  too. The bypass then lands only the human's own pull request, where
  and once *The human's own pull request* says. A check that only
  reports and is red on `main` too does not hold it, and is named in
  the report.

- **Where `main` has moved past the sha the verdict read the prose on**,
  `orchestration.md`'s *A rebase and the clearance* says who re-reads
  the prose before the branch lands, and what review a sentence found
  false there needs.
- **The pin is the head as last pushed**, not the sha a verdict named.
- **A stacked pull request lands like any other**: once its base has
  landed, it is rebased onto `main` as `CONTRIBUTING.md`'s *One subject,
  opened as soon as it is written* says, gated, decided again on the new
  head (*The decision*), and merged as *Merging* says.
- **Check what landed, once it has.** Repeat `gh pr view <n> --repo
  <owner>/<repo> --json state,mergeCommit --jq '.state,
  .mergeCommit.oid'` until it answers `MERGED`, and `<sha>` is that oid.
  Where it stays `OPEN`, the merge did not happen: report it. Once it is
  `MERGED`, `gh api repos/<owner>/<repo>/commits/<sha> --jq
  .commit.verification` is `verified: true`. What follows waits for
  this.

  Then wait for `main`'s workflow runs on `<sha>`, with *Rebase and
  CI*'s block and this test in place of its own. A workflow run is
  completed only once all its jobs are, including the jobs that wait on
  others and have no check run before they start:

  ```shell
  [ "$(gh api --paginate \
    "repos/<owner>/<repo>/actions/runs?head_sha=<sha>&event=push&per_page=100" \
    --jq '.workflow_runs[].status' | sort -u)" = completed ]
  ```

  That test also fails while no run has started. This prints how many
  `push` runs have started on `<sha>`:

  ```shell
  gh api "repos/<owner>/<repo>/actions/runs?head_sha=<sha>&event=push" \
    --jq .total_count
  ```

  **Where it still prints `0` once 10 minutes have passed since the
  merge**, the `mergedAt` that `gh pr view <n> --json mergedAt` prints,
  the merge fired none of GitHub's post-merge steps, and the session
  stops the loop. On PR btclib-org/bitcoin-core-rpc#797 the merge call
  answered HTTP 502 and `gh pr view --json state` then read `MERGED`,
  merge commit c777e11d. No `push` run started on it,
  ISS btclib-org/bitcoin-core-rpc#796, which the pull request declared
  closed, stayed open, and the head branch stayed though
  `delete_branch_on_merge` is `true`.

  Once the wait has ended, each issue the pull request declared closed
  is closed. Where the merge fired no post-merge steps, the session
  closes each one still open by hand, `<issue repo>` being the
  repository the reference names, `<owner>/<repo>` for a bare `#N`, and
  `<issue>` its number:

  ```shell
  repo=<owner>/<repo>
  n=<n>
  sha=<sha>
  irepo=<issue repo>
  issue=<issue>
  ```

  ```shell
  c="Closed by ${sha:?} (PR ${repo:?}#${n:?}), which fired no post-merge steps."
  gh issue close "${issue:?}" --repo "${irepo:?}" --reason completed \
    --comment "${c:?}"
  ```

  In that case only, it then dispatches on `main` each workflow that a
  push to `main` runs and that takes a dispatch, and names in the report
  each that a push to `main` runs and that takes none, which then never
  ran on `<sha>`. A workflow a push to `main` does not run is left
  alone, as one that runs only on a tag or a dispatch, a release's among
  them. This reads the `on:` of each workflow on `origin/main`, after
  `git fetch origin` in `<checkout>`, a checkout of the repository, and
  prints `dispatch` or `name` before each file it keeps. A workflow whose
  dispatch has a required input with no default is named, since a
  dispatch with no inputs cannot start it:

  ```shell
  checkout=<checkout>
  uv run --isolated --no-config --no-project --python 3.15 \
    --with pyyaml==6.0.3 python -I -c '
  import fnmatch, subprocess, sys, yaml
  def git(*a):
      return subprocess.run(["git", "-C", sys.argv[1], *a], check=True,
                            capture_output=True, text=True).stdout
  def main_in(bs):
      r = False
      for b in [bs] if isinstance(bs, str) else bs:
          if fnmatch.fnmatch("main", b.lstrip("!")):
              r = not b.startswith("!")
      return r
  w = ".github/workflows/"
  for f in git("ls-tree", "--name-only", "origin/main:" + w).split():
      if not f.endswith((".yml", ".yaml")):
          continue
      d = yaml.safe_load(git("show", "origin/main:" + w + f))
      on = d.get("on", d.get(True)) or {}
      on = {on: None} if isinstance(on, str) else on
      on = dict.fromkeys(on) if isinstance(on, list) else on
      if "push" not in on:
          continue
      p = on["push"] or {}
      if "branches" in p:
          runs = main_in(p["branches"])
      elif "branches-ignore" in p:
          runs = not main_in(p["branches-ignore"])
      else:
          runs = not ("tags" in p or "tags-ignore" in p)
      i = (on.get("workflow_dispatch") or {}).get("inputs") or {}
      need = any((x or {}).get("required") and "default" not in (x or {})
                 for x in i.values())
      v = "dispatch " if "workflow_dispatch" in on and not need else "name "
      if runs:
          print(v + f)' "${checkout:?}"
  ```

  Where no file was printed with `dispatch`, the time, the dispatch, the
  wait and the listing below are skipped, and the report names the files
  printed with `name`.

  Before the first dispatch the session notes the time, `<t>`:

  ```shell
  date -u +%Y-%m-%dT%H:%M:%SZ
  ```

  Each dispatch is its own call, `<file>` being a file printed with
  `dispatch`:

  ```shell
  repo=<owner>/<repo>
  file=<file>
  ```

  ```shell
  gh workflow run "${file:?}" --repo "${repo:?}" --ref main
  ```

  Then *Rebase and CI*'s block runs with this test in place of its own,
  `<files>` being the files dispatched, separated by spaces. It passes
  once each of them has a run created since `<t>`, and each such run has
  completed. Runs of other workflows are not read:

  ```shell
  repo=<owner>/<repo>
  t=<t>
  files=<files>
  q="event=workflow_dispatch&created=>=${t:?}&per_page=100"
  gh api --paginate "repos/${repo:?}/actions/runs?${q:?}" \
    --jq '.workflow_runs[] | .path + " " + .status' |
    awk -v f="${files:?}" 'BEGIN {k = split(f, a, " ")
        for (i = 1; i <= k; i++) want[".github/workflows/" a[i]]}
      ($(1) in want) {seen[$(1)]; if ($(2) != "completed") w = 1}
      END {n = 0; for (x in seen) n++; exit !(n == k && !w)}'
  ```

  A dispatched run runs on `main`'s tip when it starts, which may have
  moved past `<sha>`. This lists the runs of the files dispatched, each
  with its conclusion and the sha it ran on, and the report names each
  sha that is not `<sha>`:

  ```shell
  repo=<owner>/<repo>
  t=<t>
  files=<files>
  q="event=workflow_dispatch&created=>=${t:?}&per_page=100"
  gh api --paginate "repos/${repo:?}/actions/runs?${q:?}" \
    --jq '.workflow_runs[] | [.path, .conclusion, .head_sha] | @tsv' |
    awk -v f="${files:?}" 'BEGIN {k = split(f, a, " ")
        for (i = 1; i <= k; i++) want[".github/workflows/" a[i]]}
      ($(1) in want)'
  ```

  The head branch is left to the human and named in the report:
  deleting a remote branch is hard to undo.

  Then the session sweeps the pull request's `<work>` where
  `every-role.md`'s *Debris goes when its work ends* says.

  Then run this section's first bullet again: where the merge turned
  `main` red, its repair comes first.

- **A landing in `btclib-org/ai-agents-process` brings its primary
  checkout forward at once**, by the shared fast-forward. Where that
  checkout is the clone `$PROCESS` names, a session that starts reads
  the process through it, and reads the old one until then. A session
  already running re-reads what changed as `orchestration.md`'s *The
  process is re-read when `main` changes it* says. Then read a landed
  line back where sessions read it: under `$PROCESS`, or through the
  link of the skill or agent it changed.
- **The collateral goes back now** (`orchestration.md`'s *Closing
  collateral*), before anything new starts.
- **Remove the worktrees and the local branches** — yours, the branch
  the writer handed over among them, once the writer has removed its
  worktree (`every-role.md`'s *Debris goes when its work ends*).

Then `orchestration.md`'s *Wrap-up*.

[dependabot-rebase]: https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/manage-dependabot-prs#allowing-dependabot-to-rebase-and-force-push-over-extra-commits
[rulesets]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
