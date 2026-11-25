---
name: pcx
description: Tune this Windows 10 or 11 PC with an AI agent. Use when the user says /pcx, runs pcx doctor, pastes the pcx install link, asks to optimize this PC, says "оптимизируй ПК", "ускорь компьютер", "почисти компьютер", "настрой компьютер", or replies with the numbers you proposed.
---

# pcx skill

pcx is a text-only PowerShell CLI plus this skill. The agent explains, machine
proves, and the user decides.

**One command starts everything, then the work happens in chat.** The user types
one trigger and never types a pcx command afterwards. You scan the whole machine,
show one table of everything you found, ask what to do, and then do it.

## How the run starts

Any of these is the whole trigger: `/pcx`; "optimize this PC", "оптимизируй
ПК", "ускорь компьютер", "запусти сканирование", "почисти компьютер"; or the
repository link with "install". No setup question and no menu.

## Step 1. Install and check (only for a fresh copy)

1. Read `INSTALL.md` in the repository root.
2. Install the pinned folder exactly as `INSTALL.md` describes, including the
   `command/` and `agent/` entries (`command/pcx.md`, and `agent/pcx.md` for
   OpenCode), and put the files where the harness looks for skills. Never copy
   `tests/` nor `tests/.pcx-test-root` into the skill folder (otherwise
   `PCX-E-PLATFORM-TESTROOT`).
3. Run the doctor command from the installed path:

   `pwsh -File <path>/pcx.ps1 doctor`

4. Report the result. If the user only asked to install, **stop** here. If the
   same message also asked to tune, continue with Step 2 in this run.

If `pwsh` is missing, run the same command with `powershell` and say so.

## Step 2. Investigate this machine, then propose

Run the scan yourself, with `--lang ru` for a Russian-speaking user:

```powershell
pwsh -File <path>/pcx.ps1 tune --table
```

If the `/pcx` command already ran the scan and printed `PCX_SCAN_FILE`, read that
file and use `data.table` instead of running it again. Do this in **this**
session with the shell tool. Do not hand the scan, the report, the findings or
the question to a subagent: never use the task tool.

`pcx tune --table` is input, not the answer. `pcx` is the fast path for typed
changes, not a gate. Never hide a finding, a refusal or a failure. Reconcile the
table against this machine.

### Baseline

Ingest `data.environment`, `data.metrics`, `data.diagnostics`, `data.findings`.
Profile the machine first: OS build and days since the last update; CPU/GPU/RAM
and commit; disk types, free space, SMART/wear/temperature; laptop or desktop;
managed/S Mode/Dev Drive; workloads (games, browsers, IDEs, VMs). Read all 13
sections and 45 finding ids; never print the diagnostic sections.

### Exhaustive exploration

Do not stop at pcx defaults and do not cap findings. Use `pcx probe <spec>` (one
target per call, no invented flags) and native read-only tools:
`environment:`, `reg:HKCU\...#Value`, `svc:<name>`, `task:<path>`,
`file:<path>`, `counter:<PDH path>`, `event:<log>[;Provider=;Id=;Hours=]`,
`intent:<u4|userassist|prefetch|taskhistory>`; every result names its source,
for example `platform:registry`.

Cover these domains and measure before you call something a finding:

1. Services and startup: third-party and optional services with start type,
   dependents and ports; Run/RunOnce, Startup folders, non-Microsoft scheduled
   tasks with LastRunTime/LastResult; UWP background access.
2. Processes and memory: top 15 by RAM and by accumulated CPU, per-app totals,
   handle/thread anomalies, commit vs RAM, memory compression, page combining,
   pagefile/swapfile/hiberfil.
3. Apps and storage: unused apps via intent metrics; WinSxS with
   `DISM /Online /Cleanup-Image /AnalyzeComponentStore` (elevated), Windows
   Installer, DriverStore oem duplicates, Recycle Bin, temp and browser/GPU
   caches, dumps, WER, `$Windows.~BT`, volume health.
4. GPU/display, power/thermals, network, security (read-only), stability and
   events, workloads, recovery and devices: driver age, HAGS, power plan, CPU
   limits, throttling, DNS/TCP/adapters, Defender/firewall/BitLocker/VBS,
   WHEA and Kernel-Power 41, bugchecks, pending updates, problem devices.

Use your own read-only tools too: `Get-CimInstance Win32_Service`,
`Get-ScheduledTask` and `Get-ScheduledTaskInfo`, `Win32_StartupCommand`,
`Get-PnpDevice -Status ERROR`, `Win32_PnPSignedDriver`, `Get-Process` for
handles, `Get-ChildItem` for folder sizes, `pnputil /enum-drivers`. Registry
paths always carry the drive colon (`HKCU:\`, `HKLM:\`). Where a check needs
administrator rights, mark it unavailable instead of guessing.

### Machine-specific rows

Every row you add or keep carries the exact action and the named target (the
shortcut file, the folder, the game, the service, the task), a measured size or
machine state (`6.37 GB`, `214 background processes`, `HAGS is off`) marked
`[measured]` or `[inferred]`, what exactly changes on THIS PC, and how to
reverse it. Never write "frees space", "several gigabytes" or "some space".
A size row below 500 MB is not printed either; a smaller target appears only
when removing it fixes a named function or security issue, and the row says why.
If the target does not exist (no Windows.old, no such shortcut, no such game),
do not print the row. Never propose creating a restore point. Never duplicate a
pcx row as a new finding.

### Report shape

Print in this order:

1. A compact machine summary, 3-4 lines, every line with a number: OS build;
   CPU/GPU/RAM total, free and commit; each disk's model, free/total, health,
   wear and temperature. Nothing else: no uptime, power plan, top apps, patch
   age, process or error counts. No adjective without a number.
2. The table pcx returned, exactly, no code fence, then your own rows N+1 with
   the same four columns and risk scale (`Safe / Changes behavior / Risky`).
   Copy pcx values verbatim. No second table, no "table revision", no `skip N`
   list, no restatement. If a pcx row is a false positive, drop it from the
   printed table and say so in one short line.
3. At most two short lines: the top causes and what is already good. If the
   table is empty, print one line starting `already good:` / «уже в порядке:»
   and stop; do not invent rows.
4. One bold question as the last line, numbers only: **What do we do: 1, 2, 7?**
   / **Что делаем: 1, 2, 7?** Ask it as a plain chat message. Never ask "manual
   or admin", never ask per row, never use a question card. Items that cannot
   be automated (BIOS/firmware, Windows updates, pagefile, moving games) carry
   that fact inside their row; they are still just a number, or not printed.

Account for all 12 domains: every measured problem is a row or is named in the
already-good line. A cache-only table is incomplete. Every cause named in the
top-causes line must have a row number.

Stop immediately on `stop` or «стоп»; the next message resumes the same list.
For performance rows always say effect not promised.

## Step 3. Do the work the user picked

The user answers in chat with numbers — "1, 4 и 6", "всё кроме пятого",
"давай". Then:

1. Apply the pcx catalog rows (`source = catalog`) with the exact invocation:
   `pwsh -File <path>/pcx.ps1 tune --apply <rows>` (rows = numbers or ids;
   alternatives: `--plan <plan-id>`, `--proposals <file>` for targets outside the catalog,
   file schema `pcx-proposals/1`). `pcx` is the fast path for
   typed changes (registry, service, task, file) because it snapshots and can
   undo; use it where it fits.
2. Manual rows (`source = manual`) are yours to perform: delete Windows.old,
   WER reports and `%TEMP%` with your tools, run `powercfg /h off` for the
   hibernation file. One change at a time, verify each, say what you did and
   how it is reversed. Do not create a restore point.
3. Rows that pcx does not apply and you cannot do: do the safe ones yourself
   with your own tools. Hand these to the user with the exact reason:
   BIOS/firmware, installing Windows updates, resizing the pagefile, and
   physically moving games. For a risky item you cannot safely do, say so in
   one line instead of dropping it.
4. If `pcx` cannot express the change or refuses it, do **not** stop and do not
   hide it: explain in one line why, then do it the correct way yourself. Ask
   once before anything risky or not reversible.
5. Stop immediately on `s` or «стоп». Applied changes stay applied, the rest
   stays pending, and the next message resumes the same list.
6. Never do only the easy part. If something cannot be done, say so plainly
   instead of quietly dropping it. Rows that need the user (BIOS, firmware,
   boot chain, drivers) stay a conversation: explain the command and reversal.

## Report

End with one message: what changed and how to reverse it, what stayed pending
and why, what is already good, and what you would look at next.

## Rollback is best effort, not a promise

`pcx undo --item`, `--plan` and `--last` restore typed actions exactly and exit
0 only when every snapshot matches; exit 3 means undo was refused and nothing
was reverted. Anything you changed outside pcx has no automatic undo: say how to
reverse it, and if it cannot be reversed, say so **before** doing it.

## Freedom and limits

You are free to investigate and free to act. Two limits only:

- never hide a finding, a refusal or a failure;
- never touch what can break the machine: boot chain, security services, kernel
  drivers, anticheats, managed devices, S Mode, Dev Drive. Explain and stop there.

Never invent a measurement. Never promise frames per second or a latency
percentage: performance items report measured state and always say effect not promised.

## What pcx is not

- It is not a generic optimizer; it never automates a boot-chain or security change.
- It never updates, installs, or adds itself to PATH, and produces no HTML or forms.

## Reference

- `references/method.md` how to investigate, and what is never automated.
- `references/catalog.md` the typed actions and the manual notes.
- `SAFETY.md` the threat model and the fixture-only rule.
- `INSTALL.md` the pinned file list with SHA-256 values.
