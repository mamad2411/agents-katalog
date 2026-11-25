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

**First note where the process stands**, before reading it: the
session keeps `$PROCESS`'s `HEAD` in a directory of its scratchpad, for
the shared *The process is re-read when `main` changes it*.
`echo "$PROCESS"` prints the clone's path.

```shell
scratchpad=<the session's scratchpad>
mkdir -p "${scratchpad:?}/orchestrator"
```

```shell
scratchpad=<the session's scratchpad>
git -C "${PROCESS:?}" rev-parse HEAD > "${scratchpad:?}/orchestrator/process.sha"
```

The client loaded this file before that note, so the session reads it
again, whole and once, from `$PROCESS/skills/btclib-pr/SKILL.md`.

**Then read `$PROCESS/process/btclib-common.md`, whole.** Its opening
says what it holds and what this file holds. What the session writes,
and this file, follow its *Write plainly*.

The shared *Where you work* says how the repository is named.

**Which sections are yours**, beyond the shared file's map:

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
requests gives their diff balance (the shared *How an issue and a pull
request are named*):

```shell
gh pr list --repo <owner>/<repo> --state open --limit 200 \
  --json number,additions,deletions,changedFiles
```

**Before the table, start the outside contributors' CI.** For every
pull request of an outside contributor (*Whose pull request it is*)
whose head has runs waiting as `action_required`, the session reads
the diff and approves those runs where *Outside contributors* allows
it. A pull request whose diff fails *Outside contributors*' check is
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
- bots';
- the rest: by day, listed and not worked.

Each row is a `PR` link with its diff balance (the shared *How an issue
and a pull request are named*) and what it waits on. A draft is listed
and not worked. Then put one decision (the shared *When the human has
to decide*): which to work, and in what order, the recommended order
first with its reason. In a repository whose `main` is red, its repair
comes first (*Landing*'s first bullet). Outside contributors' pull
requests come next, oldest first: their author waits on us, and a reply
that comes days late can lose a contributor.

**At night, no decision is put: every pull request that is not a draft
is worked** up to the approval, in the recommended order, a red `main`'s
repair first and outside contributors' pull requests next: review
rounds, rebase and CI, every item of *What was raised* answered. Each
is worked as *Whose pull request it is* says for its case, and goes
on to *The decision*, or to *The human's own pull request*. One whose
approval is not obvious ends as a deferred item (*Where it is not
obvious*), never as "not worked". Where the session cannot push to
another person's branch, its findings are posted as *Another person's
branch* says, and the deferred item names the author
as what it waits on.

## Whose pull request it is

```shell
gh api user --jq .login
```

```shell
gh pr view <n> --repo <owner>/<repo> --json author,state,isDraft,\
isCrossRepository,maintainerCanModify,headRefName,headRefOid,baseRefName
```

Then the shared *Before starting*, on the pull request. Which case it
is:

- **The human's.** The session works it as its author, and ends it at
  *The human's own pull request*.
- **Another person's, on a branch of the repository.** The session
  works it as its reviewer, and changes it as *Another person's branch*
  says.
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
  `@dependabot recreate` drops the commit, which is then made again.
- **An outside contributor's**: *Outside contributors*.

## What was raised

Collect everything said on the pull request, from the API. Paginate
where a page comes back full.

- **Reviews**, each with its state, author, body and the commit it
  names: `gh pr view <n> --repo <owner>/<repo> --json reviews`. The
  bot's review from `claude-review.yml` is one of them.
- **Review threads**, inline, with whether each is resolved:

  ```shell
  gh api graphql --paginate -F owner=<owner> -F repo=<repo> -F n=<n> \
    -f query='
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

## Answering it

**Each item is re-measured first** (the shared *Orchestration*), then
answered one of three ways:

- **accept**: fixed in a new signed commit on top (the shared
  *Committing and rebasing*).
- **decline**: with the measurement that refutes it.
- **decision**: a choice the tree does not settle — design, scope, a
  reserved decision. It goes to the human or the maintainer, as the
  shared *When the human has to decide* says.

**A bot's finding, the review bot's or CodeRabbit's, takes the first of
these routes that fits**, measured on the head, unless it needs a
decision:

- **declined** where it does not hold: it needs a condition the text
  already rules out, the sentence it calls false is true where the text
  applies it and leads no reader to a wrong step, or it is a matter of
  taste (`REVIEWING.md`'s *The standard an ack is given against*).
- **accepted** where it is the branch's own: a defect or a false
  sentence its diff or its pull request body adds, or anything else the
  shared *Collateral* counts as the branch's subject (the shared *A pull
  request's rounds* says how a fix to the branch is reviewed). A
  sentence of the body is weighed as the shared *Which prose is worth a
  round* says, and is fixed by editing the body, which the reply names.
- **filed** where it is older than the branch, holding on the file at
  the merge base too, and the branch does not make it materially worse:
  it goes where the shared *Collateral* says, and the reply names the
  issue where one is filed. A line the branch rewrote can carry an older
  limit, so the case is read on the base's file, not the line looked for
  in the diff. The first command prints `<base>`, the merge base with
  the pull request's base branch, `baseRefName` (*Whose pull request it
  is*), and the second the file there. `<path>` is the file's path at
  `<base>`, the old one where `git diff --name-status -M <base> <head>`
  shows a rename:

  ```shell
  git -C <wt> merge-base origin/<baseRefName> <head>
  ```

  ```shell
  git -C <wt> show <base>:<path>
  ```

**Every inline `suggestion` is applied in the worktree or declined with
its measurement.** It is not applied with GitHub's button, so that the
gates run on it.

**Every thread gets a reply, and is then resolved.** An accepted one
names the commit that fixes it; a declined one carries its measurement.
A thread waiting on a decision or on the author is replied to and
resolved once that arrives. The reply meets the shared *What is posted
on a forge*. Write the reply to a file of your own, then:

```shell
gh api graphql -F t=<thread id> -F b=@<reply file> -f query='
  mutation($t: ID!, $b: String!) {
    addPullRequestReviewThreadReply(
      input: {pullRequestReviewThreadId: $t, body: $b}) { comment { url } }
  }'
```

```shell
gh api graphql -F t=<thread id> -f query='
  mutation($t: ID!) {
    resolveReviewThread(input: {threadId: $t}) { thread { isResolved } }
  }'
```

A review or comment outside a thread is answered in one comment on the
pull request, which meets the shared *What is posted on a forge*.

### Another person's branch

**Where the session can push to the pull request's branch, it makes
every fix the approval needs itself**, blocking findings and nits
alike: every item is answered as *Answering it* says, with no split
between minor and substantial changes.

Before pushing, the session claims the branch (the shared *A claim holds
a pull request's branch*) and pushes with the lease of the shared
*Committing and rebasing*, on the sha it built on. Where the branch
moved, they are working: stop and ask.

Where the session has no write access to the branch, the findings are
posted to the author as a review comment, and the pull request waits on
them.

## Rebase and CI

- **The reviewer reads the delta** from the sha it last read. A rebase
  goes to a reviewer only where the shared *A rebase and the clearance*
  sends it. A fresh reviewer's first read is the whole diff from its
  parent.
- **A pull request is rebased onto the default branch only where
  `CONTRIBUTING.md`'s *Landing it* says, or for a retarget.** An outside
  contributor's branch is never rebased: *Outside contributors* brings
  `main` in by a merge.
- **After a rebase or a merge of `main`, run the gates and push**; an
  armed pull request is disarmed first (*Arming auto-merge*). Ask the
  merge the forge will compute, locally:
  `git -C <wt> -c merge.union.driver=false merge-tree origin/main
  <branch>` exits `1` where GitHub will refuse. `gh pr view --json
  mergeable` is a cached value.
- **Wait for the checks on the head just pushed**, in the background,
  by asking until none is pending: `gh pr checks --watch` can return
  while runs are still queued. The list covers check runs and commit
  statuses, pre-commit.ci's among them. It must not be empty: right
  after a push nothing has reported yet. The loop gives up after 30
  minutes; say so where it does.

  Before the loop, read `gh pr view <n> --repo <owner>/<repo> --json
  mergeable,mergeStateStatus`, and read it again where it answers
  `UNKNOWN`, which means not computed yet. `CONFLICTING` (`DIRTY`) is a
  merge with a conflict: no GitHub Actions run starts, and
  pre-commit.ci's status reads `error during mergeable check`, with no
  run to read. Bring the base in as the bullets above say, or, for a
  stacked pull request whose base was amended, as `CONTRIBUTING.md`'s
  *One subject, opened as soon as it is written* says.

  ```shell
  for i in $(seq 60); do
    [ "$(gh pr checks <n> --repo <owner>/<repo> --json bucket \
      --jq 'length > 0 and all(.[]; .bucket != "pending")')" = true ] &&
      break
    sleep 30
  done
  gh pr checks <n> --repo <owner>/<repo>
  ```

  The last command's exit code says how the loop ended: `0` all passed,
  `1` a failure or no checks at all, `8` still pending with none failed.
  The loop gave up wherever that output still lists a pending check or
  says `no checks reported`.

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
  gh api graphql --paginate -F owner=<owner> -F repo=<repo> -F n=<n> -f query='
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
    | .name' > <red file>
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
      gh pr close <n> --repo <owner>/<repo>
      gh pr reopen <n> --repo <owner>/<repo>
      ```

      The reopen's runs can still test the merge with the old `main`:
      GitHub refreshes `refs/pull/<n>/merge` lazily, and the event
      carries the merge it held, as the second reopen of
      PR btclib-org/btclib#2754 did. A run's log names the merge it
      tested, `Merge <head> into <base>`. The first command writes the
      log, and the second prints the line that names it:

      ```shell
      gh run view --repo <owner>/<repo> --log <run id> > <log file>
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

      *The decision* reads the bot's review of the reopen. Closing
      disarms auto-merge (`Pull request was closed`, on
      PR btclib-org/btclib#2754), so arm it again as *Landing* says.
      A check that only reports is named in the decision;
    - **not reproducing**: the shared *A failure that does not reproduce
      is measured*. One re-run measures it (`gh run rerun <run id>
      --repo <owner>/<repo> --failed`); two different answers are an
      issue, not a green;
    - **review quota exhausted**: the log of `Claude review` holds the
      line `api_error_status 429` (match with that, not with
      `api_error_status` alone: the log also echoes the workflow's own
      source) followed by a line such as `You've hit your weekly limit ·
      resets 11am (UTC)`.
      `$PROCESS/skills/btclib-pr/review-quota.md` says how the reset is
      read and what follows, and is read where such a run fails.

- **The bot's review is answered like any other**, iterating to an ACK
  that names the current head.

## The decision

**The session's approval is the human's** (the shared file's *Three
roles this file names*). Their standing instruction covers an obvious
approval, as defined below, and nothing else. Every other approval is
theirs to give.

**GitHub refuses an approval from a pull request's author.** On the
human's own pull request the session never approves: *The human's own
pull request* says what it does instead.

**The approval is obvious where every item holds**, each measured on the
head `<sha>`. The diff is read once, by two commands that must each
exit `0`:

```shell
gh pr diff <n> --repo <owner>/<repo> --name-only > <list file>
```

```shell
gh pr diff <n> --repo <owner>/<repo> > <diff file>
```

The list omits the old path of a renamed file, so add it from the diff:

```shell
grep '^rename from ' <diff file> | cut -d' ' -f3- >> <list file>
```

- [ ] the author is not the human: `.author.login` differs from
      `gh api user --jq .login`
- [ ] the latest fresh reviewer's `CLEARED` names `<sha>`, or *A rebase
      and the clearance* carries it to `<sha>`; where the other client
      is unavailable, the dedicated reviewer's does (the shared *A pull
      request's rounds*)
- [ ] every check passed or was skipped, required or not:
      `gh pr checks <n> --repo <owner>/<repo> --json bucket --jq
      'length > 0 and all(.[]; .bucket == "pass" or .bucket ==
      "skipping")'` answers `true`; *Rebase and CI*'s command that
      writes `<red file>` exits `0`; and `test ! -s <red file>` exits
      `0`. A cancelled check (bucket `cancel`) fails this item until a
      re-run passes.
- [ ] the bot's latest review starts `ACK <sha>`: `gh pr view <n>
      --repo <owner>/<repo> --json reviews --jq '[.reviews[] |
      select(.author.login == "claude" and .body != "")] | last |
      .body'`. While the bot is out of quota (a 429 with its reset
      ahead, read as *Rebase and CI* says), this item and the checks
      item fail, and the human decides (*Where it is not obvious*); on
      the human's own pull request, *The human's own pull request* says
      who does. The missing ACK does not stop the approval. On a bot's
      pull request (*A bot's pins*) whose pins change
      `.github/workflows/claude-review.yml`, the ACK may be missing, and
      the bot's `Claude review` check may fail while every other check
      passed or was skipped, as *Arming auto-merge*'s second case
      allows
- [ ] no review thread is unresolved, every page read (*What was
      raised*). It binds every approval, the human's decision included;
      *Arming auto-merge* has it for arming
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
      or `uv.lock`, or the exported lock (*The exported lock*, below):
      the third command below prints nothing and exits `1`
- [ ] `pyproject.toml` only moves requirements it already holds to a
      new version, read from the fourth command below
- [ ] the head's `uv.lock`, its `revision` line apart, is what uv
      writes from the base's lock and the versions the body names (*The
      reproduced lock*, below)
- [ ] on a bot's pull request (*A bot's pins*, below), its pin files
      only move pins: the fifth command below prints nothing
- [ ] a major move of a dependency, a hook or an action has the latest
      fresh reviewer's `CLEARED` name the release notes or changelog it
      read between the two versions, and say that nothing in them breaks
      the tree; where the other client is unavailable, the dedicated
      reviewer's does (the shared *A pull request's rounds*)

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
uv run --no-project --python 3.15 python -c 'import sys, tomllib
r = tomllib.load(open(sys.argv[1], "rb"))["project"].get("readme", "")
r = r if isinstance(r, str) else r.get("file", "")
sys.exit(bool(r) and r in open(sys.argv[2]).read().splitlines() and r)' \
  <toml file> <list file>
```

The third prints each file that fails its item, and exits `1` where
none does. The third reads `<export file>`. This writes it empty;
*The exported lock*, below, then fills it where it applies:

```shell
: > <export file>
```

Once *The exported lock*, below, has run where it applies, the third:

```shell
grep -Ev '^(docs|tests)/|\.md$|^(pyproject\.toml|uv\.lock)$' <list file> |
  grep -vxFf <export file>
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
grep -Ev '^(\.pre-commit-config\.yaml|\.github/workflows/[^/]+\.yml)$' \
  <list file> > <rest file>
```

The fifth prints each line a pin file changes that is not a pin, and
the header lines of a diff that adds, removes or renames a pin file,
whichever of its two paths is the pin file. A pin is a `rev:` line of
`.pre-commit-config.yaml`, with its `# frozen:` comment where it has one,
or a workflow's `uses:` line naming its action at a 40-digit sha, with
its `# vX.Y.Z` comment. Each pin is paired with its own: an action's by
the line without its sha, a hook's by the `- repo:` line its hunk shows
above it. It prints an action or a repository whose pins do not pair,
and a `rev:` line whose hunk shows no `- repo:` line:

```shell
awk '/^diff --git /{f = $(3); h = 1; r = ""
    p = $(0) ~ / [ab]\/\.pre-commit-config\.yaml( |$)/ ||
      $(0) ~ / [ab]\/\.github\/workflows\/[^\/ ]+\.yml( |$)/; next}
  !p {next}
  /^@@/{h = 0; r = ""; next}
  h && !/^(index |--- |[+][+][+] )/ {print f ": " $(0); next}
  h {next}
  /^. *- repo: / {r = $(0); sub(/^. *- repo: */, "", r)}
  !/^[-+]/ {next}
  {k = substr($(0), 2); d = /^[+]/ ? 1 : -1}
  f ~ /yaml$/ && r != "" && k ~ /^ *rev: *[^ #]+( *# frozen: [^ ]+)?$/ {
    n[f " " r] += d; next}
  f ~ /yml$/ && k ~ /^ *(- )?uses: *[^ @]+@[0-9a-f]{40} *# *v?[0-9][^ ]*$/ {
    sub(/@.*/, "", k); n[f k] += d; next}
  {print f ": " $(0)}
  END {for (k in n) if (n[k]) print "unpaired: " k}' <diff file>
```

**The clone.** *The exported lock* and *The reproduced lock* run in one
clone of `<sha>`, made once where either applies, before both. The
clone directory is a new one of your own. Shell state does not survive
between calls (*Where you work*), so each fence sets the values it reads
at its head: fill them in every fence. `<base>` is the merge base of
`<sha>` with `baseRefName` (*Whose pull request it is*), which this
prints:

```shell
gh api --jq .merge_base_commit.sha \
  repos/<owner>/<repo>/compare/<baseRefName>...<sha>
```

```shell
clone=<clone dir>
git init --quiet "${clone:?}"
```

```shell
clone=<clone dir>
sha=<sha>
base=<base>
repo=<owner>/<repo>
git -C "${clone:?}" fetch --quiet --depth 1 "https://github.com/${repo:?}" \
  "${sha:?}" "${base:?}"
```

```shell
clone=<clone dir>
sha=<sha>
git -C "${clone:?}" checkout --quiet --detach "${sha:?}"
```

**The exported lock.** On a pull request whose `.author.login` is
`app/dependabot`, and whose list holds
`.clusterfuzzlite/requirements.txt`, that file passes the third command
where the commands below regenerate it on `<sha>` and find it byte for
byte the same
([ISS 249](https://github.com/btclib-org/ai-agents-process/issues/249)).
They run the `uv-export` hook, which runs `uv export` with the tree's
arguments, by the command the tree's `CONTRIBUTING.md` gives an owner
(*A bot's*, under *Whose pull request it is*), in the clone.

The file is removed first, so that a hook that does not run leaves it
missing, which the last command reads as a difference:

```shell
clone=<clone dir>
rm "${clone:?}/.clusterfuzzlite/requirements.txt"
```

The hook exits `1` when it writes the file, so its exit code is not
read:

```shell
clone=<clone dir>
env -C "${clone:?}" uv run --locked --only-group lint \
  pre-commit run uv-export --all-files
```

```shell
clone=<clone dir>
sha=<sha>
exported=<export file>
git -C "${clone:?}" cat-file -e "${sha:?}:.clusterfuzzlite/requirements.txt" &&
  git -C "${clone:?}" diff --quiet -- .clusterfuzzlite/requirements.txt &&
  echo .clusterfuzzlite/requirements.txt > "${exported:?}"
```

**The reproduced lock.** Where the list holds `uv.lock`, the commands
below run in the clone, after *The exported lock* where it applies,
since its hook reads the head's lock. In place of the head's lock they
put the base's, then move each package the pull request's body names
to the version it names. Dependabot names a group's moves one a line,
``Updates `x` from 1.0 to 1.1``, and a single move on the body's first
line, which starts `Bumps [x]` and ends `from 1.0 to 1.1.` The fence
below reads both forms. The item holds where the lock uv writes is the
head's, byte for byte, but for the `revision = N` line at its top, whose
number depends on the uv that wrote the lock. Every other change in the
lock, such as a version moved, a package dropped, an extra emptied, a
new requirement or a changed marker, is then what uv makes of those
moves. Run them with a uv the tree's `[tool.uv]` `required-version`
admits, where one is set: uv refuses any other.

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
git -C "${clone:?}" show "${base:?}:uv.lock" > "${clone:?}/uv.lock"
```

```shell
clone=<clone dir>
moves=<moves file>
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
rm -rf "${clone:?}"
```

A major move is one where a version's first non-zero number changes: a
dependency's, a hook's `rev:` or its `# frozen:` comment, an action's
`# vX.Y.Z` comment. Where the notes show a known problem, the item
fails and the human decides (*Where it is not obvious*).

**Where it is obvious, approve `<sha>`, pinned.** `gh pr review` cannot
pin a commit, so the call is the API's:

```shell
gh api repos/<owner>/<repo>/pulls/<n>/reviews -f event=APPROVE \
  -f commit_id=<sha> -F body=@<body file>
```

The body is a one-line summary naming the head it approves, `<sha>`,
then one paragraph: the `CLEARED` it relies on and the rebase case; the
bot's ACK as a link, or during a 429 the 429 run as a link; that every
check passed or was skipped, the 429 run apart; each package *The
reproduced lock* finds the head's lock adds; for a major move, the
dependency, hook or action and the notes its `CLEARED` names; and what
was not checked.

Then land it, pinned to the same `<sha>` (*Landing*).

**Read the approval back**:

```shell
gh pr view <n> --repo <owner>/<repo> \
  --json headRefOid,reviewDecision,reviews --jq '.headRefOid,
  .reviewDecision, ([.reviews[] | select(.state == "APPROVED")] | last
  | .author.login, .commit.oid)'
```

It answers `<sha>`, `APPROVED`, the human's login, and `<sha>`. Where
the head moved, decide again on the new head. Where the decision is not
`APPROVED`, the ruleset asks for another approval. Request it from an
owner who is neither the human nor the author and pushed no commit to
the branch, and report whom it waits on.

**Where it is not obvious, the human decides**, as one decision (the
shared *When the human has to decide*). Its context is the `PR` link,
the head sha, and each failed item with its measurement. The
alternatives are: approve, once the thread item holds; ask the author
for changes, naming them, where the session cannot push to the branch;
wait, naming on what or whom; close, where that is an option. Where
only the bot's quota fails the items, the human may run a Claude review
locally.
Record it as a hold (the shared *When the human has to decide*). On
"approve", approve as above, with a body saying it follows the human's
decision. At night it is a deferred item (the shared *Night mode*).

### The human's own pull request

**Where the human is a bypass actor of an active ruleset, and is the
maintainer (the shared *Three roles this file names*) or runs `--land`
(*Landing*), the session lands it through the bypass, and requests no
owner's review.** It lands once every item above holds but those on the
author, the repository, the files in the list, `pyproject.toml` and
`uv.lock`, a bot's pins and a major move, as *Landing* qualifies them,
the bot's ACK and its check included or missing as *Arming auto-merge*
allows. *Landing* gives the command. `btclib-org/.github`'s
`GOVERNANCE.md`, under *How a decision is made*, decides which
repositories give the maintainer the bypass. This command prints the id
of each user an active ruleset gives the bypass in `pull_request` mode.
The human is a bypass actor where it prints the id
`gh api user --jq .id` prints:

```shell
gh api repos/<owner>/<repo>/rulesets --jq '.[].id' \
  | xargs -I{} gh api repos/<owner>/<repo>/rulesets/{} \
    --jq 'select(.enforcement == "active") | .bypass_actors[]?
      | select(.actor_type == "User" and .bypass_mode == "pull_request")
      | .actor_id'
```

Otherwise, `--land` included, another owner decides and `--admin` is
never attempted. Once the same items hold, except the two a 429 fails:

- request the review of every owner but the human who has not approved
  `<sha>`. `btclib-org/.github`'s `GOVERNANCE.md` names the owners, and
  `gh api "orgs/btclib-org/members?role=admin" --jq '.[].login'` lists
  them:

  ```shell
  gh pr edit <n> --repo <owner>/<repo> --add-reviewer <login>
  ```

- arm the landing once *Arming auto-merge* allows it, so that their
  approval lands it (*Landing*);
- report whom it waits on.

After a push, request the review again on the new head (*Landing*).

On a pull request that changes `claude-review.yml`, which the bot does
not review (*Arming auto-merge*), `--land` does not apply. It lands
through the bypass only where the human is the maintainer and a bypass
actor, as above, and is otherwise armed.

A pull request whose description says it breaks the live setup, in a
*Breaks* section as
[PR 175](https://github.com/btclib-org/ai-agents-process/pull/175)
has, is put to the human before it lands through the bypass.

## Outside contributors

Its issue stays theirs, and no competing branch is opened. The reviewer
reviews it against `REVIEWING.md`. Its gates run in the sandbox of the
shared *The gates*, whoever runs them.

**It is completed in place where `maintainerCanModify` is `true`**, with
every fix the approval needs, blocking findings and nits alike, as the
bullets below say. Otherwise the orchestrator delivers the findings on
the pull request, warmly and as the shared *What is posted on a forge*
says: the first line thanks them and names what holds the pull request,
what is right comes before what is missing, and a fix of a few lines is
a one-click suggestion. The session then waits. Where a branch of ours
must land first and touches their lines, the maintainer decides the
order, and the contributor is told on their pull request what moved and
how to resolve it. Completing it:

- **Add, never rewrite.** Their commits stay byte for byte. `main`
  comes in by a signed merge, not a rebase, run with hooks off as the
  shared *The gates* says. The fixes are a signed commit of ours on top,
  signed off by us.
- **Their sign-off is theirs to add.** A commit of theirs without the
  trailer is not ours to fix: a sign-off we add for them is not their
  attestation. Ask them, before we push anything to their branch, to
  run the command the `Sign-off` check's failure prints and force-push.
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

Where the bot's review does not run — a fork's pull request, and any
other where `gh pr checks` shows no review — the ACK is not an item of
*The decision*, and the approval is never obvious: it goes to the
human. A fork's pull request is armed as *Arming auto-merge* says.

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
   gh pr view <n> --repo <owner>/<repo> \
     --json headRefOid,baseRefName --jq '.headRefOid, .baseRefName'
   ```

1. This prints a number below 3000. The files endpoint returns at most
   3000 files, so a larger pull request can hide a file that does not
   pass:

   ```shell
   gh pr view <n> --repo <owner>/<repo> \
     --json changedFiles --jq .changedFiles
   ```

1. This exits `0` and writes a file that is not empty.
   `previous_filename` brings in the old name of a renamed file:

   ```shell
   gh api --paginate repos/<owner>/<repo>/pulls/<n>/files \
     --jq '.[] | .filename, (.previous_filename // empty)' > <files file>
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
   gh api repos/<owner>/<repo>/commits/<base> --jq .sha
   ```

   This exits `0`:

   ```shell
   git -C <checkout> fetch -q origin <base>
   ```

   This exits `0` or `1`:

   ```shell
   git -C <checkout> grep -h -F -f <files file> <base sha> -- \
     .github/workflows/ .github/actions/ pyproject.toml > <hits file>
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
gh pr list --repo <owner>/<repo> --state open --limit 200 \
  --json number,headRefOid \
  --jq '[.[] | select(.headRefOid == "<head>")] | length'
```

This lists the runs waiting on `<head>`, and the second command approves
one:

```shell
gh run list --repo <owner>/<repo> --commit <head> -L 100 \
  --status action_required --json databaseId,name
```

```shell
gh api -X POST repos/<owner>/<repo>/actions/runs/<databaseId>/approve
```

## Arming auto-merge

**The session arms squash auto-merge on a pull request only once all
three hold on its head**:

- every required check passed or was skipped;
- the review bot's latest review starts `ACK <head>`;
- no review thread is unresolved, read as *What was raised* says
  ([ISS 152](https://github.com/btclib-org/ai-agents-process/issues/152)).

Each pull request is armed on its own measurement: never by default, in
bulk or by a workflow. Several may be armed at once, once *Landing* has
tested their merge. The bot's check is not a required check: a pull
request armed earlier lands on an approval given before the bot
answered, or after it asked for changes.

**The ACK may be missing only in these cases**, and in each the pull
request is armed once every required check is green, no review thread
is unresolved, and the latest fresh reviewer's `CLEARED` names the head,
or the dedicated reviewer's where the other client is unavailable (the
shared *A pull request's rounds*):

- the bot's run failed with a 429, its quota exhausted, matched as
  *Rebase and CI* says;
- the pull request changes `claude-review.yml`, which the bot does not
  review: the action refuses to run where its workflow differs from the
  default branch's, and its check fails;
- the pull request comes from a fork, `isCrossRepository` being `true`
  in *Whose pull request it is*
  ([ISS 248](https://github.com/btclib-org/ai-agents-process/issues/248)).
  `btclib-org/.github`'s `reusable-claude-review.yml` skips the review
  where `head.repo.full_name` is not the calling repository. The human's
  approval then lands it (*Outside contributors*).

Where such a pull request lands through the bypass (*The human's own
pull request*), every check but the bot's `Claude review` is green as
well.

It is armed pinned to the head, with squash, the only merge method
(`CONTRIBUTING.md`'s *Landing it*):
`gh pr merge --squash --auto --match-head-commit <head>`. *Landing*
gives the whole command.

**The required checks are the branch protection's contexts.** The
first command writes them, and `<required file>` must not be empty. The
second writes each check that passed or was skipped on the head:

```shell
gh api repos/<owner>/<repo>/branches/main/protection/required_status_checks \
  --jq '.contexts[]' > <required file>
```

```shell
gh pr checks <n> --repo <owner>/<repo> --json name,bucket --jq '.[]
  | select(.bucket == "pass" or .bucket == "skipping") | .name' > <green file>
```

*Rebase and CI*'s command that writes `<red file>` exits `0`. The first
command below prints each required check that has not passed or been
skipped, and the second each one written to `<red file>`. Each exits `1`
where it prints nothing:

```shell
grep -vxFf <green file> <required file>
grep -xFf <red file> <required file>
```

`gh pr checks --required` is not enough: it omits a required check that
has not reported yet.

**The bot's review is read as *The decision* reads it.**
This answers `true` where it starts `ACK <head>`:

```shell
gh pr view <n> --repo <owner>/<repo> --json headRefOid,reviews \
  --jq '.headRefOid as $h
  | [.reviews[] | select(.author.login == "claude" and .body != "")]
  | last | (.body // "") | startswith("ACK " + $h)'
```

**A pull request armed otherwise is disarmed.** One that is armed is
disarmed before a push, and armed again once this section allows it on
the new head.
This lists the armed ones, and the second command disarms one:

```shell
gh pr list --repo <owner>/<repo> --json number,autoMergeRequest \
  --jq '.[] | select(.autoMergeRequest) | .number'
```

```shell
gh pr merge <n> --repo <owner>/<repo> --disable-auto
```

## Landing

- **Read `main`'s latest push runs** when choosing which pull requests
  to work, and after each landing: `gh run list --repo <owner>/<repo>
  --branch main --event push`. `main` is red where a required check
  failed in the latest run of its workflow. A cancelled check is not a
  failure, and a check that only reports does not count. While `main`
  is red, its repair is the first work, and other pull requests are
  still approved and armed
  (`CONTRIBUTING.md`'s *Landing it*).
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
  is the pull requests about to be armed or landed and those already
  armed, which *Arming auto-merge* lists. The test comes before any more
  of them is armed, because auto-merge lands at a time the session does
  not choose.

  Every run of the test starts here, each repeat below included, because
  fetching a pull request's ref leaves `origin/main` where it was:

  ```shell
  git -C <checkout> fetch origin
  ```

  The next command is run for each pull request. `<main sha>` is the
  `origin/main` that fetch left, pinned (the shared *How you establish a
  fact*), and each `<head>` is a `headRefOid`:

  ```shell
  git -C <checkout> fetch origin refs/pull/<n>/head
  ```

  ```shell
  git -C <checkout> worktree add --detach <wt> <main sha>
  ```

  ```shell
  git -C <wt> -c core.hooksPath=/dev/null \
    merge --no-ff --no-commit <head> <head> …
  ```

  With several heads `git merge` ignores `merge=union`, so it needs no
  `merge.union.driver`, and `core.hooksPath` keeps hooks from running on
  what the heads hold. Exit `0` leaves the merge staged and uncommitted.
  The tree's gates run on it as the shared *The gates* says, the gate lock
  and `gate_wait` included, and in its sandbox where any head is an
  outside contributor's. A push to one of the pull requests voids the run.

  **Where the merge exits non-zero, `merge-tree` says why.** This
  exits `1` where `<a>` and `<b>` conflict. It runs on `<main sha>` with
  each head, and on each pair of heads:

  ```shell
  git -C <wt> -c merge.union.driver=false \
    merge-tree --write-tree --name-only <a> <b>
  ```

  A head that conflicts with `main` leaves the set and is rebased now.
  Of a pair that conflicts, the repair of a red `main` lands first, then
  the one approved on its head, since a push dismisses that approval,
  then the lower number. The other of the pair leaves the set and is
  rebased once the first has landed. Each rebase goes as the shared *A
  rebase and the clearance* says. Where a head is an outside
  contributor's, *Outside contributors* says who decides the order, and
  `main` comes in by its merge, not a rebase.

  Where every run exits `0`, the octopus failed on its own, as it does
  on a file one head renames and another edits. Of the heads that change
  the path its `ERROR:` line names, the last in that order leaves the
  set, and is tested again once the others have landed.

  A head that leaves the set is disarmed (*Arming auto-merge*), and the
  test runs again on what remains. With one head left `git merge`
  applies `merge=union`, so the `merge-tree` of `<main sha>` with that
  head runs as well.

  **A gate red on the merge and green on `main`** is a clash no merge
  shows. The pull request it names gets the fix, in a new commit through
  the shared *The rounds*, and the test runs again. A gate red on `main`
  too is `main`'s, and *Landing*'s first bullet holds. That red can hide
  a clash on that gate.

  Whatever the outcome, `git -C <wt> merge --abort` ends the merge. It
  exits `128` where an octopus stopped before its last head and left
  nothing to abort. The worktree then goes (the shared *Debris goes when
  its work ends*). Where a fixer left changes, the abort can exit `128`
  too, and the worktree goes with `--force`.

  The test covers those heads on that `main`, and nothing that lands
  from outside the set afterwards. The re-read of armed pull requests in
  the shared *A rebase and the clearance* reads their prose and runs no
  gate.

- **Squash, by auto-merge, armed as *Arming auto-merge* says.** The
  branch carries several commits once review has added any, so the
  subject and the message are written, not inherited:

  ```shell
  gh pr merge <n> --repo <owner>/<repo> --squash --auto \
    --match-head-commit <the head that lands> \
    --subject "<title> (closes #<issue>) (#<n>)" --body-file <message>
  ```

  The subject is the pull request's title with its citation (the shared
  *Citations and closing keywords*) and `(#<n>)`; `--subject` replaces the whole
  subject. The message says what the change
  does, and keeps every `Signed-off-by:` and `Co-authored-by:` line of
  the commits it squashes. A finding that lives only in the commit
  message is fixed here, with no new round.

  **Where `--auto` is refused because the pull request is already
  mergeable**, land it by the same command without `--auto`, still
  pinned by `--match-head-commit`, once *Arming auto-merge* holds,
  then *Check what landed*. GitHub's refusal reads
  `Pull request is in clean status`, which gh prints as
  `GraphQL: Pull request Pull request is in clean status
  (enablePullRequestAutoMerge)`
  ([a report quoting it](https://github.com/peter-evans/enable-pull-request-automerge/issues/1118)).
  gh 2.103.2 merges at once, without arming, where the
  `mergeStateStatus` it reads is `CLEAN`, `HAS_HOOKS` or `UNSTABLE`
  (`isImmediatelyMergeable` in its `pkg/cmd/pr/merge/merge.go`).

  Never land through the bypass (`--admin`, or any other route to it)
  except where *The human's own pull request* says. It merges with no
  approval, even with required checks red. It lands with this, in place
  of the command above:

  ```shell
  gh pr merge <n> --repo <owner>/<repo> --squash --admin \
    --match-head-commit <the head that lands> \
    --subject "<title> (closes #<issue>) (#<n>)" --body-file <message>
  ```

  **`--land` instructs it**, for the pull requests named with it, or
  opened by `/btclib-iss` for the issues named with it, and no others.
  The human's words in the session, naming the pull requests, count
  too. The bypass then lands only the human's own pull request, where
  and once *The human's own pull request* says. A check that only
  reports and is red on `main` too does not hold it, and is named in
  the report.

- **Where `main` has moved past the sha the verdict read the prose
  on**, the shared *A rebase and the clearance* says who re-reads the
  prose before the branch is armed or lands, and what review a sentence
  found false there needs.
- **The pin is the head as last pushed**, not the sha a verdict named.
- **A stacked pull request lands like any other**: once its base has
  landed, it is rebased onto `main` as `CONTRIBUTING.md`'s *One subject,
  opened as soon as it is written* says, gated, decided again on the new
  head (*The decision*), and armed.
- **Check what landed, once it has.** Where `--auto` armed the pull
  request, it returned before the merge; where gh merged at once, it
  returned after. Either way, repeat `gh pr view <n> --repo
  <owner>/<repo> --json state,mergeCommit,autoMergeRequest --jq
  '.state, .mergeCommit.oid, .autoMergeRequest'` until it answers
  `MERGED`, and `<sha>` is that oid. Where it is `OPEN` with no
  `autoMergeRequest`, the merge was cancelled: report it. Once it is
  `MERGED`, `gh api repos/<owner>/<repo>/commits/<sha> --jq
  .commit.verification` is `verified: true`, and each issue the pull
  request declared closed is closed. What follows waits for this.
  The pull requests the session armed in that repository are then
  re-read on the new `main`, as the shared *A rebase and the
  clearance* says.

  Then wait for `main`'s workflow runs on `<sha>`, with *Rebase and
  CI*'s loop and this test in place of its own. A workflow run is
  completed only once all its jobs are, including the jobs that wait on
  others and have no check run before they start:

  ```shell
  [ "$(gh api --paginate \
    "repos/<owner>/<repo>/actions/runs?head_sha=<sha>&event=push&per_page=100" \
    --jq '.workflow_runs[].status' | sort -u)" = completed ]
  ```

  Then run this section's first bullet again: where the merge turned
  `main` red, its repair comes first.

- **A landing in `btclib-org/ai-agents-process` brings its primary
  checkout forward at once**, by the shared fast-forward. Where that
  checkout is the clone `$PROCESS` names, a session that starts reads
  the process through it, and reads the old one until then. A session
  already running re-reads what changed as the shared *The process is
  re-read when `main` changes it* says. Then read a landed line back
  where sessions read it: under `$PROCESS`, or through the link of the
  skill or agent it changed.
- **The collateral goes back now** (the shared *Collateral*), before
  anything new starts.
- **Remove the worktrees** — yours, and tell the writer to remove its
  own (*Debris goes when its work ends*).

Then the shared *Wrap-up*.

[dependabot-rebase]: https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/manage-dependabot-prs#allowing-dependabot-to-rebase-and-force-push-over-extra-commits
