---
name: /complete-plan-and-merge
description: move plan to completed, merge to develop, cleanup branch
disable-model-invocation: true
---

Move the plan md from plans/ to plans/completed/. Commit. Push the current task branch. Checkout develop. Merge the task branch into develop using --no-ff. Push develop. Delete the task branch locally and on the remote. Reply here when done.

$ARGUMENTS
