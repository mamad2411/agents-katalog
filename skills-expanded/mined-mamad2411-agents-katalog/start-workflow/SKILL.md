---
name: start-workflow
description: Initialize one Workspace and authorize its first CodeBuddy Workflow Task from durable inputs.
---

# Start Workflow

Require an absolute Workspace path, one declared Workflow name, one readable
source PRD path, and a project ID. Run:

```powershell
python scripts/stage_control.py initialize --workspace <workspace> --workflow <workflow> --source <source-prd> --project-id <project-id>
```

Read the emitted JSON and current Workspace Status. Run `authorize` for the
recorded current Stage before creating a Task. The already-active top-level
`workflow-lead` creates the Task, with the required three-line
Workflow/Stage/Workspace metadata at the beginning of its description and of
its bounded child Agent prompt. Do not create `workflow-lead` through `Agent`.
Do not create any later Stage or Gate Task during initialization. The CodeBuddy
child-Agent start Hook performs the exclusive `claim`; do not run `claim`
manually.
