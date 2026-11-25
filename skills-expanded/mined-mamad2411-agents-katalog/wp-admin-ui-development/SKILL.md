---
name: wp-admin-ui-development
description: WordPress admin UI review for Codex. Use when reviewing settings pages, admin menus, notices, screen targeting, admin form flows, and capability-aware plugin interfaces.
---

# Codex WordPress Admin UI Review

## Purpose

Use this skill when Codex should review WordPress admin interfaces for capability safety, maintainability, screen structure, settings flows, and admin UX quality.

## Focus Areas

- Menu and screen registration
- Settings pages and forms
- Nonces and capabilities in admin actions
- Screen-specific asset loading
- Notices, tabs, and admin interaction patterns

## Workflow

1. Detect the admin screen type.
2. Review capability checks and save flow first.
3. Check Settings API usage, notices, and screen-specific assets.
4. Load only the needed shared references from `../../claude-skills/wp-admin-ui-development/references/`.
5. Report findings with severity, file references, admin impact, and fixes.

## References

- `../../claude-skills/wp-admin-ui-development/references/settings-and-screens.md`
- `../../claude-skills/wp-admin-ui-development/references/admin-ux-patterns.md`

