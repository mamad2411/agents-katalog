---
name: copilot-linux-diagnostics
description: Diagnose Copilot CLI, desktop-app and editor problems on Linux with scoped version, runtime, network and tool evidence.
---

# Copilot diagnostics

First identify the failing surface: CLI, desktop app, editor extension, or
one MCP/plugin. Check its actual version and installation method.

Public HTTPS reachability is not authenticated API access. Keep tokens and
browser credentials private; let the user complete sign-in and permissions.
Summarize only relevant error categories from logs, not private prompts or history.

Check the exact native-library error before changing dependencies. When a
runtime cannot load its expected OpenSSL ABI, use an available distribution
compatibility package—not an ABI-mismatched symlink or disabled TLS validation.

Use current CLI documentation for configuration paths and commands. Settings
belong in the user settings file; authentication/application state is not a
template to export or copy into a repository.

After a change, reproduce the original action. Installed packages, a listening
port and a healthy model catalog prove different things. Report unresolved
permission, runtime and server-side errors explicitly.
