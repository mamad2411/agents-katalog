---
name: proxmox-ve-operations
description: Operate, inspect, maintain, back up, restore, and safely evolve Proxmox VE 9 nodes, storage, networking, LXC, and VMs using official-first guidance. Use for Proxmox node administration, guest lifecycle, storage, network, package updates, backup/restore, upgrade planning, API/CLI inspection, and third-party helper-script review.
---

# Proxmox VE Operations

Use this skill for the **platform operations layer** of Proxmox VE 9. Pair it with `proxmox-service-guest-gate` for guest creation, storage allocation, network identity, and rollback approval. This skill does not authorize external changes; it defines how to inspect, plan, validate, and safely execute approved operations.

## Source hierarchy

Use official Proxmox VE documentation first. Treat the Administration Guide, wiki reference pages, built-in CLI help/man pages, and the host’s current UI/API as authoritative for the installed version. Use the Proxmox forum and Community Scripts only as supplemental evidence; never let community automation override official guidance or the project’s approval gates.

Read `references/official-and-community-sources.md` for the current source map and review policy.

## Operating workflow

1. **Classify the operation.** Is it read-only inventory, guest lifecycle, storage/network change, backup/restore, node update/upgrade, security/access control, or third-party automation? Identify the rollback boundary and whether the operation is state-changing.
2. **Inspect before changing.** Use the web UI, `pvesh`, `pvesm`, `pct`, `qm`, `pveversion`, and host network/storage inspection to record non-secret facts. Run `scripts/proxmox_readonly_audit.sh` only on an authorized Proxmox host for a baseline report.
3. **Select the execution boundary.** Use GUI/API/CLI for supported platform operations; use Ansible only after its tasks are idempotent and tested. Keep application configuration inside the guest rather than editing host state unnecessarily.
4. **Plan explicitly.** Record node, affected guest/storage/network object, before/after values, backup status, dependency impact, validation method, rollback method, and required approval. Use `templates/proxmox-operation-plan.md`.
5. **Obtain confirmation.** Before guest creation/deletion, storage allocation/removal, network changes, firewall changes, backup prune/delete, restore, package upgrade, or third-party script execution, obtain explicit user confirmation for the exact operation.
6. **Execute minimally.** Change only approved objects. Capture non-secret task IDs, timestamps, and output summaries. Do not combine an unrelated cleanup with a production change.
7. **Validate and document.** Check guest/node health, storage capacity, network reachability, logs, backup outcome, and workload health. Update non-secret inventory and the rollback record.

## Core operating rules

### Guests and containers

Prefer unprivileged LXC for small Linux service workloads when host-kernel sharing and the required isolation level are appropriate. Use a VM where a separate kernel, stronger isolation, unsupported LXC requirements, or a nested-container policy requires it. Never enable `nesting`, `keyctl`, privileged mode, device mounts, or bind mounts by default; justify and document each exception.

Use storage-backed container mount points for persistent state when backup, snapshots, quotas, or managed lifecycle matter. Treat host bind mounts and device mounts as special cases: they are not managed by the Proxmox storage subsystem and their contents are not included in `vzdump` backups. Never bind mount host system directories into a container.

### Storage and backup

Track free space before allocating or expanding disks. Thin provisioning can overcommit capacity; a full storage can cause guest I/O errors and data corruption. Do not create aliased storage configurations pointing to the same underlying storage. Treat `pvesm free` and destructive volume operations as irreversible.

Use `vzdump`/Proxmox backup facilities for guest configuration and managed volumes, but confirm each container mount point’s backup behavior. Establish a separate backup destination, retention, and restore test before placing irreplaceable data in a guest. A successful backup job is not sufficient; restore into disposable state and validate the recovered service.

### Network and firewall

Preserve current working connectivity. Confirm bridge, gateway, subnet, address allocation, VLAN behavior, and firewall scope before changes. Start self-hosted services on private LAN or private VPN access unless public exposure is separately approved. Test from an authorized client after any change.

**PVE firewall has TWO independent rule sets — check both before diagnosing a "blocked port":** `/cluster/firewall/rules` AND `/nodes/<node>/firewall/rules`. Node rules compile into the kernel's `PVEFW-HOST-IN` chain independently of cluster rules (a cluster-level fix alone can leave a node-level `DROP` shadowing it). Rule changes apply to the kernel live — never reboot to "apply" them. Also: an SSH "banner exchange timeout" on a loaded node means I/O starvation, not a firewall block — check load average first.

### Node updates and upgrades

For routine package updates, inspect repositories, available updates, backups, free root space, and current guest health first. Plan a maintenance window and a console/independent access path before a reboot. For a major upgrade, use the version-specific official upgrade guide, run its checker, verify backups, test on comparable hardware when practical, and do not upgrade while relying on an interruptible remote-only session.

### Community automation

Community Scripts is useful for discovering defaults and one-command installations, but it is third-party automation. Before running a script, inspect its repository, compatibility claim, maintenance state, network requests, privilege requirements, guest/storage/network defaults, rollback behavior, and post-install helper. Prefer the script’s advanced mode for a new guest. Never pipe unreviewed remote content into a root shell, and never run a helper script on a legacy or production guest solely because it is popular.

## Bundled resources

- Read `references/official-and-community-sources.md` for the official source map and community review policy.
- Read `references/operations-cookbook.md` for read-only inspection, backup/restore, updates, storage, and networking command patterns.
- Read `references/windows-wsl-to-proxmox.md` before configuring or operating Windows PowerShell, Windows Terminal, WSL, Ansible, REST API, TLS trust, SSH, or private-VPN access to a Proxmox node.
- Use `templates/proxmox-operation-plan.md` before approved state-changing work.
- Use `scripts/proxmox_readonly_audit.sh` only for authorized, read-only node inventory.
