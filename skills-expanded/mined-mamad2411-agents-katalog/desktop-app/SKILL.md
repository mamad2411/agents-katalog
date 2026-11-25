---
name: desktop-app
description: Build and modify API-driven desktop applications using Electron, Tauri, Qt, .NET, native shells, or similar stacks. Use for desktop UI, native capabilities, local storage, auto-update, packaging, permissions, IPC, filesystem access, and desktop-specific UX.
---

# Desktop App

## Workflow

1. Identify shell stack: Electron, Tauri, Qt, .NET, native, or hybrid.
2. Separate renderer/UI logic from privileged native or main-process logic.
3. Keep API access, local persistence, filesystem, and OS permissions explicit.
4. Design offline, slow network, auth expiry, and update states.
5. Verify packaging, startup, window sizing, and platform differences when relevant.

## Required Checks

- Do not expose privileged APIs directly to untrusted renderer code.
- Validate IPC messages and file paths.
- Keep secrets out of frontend bundles and local plaintext storage when possible.
- Handle proxy, certificate, network loss, and API timeout cases for API-driven apps.
- Respect OS conventions for menus, shortcuts, dialogs, tray, and notifications.

## Output

State desktop stack assumptions, native boundary changes, security implications, and verification steps.
