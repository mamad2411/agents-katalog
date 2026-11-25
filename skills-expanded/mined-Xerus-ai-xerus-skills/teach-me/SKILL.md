---
name: teach-me
description: >-
  Interactive tutor over a course folder (index.md + numbered lessons + assessment.md, as written
  by a course-builder skill or by hand). Teaches lesson by lesson with generation-first
  questioning, checks understanding with free-recall questions of randomly drawn practical types,
  grades answers against the course rubric through a separate blind grader (or an explicit
  point-by-point rubric check when subagents are unavailable), and keeps the learner's record and
  a simple spaced-review schedule in progress.md inside the course folder. Use when the user says
  "teach me {course}", "/teach-me {course}", "continue my course", "quiz me", "review what's due",
  "where am I in the course", or asks to study a course that already exists in the repository.
  Live, human-in-the-loop sessions only - it does not build courses and does not run unattended.
---

# Teach Me

Tutor a person through a course that already exists as a folder of Markdown files. Three
functions, one experience: **explain**, **check**, **track**. The course is the syllabus; this
skill is the teacher; `progress.md` is the record.

Files in this skill:

| File | What it holds |
|---|---|
| `references/course-format.md` | the parts of the course folder this skill reads |
| `references/progress-format.md` | `progress.md` shape, statuses, the review schedule rules |
| `references/questioning.md` | the seven question types and the questioning discipline |
| `references/grading.md` | grade rules, the blind grader brief, inline fallback, bad rubrics |
| `scripts/progress.py` | stdlib helper: status, due reviews, grading arithmetic, log, random draw |

Script paths below are relative to this skill's folder. If Python is unavailable, apply the
rules in `progress-format.md` by hand - exactly, never by feel.

## 0. Preconditions (check before tutoring)

- **A human is present.** Tutoring is a live conversation. If this skill is invoked with no one
  to answer (a scheduled job, a batch run, a pipeline), write one line saying tutoring needs a
  learner at the keyboard and stop. Never simulate the learner's answers.
- **A course exists.** Find courses by the rules in `course-format.md` (explicit path, then
  `courses/*/index.md`, then any `index.md` with `kind: course`). No course named: list the ones
  found (title, lessons completed from their `progress.md`) and ask which. None found: say so; if
  a course-building skill is available, suggest it; otherwise stop. Do not improvise a course.
- **The course is gradable.** `assessment.md` must have an entry for a concept before that
  concept can be graded. Missing entries: teach anyway, but say plainly those concepts cannot be
  marked retained, and never make up a rubric on the spot to grade against.

## 1. Load state

```
python scripts/progress.py status {course-dir}
```

That prints each lesson's concept states, lessons completed, the next lesson with untaught
concepts, and how many reviews are due. Read `index.md` for the title, objectives and lesson
list. If there is no `progress.md` yet, this is the first session - it is created on the first
recorded grade or log entry.

Tell the learner where they are and what is ahead **in one line**, not a lecture. Then offer the
session plan (reviews first if any are due, then the next lesson) and let them change it.

## 2. Session shape

**Due reviews first, then new material.** Memories due for review are at their most valuable
moment to retrieve; new material can wait ten minutes.

### 2a. Reviews

```
python scripts/progress.py due {course-dir}
```

For each due concept, most overdue first, **interleaved** across lessons (never all of one
lesson in a row): draw a question type, write a fresh question from the concept's
`assessment.md` entry (`python scripts/progress.py item {course-dir} {concept}` prints it), ask,
grade (section 4), record. Cap a sitting at about 15 reviews; the rest stay due for next time.
Never show `must_include` points before the answer.

### 2b. Teaching the next lesson (generation first)

Read ONLY the current lesson file - progressive disclosure keeps the explanation anchored to
what the course actually says. For each concept in the lesson (its `### ... (\`concept-id\`)`
section), in order:

1. **Predict.** Before explaining, ask one short question that makes the learner commit to a
   guess: "what do you think happens when...?" Ungraded. A wrong guess is fine - struggling
   first makes the explanation stick.
2. **Explain.** Concept first, then a concrete example, then its connection to earlier lessons.
   Resolve their prediction explicitly: what they got right, what the guess missed. Plain
   language; define any term in the sentence that introduces it. Use the lesson's worked example
   or common mistakes - but never the concept's `probe` or `transfer` situation (that would
   spoil the check).
3. **Explain it back.** Ask the learner to say the idea in their own words, in a sentence or
   two. Ungraded; correct misunderstandings now, gently and specifically.

The learner sets the pace: "next", "again", "slower", "skip", "example please" all work. A
`threshold` concept (see `weight` in the assessment) gets more time and an extra example. If the
learner stalls on a concept, check the `## Concept dependencies` in the index and re-teach what
it builds on first.

**Check at the end of the lesson, not after each concept.** Once every concept in the lesson is
taught, give one graded question per concept, in an order different from the teaching order
(any order will do - it only has to break the sequence you just taught in). The small delay turns the
check into real recall rather than repeating what was said a minute ago.

## 3. Questions

Follow `references/questioning.md`. The essentials:

- Seven practical types - find the break, fix it, predict, symptom to cause, pick and defend,
  tell them apart, push back. Draw the type at random each time
  (`python scripts/progress.py draw`), redraw only if the type truly cannot express the idea.
- The `probe` is a reference; the question asked is new, and it is what the grader receives.
- Code in a question carries a plain comment on each meaningful line saying what it does.
- Re-read the question against the rubric before asking: never put the answer in the setup.
- No multiple choice for anything graded.
- **No verdict before the grade** - no "right", "exactly", "good start" between the answer and
  the grade.

## 4. Grading

Follow `references/grading.md`. Grading independence is the point of this skill:

- **If the host can run subagents**, grade each answer with a fresh blind grader that receives
  only: the concept id, the question as asked, the `must_include` points, the listed
  misconceptions, and the learner's answer verbatim. Nothing from the conversation, the lesson,
  or your opinion of the answer.
- **Otherwise**, grade inline *before reacting*: list the applicable rubric points, quote the
  evidence for each or mark it missing, check the misconceptions, apply the grade rule, and only
  then reveal - showing the working. Log it as `grader: inline`.

Grades are `recalled` / `partial` / `missed`. Grade the idea, not the words. Record each one:

```
python scripts/progress.py grade {course-dir} {concept} {recalled|partial|missed}
```

Then give the feedback. After `partial` or `missed`, re-teach the missing point from a new angle
and move on - the schedule brings it back (the script prints the date: tomorrow after a miss,
sooner than usual after a partial; rules in `progress-format.md`). Tell the learner the date the
script printed, never a guess. A second graded attempt the same day is reported by the script as
PRACTICE and does not move the schedule; do not try to get around that, and note the practice
result in the session's log entry yourself (the script does not log it).

## 5. Track

`progress.md` (inside the course folder) is the learner's record. Its shape and every rule are
in `references/progress-format.md`; `scripts/progress.py` does the arithmetic:

- **Concept status** - `new` / `learning` / `retained` / `lapsed`, updated by each grade.
- **Review schedule** - a Leitner box per concept: a recall moves it up a box and pushes the
  next review out (2, 5, 12, 30, 75, 180 days); a miss drops it to box 0, due tomorrow.
- **lessons_completed** - recomputed: lessons whose concepts are *all* currently `retained`.
  A lesson is never complete until each of its concepts earned a `recalled` from the grader -
  enthusiasm in the conversation never counts.
- **Log** - append-only, one dated entry per session.

## 6. Session end

1. Write the session's log entry to a temporary file and append it:
   `python scripts/progress.py log {course-dir} --file {entry.md}` (the entry is headed
   `— tutoring`; say in its first line if the session was reviews only). Contents: concepts
   taught, each grade with the grader path used, misconceptions shown (quote briefly), confident
   misses, same-day practice results, and any study pattern worth remembering next time (e.g.
   "keeps confusing X with Y - revisit lesson 02's common mistakes"). Never edit earlier entries.
2. Tell the learner, in one or two lines: what was covered, how it went in grades (not
   praise), when the next reviews fall due, and what comes next.
3. When every lesson is complete, point to the course's `99-practicum.md`: recall is done, the
   next step is building something with it (a practicum skill, if installed, runs that).

## Optional integration

If the course index names an `engram_topic` other than `none` / `pending-install` **and** the
engram learning plugin (https://github.com/nagisanzenin/engram) is installed, you may run the
session through it and mirror its concept states into `progress.md`: after the session, set
each concept's status line to engram's state for that concept (untouched = `new`, still being
learned = `learning`, in review = `retained`, relearning after a lapse = `lapsed`) and recompute
`lessons_completed`; the engine wins on conflict. If it is not installed, ignore the key
and use this skill's own schedule - everything above works without it.

## Guard rails

- **Writes:** only `progress.md` in the course folder (plus temporary files for log text,
  deleted afterwards). Lessons are read-only. An `assessment.md` entry is changed only for a
  confirmed rubric defect, with the learner's explicit approval, concept id unchanged
  (`grading.md`).
- **Never answer for the learner**, never grade an answer they did not give, never record a
  grade without applying the rubric.
- **Never show the rubric as teaching material** - `must_include` points are the grading
  contract. Show them after an answer is graded, as the explanation of the grade.
- **No gamification** - no points, streaks, badges or levels. The motivator is the real thing:
  "this idea now comes back in 12 days instead of 2".
- **Honest records** - the log says what happened, including misses and inline grading. A lapse
  lowering `lessons_completed` is correct, not something to smooth over.
