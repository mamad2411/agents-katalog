---
name: tauri-plugins
description: Select, install, configure, and author Tauri 2 plugins without widening application authority unnecessarily. Use when integrating a Tauri plugin or designing reusable native functionality.
---

# Tauri plugins

This skill is scoped to Tauri 2. Verify plugin APIs, permissions, and platform support against the installed crate/npm versions and [official plugin documentation](https://v2.tauri.app/develop/plugins/).

## Workflow

1. Identify the official or maintained plugin and check Tauri 2 compatibility, supported platforms, crate/npm versions, permissions, scopes, and security notes.
2. Install Rust and JavaScript sides using the plugin's official instructions; preserve the project's package manager and lockfiles.
3. Register and initialize the plugin in the application builder as documented. Do not infer registration names from package names.
4. Add the smallest capability permissions and resource scopes needed. Inspect generated schemas and plugin source when permission behavior is unclear; permissions are part of the app's runtime authority.
5. Confirm platform-specific support and behavior. A plugin may support desktop but not Android/iOS, or implement each platform differently; handle unavailable APIs and platform permissions explicitly.
6. Exercise the plugin on every claimed target platform, including denied permission, missing capability, unsupported platform, lifecycle interruption, and malformed input behavior.

For custom plugins, follow [plugin development](https://v2.tauri.app/develop/plugins/) and keep public APIs, commands, permissions, scopes, and platform implementations explicit.

## Safe defaults

- Prefer official plugins or well-maintained sources with auditable code.
- Pin compatible versions and review changelogs before upgrades; plugin APIs are independently versioned.
- Never grant a plugin more authority than its feature needs.
- Do not copy a Tauri 1 plugin recipe into Tauri 2 without verifying current documentation.
