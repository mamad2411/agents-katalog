---
name: assessment
description: Use when reviewing or auditing an implementation against its task record and recording a verdict, and when responding to a verdict you received. Covers the three lenses, independence, and what accept, reject, and needs_revision mean.
metadata:
  area: review
  side_effects: writes-files
  credentials: none
  runs_scripts: optional
---

# Assessment

An assessment is one actor's verdict about one candidate. It is recorded in the
task record and nowhere else.

```yaml
assessments:
  - candidate: 007c7f8
    role: verifier
    actor: verifier@codex
    verdict: accept
    host: codex
    model: gpt-5.6
    at: "2026-09-18T13:02:10Z"
    findings: "..."
```

`npx --no castwork task add <id> assessment candidate=007c7f8 role=verifier
actor=verifier@codex verdict=accept findings="..."` writes the same entry under
the record's lock, so parallel lenses recording at once lose nothing.

`verdict` is `accept`, `reject`, or `needs_revision`. Record `host`, the exact
host-reported `model`, and an RFC 3339 `at` timestamp when the record must stay
self-contained or comparable without host-local telemetry. They are asserted,
informational metadata. Add `level` when your role file names the level you
run at; a level is chosen for the assessment's difficulty and creates no
independence.

`findings` is a short quoted string, a linked file relative to the repository
root, or an anchor to a heading in the body. Long findings go under a heading,
where they can be read and revised, not inline in the frontmatter. Do not
reproduce tool transcripts or a full audit report in the record: say what you
found: the contract item, observation and location, and why it blocks or accepts.
Not a walk through every file read or a restatement of earlier rounds. Link only
support that lasts, not ignored scratch or `.castwork/tasks/`: write it in
`.castwork/findings/`, named after the task, such as `T-012-review.md`. The
output of your own runs goes in `.castwork/local/runs/<task>/`, and is copied
into findings only where a finding rests on it. Record the verdict once the
checks it rests on have finished.

## Three lenses, in order

Judge risk, scale and what is consequential against the project's expected
use, as `.castwork/project.md` or the record's plan states it; where neither
does, say which use you assumed.

1. **Does it do what the record asked?** Read `## Intent` and
   `## Acceptance criteria` first, then the change. Work that is good but not
   what was asked for is still not what was asked for.
2. **Is it correct?** Look for the failure the tests do not cover: the empty
   case, the second call, the error path, the concurrent one. Inspect the
   candidate's changes to the tests, fixtures, thresholds and scripts its
   checks use: a case a criterion relies on that was removed, skipped or
   loosened, for no reason the work gives, leaves that criterion unshown.
   Where a criterion rests on an observation of an earlier candidate, check
   the record's reason that the change since could not affect it: a change
   that could, in the product code it ran or in the part of its observer,
   oracle, classifier or fixture that produced or judged it, leaves that
   criterion unshown until it runs again. The declared checks run on the
   candidate you assess, or one is cited from its run on an earlier candidate,
   its `output` beginning `cited from <earlier ref>:`: confirm with `git diff`
   between the two that the difference touches nothing it reads, that the
   invocation is the same, and that nothing outside Git it reads, such as
   installed dependencies, environment settings or a database's state, has
   changed, and that neither its purpose nor the working policy needs a fresh
   observation, and treat a citation you cannot confirm, where Git or a
   candidate's objects are unavailable included, as unshown. An input outside
   Git blocks a citation only where you can name it and how its change could
   have affected the result; state the run created and removed for itself is
   not one, nor is a newer write time alone. An input the result depends on
   that nothing recorded, and that may have changed, is a gap to name. A
   declared check that a larger command ran unchanged as a stage counts where
   its output shows the stage finished. A run of a
   declared check an assessing actor recorded on an earlier candidate, yours or
   another session's, you may cite the same way, never a producer's:
   independence is your judgement of the evidence, not a repeat of every
   command. Run again what would settle an uncertainty that matters to the
   verdict.
3. **Would this project want to maintain it?** Consistency with the surrounding
   code counts. So does the concept count — a change that adds a new idea
   should be paying for it. A finding names the concrete burden, such as a
   concept, option, layer or test a reader must carry, and a simpler
   alternative that keeps the contract; that an abstraction exists, or has one
   implementation, is not a finding. A limit the candidate names, such as a
   size, a load or a case it leaves out, is a choice, not an oversight: it is a
   finding only where it fails a criterion, a declared requirement or what the
   user committed to, such as safety or data integrity, or the expected use
   already reaches it. A test, check or option the candidate
   added for a mechanism shows what the mechanism does, not that the work needs
   it: judge that need from the record and the mechanism's users. A missing
   test is a finding only with the consequential failure it would catch and the
   gap in coverage; a defect you observed is a defect whether or not a test is
   needed.

## Read the candidate

Assess the candidate the record names, not the current branch. If the reference
does not resolve in your checkout, say so and assess nothing rather than
assessing something else.

A reference resolves when it is a commit that exists here, or a `tree:<sha>`
snapshot whose tree object exists here. A name such as `HEAD` or a branch is
not the candidate, even when it resolves: it names whatever it points at today.
Neither is a label such as a worktree name. Say so, and ask for the commit id
or a snapshot.

A snapshot is not the working tree. `task lint` says whether the working tree
still matches it; if it does not, the files in front of you are not the
candidate. A snapshot holds `.castwork/tasks/`, `findings/` and `reviews/` as
the base commit has them, so its copy of the record can differ from the live
one, which is the contract; lint leaves those folders out of drift, and a
difference there is not drift. Read the
candidate's contents with plain git, or extract it into a scratch
directory outside the repository through a temporary index. Both extraction
commands run with `GIT_INDEX_FILE` set to that temporary file: without it,
`read-tree` overwrites the repository's real index. The path must be absolute,
since git resolves a relative `GIT_INDEX_FILE` against the top of the working
tree:

```sh
git diff <base> <sha>                 # what the candidate changes
git show <sha>:<path>                 # one file as the candidate has it
# <tmp> is an absolute path to a scratch directory outside the repository
mkdir -p <tmp>/tree
GIT_INDEX_FILE=<tmp>/index git read-tree <sha>
GIT_INDEX_FILE=<tmp>/index git --work-tree=<tmp>/tree checkout-index -a
```

A snapshot exists only in the clone that took it. Reviewing from another clone,
ask for a commit the project authorizes, or for the base commit and
`git diff --binary --no-textconv <base> <sha>`: apply the diff to a clean checkout of the base and run
`npx --no castwork snapshot` there. Identical content gives the identical
`tree:` sha, which proves you hold the candidate.

Do not accept on the strength of a summary. If you did not read it, your verdict
is about the summary.

## Independence

`independent_review` compares your `actor` string against the candidate's
recorded `producers`. If you are among them, your `accept` does not satisfy it —
and recording a different `role` does not change that. Roles are presets;
independence is about who did the work.

`independent_review` asks for an accept from anyone who is not a recorded
producer; `assessment_roles` asks for an accept from a specific role. When a
particular role's verdict is what the work needs, the record should declare
`assessment_roles: [verifier]` rather than leave it to an instruction — and when
that role is unavailable, say so in the findings rather than quietly standing
in for it.

The two requirements are evaluated separately, so together they do not prove
that the verifier was independent: a producer's own `verifier` accept satisfies
`assessment_roles`, and anyone else's accept satisfies `independent_review`. If
you produced the candidate, do not record the verifier's verdict on it.

Write an actor string that identifies you honestly, for example
`verifier@codex`, or the specialist name you were started as, such as
`security-reviewer@codex`. Two reviewers whose verdicts on one candidate must
both stand never share an actor: the checks keep the last assessment per actor,
so a second verifier under the same name replaces the first one's verdict. For
the same reason, assessing again a candidate your actor already assessed,
whichever session records it, continues that assessment and replaces its
verdict: do it once a change to the criteria, scope or evidence it judged bears
on its findings, starting from those findings and naming as a limit any change
you cannot see, never as a second try. Never choose a name to avoid matching a
producer. The toolkit compares strings and reports them as asserted; it cannot
tell whether the string is true, and it never claims to.

## Verdicts

- **`accept`** — say what you checked and name what you did not, so the next
  reader knows the shape of your confidence.
- **`needs_revision`** — the work is close; name precisely what must change.
- **`reject`** — the approach is wrong; say what would be right.

A finding blocks, as `needs_revision` or `reject`, only where it fails an
acceptance criterion, a declared requirement, or what the user committed to,
such as safety or data integrity. Record any other finding as not blocking,
beside an `accept` when nothing else blocks, as a proposal for follow-up work
rather than another round. A failure shown only under a condition the run
itself arranged, rather than one that arose in use, is reported with that
condition and with how, if at all, it arises in use, and blocks only where the
criterion, or what the user committed to, covers that cause; where nothing
written settles whether it does, say that the verdict turns on that boundary.
Where a blocking finding rests only on a criterion the agents added or
tightened once the work was under way, which the user never confirmed, say so
in the finding: it questions that criterion as much as the candidate.

`reject` and `needs_revision` are ordinary outcomes. Record them plainly. The
requirement stays unsatisfied until you record a later verdict, which is exactly
what should happen — and the record stays editable throughout.

## Being assessed

Read the findings before defending anything. Fix what is right, and say clearly
where you disagree and why rather than silently not doing it. A disagreement
cites something the assessor could have read, such as a file and symbol, a
criterion, or a recorded decision; that a choice was intended is not that.
Where the reason is written nowhere, the gap is in the record: say so, for the
thinker or the user to settle and write down, rather than arguing the finding.
A dispute settled earlier does not hold against new evidence. Treat each finding
as an example of its kind: fix the same defect wherever the candidate has it
within the scope of the work, and say where you looked; name an occurrence
outside that scope as a proposal rather than fixing it. After `needs_revision`
or `reject`, or a follow-up someone chose to make, record a new candidate and
fresh evidence for what changed: the old evidence belongs to the old candidate.
A finding answered by correcting the task record alone, which snapshots leave
out, asks for no new candidate: say in the record what the correction changed
and when, and the assessor's actor assesses the same candidate again. Record no
evidence entry for it, since nothing ran. A finding recorded as not blocking
beside an `accept` asks for no new candidate: the accepted one stays accepted,
and the finding is follow-up work.

## Be specific

"The retry loop has no bound" is a finding. "Looks good" is not. One concrete
defect is worth more than a list of possible concerns.
