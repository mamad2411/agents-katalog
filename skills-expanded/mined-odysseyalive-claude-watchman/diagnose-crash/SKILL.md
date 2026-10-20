---
name: diagnose-crash
description: "ANALYZE: crash and OOM postmortem. Linux: journalctl across boots. macOS: DiagnosticReports and Unified Log jetsam events."
lane: coding
allowed-tools: Read, Glob, Grep, Bash
---

# diagnose-crash (Logic / Analyze)

Relates the facts into a cause. Walks journald **across boots** to explain crashes
and OOM kills. Key insight: a reboot (or series of them) often *follows* the
failure, so the evidence lives in the boot *before* the current one. Read-only —
it diagnoses and journals a remediation suggestion; it never applies it.

> **PRIME DIRECTIVE (outranks everything below).** Do nothing destructive. If any action
> would delete or overwrite a file or directory, modify a database in any way, sever access
> (firewall/SSH/auth), or stop/remove a service or package — STOP, WARN the operator in plain
> language why it is destructive, and ASK for explicit per-action permission before proceeding.
> In the unattended loop there is no one to ask, so the action does not happen: record it and
> surface it instead. The only non-destructive database operation is routine create-or-update
> through lib/journal.sh. This rule has no exceptions and no mode that overrides it.

## When to use

Every `/watchman audit`; especially after an unexpected reboot. Depends on logs
persisting across boots — see `check-log-retention`.

<!-- origin: watchman | version: 1.0 | modifiable: true -->
## Workflow

1. **Preflight.** Run every claude-watchman function through the dispatcher —
   `bash lib/wm <function> [args…]` — which sources the libs under bash internally; never
   `source lib/…` directly (dontAsk refuses a dot-source). Initialize with
   `bash lib/wm journal_init`. Determine the machine's family and profile by running
   `bash lib/wm watchman_family` and `bash lib/wm watchman_profile` and reading the printed
   values — use the family to pick the crash-evidence branch below. You do NOT pass them to
   `journal_upsert` (it auto-resolves them; pass `"" ""`). **I/O courtesy:** walking journald
   across boots — or `log show` on macOS — can be heavy: IF `bash lib/wm io_should_defer_heavy`,
   journal one `capacity`/`info`/`safe` `diagnostic_deferred` (`target=diagnose-crash`): first
   run `bash lib/wm io_pressure_reason`, then set detail to `"deferred: "` followed by its
   printed output (no `$(…)`). Skip this pass.

2. **Enumerate crash evidence (platform branch).**

   **Linux (family ≠ `darwin`):**
   - `bash lib/wm io_run sudo journalctl --list-boots` — walk boots **backward** from the
     current boot.
   - Per boot, hunt the kernel's own words for OOM kills, and services exiting with
     **code 137** (SIGKILL — typically the OOM killer), at idle priority:
     `bash lib/wm io_run sudo journalctl -b <id> -k -g 'Out of memory|Killed process|oom'`.

   **macOS (family == `darwin`):**
   - **DiagnosticReports.** List `/Library/Logs/DiagnosticReports/` and
     `/Users/*/Library/Logs/DiagnosticReports/` — sort by mtime, read the most recent. The
     memory-kill artifacts are `JetsamEvent-*.ips` (jetsam, with a reason field such as
     `highwater` = per-process memory limit, or `vm-compressor-space-shortage` = system-wide
     memory pressure); also scan recent `*.ips`/`*.crash` for `Exception Type: EXC_RESOURCE`.
   - **Unified Log (memory kills).** `bash lib/wm io_run log show --predicate 'eventMessage
     CONTAINS[c] "jetsam" OR eventMessage CONTAINS[c] "killed"' --last 24h 2>/dev/null` —
     extract process names and memory figures from the jetsam lines. `log show` can be slow:
     always run it through `io_run` and cap the window (`--last 48h` maximum).
   - **Note:** reading other users' DiagnosticReports needs sudo; if denied, limit the scan
     to the system-level `/Library/Logs/DiagnosticReports/`.

   **Windows (family == `windows`):**
   - There is no journald and no `journalctl`/exit-code-137 OOM-killer concept — Windows
     records the equivalent events in the Event Log. Run
     **`bash lib/wm diagnose_crash_events [days]`** (default window if `days` omitted), which
     emits one TSV line per relevant event:
     `<time>\t<log>\t<id>\t<source>\t<message>`. Parse those lines and map each event ID to
     the crash evidence:
     - **System 41** (`Kernel-Power`) — dirty / unexpected shutdown (the box went down
       without a clean stop; the kernel logged it on the *next* boot, mirroring the Linux
       "evidence lives in the prior boot" insight).
     - **System 6008** — unexpected shutdown (the previous system shutdown was unexpected).
     - **System 1001** (`BugCheck`) — a bugcheck / BSOD (stop error); the message carries the
       bugcheck code.
     - **Application 1000** — application crash (the app terminated unexpectedly).
     - **Application 1001** (`Windows Error Reporting`) — a WER fault bucket for an app crash.
   - On Windows, the "exit code 137 / OOM-killer" reasoning of the Linux branch is **replaced
     by these event IDs** — there is no SIGKILL-from-OOM signal to grep for. Treat 41/6008/1001
     as the unexpected-shutdown / crash evidence and App 1000/1001 as the app-crash evidence.

3. **Identify victim and hog.** From the OOM/jetsam evidence extract the killed process and
   the memory consumer (the hog) driving the kill. Correlate with `check-capacity`'s
   `memory_pressure` finding.

4. **Journal a finding** `check_id=oom_recent_kill`, `category=capacity`, `severity=high`,
   `risk_tier=review` (the fix touches service/app config). `target=<victim name>` — the
   systemd unit on Linux (`mysqld`), the process name on macOS, or on Windows the event
   source / faulting process name (e.g. `Kernel-Power` for a 41/6008 shutdown, or the app
   name from an Application 1000/1001 record), **never a PID or a `pid 3614` string**: PIDs
   change every boot, so a PID-bearing target duplicates the finding each run instead of
   folding it. Put the exact name and numbers in `detail`/`remediation`, with a concrete
   suggestion:
   - **Linux:** protect the victim with `OOMScoreAdjust=` or cap the offender with a cgroup
     `MemoryMax=`.
   - **macOS:** there is no `OOMScoreAdjust` and jetsam thresholds are not user-configurable;
     suggest reviewing the offending process's memory use, increasing RAM, or configuring the
     app's own memory limits.
   - **Windows:** there is no OOM killer to tune; for an unexpected-shutdown/BSOD (41/6008/1001)
     suggest reviewing the bugcheck code, drivers, and the minidump under
     `%SystemRoot%\Minidump`; for an app crash (1000/1001) suggest reviewing the faulting
     module from the WER bucket and the app's own memory/stability settings.

5. **Explain, never act.** Applying memory limits is `review`-tier and belongs to the
   operator-run fixer.
<!-- /origin -->

## Grounding

These claude-watchman functions are reached via the dispatcher (`bash lib/wm <function> [args…]`),
never by dot-sourcing the libs directly.

- `lib/distro.sh` — `journalctl` access (resolver_op `journal_read`).
- `lib/journal.sh` — `journal_upsert`.
- `check-capacity`, `check-log-retention` — the facts this skill correlates.
