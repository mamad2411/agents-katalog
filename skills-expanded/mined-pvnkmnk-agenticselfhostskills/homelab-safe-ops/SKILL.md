---
name: homelab-safe-ops
description: Encodes read-first, no-destroy-by-default safety constraints for all homelab automation.
---

# homelab-safe-ops

This skill is the standing safety contract for all homelab operations. It must be active in any session that touches infrastructure, VMs, containers, networking, storage, or services.

It is **always-on** — load it at the start of every homelab session.

## Invocation

**OpenCode / Codex:** `Invoke homelab-safe-ops`
**Freebuff:** `/skill homelab-safe-ops`

## Core Safety Rules

1. **Read before write.** Always inspect the current state (running services, configs, mounted volumes) before modifying anything.
2. **No destroy by default.** Never delete, stop, or remove a resource unless the user has explicitly requested it by name.
3. **Confirm destructive operations.** For any action that cannot be undone (delete, format, wipe, stop service) pause and confirm with the user.
4. **No direct public exposure.** Never open a port directly to the internet. Prefer Cloudflare Tunnel, WireGuard, or Tailscale.
5. **Credentials stay out of prompts.** Never write tokens, passwords, or API keys into conversation text. Reference env files or secret managers.
6. **Log all changes.** Every change must be loggable to the homelab logbook (`homelab-logbook` skill) and Obsidian (`obsidian-homelab-logbook` skill).
7. **Backup before migrate.** Any data migration or storage operation requires confirming a backup exists first.
8. **Test in staging.** If a staging VM or container exists, test changes there before applying to production.

## Escalation Rules

Stop and ask the user if:
- An operation would affect more than one service at once.
- You are unsure which VM/container a service runs on.
- A config change affects networking or firewall rules.
- Any irreversible action is required that was not explicitly mentioned.

## Companion Skills

- `homelab-change-planner` — plan before acting
- `homelab-logbook` — log after acting
- `homelab-topology-mapper` — know the environment first
- `reverse-proxy-and-tunnel` — safe exposure patterns

## Environment Facts (verified 2026-09-18 — overrides generic assumptions)

- **Proxmox host** `192.168.2.9` (tailnet `100.65.21.28`, MagicDNS `proxmox.tail0ea6ba.ts.net`), PVE 9.2.11. Hardware: 2-core i5-7200U laptop, 8 GB RAM, **5400 RPM HDD = the bottleneck**. Load 8–12 = thrashing (SSH handshakes die — looks like a network fault, isn't). One meaningful workload at a time.
- **CT 101 `homelab-core`** `192.168.2.242` — the only guest; runs Navidrome (production, never restart without asking), slskd, beets 1.6.0.
- **Access**: `ssh root@192.168.2.9` (host) and `ssh root@192.168.2.242` (CT) both work with the `idols@MVNK` key. SSH on the host required deleting TWO firewall DROP rules (cluster + node-level) — see `proxmox-ve-operations` skill before touching PVE firewall rules. `ssh pve` from WSL does not resolve (MagicDNS doesn't work inside WSL) — use IPs.
- **Router**: Bell Home Hub 3000 at `192.168.2.1`. Its ISP-side DNS filter NXDOMAINs test/reserved domains (`example.com` etc.) — if a benign domain mysteriously fails to resolve, this is why; don't debug the app first.
- **Diagnostics over GUI**: `ssh` + `pvesh` beats browser automation for anything the PVE web UI could do; xterm.js consoles in the web UI can be typed into but not read (canvas rendering).
- Full verified state: `pvnkmnk/homelab-proxmox-ansible` → `docs/findings/2026-09-18-homelab-music-library-cleanup.md` (that repo is the canonical homelab authority).

## References

- Proxmox VE docs: https://pve.proxmox.com/wiki/Main_Page
- Cloudflare Tunnel: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/
- Tailscale: https://tailscale.com/kb
- WireGuard: https://www.wireguard.com/
