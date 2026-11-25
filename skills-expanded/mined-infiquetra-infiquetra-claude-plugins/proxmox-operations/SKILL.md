---
name: proxmox-operations
description: Proxmox VE 9.x and Ceph Squid 19.x operational knowledge — correct CLI syntax, VM lifecycle patterns, and cluster management to eliminate trial-and-error
when_to_use: |
  Use this skill when the user:
  - Runs or writes any pvecm, pvesm, pveceph, qm, pct, or ceph commands
  - Creates, clones, migrates, or destroys VMs
  - Manages Ceph OSDs, pools, monitors, or storage
  - Works on proxmox_* Ansible roles
  - Asks how to do something in Proxmox or Ceph
  - Gets an error from a Proxmox CLI tool
  - Is planning an operation on the live cluster
---

# Proxmox VE 9.x Operations

You are helping manage the **olympus** Proxmox VE 9.1.1 cluster. Use the reference docs to provide correct CLI syntax and avoid known PVE 9.x quirks.

Always load these references before answering:
- `references/proxmox-cli-quirks.md` — PVE 9.x-specific behaviors and removed flags
- `references/ceph-operations.md` — Ceph Squid 19.x operational guide
- `references/vm-lifecycle.md` — VM create, clone, migrate, cloud-init patterns

## Quick Reference — Common Operations

### Cluster Status
```bash
pvecm status          # Quorum status and node list
pvecm nodes           # Node IDs and names
corosync-cfgtool -s   # Corosync ring status (network layer)
```

### VM Operations
```bash
qm list               # VMs on this node
qm status <vmid>      # VM power state
qm start <vmid>       # Start VM
qm stop <vmid>        # Graceful shutdown
qm destroy <vmid> --purge  # Delete VM and all disks
qm config <vmid>      # Show VM configuration
```

### Ceph Status
```bash
ceph -s               # Cluster health summary
ceph osd tree         # OSD layout by host
ceph osd df           # OSD disk usage
ceph df               # Pool usage
ceph pg stat          # Placement group status
ceph osd pool ls      # List pools
```

### Storage
```bash
pvesm status          # All storage pools
pvesm list ceph-fast  # Contents of a pool
```

## Ansible Integration

These are the connection details for Ansible-managed Proxmox operations:

```bash
# From ansible/ directory
ansible proxmox_hosts -i inventory/hosts.yml -m ping
ansible proxmox_master -i inventory/hosts.yml -m command -a "pvecm status"
```

See reference docs for specific operation patterns and PVE 9.x quirks before writing new tasks.
