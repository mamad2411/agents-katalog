---
name: op-biometric-unlock
description: Configure and use biometric unlock for 1Password CLI.
---
# 1Password CLI - Biometric Unlock

Biometric unlock allows you to authenticate 1Password CLI using Touch ID, Face ID, Windows Hello, or system authentication without typing your Master Password every time.

## Configuration
1. Ensure the 1Password desktop app is installed and running.
2. In the 1Password app, go to Settings/Preferences > Developer.
3. Enable "Integrate with 1Password CLI".
4. When you run your next `op` command, you will be prompted to authenticate via biometrics.

## Troubleshooting
- If biometrics don't trigger, verify that the 1Password app is unlocked and running in the background.
- Ensure the CLI version matches the desktop app requirements (v2.0.0 or later).
- In some environments (like SSH sessions), biometric unlock may not be available. You will fallback to manual authentication (`eval $(op signin)`).
