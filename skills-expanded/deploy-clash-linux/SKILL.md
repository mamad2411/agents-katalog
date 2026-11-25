---
name: deploy-clash-linux
description: Deploy and operate nelvko/clash-for-linux-install on Linux with TUN, upstream proxy nodes, GeoIP updates, and systemd autostart. Use for installation, configuration, troubleshooting, or documenting workflows involving mixin/runtime config, subscription handling, TUN routing, and service management.
---

# Deploy Clash for Linux (nelvko/clash-for-linux-install)

## Overview
Use this skill to install, configure, and operate `nelvko/clash-for-linux-install` on Linux, including TUN mode, upstream LAN proxy-as-node, GeoIP data updates, and systemd autostart.

## Workflow (Recommended)
1. Install and choose a writable `CLASH_BASE_DIR`.
2. Configure upstream LAN proxy node in `mixin.yaml` and add routing exclusions.
3. Merge mixin into `runtime.yaml`.
4. Start the kernel and enable TUN (root required).
5. Verify with logs and route checks.
6. Enable systemd autostart (with `ExecStartPre` auto-merge).

For copy-paste commands, see `references/workflow.md`.
For common failures and fixes, see `references/troubleshooting.md`.

## Key Decisions
- **Kernel**: prefer `mihomo` unless compatibility demands `clash`.
- **Upstream node type**: use `socks5` with `udp: true` when upstream is a mixed port.
- **TUN**: must run as root; service should run under systemd as root for auto-route.
- **IP-echo checks**: if `api64.ipify.org` is set to `DIRECT`, it will show local IP even when proxy works.

## Minimal Safe Defaults
- Keep `allow-lan: false` unless you need LAN access to the UI.
- Add `route-exclude-address` for upstream LAN proxy to avoid routing loops.
- Enable GeoIP auto-update via `geox-url` if you rely on Geo rules.

## References
- Step-by-step commands: `references/workflow.md`
- Troubleshooting: `references/troubleshooting.md`
