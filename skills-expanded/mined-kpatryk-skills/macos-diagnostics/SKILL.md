---
name: macos-diagnostics
description: >-
  Diagnose and fix problems on a Mac running macOS, including dev-tool
  problems. Use whenever the user reports a Mac issue (battery drain,
  heat/fans, panics, restarts, Wi-Fi/Bluetooth drops, sleep/wake, slowness,
  low disk, rogue processes) OR a tool problem (mise, bun, npm, pnpm, yarn,
  uv, pip, pipx, poetry, brew / brew doctor / brew upgrade failing, tool
  won't install/upgrade/run, wrong version, command not found). Trigger on
  "my Mac is acting up", "brew is broken", "mise won't install X", "this
  tool won't run", even without the word diagnostic. Passive checks first,
  state changes only with evidence, raw traces, structured report filed
  under diagnostics/ as resolved or unresolved.
---

# macOS Diagnostics

Evidence-first troubleshooting for Mac system issues and for dev tools installed on it. Don't guess — probe, verify, log, file a report.

## Use when

- **Mac system:** battery, heat/fans, panics/restarts, Wi-Fi/Bluetooth, sleep/wake, slowness, disk full, SMART, rogue launchd.
- **Tools:** `mise`, `bun`, `npm`/`pnpm`/`yarn`, `uv`, `pip`/`pipx`/`poetry`, or `brew` failing to install/upgrade/run; `brew doctor` warnings; wrong version; `command not found`; PATH/shadowing; arm64 vs Rosetta; Gatekeeper quarantine; broken symlinks.
- Also on "check my Mac's health" with no symptom — treat it as a health sweep and start probing.

Quick one-liner checks skip `diag.py` and the workspace entirely: read-only probes only, no report or index. A written-report request cancels that shortcut — use the full workflow below.

## Clarify first

Ask at most 2 questions if the symptom or scope is missing (what breaks and when, exact command/output, what "fixed" means); otherwise start read-only probes immediately. An explicit health sweep or written-report request needs no symptom — probe right away.

## Rules

| Rule | Behavior |
|------|----------|
| **Passive first** | Read-only probes (`system_profiler`, `pmset -g`, `/usr/bin/log show`, `diskutil`, `df`, `launchctl`, `type -a`, `brew doctor`) before any state change. |
| **10-attempt budget + user fallback** | One attempt = hypothesis + probe/action + verification. At 10, stop and ask the user for next steps. If they asked for a written report, finalize it with an honest status (`resolved` only if the fix was verified, otherwise `unresolved` plus remaining hypotheses); with no report request, keep `working/<slug>/` — never auto-file unresolved. |
| **Mutate only with evidence** | Once passive evidence supports a cause, run the Tier 2 fix (reinstall, re-link, `mise use`, PATH fix, cache clear), announce it, verify. Tier 3 (erase/repair, delete user data, `rm -rf`, system `sudo`, SIP/firmware) needs explicit per-command consent. |
| **Verify symptom + log before acting** | Re-run the failing command or confirm the symptom is gone — exit codes don't count. Log every command + output before acting and update the attempt table immediately. |

## Workspace

Default root: `./diagnostics/` or `$MACOS_DIAGNOSTICS_ROOT`. Override per subcommand with `--root`, after the subcommand: `python3 scripts/diag.py init --root ./diag --slug <slug>`.

```text
diagnostics/{working,resolved,unresolved}/<slug>/report.md + traces/{command_outputs.log,system_logs.log}
```

`<slug>` is kebab-case (`m2-sleep-drain`, `bun-install-fails`). `working/` is scratch — finalize moves it, never copies.

## Workflow

1. **Capture + init.** Write a 1–2 sentence symptom, then:
   ```bash
   python3 scripts/diag.py init --slug <slug>
   ```
   Copy the report skeleton from `references/templates.md`, then log both baselines — command output and a system-log slice (finalize requires both traces non-empty):
   ```bash
   { sw_vers; uname -m; system_profiler SPHardwareDataType; } 2>&1 | python3 scripts/diag.py log --slug <slug> --stream command --label "baseline: system"
   /usr/bin/log show --last 1h --style compact 2>&1 | python3 scripts/diag.py log --slug <slug> --stream system --label "baseline: unified log"
   ```
   Verify: `init` prints the workspace path; both `traces/command_outputs.log` and `traces/system_logs.log` contain the baselines.

2. **Investigate (≤10 attempts).** Loop: hypothesis → probe → fix if justified → verify → log. Log every command and output; use `--stream system` for system-log slices:
   ```bash
   <command> 2>&1 | python3 scripts/diag.py log --slug <slug> --stream command --label "<what you ran>"
   ```
   Verify each attempt by re-running the failing command; update the attempt table in `report.md` immediately.

3. **Finalize only when done.**
   ```bash
   python3 scripts/diag.py finalize --slug <slug> --status resolved --description "One-line index description"
   ```
   `finalize` preflights the report status, the `Issue Folder` slug, and non-empty traces, moves the folder, and appends the index row. Finalize when the investigation is done: if the user requested a report, file it with an honest status — `resolved` only when the fix was verified, otherwise `unresolved` with remaining hypotheses and next steps. If the budget runs out and no report was requested, keep the workspace in `working/`, summarize the evidence, and ask the user for next steps — never auto-file `unresolved` without a request.

## Report

Copy `references/templates.md` exactly: Summary, RCA, Attempts table, Traces, Incidental, Lessons. Keep the `- **Status**:` line exactly `RESOLVED` or `UNRESOLVED`; it must match the destination folder.

## References

- `references/templates.md` — exact `report.md` / `index.md` format; `python3 scripts/diag.py <command> --help` — `init` / `log` / `finalize` only.

## Escalate, don't flail

Failing SMART / I/O errors, repeated panics same signature, data loss, T2/enclave/firmware errors, liquid damage, survives Safe Mode → stop, point to Apple Diagnostics, Safe Mode isolation, hardware service.
