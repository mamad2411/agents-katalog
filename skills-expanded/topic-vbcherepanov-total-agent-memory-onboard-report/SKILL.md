---
name: onboard-report
description: >
  Department head / company viewer view of employee onboarding on the
  total-agent-memory team server. Use when the user types /onboard-report, asks how
  new employees are doing with training, who finished which module, quiz scores,
  wants to grade open quiz answers, or to build/edit the department curriculum or quizzes.
argument-hint: "[department id]"
---

# /onboard-report — onboarding results and curriculum

Tools are named `onboarding_*` (possibly client-prefixed). The server enforces
access: department heads (team role `manager`) see and manage their own
department; `company_viewer` and `superadmin` see every department; `superadmin`
may also manage. A `Forbidden` error means the user lacks that role — say so.

## 1. Pick the department

Use `$ARGUMENTS` if given. Otherwise call `onboarding_overview` and choose from
`viewable_teams` (report) or `manageable_teams` (editing).

## 2. Report

Call `onboarding_team_report(team_id)` and present:

- a table: employee × module with status (not started / in progress /
  quiz available / awaiting review / passed / failed), lessons done, best quiz
  score, and the relevant date (started, finished, passed);
- who is stuck (failed with no attempts left, or no activity) and lessons
  flagged as updated since people studied them (`summary.updated_lessons`);
- the latest entries of `log` in plain language.

For one person's detail: `onboarding_progress(team_id, user_id)`.

## 3. Grade open answers (department head)

For each item in `grading_queue`, show prompt, rubric and answer, ask the head
for points (0..`points`) and an optional comment, then call
`onboarding_grade(attempt_id, question_id, score, comment)`. Grading the last
open answer finalizes the attempt. Never grade without the head's decision.

## 4. Build or edit the curriculum (department head)

1. `onboarding_curriculum_get(team_id)` → current curriculum and `revision`.
2. For a first version, `onboarding_curriculum_draft(team_id)` groups the
   department's memory into modules/lessons (LLM-polished only if the server
   has one). Review it with the head: reorder, rename, remove, add lesson text.
3. Save with `onboarding_curriculum_set(team_id, expected_revision, curriculum)`.
   Keep existing `id`s so employees keep their progress; omitted items are archived.
4. Quizzes per module: `onboarding_quiz_draft(module_id)` (needs a server LLM;
   drafts are checked against lesson quotes) or write questions with the head,
   then `onboarding_quiz_set(module_id, expected_revision, questions)`.
   Question types: `single`, `multiple` (zero-based `correct` indexes), `open`
   (needs `rubric`). Set `pass_threshold` and `max_attempts` per module in the
   curriculum.

Always show the head what will be saved before calling a `*_set` tool.
