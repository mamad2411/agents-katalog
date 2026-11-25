---
name: devops-infra-orchestrator
description: "Route a DevOps / infrastructure task to the right specialist among 13 — container & compose patterns, self-hosting clusters, post-deploy canary checks, reproducible dev environments, enterprise network-device diagnostics (Cisco IOS, BGP, interfaces, config validation, Netmiko SSH), and homelab networking (setup, VLANs, Pi-hole DNS, WireGuard VPN). USE WHEN a user is provisioning, diagnosing, segmenting, or shipping infrastructure but hasn't named the specific layer or tool."
cluster: devops-infra
version: 1.0.0
---

# DevOps & Infra Orchestrator

The single entry skill for infrastructure work. It locates the task on the **layer ×
operation** map — containers, networks (enterprise or homelab), and the deploy/dev-env edges —
and delegates to one of 13 specialist spokes. The cross-cutting rule every spoke shares — the
**read-only-by-default / change-window-for-mutations** safety boundary — lives in
`devops-infra-core`; read it before any command that changes state on a device, a cluster, or a
production deploy.

## Cluster map (spoke → role)

**Containers & deploy**
- `docker-patterns` — Docker & Compose for local dev, multi-service orchestration, container security, volumes, networking.
- `uncloud` — self-hosting cluster mgmt via the `uc` CLI (Docker + WireGuard mesh + Caddy ingress); deploy, scale, route, inspect.
- `canary-watch` — post-deploy smoke / canary verification of a live URL (HTTP, SSE, assets, console errors, perf regressions).

**Dev environments**
- `flox-environments` — reproducible, cross-platform dev environments (Nix-based, declarative `manifest.toml`); pin system deps, run local services, kill "works on my machine".

**Enterprise network devices**
- `cisco-ios-patterns` — IOS / IOS-XE review: show commands, config hierarchy, wildcard masks, ACL placement, interface hygiene, safe change-window verification.
- `netmiko-ssh-automation` — safe Python/Netmiko automation: read-only collection, bounded batch SSH, TextFSM parsing, guarded config changes, timeouts, error handling.
- `network-bgp-diagnostics` — diagnostics-only BGP triage: neighbor state, route exchange, prefix policy, AS-path inspection, safe evidence collection.
- `network-config-validation` — pre-deployment config review: dangerous commands, duplicate addresses, subnet overlaps, stale references, management-plane risk.
- `network-interface-health` — interface errors, drops, CRCs, duplex mismatches, flapping, speed negotiation, counter trends on routers, switches, and Linux hosts.

**Homelab networking**
- `homelab-network-setup` — home / small-lab network design: gateways, switches, APs, IP ranges, DHCP reservations, DNS, cabling, beginner mistakes.
- `homelab-vlan-segmentation` — split a home network into isolated VLANs (UniFi, pfSense/OPNsense, MikroTik): trunk config, firewall rules, SSID mapping.
- `homelab-pihole-dns` — Pi-hole install, blocklists, DoH, DHCP integration, local DNS records, broken-resolution troubleshooting.
- `homelab-wireguard-vpn` — WireGuard server + peers, key generation, split- vs full-tunnel routing, remote access from mobile and laptop.

## Folded spokes

Additional spokes folded into this cluster; route to them the same way as the map above (load on demand).

**Host security & hardening**
- `healthcheck` — host security audit + risk-tolerance hardening for a machine running an agent runtime / gateway: OS firewall, listening ports, SSH, disk encryption, OS auto-updates, exposure review, plan-then-apply remediation with rollback, and scheduling periodic re-audits. Read-only assessment first; every state change needs explicit approval.

## Routing rules by intent

- **"Set up / run containers locally"** → `docker-patterns`. Self-hosting it on a cluster → `uncloud`.
- **"I just deployed — is it healthy?"** → `canary-watch`. **"Is this *host* secure / harden it before I expose it"** → `healthcheck` (OS firewall, ports, SSH, encryption, updates, exposure).
- **"Make this project's toolchain reproducible / works-on-my-machine"** → `flox-environments`.
- **A router/switch is misbehaving** → start read-only: `network-interface-health` (physical/link), `network-bgp-diagnostics` (routing), `cisco-ios-patterns` (IOS specifics). Automating the collection → `netmiko-ssh-automation`.
- **About to push a device config** → `network-config-validation` first; on Cisco, pair with `cisco-ios-patterns`.
- **Home network: build it** → `homelab-network-setup`. **Secure it** → `homelab-vlan-segmentation` (segments) + `homelab-pihole-dns` (DNS filtering). **Reach it remotely** → `homelab-wireguard-vpn`.

## Standard flow

1. Locate the task: which **layer** (container / dev-env / enterprise-network / homelab-network) and which **operation** (design → diagnose → change → verify).
2. If the task **mutates state** (config push, deploy, firewall rule, container/cluster change), pull the safety boundary from `devops-infra-core` first — diagnose read-only, then change in a window with a rollback.
3. Delegate to the spoke(s). Multi-step asks fan out in operation order — e.g. "lock down my home net" → `homelab-vlan-segmentation` → `homelab-pihole-dns` → `homelab-wireguard-vpn`; "ship + confirm" → `uncloud`/`docker-patterns` → `canary-watch`.
4. Return: chosen spoke(s), whether the action is read-only or a change, the change-window/rollback implied, and the next action.

## Guardrails

See `devops-infra-core`. In short: **diagnose before you change.** The default path on any
device, cluster, or deploy is read-only evidence collection. Treat every mutation — a config
line, a firewall rule, a `uc` deploy, a VLAN cutover — as a change that needs a window, a
rollback, and console/out-of-band access secured first. Network and segmentation changes only
*add* isolation; verify reachability between segments after each step before moving on. Never
widen access (open a port, loosen an ACL, full-tunnel a VPN) without saying so explicitly.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
