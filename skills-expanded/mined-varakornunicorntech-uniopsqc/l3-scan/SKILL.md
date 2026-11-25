---
name: l3-scan
description: Initiate an L3 Full Code Scan following the §7 Pre-Existing Codebase Standards. Requires Commander authorization. Provide project name (e.g., /l3-scan BOS.Kit).
---

# L3 Full Code Scan

Initiate and execute an L3 Full Code Scan following `.claude/policies/05_PreExisting_Codebase.md`.

## Pre-Check

**HALT if Commander has not explicitly authorized this L3 scan.** L3 requires Commander authorization regardless of codebase size.

## Steps

1. **Parse arguments:** `$1` = Project name (e.g., BOS.Kit)
2. **Read `.claude/ProjectEnvironment.md`** to locate the project's source code path and Development folder.
3. **Verify L1 and L2 exist** in `Development/$1/PreExisting TechStack/$1.md`. If not, run L1 → L2 first.
4. **Execute L3 — Full Code Scan:**
   - Read all source files in depth across the entire codebase
   - Complete all subsystem sections to full depth in the PreExisting TechStack file
5. **Execute §7b — All 5 Mandatory Verification Checks (in order):**

   **Check 1 — File Manifest:**
   - Run raw file listing per subsystem directory
   - Compare Files Found vs Files Documented
   - Any gap = mandatory re-scan

   **Check 2 — Service-URL Tracing:**
   - Trace every frontend service file to its backend handler
   - Document in Frontend → Backend Service Map

   **Check 3 — Conductor Independence Cross-Check:**
   - Independently verify file counts per subsystem (NOT delegated to scan subagent)
   - Compare against scan output

   **Check 4 — Cross-Layer Subsystem Tracing:**
   - Extract subsystem registry from ALL layers (DB, App, Frontend, Infra)
   - Build Cross-Layer Matrix
   - Flag every gap

   **Check 5 — External Dependency & Hidden Service Audit (6 sub-audits):**
   - 5a: External Service & Integration Audit
   - 5b: Background Worker & Hosted Service Audit
   - 5c: Middleware & Pipeline Component Audit
   - 5d: Dependency Manifest Audit
   - 5e: Inter-Service Communication Audit
   - 5f: Environment Configuration Audit

6. **All 5 checks must PASS** before presenting output to Commander.
7. **Update** the PreExisting TechStack file with all findings and verification tables.

## Arguments

- `$1` — Project name (required, must match a project in ProjectEnvironment.md)

## Example

```
/l3-scan Unicorn.BOS-A-PROJECT
```
