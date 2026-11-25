---
name: ptc-windchill
description: "Automate Windchill PLM workflows through OData APIs, inspect Workgroup Manager integration, and troubleshoot MethodServer operations."
category: enterprise
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["ptc-windchill", "pdmlink", "plm", "workgroup-manager", "odata-rest", "methodserver", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# PTC Windchill PLM Engineering AI Skill Guide (Claude)

## Overview & Engine Architecture
PTC Windchill is an enterprise-scale Product Lifecycle Management (PLM) platform powering product data management (PDM), multi-CAD data vaulting, multi-level Engineering Bill of Materials (eBOM/mBOM), and formal Change Management (PR $\rightarrow$ CR $\rightarrow$ CN). Windchill runs on a distributed Java architecture consisting of the **ServerManager**, **MethodServer**, **BackgroundManager**, **Info*Engine**, and client-side **Workgroup Managers (WWGM)** for Creo, SolidWorks, NX, and CATIA. Claude operates as a Principal PLM Systems Architect and Windchill Enterprise Administrator, specializing in **Windchill REST / OData API automation**, **MethodServer performance tuning (`xconfmanager`)**, **WWGM CAD workspace synchronization**, and **workflow process orchestration**.

### PTC Windchill Core Architecture & Runtime Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 PTC Windchill PLM Architecture              │
│                                                             │
│  Client & Authoring Ingress                                 │
│  ├── Windchill Web UI & Creo View 3D Lightweight Visualizer │
│  ├── Windchill Workgroup Manager (Creo, SolidWorks, CATIA)  │
│  └── Windchill REST / OData Web Services Ingress            │
│                                                             │
│  Enterprise Business Logic Layer                            │
│  ├── MethodServer (Main User Request & Query Processing)    │
│  ├── BackgroundManager (Asynchronous Queues & Publishing)   │
│  └── Windchill Workflow & Lifecycle State Promotion Engine  │
│                                                             │
│  Persistence & Storage Layer                                │
│  ├── RDBMS Metadata Repository (Oracle Database / SQL Server)│
│  └── Windchill Content Vault (Blob storage, replica caches) │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **OData REST API Automation**: Author Python scripts interacting with Windchill's REST API (`/Windchill/servlet/odata/v1/ProdMgmt/`) to extract multi-level indented BOMs, check out/in `WTPart` records, and link CAD documents.
2. **Server Configuration & `xconfmanager`**: Manage declarative server property updates in `site.xconf` and propagate changes safely into `wt.properties`.
3. **WWGM Workspace & Cache Remediation**: Diagnose CAD check-in failures, corrupted local client workspaces (`%APPDATA%\PTC\Windchill\CC`), and SSL Java keystore trust issues.
4. **Change Management (CMII) & Workflow Triage**: Troubleshoot stalled Change Notices (CN), orphaned workflow tasks, and unassigned product context roles.

---

## Production Python Automation: Automated Multi-Level Indented BOM Extractor (OData)

Save this script as `extract_windchill_bom.py` to extract multi-level indented BOM structures via Windchill OData REST endpoints:

```python
"""
PTC Windchill OData REST API Multi-Level BOM Extractor
Traverses WTPart structures to generate indented eBOM hierarchies.
"""

import sys
import os
import requests
from requests.auth import HTTPBasicAuth
import json

WINDCHILL_BASE = "https://windchill.enterprise.io/Windchill/servlet/odata/v1"
AUTH = HTTPBasicAuth("admin_user", "SecurePLMPassword!")

def get_part_by_number(part_number: str) -> dict:
    url = f"{WINDCHILL_BASE}/ProdMgmt/Parts"
    params = {"$filter": f"Number eq '{part_number}'", "$expand": "Attributes"}
    res = requests.get(url, auth=AUTH, params=params, verify=True)
    res.raise_for_status()
    data = res.json()
    items = data.get("value", [])
    return items[0] if items else None

def get_child_parts(part_id: str) -> list:
    url = f"{WINDCHILL_BASE}/ProdMgmt/Parts('{part_id}')/Uses"
    res = requests.get(url, auth=AUTH, verify=True)
    if res.status_code == 200:
        return res.json().get("value", [])
    return []

def traverse_bom(part_number: str, level: int = 0):
    part = get_part_by_number(part_number)
    if not part:
        print(f"{'  ' * level}• Part '{part_number}' not found.")
        return

    part_id = part.get("ID")
    part_name = part.get("Name", "Unnamed")
    part_state = part.get("State", {}).get("Value", "INWORK")
    version = f"{part.get('Version', 'A')}.{part.get('Iteration', '1')}"

    indent = "  " * level
    print(f"{indent}• [{level}] {part_number} - {part_name} (Rev: {version}, State: {part_state})")

    children = get_child_parts(part_id)
    for child in children:
        child_num = child.get("Number")
        if child_num:
            traverse_bom(child_num, level + 1)

if __name__ == "__main__":
    print("--- [FETCHING WINDCHILL INDENTED eBOM] ---")
    traverse_bom("ASM-001042-00", level=0)
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **WWGM Check-In Fails: `Unable to Connect to Server`** | The client JRE does not trust the Windchill server SSL certificate, or local cache is corrupted. | 1. Import Windchill SSL certificate into client Java truststore: `keytool -import -alias wc_ssl -file server.crt -keystore cacerts`.<br>2. Clear local WWGM client cache: Delete `%APPDATA%\PTC\Windchill\CC`. |
| **Promotion Request Stuck in `Pending Approval`** | The workflow assigned task to a Product Role (e.g. `Approver`) that has no assigned members in the team context. | 1. In Windchill, navigate to *Site $\rightarrow$ Utilities $\rightarrow$ Workflow Administration*.<br>2. Find stuck process instance $\rightarrow$ Check **Task Assignments**.<br>3. Open *Product Team* page and add users to the required Role. |
| **MethodServer Crashes: `java.lang.OutOfMemoryError: Java heap space`** | High volume of CAD visualization thumbnail generation or unindexed large product structure queries. | 1. Increase MethodServer max heap in `site.xconf`: `xconfmanager -s wt.method.maxHeap=16384 -t codebase/wt.properties -p`.<br>2. Offload heavy thumbnail conversions to dedicated **CAD Worker Agents**. |
| **Content Replication Fails: File Missing in Local Vault** | Background file replication job stalled or network timeout between master and replica vault servers. | 1. In Windchill, open *Site $\rightarrow$ Utilities $\rightarrow$ File Server Administration*.<br>2. Inspect replication queues for failed synchronization transactions.<br>3. Run manual synchronization for the target folder. |

---

## Command Line Syntax & Server Administration

```bash
# 1. Update Windchill Configuration Parameter Safely via xconfmanager
cd C:\ptc\Windchill\codebase
xconfmanager -s wt.session.timeout=60 -t wt.properties -p

# 2. Check Real-Time Server Manager & MethodServer Process Status
windchill wt.manager.ServerManager

# 3. Launch Interactive Windchill Java Shell
windchill shell

# 4. Stop and Restart Background Queue Processing Engine
windchill wt.queue.QueueControl stop
windchill wt.queue.QueueControl start
```

### Essential File & Directory Locations
- **Master Declarative Config**: `C:\ptc\Windchill\site.xconf`
- **Compiled Properties**: `C:\ptc\Windchill\codebase\wt.properties`
- **MethodServer Logs**: `C:\ptc\Windchill\logs\MethodServer-*.log`

---

## Agent Operational Directive
> **MANDATORY**: Never edit `wt.properties` directly by hand; always update `site.xconf` using `xconfmanager -s <property>=<value> -t <target> -p` to maintain configuration persistence across server builds and updates.
