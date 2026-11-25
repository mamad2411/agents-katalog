---
name: servicenow-desktop
description: "Automate ServiceNow agent and integration workflows using MID Server, Agent Client Collector, and Table REST APIs."
category: enterprise
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["servicenow", "mid-server", "agent-client-collector", "itsm", "cmdb-discovery", "ecc-queue", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# ServiceNow Enterprise Desktop & MID Server AI Skill Guide (Claude)

## Overview & Engine Architecture
ServiceNow provides enterprise IT Service Management (ITSM), Configuration Management Database (CMDB) governance, and automated IT Operations Management (ITOM). Hybrid enterprise connectivity is established via the **MID Server (Management, Instrumentation, and Discovery)** on-premise Java daemon and the lightweight **Agent Client Collector (ACC)**. Asynchronous orchestration flows through the **External Communication Channel (ECC Queue - `ecc_queue`)**. Claude operates as a Principal ServiceNow Technical Architect and ITOM Engineer, specializing in **MID Server deployment & clustering**, **Table REST API integration**, **Discovery & Service Mapping pattern debugging**, and **ECC Queue queue tuning**.

### ServiceNow Cloud & MID Server Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 ServiceNow Enterprise Stack                 │
│                                                             │
│  ServiceNow Cloud Instance                                  │
│  ├── ITSM Applications (Incident, Change, Problem, Request) │
│  ├── CMDB (Hardware, Software, Service CIs)                 │
│  └── ECC Queue (`ecc_queue` Ingress / Egress Message Bus)   │
│                                                             │
│  On-Premise Desktop & Infrastructure Tier                   │
│  ├── MID Server Cluster (Java Long-Polling Daemon over 443) │
│  ├── Agent Client Collector (ACC Endpoint Telemetry Daemon) │
│  └── WMI / WinRM / SSH Discovery & Orchestration Probes     │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Table REST API Automation**: Author clean, authenticated Python integration scripts interacting with the ServiceNow Table API (`/api/now/table/incident`, `/api/now/table/cmdb_ci`) with query filters (`sysparm_query`).
2. **MID Server Configuration & Clustering**: Configure `config.xml`, manage Java truststores, tune JVM thread pools (`mid.threads`), and group MID Servers into load-balanced and failover clusters.
3. **Discovery & WMI/WinRM Triage**: Diagnose probe/pattern failures on Windows and Linux targets, evaluating DCOM permissions, WinRM endpoints (`Test-WSMan`), and SSH sudo elevation.
4. **ECC Queue Monitoring & Remediation**: Troubleshoot stuck `ready` state payloads, correlate output payloads with input responses, and purge corrupt queue items.

---

## Production Python Automation: Automated Incident Creator & CMDB CI Linker

Save this script as `servicenow_incident_manager.py` to programmatically open and update high-priority incidents linked to specific CMDB Configuration Items:

```python
"""
ServiceNow Table REST API Incident & CMDB Manager
Creates high-priority incidents linked to specific servers in the CMDB.
"""

import sys
import requests
import json

SERVICENOW_INSTANCE = "https://your-instance.service-now.com"
AUTH = ("rest_admin", "SecureServiceNowPass123!")

def get_ci_sys_id(ci_name: str) -> str:
    url = f"{SERVICENOW_INSTANCE}/api/now/table/cmdb_ci_server"
    params = {
        "sysparm_query": f"name={ci_name}",
        "sysparm_fields": "sys_id,name,ip_address",
        "sysparm_limit": 1
    }
    res = requests.get(url, auth=AUTH, params=params, headers={"Accept": "application/json"})
    res.raise_for_status()
    results = res.json().get("result", [])
    return results[0].get("sys_id") if results else None

def create_incident(ci_name: str, short_desc: str, details: str, urgency: int = 1, impact: int = 1):
    ci_sys_id = get_ci_sys_id(ci_name)
    if not ci_sys_id:
        print(f"Warning: Configuration Item '{ci_name}' not found in CMDB. Proceeding without CI link.")

    url = f"{SERVICENOW_INSTANCE}/api/now/table/incident"
    payload = {
        "short_description": short_desc,
        "description": details,
        "urgency": urgency,
        "impact": impact,
        "category": "Hardware",
        "cmdb_ci": ci_sys_id if ci_sys_id else "",
        "assignment_group": "Hardware Support"
    }

    print(f"Submitting P1 Incident to ServiceNow for CI: {ci_name}...")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    res = requests.post(url, auth=AUTH, json=payload, headers=headers)

    if res.status_code == 201:
        inc = res.json().get("result", {})
        number = inc.get("number")
        sys_id = inc.get("sys_id")
        print(f"✅ Success! Created Incident: {number} [SysID: {sys_id}]")
    else:
        print(f"🚨 Failed with HTTP {res.status_code}:\n{res.text}")

if __name__ == "__main__":
    create_incident(
        ci_name="PROD-DB-SRV01",
        short_desc="Disk Array Degradation Alert on Production Database",
        details="RAID controller reporting physical drive 3 failure on storage array.",
        urgency=1,
        impact=1
    )
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **MID Server Status Shows `Down`** | Host cannot establish outbound HTTPS (443) long-polling connection to the ServiceNow instance or proxy credentials expired. | 1. Verify outbound connectivity: `curl -I https://your-instance.service-now.com`.<br>2. In `C:\ServiceNow\agent\config.xml`, verify proxy host/port and credentials.<br>3. Inspect `agent0.log.0` in `C:\ServiceNow\agent\logs\`. |
| **Discovery Fails: `Credential Test Failed / Access Denied` (WMI/WinRM)** | Windows domain service account lacks local administrative permissions or WinRM service is stopped on target host. | 1. On target host, execute: `winrm quickconfig`.<br>2. Test connectivity from MID host: `Test-WSMan -ComputerName <TargetIP>`.<br>3. Verify credentials in *Discovery $\rightarrow$ Credentials*. |
| **ECC Queue Stuck in `ready` Status** | MID Server worker thread pool (`mid.threads`) saturated with long-running probes. | 1. In ServiceNow, navigate to *MID Server $\rightarrow$ Parameters*.<br>2. Increase max threads: `threads.max = 50`.<br>3. Restart the MID Server Windows service. |
| **Agent Client Collector (ACC) Fails to Register** | ACC API Key revoked or WebSocket endpoint unreachable. | 1. In `acc.yml`, verify `api-key` matches the active instance key.<br>2. Restart ACC service: `Restart-Service -Name "AgentClientCollector"`. |

---

## Command Line Syntax & Operational Recipes

```bash
# 1. Install MID Server as Windows Service via Scripted CLI
cd "C:\ServiceNow\agent"
start-service.bat

# 2. Test Remote WinRM Connection from MID Host via PowerShell
Test-WSMan -ComputerName 192.168.1.50 -Credential (Get-Credential)

# 3. Query ECC Queue Status via ServiceNow REST API
curl -X GET "https://your-instance.service-now.com/api/now/table/ecc_queue?sysparm_query=state=ready^queue=output&sysparm_limit=10" \
     -u "rest_admin:password"
```

### Essential File Locations
- **MID Server Config**: `C:\ServiceNow\agent\config.xml`
- **MID Server Logs**: `C:\ServiceNow\agent\logs\agent0.log.0`
- **Agent Client Collector Config**: `C:\ProgramData\ServiceNow\agent-client-collector\config\acc.yml`

---

## Agent Operational Directive
> **MANDATORY**: MID Servers require only outbound port 443 connectivity to the ServiceNow cloud instance; never require opening inbound firewall ports to the MID host. Use sysparm query filters in REST calls.
