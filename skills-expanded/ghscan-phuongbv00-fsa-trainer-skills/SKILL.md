---
name: fsa-training-material
description: Write and check FSA teaching material. Produces lecture notes, module handbooks, module appendices, and the step-by-step lab guides a session plan calls for, and cross-checks a module's materials against the plan that asks for them. Use when asked to "viết bài giảng", "soạn tài liệu", "viết lab", "tạo lecture notes", "write a lecture note", "write a lab guide", "write the module handbook", or "check which materials are missing".
---

# FSA training material

Writes the teaching material a session plan calls for, and checks that what the
plan promises exists.

## What this skill does not own

A session row in a programme's plan names the file that serves it. Producing
*that file* is this skill's job when it is teaching material, and someone else's
otherwise.

| Artifact | Skill |
|---|---|
| quiz questions, assignment briefs, exams, rubrics, grading | `fsa-training-assessment` |
| session plans, syllabi, schedules, module structure | `fsa-training-program` |
| lecture notes, handbooks, appendices, lab guides | this one |

A lab guide is the guided middle: shorter than an assignment, step-numbered,
checkable by the learner. If it carries marks and a rubric it is an assignment,
and it belongs to the assessment skill. Say so rather than writing it here.

## This skill is stateless

It knows nothing about the directory structure it was installed into and assumes
nothing about the project around it. **Every path it touches is one the user
gave it.**

> **Do not list, glob, read, or run anything until every required Step 0 value
> below has a confirmed value.** The only file you may read before that point is
> one the user has just named in this conversation.

The one path you legitimately know is `SKILL_DIR` — the directory containing the
`SKILL.md` you are reading right now.

## Step 0 — Collect inputs

Ask only for what is missing, and batch the questions.

| Key | Required for | Default |
|---|---|---|
| `materials_dir` | all | ask; never assume |
| `schedule` | authoring, coverage | ask — the topic's ScheduleDetail CSV |
| `syllabus` | objectives checks, the appendix | ask |
| `document_kind` | authoring | infer from the request, then confirm |
| `index` or `lab number` | authoring | derive from what is already in the folder |

**A note serves a session.** Before writing, find the row in the session plan
that names the file: it gives the objective codes, the minutes, and one line
saying what happens. Write to that, and say so in the plan echo.

Before writing anything, report the resolved **absolute** paths, the filename,
and the session it serves. Wait for an explicit go-ahead.

## Resolving the CLI

Do this once per session, before the first command, and call the result `FSA`.

1. Read `.fsa-trainer-skills-install.json` next to this `SKILL.md`; use its
   `cli.invocation` array, adding its `pythonpath` to `PYTHONPATH`.
2. Otherwise try `fsa-trainer-skills --version` on `PATH`.
3. Otherwise stop and ask the user to run `pip install fsa-trainer-skills` or
   `npm install -g fsa-trainer-skills`. Do not improvise a path to a script.

A receipt written on another machine names an interpreter that does not exist
here; when its invocation fails to run, fall through to option 2. If option 2
reports a version different from the `VERSION` file beside this `SKILL.md`, say
so — payload and CLI ship in lockstep.

`FSA` is the **bare CLI**, with no subcommand attached. This skill's own work
runs under its namespace — `FSA material verify` — while the lifecycle commands
every skill shares take no namespace: `FSA doctor`, `FSA status`, `FSA update`.
A worker verb written without its namespace resolves to nothing.

## Step 1 — Route to the workflow

Read **exactly one** workflow file — the one matching the confirmed intent.

| Intent | Workflow |
|---|---|
| write a lecture note | `references/workflows/author/lecture.md` |
| write a lab guide | `references/workflows/author/lab.md` |
| write the module handbook | `references/workflows/author/handbook.md` |
| write or refresh the module appendix | `references/workflows/author/appendix.md` |
| read a verification report | `references/workflows/verify/report.md` |
| find out what material is missing | `references/workflows/coverage/gaps.md` |

Supporting material, read as needed rather than up front:

| File | Holds |
|---|---|
| `references/structure.md` | every template and every rule, generated from the checker |
| `references/conventions.md` | register, callouts, code style, the language rule |
| `references/templates/` | skeletons for each kind of document |
| `references/examples/` | a small, complete, correct module |

## Commands

| Command | Does |
|---|---|
| `FSA material verify PATH...` | check documents against the template their names claim |
| `FSA material coverage --schedule CSV --dir DIR` | what the plan asks for versus what exists |
| `FSA material derive appendix --syllabus MD --dir DIR --appendix MD --write` | rebuild the appendix's syllabus map |

## Standing rules

- **Write to the session, not to the topic.** A note covering more than the
  session it serves is a note that session cannot deliver.
- **The syllabus map is derived, never typed.** Its deep anchors break silently
  when a heading is renamed.
- **English by default.** A translation is a separate file whose stem ends
  `_vn`, never a rewrite of the original — everything else links to the original.
- **Report measurements, not impressions.** "12 of 12 notes pass, 3 labs the
  plan names are missing" is a measurement.
- **Do not invent work the plan did not ask for.** If a module needs a session
  that is not there, the session plan changes first, and that belongs to
  `fsa-training-program`.

## Step 2 — Report back

List every file written with its full path and the session it serves, the
`FSA material verify` result with its rule ids, and — when material was missing
— which of the gaps belong to another skill.
