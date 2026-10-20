---
name: managing-glinet-routers
description: Diagnoses, configures, repairs, and documents GL.iNet routers running stock firmware or OpenWrt through SSH, BusyBox, UCI, ubus, LuCI, and model-aware workflows. Use when a user mentions GL.iNet, Flint, Slate, Beryl, Mudi, Brume, Puli, Spitz, Marble, GL-MT, GL-BE, GL-XE, GL-AXT, GL-A1300, GoodCloud, AstroMesh, repeater mode, cellular modems, VLANs, Wi-Fi, WireGuard, OpenVPN, firmware, recovery, or router-specific shell commands. Do not use for GL.iNet Comet KVM tasks unless the request is specifically about a router connected to the KVM.
license: MIT
compatibility: Requires an SSH client for command execution. Router-side scripts target BusyBox ash and are intended primarily for stock GL.iNet firmware 4.x or OpenWrt; detect the actual model, firmware, target, and available commands before making changes.
metadata:
  author: Nicholas Bennett
  version: "0.1.0"
---

# Managing GL.iNet Routers

Help the user inspect, troubleshoot, configure, and recover GL.iNet routers without assuming that two models or firmware releases behave identically.

## Core behavior

Use this order unless the user already supplied trustworthy output for a step:

1. Identify the device and management path.
2. Gather read-only evidence.
3. Explain the likely cause from that evidence.
4. Back up the affected configuration.
5. Provide exact commands for the smallest safe change.
6. Verify the result.
7. Provide a rollback command or recovery route.

Do not repeat questions that the user has already answered. When the user supplies terminal output, reason from that output instead of restarting generic troubleshooting.

## Scope boundary

Use this skill for GL.iNet routers and GL.iNet-customized OpenWrt.

Do not assume that a GL.iNet-branded non-router product uses OpenWrt. In particular, Comet and Comet Pro KVM tasks are outside this skill unless the task concerns a separate GL.iNet router.

Generic OpenWrt guidance may be relevant, but preserve GL.iNet-specific services and UI integration. Avoid replacing stock configuration wholesale with vanilla OpenWrt examples.

## Required preflight

Before giving a mutating command, determine as many of these as the available evidence permits:

- Exact model and board name
- Stock GL.iNet firmware versus vanilla/custom OpenWrt
- Firmware and OpenWrt versions
- Architecture and target
- Current management IP and SSH port
- Whether access is local, VPN, GoodCloud, or another remote path
- Network stack: DSA, swconfig, or vendor-specific switch handling
- Firewall stack: firewall4/nftables or firewall3/iptables
- Relevant interface, radio, bridge, modem, and UCI section names
- Whether the requested change can break the current management session

Start with the commands in [platform detection](references/platform-detection.md).

When the user can run a bundled script, use:

```sh
sh scripts/collect-glinet-diagnostics.sh
```

The script is read-only, but the user must review its output before sharing.

## Command presentation

For changes, present commands in this structure:

```text
READ-ONLY CHECK
<commands>

BACKUP
<commands>

CHANGE
<commands>

VERIFY
<commands>

ROLLBACK
<commands>
```

Mark connectivity-impacting commands with:

```text
DISRUPTIVE: this may disconnect the current SSH session.
```

Give straight copy-and-paste commands when the environment is known. Use clearly named shell variables only when they reduce repeated editing or protect against applying a command to the wrong interface.

Do not hide important state changes inside an unexplained one-liner.

## Safety rules

Follow [safe changes](references/safe-changes.md).

Critical rules:

- Never request or print passwords, Wi-Fi keys, VPN private keys, preshared keys, API tokens, cloud tokens, or SIM PIN/PUK values.
- Never place a router password directly in a command line.
- Never use `sshpass` as the default authentication method.
- Never run `firstboot`, `jffs2reset`, `sysupgrade -n`, `mtd`, raw flash writes, factory reset, or U-Boot recovery without explicit user intent and a model-correct recovery plan.
- Never flash firmware based only on a product nickname. Verify the exact model and hardware revision.
- Never restart networking blindly over the only remote management path.
- Never replace `/etc/config/network`, `/etc/config/wireless`, or `/etc/config/firewall` wholesale when a targeted UCI change will work.
- Never assume a configuration backup can safely restore across firmware versions.
- Never assume radio indexes, interface names, modem device nodes, or GL service names from another model.
- Never change cellular RAT, bands, APN, SIM slot, or modem firmware while treating it as a harmless diagnostic.
- Never disable firewall, VPN kill switch, or DNS protections without explaining the exposure created.

## Read-only discovery

Prefer commands that exist on BusyBox/OpenWrt:

```sh
ubus call system board
cat /etc/openwrt_release 2>/dev/null
cat /etc/glversion 2>/dev/null
cat /tmp/sysinfo/model 2>/dev/null
uname -a
uci show network
uci show wireless
uci show firewall
uci show dhcp
ubus call network.interface dump
ip addr show
ip route show
logread | tail -n 200
dmesg | tail -n 200
```

Probe command availability before relying on optional utilities:

```sh
command -v bridge
command -v nft
command -v iptables
command -v swconfig
command -v iw
command -v wg
command -v gl_modem
command -v uqmi
command -v qmicli
command -v mmcli
```

Do not present absence of an optional command as proof that a feature is unsupported.

## Configuration method

Prefer UCI for settings managed by OpenWrt:

```sh
uci changes
uci export network
uci show network
```

For a planned change:

1. Export or copy the affected configuration.
2. Use `uci batch` or targeted `uci set`, `uci add`, and `uci delete`.
3. Show `uci changes <package>`.
4. Commit only the affected package.
5. Reload the narrowest applicable service.
6. Verify runtime state and persistent UCI state.

Example pattern:

```sh
STAMP="$(date +%Y%m%d-%H%M%S)"
uci export network >"/tmp/network-before-$STAMP.uci"

uci batch <<'EOF'
# Insert model-verified commands here.
EOF

uci changes network
uci commit network
```

Do not copy this pattern into production with placeholders still present.

## Troubleshooting method

Build a hypothesis from evidence instead of listing every possible fix.

Use this progression:

1. Physical/link state
2. Interface and address state
3. Routes and policy rules
4. DNS
5. Firewall and zones
6. GL.iNet orchestration services
7. VPN/policy routing
8. Hardware acceleration, flow offload, DPI, or vendor acceleration
9. Kernel/driver/modem logs
10. Firmware-specific defect or regression

When a change fails, compare:

- Intended UCI state
- Runtime state from ubus/ip/bridge/iw/wg
- Relevant daemon status and logs
- Whether a GL.iNet service regenerated or overrode the setting

## Topic references

Load only the relevant reference:

- Device, target, DSA, firewall, and service detection: [platform detection](references/platform-detection.md)
- Backups, commits, reloads, remote-session safety, and rollback: [safe changes](references/safe-changes.md)
- WAN, LAN, DHCP, bridges, VLANs, routes, and firewall zones: [networking and VLANs](references/networking-and-vlans.md)
- Radios, SSIDs, repeater, MLO, mesh, and AstroMesh: [wireless and mesh](references/wireless-and-mesh.md)
- WireGuard, OpenVPN, policy routing, kill switches, and DNS: [VPN and DNS](references/vpn-and-dns.md)
- Cellular modems, APNs, SIMs, RAT, bands, and AT/QMI/MBIM tooling: [cellular](references/cellular.md)
- Firmware, backups, sysupgrade, U-Boot, and debricking: [firmware and recovery](references/firmware-and-recovery.md)

## Output quality

A useful answer should include:

- What the evidence shows
- The most likely cause
- Exact commands appropriate to the detected device
- Which command is disruptive
- What successful output should look like
- How to roll back
- Any uncertainty caused by missing model or firmware details

Avoid long generic tutorials when the user asked for a direct command. Explain only the parts needed to apply the command safely.
