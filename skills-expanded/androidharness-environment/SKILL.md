---
name: androidharness-environment
description: AndroidHarness workspaces, execution tiers, runtime paths and tool workflows.
category: environment
---

# Working inside AndroidHarness

You run inside an Android app. The live environment section and the tool schemas attached to the current request describe this run. A reference explains how a capability works; it does not make that capability available or authorize its use.

## Read the environment before choosing tools

- Identify the selected workspace and its access. Local folders, Android document trees and SSH hosts have different execution capabilities. Use `workspace_id` for a selected project; never borrow another chat's project or the globally selected folder.
- Separate connection readiness, verified UID, root allowance and the default route. A connected Shizuku service is independent of a direct-root grant. Ordinary app-owned workspace work normally stays on the app UID even when privileged connections exist.
- Prefer tools that directly perform the task. Their schemas are the parameter reference. Installed package records do not prove executable health, and Linux readiness does not imply an Android SDK exists.
- The harness supplies `PATH`, `PREFIX`, library paths and `HARNESS_SCRATCH`. Call commands by plain name. Do not improvise linker commands, replace the harness environment, invoke `su`/`sudo`, or use the separate Termux app's paths.
- After a connection failure or changed environment, inspect `env_status` once when available and act on its specific result. Do not repeat unchanged failing commands or silently replay a possibly dispatched mutation.
- Preserve the user's scope. Plan mode is read only; Full access does not override selected-workspace grants or create root privileges. A skill never grants approval for an external action.

## Load only the relevant details

Use `skill_view(name="androidharness-environment", file_path="…")`:

- Files, project selection, storage or skills: `references/workspaces-and-paths.md`.
- Shizuku, root, normal access, verified identity or system commands: `references/device-access.md`.
- Packages, Java, DEX, APK builds, native binaries or shared-storage errors: `references/packages-and-builds.md`.
- Choosing file, search, browser, Git, rich-response or artifact tools: `references/tools-and-workflows.md`.
- Lost files, undo, interrupted jobs, large output or diagnostics: `references/recovery-and-diagnostics.md`.
- MCP, credentials, background servers, subagents, memory or Chat/Code handoff: `references/integrations-and-sessions.md`.
- A concise environment report after a relevant failure: `templates/environment-check.txt`.

The essential guide is supplied automatically in Code when this skill is enabled. Supporting files stay on demand. Do not run a diagnostic checklist for an ordinary task whose required capability is already clear.
