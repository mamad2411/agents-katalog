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
again, whole and once, from `$PROCESS/skills/btclib-iss/SKILL.md`.

**Then read `$PROCESS/process/btclib-common.md`, whole.** Its opening
says what it holds and what this file holds. What the session writes,
and this file, follow its *Write plainly*.

**Where $ARGUMENTS names no issue, ask the human which, before reading
anything**: no tracker, no checkout, and no earlier context stands in for
the answer. Where the repository is not named either, that question comes
first (the shared *Where you work*).

GitHub numbers issues and pull requests together, so `gh pr view <n>`
says which a number is. A pull request among the arguments is
`/btclib-pr`'s: skip it and tell the human.

**Which sections are yours**, beyond the shared file's map:

- **The writer**: *What the issue still asks*, and `/btclib-pr`'s *What
  was raised*, *Answering it* and *Rebase and CI*.
- **The reviewer**: `/btclib-pr`'s *Rebase and CI*'s first bullet, for
  the delta it reads.
- **The orchestrator**: all of this file.

## Several issues, several pull requests

- **Never as a batch; never hold one that is ready.** Open each pull
  request as soon as it is cleared, except an embargoed fix (the shared
  *Committing and rebasing*).
- **Bundle by subject, not by file**, as the tree's `CONTRIBUTING.md`
  says in *One subject, opened as soon as it is written*. Issues one
  decision answers share a subject; issues that only touch the same file
  do not. Before assigning a worker, look for open issues sharing a
  subject with the one at hand (`gh issue view` each) and take them
  together.
- **A port asks for convergence.** Hash the copies first; ask each tree
  to take the source byte for byte rather than apply the delta you
  measured, which can come up short.
- **Where a pull request is already open for an issue**, this skill
  opens no competing branch: that pull request is `/btclib-pr`'s.

## What the issue still asks

The writer does this for its issue; the orchestrator does it before
briefing anybody, after the shared *Before starting*.

**Re-derive the issue's *Done when* and its central measurement against
`origin/main`**, and say which parts are already answered. An issue
answered entirely is closed with the measurement. Within one repository
this finds landed commits citing still-open issues:

```shell
open=$(gh issue list --repo <owner>/<repo> --state open --limit 200 \
  --json number -q '.[].number')
git -C <wt> log --format='%h|%s' -80 origin/main |
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
gh issue edit <n> --repo <owner>/<repo> --remove-label upstream-dependent
```

An issue with a reason label (the shared *When the human has to decide*,
*A hold is recorded*) is taken only once the wait its label names is
over, and taking it removes that label the same way.

## Opening the pull request

The orchestrator's. **Before opening, and the last item once it is
open:**

- [ ] the latest fresh reviewer's `CLEARED` (the shared *Local review*)
      names the branch's content, or *A rebase and the clearance*
      carries it to the rebased branch; where the other client is
      unavailable, the dedicated reviewer's does (the shared *A pull
      request's rounds*)
- [ ] no conflict with `origin/main` (`/btclib-pr`'s *Rebase and CI*);
      where there was one, rebased and the gates re-run (the shared *A
      rebase and the clearance*)
- [ ] the subject that lands carries the right citation (the shared
      *Citations and closing keywords*)
- [ ] the closing block comes after the sections, as the bullet below
      describes, and the sweep finds no other keyword
- [ ] the body has the shape below: the opening paragraphs, `## Evidence`,
      and `## Decision` where a decision was reserved
- [ ] `closingIssuesReferences` counts what you meant to close

- **A change to `claude-review.yml` is its own pull request**: the bot
  does not review it (`/btclib-pr`'s *Arming auto-merge*).
- **The body is the paragraphs, then sections, then the closing block
  (the shared *Citations and closing keywords*).** The paragraphs keep
  the body limit of the shared *What is posted on a forge* and say what
  the change does and why. The sections do not count against that limit,
  and each stays short.
- **`## Evidence` is a short table or list**: the gates that ran on the
  head, with their exit codes; the rebase case the clearance is in; the
  review. The records the tree asks of a body go here too, each where
  its own text says it applies: the command that verifies a rule
  (`CONTRIBUTING.md`), the count that decided the change (the shared
  *What the prose that lands may say*), the runs the bot can repeat
  (the shared *A pull request's rounds*), the command that reads a
  setting back (the shared *Collateral*), and the command that measured
  a claim (`REVIEWING.md`).
- **`## Decision` is there only where the issue reserved one**: it says
  that the branch takes it, on what ground, and what the cut-back is.
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
restated here: *What was raised*, *Answering it*, *Rebase and CI*,
*The human's own pull request*, *Arming auto-merge*, and *Landing*'s
bullets from *Read `main`'s latest push runs* to *The pin is the head
as last pushed*, and its *Check what landed*. Under `--land`, all of
*Landing* applies.

- **The `/btclib-pr` *Landing* bullets on the collateral and on the
  worktrees hold here**, and *Debris goes when its work ends* removes
  the worktrees once the session hands the pull request over to whom it
  waits on.
- **Report to the human** each pull request as a `PR` link with its
  diff balance (the shared *How an issue and a pull request are
  named*), what it closes, and whom it waits on or that it landed.
  What arrives after the session ends — a review, a conflict with
  `main` — is `/btclib-pr`'s.

Then the shared *Wrap-up*.
