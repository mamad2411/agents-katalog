---
name: github-triage
description: Fixture for project skill tool reference tests.
---

Task tracking examples must use the real task management tool names:

```text
task_create(subject="Triage: #{number} {title}")
task_update(id=task_id, status="completed", description=REPORT_SUMMARY)
```

