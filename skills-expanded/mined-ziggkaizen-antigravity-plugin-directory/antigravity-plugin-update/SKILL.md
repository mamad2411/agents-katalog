---
name: antigravity-plugin-update
description: Updates and changes existing Antigravity plugins while preserving scope, compatibility, safety, README accuracy, index accuracy, and minimal context. Use when modifying plugin files, adding capabilities, changing versions, or applying review findings.
license: MIT
compatibility: "Antigravity plugin authoring; intended for safe incremental plugin maintenance."
---

# Antigravity Plugin Update

This skill changes existing plugins without turning them into sprawling, incompatible packages.

## Use this skill when

- A user asks to update, change, extend, or refactor a plugin.
- A review found issues that need fixes.
- A technology version changes and the plugin must be upgraded.
- A skill, workflow, rule, hook, or MCP server should be added or removed.

## Update principles

- Preserve the plugin’s stated scope unless the user explicitly changes it.
- Prefer adding a separate plugin over expanding beyond the 95% rule.
- Update README and `_INDEX.md` whenever plugin contents change.
- Keep optional integrations disabled unless they are safe and require no setup.
- Do not remove existing safety constraints unless the user explicitly asks and the risk is acceptable.

## Workflows

- Use [plugin-update-workflow.md](workflows/plugin-update-workflow.md) for ordinary changes.
- Use [version-upgrade-plugin-workflow.md](workflows/version-upgrade-plugin-workflow.md) for target-version upgrades.

## Resources

- [change-request-template.md](resources/change-request-template.md)
- [migration-notes-template.md](resources/migration-notes-template.md)

## Patch checklist

Before finalizing changes:

- Changed files are listed.
- JSON remains valid.
- README matches generated files.
- `_INDEX.md` matches plugin inventory.
- New workflows are referenced from parent skills.
- Scripts and hooks remain safe.
- Version claims are current and documented.
