---
name: proxmox-service-guest-gate
description: Plan, inspect, approve, create, validate, and roll back a fresh Proxmox service guest while protecting legacy guests. Use before creating or changing an LXC or VM for self-hosted services, especially on resource-constrained Proxmox hosts.
---

# Proxmox Service Guest Gate

Use this skill to prevent a self-hosting plan from becoming an unreviewed Proxmox change. It separates read-only inventory from state-changing creation, makes guest parameters explicit, and preserves legacy guests unless the user separately authorizes work on them. Read `proxmox-ve-operations` first for official-first storage, networking, backup, update, CLI/API, and community-script guidance; use this skill for the creation-specific approval gate.

## Change-gated workflow

1. **Inventory read-only.** Inspect node health, CPU/RAM, storage pools, existing guests, bridge/network, templates, backups, and the next available guest ID. Record only non-secret facts.
2. **Classify existing guests.** Mark each guest as managed, legacy, disposable, or unknown. A legacy guest is out of scope: do not reconfigure, stop, migrate, delete, or reuse it implicitly.
3. **Write the guest proposal.** Specify guest type, ID, hostname, CPU, RAM, swap, root disk, data disk, storage pool, network bridge, address strategy, runtime features, autostart behavior, service scope, data paths, backup boundary, and rollback condition.
4. **Check resource fit.** Reserve enough headroom for the Proxmox host and existing workloads. Start with the smallest guest that can validate the first services. Defer resource-heavy services until measured behavior supports them.
5. **Stop at the confirmation gate.** Immediately before creation, show the exact state-changing request: guest ID, hostname, storage allocation, network identity, runtime features, and first-service scope. Obtain explicit confirmation. General permission to continue is not approval for changed parameters.
6. **Create only the approved guest.** Record the resulting non-secret guest ID, storage volumes, address, and configuration. Do not make unrelated Proxmox changes.
7. **Validate before data.** Confirm boot, private-LAN access, updates, storage mounts, logs, runtime prerequisites, health checks, and the backup plan before placing irreplaceable media or databases.
8. **Roll back safely.** If the guest fails validation, stop deployment. Destroy only the newly created disposable guest after confirming it contains no user data. Never use rollback as justification to alter legacy guests.

## Default safety decisions

Use a fresh unprivileged Debian LXC for light always-on services when a full VM is unnecessary. Enable `nesting` or `keyctl` only when the selected container runtime requires them and record why. Start with private LAN or private VPN access; public exposure is a later, separately approved change.

Place first services in stages. Deploy a low-resource pair first, measure CPU/RAM/disk I/O, establish backups, run a disposable restore, then add database- or thumbnail-heavy services. Treat the suggested sizing as an assumption until the current node inventory is confirmed.

## Required confirmation record

Before creation, write or present a table containing: node; new guest ID; hostname; guest type; vCPU; RAM/swap; root/data volumes and storage pools; bridge; DHCP reservation or static address; runtime features; autostart timing; first services; backup destination; and rollback boundary. Use `templates/guest-change-request.md`.

## Bundled resources

- Read `references/guest-validation.md` for the read-only, creation, validation, and rollback gates.
- Use `templates/guest-change-request.md` for the user-confirmation request. Do not perform the creation action until the exact request is approved.
