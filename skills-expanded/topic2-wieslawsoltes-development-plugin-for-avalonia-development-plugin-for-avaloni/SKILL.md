---
name: development-plugin-for-avalonia
description: Repo-local umbrella skill for building, reviewing, designing, porting, and migrating Avalonia applications with modern XAML/C# patterns on Avalonia 11.3.12. Use when working inside this repository and the request is broad Avalonia work; route quickly to the focused plugin skills for startup, bindings, styling, controls, layout, rendering, testing, design systems, or HTML/WinForms/WPF/WinUI/Avalonia 12 migration work.
---

# Development Plugin for Avalonia

Use this as the repo-local entrypoint when Codex is operating inside this repository.

This wrapper keeps repo-local skill discovery separate from plugin skill discovery:

- repo-local discovery entrypoint: `.agents/skills/development-plugin-for-avalonia/SKILL.md`
- plugin manifest: `../../../.codex-plugin/plugin.json`
- plugin skills: `../../../skills/`
- shared references: `../../../references/`

Load the canonical umbrella workflow from:

- `../../../SKILL.md`

Then follow the routing rules from `../../../SKILL.md` instead of copying the full routing table here. The focused plugin skills under `../../../skills/` and the shared references under `../../../references/` remain the actual implementation surface.

Keep default guidance pinned to Avalonia `11.3.12` and treat Avalonia 12 work as an explicit migration lane.
