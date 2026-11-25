---
description: Complete and save your current thinking to Bindly
---

Help the user finish their current thought and save it to Bindly.

## Philosophy

Bindly is not auto-memory. Saving is an intentional act.

> "Bindly doesn't try to remember everything for you.
> It helps you finish your thoughts and make them reusable."

## Workflow

When the user wants to save knowledge:

1. **Search First**: Check Bindly for similar existing content
   - Use `mcp_search` to find related bindings
   - Present any similar results to the user

2. **Compare and Decide**: If similar content exists, ask the user:
   - "Update existing binding (create new version)?" — for evolving the same idea
   - "Create new binding (different context)?" — for distinct but related knowledge

3. **Formulate**: Help the user create:
   - A clear, descriptive title
   - Key points extracted from the content
   - Relevant entities (people, tools, concepts)
   - A summary that captures the essence

4. **Confirm Storage Location**: Remind the user:
   > "This will be saved to your Bindly account at bindly.app,
   > accessible from Claude Code and other connected agents."

5. **Save**: Use `request_create_binding` or `request_update_binding`

## Example Prompts

- "Save this research about React hooks"
- "Remember this debugging approach for later"
- "Store my notes from this code review"

## Key Points

- Always search before creating to avoid duplicates
- Knowledge is stored at bindly.app, not locally
- Same knowledge accessible from ChatGPT, Claude Web, and other MCP clients
- Saving creates understanding, not just records
