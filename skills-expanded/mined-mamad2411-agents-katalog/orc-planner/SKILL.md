---
name: orc-planner
description: "Produce acceptance criteria and a concise implementation plan; create dependency-linked tasks only when decomposition is requested."
---

# Plan a work unit

Read the task, feedback, affected code and relevant memory/KB decisions. Resolve
observable questions through inspection. Ask only for decisions the evidence cannot
settle. Preserve user scope and do not invent adjacent requirements.

Record the user-visible outcome, checkable acceptance criteria, approach, affected
boundaries, validation method, risks and immediate next action in a task comment.
Scale planning to the change. An ordinary feature needs a concise plan, not an
automatic tree of three to eight tasks or another flow.

If decomposition is requested, create only independently useful, verifiable work
units using task_batch_create with workflow assignments and dependency links.
Do not queue implementation before a required human planning gate is satisfied.

Record durable decisions with evidence and review knowledge inline before delivery.
Inside a flow, report the node's declared planning outcome and stop; do not set
the parent status to review or submit an implementation outcome. Outside a flow,
present the plan and follow the user's agreed task workflow.
