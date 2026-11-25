---
name: 1password-developer
description: "Guidelines for utilizing developer-focused features in the 1Password Chrome Extension, including Passkey support and SSH Agent integration."
---

# 1Password Developer Features

The 1Password Chrome Extension offers robust support for modern web development workflows and passwordless authentication.

## Core Features

### 1. Passkey Management
1Password acts as a universal passkey provider, intercepting the Web Authentication API (`navigator.credentials.create` and `navigator.credentials.get`).
*   **Cross-Device Sync:** Passkeys generated in Chrome are synced to the 1Password vault, allowing seamless login across Safari, iOS, and other devices without relying on ecosystem-locked providers like iCloud Keychain.
*   **Testing Passkeys:** When building WebAuthn flows on a site, 1Password is an excellent tool for testing passkey registration and assertion flows locally.

### 2. SSH Agent and Developer Tooling
While technically handled by the Desktop app, the extension serves as the entry point for configuring developer environments:
*   **SSH Keys:** 1Password can manage SSH keys and act as your SSH agent. This allows you to authorize Git pushes via Touch ID instead of managing plain text private keys.
*   **Developer Dashboard:** From the extension, you can access the Developer Dashboard to manage Service Accounts, API tokens for the 1Password CLI (`op`), and secrets injection.
