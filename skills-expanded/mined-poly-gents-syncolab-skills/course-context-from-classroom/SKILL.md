---
name: course-context-from-classroom
description: Sync Google Classroom course metadata into academic-learning-context and living docs so course TAs stay syllabus-aware.
---

# Course context from Classroom

## Purpose

Pull **authoritative course structure** from Google Classroom (courses, topics, coursework, announcements) and merge it into **`academic-learning-context`** / SKS living docs so practice TAs reference the right syllabus, deadlines, and materials.

## When to Use

- After Google Classroom is connected on Integrations.
- When the lecturer binds a TA to a specific course or topic.
- When announcements or coursework changed and context looks stale.

## When NOT to Use

- Student tutoring mid-session → **course-practice-ta-session-flow**.
- Scheduling → **calendly-office-hours-scheduling**.

## Expected Outcome

- Updated context doc sections: **Courses**, **Schedule**, **Tooling**.
- Clear note of which Classroom `courseId` this TA serves.
- Links or summaries of recent announcements when relevant.

## Workflow

1. Verify Classroom connection with **`classroom_list_courses`**.
2. List courses; confirm target **`courseId`** with the lecturer.
3. **`classroom_get_course`** for name, section, room, courseState.
4. **`classroom_list_topics`** and **`classroom_list_coursework`** — map units to living-doc headings.
5. **`classroom_list_announcements`** — capture policy changes (deadlines, AI rules, exam dates).
6. Propose patches to **`academic-learning-context`** via SKS (`sks_docs_propose_patch`) — lecturer approves before treating as canonical.
7. Store stable IDs (courseId, topic ids) in living docs for future sessions.

## Anti-patterns

- Guessing course ids from names alone.
- Copying full roster or grades into chat logs — summarize policies, redact student identifiers.
