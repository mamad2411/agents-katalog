---
name: devops-infra-core
description: "Shared reference for the devops-infra cluster: the read-only-by-default safety boundary every spoke turns on (diagnose → change-window → verify → rollback), the change-class taxonomy, shared conventions for evidence and isolation, and the tooling/version matrix. USE WHEN any infra task is about to mutate state — a device config, a firewall/VLAN rule, a container or cluster deploy — or when you need the conventions every devops-infra spoke shares."
cluster: devops-infra
version: 1.0.0
---

# DevOps & Infra Core

Shared model for the `devops-infra` cluster. The container, network, and homelab spokes span
very different tools, but they all turn on **one decision**: is this action *read-only*, or does
it *change state*? Keep that boundary consistent here so no spoke quietly normalizes a risky
change.

## 1. The decision the whole cluster turns on (the safety boundary)

Every spoke has two paths. The **default is read-only**; the change path is gated.

```
DIAGNOSE (read-only)  ──>  PLAN change + rollback  ──>  CHANGE WINDOW  ──>  VERIFY  ──>  rollback if regressed
   always safe              write down the undo        out-of-band access     prove it       cheap because planned
```

- **Read-only / diagnose** — show commands, counters, logs, `uc inspect`, a canary probe, a config *review*. Run freely, anytime, in production. This is where triage starts and usually ends.
- **Change / mutate** — a config line pushed, a firewall or ACL or VLAN rule, a `uc` deploy or scale, a container restart, a VPN route. Requires: a known rollback, a maintenance window, and secured console / out-of-band access **before** you touch anything.

**Rule:** never let a diagnosis turn into a change in the same breath. Collect evidence first;
state explicitly when you cross into a change.

## 2. Change-class taxonomy (how risky is this action?)

| Class | Examples | Gate |
|---|---|---|
| **Observe** | show/log/counter, `docker logs`, `canary-watch`, config review, `flox activate` | none — safe in prod |
| **Additive-isolation** | new VLAN, new firewall *deny*, Pi-hole blocklist, new capability scope | window + verify reachability after each step (isolation can over-block) |
| **Mutating** | push device config, `uc deploy`/scale, restart container, change DHCP/DNS | window + rollback + out-of-band access |
| **Widening** | open a port, loosen an ACL, full-tunnel a VPN, expose a service | window + rollback + **explicit** justification (reduces security posture) |

Route by class: `network-config-validation` and `cisco-ios-patterns` gate the *mutating*
device path; `homelab-vlan-segmentation`/`-pihole-dns`/`-wireguard-vpn` are *additive/widening*;
`canary-watch` is the *observe* step that proves a *mutating* deploy.

## 3. Shared conventions

- **Evidence before action.** Capture the before-state (counters, neighbor table, current config, a canary baseline) so you can prove the change helped and roll back to a known point. → `network-interface-health`, `network-bgp-diagnostics`, `netmiko-ssh-automation`, `canary-watch`.
- **Automation defaults to read-only.** Netmiko/SSH and any script collect by default; config push is a separate, peer-reviewed, rollback-backed path. → `netmiko-ssh-automation`.
- **Isolation is added, never silently removed.** VLAN/firewall changes increase separation; verify cross-segment reachability after each step. → `homelab-vlan-segmentation`.
- **Reproducibility over snowflakes.** Pin environments and infra declaratively (Flox `manifest.toml` committed to the repo; Compose files; `uc` service specs) so a teammate or agent reproduces them exactly. → `flox-environments`, `docker-patterns`, `uncloud`.
- **Verify the deploy, don't assume it.** A merge or release isn't done until a canary confirms the live endpoint. → `canary-watch`.

## 4. Tooling / version matrix

| Layer | Tool / target | Spoke |
|---|---|---|
| Containers (local) | Docker + Docker Compose | `docker-patterns` |
| Self-hosting cluster | `uc` CLI — Docker + WireGuard mesh + Caddy | `uncloud` |
| Post-deploy check | HTTP / SSE / asset / console / perf probes | `canary-watch` |
| Dev environments | Flox (Nix-based, `manifest.toml`, 150k+ pkgs, macOS + Linux) | `flox-environments` |
| Enterprise switches/routers | Cisco IOS / IOS-XE | `cisco-ios-patterns`, `network-config-validation` |
| Network automation | Python + Netmiko + TextFSM | `netmiko-ssh-automation` |
| Routing | BGP | `network-bgp-diagnostics` |
| Physical / link layer | router, switch, Linux interfaces | `network-interface-health` |
| Homelab gateway/switch/AP | UniFi · pfSense/OPNsense · MikroTik | `homelab-network-setup`, `homelab-vlan-segmentation` |
| Local DNS filtering | Pi-hole (+ DoH, DHCP) | `homelab-pihole-dns` |
| Remote access | WireGuard | `homelab-wireguard-vpn` |

## 5. Shared guardrails

- **Read-only by default.** Diagnose first; cross into a change only deliberately, and say so.
- **Plan the rollback before the change** — and secure console / out-of-band access first; a network change can cut the path you're connected over.
- **Change window for anything Mutating or Widening.** Verify after each step; don't batch unverified changes.
- **Isolation changes add, never remove** — confirm reachability between segments after each step.
- **State every access-widening change** (open port, loosened ACL, full-tunnel VPN, exposed service) explicitly — it lowers the security posture.
- **Pin and commit** environment/infra definitions so they're reproducible, not snowflakes.
- **A deploy isn't done until a canary confirms it** on the live endpoint.
