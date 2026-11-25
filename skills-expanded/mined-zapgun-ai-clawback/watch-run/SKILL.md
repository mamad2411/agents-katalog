---
name: watch-run
description: Emit-on-event health watcher for a long paired/ab benchmark run, meant to be fed to the Monitor tool (each stdout line becomes one notification) so an unattended 75-min run cannot fail silently. Coverage-first by design — it speaks up on liveness (ALIVE), on new error signatures in the proxy/tee logs (ERROR), on a stall or crash (STALL/DEAD — silence is not success), and on completion (COMPLETE) — not just the happy path. Stall is tracked on the SHADOW (A0) turn-log, which is passthrough with keep-alive OFF so every line is a real turn; the PRIMARY (A5) log also grows from keep-alive pings during idle gaps and would mask a stalled conversation, so it must not drive stall detection. Use it to babysit `.skills/paired` or `.skills/ab` runs whose wall clock exceeds the Monitor's 60-min non-persistent cap (run it persistent).
---

# clawback run health watcher

`.skills/watch-run/scripts/watch_run.sh <out-dir> [listen-port primary-port shadow-port]`

Defaults: ports `8788` (tee/listen) `8790` (primary) `8791` (shadow) — the
`.skills/paired` defaults. Pass the run's `--out` dir as the first arg.

## How to use (with Monitor)

Launch the run in the background first (e.g. `.skills/scripts/run_paired.sh … --out
runs/paired-haiku-L1`), then attach this under the **Monitor** tool with
`persistent: true` (a 75-min run exceeds Monitor's 60-min non-persistent
timeout). The watcher exits on its own at COMPLETE/DEAD/WATCH-END, which ends
the Monitor cleanly; TaskStop it early if you abort the run.

```
Monitor(persistent=true,
  command=".skills/watch-run/scripts/watch_run.sh runs/paired-haiku-L1 8788 8790 8791")
```

## Events it emits (one line = one notification)

- `ALIVE a0=.. a5=..` — first turns observed; the run came up.
- `ERROR(+n) … :: <last matching line>` — n new error-signature lines in
  `proxy.primary.log` / `proxy.shadow.log` / `tee.log` (overload, 429,
  EADDRINUSE/ECONN*, `→ 4xx/5xx`, Traceback, force-exit, `[error]`, …).
- `STALL …` — no new SHADOW turn for 12 min but a proxy is still listening
  (warned once; the conversation is wedged, processes alive).
- `DEAD …` — no new SHADOW turn for 12 min AND no proxy listening → the run
  crashed; exits 1.
- `COMPLETE a0=.. a5=.. (+Nm)` — `report.md` present (analyzer finished);
  exits 0.
- `WATCH-END` — ~95-min wall-clock backstop tripped; exits 2.

## Why shadow-tracked stall (the subtle bit)

On a paired run the PRIMARY arm (A5 stack) fires keep-alive **pings** during
idle gaps, each appended to `instance.A5.ndjson`. So A5's line count rises even
when no real turn happens — tracking it for staleness would hide a stalled
conversation behind ping traffic. The SHADOW (A0) is `--passthrough` with
keep-alive off, so its line count == real-turn count: the honest liveness
signal. `ALIVE` still fires on either arm (proxies-up signal); only stall/crash
detection keys on A0.

## Tuning

Both are **env vars** (soft default + knob), so tune them per profile without
editing the script — pass them on the Monitor command line:

```
STALL_SEC=2400 .skills/watch-run/scripts/watch_run.sh runs/paired-haiku-L2 8788 8790 8791
```

- `STALL_SEC` (env, default 720s ≈ 12 min) — raise for L2+ where long gaps are
  normal: `STALL_SEC=2400` for L2 (up-to-30-min gaps), `~6000` for L3 (90-min).
  Set it above the profile's max gap + response slack. Too-low only emits a
  STALL warning; it never causes a false DEAD (that requires no proxy
  listening), so erring high is safe.
- `HARD_MAX_SEC` (env, default 5700s ≈ 95 min) — raise for runs capped longer
  than 75 min.

## Self-check (error detection is the fragile part)

The error-signature pipeline misfired twice in production — a startup crash
(`grep -c`'s print-0-and-exit-1 double-counted into `0\n0: syntax error`) and a
false ERROR on a healthy `.429Z` keep-alive ping (a bare `429` matched the
timestamp's milliseconds). Both are fixed and the detection now lives in one
tested function reachable via a hidden entry point:

    .skills/watch-run/scripts/watch_run.sh --errcount <logfile>   # prints the error count for one file

`test/watch_run.test.js` pins the must-NOT-cry-wolf cases (the `.429Z` ping, the
`→ 404 [no-route]` probe, a 4-digit `→ 4096` count) and the must-NOT-go-blind
cases (`→ 529`, `→ 5xx`, `EADDRINUSE`, `Traceback`, `[error]`). After touching
`ERRRE`/`IGNORE`, run `npm test -- watch_run`.
