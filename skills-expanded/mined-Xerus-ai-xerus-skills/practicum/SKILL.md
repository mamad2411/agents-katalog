---
name: practicum
description: >-
  Runs a course's practical task. It proposes three real build targets in the
  user's live codebase, then builds the chosen one WITH the human as a pair:
  the human makes the design calls and a decision log is kept as the work
  happens. Finally a separate, blind grader scores two things: the artifact,
  against the course's acceptance criteria, and how well the human directed
  the agent, against a six-dimension orchestration rubric. Works on Markdown
  course folders (courses/{slug}/ with a 99-practicum.md spec) and can draft a
  spec with the human when a course has none. Use when the user says
  "/practicum {course}", "do the practical task", "let's build the capstone",
  "apply what I learned", "practice this on my real code", or has just
  finished a course's lessons or recall quiz. Interactive only. The tutor
  explains and the practicum builds.
---

# Practicum

A course has three acts. The lessons teach the material, a recall test shows
it stuck, and the practicum shows it is **usable**. It does that by building
something real in the learner's own codebase and having someone other than
the builder grade it.

Two things get graded, because two things are being learned:

1. **The artifact.** Does what was built meet the course's own acceptance
   criteria? The rubric is the course's practicum spec.
2. **The orchestration.** Did the human direct the agent well? The rubric is
   `references/orchestration-rubric.md`, and it is the same for every course.

The second one is why this is done with an agent at all. The learner is
practising the topic, and also practising getting things built this way.

## Files in this skill

| File | Read it when |
|------|--------------|
| `references/course-format-minimum.md` | Finding the course, reading its spec and progress, or when the course has no spec |
| `references/practicum-record.md` | Step 3 (writing the record) and throughout the build (the decision log) |
| `references/orchestration-rubric.md` | You never apply it yourself. It goes to the grader |
| `references/blind-grading.md` | Step 5: choosing a grader, the grader prompt, the fallbacks |
| `scripts/grade_bundle.py` | Step 5: builds the evidence-only bundle the grader sees |

## Input

- `course`: a course slug or path. If absent, find courses using
  `references/course-format-minimum.md`, list those that have a
  `99-practicum.md`, and ask which one.
- If there is no course folder but the user names a topic they studied,
  follow "No conforming course" in that same reference.

## Hard rules

- **The builder never grades, and the grader never builds.** No informal
  verdict, no "I think that went well", no provisional score, not even when
  asked. If there is no grade yet, say "not graded yet".
- **The human makes the design calls.** Quietly picking the good option takes
  away exactly the learning the practicum exists for.
- **Never invent check output.** If the acceptance check did not run, the
  criterion is `unverified`, and that is the finding.
- **Secrets are never read or written in any mode**: `.env*`, key files,
  credential stores, `secrets/`-style directories. If a task needs them, it is
  the wrong task.
- **Interactive only.** A practicum is a pairing session. If there is no human
  to answer (a headless or scheduled run), write one line saying why and stop.
- **Bounded.** When about 80% of the budget is spent (the time box the human
  set, or your context/token budget), stop building. Ship what exists, grade
  it honestly as partial, and record what was left undone.

## Procedure

### 1. Gate on recall

A practicum is not a substitute for knowing the material. The order is
lessons, then recall test, then practicum, and it is deliberate: on material
the learner cannot recall, the build turns into dictation.

Read `{course-dir}/progress.md`. The gated concepts are the spec's
`concepts:` that appear on a **lesson line** (`01`..`NN`) of the index's
concept map. Concepts found only on the `- 99:` line are **exempt**. No lesson
teaches them, so they never get a status, and exercising them is the
practicum's own job. Look up each gated concept:

- All `learning` or `retained`: the gate passes (`recall_gate: passed`).
- Any concept `new` or absent (never studied): stop and say which ones. If a
  tutor skill is installed (for example one that reads this course format),
  offer to run a recall pass with it first, then re-check. If none is
  installed, offer a short screen: ask the `probe` from `assessment.md` for
  each missing concept. The human answers from memory, and you compare the
  answer against `must_include`. The screen only catches "cannot recall it at
  all". If it passes, set `recall_gate: screened`. Do not record it as a
  grade, and never write it into concept status; that belongs to the tutor.
- Any concept `lapsed`: recommend a review first, and let the human decide.
- No `progress.md` at all: ask whether they have worked through the course. A
  yes gives `recall_gate: no-record`.

Whatever happens, log the outcome as a `GATE` entry. The human may override
the gate explicitly ("skip it, I want to build"): log that as `OVERRIDE` and set
`recall_gate: overridden`. The grader needs this context. An ungated learner
leaning hard on the agent means something different from a gated one doing
the same.

### 2. Propose three targets

Read the spec: concepts under test, acceptance criteria, shape of a good task,
anti-tasks. Also read the previous attempts in `{course-dir}/practicum/`, if
any. Their "one thing to do differently" lines carry forward.

Then **look at the live codebase**, not at what the course assumed. If the
spec's shape of a good task depends on history (for example "a failure that
has happened at least twice"), search the real history for it: commits,
issues, TODOs, logs. Propose exactly **three** concrete tasks, spread across
modes where the codebase allows:

| Mode | Where it writes | Use it for |
|------|-----------------|------------|
| `in-repo` | The user's working tree | The strongest option when the concept applies to code the user owns. Real writes and real consequences. The repo's own tests, linters and build must still pass afterwards. |
| `patch-only` | Only `attempt-NN/` (a patch file plus rationale) | Code the agent must not modify: a dependency, vendored or generated code, another team's service, anything the user puts off-limits. The patch is **read** against the target and never applied by the agent. The human applies it by hand if they want it. If a task cannot be expressed as a patch, it is the wrong task for this mode. |
| `greenfield` | A new directory the human approves (default `{course-dir}/practicum/attempt-NN/build/`) | Nothing real fits, or the honest task really is to build something from nothing. Also the way out for a task the course did not anticipate. |

Each proposal takes **three lines at most**:

1. **Build**: what you would build, and where.
2. **Forces**: which spec concepts it makes the learner use.
3. **Done when**: the acceptance check. Make it concrete, and runnable where
   possible (a command, a test, a grep, a before/after measurement).

**A proposal with no acceptance check is not a proposal.** Rework it or drop
it. Also drop any proposal that matches one of the spec's anti-tasks. If the
codebase honestly has fewer than three good targets, do not pad the list with
near-duplicates. Offer the ones that exist plus one `greenfield` option, and
say that is why.

Offer them all in **one** question. Use the environment's multiple-choice
question tool if it has one; otherwise use a numbered list and wait. The human
picks one or redirects. If they name their own target, shape it into the same
three lines and confirm it before starting.

### 3. Contract the task

Before any build work, write `{course-dir}/practicum/attempt-NN.md` from the
template in `references/practicum-record.md`. NN is the next free number. Fill
in the frontmatter (including `base` and `preexisting_changes` when the target
is in git), and the Task and Acceptance criteria sections. Put the previous
attempt's "one thing to do differently" in the Task section. Create the
`attempt-NN/` evidence folder.

In `progress.md`, set `practicum: in-progress`, bump `updated:`, and append
a new `### YYYY-MM-DD — practicum` entry whose first bullet is
`- attempt NN: started, target {target}`.
Create `progress.md` in the minimum shape first if it does not exist.

### 4. Build as a pair, logging decisions as you go

These pairing rules stop the practicum from becoming the agent doing homework
while the human watches:

- **At every fork, give the options and the trade-off in one or two lines,
  and let the human choose.** A fork is any choice where a reasonable engineer
  could go either way and the course's concepts bear on it. Mechanical choices
  that don't touch those concepts are not forks. Make them and move on.
- **Do the work you are asked to do.** Pairing is no excuse to hold back
  execution. Once a direction is chosen, build it properly and completely.
- **Say when you disagree**, once, with a reason. Then follow the decision.
- **Do not steer the human toward the rubric.** Do not coach them to "ask for
  proof" or "write the check first" so they score well. What they do on their
  own is what is being measured. You may, and should, show evidence with every
  claim you make. That is ordinary honesty, not coaching.
- **Append to the decision log as things happen**, not at the end, in the
  format and with the event types in `references/practicum-record.md`. The log
  is the grader's only evidence for orchestration. A thin log gives a thin
  grade, and that is itself an honest finding.
- **Save raw check output** to `attempt-NN/check-{n}.txt` every time the
  acceptance check runs. The first lines of each file give the exact command
  and the commit it ran against (`git rev-parse HEAD`, plus "with uncommitted
  changes" when the tree is dirty), so the grader knows what the output
  belongs to. Where a criterion is a check, run it against a
  deliberately bad case as well as the real one: a check shown only passing
  has not been shown to work.
- **In `patch-only` mode**, never write to the target. Write
  `attempt-NN/change.patch` plus `attempt-NN/rationale.md` (what it changes,
  why, how to apply it, how to check it). Run the checks you can without
  applying it, and mark the rest `unverified`.

### 5. Blind grade

Follow `references/blind-grading.md`. In short:

1. Build the bundle with the script. It includes only the spec, the rubric,
   the record's Task, Acceptance criteria and Decision log sections, the diff
   or files, and the raw check output:

   ```
   python {skill-dir}/scripts/grade_bundle.py --spec {course-dir}/99-practicum.md \
     --record {course-dir}/practicum/attempt-NN.md \
     --git-base {base} --path {target paths} \
     --check-output {course-dir}/practicum/attempt-NN/check-1.txt \
     --out {course-dir}/practicum/attempt-NN/grade-bundle.md
   ```

   Run it **from the repository root**, giving the script's path (for example
   `python .claude/skills/practicum/scripts/grade_bundle.py ...`, or wherever
   the skill is installed). `--path` values are relative to the repository
   root. When `--repo` is not given, the script uses the git repository that
   contains the record. Use `--diff-file attempt-NN/change.patch` for
   `patch-only` and `--files ...` for `greenfield`. Treat its warnings (thin log, empty diff, missing check
   output) as findings, not as things to fix by editing the log after the fact.
2. Get the grade from something that did not watch the build. Try, in this
   order: a subagent with a fresh context; a fresh headless process from an
   installed agent CLI; or the human carrying the bundle to a new session. Set
   `grader:` to whichever was used.
3. Paste the grade into `## Grade` verbatim. If there is no grader yet, set
   `status: awaiting-grade` and stop. Never fill the gap yourself.

The grader returns two sections. **Artifact** gives a verdict per criterion,
the anti-task drift, and findings marked BLOCKING or MINOR. **Orchestration**
gives the six dimensions, each score cited to a log entry, and the one
behaviour to change next time.

### 6. One improvement round, then stop

Fix what the grader marked BLOCKING, re-run the acceptance check, save the
output, and log the round (`D{n}` entries continue). **One round, capped.** A
practicum that needs three rounds is telling you the task was too big. Record
that finding instead of grinding on. Only the human can override the cap, and
it is logged as `OVERRIDE`.

### 7. Record

- **Record**: `status: graded`, and fill in `## Result` (see
  `references/practicum-record.md`).
- **`progress.md`**: set `practicum: done`, bump `updated:`, and append a new
  `### YYYY-MM-DD — practicum` entry (never add to the one written at the
  start). Its bullets give `- attempt NN: graded`, what was built, the
  artifact verdict, the orchestration score as `{n}/{5k} over {k} evidenced`,
  and the one behaviour to change.
- **Patterns**: if the same orchestration dimension has been the weakest in
  three attempts (this course or others in the same courses root), name it in
  the progress entry as a recurring pattern, and cite the three attempt files.
  Fewer than three is not yet a pattern. Don't call it one.
- Tell the human, briefly: what exists now, where the record is, the one
  behaviour to change. Give no commentary of your own on the grade.

An abandoned attempt keeps its record (`status: abandoned`, one line in Result
saying why) and puts `progress.md`'s `practicum:` back to its previous value.

## Anti-patterns

| Looks like | Why it fails |
|------------|--------------|
| Proposing targets from the course's examples instead of the real code | Tests recall of the lesson, not transfer. The practicum exists to test transfer. |
| "Here's what I'd suggest…" then building it | The agent made the design call. The log should show `agent-default`, and the learning is lost. |
| Filling in the decision log at the end | It becomes the builder's narrative, which the grader must not see. |
| Handing the grader a summary "for context" | Breaks blindness. The bundle is the whole input. |
| Scoring orchestration yourself "to save a step" | Builder grading builder. Status stays `awaiting-grade` instead. |
| A second and third improvement round | The task was too big. Record that and stop. |
| Check shown only passing | Not yet shown able to fail. Seed a bad case. |
| A patch-only task that "just needs one small edit" to the target | Mode violation. The patch is the deliverable. |
