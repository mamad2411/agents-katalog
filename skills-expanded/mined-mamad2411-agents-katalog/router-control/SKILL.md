---
name: router-control
description: >
  Universal home network discovery and device control via router.
  Use when: (1) discovering devices on local network, (2) SSH into a router,
  (3) managing WireGuard/VPN on a router, (4) setting up AdGuard Home / DNS filtering,
  (5) controlling smart home devices found via DHCP, (6) checking device online status.
  Works with any router (OpenWrt, GL.iNet, ASUS, TP-Link, etc.) — auto-detects model and capabilities.
  Designed for local Mac/Linux deployment with OpenClaw.
---

# Router Control

Universal home router discovery and device management. Zero config — auto-detects your router, finds all devices, identifies them from community-maintained YAML profiles.

## Quick Start

```bash
python3 cli.py discover        # Find router + all LAN devices
python3 cli.py connect         # SSH into router (key → password → defaults)
python3 cli.py devices         # List devices with type identification
python3 cli.py supported       # What devices are supported
python3 cli.py commands lg-webos  # What can this device do
python3 cli.py health          # Router health check
```

## How It Works

1. **discover.sh** — Finds router via default gateway, detects fake IPs (Clash TUN), probes SSH/HTTP
2. **connect.sh** — Establishes SSH (tries key → password → common defaults)
3. **devices.sh** — Reads DHCP leases, matches against `devices/**/*.yaml` profiles via `registry.py`
4. **registry.py** — Auto-scans all YAML in `devices/`, provides `identify(mac, hostname)` matching

## Device Profiles

Community-maintained YAML files in `devices/<type>/`:

```
devices/
  router/    OpenWrt, GL.iNet, ASUS Merlin, TP-Link
  tv/        LG webOS, Samsung Tizen, Roku
  ir-remote/ BroadLink, Tuya IR
  speaker/   Google Nest, Amazon Echo
  camera/    Reolink, Hikvision
  ac/        Generic IR AC
  iot/       ESP/Tuya, Tasmota
```

Each YAML defines: `device` (metadata), `discovery` (MAC/hostname/mDNS), `connection` (protocol/auth), `commands` (what the device can do).

See `devices/_schema.yaml` for the template. Full schema: `references/device-schema.md`.

## Adding a New Device

1. Create `devices/<type>/my-device.yaml` (copy from `_schema.yaml`)
2. Fill in discovery (MAC prefix + hostname pattern), connection, commands
3. Test: `python3 cli.py supported` should list it
4. Submit PR

See `references/contributing.md` for the full guide.

## Shell Scripts (Advanced)

Direct router access when you need raw control:

```bash
bash scripts/run.sh "wg show"           # Run any command on router
bash scripts/ping.sh "LGwebOSTV"        # Ping by hostname
bash scripts/health.sh                  # Full health dump
```

## Troubleshooting

See `references/troubleshooting.md` for:
- Fake IPs (VPN/Clash TUN masquerading as router)
- ISP port blocking on WireGuard
- SSH auth failures with Dropbear
- Double NAT detection
- Router memory pressure
