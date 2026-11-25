---
name: antigravity-plugin-optimize
description: Optimizes Antigravity plugins for minimal context bloat, progressive disclosure, structural correctness, safe hooks, reusable resources, and maintainability. Use when a plugin feels too large, repetitive, slow to load, or hard for agents to navigate.
license: MIT
compatibility: "Requires bash for scan-plugin.sh. Python 3 is required for hook helper scripts."
---

# Antigravity Plugin Optimize

This skill improves plugin quality without changing the user-visible scope unless requested.

## Use this skill when

- A plugin is too large or repetitive.
- A skill contains long reference material.
- README and index content are duplicated.
- Workflows are embedded directly in `SKILL.md`.
- Hooks, MCP config, or scripts need safety review.
- A user asks to optimize an Antigravity plugin.

## Optimization strategy

1. Preserve behavior first.
2. Move detail to resources.
3. Split broad skills.
4. Shorten rules to durable constraints.
5. Keep `_INDEX.md` minimal.
6. Keep README as the plugin’s detailed entry point.
7. Add scripts only when they reduce repeated manual work.
8. Remove examples that do not teach a useful pattern.

## Workflows

- Use [plugin-optimization-workflow.md](workflows/plugin-optimization-workflow.md) for structured optimization.

## Resources

- [context-bloat-reduction-guide.md](resources/context-bloat-reduction-guide.md)
- [progressive-disclosure-patterns.md](resources/progressive-disclosure-patterns.md)

## Scripts

- Run `scripts/scan-plugin.sh --help` before using the scanner.
- Prefer running `scripts/scan-plugin.sh .agents/plugins/<plugin-name>` before and after optimization.

## Optimization checklist

- No repeated long checklists across files.
- No giant “do everything” skill unless the plugin’s scope truly requires it.
- Skill descriptions are activation-friendly.
- Resources are one level deep from `SKILL.md`.
- Scripts are safe by default.
- Hooks are conservative.
