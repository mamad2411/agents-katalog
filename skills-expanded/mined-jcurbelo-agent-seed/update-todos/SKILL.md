---
description: Interactive todo review. Walk through open items, get status updates, update the file.
---

# /update-todos - Interactive Todo Review

## Step 1: Load Today's Todos

Read `todos/YYYY-MM-DD/todos.md` for today's date. If it doesn't exist, ask if the user wants to create one.

## Step 2: Present Open Items

Show all unchecked items as a numbered list:

```
Here are your open items:

1. [HIGH] Task description
2. [HIGH] Another task
3. [MED]  Medium priority task
4. [LOW]  Low priority task

What's the status? You can say things like:
- "1 done" / "1,2 done"
- "3 blocked on X"
- "4 drop"
- "move 3 to high"
- "add: new task description"
```

## Step 3: Process Updates

For each update:
- **done** -> mark `- [x] ~~text~~`
- **blocked** -> add "(blocked: reason)" to the item
- **drop** -> remove the item
- **move** -> move to the specified priority section
- **add** -> add new item to the specified (or default medium) priority

## Step 4: Save

Update the todo file. Do NOT commit — the user may want to make more changes.

Show the updated summary: "Updated X items. Y remaining."
