---
name: create-course
description: >
  Scaffold a new course directory from the COURSE.md schema. Creates
  the directory structure, populates COURSE.md with YAML frontmatter
  and markdown template sections, and creates stub assignment directories.
  Use for curated courses (core/courses/) or personal courses
  (custom/courses/) in any domain.
metadata:
  version: '1.0'
---

## Purpose

This skill scaffolds a new course directory with a properly structured
COURSE.md. It works for both curated courses (`core/courses/` — community-
contributed, upstream-managed) and personal courses (`custom/courses/` —
user-owned, never upstreamed). The output is a ready-to-edit COURSE.md
with structure in place — the author fills in the details, then learners
use `/start-course` to begin.

Upstack is domain-agnostic. The course being created could teach Go
programming, management accounting, network administration, project
management, or anything else that can be taught through productive
struggle.

---

## Before You Start

Read these files — they must be in your context before continuing:

1. `references/COURSE-SCHEMA.md` — the full COURSE.md schema with
   YAML frontmatter fields, markdown body structure, and formatting rules
2. `core/courses/go-lang-for-developers/COURSE.md` — the reference
   course. Read this to calibrate what a well-structured COURSE.md looks
   like: YAML frontmatter, assignment descriptions, suggested milestones,
   design questions, paradigm shift flags, scope notes, topic checklists,
   and reasoning review prompts. Match its register and depth when
   generating the new course scaffold.

---

## Procedure

### Step 1 — Gather course details

Ask the author for the following. Suggest sensible defaults where
possible (e.g., derive slug from title).

1. **Course location** — "Is this a curated course for the community
   (`core/courses/`) or a personal course (`custom/courses/`)?"
   - **Core:** upstream-managed, community-contributed, reviewed.
     Use for featured courses and catalogue content.
   - **Custom:** user-owned, stays in the learner's fork, never
     upstreamed. Use for personal learning goals.
2. **Course title** — "What is this course called?"
3. **Slug** — suggest a kebab-case slug from the title. Confirm with
   the author.
4. **Domain** — "What domain does this course belong to?" Offer:
   - languages
   - system-design
   - architecture
   - engineering-practices
   - soft-skills
   - domain-knowledge
5. **Target Dreyfus level** — "Who is this course designed for?" Offer:
   - **Novice** — no prior exposure to this subject
   - **Beginner** — some exposure, can follow instructions
   - **Competent** — can work independently on routine tasks
   - **Proficient** — strong working knowledge, sees the big picture
   - **Expert** — deep expertise, learning nuance and edge cases
6. **Target audience** — "Describe the ideal learner in 1–2 sentences.
   What background and prior knowledge should they have?"
7. **Modules and assignments** — "How many modules? How many assignments
   per module? Give me a brief title for each assignment."
8. **Prerequisites** — "Does this course assume prior courses or
   knowledge? If none, that's fine."
9. **Milestones** — "For each assignment, what's the natural order of
   work? What would you tackle first, second, third?" These become
   suggested milestones in the COURSE.md.
10. **Design questions** — "What decisions should the learner think
    through before they start working? What trade-offs or structural/design
    choices will they face?" These are posed by the tutor before
    execution (see TUTOR-CONTRACT.md §10.3).
11. **Paradigm shifts** — "Does the learner come from a different
    paradigm? Which topics will conflict with their existing instincts?"
    If yes, flag those topics with paradigm shift annotations.
12. **Scope boundaries** — "Is there domain knowledge the learner needs
    but isn't here to learn? (e.g., an API, a data format, a business
    process)" If yes, add scope notes telling the tutor to scaffold
    that knowledge so struggle stays focused on the course subject.

Move through the questions conversationally. If the author has a clear
vision, this can be quick. If they're exploring, help them think through
the structure. Items 9–12 can be deferred to a refinement pass if the
author wants to scaffold first and refine later.

### Step 2 — Create directory structure

Create the course directory under the chosen location
(`core/courses/` or `custom/courses/`):

```
<location>/<slug>/
├── COURSE.md
└── references/
    └── .gitkeep
```

The course directory contains curriculum and reference material only.
Learner work lives in the learner's own separate workspace — each
assignment is a self-contained project, not a subdirectory of the course.

### Step 3 — Generate COURSE.md

Populate using the schema from `references/COURSE-SCHEMA.md`:

- **YAML frontmatter** — fill all required fields from gathered inputs.
  Set `created` and `updated` to today's date. Set `author` from
  `profile/PROFILE.md` if it exists, otherwise ask.
- **Course description** — write a brief summary from what the author
  described. The author will refine it.
- **What You Will Learn / Learning Objectives** — generate placeholders
  based on the assignment titles. Mark them as TODO for the author to
  refine.
- **Course Structure** — create module headings, assignment headings,
  suggested milestone placeholders, design question placeholders,
  and topic placeholders (`- [ ] Topic — TODO: describe`). Add
  paradigm shift annotations if identified in Step 1. Add scope
  notes if domain scaffolding boundaries were identified.
- **Reasoning Review Prompts** — add placeholder prompts per assignment.
  These should be refined by the author before the course is used.

### Step 4 — Confirm

Show the author a summary:
- Course title and slug
- Directory structure created
- Number of modules, assignments, and placeholder topics

Note that COURSE.md is a scaffold — the author should edit it to fill
in topic details, learning objectives, and reasoning review prompts
before running `/start-course`.

### Step 5 — Commit

```
git add <location>/<slug> && git commit -m "course: scaffold <slug>"
```

---

## Authoring Guidelines

- **Assignments are projects, not exercises.** Each assignment should
  produce something meaningful — a system, a workflow, a model, an
  analysis. "Build a REST API client" or "Create a quarterly budget
  forecast" is an assignment. "Write a for loop" or "Add two cells"
  is not.
- **Topics are learnable concepts, not task steps.** "Understand
  goroutine scheduling" or "Master double-entry bookkeeping" are topics.
  "Create a file" or "Run the tests" are tasks.
- **Milestones are a suggested order, not rigid steps.** Each milestone
  names one thing to produce and one concept that emerges. The tutor
  adapts them to the learner's pace. Milestones help the tutor sequence
  the assignment and give the learner a sense of progression.
- **Design questions drive struggle before execution.** Pose decisions
  the learner must resolve before starting work. Target trade-offs and
  structural decisions, especially where prior instincts mislead.
- **Paradigm shift flags help the tutor bridge.** When the learner's
  prior knowledge will actively conflict with a topic, flag it. The
  tutor can then anticipate the conflict and apply bridging rather
  than teaching from scratch.
- **Scope notes separate learning from scaffolding.** If an assignment
  requires domain knowledge that isn't the course subject, tell the
  tutor to help with it. The learner's struggle should stay on the
  course topic, not on deciphering an API or a business rule.
- **Reasoning review prompts test understanding, not recall.** "Explain
  why you chose this approach over the alternative" — not "What function
  did you use?"
- **Domain-agnostic language in the schema.** The COURSE.md structure
  works for any domain. Don't assume the course is about programming.

---

## Reference

- COURSE.md schema and field reference: `references/COURSE-SCHEMA.md`
- Tech spec §3: full schema specification with parsing rules
