---
name: proxmox-api-skill
description: "Manage Proxmox VE clusters via REST API (proxmoxer) — VMs, LXC, storage, backup, Ceph, HA, SDN, firewall, ACME, users, metrics. Use when the user asks about Proxmox, PVE, their homelab cluster or nodes, VMs/containers on Proxmox, vzdump backups, or Proxmox storage/network/firewall configuration."
version: 2.1.0
category: devops
---

# PVE Cluster Management

Complete Proxmox VE management via the REST API using `proxmoxer`.

## Connection (always start here)

Use this skill's **base directory** (announced when the skill loads) — never a relative `./scripts`, since your working directory is the user's project, not this skill:

```python
import sys
sys.path.insert(0, "<SKILL_BASE_DIR>/scripts")  # replace with this skill's actual base directory
from pve_helper import get_proxmox, wait_for_task, fmt_vm, fmt_node, fmt_storage, fmt_task
prox = get_proxmox()
```

`pve_helper` handles the rest:
- **Dependencies** (`proxmoxer`, `python-dotenv`) auto-install on import; if that fails (PEP 668 externally-managed env), the error message tells you the exact command to run.
- **Credentials** resolve through a fallback chain: function params → env vars (`PVE_HOST`, `PVE_USER`, `PVE_TOKEN_NAME`, `PVE_TOKEN_VALUE`, `PVE_VERIFY_SSL`, `PVE_TIMEOUT`) → `.env` in CWD or skill root → `~/.config/pve-skill/credentials.conf`. Debug with `show_creds_source()`.
- **Token setup** (PVE side): Datacenter → Permissions → API Tokens → create token, assign privileges, copy the UUID (shown only once).

## Safety Rules (for agents)

- **Confirm with the user before destructive operations**: deleting VMs/CTs/volumes/pools/OSDs, node shutdown/reboot, snapshot rollback, restore with `force=1`, firewall policy changes, password changes.
- Prefer graceful `shutdown` over hard `stop` for VMs/CTs unless the user asks for a forced stop.
- After any mutation: poll the returned UPID with `wait_for_task()` and check `success` — never assume a task succeeded. For config changes, read the config back to verify.
- Never print or log token values or passwords.

## API Conventions

**Method mappings:** `get()` → GET | `post()`/`create()` → POST | `put()`/`set()` → PUT | `delete()` → DELETE

**Path notation:**
```python
# Dotted (pythonic) — preferred
prox.nodes("pve1").qemu(100).status.current.get()

# String path — for hyphens in endpoint names
prox("nodes/pve1/qemu/100/agent/exec-status").get(pid=1234)
prox.nodes("pve1").storage("local")("download-url").post(...)
```

**Hyphenated parameter names** — proxmoxer does NOT convert underscores to hyphens (in paths or params). Pass hyphenated params via dict unpacking:
```python
prox.nodes("n").vzdump.post(vmid="100", **{"prune-backups": "keep-last=3"})
```

**Task-based operations:** VM create, clone, snapshot, backup, migrate, Ceph OSD create, etc. return UPID strings. Always poll:
```python
upid = prox.nodes("node").qemu(vmid).clone.post(newid=200, full=1)
result = wait_for_task(prox, "node", upid, timeout=600)
assert result["success"], result
```

## Quick Recipes

```python
prox.cluster.resources.get(type="vm")                    # All VMs/CTs cluster-wide
prox.nodes("node").qemu(vmid).status.current.get()       # VM status
prox.nodes("node").qemu(vmid).status.start.post()        # Start VM
prox.nodes("node").qemu(vmid).config.get()               # VM config
prox.cluster.nextid.get()                                # Next free VMID

# Helpers: find_vm_node(prox, vmid), get_vm_status(prox, vmid),
#   list_all_vms(prox, status_filter=..., node_filter=...), cluster_summary(prox),
#   storage_usage(prox, node), backup_list(prox, node, storage)
```

## Category Reference

Read **only** the file(s) relevant to the current task:

| Topic | File |
|---|---|
| Cluster overview, nodes, services, network, DNS, APT, tasks, PCI/USB mapping, metric servers | `references/cluster-nodes.md` |
| QEMU VMs — CRUD, config params, disks, snapshots, guest agent, cloud-init, console | `references/qemu.md` |
| LXC containers — CRUD, config params, disks, snapshots, firewall, console | `references/lxc.md` |
| Storage (15 types), volumes, upload/download, backup jobs, vzdump, restore, ZFS replication | `references/storage-backup.md` |
| Firewall (cluster/node/guest) and SDN (vnets, zones, controllers, IPAM) | `references/firewall-sdn.md` |
| Ceph — OSD, pools, CephFS, MON/MGR/MDS, CRUSH | `references/ceph.md` |
| High Availability — resources, rules (PVE 9+), groups, migrate/relocate | `references/ha.md` |
| Users, groups, roles, ACL, auth domains, TFA, ACME, certificates | `references/access-certificates.md` |
| Full endpoint catalog — every path/method/params, searchable | `references/api-endpoints.md` |

## Pitfalls

1. **Self-signed certs**: Use `verify_ssl=False` until proper certs configured (helper suppresses the urllib3 warning)
2. **Task-based operations**: VM create, clone, snapshot, backup, migrate return UPID — must poll
3. **Cluster-wide vs node-scoped**: `/cluster/resources` shows all VMs; `/nodes/{node}/qemu` shows only that node's
4. **API token permissions**: Token inherits user's permissions unless separated. Verify with `pveum token permissions` on PVE host
5. **LXC rootfs format**: `rootfs="local-lvm:10"` means 10GB on that storage
6. **Network config difference**: VMs use `net0="virtio,bridge=vmbr0"`; LXC uses `net0="name=eth0,bridge=vmbr0,ip=dhcp"`
7. **cluster.status.get()** returns a **list** — iterate checking `type` field
8. **Upload endpoint** requires multipart/form-data; token must have Privilege Separation OFF
9. **NUMA required for memory hotplug**: Set `numa=1` before enabling memory hotplug
10. **SDN changes require apply**: After creating zones/vnets/controllers, call `sdn.apply.post()`
11. **HA Groups deprecated in PVE 9**: Use `ha.rules` instead of `ha.groups`
12. **/nodes/{node}/execute** is batch API calls only — NOT shell execution
13. **Restore uses create endpoints**: POST to `/qemu` or `/lxc` with `archive`/`ostemplate` param
14. **Backup retention**: Use `prune-backups` string, NOT deprecated `maxfiles`
15. **Hyphenated names**: proxmoxer never converts `_` to `-`. Hyphenated endpoints need string path segments (`("download-url")`, `("challenge-schema")`); hyphenated params need `**{"prune-backups": ...}` dict unpacking. A `400 Parameter verification failed` often means an underscore/hyphen mismatch

## Common Errors

| Error | Likely cause | Fix |
|---|---|---|
| `401 Unauthorized` / `authentication failure` | Wrong token value, expired token, wrong `user@realm` | Re-check `PVE_USER` includes realm (`root@pam`), token value is the UUID |
| `403 Permission check failed` | Token lacks privileges, or Privilege Separation limits it | Grant role via ACL on the token itself, or disable Privilege Separation |
| `595 Errors during connection establishment` / `ConnectionError` | Wrong host/port, firewall, node down | Verify `PVE_HOST` reachable on port 8006 |
| `SSLError` / certificate verify failed | Self-signed cert with `PVE_VERIFY_SSL=true` | Set `PVE_VERIFY_SSL=false` or install proper certs |
| `400 Parameter verification failed` | Wrong param name/format for the endpoint | Check exact params in `references/api-endpoints.md` |
| `500 ... does not exist` | Wrong node name or VMID | Use `find_vm_node(prox, vmid)` to locate the guest |
