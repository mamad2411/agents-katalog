> ⚠️ PROJECT SCOPED: Read/write .claude/tasks/ only.

Handles listing, adding, and picking up tasks.

## When called with no argument — show task board

1. Read all files in .claude/tasks/todo/
2. Read all files in .claude/tasks/inprogress/
3. Read last 5 files in .claude/tasks/done/

Report:

## 📋 Todo ([count])

| Priority                             | Task | Module | Effort | Added By |
| ------------------------------------ | ---- | ------ | ------ | -------- |
| [sorted: 🔴 first, then 🟡, then 🟢] |

## 🔄 In Progress ([count])

| Task | Module | Assigned To | Started |
| ---- | ------ | ----------- | ------- |

## ✅ Recently Done (last 5)

| Task | Module | Completed By |
| ---- | ------ | ------------ |

After showing list: "Pick a task? Tell me which one and I'll move it to in-progress and start."

## When called with argument — add a new task

e.g. /r-todo add authentication rework
Infer developer name from .claude/settings.local.json or git config user.name.
Gather or infer: title, module, priority (🔴/🟡/🟢), description, acceptance criteria, effort.
Save to .claude/tasks/todo/YYYY-MM-DD-[title].md with full template:

# Task: [title]

**Added By**: **Date Added**: **Priority**: **Module**: **Estimated Effort**: **Assigned To**: unassigned

## Description / ## Acceptance Criteria / ## Notes / ## Related Files

Confirm saved. Remind: commit and push.

## When the user picks a task from the list

Move .claude/tasks/todo/[file] → .claude/tasks/inprogress/
Add: Assigned To + Started date.
Then automatically run /r-task with the task description.
Remind: commit and push so team knows it is taken.
