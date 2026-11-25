---
name: wsl2-browser-setup
description: "Set up and troubleshoot browser access from WSL2: native Linux Chrome, a Windows Chrome or Edge CDP bridge, or `agent-browser` on either path. Use for WSL browsing, sign-in, CDP connectivity, and `agent-browser` runtime setup; not for browsers outside WSL2."
---

# WSL2 Browser Setup

Use this skill for the complete WSL2 browser path, from browser availability through optional `agent-browser` setup.

## Choose The Path

| Need | Start with | Success signal |
| --- | --- | --- |
| Interactive browsing or sign-in inside WSL | Native WSL Chrome | Normal HTTPS sites and the target sign-in page render in Linux Chrome. |
| A WSL tool must control Windows Chrome or Edge | Windows host browser bridge | WSL reaches the bridge's `/json/version` endpoint. |
| The requested client is `agent-browser` | First establish either browser path, then add the client layer | `agent-browser` opens or attaches to the chosen browser and returns a snapshot. |

Read [`references/architecture.md`](./references/architecture.md) when the correct path is unclear.

## Native WSL Chrome

Run:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-native-wsl-chrome.sh"
```

The script verifies WSL2, installs Linux `google-chrome` when needed, writes the standard Windows `.wslconfig` networking settings, and reports whether a WSL restart is needed.

After a configuration change, have the human run `wsl --shutdown`, reopen WSL, and launch `google-chrome`. In `chrome://settings/security`, turn `Use secure DNS` fully off; `OS default (when available)` is not off. Reopen Chrome and verify a normal HTTPS site plus the real target or sign-in page.

## Windows Host Browser Bridge

Run:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-windows-host-browser-bridge.sh"
```

The script finds Windows Edge or Chrome, launches it with remote debugging, requests Windows elevation for the port proxy and firewall rule, and waits for the CDP endpoint to become reachable from WSL2. It exposes a generic browser endpoint; client attachment is a separate step.

## `agent-browser`

Only add this layer after native Chrome browsing or the Windows bridge is proven. Read [`references/agent-browser.md`](./references/agent-browser.md) for runtime installation, the interactive upstream-skill step, native checks, bridge attachment, and the compatibility wrapper.

## Safe Checks

Use the non-mutating checks first when diagnosing an existing setup:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-native-wsl-chrome.sh" --check-only
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-windows-host-browser-bridge.sh" --check-only
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-agent-browser-runtime.sh" --check-only
```

## Deeper Guidance

- Read [`references/troubleshooting.md`](./references/troubleshooting.md) when a browser launches but browsing, sign-in, bridge access, or `agent-browser` still fails.
- Read [`references/dead-ends.md`](./references/dead-ends.md) before attempting low-level DNS, firewall, package, or client workarounds.
- Use [`scripts/setup-agent-browser-wsl2.sh`](./scripts/setup-agent-browser-wsl2.sh) only when the older one-shot Windows bridge flow is specifically useful.
