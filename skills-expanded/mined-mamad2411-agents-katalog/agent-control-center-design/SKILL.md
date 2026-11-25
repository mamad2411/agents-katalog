---
name: agent-control-center-design
description: "Design commercial control-center UIs for AI agent platforms covering settings, prompts, tools, skills, memory, sessions, automation, gateways, APIs, and diagnostics."
---

# agent-control-center-design

## Purpose

Design commercial control-center UIs for AI agent platforms covering settings, prompts, tools, skills, memory, sessions, automation, gateways, APIs, and diagnostics.

## Use When

- The user is building an agent runtime UI, assistant control center, runtime manager, or settings-heavy console.
- The UI must represent many backend capabilities without making the homepage a raw endpoint dump.

## Workflow

1. Inventory runtime capabilities: prompts, tools, skills, memory, sessions, automations, MCP/plugins, logs, and diagnostics.
2. Group capabilities into product modules and keep high-risk actions behind guardrails.
3. Design daily-use homepage around health, recent activity, risks, and key actions.
4. Move complexity into settings, API reference, diagnostics, and specialized workspaces.
5. Coordinate with frontend/UI implementation skills when code changes are required.

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

Module map, screen plan, risk model, implementation handoff.

For non-trivial work, include:

```markdown
Result: ...
Evidence: ...
Verification: PASS/FAIL/NOT RUN
Risks / Next Steps: ...
```
