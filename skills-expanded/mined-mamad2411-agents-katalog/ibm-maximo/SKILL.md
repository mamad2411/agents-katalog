---
name: ibm-maximo
description: "Automate IBM Maximo asset workflows with MBO Jython scripts, OSLC REST interfaces, and MIF integrations."
category: enterprise
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["ibm-maximo", "maximo-application-suite", "eam", "mbo-scripting", "jython", "mif-integration", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# IBM Maximo Enterprise Asset Management AI Skill Guide (Claude)

## Overview & Engine Architecture
IBM Maximo Asset Management (and Maximo Application Suite / MAS) is the world's leading enterprise asset management (EAM) platform, powering physical asset tracking, work order lifecycles, preventive maintenance (PM), supply chain inventory, and service contracts across global infrastructure. Maximo runs on a multi-tier Java enterprise runtime (WebSphere / Open Liberty / Red Hat OpenShift), utilizing the **Maximo Business Object (MBO) Component Framework**, the **Maximo Integration Framework (MIF)**, and embedded **Jython / JavaScript Automation Scripting**. Claude operates as an Enterprise Maximo Solution Architect and SRE, specializing in **MBO / MboSet Jython script development**, **OSLC / REST API integration**, **MIF JMS queue troubleshooting**, and **zero-downtime database configuration (`configdb`)**.

### IBM Maximo Multi-Tier Architecture & MBO Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                 IBM Maximo EAM Architecture                 │
│                                                             │
│  Presentation & Integration Layer                           │
│  ├── Maximo Web UI & Mobile Work Execution (Maximo Mobile)  │
│  ├── Maximo Integration Framework (MIF - REST/OSLC/JMS)     │
│  └── Object Structures (MXWO, MXASSET, MXPERSON)            │
│                                                             │
│  Business Logic & MBO Layer                                 │
│  ├── Maximo Business Objects (`Mbo`, `MboSet`, `MboValue`)  │
│  ├── Jython / JavaScript Automation Scripting Engine        │
│  └── Escalation & Cron Task Manager (Thread Pool Scheduler) │
│                                                             │
│  Data & Schema Layer                                        │
│  ├── Enterprise RDBMS (Oracle Database, IBM Db2, MS SQL)    │
│  └── Live Database Configuration (`configdb.bat` / `updatedb`)│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Jython Automation Script Development**: Author robust, transactional Jython scripts implementing Attribute (`Validate`, `Init`), Object (`Save`, `Action`), and Integration Launch Points using the `mbo` and `mboSet` APIs.
2. **REST / OSLC API Integration**: Construct authenticated HTTP REST / NextGen OSLC API payloads (`/maxrest/oslc/os/mxwo`, `/maximo/oslc/os/mxasset`) with lean JSON projection queries (`oslc.select`, `oslc.where`).
3. **MIF & Queue Bottleneck Remediation**: Diagnose stalled JMS sequential/continuous queues (`sqin`, `sqout`, `cqin`), error queue reprocessing (`mifevents`), and WebSphere message engine locks.
4. **Database Configuration & Schema Deployment**: Script `configdb.bat` and `updatedb.bat` routines safely, analyzing table spaces, foreign key constraint violations, and index fragmentation.

---

## Production Jython Automation: Work Order Status & Safety Plan Validator

Save this script as an **Object Launch Point** on the `WORKORDER` object before Save:

```python
# ------------------------------------------------------------------------------
# Maximo Automation Script (Jython): Work Order Safety Plan & GL Account Enforcer
# Launch Point: Object Launch Point (WORKORDER) -> Event: Save -> Before Save
# ------------------------------------------------------------------------------
from psdi.server import MXServer
from psdi.mbo import MboConstants

# Only validate when moving to Approved (APPR) status
current_status = mbo.getString("STATUS")
is_status_changed = mbo.isModified("STATUS")

if is_status_changed and current_status == "APPR":
    asset_num = mbo.getString("ASSETNUM")
    site_id = mbo.getString("SITEID")

    if asset_num:
        # 1. Fetch Related Asset MBO
        asset_set = mbo.getMboSet("ASSET")
        asset_mbo = asset_set.getMbo(0)

        if asset_mbo:
            is_critical = asset_mbo.getBoolean("ISCRITICAL")
            has_safety_plan = not mbo.isNull("SAFETYPLANID")

            # Enforce Safety Plan on Critical Assets
            if is_critical and not has_safety_plan:
                # Throw User-Friendly Maximo Error
                params = [asset_num, mbo.getString("WONUM")]
                # Group: workorder, Key: safetyplan_required
                service.error("workorder", "safetyplan_required", params)

    # 2. Auto-Populate Default GL Account if Empty
    if mbo.isNull("GLACCOUNT"):
        location_set = mbo.getMboSet("LOCATION")
        location_mbo = location_set.getMbo(0)
        if location_mbo and not location_mbo.isNull("GLACCOUNT"):
            default_gl = location_mbo.getString("GLACCOUNT")
            mbo.setValue("GLACCOUNT", default_gl, MboConstants.NOACCESSCHECK)
            service.log("Auto-populated GL Account from Location: " + default_gl)
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Escalation Cron Task Fails to Fire After Restart** | Cron task thread pool locked in JVM or instance marked inactive in `CRONTASKINSTANCE` table. | 1. Navigate to *System Configuration $\rightarrow$ Cron Task Setup $\rightarrow$ ESCALATION*.<br>2. Verify `Active` checkbox is checked and schedule is valid (e.g., `10m`).<br>3. In Action Menu, select **Reload Request**.<br>4. Check `crontask.log` for thread timeout deadlocks. |
| **Jython Script Error: `MboException: Cannot find attribute XYZ`** | Custom field was added in Database Configuration without applying structural database changes. | 1. Verify attribute name is uppercase in Jython: `mbo.getString("CUSTOM_ATTR")`.<br>2. Run *Database Configuration $\rightarrow$ Apply Configuration Changes* (`configdb.bat`). |
| **MIF Messages Stuck in Inbound Sequential Queue (`SQIN`)** | A single malformed XML/JSON payload failed validation, blocking all subsequent sequential queue records. | 1. Navigate to *Integration $\rightarrow$ Message Reprocessing*.<br>2. Search for the error record with status `HOLD` or `ERROR`.<br>3. Inspect the error trace, correct the payload data, and click **Process**. |
| **`configdb.bat` Fails with Table Lock Error** | Active user sessions or background cron task threads held open transactions against target tables. | 1. Put Maximo into **Admin Mode** (*System Configuration $\rightarrow$ Admin Mode ON*).<br>2. Terminate all client connections.<br>3. Execute `configdb.bat` from `C:\IBM\SMP\maximo\tools\maximo\`. |

---

## Command Line Syntax & Server Administration

```bash
# 1. Apply Schema Changes Offline (Maximo Tools Directory)
cd C:\IBM\SMP\maximo\tools\maximo
configdb.bat

# 2. Rebuild and Deploy Maximo Enterprise Application Archive (EAR)
buildmaximoear.bat

# 3. Query Active Work Orders via OSLC REST API (cURL)
curl -X GET "https://maximo.enterprise.io/maximo/oslc/os/mxwo?oslc.select=wonum,description,status,assetnum&oslc.where=status=\"APPR\"" \
     -H "apikey: your-maximo-api-key" \
     -H "Content-Type: application/json"
```

### Essential File Locations
- **Master Properties**: `C:\IBM\SMP\maximo\applications\maximo\properties\maximo.properties`
- **Logging Config**: `C:\IBM\SMP\maximo\tools\maximo\log4j2.xml`
- **WebSphere Profile**: `C:\IBM\WebSphere\AppServer\profiles\ctgAppSrv01\`

---

## Agent Operational Directive
> **MANDATORY**: Before running structural database updates via `configdb.bat`, always place Maximo into Admin Mode (`AdminMode ON`). In Jython scripts, use `MboConstants.NOACCESSCHECK` only when setting system-derived fields to prevent privilege escalation.
