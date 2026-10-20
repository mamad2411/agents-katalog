# Frontend development

Carry out the user's task as a Vue.js/React frontend developer.

## Before you start

Read @CLAUDE.md and @.docs/FRONTEND.md (if present) — they are the law.

## Implementation

Launch Agent(subagent_type: "frontend-expert") with the user's task.

Give the agent the full context: what has to be done, which components are affected.

## After implementation

Launch in parallel:

Agent(subagent_type: "architecture-validator"):
- Check the code that was written

Agent(subagent_type: "code-critic"):
- Code review of the code that was written

If there is a BLOCK/FAIL — fix it through Agent(subagent_type: "frontend-expert") and run the check again.

Show the user the result.
