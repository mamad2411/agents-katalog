---
name: inventory-sync
description: Validates inventory consistency and generates checklists when hardware changes — prevents cascade update misses across host_vars, group_vars, monitoring, and playbooks
when_to_use: |
  Use this skill when the user:
  - Is adding a new server/node to the Proxmox cluster
  - Is decommissioning or removing a server
  - Changes an IP address, NIC name, or disk configuration
  - Modifies host_vars or group_vars files
  - Says "add a new node", "decommission", "hardware swap", "replace server"
  - Asks what files need to be updated when hardware changes
  - Wants to check that all inventory references are consistent
---

# Inventory Sync — Olympus Cluster

You are helping maintain inventory consistency for the **olympus** Proxmox cluster. Hardware changes require updating multiple files — this skill ensures nothing is missed.

## Inventory File Map

The olympus cluster inventory spans these files:

```
ansible/
├── inventory/
│   ├── hosts.yml                          # Group memberships, ansible_host IPs
│   └── host_vars/
│       ├── r420.infiquetra.com.yml        # Ceph bulk OSDs, ceph_nic
│       ├── r640-1.infiquetra.com.yml      # Ceph fast OSDs, ceph_nic
│       ├── r640-2.infiquetra.com.yml
│       ├── r640-3.infiquetra.com.yml
│       ├── r720xd.infiquetra.com.yml
│       └── r820.infiquetra.com.yml
├── inventory/group_vars/
│   └── all/
│       └── all.yml                        # Vault-encrypted shared vars
└── roles/*/defaults/main.yml              # Role-level defaults
```

## Hardware Onboarding Checklist

When adding a new Proxmox node, update **every** file in this list:

### 1. `ansible/inventory/hosts.yml`

```yaml
# Add to ALL applicable groups:
proxmox_hosts:
  hosts:
    <new-hostname>.infiquetra.com:
      ansible_host: 10.220.1.<x>

proxmox_nodes:        # If not the master
  hosts:
    <new-hostname>.infiquetra.com:
```

### 2. `ansible/inventory/host_vars/<new-hostname>.infiquetra.com.yml`

Create this file with the full disk/NIC definition. Required variables:

```yaml
# Ceph cluster network NIC (the 10GbE interface)
ceph_nic: nic0          # e.g. nic0, nic4 — check 'ip link' on the physical host

# Ceph OSD disk definitions
ceph_disks:
  - name: nvme0n1       # kernel device name (no /dev/ prefix)
    device_class: ssd   # 'ssd' or 'hdd'
  - name: sdc
    device_class: ssd

# iDRAC management IP (for IPMI monitoring)
idrac_ip: 10.220.1.<management_ip>
```

**For fast-tier nodes (R640s)**: use `device_class: ssd` or `device_class: nvme`
**For bulk-tier nodes (r420, r720xd, r820)**: use `device_class: hdd`

### 3. Monitoring scrape targets

The Prometheus config in `roles/monitoring/files/prometheus/prometheus.yml` has static scrape targets. Add the new node's IP to:

- `node_exporter` job — scrape `<ip>:9100`
- `ipmi_exporter` job — add iDRAC IP to the targets list
- (If Proxmox host) `pve_exporter` job — add to proxmox targets

### 4. CLAUDE.md hardware table

Update the hardware table in `CLAUDE.md` with the new node's specs.

### 5. Ansible Vault (if node has unique credentials)

If the new node uses a different iDRAC password, add to vault:
```bash
ansible-vault edit inventory/group_vars/all/all.yml --vault-password-file ~/.vault_pass.txt
```

---

## Hardware Decommission Checklist

When removing a node, clean up these locations:

- [ ] Remove from `inventory/hosts.yml` (all groups)
- [ ] Delete `inventory/host_vars/<hostname>.infiquetra.com.yml`
- [ ] Remove scrape targets from monitoring Prometheus config
- [ ] Remove from Ceph cluster: `ceph osd out osd.<id>` then drain PGs
- [ ] Remove from corosync: `pvecm delnode <hostname>`
- [ ] Remove from `CLAUDE.md` hardware table
- [ ] Verify no role `defaults/main.yml` references the hostname directly

---

## Variable Dependency Map

Key variables and where they flow:

| Variable | Defined In | Used In |
|----------|-----------|---------|
| `ansible_host` | `hosts.yml` | All SSH connections |
| `ceph_nic` | `host_vars/<host>.yml` | `proxmox_network/tasks/setup.yml` — creates vmbr1 bridge |
| `ceph_disks` | `host_vars/<host>.yml` | `proxmox_ceph/tasks/setup.yml` — creates OSDs |
| `idrac_ip` | `host_vars/<host>.yml` | `monitoring/files/prometheus.yml` — IPMI scrape |
| `proxmox_master` | `group_vars/all/all.yml` | `delegate_to:` in cluster/ceph roles |
| `proxmox_cluster_name` | `group_vars/all/all.yml` | `proxmox_cluster/tasks/setup.yml` — pvecm create |
| `vault_*` | `group_vars/all/all.yml` (encrypted) | Roles that need credentials |

---

## Consistency Validation Commands

Check all hosts in a group have the same required variables:

```bash
# Verify all proxmox_hosts have ceph_nic defined
ansible proxmox_hosts -i inventory/hosts.yml -m debug \
  -a "msg={{ ceph_nic | default('MISSING') }}"

# Verify all proxmox_hosts have ceph_disks defined
ansible proxmox_hosts -i inventory/hosts.yml -m debug \
  -a "msg={{ ceph_disks | default('MISSING') }}"

# Check ansible connectivity to all hosts
ansible all -i inventory/hosts.yml -m ping
```

---

## IP Address Reference

Current cluster IPs — verify consistency across `hosts.yml`, host_vars, and monitoring configs:

| Host | Main IP | Ceph IP | iDRAC IP |
|------|---------|---------|----------|
| r420 | 10.220.1.7 | 10.220.2.7 | 10.220.1.17 |
| r640-1 | 10.220.1.8 | 10.220.2.8 | 10.220.1.18 |
| r640-2 | 10.220.1.9 | 10.220.2.9 | 10.220.1.19 |
| r720xd | 10.220.1.10 | 10.220.2.10 | 10.220.1.20 |
| r820 | 10.220.1.11 | 10.220.2.11 | 10.220.1.21 |
| r640-3 | 10.220.1.12 | 10.220.2.12 | 10.220.1.22 |

VM IPs (agent VMs 100-107 → 10.220.1.50-57, service VMs 200-203 → 10.220.1.60-63)

When changing an IP, search for stale references:
```bash
grep -r "<old_ip>" ansible/  # Find all files referencing the old IP
```
