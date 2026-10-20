---
name: control-center-ui-design
description: "Design commercial control centers, runtime managers, admin consoles, and API-driven operations UIs with many settings or backend capabilities."
---

# control-center-ui-design

## Purpose

Design commercial control centers, runtime managers, admin consoles, and API-driven operations UIs with many settings or backend capabilities.

## Use When

- The user mentions control center, admin console, runtime manager, API dashboard, settings-heavy app, or operations UI.
- A product has many backend capabilities that need a calm, navigable interface.

## Workflow

1. Identify daily users, critical workflows, backend capability groups, high-risk actions, and operational status needs.
2. Keep the home screen focused on status, common actions, risks, and navigation into deeper modules.
3. Move raw endpoints, advanced settings, logs, and diagnostics into dedicated areas.
4. Use consistent risk labels, confirmations, audit trails, and rollback cues for writes or destructive operations.
5. Pair with frontend/design skills for implementation and visual QA when code is involved.

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

Control-center IA, module map, screen requirements, risk gates.

For non-trivial work, include:

```markdown
Result: ...
Evidence: ...
Verification: PASS/FAIL/NOT RUN
Risks / Next Steps: ...
```
