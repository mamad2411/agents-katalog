---
name: ctf-frp
description: Use when pi needs the local frp package for internal tunneling, reverse proxying, port forwarding, dashboard configuration, or temporary exposure of internal services. Trigger on mentions of frp, frpc, frps, reverse tunnel, port forward, or intranet penetration.
---

# Local Assets

- Tool root: wherever `frp` is installed (put it on PATH, or `cd` into its directory).
- Bundles: `frp_0.67.0_windows_amd64`, `frp_0.67.0_linux_amd64`
- Docs: `common.md`, `client-configures.md`, `server-configures.md`

# Workflow

- Decide whether the user needs server (`frps`) or client (`frpc`) mode.
- On this Linux host, prefer the Linux bundle (`frp_*_linux_amd64`).
- Prefer config-file based runs instead of long inline commands.
- Keep bind ports, auth, and dashboard exposure scoped tightly.

# Common Commands

```bash
# frp should be on PATH or run from its install dir (Linux amd64 build)
frps -c ./frps.toml
frpc -c ./frpc.toml
```

# Notes

- Read `common.md` for shared config fields.
- Read `server-configures.md` for `frps` options and `client-configures.md` for `frpc` options.
- Avoid opening public listeners wider than the user asked for.
