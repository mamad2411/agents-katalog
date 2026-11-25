---
name: hm-sa-skill
description: >
  HarmonyOS/OpenHarmony System Ability Manager (SAMgr) daemon domain expertise.
  Covers SA architecture, lifecycle management, IPC/RPC communication patterns,
  service registration/discovery, source code structure, and API reference.
  Use when: (1) Working with OpenHarmony SAMgr / systemabilitymgr_samgr code,
  (2) Questions about SA lifecycle, daemon startup, or boot sequence,
  (3) Implementing or debugging IPC/RPC Proxy/Stub patterns for system services,
  (4) Understanding SA registration (AddSystemAbility, GetSystemAbility, LoadSystemAbility),
  (5) Analyzing SAMgr crash recovery, on-demand loading, or distributed SA routing,
  (6) Navigating the systemabilitymgr subsystem source tree.
---

# HarmonyOS System Ability Manager (SAMgr) Skill

## Overview

SAMgr is the daemon-level service registry and lifecycle manager for all system services in HarmonyOS/OpenHarmony. It plays a role analogous to Android's `servicemanager` + `init` daemon, with stronger lifecycle governance and native cross-device distributed support.

## Knowledge Domains

This skill covers four domains. Load the relevant reference file based on the task:

| Domain | Reference | When to Load |
|--------|-----------|--------------|
| Architecture & Concepts | [references/hm-sa-architecture.md](references/hm-sa-architecture.md) | Understanding SAMgr's role, boot sequence, SA lifecycle, data structures, registration modes |
| API Reference | [references/hm-sa-api-reference.md](references/hm-sa-api-reference.md) | Writing SA code, Proxy/Stub patterns, registration macros, death notifications |
| Source Code Structure | [references/hm-sa-source-structure.md](references/hm-sa-source-structure.md) | Navigating the repo, finding files, understanding build config, SA .cfg format |

## Quick Reference

### SAMgr's Four Roles
1. **Service Registry** — Central table mapping SA ID → proxy object
2. **Lifecycle Manager** — OnStart/OnStop, crash detection, auto-restart
3. **IPC Router** — Local via Binder, cross-device via DSoftBus
4. **Capability Scheduler** — Boot ordering, priority, on-demand loading

### SA Lifecycle
```
Register → Publish → Discovery → IPC Invocation → Reclamation
```

### Core API (C++)
```cpp
// Get SAMgr client
sptr<ISystemAbilityManager> samgr =
    SystemAbilityManagerClient::GetInstance().GetSystemAbilityManager();

// Register SA
samgr->AddSystemAbility(saId, new MyAbility());

// Get SA proxy
sptr<IRemoteObject> obj = samgr->GetSystemAbility(saId);
```

### Boot Sequence
```
init → parse .cfg → SAMgr daemon → foundation (safwk + samgr) → appspawn → apps
```

### Source Repo
- **GitHub**: https://gitcode.com/openharmony/systemabilitymgr_samgr
- **Path**: `foundation/systemabilitymgr/samgr/`

## Fetching Official Docs

To refresh the fetched Huawei developer docs, run:

```bash
# Fetch IPC Kit docs (preset)
python3 scripts/fetch_sa_docs.py --preset ipc --out-dir references/fetched-docs

# Fetch a single doc by slug
python3 scripts/fetch_sa_docs.py --slug ipc-rpc-overview --out /tmp/doc.md

# List all known working slugs
python3 scripts/fetch_sa_docs.py --list-slugs
```

Known working slugs:
- `ipc-rpc-overview` — IPC Kit V13 overview (current)
- `ipc-rpc-overview-0000001427584740-V2` — IPC RPC V2 overview (archived)

## Key Comparison: Android vs HarmonyOS

| Dimension | Android | HarmonyOS SAMgr |
|-----------|---------|-----------------|
| Service Management | Dispersed (app-driven) | Unified (system-driven) |
| Lifecycle | App-controlled | System-controlled |
| Cross-device | None built-in | Natively supported |
| Crash Recovery | Limited | Auto-restart + client notification |

## Recognized SA IDs

| SA ID | Service |
|-------|---------|
| 3001 | PowerManager |
| 3002 | LocationService |
| 3400 | BundleMgrService |
