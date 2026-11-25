---
name: verification-evidence
description: Use when recording what a check actually did — after running tests, a linter, a build, or a manual inspection. Covers candidates, evidence entries, and the difference between what was observed and what was claimed.
metadata:
  area: evidence
  side_effects: writes-files
  credentials: none
  runs_scripts: optional
---

# Verification evidence

Evidence says what happened to a specific candidate. It is not a summary and not
a promise.

## Record the candidate first

Evidence binds to an explicit reference, never to whatever the branch has become
since:

```yaml
candidates:
  - ref: 007c7f8
    producers: [worker@claude]
    host: claude
    model: claude-opus-5
    at: "2026-09-18T12:30:00Z"
```

`ref` is a commit when you may make one. When the work may not be committed
yet, take a snapshot instead: `npx --no castwork snapshot` prints a
`tree:<sha>` reference to exactly what is in the working tree, with ignored
files and `.castwork/local/` left out and `.castwork/tasks/`, `findings/` and
`reviews/` as the base commit has them, and you record that:

```yaml
candidates:
  - ref: tree:4697b75db8a9dbc2c4186c61d299e0069ce1388c
    producers: [worker@claude]
    host: claude
    model: claude-opus-5
    at: "2026-09-18T12:30:00Z"
```

Do not invent a digest of your own, and do not record a name such as `HEAD`, a
branch, or a worktree label: it keeps moving, so nobody can tell later what was
assessed, and lint notes it as `candidate.moving_ref`. If the CLI is not
available, say so and record the candidate as a label anyway; never invent a
reference.

Because a snapshot leaves ignored files out, it does not identify work kept in
ignored paths, such as a harness under a scratch directory. Say so, and name
those files and their hashes in the evidence that ran them.

A snapshot exists only in the clone that took it: it can be reviewed there,
including by an agent CLI working in the same checkout, but not from another
clone. For a reviewer elsewhere, use a commit the project authorizes, or send
the base commit and `git diff --binary --no-textconv <base> <sha>`; the reviewer applies it to a clean
checkout of the base and runs `snapshot`, and identical content gives the
identical `tree:` sha.

Evidence belongs to the bytes it ran on. Take the snapshot after your last
change and before your final evidence. If you change anything afterwards, take
a new snapshot, record it as a new candidate, and run again for it the declared
checks and the earlier observations the change could affect. Decide which from
what changed: the product code an observation ran, or the part of its
observer, oracle, classifier or fixture that produced or judged it, can affect
it even when the product is unchanged, as a fix to a shared false-pass
condition affects every result it judged; a change to a branch only another
case uses need not. An observation the change could not affect can still show
a criterion: cite it with its candidate and say why it still stands. So can a
declared check when the difference between the two candidates touches nothing
it reads, such as a plan document no test opens, or a test tool only another
check runs, as when only browser instruments changed and the unit and server
suites never load them: record an entry for the new
candidate with the earlier run's `check`, `result` and `command`, no
`exit_code`, and an `output` that begins `cited from <earlier ref>:` and names
the paths the difference touches and why the check reads none of them. A check
that reads any of them, or whose inputs you cannot tell, runs again. Inputs
outside Git count too, such as installed dependencies, environment settings, a
database's state, a served image or an external service: cite a check only
with the same invocation, where none of those it reads has changed since its
run, and never one whose purpose or the working policy needs a fresh
observation. Judge that from what the run read. State the run created and
removed for itself, such as a database built fresh for it, carries nothing
from one candidate to the next. A newer write time alone, such as a rebuild
of unchanged sources leaves, changes nothing; different contents or build
inputs do. What blocks a citation is an input you can name that could have
changed in a way that could affect the result: lacking a full record of the
machine is not that, but an input the result depends on that nothing
recorded, and that may have changed, is a gap to name, never an unchanged
input. Cite the entry that ran, by its `at` or linked output where
several share a check and candidate, never another citation, and give its
`command` as that entry records it, adding no value the record must not
hold. A verifier
confirms the difference with `git diff` before relying on the citation; where
Git or either candidate's objects are unavailable, it cannot be confirmed: run
the check again within existing authority, or name the gap.
`task lint` says whether the working tree still matches the current snapshot.

`producers` is who made it — the actor strings that later decide whether a
review was independent. Optional candidate `host`, `model`, and `at` are
asserted: use the host id and exact reported model; `at` means recorded at.
Omit an unknown model, never write `unknown`; omit mixed-producer host/model
attributes rather than picking one. These attributes never decide outcomes.

## Then the evidence

```yaml
evidence:
  - check: test
    candidate: 007c7f8
    result: pass
    command: "npm test"
    exit_code: 0
    host: claude
    model: claude-opus-5
    at: "2026-09-18T12:34:56Z"
  - { check: lint, candidate: 007c7f8, result: fail, command: "npm run lint", exit_code: 1, output: "logs/lint.txt" }
```

- `check` matches the name the task declared under `requirements.checks`.
- `candidate` is the `ref` you just recorded.
- `result` is `pass` or `fail`.
- `command`, `exit_code`, `output`, `actor`, `host`, `model`, `level`, `at` are optional.
  `level` is the level your role file says you run at; omit it otherwise.
  Record them when they help someone reproduce what you did.

`npx --no castwork task add <id> evidence check=test candidate=007c7f8 result=pass
command="npm test" exit_code=0 at=now` writes the same entry, and
`task add <id> candidate ref=... producers=...` the candidate. It takes only
these fields, refuses a `candidate` that is not a recorded `ref`, and fills in
nothing you did not give: `at=now` is the CLI's clock when it records.

Record `host`, the exact host-reported `model`, and an RFC 3339 `at` timestamp
when the record must remain self-contained or comparable without host-local
telemetry. They are asserted, informational metadata; document order still
decides which entry is effective.

`output` may be a short string, or a path to a file relative to the repository
root. A path that climbs out of the checkout with `..` is ignored rather than
reported.

Do not retain routine successful output. The entry's command, exit code and a
short observed result are normally enough. What a run produces, such as logs,
exit and pid files, dumps, captures, and the scripts of one-off probes, goes in
`.castwork/local/runs/<task>/`, which Git ignores and snapshots leave out; the
entry says what the run showed, so it reads without the file. Capture a
check's whole output there, not only a tail, and keep a failing run's before
you summarize or rerun it: a later pass does not recover what failed, while a
passing run's need not be kept. When long output
materially supports a failure, reproduction, or review finding, put it in a
linked file named under `output` rather than pasting a transcript into the
record. Link only where it lasts, not ignored scratch or `.castwork/tasks/`:
write it in `.castwork/findings/`, named after the task, such as
`T-012-test.log`. Copy the part it rests on, such as the lines that show the
result, not copied sources, archives or a whole run's output the entry already
states. A snapshot holds that folder as the base commit has it, without what
was written there since, so writing there never changes a candidate. A script a declared check runs is part of the candidate,
never there: a reviewer extracting the candidate must have it.

A routine successful probe is a sentence in the body, or nothing. An observation
supporting acceptance or a finding stays a candidate-bound evidence entry, under
its own name when undeclared. After a costly step, write a short observation:
what was seen, what it means, what is next; not a new narrative section per run.

## Rules that matter

- **Record what you ran.** An `exit_code` you did not observe is worse than no
  evidence at all. If you did not run it, on this candidate or, cited as above,
  on an earlier one, there is no evidence entry.
  Resolve a declared check to the project's actual invocation: working directory,
  paths, flags, environment and selection. Run that invocation within existing authority; a
  narrower or modified command is a different check and leaves the declared one
  unmet. If the invocation is unclear or cannot be run, name that gap.
- **Record what a later citation needs.** A costly run that may be cited for
  a later candidate records, in its `output` or a linked file, what it read
  outside Git that could change between candidates: the launcher and tool
  versions it resolved, the installed dependencies where the result rests on
  them, and the database, service or image it ran against, with whether the
  run created and removed it. Record versions and identities, such as an
  image digest, as they are; for an environment setting or other
  configuration, record its name and whether it was set, or the file or
  setup it came from, never its value or a secret. Only what that run read,
  and no dump of the whole environment. Without it, a later citation names
  the gap.
- **Record failures.** A `fail` is information. The later entry for the same
  check and candidate wins, so a `fail` after a `pass` correctly says the check
  is now failing.
- **Re-record after a new candidate.** Evidence for an earlier candidate is
  simply not applied to a new one. Nothing is invalidated and no diagnostic is
  raised — but the new candidate has no evidence until you record some, by
  running a check again or citing an earlier run as above.
- **A manual check is still evidence.** Name what you inspected and what you
  concluded. Do not invent an exit code for it.
- **Say what the run arranged.** A failure shown only under a condition the
  run itself arranged, such as an input built for the test, a state set up by
  hand, or a timing the test imposed, is recorded with that condition and with
  how, if at all, it arises in use: it shows the failure possible there, not
  that it happens. Whether it matters turns on what the criterion covers, not
  on the condition being arranged.
- **One command per entry.** `exit_code` belongs to a single command you ran
  and saw, never to prose or a chain of commands. In Bash and other POSIX
  shells a pipeline reports its last command's status, so `npm test | tail -50`
  gives `tail`'s exit code, not the check's, and `pipefail` reports a failure
  from any stage without saying which. Record the check's own status, such as
  `${PIPESTATUS[0]}` in Bash, read before running another command, or run it
  without the pipe.
- **Name the check honestly.** A subset of a declared check, such as some of
  the tests, goes under its own name, never under the declared check's name.
  A declared check that a larger command ran unchanged as a stage, such as a
  full gate that runs `check` first, takes its entry from that run where the
  output shows the stage finished: the larger command as `command`, and
  `exit_code` only where the whole command passed. Running it again only to
  have an entry under its name repeats work without adding evidence.
  `task lint` reports on the record, so it is not evidence about the candidate.
- **Say what decided the result.** Where an entry claims a particular guard or
  behaviour, keep the inputs it does not test valid, and say which cases or
  assertions decided the result and that they ran. A pass or a refusal that
  something else could have produced, such as another check refusing first or
  the test's own condition, does not show it. That a test passes now shows
  present behaviour; that it fails without the change is a separate showing.
- **Check what you derived.** A figure or class you built from another
  producer's output, by joining, classifying or totalling it, is checked
  against that producer before an entry or finding rests on it: the join
  matches the cardinality it intends and keeps each source's identity, totals
  reconcile over the population you state, and real examples try to falsify
  each materially different class. Name the cases left ambiguous or unmatched.
  A configured limit, such as a call ceiling, is not the usage it allowed.
- **Compare when attribution matters.** Reuse applicable baseline or batch
  evidence, or make a proportionate comparison within existing authority, using
  comparable commands, inputs and conditions. Matching baseline failures may
  establish non-introduction; they do not establish the cause. A pass in
  isolation shows a failure did not reproduce; it does not explain it either.
  A comparison that turns on which version ran shows it only where the run
  executed that version. A checkout, directory, version header or recorded
  commit names what was meant, while an installed or linked package, a path
  setting, or a counterpart copied in can run other code, child processes
  included: say how you know what ran, such as the path a module loaded from
  or the counterpart's files checked against their tag, and keep it with the
  entry. Do not require a fresh baseline run for every check or silently spend
  another run allowance.
- **Names, not secrets.** Record an environment variable's name, never its
  value: records are repository files, and the repository's own checks read
  them.
- **Say which clock.** `at` is in UTC with `Z`, or carries an explicit offset.
  A local time labelled `Z` is wrong by the offset.

## What the toolkit does with it

`task lint` reports each declared requirement as `satisfied`, `not_satisfied`,
or `unknown`, and marks each supporting fact **checked** (it observed it) or
**asserted** (you wrote it). Almost everything you record is asserted. That is
the honest state of affairs, and the report says so rather than pretending
otherwise.
