---
name: agent-memory-system-evaluation
description: "Evaluate external agent memory, brain, or knowledge systems and decide whether they belong as core memory, project docs, plugin, MCP service, or optional integration."
---

# agent-memory-system-evaluation

## Purpose

Evaluate external agent memory, brain, or knowledge systems and decide whether they belong as core memory, project docs, plugin, MCP service, or optional integration.

## Use When

- The user asks whether a memory or knowledge system should be integrated.
- A project needs memory boundaries, persistence rules, retrieval strategy, or storage ownership decisions.
- A memory feature could overlap with existing Codex global memory, project docs, or external knowledge bases.

## Workflow

1. Identify the memory layer: user preference, project fact, long-form knowledge, runtime cache, or external brain.
2. Map read/write triggers, retention, privacy, portability, and failure behavior.
3. Compare integration options: no integration, docs-only, built-in memory, plugin/tool, MCP service, or separate app.
4. List risks: stale retrieval, prompt bloat, sensitive storage, duplicated truth, vendor lock-in, and unclear deletion.
5. Recommend the smallest integration that preserves boundaries and can be verified.

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

Decision, boundary map, integration option, risks, verification plan.

For non-trivial work, include:

```markdown
Result: ...
Evidence: ...
Verification: PASS/FAIL/NOT RUN
Risks / Next Steps: ...
```
