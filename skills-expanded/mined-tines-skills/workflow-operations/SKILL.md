---
name: workflow-operations
description: Add production operating behavior to a workflow. Use for schedules and event triggers, completion or failure notifications, targeted retries, operational logging, and follow-on automation.
license: Apache-2.0
compatibility: Tines 3B
---

# Workflow operations

Add operating behavior from the workflow’s real reliability requirements:

- Choose a schedule or event trigger that matches when the source data becomes ready.
- Notify only people who can act, and include the workflow, run, outcome, and next action.
- Retry transient operations with bounded attempts; surface permanent or exhausted failures.
- Log stable identifiers and decisions needed to trace a run without recording secrets or redundant payloads.
- Build follow-on automation as another composable workflow when it has an independent trigger, owner, or lifecycle.

For scheduled work on named volumes, use `workflow-volume-design`. Keep each run bounded, keep input until the change that applied it is published, and verify that pending work drains faster than it arrives. A completed run alone does not establish that the schedule is keeping up.

Run the workflow with representative input after changing its operating behavior.
