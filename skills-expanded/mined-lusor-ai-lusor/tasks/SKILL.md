---
name: tasks
description: Tasks to-do app (org.tasks); read, filter, create and complete tasks and their due dates. Use whenever the task involves the Tasks app.
keywords: [tasks, to-do, todo, task list, due date, completed, incomplete, overdue]
platform: android
app_package: org.tasks
---

A row's checkbox is the `completeBox` ImageView, its completion toggle: one tap completes or reopens the task and rewrites its completion time. Open a task with its `rowBody` index, printed just before `completeBox`; never use the index printed after the row, which is `completeBox`. The title TextView has no index. On a question, never touch `completeBox` or the list's view options, such as Show completed. If you tap `completeBox` by mistake, tap it once more to restore the status, confirm it on screen, then report in `done()` that the completion time changed.

A due label with only a weekday (“Tue”, “Tuesday 22:06”) is not a date, and the task's own screen may show only the weekday too. For each such task whose date matters, open it and tap its due date: the date picker marks the due day Selected. Read the full date (if the month is not in the screen text, take one screenshot of the picker), then leave with Cancel or Back, never OK. Never infer one task's date from another's or from the current week.

“My Tasks” can include completed tasks when “Show completed” is enabled: completed rows have a checked box and a struck-through title, while incomplete rows have an empty box. The `completeBox` ImageView may expose no checked state in the UI tree, so read its appearance in a screenshot or open the task via `rowBody` and scroll to the bottom, where a completed task shows a “Completion” timestamp.
