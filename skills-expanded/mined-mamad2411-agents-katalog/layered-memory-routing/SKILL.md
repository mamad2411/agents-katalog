---
name: layered-memory-routing
description: "Route memory requests between compact built-in memory, project memory, and explicit external brain or knowledge-base systems."
---

# layered-memory-routing

## Purpose

Route memory requests between compact built-in memory, project memory, and explicit external brain or knowledge-base systems.

## Use When

- The user says remember, save memory, project memory, external brain, GBrain, or knowledge base.
- A fact could be stored in more than one memory layer.
- The task needs read/write destination decisions for durable context.

## Workflow

1. Classify the item as user preference, project fact, evidence, long-form reference, or one-off context.
2. Use built-in/global memory only for compact cross-project behavioral preferences.
3. Use project docs and project memory for project facts, plans, decisions, commands, and evidence.
4. Use external brain only when the user explicitly asks for that system or configured trigger phrase.
5. Report the chosen destination and why; skip writes for sensitive, uncertain, or one-off data.

## Codex Runtime Rules

- Use only tools, plugins, MCP servers, files, and credentials that are actually available in the current Codex session.
- If an external write, install, publish, deploy, paid action, credential use, or account operation is needed, ask for explicit confirmation first.
- If the required tool is unavailable, return a portable fallback such as Markdown, CSV, prompt pack, implementation plan, or verification checklist.
- Do not claim files, videos, images, issues, API calls, or integrations were created unless there is concrete local or tool evidence.
- Keep long vendor recipes and examples out of the prompt path; load only task-relevant references when they exist.

## Avoid

- Do not import source-runtime commands, reload semantics, home-directory paths, or tool names as if they are Codex capabilities.
- Do not fabricate external state, API results, generated media, issue updates, or test outcomes.
- Do not broaden the task into unrelated setup or account configuration.

## Output

Read layer, write destination, skip/update reason, retrieval pointer.

For non-trivial work, include:

```markdown
Result: ...
Evidence: ...
Verification: PASS/FAIL/NOT RUN
Risks / Next Steps: ...
```
