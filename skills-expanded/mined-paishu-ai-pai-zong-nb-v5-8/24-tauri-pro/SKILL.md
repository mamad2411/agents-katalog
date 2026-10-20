---
name: tauri-pro
description: Professional Tauri desktop application development with Rust commands, webview frontend, permissions, IPC, filesystem access, secure storage, sidecars, updater, packaging, and cross-platform desktop behavior. Use for Tauri apps, Tauri + React/Vue/Svelte, Rust backend commands, desktop APIs, tauri.conf, capabilities, and build/release issues.
---

# Tauri Pro

## Workflow

1. Identify Tauri version, frontend framework, Rust command layout, plugins, and `tauri.conf`.
2. Keep frontend, command API, plugin permissions, and OS capabilities separate.
3. Validate IPC command inputs and return typed errors to the frontend.
4. Review filesystem, shell, dialog, updater, deep link, notification, and sidecar permissions.
5. Test both dev mode and production build behavior when possible.

## Rust Command Rules

- Keep commands small and delegate business logic to Rust modules.
- Use typed request/response structs.
- Avoid `unwrap()` / `expect()` in command paths that can fail due to user input or environment.
- Map errors into stable frontend-facing error codes/messages.
- Do not pass raw user input into shell commands or filesystem paths without validation.

## Frontend Bridge Rules

- Centralize `invoke` calls in an API layer.
- Normalize loading, cancellation, and error states.
- Treat IPC like an API boundary, not a direct function call.
- Do not expose privileged functionality through broad generic commands.

## Security Checklist

- Minimize capabilities and plugin permissions.
- Validate paths and prevent traversal.
- Keep secrets out of frontend bundles.
- Use OS credential storage or vetted secure storage for tokens.
- Audit shell, opener, filesystem, and sidecar usage.

## Packaging Checklist

- Verify `npm run tauri dev` and production build command.
- Check icons, bundle identifier, app name, updater config, signing/notarization needs.
- Document platform-specific differences for Windows/macOS/Linux.

## Output

State Tauri stack, native boundary touched, capability/security impact, build command, and verification result.

## Bundled Resources

- `references/tauri-production-patterns.md`: layer boundaries, command rules, IPC security, release checks.
- `assets/command-error-pattern.rs`: typed Rust command error pattern to adapt when implementing Tauri commands.
