---
name: course-ta-setup-playbook
description: Lecturer-facing Agent Studio setup — connect integrations, bind Classroom course, seed living docs, and smoke-test a course practice TA in the playground.
---

# Course TA setup playbook

## Purpose

Guide the **lecturer** (not students) through configuring a Reichmann-style course practice TA: integrations, context docs, template hire, and validation.

## When to Use

- First-time setup for a new course or semester.
- Lecturer hires **`university-course-setup-advisor`** or asks "how do I configure my מתרגל?"
- After OAuth or Classroom course structure changes.

## When NOT to Use

- Live student tutoring → **course-practice-ta-session-flow**.

## Expected Outcome

- Integrations connected: Classroom, Calendly, and relevant Google services.
- Living docs + **`academic-learning-context`** drafted and approved.
- One digital employee hired from **`university-course-practice-ta`** with course id documented.
- Playground smoke test passes (`classroom_list_courses`, optional `calendly_list_event_types`).

## Setup checklist

1. **Integrations page:** connect Google Classroom, Calendly, Drive/Docs/Sheets/Calendar/Gmail as needed.
2. **SKS / living docs:** create course binder (syllabus rules, integrity policy, OH policy).
3. **Classroom bind:** run **course-context-from-classroom**; confirm `courseId`.
4. **Calendly:** run **calendly-office-hours-scheduling**; store event type URI in living docs.
5. **Agent Studio:** hire **`university-course-practice-ta`**; attach initiative files if used.
6. **Playground:** clock in; ask agent to list courses and summarize syllabus sections from context.
7. **Iterate:** adjust allowed tools/skills only via template policy — do not expose raw lecturer corpus to students in this phase.

## Notes

- Multiple practice TAs = multiple hires (one per course/topic), each with scoped context.
- Student/public embed is **out of scope** until a later phase.
