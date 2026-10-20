---
name: orc-tasks
description: "Create and track ORC work with acceptance criteria; use flow outcomes for managed agents and explicit transitions for manual tasks."
---

# Track work in ORC

Call context first, then inspect task_list/task_get before creating or claiming work.
The task body records acceptance criteria, constraints and expected artifacts.
Use a readable project name on MCP operations.

## Managed development

Choose orc-default for development, orc-human-review when human sign-off is needed,
or orc-review-only for existing work. Set skill_name to orc-coder or a specialized
workflow; development defaults to orc-coder when the task has no skill.
Use task_batch_create with dependency links only when separate work units are useful.

The flow owns task status. Agent nodes report flow_report with the exact outcome
listed in their prompt, then stop. Do not set review/done to move a flow, approve
your own work, or start the next node. Use flow_status to inspect the current run.

Human nodes wait for the human. The dashboard gate or orc flow resume supplies the
declared approval/rework outcome and feedback. Review rounds and retry limits bound
rework. required_review controls agent review in orc-default; orc-human-review always
requires both agent review and human sign-off, even when that task flag is false.

## Manual tasks

Outside a managed flow, use the explicitly agreed status transitions through
task_update. Read existing claims and review feedback before working. Human approval
belongs to the human; do not imply every agent review is a human approval.

Progress belongs in task comments/session events. Preserve the artifact, verification,
risks, relevant knowledge and next action at each handoff. Memory/KBs are for durable
knowledge, not a second task board. Use orc-session and orc-memory-review for continuity.

CLI operations include orc task add/show/note and orc flow attach/status/resume.
Only invoke destructive or publishing operations when authorized by the user/project.
