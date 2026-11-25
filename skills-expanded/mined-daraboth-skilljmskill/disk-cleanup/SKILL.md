---
name: disk-cleanup
description: Reclaim space on the Windows C: drive by clearing regenerable caches (npm, pip, temp, Windows Update, puppeteer, driver leftovers). Use when the system drive is low on space, when an installer needs room to extract, or when the user asks to free up / clean up disk space. Scans and reports first, never deletes without confirmation.
---

# Disk Cleanup

Frees space on the system drive by removing caches that regenerate on their own.
Only known cache folders are targets; your projects and documents are never touched.

## Non-negotiable rules

1. **Always scan before deleting.** Report the table, get an explicit yes, then clean.
2. **Never delete an unrecognised folder.** Anything not on the allowlist is reported
   as `ask` risk and left alone until the user says what owns it.
3. **Protected folders are never touched:** `Temp\claude` and `.cache\claude` hold the
   active session's scratchpad and background task output. Deleting them breaks the
   running session. The script excludes them by name.
4. **No wildcards over user data.** Targets are an explicit allowlist of cache paths.

## Workflow

### 1. Scan

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\skills\disk-cleanup\cleanup.ps1"
```

Prints every target that exists with its size, risk level, and what the consequence
of deleting it is. Nothing is modified.

### 2. Report

Show the user a table: target, size, and the real consequence. Call out anything
with a side effect rather than burying it, for example:

- `puppeteer` — re-downloads Chromium on the next browser-automation run
- `npm-cache` / `pip-cache` — next install is slower once, then normal
- `winupdate` — some files stay locked without admin; those are skipped

Separate `safe` totals from `ask` totals. Give the projected free space after.

### 3. Confirm, then clean

Dry run first if there is any doubt:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\skills\disk-cleanup\cleanup.ps1" -Mode Clean
```

Then, only after the user agrees:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\skills\disk-cleanup\cleanup.ps1" -Mode Clean -Execute
```

Reports free space before, after, and the delta.

### 4. Verify

Confirm the reclaimed figure matches roughly what was projected. If it falls well
short, locked files were skipped, usually the Windows Update cache without admin.
Say so rather than reporting the projection as though it happened.

## Options

| Flag | Effect |
|---|---|
| `-Mode Scan` | Measure only (default) |
| `-Mode Clean` | Delete, but only together with `-Execute` |
| `-Execute` | Required to actually delete anything |
| `-Only a,b` | Restrict to specific target ids |
| `-Skip a,b` | Exclude specific target ids |
| `-IncludeAsk` | Also clean `ask`-risk targets. Only after the user confirms each one. |

> **Array parameters need `-Command`, not `-File`.** With `powershell -File`, a
> comma list arrives as a single string and `-Only` / `-Skip` silently match nothing
> (the run reports 0.00 GB and does nothing). Invoke them like this instead:
>
> ```powershell
> powershell -ExecutionPolicy Bypass -Command "& '$env:USERPROFILE\.claude\skills\disk-cleanup\cleanup.ps1' -Mode Clean -Execute -Only @('npm-cache','user-temp')"
> ```

## Targets

**Safe** (regenerable, no decision needed):
`npm-cache`, `pip-cache`, `winupdate`, `windows-temp`, `user-temp`, `puppeteer`,
`nvidia-extract`, `nvidia-extract2`, `nvidia-ota`, `recycle-bin`

`nvidia-ota` is the usual culprit when C: fills up suddenly. The NVIDIA App
pre-downloads each new driver into
`C:\ProgramData\NVIDIA Corporation\NVIDIA App\UpdateFramework\ota-artifacts`,
which can grow by several GB and fill the drive to 0 bytes free.
Check it first on any "disk is full" report.

**Ask** (needs a human decision, never cleaned by default):
`windows-old`, plus any unrecognised child of `~\.cache` discovered at scan time.

## Notes

- Run without admin. Locked files are skipped rather than failing the run.
- `nvidia-extract` (`C:\NVIDIA`) is driver-installer leftovers, safe to remove once
  the driver install has finished.
- If C: is low specifically because an installer needs extraction room, clean first,
  then confirm free space before telling the user to run the installer.
