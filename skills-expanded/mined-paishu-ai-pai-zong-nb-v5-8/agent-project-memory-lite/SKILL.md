---
name: agent-project-memory-lite
description: "Use when repository work changes durable project knowledge and agent runtime should update the smallest relevant project files such as `.ai_project.md`, `AGENTS.md`, or `docs/` without importing a separate global memory system."
---

# agent-project-memory-lite

## Purpose

Use when repository work changes durable project knowledge and agent runtime should update the smallest relevant project files such as `.ai_project.md`, `AGENTS.md`, or `docs/` without importing a separate global memory system.

## Use When

- The user request matches `agent-project-memory-lite`, `agent project memory lite`, `software-development` or the skill description.
- Use when repository work changes durable project knowledge and agent runtime should update the smallest relevant project files such as `.ai_project.md`, `AGENTS.md`, or `docs/` without importing a separate global memory system.
- The task benefits from domain-specific workflow, checks, output structure, or safe fallback behavior.

## Workflow

1. Inspect the relevant project files, docs, scripts, and existing patterns before changes.
2. Keep source-runtime naming as historical source only; translate workflow to Codex-compatible practice.
3. Prefer small, verifiable changes with tests or concrete checks.
4. Update project docs or memory when durable project behavior changes.

## Codex Runtime Rules

- Use only tools, plugins, MCP servers, files, commands, and credentials that are actually available in the current Codex session.
- If an external write, install, publish, deploy, paid action, credential use, account operation, physical-device action, or production action is needed, ask for explicit confirmation first.
- If the required tool is unavailable, return a portable fallback such as Markdown, CSV, prompt pack, implementation plan, config sketch, or verification checklist.
- Do not claim files, media, issues, API calls, payments, deployments, transactions, messages, or integrations were created unless there is concrete local or tool evidence.
- Treat source repository runtime details as historical source context, not active Codex capabilities.

## Avoid

- Do not assume source-runtime CLIs, paths, or tools exist in Codex.
- Do not claim tests/builds passed unless run.

## Output

Return the useful artifact first, then evidence and verification status.

For non-trivial work, include:

```markdown
Result: ...
Evidence: ...
Verification: PASS/FAIL/NOT RUN
Risks / Next Steps: ...
```
