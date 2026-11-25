---
name: project-os-task
description: Prepare a scoped Project OS task with testable acceptance criteria and approval references.
---

# project-os-task

Read AGENTS.md, .project-os.json, planning/decisions.md, planning/flow.md and planning/tasks/_template.md.
Draft one task for one repository in the shapes from planning/formats.md, with scope, branch, dependencies, risk flags, stable criterion IDs and a verification plan.
Use observable outcomes and real project evidence. Never invent a build command, approval, model result or completed task.
Drafting within authorised planning scope is allowed; product code waits for applicable scope/code approval.
Run node .project-os/check.mjs --workspace . after editing records and fix every finding. Record dated CHANGED criteria before redispatching altered work. Update the board and route essential decisions through PM.
Delegate implementation to project_os_developer only after permission and dispatch checks pass.
