---
name: btclib-iss
description: "btclib-iss — from an issue to an open pull request, locally reviewed before GitHub and followed as its author, measuring rather than asserting"
argument-hint: "[--night] [--land] <issue numbers or URLs>"
---

# From an issue to a pull request

Take on the issues named in $ARGUMENTS, in a repository of `btclib-org`,
and take each to an open pull request, written, gated and cleared by a
local review (*Opening the pull request*). Then follow each as its
author (*Following it*).

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
again, whole and once, from `$PROCESS/skills/btclib-iss/SKILL.md`.

**Then read the shared files, whole**: `every-role.md`, `writing.md`,
`local-review.md` and `orchestration.md`, in `$PROCESS/process/`.
`every-role.md`'s opening says what they hold and what this file holds.
What the session writes, and this file, follow `every-session.md`'s
*Write plainly*.

**Where $ARGUMENTS names no issue, ask the human which, before reading
anything**: no tracker, no checkout, and no earlier context stands in for
the answer. Where the repository is not named either, that question comes
first (`every-role.md`'s *Where you work*).

GitHub numbers issues and pull requests together, so `gh pr view <n>`
says which a number is. A pull request among the arguments is
`/btclib-pr`'s: skip it and tell the human.

**Which sections are yours**, beyond `every-role.md`'s map:

- **The writer**: *What the issue still asks*, *Ports of the standard*
  where it writes a port, and `/btclib-pr`'s *What was raised*,
  *Answering it* and *Rebase and CI*.
- **The reviewer**: `/btclib-pr`'s *Rebase and CI*'s first bullet, for
  the delta it reads.
- **The designer**: *The design pass*.
- **The orchestrator**: all of this file.

## Several issues, several pull requests

- **Never as a batch; never hold one that is ready.** Open each pull
  request as soon as it is cleared, except an embargoed fix
  (`writing.md`'s *Committing and rebasing*). Ports of the standard are
  the one batch (*Ports of the standard*).
- **Bundle by subject, not by file**, as the tree's `CONTRIBUTING.md`
  says in *One subject, opened as soon as it is written*. Issues one
  decision answers share a subject; issues that only touch the same file
  do not. Before assigning a worker, look for open issues sharing a
  subject with the one at hand (`gh issue view` each) and take them
  together. The exception is a known-limits issue (`local-review.md`'s
  *The rounds*), which shares a subject with any issue whose branch
  changes its script, and is taken with it.
- **Where a pull request is already open for an issue**, this skill
  opens no competing branch: that pull request is `/btclib-pr`'s.

## Ports of the standard

A change of the standard in `btclib-org/.github` that every tree has
to take lands there first, and reaches each other tree by a port.

- **A tree's ports go in one batch**: one pull request holding every
  change of the standard landed since the tree's last port. **A batch
  goes once a day**, after the day's release where the tree had one, and
  the first session that day to find an issue waiting for it (below)
  starts it.
- **A change that may not wait goes at once**, in a round of its own,
  or as the tree's first batch where none has landed, since the guess
  below would pass the changes still waiting: a security fix, a change
  without which a tree's gates, a required check or a release fail, and
  a change the maintainer names on its issue. A session unsure whether a
  change may wait asks the maintainer (`every-session.md`'s *When the
  human has to decide*).
- **The standard's issue waits for the batches.** Once the standard's
  change lands, the issue takes `on-hold`, a pause the maintainer
  decided, and a comment saying its port "travels with the next batch"
  (`every-session.md`'s *A hold is recorded*). It waits for each tree
  whose last port (below) does not hold its change. A session finds the
  waiting issues with:

  ```shell
  gh issue list -R btclib-org/.github --state open --label on-hold \
    --limit 1000 --search '"travels with the next batch" in:comments'
  ```

  No port closes the issue, the last tree's included: each cites it as
  *The subject that lands records the port* says, and section 11 of the
  standard, *What a pull request says it is*, says which session closes
  it by hand and with what measurement. That session also takes the
  label off.
- **The standard's alignment tests expect the drift.** The standard's
  pull request adds to `EXPECTED_DRIFT`, in `tests/verbatim_test.py`,
  each path it changes that section 14 compares and that has no entry
  yet, citing the issue. The entry's strict expected failure turns red
  once every copy agrees. The session that closes the issue an entry
  cites (above) then changes the entry, in a pull request of the
  standard. Where the copies agree, it removes the entry. Where they
  still differ and another open issue holds that drift, a change still
  waiting on the path among them, it points the entry at that issue.
  Where they differ and no open issue holds that drift, it files one in
  btclib-org/.github and points the entry at the issue it filed. A
  removed entry would leave that pull request red on the copies that
  differ.
- **A batch takes the standard's copies byte for byte**, rather than
  applying the delta, which can come up short. It takes them from
  `<S>`, the standard's `origin/main` when the batch starts. A file with
  a `## This repository in particular` heading takes the part above it.
  Each other change since the tree's last port is adapted as its issue
  says.
- **A batch that moves the tree's calls into `btclib-org/.github` to a
  new tag moves `claude-review.yml`'s with them**, in the same pull
  request, since section 10 of the standard pins `btclib-org/.github`
  at one commit throughout a tree's workflows. The bot does not review
  that pull request, which lands as the second case of `/btclib-pr`'s
  *The reviews on GitHub* says: on the local review, in place of the
  bot's ACK.
- **The subject that lands records the port**: a batch's is
  `Port btclib-org/.github@<S>` alone, with neither the citations of
  `writing.md`'s *Citations and closing keywords* nor the pull request's
  number. The body of every port's pull request, a round of its own
  included, cites each issue the port advances on an `Advances …` line.
  A round of its own takes a subject of its own, so that the record does
  not pass the changes still waiting. Before the first batch, no subject
  records one: the script below guesses it from the copies, the writer
  checks each change it lists against the tree, and the body names the
  guess.
- **`scripts/port-check.py` checks a batch against `<S>`.** Its
  docstring says which files it compares, what it prints and what each
  exit code means:

  ```shell
  std=<checkout of btclib-org/.github>
  s=<S>
  tree=<the tree's worktree>
  base=<the batch's parent on main>
  head=<the batch's head>
  python3 "${PROCESS:?}/scripts/port-check.py" \
    "${std:?}" "${s:?}" "${tree:?}" "${base:?}" "${head:?}"
  ```

  `orchestration.md`'s *Running the rounds* says what its exit decides.

## What the issue still asks

The writer does this for its issue; the orchestrator does it before
briefing anybody, after `writing.md`'s *Before starting*.

**Re-derive the issue's *Done when* and its central measurement against
`origin/main`**, and say which parts are already answered. An issue
answered entirely is closed with the measurement. Within one repository
this finds landed commits citing still-open issues:

```shell
repo=<owner>/<repo>
wt=<wt>
open=$(gh issue list --repo "${repo:?}" --state open --limit 200 \
  --json number -q '.[].number')
git -C "${wt:?}" log --format='%h|%s' -80 origin/main |
while IFS='|' read -r sha subj; do
  echo "$subj" | grep -oE '#[0-9]+' | tr -d '#' | while read -r n; do
    echo "$open" | grep -qx "$n" && echo "$sha ISS $n  $subj"
  done
done
```

An issue labelled `upstream-dependent` is taken only once its wait is
over; taking it removes `upstream-dependent`. The wait is what the issue
names, in its body or a later comment: an upstream issue, pull request,
release or draft. Read its state there.

```shell
n=<n>
repo=<owner>/<repo>
```

```shell
gh issue edit "${n:?}" --repo "${repo:?}" --remove-label upstream-dependent
```

An issue with a reason label (`every-session.md`'s *When the human has
to decide*, *A hold is recorded*) is taken only once the wait its label
names is over, and taking it removes that label the same way, except the
`on-hold` of a port's wait, which *Ports of the standard* takes off.

## The design pass

The orchestrator's, once *What the issue still asks* leaves something to
write, and before a writer is dispatched. A `designer` agent at fresh
context weighs how the issue could be answered, because a design choice
a review finds in a later round costs a rewrite, its gates and another
round.

**It runs for every issue except these**, and the writer's brief says
which exception applied:

- **a port of the standard** (*Ports of the standard*);
- **an issue whose shape is fixed**: the issue, or a comment of the
  maintainer on it, says what to write, as the file and the text, the
  command or the code, and leaves the writer only its wording. An issue
  that names only an outcome, or a change with a choice still open in
  it, is not one.

**Its brief** holds the issue with its comments, the repository, and the
`origin/main` sha the designer reads the tree at, as
`orchestration.md`'s *Orchestration* says of a brief. It asks for this
report:

1. the problem and the goal, stated without the solution;
1. the baseline: what doing nothing costs, and what the tree already
   holds that answers part of it;
1. the benefit a pull request, an issue or a run shows, apart from the
   benefit only claimed;
1. at most four alternatives, each materially different from the others,
   with its benefit, its cost and what stays unverified; an empty list
   rather than a generic one;
1. the one to take, and why;
1. where the choice depends on a requirement, a measurement or the
   maintainer's preference, that as one decisive question.

**The pass stays small**: no gate, no build, and a report that fits in a
writer's brief.

**The report goes whole into the writer's brief.** Its question is put
as `every-session.md`'s *When the human has to decide* says, and the
writer starts once it is answered; at night, `night-mode.md` says what
becomes of it. The pull request body's `## Decision` records it
(*Opening the pull request*).

## Opening the pull request

The orchestrator's. **Before opening, and the last item once it is
open:**

- [ ] the latest fresh reviewer's `CLEARED` (`local-review.md`'s *Local
      review*) names the branch's content, or `orchestration.md`'s *A
      rebase and the clearance* carries it to the rebased branch; where
      the other client is unavailable, the dedicated reviewer's does
      (`orchestration.md`'s *Where the other client is unavailable*)
- [ ] no conflict with `origin/main` (`/btclib-pr`'s *Rebase and CI*);
      where there was one, rebased and the gates re-run
      (`orchestration.md`'s *A rebase and the clearance*)
- [ ] the subject that lands carries the right citation (`writing.md`'s
      *Citations and closing keywords*)
- [ ] the closing block comes after the sections, as the bullet below
      describes, and the sweep finds no other keyword
- [ ] the body has the shape below: the opening paragraphs,
      `## Evidence`, and `## Decision` where a decision was reserved or
      the design pass put one
- [ ] `closingIssuesReferences` counts what you meant to close

- **A change to `claude-review.yml`, or to a reusable workflow it calls
  by a local path, is its own pull request**: the bot reviews neither
  (`/btclib-pr`'s *The reviews on GitHub*). A batch of ports that moves
  the tree's calls to a new tag is the exception (*Ports of the
  standard*).
- **The body is the paragraphs, then sections, then the closing block
  (`writing.md`'s *Citations and closing keywords*).** The paragraphs
  keep the body limit of `every-session.md`'s *What is posted on a
  forge* and say what the change does and why. The sections do not count
  against that limit, and each stays short.
- **`## Evidence` is a short table or list**: the gates of the head,
  with their exit codes, as `writing.md`'s *The gates* reports them; the
  rebase case the clearance is in; the review, with each finding
  `local-review.md`'s *The rounds* files from the third round, as not
  covered, with the issue that holds it; and, once they have answered,
  each review on GitHub that is absent, with its reason (`/btclib-pr`'s
  *The reviews on GitHub*). The records the tree asks of a body go here
  too, each where its own text says it applies: the command that
  verifies a rule (`CONTRIBUTING.md`), the count that decided the change
  (`writing.md`'s *What the prose that lands may say*), the runs the bot
  can repeat (`local-review.md`'s *A pull request's rounds*), the
  command that reads a setting back (`every-role.md`'s *Collateral*),
  and the command that measured a claim (`REVIEWING.md`).
- **`## Decision` is there only where the issue reserved one, or the
  design pass put one** (*The design pass*): it says what the branch
  takes, on what ground, and what the cut-back is.
- **Count what GitHub will close**:
  `gh pr view <n> --json closingIssuesReferences --jq
  '.closingIssuesReferences | length'`. The field lags creation by
  seconds to minutes; ask again.
- **Request the reviews `/btclib-pr`'s *The human's own pull request*
  names**, unless that section has the session land it through the
  bypass.

## Following it

Once a pull request is open, the session follows it as its author.
`$PROCESS/skills/btclib-pr/SKILL.md` holds the rules, read there and not
restated here: *What was raised*, *Answering it*, *Rebase and CI*, *The
reviews on GitHub*, *The human's own pull request*, *Merging*, and
*Landing*'s bullets from *Read `main`'s latest push runs* to *The pin is
the head as last pushed*, and its *Check what landed*. Under `--land`,
all of `/btclib-pr`'s *Landing* applies.

- **The `/btclib-pr` *Landing* bullets on the collateral and on the
  worktrees hold here**, and `every-role.md`'s *Debris goes when its
  work ends* removes the worktrees once the session hands the pull
  request over to whom it waits on.
- **Report to the human** each pull request as a `PR` link with its
  diff balance (`every-role.md`'s *How an issue and a pull request are
  named*), what it closes, and whom it waits on or that it landed.
  What arrives after the session ends — a review, a conflict with
  `main` — is `/btclib-pr`'s.

Then `orchestration.md`'s *Wrap-up*.
