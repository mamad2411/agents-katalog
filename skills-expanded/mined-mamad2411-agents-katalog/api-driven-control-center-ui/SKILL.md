---
name: api-driven-control-center-ui
description: "Design API-driven management-console UIs where each backend endpoint or capability maps to a visible feature, risk level, and adapter boundary."
---

# api-driven-control-center-ui

## Purpose

Design API-driven management-console UIs where each backend endpoint or capability maps to a visible feature, risk level, and adapter boundary.

## Use When

- The user needs a UI over an existing API surface, admin console, runtime API, settings dashboard, or endpoint coverage map.
- The task requires translating routes/OpenAPI/source handlers into product screens.

## Workflow

1. Inventory endpoints, methods, data objects, write operations, auth, and risk levels.
2. Group endpoints into product modules instead of exposing a raw endpoint list as the main UX.
3. Define adapter boundaries so the frontend calls stable product APIs.
4. Create API reference/coverage screens for completeness without overwhelming daily workflows.
5. Specify filters, search, risk badges, confirmations, audit logs, and rollback hints for high-risk actions.

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

API-to-feature map, screen architecture, risk model, adapter plan.

For non-trivial work, include:

```markdown
Result: ...
Evidence: ...
Verification: PASS/FAIL/NOT RUN
Risks / Next Steps: ...
```
