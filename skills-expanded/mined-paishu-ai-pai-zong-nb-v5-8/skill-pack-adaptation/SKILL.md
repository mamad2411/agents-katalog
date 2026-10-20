---
name: skill-pack-adaptation
description: "Evaluate and adapt external AI-agent skill packs, prompt systems, memory layers, and workflow repos for Codex without importing incompatible runtime assumptions."
---

# skill-pack-adaptation

## Purpose

Evaluate and adapt external AI-agent skill packs, prompt systems, memory layers, and workflow repos for Codex without importing incompatible runtime assumptions.

## Use When

- The user asks whether an external skill/prompt/agent repo should be merged, installed, or rewritten for Codex.
- A source package mixes portable workflows with runtime-specific commands, memory, paths, or tools.

## Workflow

1. Identify package type: skills library, runtime prompt, memory system, installer, plugin, or mixed bundle.
2. Classify contents: portable as-is, portable after rewrite, do not import, or verification tooling reference.
3. Check for runtime coupling: paths, tool names, reload semantics, memory roots, mandatory file reads, and unsafe writes.
4. Map portable knowledge to Codex layers: professional skills, user-skills, project docs, or optional references.
5. Recommend batch order, validation gates, and rollback/backup needs.

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

Use as-is/adapt/skip table, risks, batch plan, validation gates.

For non-trivial work, include:

```markdown
Result: ...
Evidence: ...
Verification: PASS/FAIL/NOT RUN
Risks / Next Steps: ...
```
