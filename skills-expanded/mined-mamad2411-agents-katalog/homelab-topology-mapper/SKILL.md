---
name: homelab-topology-mapper
description: Maps Proxmox cluster topology including nodes, VMs, containers, storage, and network layout.
---

# homelab-topology-mapper

Produces a current-state map of the Proxmox homelab cluster. Enumerates all nodes, VMs (QEMU), LXC containers, storage pools, and network bridges. Output is used as the starting context for any change operation.

## Invocation

**OpenCode / Codex:** `Invoke homelab-topology-mapper`
**Freebuff:** `/skill homelab-topology-mapper`

## Workflow Steps

1. **Connect:** Use `mcp/proxmox-mcp.json` to authenticate to Proxmox API.
2. **List nodes:** Enumerate all cluster nodes and their status.
3. **List VMs:** For each node, list all QEMU VMs (ID, name, status, CPU, RAM).
4. **List containers:** For each node, list all LXC containers (ID, name, status, CPU, RAM).
5. **List storage:** Enumerate storage pools with type, size, and usage.
6. **List networks:** Map network bridges and VLANs.
7. **Output:** Render topology as structured Markdown table.
8. **Store:** Optionally write snapshot to `obsidian-homelab-logbook`.

## Output Format

```
## Nodes
| Node | Status | CPU | RAM |

## VMs
| ID | Name | Node | Status | CPU | RAM |

## Containers
| ID | Name | Node | Status | CPU | RAM |

## Storage
| Name | Type | Size | Used |
```

## Verified Baseline (2026-09-18)

Last verified live topology — re-enumerate before acting, but use this as the sanity baseline:

| Object | Value |
|---|---|
| Node | `proxmox` — PVE 9.2.11, `192.168.2.9`, tailnet `100.65.21.28` (i5-7200U 2c/4t, 8 GB, 1 TB 5400 RPM HDD) |
| Storage | `local` (14% used), `local-lvm` (25.6% used) |
| CT 101 | `homelab-core` — `192.168.2.242`, tailnet `100.80.82.44`, 2 vCPU/4 GB (verify before changes), Navidrome + slskd + beets |
| Pool | `apppol` |
| Tailnet | `tail0ea6ba.ts.net`: `mvnk` (Windows PC, 100.69.36.47), `proxmox`, `homelab-core`, `ai`, `pixel-10` |
| Router | Bell Home Hub 3000, `192.168.2.1` — DNS filter NXDOMAINs reserved domains (example.com); account-level, not in hub UI |

Rollback snapshot `pre-dedup-20260917` covers CT 101 rootfs + music volume. Full detail: `pvnkmnk/homelab-proxmox-ansible` → `docs/findings/2026-09-18-homelab-music-library-cleanup.md`, plus `docs/observed-state.md` and `docs/network-map.md` there for the canonical topology.

## Companion Skills

- `homelab-change-planner` — use topology as pre-flight context
- `homelab-safe-ops` — always-on safety gate

## References

- Proxmox VE API: https://pve.proxmox.com/wiki/Proxmox_VE_API
- proxmox-mcp: https://github.com/canvrno/ProxmoxMCP
