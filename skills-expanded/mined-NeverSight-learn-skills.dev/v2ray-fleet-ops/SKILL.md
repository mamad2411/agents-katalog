---
name: v2ray-fleet-ops
description: Operate a multi-node V2Ray fleet over SSH with role-aware targeting (relay, egress, control-plane), including health checks, cautious OS updates, and dependency-conflict-safe maintenance for mixed Debian/CentOS nodes. Use when users ask to check node status, run package upgrades, verify docker/v2ray services, or maintain a V2Ray/SS-panel VPS fleet.
---

# V2Ray Fleet Ops

Use a config file for all SSH endpoints. Do not hardcode hosts/ports/users in commands or in this skill text.

## Quick start

1. Preferred config location: `~/.openclaw/workspace/.config/v2ray-fleet/fleet.prod.json` (private workspace path, not inside skill folder).
2. Copy from `assets/fleet.example.json` (or sanitized `assets/fleet.prod.json`) into that private path.
3. Ensure SSH key-based auth from the OpenClaw gateway to each node.
4. Run role-filtered operations with `scripts/fleet_ops.py`.

Examples:

```bash
# Health check all nodes
python3 skills/v2ray-fleet-ops/scripts/fleet_ops.py \
  --config ~/.openclaw/workspace/.config/v2ray-fleet/fleet.prod.json health

# Health check only CN relay nodes
python3 skills/v2ray-fleet-ops/scripts/fleet_ops.py \
  --config ~/.openclaw/workspace/.config/v2ray-fleet/fleet.prod.json --role relay-cn health

# Upgrade only egress nodes
python3 skills/v2ray-fleet-ops/scripts/fleet_ops.py \
  --config ~/.openclaw/workspace/.config/v2ray-fleet/fleet.prod.json --role egress upgrade
```

## Required config model

Use JSON config with this shape:

- `nodes[]`
  - `name`: display name
  - `host`: DNS/IP
  - `user`: SSH user
  - `port`: SSH port
  - `roles[]`: one or more roles (`relay-cn`, `egress`, `control-plane`, etc.)
  - `notes` (optional)

Schema reference: `references/config.schema.json`.

## SSH setup guidance (pubkey-first)

For each node, from the OpenClaw gateway:

1. Generate a key if missing:
```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
```

2. Install key (if password login is still possible):
```bash
ssh-copy-id -p <port> <user>@<host>
```

3. Verify non-interactive login:
```bash
ssh -o BatchMode=yes -p <port> <user>@<host> 'echo ok'
```

4. Hardening target state:
- Prefer `PubkeyAuthentication yes`
- Prefer `PasswordAuthentication no` after key validation
- Keep a break-glass console path before tightening SSH

## Operations playbook

### 1) Health check

Run `health` first. Confirm:
- OS/kernel/uptime
- root filesystem disk usage and inode usage
- package manager state (`apt` or `dnf`)
- pending updates
- docker present and container status

### 2) Cautious OS upgrade

Run `upgrade` per role batches, not all at once:
- `relay-cn` one node at a time
- `egress` one node at a time
- `control-plane` last

For CentOS Stream nodes with Docker CE conflicts, keep `container-tools` module disabled (as needed) before upgrade.

### 3) Post-upgrade verification

After each node:
- re-run `health`
- confirm v2ray-related containers are up
- confirm control-plane web/db listeners if applicable

## Safety defaults

- Use role filters to avoid fleet-wide blast radius.
- Avoid `--aggressive` unless explicitly requested.
- Stop on first unexpected failure and report exact error.
- For DNF conflicts involving `containerd.io` vs AppStream `runc`, align modules before retrying.

## Files in this skill

- `scripts/fleet_ops.py`: role-aware health/upgrade executor over SSH
- `assets/fleet.example.json`: template config
- `~/.openclaw/workspace/.config/v2ray-fleet/fleet.prod.json`: preferred private location for real prod config
- `references/config.schema.json`: config schema
