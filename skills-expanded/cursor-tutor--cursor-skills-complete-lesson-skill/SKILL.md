---
name: complete-lesson
description: Writes the lesson summary, updates .data/STUDENT.md mastery, and advances the current-lesson pointer when a lesson end goal is met. Use when the student has met the current lesson end goal or the tutor confirms the lesson is complete.
---

# Complete Lesson

## Instructions

1. Confirm the current lesson’s **end goal** in `curriculum/CURRICULUM.md` is met. If not, stop and say what is still missing.
2. Create the summary file (create the section folder if needed):

   `curriculum/lesson_summaries/NN-section-slug/N.N-lesson-slug.md`

   Example: `curriculum/lesson_summaries/01-your-computer-as-a-workshop/1.1-files-folders-and-the-terminal.md`

3. Write the summary with these headings:

   - **Concepts** — ideas from the lesson
   - **Commands / APIs** — commands, functions, or APIs they used
   - **What you built** — files or artifacts they created
   - **Open questions** — optional; omit the section if none

4. Update the `# Current lesson:` line at the top of `curriculum/CURRICULUM.md` to the next lesson, if there is one. If this was the last lesson in a section and the section end goal is met, follow the `section-review` skill **before** archiving anything (section-review still needs the live `CURRICULUM.md`). If this was the last lesson of the **last** section (the course is finished):
   - **Map exists and `.data/IN_MASTERTRACK_CURRICULUM` is `on`:** after section-review, follow `.cursor/skills/mastertrack/complete-step.md`. Do not treat the journey as over. Do not write the next course.
   - **No map, or flag `off` / missing:** set the current-lesson line to a clear “complete” note as usual.
5. Follow the `student-profile` skill: set this lesson’s Skills-table row to `mastered` or `shaky` from how independently they finished, set the next lesson to `learning` if needed, and refresh strengths / growth areas if a pattern showed up.
6. Do this bookkeeping without waiting to be asked. Then tell the student the lesson is done and what the next lesson is — unless `complete-step.md` ran, in which case wait after the celebration.

## Do not

- Advance if the end goal is not met.
- Overwrite an existing summary unless correcting a mistake the student agrees with.
- Start teaching the next lesson in the same breath as a long dump — name it, then wait for them to begin.
- After a mastertrack course ends, auto-start the next map item or write the next `CURRICULUM.md`.
