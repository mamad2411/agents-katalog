---
name: office-com-cleanup
description: Use when Office COM automation leaks WINWORD.EXE/EXCEL.EXE processes, files stay locked after a script, scripts hang on hidden dialogs, or you need the correct release/quit pattern for Word.Application and Excel.Application COM objects in PowerShell
---

# Office COM Cleanup and Lifecycle

## Overview

COM objects created from PowerShell are not freed by normal scope exit. If you
do not explicitly quit the application and release every reference, the hidden
`WINWORD.EXE` / `EXCEL.EXE` process survives, keeps the file locked, and
accumulates with every run.

**Core principle:** Every COM reference you create must be released with
`Marshal.ReleaseComObject`, the app must be told to `Quit()`, and you must force
a GC — all inside a `finally` block so it runs even when work throws.

## The Lifecycle Rule

```dot
digraph lifecycle {
    rankdir=LR;
    create [label="New-Object\n-ComObject", shape=box];
    config [label="Visible=$false\nDisplayAlerts off", shape=box];
    work   [label="do work\n(may throw)", shape=box];
    finally [label="finally:", shape=box, style=filled, fillcolor="#ffe0b0"];
    quit   [label="app.Quit()", shape=box];
    release [label="ReleaseComObject\n(every ref)", shape=box];
    gc     [label="GC.Collect +\nWaitForPendingFinalizers", shape=box];

    create -> config -> work -> finally;
    finally -> quit -> release -> gc;
}
```

## Canonical Pattern

```powershell
$ErrorActionPreference = 'Stop'
$app = $null
$doc = $null
try {
    $app = New-Object -ComObject Word.Application   # or Excel.Application
    $app.Visible = $false
    $app.DisplayAlerts = 0     # Word: 0 (wdAlertsNone). Excel: $false.

    $doc = $app.Documents.Open([System.IO.Path]::GetFullPath($path))
    # ... work ...
    $doc.Save()
}
finally {
    # 1. Close documents/workbooks WITHOUT prompting.
    try { if ($doc) { $doc.Close($false) } } catch { }
    # 2. Quit the application. (Wrap in try/catch: Quit() can throw RPC
    #    errors like 0x800706BA even after a successful Save, especially
    #    under $ErrorActionPreference='Stop'.)
    try { if ($app) { $app.Quit() } } catch { }
    # 3. Release EVERY COM reference you held (children first).
    foreach ($o in @($doc, $app)) {
        if ($o) { try { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($o) } catch { } }
    }
    # 4. Drop the variables and force finalization.
    $doc = $null; $app = $null
    [GC]::Collect(); [GC]::WaitForPendingFinalizers()
}
```

## Why each step matters

| Step | If you skip it |
|------|----------------|
| `Close($false)` | Hidden "Save changes?" dialog → script hangs forever |
| `Quit()` | Application process never exits |
| `ReleaseComObject` | RCW keeps the process alive even after `Quit()` |
| `$null` the vars | Lingering references block GC from finalizing RCWs |
| `GC.Collect` + `WaitForPendingFinalizers` | Process exit is delayed/non-deterministic |

## Release EVERY intermediate reference

A reference is created for **every COM member access**, even ones you don't
store in a variable. Long dotted chains leak the intermediate objects:

```powershell
# ❌ LEAKS: Worksheets, Item(1), Cells, Item(1,1) are all unreleased RCWs
$value = $excel.Workbooks.Open($p).Worksheets.Item(1).Cells.Item(1,1).Value2

# ✅ Capture intermediates so you can release them
$wb = $excel.Workbooks.Open($p)
$ws = $wb.Worksheets.Item(1)
$cell = $ws.Cells.Item(1, 1)
$value = $cell.Value2
# release $cell, $ws, $wb in finally
```

For deeply nested loops where capturing every cell is impractical, rely on the
final `GC.Collect()` + `WaitForPendingFinalizers()` to sweep them — but always
release the top-level handles (`app`, `workbook`/`document`, `worksheet`)
explicitly.

## Don't suppress the visible window with Kill

Do not "fix" leaks with `Stop-Process -Name WINWORD`. That:
- Kills documents the user opened manually.
- Can corrupt files mid-write.
- Hides the real bug (a missing release).

Killing the process is a **last-resort recovery** for orphans from a previous
crashed run, not part of normal teardown.

## Recovering orphaned processes (after a crash)

If a previous run crashed and left orphans, you can clean up ones that have no
visible window. This is still risky if a human has Office open — prefer asking
the user. A targeted approach:

```powershell
# List Office processes so the user can confirm before killing anything.
# Include the WPS process names too — see the WPS note below.
Get-Process -Name WINWORD, EXCEL, wps, et, wpp -ErrorAction SilentlyContinue |
    Select-Object Id, ProcessName, MainWindowTitle, StartTime
```

Only kill specific PIDs you are certain are orphans from your automation.

## WPS Office uses different process names

If `New-Object -ComObject Word.Application` / `Excel.Application` is actually
serviced by **WPS Office** (it registers itself under the Microsoft ProgIDs —
see `office-docs:office-docs-overview`), the hidden process is **not**
`WINWORD.EXE` / `EXCEL.EXE`:

| Microsoft app | MS process | WPS equivalent |
|---------------|-----------|----------------|
| Word          | `WINWORD.EXE` | `wps.exe` |
| Excel         | `EXCEL.EXE`   | `et.exe`  |
| PowerPoint    | `POWERPNT.EXE`| `wpp.exe` |

The `Quit()` + `ReleaseComObject` + `GC` teardown is identical regardless of
which engine answered — but any leak detection or orphan cleanup that greps for
`WINWORD`/`EXCEL` will silently miss WPS leaks. Check for the WPS names too.

## Reusable release helper

Drop this into a script to release a list of objects safely:

```powershell
function Release-Com {
    param([object[]]$Objects)
    foreach ($o in $Objects) {
        if ($o -and [Runtime.InteropServices.Marshal]::IsComObject($o)) {
            try { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($o) } catch { }
        }
    }
    [GC]::Collect(); [GC]::WaitForPendingFinalizers()
}

# usage in finally:
# Release-Com @($cell, $ws, $wb, $excel)
```

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Cleanup outside `finally` | Leaks whenever work throws | Put teardown in `finally` |
| `Quit()` but no release | Process stays alive | `ReleaseComObject` every handle |
| Long dotted chains | Silent intermediate leaks | Capture + release intermediates |
| `Stop-Process` as teardown | Corrupts files, kills user's docs | Use proper release; kill only orphans |
| No `GC.Collect` | Process exits late or never | `GC.Collect()` + `WaitForPendingFinalizers()` |
| Orphan process locks output file | `IOException` on next run, file "in use by another process" | Kill orphans first, or use unique filenames; wrap `Quit()` in `try/catch` |
| `DisplayAlerts` left on | Script hangs on hidden dialog | Disable before work |
| `Close()` / `Quit()` unguarded | RPC error (0x800706BA) kills script when `$ErrorActionPreference='Stop'` | Wrap both in `try/catch` |
| Only checking `WINWORD`/`EXCEL` | WPS leaks go undetected | Also check `wps.exe`/`et.exe`/`wpp.exe` |
