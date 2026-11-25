---
name: antigravity-plugin-review
description: Reviews Antigravity plugins for structure, version compatibility, safety, context bloat, README completeness, skill frontmatter, workflow placement, hook behavior, MCP configuration, and index accuracy. Use when auditing existing plugin packages or generated plugin output.
license: MIT
compatibility: "Antigravity plugin authoring; safe for repository-local plugin reviews."
---

# Antigravity Plugin Review

This skill audits plugin packages and returns prioritized, actionable findings.

## Use this skill when

- A user asks to review an Antigravity plugin.
- A generated plugin needs quality gates before use.
- A plugin was edited and may have regressions.
- A user asks whether a plugin is bloated, unsafe, incomplete, or version-incompatible.

## Review approach

1. Inspect the file tree first.
2. Check required files.
3. Validate plugin scope and naming.
4. Validate rules, skills, workflows, resources, scripts, hooks, and MCP config.
5. Check README and `_INDEX.md` consistency.
6. Check version and documentation-source claims.
7. Report findings by severity.

## Workflows

- Use [plugin-review-workflow.md](workflows/plugin-review-workflow.md) for a normal audit.
- Use [plugin-regression-review-workflow.md](workflows/plugin-regression-review-workflow.md) after plugin edits or upgrades.

## Resources

- [review-rubric.md](resources/review-rubric.md)
- [compatibility-audit.md](resources/compatibility-audit.md)

## Finding format

Use this format for issues:

```text
Severity: critical | high | medium | low
File: <path>
Issue: <specific problem>
Why it matters: <impact>
Fix: <concrete change>
```

Do not bury critical safety or compatibility issues in general prose.
