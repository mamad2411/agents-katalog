---
name: agent-group-usage
description: Use this skill when the user needs to create agents, join rooms, send messages, publish tasks, claim tasks, deliver results, or inspect task status inside an agent-group collaboration space. Guide the model to choose the right tools, call them in the right order, and fill in missing prerequisites before taking the main action.
---

# agent-group Usage Guide

This skill helps the model use a set of MCP tools for multi-agent collaboration more reliably. The goal is not to list tools mechanically, but to choose the right tool for the user’s objective, call tools in the right order, and move the task forward based on the result.

## When To Use This Skill

Use this skill when the user wants to:

- create or inspect their agents
- create a room or enter an existing room
- see room members and exchange messages between agents
- publish claimable tasks
- claim tasks and submit results
- inspect task status, the taskboard, or a task subtree

If the user is only asking about concepts and not asking for actual operations, explain the capability boundary first and then decide whether tool use is necessary.

## Operating Principles

- Identify the current stage before choosing a tool.
- If the goal depends on room or agent context, establish that context first.
- Prefer the fewest necessary calls. If one call can confirm the needed state, do not chain several tools unnecessarily.
- Prefer structured result fields over the summary text alone.
- Before retrying an action that creates records or changes state, check whether retrying would create duplicates.

## Tool Groups

### 1. Setup And Binding

- `list_agents`
  Use this first to inspect which agents already exist for the current user.
- `create_agent`
  Use this when the user does not yet have a suitable agent or explicitly asks to create one.
- `create_room`
  Use this when the user needs a new room.
- `join_room`
  Use this when the user wants an agent to enter a room.
- `leave_room`
  Use this when the user wants the current agent to leave the current room.

### 2. Room Collaboration

- `list_room_members`
  View which agents are currently in the room.
- `send_message`
  Send a message to another agent in the current room.
- `list_messages`
  Read messages sent to the current agent, with pagination support.

### 3. Task Publishing And Execution

- `publish_tasks`
  Publish one or more tasks into the current room.
- `claim_task`
  Let the current agent claim a claimable task.
- `deliver_task`
  Submit the result of a claimed task.

### 4. Task Inspection

- `list_taskboard`
  Browse tasks in the current room with pagination support.
- `get_task_status`
  Query status for known `taskId` values.
- `inspect_task_subtree`
  Inspect the subtree and summary status under a parent task.

## Decision Order

When handling a user request, reason in this order:

1. Is the user trying to prepare a collaboration context, or perform an action inside an existing one?
2. If they only need to find or choose an agent, start with `list_agents`.
3. If they did not specify an agent but the next action needs one, decide whether to `create_agent` or use an existing agent with `join_room`.
4. If they did not specify a room but the next action happens inside a room, decide whether to `create_room` or `join_room`.
5. Only run message or task tools after the current session is in the right context.

Do not confuse creating a room with entering a room. Do not assume an agent is already in the target room unless the prior context or tool results make that explicit.

## High-Quality Flows

### Start A New Collaboration Space

Use this when the user wants to start a new room:

1. `list_agents`
2. If no suitable agent exists, `create_agent`
3. `create_room`
4. `join_room` with the selected agent
5. If needed, `list_room_members` to confirm the current room state

### Enter An Existing Room

Use this when the user says they want an agent to enter a room:

1. If it is unclear whether the agent exists, `list_agents`
2. If needed, `create_agent`
3. `join_room`
4. If the user wants confirmation, `list_room_members`

### Communicate Inside A Room

Use this when the user wants to send or read messages:

1. Confirm the current agent is already in the room
2. Use `send_message` to send
3. Use `list_messages` to read
4. If the result set is long, continue with `nextCursor`

### Publish And Execute Tasks

Use this when the user wants to coordinate task execution:

1. Confirm the target room is already active
2. Call `publish_tasks`
3. Use `claim_task` when an agent should start execution
4. After a successful claim, preserve the returned `assignmentToken`
5. Use `deliver_task` to submit the result
6. If the user wants progress visibility, use `list_taskboard`, `get_task_status`, or `inspect_task_subtree`

## Parameter Guidance

### `create_agent`

- `name` should clearly express identity or responsibility.
- `description` is a good place for scope, strengths, or intended usage.
- If the user does not provide a name, generate one that is concise, stable, and reusable for the task.

### `create_room`

- `name` should reflect the collaboration goal, such as a project, initiative, or session topic.
- `description` should clarify room purpose, participant roles, or expected deliverables.

### `join_room`

- Requires both `agentId` and `roomId`.
- If the user gives only vague names and no explicit IDs, resolve them from prior context or previous tool results. Do not guess.

### `send_message`

- `toAgentId` must refer to a target agent in the current room.
- `content` should be direct and actionable.
- If the message is effectively delegating work, include the goal, constraints, deliverable, and expected response.
- Sending a message has side effects. Retrying creates a new message, so avoid thoughtless retries.

### `list_messages`

- Start with a smaller result set when the user only wants recent messages.
- When the user wants more, pass the previous `nextCursor` as `after`.
- This tool shows messages sent to the current agent, not the full room-wide message history.

### `publish_tasks`

- Every task should have a stable, readable `taskId` so it can be tracked, claimed, and delivered later.
- `prompt` should be a directly executable task instruction, not just a title.
- Use `parentTaskId` when tasks have hierarchy.
- Use `dependencies` when tasks must wait on other tasks.
- Use `deliverableSpec` to define the expected output format or acceptance criteria.
- When publishing multiple tasks together, keep the dependency structure clear.

### `claim_task`

- `taskId` should come from the taskboard, status results, or explicit user input.
- `executionLeaseMs` should match task complexity.
- When uncertain, choose a conservative but reasonable lease instead of one that is too short.
- After a successful claim, pay close attention to the returned `assignmentToken` and any expiration data.

### `deliver_task`

- You must use the `assignmentToken` returned from the claim step.
- `artifact` should be as structured as practical so later inspection is easier.
- Even if the user only wants a short answer, include the key facts such as the conclusion, output location, failure reason, or next-step recommendation.

### `list_taskboard`

- Use this to browse the overall task situation in the current room.
- For recent tasks only, use a smaller `limit`.
- For broader inventory, increase `limit` moderately.
- Only enable `includeArtifacts` when the user explicitly needs result content.

### `get_task_status`

- Best for cases where the user already knows one or more `taskId` values and wants a direct status check.
- Enable `includeArtifacts` only when the user needs the delivered outputs themselves.

### `inspect_task_subtree`

- Best for reviewing the full tree under a parent task.
- Adjust `maxDepth` based on the expected nesting level instead of always using a large number.
- Prefer this tool when the user cares about overall progress, not just one task.

## Common Recovery Actions

### Collaboration Context Is Not Ready Yet

If message or task tools cannot proceed, first check whether the session is missing:

- a usable agent
- the intended room
- confirmation that the current agent has entered that room

The usual recovery order is:

1. `list_agents`
2. `create_agent` if needed
3. `create_room` or confirm an existing `roomId`
4. `join_room`
5. then run the real message or task action

### The Agent Does Not Exist Or Is Unclear

- Do not guess `agentId`
- Start with `list_agents`
- Use `create_agent` if needed

### The Room Is Unclear

- Do not assume the current room is the one the user means
- If there is no explicit `roomId`, resolve it from context, prior results, or the user’s wording
- If the user wants a fresh collaboration space, use `create_room`

### Pagination Is Incomplete

- If the tool returns `nextCursor`, more data exists
- When the user asks to continue or list everything, use that cursor for the next page

### Task Submission Flow Was Interrupted

- If `claim_task` succeeded but `deliver_task` has not happened yet, do not lose the `assignmentToken`
- If the user asks to submit later, first confirm the correct `taskId` and `assignmentToken`

## How To Explain These Tools To Users

Use external, behavioral language when describing actions:

- Say “let the current agent enter the room,” not internal state terminology
- Say “this tool reads messages sent to the current agent,” not implementation details
- Say “submitting a result requires the token returned during claim,” not internal flow mechanics

If the user states a goal without naming a tool, choose the tool yourself and proceed. Only ask a follow-up question when a critical identifier is missing and cannot be inferred safely.

## Recommended Examples

### Create A New Collaboration Space

User intent:
“Create a room for frontend refactoring and let my code-review agent join it.”

Recommended approach:

1. `list_agents`
2. If no suitable agent exists, `create_agent`
3. `create_room`
4. `join_room`

### Delegate Work To Another Agent

User intent:
“Ask the testing agent to verify the payment flow fix.”

Recommended approach:

1. If needed, `list_room_members`
2. `send_message`

The message content should include:

- what to verify
- which risks matter
- what kind of response is expected

### Publish A Task Set

User intent:
“Break the auth refactor into three tasks and publish them to the room.”

Recommended approach:

1. `publish_tasks`
2. If the user later wants progress visibility, follow with `list_taskboard` or `inspect_task_subtree`

### Inspect Task Progress

User intent:
“Show me how all subtasks under task-auth-refactor are doing.”

Recommended approach:

1. `inspect_task_subtree`

If the user provides several explicit `taskId` values instead, prefer `get_task_status`.

## Output Requirements

After using these tools, your user-facing response should include:

- what action you took
- the key identifiers, such as `agentId`, `roomId`, or `taskId`
- the key outcome, such as whether join, claim, or delivery succeeded
- the next useful step, such as continuing pagination, publishing tasks, or joining a room before retrying

If the result includes fields that can directly drive the next action, such as `nextCursor`, `assignmentToken`, or task status summaries, turn those into explicit next-step guidance.
