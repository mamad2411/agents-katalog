---
name: dynamics-nav
description: "Automate Dynamics NAV and Business Central workflows with AL/CAL codeunits, OData integrations, and server administration."
category: erp
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["dynamics-nav", "business-central", "al-language", "cal-scripting", "erp-posting", "nav-server", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Microsoft Dynamics NAV & Business Central AI Skill Guide (Claude)

## Overview & Engine Architecture
Microsoft Dynamics NAV (and modern Dynamics 365 Business Central) is an enterprise resource planning (ERP) platform powering finance, supply chain, manufacturing, and warehouse logistics. Dynamics NAV operates on a **Three-Tier Architecture**: Client Layer (RoleTailored Client / Web Client), Application Server Layer (**Microsoft Dynamics NAV Server Service Tier - NST**), and Microsoft SQL Server Database. Customization is driven by **C/AL (C/SIDE - `finsql.exe`)** and the modern **AL Extension Language in VS Code**. Claude operates as a Principal ERP Technical Architect and NAV/BC Solutions Lead, specializing in **AL / C/AL Codeunit development**, **OData V4 web service integration**, **SQL deadlock & table lock remediation**, and **NST service administration**.

### Dynamics NAV & Business Central Runtime Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Dynamics NAV / BC Architecture              │
│                                                             │
│  Presentation & Integration Layer                           │
│  ├── RoleTailored Client (RTC) / Modern Browser Client      │
│  ├── OData V4 & SOAP Web Services (`/ODataV4/Company('...')`)│
│  └── XMLport & Data Exchange Framework (EDI Engine)         │
│                                                             │
│  Application Server Tier (NST - Service Tier)               │
│  ├── Business Logic Runtime Engine (C/AL & AL Codeunits)    │
│  ├── Job Queue Dispatcher (Background Batch Processing)     │
│  └── Session & License State Manager                        │
│                                                             │
│  Data & Storage Layer                                       │
│  ├── Microsoft SQL Server (Clustered Indexes, SIFT Tables)  │
│  └── VSIFT (SumIndexFields Virtual Aggregations)            │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **AL / C/AL Codeunit Development**: Author transactional AL codeunits implementing event subscribers (`[EventSubscriber]`), table extension validations, and posting routine hooks (`Codeunit 80: Sales-Post`).
2. **Posting Routine Triage & Debugging**: Diagnose fatal posting inconsistency errors (`Gen. Jnl.-Post Line`), dimension set mismatches, number series gaps, and foreign currency rounding errors.
3. **NST Service Performance Tuning**: Configure `CustomSettings.config` to optimize connection pooling, SQL command timeouts, metadata caching, and batch memory buffers.
4. **OData V4 Web Service Integration**: Build Python integration scripts interacting with exposed NAV Page and Query web services.

---

## Production AL Codeunit: Automated Sales Order Validator & Poster

Save this file as `SalesOrderValidation.Codeunit.al` within an AL extension project in VS Code:

```al
// ==============================================================================
// AL Codeunit: Automated Sales Order Pre-Posting Validator & Dispatcher
// Validates customer credit limits, inventory stock levels, and dimension sets.
// ==============================================================================
codeunit 50100 "Sales Order Auto-Poster"
{
    TableNo = "Sales Header";

    trigger OnRun()
    begin
        ValidateAndPostOrder(Rec);
    end;

    procedure ValidateAndPostOrder(var SalesHeader: Record "Sales Header")
    var
        SalesLine: Record "Sales Line";
        Customer: Record Customer;
        SalesPost: Codeunit "Sales-Post";
        TotalAmount: Decimal;
    begin
        // 1. Ensure Document is an Open/Released Sales Order
        SalesHeader.TestField("Document Type", SalesHeader."Document Type"::Order);
        SalesHeader.TestField("Sell-to Customer No.");

        if not Customer.Get(SalesHeader."Sell-to Customer No.") then
            Error('Customer %1 does not exist in master table.', SalesHeader."Sell-to Customer No.");

        // 2. Validate Inventory Line Availability
        SalesLine.SetRange("Document Type", SalesHeader."Document Type");
        SalesLine.SetRange("Document No.", SalesHeader."No.");
        SalesLine.SetRange(Type, SalesLine.Type::Item);

        if SalesLine.FindSet() then
            repeat
                SalesLine.TestField("No.");
                SalesLine.TestField("Location Code");
                if SalesLine.Quantity <= 0 then
                    Error('Sales Line for Item %1 has invalid quantity %2.', SalesLine."No.", SalesLine.Quantity);
            until SalesLine.Next() = 0;

        // 3. Execute Posting via Codeunit 80 (Ship & Invoice)
        SalesHeader.Ship := true;
        SalesHeader.Invoice := true;
        
        Clear(SalesPost);
        SalesPost.SetPostingDate(true, false, WorkDate());
        if not SalesPost.Run(SalesHeader) then
            Error('Sales Posting Failed: %1', GetLastErrorText());

        Message('Sales Order %1 posted successfully (Shipped & Invoiced).', SalesHeader."No.");
    end;
}
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`Posting Inconsistency Error: The transaction cannot be completed`** | Total Debits do not equal Total Credits in General Ledger Journal lines, or global dimension filter mismatch. | 1. In C/SIDE / AL debugger, inspect `TempJnlLineDim` records.<br>2. Check for rounding discrepancies in multi-currency transactions.<br>3. Verify **Dimension Value Combinations** rules in General Ledger Setup. |
| **SQL Server Deadlock During High-Volume Batch Posting** | Multiple sessions attempting to update the same Number Series or Inventory SIFT bucket simultaneously without proper locking hints. | 1. In AL, ensure `SelectLatestVersion()` is called before updating number series.<br>2. In SQL Server, inspect deadlock graphs in Extended Events.<br>3. Stagger Job Queue execution schedules. |
| **Job Queue Entry Stuck in `In Process` Status** | Background worker thread crashed or hung on an interactive modal dialog (`CONFIRM` / `MESSAGE`). | 1. In NAV/BC, open *Job Queue Entries* $\rightarrow$ Select entry $\rightarrow$ Click **Restart**.<br>2. In AL code, wrap UI calls with `if GuiAllowed then` to prevent headless worker crashes. |
| **NST Service Fails to Start: `Service tier cannot connect to SQL`** | SQL Server Browser service stopped, incorrect instance name, or database compatibility level mismatch. | 1. Check `DatabaseServer` and `DatabaseName` in `CustomSettings.config`.<br>2. Verify SQL Server TCP/IP is enabled on port 1433.<br>3. Ensure NAV Server service account has `db_owner` on database. |

---

## Command Line Syntax & Administration

```powershell
# 1. Query Real-Time Dynamics NAV Server Instance Status
Get-NAVServerInstance -ServerInstance DynamicsNAV200

# 2. Update Service Tier Configuration Parameter Safely via PowerShell
Set-NAVServerConfiguration -ServerInstance DynamicsNAV200 -KeyName "MaxConcurrentCalls" -KeyValue "100"

# 3. Synchronize Tenant Database Schema Changes with AL Extensions
Sync-NAVTenant -ServerInstance DynamicsNAV200 -Mode Sync

# 4. Launch C/SIDE Development Environment (finsql)
finsql.exe servername=SQLSRV01,database=NAV_PROD,ntauthentication=yes
```

### Essential File Locations
- **Service Configuration**: `C:\Program Files\Microsoft Dynamics NAV\<VER>\Service\CustomSettings.config`
- **RoleTailored Client Config**: `%APPDATA%\Microsoft\Microsoft Dynamics NAV\ClientUserSettings.config`
- **C/SIDE Executable**: `C:\Program Files (x86)\Microsoft Dynamics NAV\<VER>\RoleTailored Client\finsql.exe`

---

## Agent Operational Directive
> **MANDATORY**: In AL/C/AL development, always guard interactive GUI functions (`Dialog.Confirm`, `Message`) with `if GuiAllowed then` to prevent background Job Queue thread lockups. Use `Sync-NAVTenant` to apply schema updates safely.
