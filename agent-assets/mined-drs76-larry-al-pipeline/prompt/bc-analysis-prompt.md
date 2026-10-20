---
name: BC Extension Analysis
description: Analyse a Microsoft Business Central AL extension codebase and produce a technical Wiki and Performance Improvements report for a customer engagement.
author: BC Practice
version: 1.1
---

# BC Extension Analysis Skill

## Purpose

Analyse a Microsoft Business Central AL extension codebase. The customer's AL source files sit in a subfolder (e.g. `CustomerName_vX.X.X.X/`). Produce two documents inside that subfolder: `WIKI.md` and `PERFORMANCE_IMPROVEMENTS.md`.

A third document (e.g. `DUPLICATE_INVOICE_FIX.md`) is only needed if you are writing a specific fix — do not produce it by default.

**Every analysis must include the Universal Code Initiative (UCI) compliance check** — see the dedicated check in `PERFORMANCE_IMPROVEMENTS.md — Checks To Run` below. This is not optional and applies regardless of whether the extension is OnPrem or SaaS.

---

## Read Strategy — Token Efficiency

**Do not read every file. Work in passes.**

### Pass 1 — Orientation (always do this first)

Read only:
- `app.json` — publisher, version, object ID range, dependencies, **`target` field (Cloud/OnPrem — feeds UCI check)**
- Any `*Install*.Codeunit.al` or `*Setup*.Codeunit.al` — install-time configuration

Then list all AL files:
```
Glob: **/*.al
```
Mentally group the file list into: Codeunits | Tables | TableExts | Pages | PageExts | Reports | XMLPorts | Enums

If `target` is **not** `"Cloud"` (i.e. `"OnPrem"`, or the field is absent/older app.json), also run the UCI red-flag grep (last row of the Grep Before Reading table) once, across the whole extension, right now — it's one cheap call and the result feeds Check 8 later. Don't re-run it per-file.

If `target` **is** `"Cloud"`, skip that grep entirely — see Check 8, it's not needed.

### Pass 2 — Codeunits (highest value)

Read all codeunits — they contain ~80% of the logic. Skip XMLPorts on this pass.

### Pass 3 — Tables and TableExts (field inventory)

Read Table files for custom entities. For TableExts, grep rather than full-read:
```
Grep: field\([0-9]+;
```
This finds all custom fields across all TableExts in one pass.

### Pass 4 — Pages (only if needed)

Read Page/PageExt files only if:
- Documenting a specific UI workflow for the Wiki
- Investigating an action or promoted button for a fix doc

Skip Report and XMLPort files unless referenced in a performance issue.

### Grep Before Reading

Before reading a full file, try grep first:

| Question | Grep pattern |
|---|---|
| Where are HTTP/CRM calls made? | `HttpClient\|RegisterConnection\|CRMInvoice.Get\|Dataverse` |
| Where are event subscribers? | `\[EventSubscriber\]` |
| Where are long loops with no commit? | `FindSet` |
| Where is SetAutoCalcFields used? | `SetAutoCalcFields` |
| Where are TryFunctions? | `\[TryFunction\]` |
| What SetCurrentKey calls exist? | `SetCurrentKey` |
| Where are job queue codeunits? | `trigger OnRun` |
| Where is OnPrem-only code (UCI check)? | `\bDotNet\b\|SqlConnection\|System\.Net\|System\.Data\|ServerFilePath\|ServerTempFileName\|IsLocalFileSystemAccessible\|GetServerDirectory\|GetDirectoryFiles\|FileManagement\.(CopyClientFile\|ClientFileExists)\|FILE\.(EXISTS\|ERASE\|COPY\|RENAME)` |

**Note on `\|` above**: that's markdown-table escaping so pipes render instead of breaking the column. When you actually run any pattern from this table, use a plain `|` for alternation — a literal `\|` in most regex engines matches a pipe *character*, not "or", and silently returns zero hits.

---

## Efficiency Rules

1. **Glob before Read** — always list files before reading any.
2. **Grep before Read** — if looking for a specific pattern, grep first; read only matching files.
3. **Read codeunits top-to-bottom once** — don't re-read to verify a detail.
4. **Skip XMLPorts on first pass** — they are import/export schemas and rarely affect Wiki or performance analysis.
5. **Skip Report files unless** they appear in a performance finding or are called from a job queue.
6. **Do not read Page files for the Object Inventory** — derive the name from the filename; read only if the page has non-trivial logic.
7. **Write documents in one pass** — draft each section from your notes and move on.

---

## WIKI.md — Required Sections

Always include all nine sections. Expand or contract depth based on complexity.

```
1. Overview
   - Customer name, business purpose, BC version, object ID range

2. Architecture Summary
   - ASCII diagram of major components and data flow

3. [Functional Area 1] — e.g. Direct Debit, CRM Integration
   - Purpose
   - Core Tables (ID | Name | Description)
   - Codeunits (key procedures, event subscribers)
   - Pages (if UI is non-trivial)

4. [Functional Area 2] ...

5. End-to-End Business Process Flows
   - Numbered step flow for each major process
   - Use ASCII art, not Mermaid diagrams

6. Job Queue Entries
   - Table: Job | Codeunit | Recommended Frequency | Description

7. Configuration & Setup
   - Key setup tables and fields

8. Web API / OData Pages (if any)

9. Object Inventory
   - Tables | Codeunits | Reports | Pages | XMLPorts | Enums (ID | Name | Purpose)
```

**Write the Object Inventory last** — it is mechanical and can be drafted from the Glob file list without re-reading files.

---

## PERFORMANCE_IMPROVEMENTS.md — Checks To Run

Work through these in order. Each check has a grep to run first.

### 1 & 2. N+1 Calls and Missing Commits in Loops — share one grep pass

Grep `FindSet` **once**. For each matching codeunit, inspect the same loop body for both of these together (don't grep twice):
- Check 1 — `Get(` or `Find` inside the loop body → N+1 database call per record. Also grep `CRM.*\.Get\(` separately — each hit is a live Dataverse HTTP call per record.
- Check 2 — whether `Commit()` appears inside or after the loop → long transaction risk if posting invoices, modifying mandates, or inserting journal lines with none.

**Red flags**: any `.Get(` or `FindFirst` inside a `repeat...until` block (Check 1); a posting/insert loop with no `Commit()` between records (Check 2).

### 3. SetAutoCalcFields Inside FindSet Loop

Grep `SetAutoCalcFields`. Check whether it is called before a `FindSet` loop.

**Red flag**: FlowField backed by a CRM or Integration table — each row triggers a coupling lookup.

### 4. Missing Indexes

Look for `SetRange` / `SetFilter` on fields not part of any key. Common culprits:
- `"Order No."` on Sales Invoice Header/Line
- `"Your Reference"` on Sales Invoice Header
- Custom Code fields used for filtering but not declared as keys

**Fix**: Add keys to the TableExt for the standard table.

### 5. SetCurrentKey Mismatch

Grep `SetCurrentKey`. Verify the key matches the filter fields that follow.

**Red flag**: `SetCurrentKey("Field A", "Field B")` followed by `SetFilter("Field C", ...)` — the index is unused.

### 6. HTTP Timeout Configuration

Grep `HttpClient`. Note whether `HttpClient.Timeout` is explicitly set.
For standard CRM integration, note that timeouts are a BC server config setting, not AL code.

### 7. Job Queue Reliability

Check job queue codeunits (`trigger OnRun`) for:
- Whether `Commit()` saves progress incrementally (watermark pattern)
- Whether retry is possible without reprocessing all records
- Whether one failing record halts the entire batch

### 8. Universal Code Initiative (UCI) Compliance — Always Run

Microsoft's Universal Code Initiative requires all BC customisations to be delivered as extensions, `Target = Cloud`, with no Base Application modifications and no OnPrem-only constructs. Non-compliance triggers additional annual licensing charges **per Full User** (Essential or Premium), applied estate-wide — one non-compliant extension surcharges every Full User on the tenant, not just users of that extension:

| Module | Trigger | Cost / Full User / Year |
|---|---|---|
| "Implemented code is not in extensions" | Base Application modifications | $125 |
| "Implemented code is not cloud-optimized" | OnPrem-only extension code | $75 |
| Both apply | Base mods **and** OnPrem-only code | $200 |

Uses results already captured earlier — **no new file reads or greps needed** if Pass 1 was followed:

1. **Target** — reuse the `"target"` field noted from `app.json` in Pass 1.
2. **If `target: "Cloud"`** — the compiler already rejects DotNet/SQL/server-file-system APIs at build time for a Cloud-targeted extension, so the "not cloud-optimized" ($75) trigger cannot fire. **Skip construct-level checking entirely** — no grep, no per-hit classification. Go straight to the Base Application modifications check (next step) and write up the result.
3. **If `target` is `"OnPrem"` or absent** — this is where non-compliance actually lives. Classify the hits from the Pass 1 UCI grep:
   - `DotNet`-typed variable → live .NET Interop violation
   - `SqlConnection` / `System.Net` / `System.Data` → live direct SQL/network violation
   - `ServerFilePath` / `ServerTempFileName` / `IsLocalFileSystemAccessible` / `GetServerDirectory` / `GetDirectoryFiles` / `FileManagement.CopyClientFile` / `FileManagement.ClientFileExists` / `FILE.(EXISTS|ERASE|COPY|RENAME)` → live server file-system violation
   - **Do not flag `using System.IO;` on its own** — that's AL's own Cloud-safe platform namespace (Stream/InStream/OutStream/File helper types), not .NET's file system API.
   - **Check whether each hit is live or commented out.** Commented-out legacy code is a hygiene note, not a compliance violation — but call it out as a risk it could be uncommented later.
4. **Base Application modifications** — regardless of target, confirm from the Pass 1 file listing that everything is packaged as a proper extension (app.json + AL objects), not classic C/AL modifications merged into base objects. Target=Cloud does **not** guarantee this — it's a separate ($125) trigger.
5. **Estimate exposure** — if any live violation is found, state which module(s) apply ($75 / $125 / $200) and show the per-Full-User annual cost formula (`Full Users × rate`). If the client's Full User count is unknown, state the rate per-user and flag that the actual user count needs confirming — do not guess a headcount.

**Red flag**: `target: "OnPrem"` (or missing) in app.json with any *live* (non-commented) DotNet/SQL/file-system call, or any Base Application modification regardless of target.

**Clean result**: `target: "Cloud"` with no Base App mods → state explicitly that exposure is $0 (construct-level check was skipped as compiler-enforced, not because it was run and passed).

### Finding Template

Each finding must use this structure:

```
### Issue N — [Short title]
**Location**: Codeunit/Table name and relevant procedure
**Root Cause**: What the code does and why it is a problem
**Impact**: Business/performance consequence
**Recommendations**:
  - Short term (config change, no code)
  - Medium term (code change, with example snippet)
```

End the document with a Priority Summary Table:

```
| # | Issue | Files Affected | Severity | Effort |
```

---

## Patterns To Recognise

Common patterns in KPMG/SLG-style BC extensions. Check for these proactively.

| Pattern | Where to look | Note |
|---|---|---|
| Order-split retry bug | `Process Sales Order` style codeunits | Duplicate invoice risk if no idempotency guard |
| Deferred income | `SLG Deferral` style codeunits | Check for rounding residual in last period |
| CRM update watermark | `CRM Synch Status` or similar | Check whether watermark advances per-batch or only on full success |
| Auto-post journal batches | `Auto Post` flag on Gen. Journal Batch | Check for concurrent run protection (LockTable) |
| Mandate singleton rule | SEPA Direct Debit Mandate | Verify only one non-blocked mandate per bank account is enforced |
| ADDACS/ARUDD loop | File import codeunits | Check for commits between records to reduce deadlock window |

---

## Output Quality Rules

- Use **tables** for object inventories — never bullet lists.
- Use **ASCII diagrams** for architecture and flows — Mermaid is not reliably rendered in all viewers.
- Object IDs must be **accurate** — take them from the actual AL file declarations, not filenames.
- Do **not** document XMLPort field-level detail unless explicitly asked.
- Write the Wiki for a **developer who is new to this customer** — assume BC knowledge, not customer knowledge.
- Write Performance findings for a **consultant** presenting to the customer — include business impact, not just technical detail.
