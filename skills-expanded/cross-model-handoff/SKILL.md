---
name: cross-model-handoff
description: Create continuation notes that another model, provider, or agent can resume without relying on hidden context or exact tool names. Use when the user asks to hand off work between Claude, ChatGPT, Gemini, Codex, local agents, or another MCP-enabled assistant.
---

# Cross-Model Handoff

Use this skill when work may continue in a different model or client.

## Core Rule

Write the handoff so a different agent can continue without access to this conversation's hidden context.

## Workflow

1. Capture objective
   - State the user's goal.
   - Include current scope and non-goals.

2. Capture state
   - Files changed or inspected.
   - Decisions made.
   - Commands, tests, or checks run.
   - Tool capabilities used.

3. Separate facts from assumptions
   - Verified facts
   - Assumptions
   - Unknowns
   - Blockers

4. Translate tools
   - Say capabilities, not only exact tool names.
   - Example: "Used file search and read tools" instead of only "called search_in_files".
   - Include exact local names only as optional implementation detail.

5. Give next actions
   - First next step
   - Validation step
   - Risk to watch

## Output Format

```markdown
# Cross-Model Handoff

## Objective

## Current State

## Decisions

## Files And Artifacts

## Tool Capabilities Used

## Verification

## Assumptions

## Next Steps

## Risks
```

## Rules

- Do not reference hidden conversation context as required knowledge.
- Do not assume the next agent has the same tools.
- Do not imply tests passed unless they actually ran.
- Include exact paths, URLs, commands, or artifacts when they matter.
