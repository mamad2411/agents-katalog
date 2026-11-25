---
name: commercial-control-center-ui
description: "Design polished desktop, admin, runtime, and operations control centers for complex local or API-heavy systems."
---

# commercial-control-center-ui

## Purpose

Design polished desktop, admin, runtime, and operations control centers for complex local or API-heavy systems.

## Use When

- The user wants a commercial dashboard, desktop control center, runtime manager, admin UI, or API-heavy settings console.
- The UI must feel operational, stable, and scalable rather than decorative.

## Workflow

1. Separate daily home, settings center, diagnostics, automation/workflows, API reference, and logs.
2. Design homepage around status, risks, primary actions, and recent work.
3. Use dense but readable layouts, stable navigation, compact tables, clear filters, and restrained visual style.
4. Classify actions by risk and require confirmation/diff/backup for high-risk operations.
5. Verify implemented UI with browser/screenshot checks when code is changed.

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

Information architecture, screen specs, risk guardrails, verification plan.

For non-trivial work, include:

```markdown
Result: ...
Evidence: ...
Verification: PASS/FAIL/NOT RUN
Risks / Next Steps: ...
```
