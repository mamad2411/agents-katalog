```---
applyTo:
  - "**"
description: "CRITICAL POLICY: Rules regarding file creation restrictions, output formatting, minimal coding standards, and MCP memory protocols."
tags:
  - policy
  - memory
  - mcp
  - formatting
  - file-restrictions
version: "1.0"
---```

# AI Agent Output & Memory Policy

## 🚨 Critical File Creation Restrictions

**You MUST NOT automatically create markdown files** in the following directories without explicit user approval:

- root directory
- `.agents/`
- `.github/`
- `.kiro/`
- `.amazonq/`
- `.cursor/`
- `.gemini/`
- `.junie/`
- `.opencode/`

**Prohibited File Types**:
Do not create the following files to summarize your work. Provide this information inline in the chat instead:

- Reports (`*-report.md`)
- Summaries (`*-summary.md`)
- Checklists (`checklist-*.md`)
- Implementation logs
- Task status files

**Exception**: You may create these files only if the user explicitly prompts with "create a file", "save to file", or specifies a filename.

## ✅ Default Response Mode

1. **Inline Chat First**: Your primary output must be the chat interface.
2. **Structure**: Use Markdown headers, lists, and tables within the chat to organize information.
3. **Summary**: Always summarize findings and recommendations in the chat, not in a new file.

## 💻 Minimal Code Policy

When generating code:

1. **Write ONLY necessary code**.
2. Avoid verbose boilerplate if it does not contribute to the immediate solution.
3. Prioritize clarity and simplicity.
4. Do not include code that doesn't directly solve the stated problem.

## 🧠 Memory & Context Protocol (MCP)

You are integrated with an **MCP Memory Server**. You must prioritize this over file-based memory.

### 1. Initialization (Start of Task)
Before generating code or answers, you must query the memory server to understand the context:

- Use `search_nodes` to find relevant entities (e.g., features, patterns, bugs).
- Use `open_nodes` to retrieve detailed context.

### 2. Implementation (During Task)

- Do not create temporary tracking files.
- If you discover a new pattern or fix a bug, use `create_entities` or `add_observations` to store this knowledge in the Memory Server.

### 3. Completion (End of Task)

- **Update Memory**: Record the status of the feature or fix using `add_observations` on the relevant entity.
- **Traceability**: Ensure `technical_implementation` entities are linked to their requirements via `create_relations`.

### Fallback
If the MCP Memory Server is unavailable, fallback to reading/updating `.agents/memory.instructions.md`, but strictly adhere to the "No new markdown files" rule for general reporting.
