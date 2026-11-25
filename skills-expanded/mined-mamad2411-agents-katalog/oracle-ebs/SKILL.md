---
name: oracle-ebs
description: "Automate Oracle EBS workflows with Concurrent Programs, PL/SQL, Oracle Forms, and FNDLOAD configuration migrations."
category: erp
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["oracle-ebs", "oracle-forms", "concurrent-manager", "plsql-apps", "fndload", "r12-ebs", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Oracle E-Business Suite (EBS) AI Skill Guide (Claude)

## Overview & Engine Architecture
Oracle E-Business Suite (EBS R12.1 / R12.2) is a comprehensive global ERP suite covering Financials (GL/AP/AR), Supply Chain (OM/INV/PO), Human Capital Management (HCM), and Manufacturing. EBS operates on a **Three-Tier Architecture**: Desktop Client Tier (Oracle Forms via Java Web Start JNLP / Browser), Application Tier (Oracle WebLogic Server, Forms & Reports Services, Concurrent Processing Subsystem), and Database Tier (Oracle Database 19c running the unified **`APPS`** schema). Claude operates as a Principal Oracle Applications DBA and Techno-Functional Architect, specializing in **Concurrent Processing optimization**, **PL/SQL APPS API automation**, **FNDLOAD configuration migrations**, and **Forms JNLP troubleshooting**.

### Oracle EBS Multi-Tier Architecture & Concurrent Processing Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Oracle EBS R12.2 Architecture               │
│                                                             │
│  Client & Presentation Tier                                 │
│  ├── Oracle Forms Thick Client (Java Web Start / JNLP)      │
│  ├── Oracle Application Framework (OAF HTML Pages)          │
│  └── REST / SOAP Integrated SOA Gateway (ISG)               │
│                                                             │
│  Application Tier & Processing Engine                       │
│  ├── Oracle WebLogic Server (oafm, forms, oacore Managed Srv│
│  ├── Internal Concurrent Manager (ICM) & Worker Farms (FNDLIBR)│
│  └── Oracle Workflow Engine & Business Event System (BES)   │
│                                                             │
│  Database Tier & APPS Schema                                │
│  ├── Oracle 19c Enterprise Database (EBR Editioning Views)  │
│  └── Shared Master Repository (`APPLSYS`, `APPS`, `GL`, `PO`)│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **PL/SQL APPS API Automation**: Author transactional PL/SQL packages interacting with standard public APIs (`FND_REQUEST.SUBMIT_REQUEST`, `GL_JOURNAL_IMPORT_PKG`, `PO_DOCUMENT_CONTROL_PUB`) with proper application session initialization (`FND_GLOBAL.APPS_INITIALIZE`).
2. **Concurrent Manager Administration**: Diagnose request queue bottlenecks, configure Manager Specialization rules, adjust worker process counts, and resolve incompatible request conflicts.
3. **FNDLOAD Configuration Data Migration**: Author scripts to migrate Concurrent Programs, Request Groups, Value Sets, and Descriptive Flexfields (DFF) across DEV/TEST/PROD instances using `.lct` control files and `.ldt` data files.
4. **Oracle Forms & JNLP Remediation**: Troubleshoot `FRM-92095` Java runtime errors, expired JAR code-signing certificates, and WebLogic managed server thread deadlocks.

---

## Production PL/SQL Automation: Programmatic Concurrent Request Submission & Polling

Save this package script as `submit_concurrent_job.sql` to programmatically initialize an EBS session, submit a batch job, and poll execution status:

```sql
-- =============================================================================
-- Oracle EBS PL/SQL Automation: Programmatic Concurrent Job Dispatcher
-- Initializes APPS context, submits Concurrent Request, and polls completion.
-- =============================================================================
DECLARE
    l_user_id      NUMBER;
    l_resp_id      NUMBER;
    l_resp_appl_id NUMBER;
    l_request_id   NUMBER;
    l_phase        VARCHAR2(80);
    l_status       VARCHAR2(80);
    l_dev_phase    VARCHAR2(30);
    l_dev_status   VARCHAR2(30);
    l_message      VARCHAR2(240);
    l_call_status  BOOLEAN;
BEGIN
    -- 1. Fetch System Administrator User & Responsibility IDs
    SELECT user_id INTO l_user_id FROM fnd_user WHERE user_name = 'OPERATIONS_USER';
    SELECT responsibility_id, application_id INTO l_resp_id, l_resp_appl_id 
    FROM fnd_responsibility_vl WHERE responsibility_name = 'General Ledger Super User';

    -- 2. Initialize Oracle EBS Session Context
    fnd_global.apps_initialize(
        user_id      => l_user_id,
        resp_id      => l_resp_id,
        resp_appl_id => l_resp_appl_id
    );
    dbms_output.put_line('Initialized EBS Session Context for User ID: ' || l_user_id);

    -- 3. Submit Concurrent Request (e.g. Program: GLLEZL / General Ledger Import)
    l_request_id := fnd_request.submit_request(
        application => 'SQLGL',
        program     => 'GLLEZL',
        description => 'Automated Nightly Journal Import',
        start_time  => NULL,
        sub_request => FALSE,
        argument1   => '101',    -- Source ID
        argument2   => 'BATCH_001' -- Group ID
    );

    IF l_request_id = 0 THEN
        dbms_output.put_line('ERROR: Failed to submit Concurrent Request: ' || fnd_message.get);
        RETURN;
    END IF;

    COMMIT;
    dbms_output.put_line('Successfully submitted Concurrent Request ID: ' || l_request_id);

    -- 4. Poll Request Execution Status
    LOOP
        dbms_lock.sleep(5); -- Wait 5 seconds between polls
        
        l_call_status := fnd_concurrent.get_request_status(
            request_id => l_request_id,
            phase      => l_phase,
            status     => l_status,
            dev_phase  => l_dev_phase,
            dev_status => l_dev_status,
            message    => l_message
        );

        dbms_output.put_line('Status: ' || l_phase || ' / ' || l_status);
        EXIT WHEN l_dev_phase = 'COMPLETE';
    END LOOP;

    IF l_dev_status = 'NORMAL' THEN
        dbms_output.put_line('✅ SUCCESS: Request completed normally.');
    ELSE
        dbms_output.put_line('🚨 FAILED: Request finished with status: ' || l_dev_status);
    END IF;
END;
/
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Oracle Forms Fails: `FRM-92095: Oracle JInitiator version too low`** | Client browser attempting to invoke deprecated NPAPI plugin rather than Java Web Start (JNLP). | 1. In `$INST_TOP/ora/10.1.2/forms/server/formsweb.cfg`, set `forms_launch_method=jnlp`.<br>2. Associate `.jnlp` files with local Java Runtime (`javaws.exe`). |
| **Concurrent Request Stuck in `Pending - Standby`** | Request has incompatible conflicting programs currently running, or target manager queue is full. | 1. In System Administrator $\rightarrow$ *Concurrent $\rightarrow$ Requests*, click **View Details** $\rightarrow$ **Diagnostics**.<br>2. Check for program conflict domain rules.<br>3. Verify Standard Manager worker count in *Administer Managers*. |
| **FNDLOAD Upload Fails: `ORA-00001: Unique Constraint Violated`** | Target `.ldt` file contains entity keys that conflict with existing definitions with different unique IDs. | 1. In `FNDLOAD` command, add `UPLOAD_MODE=REPLACE` or `CUSTOM_MODE=FORCE`.<br>2. Verify entity version compatibility in the `.lct` control file. |
| **OACore / WebLogic Managed Server Out of Memory** | Leak in custom OAF Controller extensions keeping large ViewObjects in memory. | 1. In `$EBS_DOMAIN_HOME/bin/setDomainEnv.sh`, increase `-Xmx4096m -XX:MaxMetaspaceSize=1024m`.<br>2. Run `adautocfg.sh` to persist changes. |

---

## Command Line Syntax & Admin Recipes

```bash
# 1. Export Concurrent Program Definition via FNDLOAD
FNDLOAD apps/apps_pwd 0 Y DOWNLOAD $FND_TOP/patch/115/import/afcpprog.lct custom_program.ldt PROGRAM APPLICATION_SHORT_NAME="SQLGL" CONCURRENT_PROGRAM_NAME="GLLEZL"

# 2. Check Status of All Concurrent Managers
adcmctl.sh status apps/apps_pwd

# 3. Execute AutoConfig Engine to Re-generate Application Configurations
adautocfg.sh
```

### Essential File & Environment Locations
- **Application Top**: `$APPL_TOP` (e.g. `/u01/install/APPS/fs1/EBSapps/appl`)
- **Instance Top**: `$INST_TOP` (e.g. `/u01/install/APPS/fs1/FMW_Home`)
- **Context File**: `$APPL_TOP/admin/$CONTEXT_NAME.xml`

---

## Agent Operational Directive
> **MANDATORY**: In custom PL/SQL scripts executing EBS logic, always invoke `fnd_global.apps_initialize` before calling public APIs. Use `adautocfg.sh` to apply configuration updates across Oracle WebLogic and Apache tiers.
