---
name: start-course
description: >
  Initialise a learning session. Checks for an existing journal in
  progress/<course-slug>/journal.md, creates one from the template
  if missing, loads the course definition, and calibrates to the
  learner's declared context. Use when starting a new course or
  resuming after a break.
metadata:
  version: '1.0'
---

## Purpose

This skill sets up a learning session. It handles two scenarios:

- **New course** — creates the journal and learner context, calibrates
  the tutor, and orients the learner on what's ahead.
- **Resuming** — loads existing progress, recalibrates, and picks up
  where the learner left off.

The skill ensures the tutor never starts cold. By the time the learner
begins working, the tutor knows who they are, what course they're
taking, and where they are in it.

---

## Before You Start

Read these files — they must be in your context before continuing:

1. `references/JOURNAL-TEMPLATE.md` — journal scaffold with
   placeholders and scribe instructions
2. `references/LEARNER-CONTEXT.md` — measurement checklist for the
   learner context interview, output format, and interview tips

---

## Procedure

### Step 1 — Identify the course

Scan `core/courses/` and `custom/courses/` for directories containing
a `COURSE.md` file. Each is an available course.

- **One course found** — use it automatically. Confirm with the
  learner: "I found [title]. Starting that one?"
- **Multiple courses found** — list them by title and slug. Ask the
  learner which one they want to start.
- **No courses found** — tell the learner there are no courses
  available and suggest using `/create-course` to scaffold one.

### Step 2 — Read the course definition

Read the selected `COURSE.md`. Extract:

- Course title, slug, and domain
- Target Dreyfus level and target audience
- Course Structure section — modules and assignments (titles,
  descriptions, topic checklists)
- Reasoning Review Prompts per assignment
- Prerequisites (if any)

If the course has prerequisites, check whether the learner has
completed them (look in `progress/` for completed journals). Warn
if prerequisites are unmet — but don't block. The learner decides.

### Step 3 — Create or load the journal

Check if `progress/<slug>/journal.md` exists.

**If it does not exist (new course):**

Create the journal from `references/JOURNAL-TEMPLATE.md`:

1. Copy the template content below the `<!-- JOURNAL START -->` marker
2. Replace placeholders:
   - `{course-title}` — from COURSE.md title
   - `{learner-name}` — from `profile/PROFILE.md` if it exists,
     otherwise ask the learner
   - `{start-date}` — today's date (YYYY-MM-DD)
   - `{progress-tracker}` — generate from COURSE.md assignments:
     ```
     - [ ] **Assignment 1: Title**
     - [ ] **Assignment 2: Title**
     ```
   - `{assignment-sections}` — generate one section per assignment
     using the Per-Assignment Section Structure from the template:
     ```markdown
     ## Assignment N: Title

     **Goal:** {from COURSE.md assignment description}

     ### What I Attempted

     ### Mistakes and Corrections

     ### Got It Right

     ### What Clicked
     ```
3. Write to `progress/<slug>/journal.md`. Create the
   `progress/<slug>/` directory if it does not exist.

**If it does exist (resuming):**

Read the existing journal. Note which assignments are completed
(checked in the Progress Tracker) and which is next.

### Step 4 — Create or load the learner context

Check if `progress/<slug>/learner-context.md` exists.

**If it does not exist (new course):**

Interview the learner using `references/LEARNER-CONTEXT.md` as the
measurement checklist. Walk through all 6 fields conversationally:

1. **Prior Skills Relevant to This Course**
2. **Mental Models Being Brought In**
3. **Level in This Subject** (offer the Dreyfus scale)
4. **Prior Exposure to This Subject**
5. **Learning Preferences**
6. **Prior Upstack Courses Completed**

Before asking, read the course's target audience and target Dreyfus
level from COURSE.md — the garment spec tells you what body type this
garment is designed for. Use it to ask better questions.

If `profile/PROFILE.md` exists, read it first. Some answers may
already be covered by the profile — acknowledge what you already know
and probe for course-specific details rather than re-asking generics.

Write the answers to `progress/<slug>/learner-context.md` using the
output format defined in the template.

**If it does exist (resuming):**

Read the existing learner context. Do not re-interview.

### Step 5 — Commit progress files

If new files were created in Steps 3–4:

```
git add progress/<slug>/ && git commit -m "progress: start <slug>"
```

If resuming with no new files, skip this step.

### Step 6 — Update AGENTS-CUSTOM.md Active Course section

Read the root `AGENTS-CUSTOM.md` file. Find the `<!-- start-course -->`
comment. Replace everything from that comment up to (and including) the
`---` separator that follows the Active Course content with:

```markdown
<!-- start-course -->
## Active Course

**Course:** {title}
**Slug:** {slug}
**Path:** {core/courses or custom/courses}/{slug}/COURSE.md
**Journal:** progress/{slug}/journal.md
**Learner Context:** progress/{slug}/learner-context.md

---
```

This ensures the tutor has the active course in context on every
session load without needing to re-run the skill.

### Step 7 — Calibrate

Read calibration sources in this order:

1. `profile/PROFILE.md` (if it exists) — the learner's full
   background across all courses. See
   `.agents/skills/core/configure-profile/references/PROFILE-TEMPLATE.md`
   §"How the Tutor Reads the Profile" for per-section guidance.
2. `progress/<slug>/learner-context.md` — course-specific context.
   How this learner's background applies to this particular course.

Profile first (who you are), then context (how your background
applies here). Together they tell you:

- What analogies will land (prior skills + mental models)
- What level to pitch at (Dreyfus level in this subject)
- What transfer errors to watch for (mental models from other domains)
- How to interact (learning preferences)

### Step 8 — Summarise and orient

Present the learner with a brief summary:

**For a new course:**
- Course title and what it covers (1–2 sentences from COURSE.md)
- Number of assignments and their titles
- Where to begin (Assignment 1)
- A note that the journal will be maintained automatically

**For a resuming learner:**
- Where they left off (last completed assignment, or current
  in-progress assignment)
- What's next
- Any relevant context from the journal (last session's key
  takeaways, if available)

End with an invitation to begin: "Ready to start Assignment 1?" or
"Ready to pick up where you left off?"

---

## Notes

- **The learner context interview is a conversation, not a form.**
  Ask one question at a time, respond to the answer, then move on.
  See `references/LEARNER-CONTEXT.md` §Tips for the Tutor During
  Measurement for guidance on probing, overstatement/understatement,
  and using the conversation itself as calibration data.
- **Don't block on missing profile.** If `profile/PROFILE.md` does
  not exist, the learner context alone is sufficient for calibration.
  Suggest running `/configure-profile` later for richer calibration
  across future courses, but don't require it.
- **Commit before the interview, not after.** If the journal is
  created but the learner context interview hasn't started yet, don't
  commit. Wait until both files exist (or just the journal, if
  resuming and context already exists), then commit once.

---

## Reference

- Journal template and scribe instructions: `references/JOURNAL-TEMPLATE.md`
- Learner context measurement checklist: `references/LEARNER-CONTEXT.md`
- Profile reading guidance: `.agents/skills/core/configure-profile/references/PROFILE-TEMPLATE.md`
- Tech spec §6.3.1: full skill specification
