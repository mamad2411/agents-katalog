---
name: gbrain-integration
description: "Plan or troubleshoot GBrain-style external memory integration for Codex-compatible workflows without assuming the external service or credentials are available."
---

# gbrain-integration

## Purpose

Plan or troubleshoot GBrain-style external memory integration for Codex-compatible workflows without assuming the external service or credentials are available.

## Use When

- The user mentions GBrain, external brain, external memory provider, embedding provider, or memory MCP.
- A memory issue involves provider config, embedding compatibility, retrieval failures, or tool exposure.

## Workflow

1. Separate built-in Codex memory, project docs, and the external brain before changing anything.
2. Check which tools, configs, files, and credentials are actually available in the current environment.
3. For configuration work, inspect persisted config first, then apply only requested changes.
4. For debugging, capture the failing path: write, embed, search, retrieve, summarize, or inject.
5. If tools are unavailable, produce a config checklist and test plan rather than claiming integration.

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

Current boundary, available capabilities, change plan or diagnosis, test command/checklist.

For non-trivial work, include:

```markdown
Result: ...
Evidence: ...
Verification: PASS/FAIL/NOT RUN
Risks / Next Steps: ...
```
