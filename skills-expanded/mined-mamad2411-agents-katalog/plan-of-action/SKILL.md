---
name: plan-of-action
description: Turning a settled proposal into a Plan of Action — a staged implementation plan written for an AI agent to carry out, one <n>-<description>.md file per stage in the proposal's plan-of-action/ directory, summarised with every stage's status in plan-of-action/plan.md, each stage opening with a status header, with a checkpoint between stages and human steps called out explicitly. Use when a proposal's design is settled and it is time to plan the build, when writing a plan of action or splitting one into stages, and when implementing one — executing a proposal, working through the next stage, prefixing the commits a plan run makes, or asking what to build next from proposals/.
---

# Plan of Action

A **Plan of Action** is the bridge between a proposal and the work. The proposal argues what should
be built and why that shape; the plan says what to do about it. It lives in the proposal's own
directory, and it is **written for an AI agent to implement** — a sequence of instructions, not an
argument.

The proposal itself — its layout, status line, rejected options and lifecycle — is governed by the
`documentation` skill. This skill covers only the plan: writing it, staging it, and carrying it
out.

## When it is written

**Once a proposal's design is settled, it is turned into a Plan of Action before any of it is
built.** Writing the plan is a separate act from writing the proposal, and doing it separately is
the point: the proposal is where the design is argued out, and once that argument has landed the
plan can be written without relitigating it.

**The proposal's blocking questions are answered first.** A proposal marks which of its outstanding
decisions block work; a plan written over an unanswered one encodes a guess as an instruction, and
an agent implementing it has no way to tell the guess from the decisions. **Check
`decisions/decisions.md` before writing anything**: no row may be outstanding and blocking work, and
no assumption test that a blocking decision waits on may still be `Planned` in `tests/tests.md`. A
non-blocking decision can be carried into the stage that needs it, linked by its `D<n>` and said
plainly as a question rather than dressed up as a step. The decision and test files are described
in the `documentation` skill's `reference/decisions-and-tests.md`.

**Writing the plan stays inside the proposal's directory**, as writing the proposal does:
`plan-of-action/plan.md` and the stage files beside it are the only thing written, and nothing
outside `proposals/<proposal-slug>/` is touched until implementation begins or the user confirms
the change. Other agents may be writing other proposals in the same tree at the same time. The rule
and its reasoning are in the `documentation` skill's `reference/proposals.md`.

## Stages

A Plan of Action may be split into **stages**, one file per stage, in a `plan-of-action/`
directory beside `proposal.md`:

```
proposals/<proposal-slug>/
  proposal.md
  plan-of-action/
    plan.md                          # the plan summarised, every stage with its status
    1-update-database.md             # a plan of nine stages or fewer: no padding
    2-backfill-existing-rows.md
    01-update-database.md            # a plan of ten to ninety-nine stages: pad to two digits
    10-cut-over-the-reader.md
```

- **`plan-of-action/<iteration>-<description>.md`.** The iteration is the stage's position in the
  sequence; the description is a few words at most saying what that stage does. The directory
  says what the files are, so they carry no `plan-` prefix of their own
- **Zero-pad only as far as the current plan needs.** Nine stages or fewer take no padding at all,
  ten to ninety-nine pad the single digits to two, and so on. Padding is there so a directory
  listing shows the stages in execution order; padding wider than the plan needs implies stages
  that do not exist
- **List the stages in `plan-of-action/plan.md`**, in order — see *The plan summary* below. A
  stage file links back up with `../proposal.md`, and `../decisions/D3-...md` for a decision it
  carries out

**Corrected:** stage files used to sit beside `proposal.md` as `plan-<iteration>-<description>.md`.
Every stage added another file to a listing shared with `proposal.md`, its diagrams and its
supporting documents; the directory groups the stages, and the prefix it made redundant was
dropped. A proposal planned under the old naming need not be moved — see
*Migrating an old-layout proposal* in the `documentation` skill's `reference/proposals.md`.

### The plan summary

**`plan-of-action/plan.md` summarises the plan and lists every stage with its status.** It is
written with the stages and kept current as they run, and it is where a reader goes to see how
far through the plan the work has got:

- **The table of contents, then a title** — `# Plan of Action: <Proposal Name>`
- **A short summary of the plan**: what it builds, the shape of the sequence and why it runs in
  that order, and anything that cuts across stages, such as a human step several stages wait on
- **A counts line**: how many stages there are and how they split by status
- **One table with one row per stage, in order.** The columns are the stage (linked), what it does
  in one line, and its status in short form

```markdown
**Contents**

- [Plan of Action: User Invitations](#plan-of-action-user-invitations)

# Plan of Action: User Invitations

Adds the invitations table, then the endpoints that write it, then the email that announces it.
The table and its backfill come first because both endpoints are transcriptions of its columns.
Stage 3 waits on SES production access, which is a human step in stage 1.

Four stages: one complete and deployed, one built and not yet deployed, two not started.

| Stage | Does | Status |
| --- | --- | --- |
| [1](./1-update-database.md) | Adds the `invitations` table and its expiry index | COMPLETE and DEPLOYED |
| [2](./2-backfill-existing-rows.md) | Backfills an invitation for every existing member | BUILT, NOT YET DEPLOYED |
| [3](./3-the-invite-endpoints.md) | Adds `POST /invitations` and `POST /invitations/{id}/accept` | Not Started |
| [4](./4-documentation.md) | Moves what was built into `architecture/` and `instructions/` | Not Started |
```

**The stage header is the source of truth, and `plan.md` is a copy of it.** A stage's row, and the
counts, are updated in the same commit as its header. **`proposal.md` does not repeat the stage
list**: it gives a line with the counts and a link to `plan.md`, the same way it treats decisions
and tests.

**Corrected:** stages used to be linked in order from `proposal.md` itself. That put a second list,
growing with the plan, in the file that is meant to stay short, and it held no status, so finding
where a run had got to meant opening every stage file's header in turn.

**Splitting a plan into stages reduces the risk and the context of implementing it.** A stage is a
unit small enough for the implementing agent to hold at once, and small enough for a mistake to be
caught inside it rather than discovered twenty steps later with everything since built on top.

**Put the boundaries where a checkpoint is worth having.** The second reason to split is to stop
and verify, so a stage that can be tested or inspected on its own is a stage worth splitting out,
and consecutive work with nothing worth checking between it is one stage rather than three. Where
it can be had cheaply, a stage boundary should also leave the repository in a coherent state — one
that builds, deploys and makes sense on its own — so that stopping after any stage is a safe place
to stop.

## What a stage file contains

- **The status header, before anything else** — where this stage has got to, what it depends on
  and where it sits in the plan. See *The stage header* below
- **The instructions for that stage, as numbered sections** — the files to change, the commands to
  run, the end state to arrive at. Concrete enough to follow without re-deriving the design; where
  the *why* matters, link back to the section of `proposal.md` that argues it rather than restating
  it. The numbers are addresses: they are what the implementing agent's commit subjects cite, so
  once work has started a new section is appended rather than inserted, because renumbering the
  sections after it orphans every commit already made
- **Human steps, named as such, with whatever they have to run.** Some work cannot be done by the
  agent — issuing a credential, flipping a console setting, obtaining an approval, anything
  needing a login the agent does not have. Call these out explicitly at the point they are needed,
  and see *Human steps* below for what one contains
- **The checkpoint, at the end** — the tests to run, the command whose output should have changed,
  the thing to look at in a console. A stage with no way to verify it says so, rather than leaving
  the reader to wonder whether a check was forgotten

## The stage header

**Every stage file opens with a status header:** one blockquote, before the first heading, saying
where this stage has got to and how it sits in the rest of the plan. It is what a session resuming
a part-built plan reads first, and it carries what `git log` cannot — that the build is finished
but the apply is not, that a human step at the foot of the file is still outstanding, that a check
was made from a diff because the credentials to run it were not there.

**The stage file's table of contents comes straight after the status header**, before the first
heading, and is kept current as steps are added or corrected — see the `documentation` skill's
"Table of Contents" rule.

The header has six parts, in this order:

| Part | Holds |
| --- | --- |
| **Status** | Where this stage is, in one line — one of the four states below |
| **Build record** | The commits this stage was built in, each with a word on what it covers |
| **Divergences** | What the plan assumed that turned out not to hold, numbered, each saying what was done instead — or one line pointing at the steps, once they carry the detail |
| **Standing preamble** | Two fixed paragraphs, identical in every stage file of every proposal: that this is an execution plan for an agent rather than a description of the system, and that a divergence is corrected in place and said |
| **Dependencies** | Which earlier stages this one needs, linked, and **why** it needs them — plus anything else that changes how the file should be read |
| **Stage index** | A link to `plan.md`, then every stage of the plan, linked, in order, with this one bold, unlinked and marked `(this)` |

**The last three are written when the file is; the first three appear as they become true.** A
stage that has not started carries a status and nothing else above the preamble.

| Status | Means |
| --- | --- |
| `**Status: Not Started.**` | Written, not begun |
| `**Status: In Progress — Step 3 Done.**` | Begun — name the last step that landed, never a percentage |
| `**Status: BUILT, and its checkpoint cleared. NOT YET DEPLOYED**` | The repository is finished and the world is not. Say what is outstanding, and any ordering constraint on it |
| `**Status: COMPLETE and DEPLOYED.**` | Both. Say what was confirmed live, and name what was *not* exercised |

- **Capitals are for the state that will mislead someone.** `NOT YET DEPLOYED` shouts because a
  stage whose code is merged and whose apply has not run is the one a later reader most reliably
  mistakes for finished — and the one where that mistake costs the most
- **Update the header as the stage runs, not at the end.** A header that is only made true on
  completion is wrong for exactly the window in which someone is most likely to pick the work up:
  mid-stage, from a new session, with no memory of it
- **The build record maps steps to commits.** The commit prefix (below) makes a stage's commits
  findable from the log; the header is what says which step each one was, and what is still only
  half-committed
- **A divergence goes in both places.** The full account lives under the step it happened in, where
  someone following the plan will hit it; the header carries the one-line version, because the
  header is read first and a divergence nobody sees is one that gets made again. **Record the cost,
  not only the correction** — that an omission caused a failed apply is the part that stops the
  next plan omitting the same thing
- **Dependencies say why.** "Depends on Stage 1" gives the reader nothing to act on; naming what of
  Stage 1's this stage is a transcription of tells them what breaks if they run it early, and lets
  them judge whether the part they need is already there
- **The stage index makes every file an entry point.** `plan.md` indexes the stages, but a reader
  arriving at stage 6 from a commit message should not have to go back up to find out what else
  exists or where they are in it. The index links `plan.md` first, for the statuses it does not
  carry

## Human steps

**A human step that involves running something gives both halves: the instruction, and the exact
thing to run in a copyable block.** Project scripts, `aws` and other CLI invocations, SQL queries,
migrations, `terraform` commands — if the human's job is to execute it, the plan writes it out
ready to paste, not a description of what to assemble.

````markdown
**Human step — grant the processor role read access to the invitations bucket.** The deploy in
section 4 will fail without it. Run:

```bash
aws iam attach-role-policy \
  --role-name invitations-processor \
  --policy-arn arn:aws:iam::123456789012:policy/invitations-bucket-read
```

Confirm with `aws iam list-attached-role-policies --role-name invitations-processor`, which
should now list the policy.
````

**Neither half works alone.** An instruction on its own makes the human reconstruct a command the
plan's author already had in front of them, which is where the wrong profile, the wrong
environment and the half-remembered flag come from. A bare block is worse: pasted into a terminal
with nothing saying what it does or what a good result looks like, it gets run blind — and a step
is a human step precisely because it is the part the agent cannot do and cannot undo.

- **Fill in every value the plan already knows.** The bucket, the table, the role, the region: if
  the proposal settled it, it belongs in the command rather than as `<bucket-name>`. Mark what
  genuinely varies, and say where to get it
- **Say what the result should look like** — the output, the row count, the exit status, the thing
  now visible in a console. That is how the human knows to carry on rather than to stop
- **Never write a secret into the block.** A command may name where a credential comes from — an
  environment variable, a profile, a secret store path — but a plan file is committed, and a
  credential pasted into one is in `git log` for good

## Implementing the plan

**One stage at a time, in order.** Read `plan-of-action/plan.md` to find the stage you are on,
then that stage, plus `proposal.md` for context; do not read ahead into later stages. Reading ahead
spends the context the split exists to save, and pulls decisions forward into a stage that was
deliberately not making them yet.

- **Stop and prompt the human at a human step**, then wait — handing them the commands the plan
  gives, with anything only knowable now filled in: the id that was just generated, the ARN of the
  resource this stage created, the environment actually being worked on. Do not work around it, and
  do not assume it has been done because the plan says it should be — the whole reason it is in the
  plan is that the agent cannot verify it
- **Clear the stage's checkpoint before starting the next stage.** A failing checkpoint is the end
  of the run, not a note to carry forward; the next stage is written on the assumption that this
  one landed
- **Bring the header up to date in the same commit as the work it describes**, and the stage's row
  in `plan.md` with it when the status changes. The status, the new commit in the build record, a
  divergence just corrected: all of it is part of the step, not tidying to be done afterwards. A
  header updated later is a header that is wrong in between
- **Commit as the work lands, with a prefixed subject** — see *Commit subjects* below — so where
  the run got to is legible from `git log` rather than from memory. A session that resumes a
  part-built plan finds out where it got to that way
- **When reality contradicts the plan, stop and amend the plan** rather than improvising past it.
  The divergence — the thing the plan assumed that turned out not to hold — is exactly what the
  next reader needs, and a plan that has been quietly diverged from is worse than no plan at all,
  because it still reads as a description of what was done

**When the last stage is done, the proposal's lifecycle takes over**: what now exists is described
in `architecture/`, the operational side in `instructions/`, and the proposal's status line is
updated to say it has been implemented and to point at both. `plan.md` and the plan stages stay
where they are, with the proposal. See the `documentation` skill.

## Commit subjects

**Every commit made while implementing a plan is prefixed with the proposal and the section of the
plan it came from:**

```
<Proposal Name> Proposal <stage>.<section>: <subject>
```

```
User Invitations Proposal 02.1: Database updates
User Invitations Proposal 13.15: Final Testing of Invitations
```

- **`<Proposal Name>`** is the proposal's own name, as its `proposal.md` title gives it —
  `proposals/user-invitations/` implementing *User Invitations* gives `User Invitations Proposal`
- **`<stage>`** is the number in the stage file's name, **exactly as written there, padding
  included**. `plan-of-action/02-update-database.md` gives `02` and
  `plan-of-action/2-update-database.md` gives `2`; normalising it either way breaks the match
  between a commit and the file it names
- **`<section>`** is the number of the section *within that stage file* that the commit's work
  belongs to, not a running count of commits
- **The subject after the colon** is written the way any other commit subject on the project is
  written — the prefix replaces none of that, and whatever subject-length limit the project holds
  itself to covers the whole line, prefix included

**Several commits may share one prefix.** A section is a unit of the plan, not a unit of committing;
splitting it across commits where that makes the diffs readable is expected, and needs no
distinguishing suffix. What must not happen is the reverse — one commit spanning two sections —
because the prefix then names only one of them and the other's work is invisible in the log.

**The prefix is what makes a run legible from outside it.** Without it, `git log` over a
half-implemented plan is a list of ordinary subjects with nothing saying which proposal they serve
or how far through its stages they got, and a session resuming that work has to read diffs to find
out. With it, `git log --oneline --grep 'User Invitations Proposal'` is the progress report, and
the last subject in it says exactly which stage and section to pick up from.

**Corrected:** this rule previously said only to *commit at each stage boundary*, with no prefix
and no mention of sections. That was too coarse in both directions — it made a whole stage the
smallest committable unit, and it left the commits of a plan run indistinguishable from every other
commit on the branch.

## References

- **`reference/stage-header.md`** — the standing preamble to copy, and the same stage file's header
  worked through all four states, from not started to deployed

## Related

- `documentation` skill — the proposal itself, the three tenses, and where the description of the
  built thing goes afterwards
- `conventions` skill — the project's own `conventions/` file, which wins over anything here
- `product-requirements` skill — `requirements/`, where a user-level feature and its acceptance
  criteria are recorded, as opposed to a plan for building one
