---
name: start-learning-path
description: >
  Enrol in a curated learning path. Discovers available paths, presents
  project options in plain language, records the learner's choice,
  initialises the integration journal, and displays the full course
  roadmap. Run once at the start of the path — not at the start of each
  course. Distinguishes enrolment (path level, one-time) from starting
  a course (delegates to start-course).
metadata:
  version: '1.0'
---

# start-learning-path

## What This Skill Does

Enrols the learner in a learning path. Discovers available paths, lets the
learner choose one (if more than one is available), presents that path's
project options, records the choice, creates the two progress files that
track path-level state, updates the active learning path in
`AGENTS-CUSTOM.md`, and displays the roadmap. Does not start the first
course — that is the learner's explicit next action via `start-course`.

This skill works for any learning path that conforms to the
`LEARNING-PATH.md` schema. Path-specific content (project options, course
sequence, integration tasks) is read from the path's definition; nothing
in this skill is hardcoded to a specific path.

→ Schema reference: `references/LEARNING-PATH-SCHEMA.md`

---

## Before You Start

Read these files — they must be in your context before continuing:

1. `references/LEARNING-PATH-SCHEMA.md` — the schema you'll be reading
2. `references/LEARNER-CONTEXT-TEMPLATE.md` — skeleton for the learner
   context file you'll generate
3. `references/INTEGRATION-JOURNAL-TEMPLATE.md` — skeleton for the
   integration journal you'll generate

---

## Instructions

### Step 1 — Identify the learning path

Scan `core/learning-paths/` and `custom/learning-paths/` for directories
containing a `LEARNING-PATH.md` file. Each is an available path.

- **One path found** — use it automatically. Confirm with the learner:
  "I found [title]. Starting enrolment?"
- **Multiple paths found** — list them by title and slug. Ask the
  learner which one they want to enrol in.
- **No paths found** — tell the learner there are no learning paths
  available and end the skill.

Record the resolved `<path-slug>` for use in later steps.

---

### Step 2 — Check for existing enrolment

Read `progress/<path-slug>/learner-context.md`.

**If it exists:** The learner is already enrolled. Read the file and display:

- Chosen project
- Current position (course they are on)
- Integration task checklist (which tasks are done)
- What to do next (the next incomplete course or the capstone)

Do not re-enrol. End the skill here.

**If it does not exist:** Proceed with enrolment.

---

### Step 3 — Read the path definition

Read `core/learning-paths/<path-slug>/LEARNING-PATH.md` (or the `custom/`
equivalent). Extract:

- Path title, target audience, estimated weeks
- `courses` list (slug, order, `integration-task-summary`)
- `project-options` list (slug, title)
- `capstone-title`
- The `## Project Options` markdown section (full briefs)
- The `## Integration Tasks` markdown section (per-course task variants)

---

### Step 4 — Orient the learner

Before presenting project options, explain in plain language how a learning
path works. The learner may have come to this skill cold — they need
context for the choice they're about to make.

**Part A — Shape (4–6 sentences):**

- **A learning path is a sequence of courses bundled around one project.**
  State the path's title, the number of courses, and the estimated duration
  (read from `estimated-weeks`).
- **You pick one project at enrolment, and it threads through every course.**
  Each course teaches a skill; the integration task at the end of the course
  applies that skill to your project. By the time you finish all the courses,
  every component of the project has been built.
- **The capstone at the end is assembly, not a new course.** Read
  `capstone-title` and describe what the learner will have at the end.
- **The project doesn't change mid-path** — pick one you'll be happy
  working with for the duration.

**Part B — What you'll build, course by course:**

Show a concrete table built from the path's `courses` YAML so the learner
can see what they will actually have produced by the end. Use
`courses[].title` for the course name and `courses[].integration-task-summary`
for the second column — both are read directly from the path YAML; do
not open each course's `COURSE.md`. Append the capstone row using
`capstone-title`.

```
| # | Course           | What gets built                       |
|---|------------------|---------------------------------------|
| 1 | [Course Title]   | [integration-task-summary]            |
| ...                                                          |
| — | Capstone         | [capstone-title]                      |
```

This grounds the abstract "you'll build a project" in concrete deliverables
the learner can evaluate against their goals.

No filenames, no framework terms. Then say something like: "With that in
mind, here are your project options."

---

### Step 5 — Present project options

Present the project options in plain language. No filenames, no framework
terms, no internal jargon. Use the full project briefs from the
`## Project Options` section — the core workflow example, the key design
decisions, and why each is a good vehicle. Give the learner enough
information to make a genuine choice.

Format as numbered options (one per `project-options` entry). Ask the
learner to choose.

---

### Step 6 — Record the choice

Wait for the learner's choice (number, slug, or title).

Resolve to the project slug from the `project-options` YAML list.

Read the learner's name from `profile/PROFILE.md` (use "Learner" if
not found).

---

### Step 7 — Create progress files

Read today's date for the enrolment timestamp.

**Create `progress/<path-slug>/learner-context.md`** from
`references/LEARNER-CONTEXT-TEMPLATE.md`. The template is a skeleton
with placeholders and one example checklist row. Generate the concrete
file by:

- Replacing top placeholders: `[Path Title]`, `[Learner Name]`,
  `[YYYY-MM-DD]`, `[project-slug]`, `[Project Title]`,
  `[first-course-slug]`, `[total-course-count]`
- Generating one checklist row per entry in the path's `courses` YAML
  list, in order. Each row uses `courses[].order`, `courses[].slug`, and
  `courses[].integration-task-summary` for the columns
- Appending a final capstone row using `capstone-title` from YAML

**Create `progress/<path-slug>/integration-journal.md`** from
`references/INTEGRATION-JOURNAL-TEMPLATE.md`. Generate by:

- Replacing top placeholders: `[Path Title]`, `[Learner Name]`,
  `[project-slug]`, `[Project Title]`, `[YYYY-MM-DD]`
- Generating one `## After <course-slug>` section per entry in `courses`,
  each with body `*Not yet completed.*`
- Appending a final `## Capstone` section with body `*Not yet started.*`

---

### Step 8 — Update AGENTS-CUSTOM.md

Update the `## Active Learning Path` section in `AGENTS-CUSTOM.md`.

Replace the placeholder content with:

```
**Path:** <path-slug>
**Project:** <project-slug> — <Project Title>
**Context:** progress/<path-slug>/learner-context.md
```

---

### Step 9 — Commit

```
git add progress/<path-slug>/ AGENTS-CUSTOM.md
git commit -m "progress: enrol in <path-slug> (<project-slug>)"
```

---

### Step 10 — Display the roadmap

Build the roadmap from the path's `courses` YAML — one line per course
showing `order`, `courses[].title`, and `integration-task-summary`.
Append the capstone using `capstone-title`. Do not read each course's
`COURSE.md` for this — `title` in the path YAML is authoritative.

Example shape (the actual course count and content depends on the path):

```
[Path Title] — your roadmap
Project: [Project Title]

Course sequence:
  1. [Course Title]    → Integration task: [integration-task-summary]
  2. [Course Title]    → Integration task: [integration-task-summary]
  ...

  Capstone: [capstone-title]
```

Then tell the learner in plain language:

> You're enrolled. Each course ends with an integration task that applies
> what you learned to your project — complete the task before moving to
> the next course.
>
> To start your first course, use `/start-course`.

Do not start the first course automatically. Enrolment and course start
are separate, explicit learner actions.
