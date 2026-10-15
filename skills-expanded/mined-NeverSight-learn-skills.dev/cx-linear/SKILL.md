---
name: cx-linear
description: Integrate with Linear for issue tracking. Activate when the developer wants to create or reference Linear issues, or synchronize task tracking.
---

# Skill: cx-linear

## Description
Integrate with Linear for issue tracking. Creates, updates, and links Linear issues to CX changes and tasks.

## Triggers
- Developer wants to create a Linear issue
- Developer references a Linear issue ID
- Task tracking needs to be synchronized

## Steps
1. Ensure Linear MCP server is configured
2. Create or link issues as needed
3. Update issue status as work progresses
4. Link issues to change documents in tasks.md

## Rules
- Requires Linear MCP server to be configured
- Issue references use the format TEAM-123
- Keep Linear status in sync with change status
