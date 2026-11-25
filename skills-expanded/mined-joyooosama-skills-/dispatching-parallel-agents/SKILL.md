---
name: dispatching-parallel-agents
description: Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies
---

# dispatching parallel agents

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No shared state between investigations
- Failures are related (fix one might fix others)
- Need to understand full system state
- Agents would interfere with each other
- File A tests: Tool approval flow

## Available sections

- Dispatching Parallel Agents
- Overview
- When to Use
- The Pattern
- 1. Identify Independent Domains
- 2. Create Focused Agent Tasks
- 3. Dispatch in Parallel
- 4. Review and Integrate
- Agent Prompt Structure
- Common Mistakes
- When NOT to Use
- Real Example from Session

