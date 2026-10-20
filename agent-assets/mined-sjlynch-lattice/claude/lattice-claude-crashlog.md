# crashLog

Crash evidence for the backend and detached terminal-server lives under
`~/.lattice/logs/`. This code runs during early boot and fatal shutdown;
changes to dependencies, I/O or cleanup can affect evidence and process lifetime.

## Ownership

- [../crashLog.ts](../crashLog.ts) owns the process-global, install-once
  `installCrashLogging(label)`, bounded console ring, `noteCrashContext`,
  console tee, synchronous `writeCrashLog` and `crashLogDir`. It also configures
  diagnostic reports, owns signal/exit handlers and re-exports orphan adoption.
- [format.ts](./format.ts) contains pure argument/error rendering, memory
  summaries and filename timestamps/counter width. Keep it free of filesystem
  access and process lifecycle effects.
- [liveMirror.ts](./liveMirror.ts) owns dirty/in-flight snapshot state,
  `live-<label>-<pid>.log`, removal and next-boot orphan adoption.
- [retention.ts](./retention.ts) identifies owned files by filename and prunes
  each retention bucket independently.

The tee captures context and sends console output through
[../consoleSink.ts](../consoleSink.ts); that module owns bounded async output
and fatal flushing. [../processGuards.ts](../processGuards.ts) owns the backend's
exception/rejection fatal boundary and calls the crash writer before exiting.

The ring is bounded, but the tee is not cheap: every `console.*` argument goes
through `formatArg`, an unbounded `JSON.stringify`, before the line is cut to
2000 chars. Console-log a summary (ids, counts, sizes), never a whole large
object, array or Buffer — on a hot path that is per-call memory churn.

## Exit and evidence invariants

- Logging is best-effort: filesystem, report setup and console-capture failures
  must not turn logging into another fatal error.
- Fatal crash writes are synchronous. An async write may be lost when the
  caller exits; keep `writeCrashLog` usable directly from fatal/exit handlers.
- A successful crash write removes the live mirror immediately, including for
  fatal paths that later force-exit without running the `exit` handler.
- Every observed `exit` attempts to remove the live mirror, including normal
  exits. Leaving it behind would misidentify an orderly exit as a no-JS death.
  An uncovered nonzero exit writes a crash log unless a crash was already
  written or the installer is exiting on a lifecycle signal.
- Signal-handler ownership stays in the parent installer: `SIGINT`, `SIGTERM`
  and `SIGHUP` add breadcrumbs and defer when another listener owns shutdown.
  Without another listener, exit with `128 + signal number`; registering a
  listener suppresses Node's default termination, so merely recording is unsafe.
  The installer's signal exit is orderly and suppresses the nonzero crash backstop.
- Diagnostic `report.*.json` files cover JS-heap OOM and V8 fatal errors, not
  every native/OS death. Access violations, OS OOM-kills and `taskkill /F` can
  bypass JavaScript and report generation; absence of a report is not proof
  that no crash happened.

## Live snapshots and orphan adoption

Snapshots run every two seconds only when dirty, with at most one write in
flight, and contain the ring's latest 150 lines. The timer is `unref()`'ed:
mirroring must never keep an otherwise finished process alive.

At installation, adopt old live logs before starting this process's mirror.
Skip this PID and PIDs that are still alive; promote dead-PID mirrors to
`crash-<timestamp>-<dead-pid>-<label>-nojs.log` and remove the old live file,
best-effort. This preserves the available tail of deaths that ran no JS;
the tail can be stale and cannot establish the exact cause of death.

The local PID liveness helper is intentionally distinct from
[../projectRunLock/liveness.ts](../projectRunLock/liveness.ts): integer versus
finite validation and optional error-code access differ, and importing that
module brings in `child_process` and `crypto` during very early boot. Do not
deduplicate casually. The local probe treats `EPERM` as alive; only `ESRCH`
proves a probed PID is gone.

## Retention and existing coverage

Keep the newest `KEEP_FILES` (currently 20) by descending filename in each
separate bucket: `crash` (`crash-*` excluding `-nojs.log`), `crash-nojs`
(`crash-*-nojs.log`), and `report` (`report.*`). Timestamp-led filenames
determine order, not mtime. No-JS bursts
must not evict handler-written crashes; unrelated files and live mirrors are
outside retention ownership. Pruning runs at installation, crash write and adoption.

Existing coverage: [../__tests__/crashLog.test.ts](../__tests__/crashLog.test.ts)
checks crash content, location, retention and orphan adoption;
[../__tests__/crashLogSignalExit.test.ts](../__tests__/crashLogSignalExit.test.ts)
checks signal termination and delegation to another shutdown listener.
