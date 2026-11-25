---
name: task-record-contract
description: Use when writing or revising a task record — deciding its intent, scope, acceptance criteria, and which requirements to declare. Covers the frontmatter fields, the status vocabulary, and what each requirement kind actually demands.
metadata:
  area: records
  side_effects: writes-files
  credentials: none
  runs_scripts: none
---

# Task record contract

A task record is ordinary Markdown under `.castwork/tasks/`. Structured data
lives in the YAML frontmatter; the body is prose. The full contract is
`docs/record-format.md`; this is how to write a good one.

## Minimum

```yaml
---
schema: 1
id: T-001
title: Greet by name
status: draft
---
```

Then a body with `## Intent`, `## Scope`, `## Out of scope`, and
`## Acceptance criteria`. Any additional heading is fine.

## Writing the body

- **Intent** — the outcome, in the user's terms. Why this is being done.
- **Scope** — what changes. Name files or areas when you know them.
- **Out of scope** — the nearby work that must *not* be bundled in. This is the
  most useful heading in the record and the most often skipped. Where the
  request leaves its scope open, the criteria describe the smallest version
  that does its core job, and what that leaves out, such as features or
  options nobody asked for, is listed here, so the user can ask for it.
- **Acceptance criteria** — observable outcomes, one per bullet. If you cannot
  say how you would see it, it is not a criterion yet. Seeing it can be an
  existing check, a run or an inspection: a criterion does not by itself call
  for a new test. Say where a consequential criterion comes from: the user's
  words, a decision by id, or the agents' proposal. A criterion an agent adds
  or tightens once the work is under way, such as a clarification after a
  finding, stays the agents' proposal, marked so where it stands, until the
  user confirms it: a later re-plan or step back may narrow or drop it, saying
  why, where nothing the user committed to needs it. A criterion that guards
  against a harm names what could bring it about in use, by accident or on
  purpose, and what that would take. A cause that ordinary use, concurrent use
  included, would not produce by accident, and that someone could produce on
  purpose only with access that already lets them do the harm directly, lies
  outside it unless the user, a decision or the project's documents put it in.
- **Plan** — when the work needs one, the thinker's current plan. A re-plan
  rewrites it in place, like Current state, replacing every earlier plan still
  in the record, with what changed and why under
  `## Blockers and decisions`, in place of the entry the last re-plan left: the
  record holds one current plan, and a superseded plan's reasoning stays in the
  findings it cites.
- **Current state** — what holds now: current candidate, unresolved issues,
  restrictions with decision ids and source line pointers, next step. Rewrite
  in place, about fifteen lines. Open with what holds now; who wrote it and
  when go after, since the first paragraph is what `report` shows. When roles
  are coordinated it is the
  coordinator's, written from the roles' reports or assigned to one role at a
  time; otherwise the agent working alone keeps it. It grants nothing; cited
  decisions and the user's current instructions govern.
- **Blockers and decisions** — what blocks the work now and the decisions still
  in force for it, each written when it happens rather than reconstructed
  later. When a blocker clears or a decision is superseded, rewrite or remove
  its entry, so the record keeps what a reader acts on; where nothing committed
  keeps reasoning that surviving evidence, assessments or decisions rest on,
  move it to a findings file the record cites first. It is not a log of rounds:
  what a round observed is evidence or an
  assessment in the frontmatter lists, what it means for the next step is
  Current state, and reasoning that must outlive the record goes in a findings
  file it cites.

Candidates, evidence, and assessments go in the frontmatter lists, never in a
fenced block in the body: the checks read only the frontmatter, and lint reports
body entries as `entries.in_body`. Append to the lists, by hand or with
`npx --no castwork task add`; do not rewrite someone else's entry.

Record durable decisions and material failures. Do not paste command
transcripts, lint output, or a table of every check you ran. Routine successful
output does not need to be retained; link a file under `output` only when its
contents materially support a failure, reproduction, or review finding. A
milestone narrative belongs in the milestone document, not repeated in every
task that contributed to it. Run output stays out of the record: a record past
100 KB is reported as `record.large`. A routine successful probe is a sentence
in the body, or nothing; material observations stay candidate-bound evidence.
What a run produces and no record links, such as logs, exit and pid files,
dumps, and captures, goes in `.castwork/local/runs/<task>/`, which Git ignores.
Link only durable support, not ignored scratch or `.castwork/tasks/`: write it
in `.castwork/findings/`, named after the task, such as `T-012-review.md`, and
copy a run's output there only where a failure, an acceptance or a
reproduction rests on it, and only the part it rests on, not copied sources,
archives or a whole run's output the entry already states. A snapshot holds that
folder, as it holds
the records, as the base commit has it, without what was written there since, so
a file the task delivers, or a script a declared check runs,
never goes there: it is part of the candidate. A review of how work went goes
in `.castwork/reviews/`.

`task archive [<id>] [--check]` explicitly moves the entries for earlier
candidates
into a paired `<record>.archive.md`; the two files remain one logical record,
and
the body never moves, so keep it short. It never weakens requirements, and a
named verification refusal writes nothing. After archiving
or resuming an archived task, read both files when refreshing Current state.

## Criteria that something stays unchanged

Most tasks need no such criterion. When one needs evidence that the work left
something alone, the criterion is observable only if the record settles five
questions before the work starts. Each one left open gets decided later, in an
assessment, as a dispute:

- **What is protected.** Name the smallest set of files or resources. Left
  open, a change someone else made during the work, such as an update, counts
  against it.
- **What counts as an input.** Say whether task records, decisions, and the
  skills a host loads are included. Left open, every unrecorded read is argued.
- **When identities are captured.** Before an input's first read, including an
  input found partway through. Left open, a late capture is argued as a pass
  or a failure.
- **Which permitted actions write anyway.** This record, which the work
  updates, and `snapshot`, which writes Git objects. Left open, they count
  against the work.
- **What shows it.** The observation, recorded as evidence, and where its
  capture steps sit in the plan. Left open, later evidence is offered to
  repair an earlier gap.

For example: "Files under `config/` and the decisions this task cites are
unchanged by it: each is hashed before its first read, an input found partway
through as soon as it is found, and all again at the candidate. This record
and the Git objects `snapshot` writes are not inputs."

A capture step the record asked for and the work missed stays missed, unless
existing evidence shows the criterion met or the user changes the criterion;
record that change as a decision.

## Candidate attributes

```yaml
candidates:
  - ref: 007c7f8
    producers: [worker@claude]
    host: claude
    model: claude-opus-5
    at: "2026-09-18T12:30:00Z"
```

Optional, asserted attributes: use the host id, not the machine name, and the
exact model the host reports. Omit an unknown model, never write `unknown`.
For producers on different hosts or models, omit the mixed attributes rather
than selecting one. Candidate `at` means recorded at; it never orders entries.
`level` names the level a role ran at (`simple`, `standard`, or `complex`),
when its role file says so; omit it otherwise, and for producers at different
levels. An omitted level means unrecorded, not `standard`.

## Declaring requirements

Requirements are the one thing the toolkit checks. Declare only what you would
actually insist on, because every declared requirement must be satisfied before
the task can be set to `done`.

```yaml
requirements:
  checks: [test, lint]
  independent_review: true
  assessment_roles: [verifier]
```

Every requirement key goes under `requirements:`. Written at the top level, it
is a structural error, `requirement.misplaced`: lint fails and the task cannot
be set to `done` until the key is moved.

- `checks: [name, ...]` — each name needs a passing evidence entry for the
  current candidate. Name them after the project's real commands.
- `independent_review: true` — someone whose actor string is not among the
  candidate's producers must record an `accept`.
- `assessment_roles: [role, ...]` — each named role must record an `accept`.

`independent_review` asks for an accept from anyone who is not a recorded
producer; `assessment_roles` asks for an accept from a specific role. Declare
the second when a specific role's verdict is what you need.

A task with no `requirements` block is completely normal. Most tasks want
`checks` and nothing else.

Do not declare a requirement you intend to remove later to get a green result.
Removing it defeats the reason for writing it down.

When the owner accepts a check that fails, change the requirement deliberately
to exactly what they accepted. When they waive the whole check, remove it. When
they accept known failures within it, replace it with a narrower check under
its own name that excludes exactly those and still has to run and pass on the
candidate, so a new failure still shows. Cite their decision under
`## Blockers and decisions` and keep the failed evidence. A disposition is a
decision, not evidence: declare no check that passes by restating it.

## Status

`draft`, `agent_ready`, `in_progress`, `in_review`, `needs_revision`, `blocked`,
`needs_context`, `done`, `cancelled`.

Status describes progress. Any status may follow any other, and no status
grants a permission. The record stays readable and editable in every state.

Who sets it depends on who is working. When a coordinator runs the roles,
statuses are the coordinator's: a role it started records only `blocked` or
`needs_context`. An agent working alone sets status itself with
`npx --no castwork task set`, and `done` only once `task lint` shows the
declared requirements met. `done` does not wait for a verdict: work that went
straight
through may have no verifier, and its requirements decide.

## Sizing

One task is what one agent can finish in one sitting. If it needs phases, it is
several tasks. If it cannot be described without the word "and", check whether
the second half belongs in `## Out of scope`.

Alternatives worth a record get a task each, with shared acceptance criteria,
and a comparison task that depends on them records the choice. Each alternative
ends `done` or `cancelled`, set by whoever owns status: `done` when it
delivered, chosen or not; `cancelled` when abandoned, and it leaves the
comparison's `depends_on`. Never record alternatives as candidates of one task:
the checks read only the last one.

## Revising

Edit the file. It is Markdown and nothing objects. If the scope was wrong, fix
the scope and say why under `## Blockers and decisions` — a record that quietly
grew to match what was built is not worth keeping.
