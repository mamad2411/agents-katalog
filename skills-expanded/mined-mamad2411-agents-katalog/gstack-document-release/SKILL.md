---
name: gstack-document-release
description: Update or audit OPC documentation after code changes. Use when behavior, setup, CLI flags, desktop workflow, provider support, or plugin surfaces changed.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Edit
  - Write
---

# gstack-document-release

Use this skill to keep docs aligned with shipped behavior.

## Workflow

1. Inspect the current diff and identify user-visible changes.
2. Map affected docs: README files, plugin READMEs, desktop docs, examples, settings, and scripts.
3. Check for stale commands, paths, model/provider names, environment variables, screenshots, and troubleshooting text.
4. Update only the docs that are directly affected.
5. Verify links, commands, and JSON snippets where practical.

## Documentation Standard

Prefer Diataxis-style clarity:

- Tutorial: first successful path
- How-to: task-specific steps
- Reference: exact flags, settings, APIs, schemas
- Explanation: architecture and tradeoffs

## Output

Report:

- Docs changed
- Behavior now documented
- Commands or snippets verified
- Known documentation gaps left for later
