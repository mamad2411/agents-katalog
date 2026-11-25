---
name: aflow-loop
description: Develop Aflow through its own loop from a terminal session — plan nodes on the board, Helmsman conversations that commission, review and publish, the merge under the folder's merge posture, then the post-merge cycle on the operator's checkout and live stack. Use when the operator asks you to drive plan work, run a stream, land a fix through the loop, or close out a merge. Builds on aflow-operate. Not for a commissioned change.
---

# Developing Aflow through its own loop

**Not for you if your task arrived as a commission or review brief.** This skill is for the
session beside the operator that drives the loop; the loop's coding agent follows its brief.

Read `aflow-operate` first: it holds the posture, the routes, the watchers and the gate
rules. `docs/dev/driving-work-through-the-loop.md` holds the mechanics of a round, the
resident, what a commission runs under, and how the machine is shared; this skill is the
operator-side procedure that uses them. Do not restate either; point at them.

## The shape

Work is a plan node on the board, under a plan root. A Helmsman conversation takes a node:
it commissions the coding harness on the repository's host binding from `origin/main`, the
publication runs the folder's checks and Local Code Review, pushes, and opens the pull
request. Who merges it depends on the folder's merge posture
(`docs/dev/driving-work-through-the-loop.md`, The pieces): under `never`, the default, the
operator merges; under `when-green` the Local PR Shepherd merges a green pull request
whose review approved its head, on the operator's approval. The conversation whose
publication opened the pull request owns it: each `pull_request.changed` wakes it, and it
runs a shepherd pass aimed at the pull request. A later publication by another conversation
takes the pull request over only where its owner has ended or failed. The hourly schedule sweeps only the pull
requests no conversation holds (Plan 339 D4). Never open a loop pull
request by hand: the shepherd sees only the ones a publication opened. The session's job is
to brief, watch, judge, report the pull request, wait for the merge, close it out, and keep
the stack current.

Board markers: `active` nodes in position order are the approved queue; `blocked` waits on
a person; `waiting` waits on a run; a proposal is created `blocked` and only a person moves
it. A node's first status follows `work` on `plan.node.create` (Plan 339 D6): approved
work starts `active`, and a node starts `blocked` only for a decision its card names in
`waitsOn`, which is where the rail's Approve appears. A root whose steps have all closed
reads finished and asks for no approval. A node reopened from `done` keeps "Reopened; it was done: <outcome>" at the head of its
note. A node that asks the operator for a decision carries a `card` (Plan 337): what
changes, why, what it affects, risks, open questions with a recommended answer, and what is
not done. A commissioned plan document opens with the same card, and the Helmsman links the
merged document to its node at the merge sha. The resident (Plan 331) takes the next active node on a schedule when the operator
has armed it; until then a node moves only when a Helmsman is told to take it.

## A stream, step by step

1. **Brief a Helmsman** (`aflow-operate`, [hm.sh](../aflow-operate/scripts/hm.sh) `new`). One conversation per
   stream. The brief names the node, the binding, the base (`origin/main` at a sha you
   read from the record), the rounds rule the operator set, and "report run ids, then
   hold". The node's goal, criteria and note are the harness brief; do not paste a second
   version of them.
2. **Watch the runs**, not the conversation: a commission, then a publication whose tasks
   are `commit`, `check-commit`, `review-commit`, `decide-push`, `approve-push`, `push`,
   `open-pr`. A `hand-fix-round` that succeeded means a fix round is next; the Helmsman
   starts it on its own. Re-arm a watcher on every new run id.
3. **Read every review**, from the `review-commit` task's `output_ref`. The rounds rule is
   the operator's: round 1 with a minor or worse gets a fix round; after round 1,
   minors and nits publish as is; a major or a blocker always gets a fix round; a stream
   with majors every round stops at the operator's limit, and the branch holds local
   while a design pass settles what the reviews kept re-finding. The publication reads
   this rule from its table (`ROUNDS_RULE`) with no model asked, so it does not hold
   minors past round 1. `override` stays for genuine exceptions, and raises a gate only
   the operator may approve.
4. **A gate** is read before it is touched (`aflow-operate`, Gates). The one the loop
   raises most is the override gate; its premise is "minors only" — check the run's own
   review, not the previous run's, before giving the operator the link.
5. **The merge** depends on the folder's merge posture (`host.binding.inspect` shows it).
   Under `never`, the default, the merge is the operator's: report the pull request and
   what its review returned, then wait. Under `when-green`, the shepherd merges
   by squash once the required checks pass on the head, the publication's review returned
   `approve` for that head and no person requests changes. A `comment` verdict merges the
   same way only where the space's autonomy is `full`, and its findings are on the pull
   request and brief the next node. Under `ratify` a `comment` head's merge asks the
   operator, as before. A `request_changes` verdict holds the head for a fix round. The merge asks the operator only where the
   space's write policy, composed with its autonomy, gates it (Plan 345). Read the
   shepherd's last `decide` output when a green pull request sits under `when-green`.
6. **After the merge**, on the operator's checkout (theirs: fast-forward only, never
   switch its branch — use a worktree for anything else):
   `git fetch origin && git merge --ff-only origin/main`; verify the branch's remote tip
   equals the pull request's `headRefOid` and that no worktree has it checked out; delete
   it on origin and locally; then tell the Helmsman `folder at <merge sha>` so it marks the
   node done and takes the next. Read every sha from the record; never spell one from
   memory.
7. **Absorb into the live stack** when nothing is mid-check: merge `origin/main` into the
   live worktree and restart (`docs/dev/driving-work-through-the-loop.md`, Sharing the
   machine). A restart kills the harness runs and checks in flight and stales the check
   receipt of any gate waiting on a person, so: every driving conversation paused on user
   input, no run `running`, no gate open. `yarn db:migrate` when a migration arrived;
   `POST /v1/spaces/:spaceId/store/update-preview { catalogId }` then `update` when a
   Store bundle's catalog version moved. Documentation-only merges need no restart.
8. **Record** what the stream learned where the next session reads it: the loop's carrier
   node for defects of the loop itself, the plan node's note or learnings for the work, and
   the session's own memory for the operator's rulings.

## What goes wrong, and what to do

- **The publication's decision step holds minors past round 1** — a known inconsistency;
  one more cheap fix round often beats an override gate the operator must click.
- **A remedy publication fails and the shepherd answers `wait` forever** — republish the
  branch as it stands (its head as `baseSha`, no `patchRef`, no `commitMessage`, no
  `override`); a re-commission returns an empty patch because the fix is already in the clone.
- **A gate approved and then "check receipt this executor did not issue"** — the executor
  restarted between check and approval; republish as it stands and the operator approves
  again. Never restart while a gate waits.
- **A Helmsman's diagnosis names a cause the record does not show** — check the process
  table and the executor log; correct it with the record before it writes the wrong cause
  into a node.
- **A conversation is blocked on a child run and cannot take your message** — it queues;
  resolving or ending the run delivers it.
- **A kept coding session expires after an hour idle** — the fix round is commissioned
  fresh from the branch; that is normal.
- **Stale local branches** accumulate under `aflow/*` in the operator's checkout after
  squash merges; prune only with the operator's word, since ancestry cannot prove a merge.

## What stays the operator's

The gate click, the hand merge, the push posture, the egress and write policy, the default
coding agent of the space, the model behind a decision step, the credentials, arming the
resident or the shepherd, pruning their branches, and resetting infrastructure. Declining a
gate with the record as the reason is yours; so is retrying a failed review, which never
cancels a publication whose commit is already on the branch.

## Keeping this skill honest

Task ids of the publication, the rounds rule's defaults, the shepherd's merge rule and the
board's status markers are the facts here that move. A change to the loop's skills or to the
plan engine updates this file in the same pull request. The machine's paths, the space id,
the binding id and the session ids are the session's notes, not this file's.
