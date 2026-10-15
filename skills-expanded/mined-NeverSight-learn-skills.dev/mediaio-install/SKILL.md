---
name: mediaio-install
metadata:
  version: "0.2.6"
description: |
  Install or update the shared Media.io CLI and plugin manifests for Codex or Claude Code. Use when the user asks to set up Media.io, refresh an existing installation, or align the installed plugin with the checked-out skills. Do not use for image or video generation tasks.
---

# Media.io Install

Install or update the Media.io stack for the current host.

## Scope

- Use this skill for first-time setup and refreshes.
- Do not use it for generation requests; `mediaio-generate` handles those.
- Keep the Codex and Claude plugin manifests aligned with the shared skills version.
- When a plugin or CLI update is available, the install skill should point the user at the matching upgrade path rather than treating the existing install as sufficient.

## Host paths

### Codex

- Install the shared skills package with `npx skills add <repository>/skills`.
- If you are doing local development from `media-plugin-main`, use the repo's own deployment scripts instead of inventing a parallel flow.

### Claude Code

- Ensure the shared `mediaio` CLI is installed and logged in before installing the plugin.
- Install this repository as a Claude Code plugin and point the plugin manifest at `.claude-plugin/`.
- Reuse the shared `skills/` directory rather than copying skills into a host-specific tree.

## Verification

- `mediaio version`
- Confirm the host can see the installed `mediaio` skill set
- Keep `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, and `skills/mediaio-install/SKILL.md` on the same release version
