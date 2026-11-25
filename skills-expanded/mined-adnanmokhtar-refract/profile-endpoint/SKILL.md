---
name: profile-endpoint
description: Load one endpoint at a fixed arrival rate, profile where its time goes with the runtime's sampling profiler, and capture its slow queries — runnable commands per stack. Use before optimizing.
kind: skill
pack: performance
allowed-tools: [Read, Grep, Glob, Bash]
---

# profile-endpoint

Load + flamegraph + slow-query capture on one endpoint. Never optimize on vibes.

## Premise

Real signals only. Every percentile, RPS number and "% of time in" comes from a run whose command line is in the report: the load tool's output captured verbatim, the profile file written to disk, the slow-query list read from the database. Recommendations cite the frame, the query or the function from that artifact. A dev-mode server (watch mode, debug build), an empty table or a laptop-only number is either re-run on realistic data or reported as what it is.

**What this skill proves, and what it does not.** It measures **cost** and **attributes** it: where time goes under a stated load. It does not by itself prove a defect class. A hot frame is a *candidate* for the detector that owns its class, and a candidate becomes a finding only through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with its class oracle from [`proof-oracles.md`](../../../../snippets/proof-oracles.md) — the query count at two sizes for an N+1, the event-loop delay for blocking work. A profile ranks; an oracle proves.

## Halt conditions

- Refuse to report p50/p95/p99 without the load-tool output and the exact command that produced it.
- Refuse a latency claim from a closed-model run (autocannon without `-R`, plain `wrk`, `hey`, k6 `constant-vus`): coordinated omission understates the tail (`precedents/performance.md` § 48). Open model, and print the achieved rate beside the target.
- Refuse to claim "X% of time in Y" without the profile file whose frame Y carries that share, labelled with the sample count.
- Halt if the tables are empty or seeded so thinly that the planner picks a plan production would not. The threshold is not a row count: run the plan on the seeded data and compare the access method with production's (`pg_stat_statements` / `auto_explain` from production, or the plan `index-coverage-scan` captured, *database pack, when installed*). A profile on a toy table describes a database you do not run (`precedents/performance.md` § 4).
- Don't propose an index without the slow query that needs it, cited from the captured list; hand index decisions to `/optimize-query` *(database pack, when installed)*.
- Don't recommend "optimize the loop" without the file, the line and the frame.
- No candidate reaches a report as a finding without the `refute-before-report.md` pass.

## When to use

- An SLO is being missed on one route, job or consumer.
- Before a "performance" change — the baseline comes first.
- After a release that quietly slowed something else.
- When `load-test` found a knee and handed over the subject at that knee.

## Prerequisites

- The service built and started the way production runs it (`NODE_ENV=production`, a release build, no `--watch`, no debugger, the same worker count), on data shaped like production's.
- A load generator on a separate host, or at least on cores the server does not use; generator CPU stays under 80% or the run measured the generator (`precedents/performance.md` § 48).
- The profiler's permissions: ptrace-based samplers need root on macOS and `SYS_PTRACE` in a container (Docker `--cap-add SYS_PTRACE`; Kubernetes `securityContext.capabilities.add: [SYS_PTRACE]`).
- An output folder outside the source tree for artifacts: `mkdir -p prof`.

## Step 1 — Load at a fixed arrival rate (open model)

```bash
URL='http://localhost:3000/api/orders?limit=50'; RATE=200
# autocannon 8.0.0: -R fixes the overall rate (coordinated-omission correction on by default); headers are K=V
npx --no autocannon --version >/dev/null 2>&1 || echo "NOT-RUN (autocannon not installed — to enable: npm i -D autocannon@8)"
npx --no autocannon -c 64 -d 60 -R "$RATE" -l -j --renderStatusCodes -H "authorization=Bearer $TOKEN" "$URL" > prof/load.json
# oha 1.16.0: the correction only works together with -q
oha -z 60s -c 64 -q "$RATE" --latency-correction --no-tui --output-format json -H "Authorization: Bearer $TOKEN" "$URL" > prof/load.json
# k6 2.x: constant-arrival-rate; thresholds exit non-zero. AGPL-3.0 — run it as a tool, never vendor it into the project
k6 run -e URL="$URL" -e TOKEN="$TOKEN" --summary-trend-stats="avg,med,p(95),p(99),max" prof/load.js
```

```js
// prof/load.js
import http from 'k6/http';
export const options = { scenarios: { s: { executor: 'constant-arrival-rate', rate: 200, timeUnit: '1s', duration: '60s', preAllocatedVUs: 100 } },
  thresholds: { dropped_iterations: ['count<1'] } };
export default () => http.get(__ENV.URL, { headers: { Authorization: `Bearer ${__ENV.TOKEN}` } });
```

Pick a rate from the route's production call rate (APM, access logs) or the SLO's target; a rate the generator could not reach (k6 `dropped_iterations` > 0, autocannon's achieved req/s below `-R`) measured a lower load than claimed.

## Step 2 — Profile under that load, per runtime

Attach while Step 1 runs at the same rate; one artifact per run, kept under `prof/`. Versions and flags as of 2026-10-02.

| Runtime | Command (CPU unless stated) | Read it with | Traps |
|---|---|---|---|
| **Node.js** | `npx 0x -D 'prof/{pid}.0x' -- node dist/main.js` (0x 6.0.0, Node ≥ 20; stop with Ctrl-C / SIGINT, which writes the flamegraph). Built-in: `node --cpu-prof --cpu-prof-dir=prof dist/main.js` writes a `.cpuprofile` at process exit — give the app a graceful `SIGINT` path that calls `process.exit()`, and check the file exists. Sync I/O on the loop: `node --trace-sync-io dist/main.js` | `.cpuprofile` in Chrome DevTools → Performance, or speedscope | `clinic` 13.0.0 (last release 2023-06; its README says it is not actively maintained) may misreport on current Node — optional, never a required step |
| **Python** | `py-spy record -o prof/cpu.svg -d 60 --pid "$PID"` (py-spy 0.4.2); add `--subprocesses` on the gunicorn / uvicorn master, `--idle` to include waiting frames (wall clock), `--gil` for GIL holders; `--format speedscope -o prof/cpu.json` for speedscope | the SVG, or speedscope | root on macOS; `SYS_PTRACE` in containers; Python 3.15's `python -m profiling.sampling` is the stdlib alternative once you run 3.15 |
| **Go** | the service imports `net/http/pprof` on an internal-only port, then `curl -s -o prof/cpu.pb.gz "http://localhost:6060/debug/pprof/profile?seconds=60"` (Go 1.27) | `go tool pprof -top -nodecount=25 prof/cpu.pb.gz`; `go tool pprof -http=:8080 prof/cpu.pb.gz` | never expose the pprof port publicly; `block` / `mutex` profiles are empty unless `runtime.SetBlockProfileRate` / `SetMutexProfileFraction` are set |
| **JVM** | `asprof -e cpu -d 60 -f prof/cpu.html "$PID"` (async-profiler 4.5); `-e wall -t` for threads parked in I/O; `-e alloc` for allocation. JFR: `jcmd "$PID" JFR.start duration=60s settings=profile filename=prof/rec.jfr` | the HTML flamegraph; JDK Mission Control for `.jfr` | containers block `perf_event_open`: use `--fdtransfer` or `-e ctimer` |
| **.NET** | `dotnet-trace collect -p "$PID" --profile dotnet-sampled-thread-time,dotnet-common --duration 00:00:01:00 --format Speedscope -o prof/trace.nettrace`; thread-pool starvation: `dotnet-counters monitor -p "$PID"` | speedscope (the converted file), PerfView or Visual Studio for `.nettrace` | `collect` no longer has a `cpu-sampling` profile (Microsoft Learn, 2026-06-10); `--duration` is `dd:hh:mm:ss`; run as the target process's user |
| **Ruby** | `sudo rbspy record --pid "$PID" --duration 60 --format flamegraph --file prof/cpu.svg` (rbspy 0.53.0); `--subprocesses` on the Puma / Unicorn master | the SVG; `--format speedscope` for speedscope | ptrace capability in containers; GVL contention needs vernier, not rbspy |
| **Native / Rust (Linux)** | `perf record -F 99 -g -p "$PID" -- sleep 60` | `perf report --stdio` | needs `kernel.perf_event_paranoid` ≤ 1 or root; symbols from a release build with debug info |

A share is reported as `measured (sampling, <n> samples, <tool@version>)`. A frame under a few percent of samples is noise unless it is the whole of a slow request's tail.

## Step 3 — The database side of the same run

Reset before Step 1, read after it, on the database the profiled server talks to — never a production primary without the user's go.

```sql
-- PostgreSQL (pg_stat_statements loaded via shared_preload_libraries)
SELECT pg_stat_statements_reset();                       -- before the run
SELECT calls, round(total_exec_time::numeric, 1) AS total_ms, round(mean_exec_time::numeric, 2) AS mean_ms,
       rows, left(query, 120) AS query
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 20;   -- after the run
-- without the extension: ALTER DATABASE app_dev SET log_min_duration_statement = '50ms'; (new sessions only; RESET it afterwards)
-- MySQL: SET GLOBAL slow_query_log = ON; SET GLOBAL long_query_time = 0.05;  then  pt-query-digest <slow-log> --limit 95%:20
-- MongoDB: db.setProfilingLevel(1, { slowms: 50 });  then  db.system.profile.find().sort({ millis: -1 }).limit(20)
```

`calls` divided by the requests the load tool completed is **queries per request**. A count that grows with the page size is an N+1 candidate: prove it with the query-count scaling oracle (`proof-oracles.md` § Query-count scaling) and hand it to `n-plus-one-scan` *(database pack, when installed)*. A slow statement goes to `/optimize-query` *(database pack, when installed)*; without that pack, report it Unconfirmed with the `EXPLAIN (ANALYZE, BUFFERS)` to run on production-shaped data.

## Procedure

1. Start the server as in § Prerequisites; reset the database statistics (Step 3).
2. **Warm up** 30 s at the target rate and discard it (JIT, pools, caches).
3. **Baseline** at the target rate, 60 s (Step 1). **Repeat it twice more** without changing anything: the spread of the three p95s is the noise band, and any later delta inside it is `NO-CHANGE` (`proof-oracles.md` § Noise band rules for timing oracles).
4. **Profile** a fourth run at the same rate, profiler attached (Step 2). A ramp at higher rates belongs to `load-test`; profile at the rate where the SLO is missed.
5. **Read the database side** (Step 3) and compute queries per request.
6. Turn verbose logging back off; keep `prof/` out of version control.

## Output

```
Endpoint: GET /api/orders?limit=50          build: release, NODE_ENV=production, 1 process
Load:     autocannon 8.0.0 -c 64 -d 60 -R 200 · target 200/s achieved 199.4/s · gen CPU 31%
Baseline (3 runs): p50 41 / 43 / 42 ms · p95 88 / 93 / 90 ms (band ±3 ms) · p99 140 ms · errors 0
Profile:  0x 6.0.0, 11,820 samples → prof/48211.0x/
  38%  OrderRepository.findForList        (measured, sampling)
  17%  OrderMapper.toDto → JSON.stringify  (measured, sampling)
  12%  pg-protocol Parser.parse            (measured, sampling)
DB (pg_stat_statements, reset before the run): 11,964 requests completed
  SELECT … FROM order_items WHERE order_id = $1     calls 598,200 → 50.0 per request
  SELECT … FROM orders WHERE seller_id = $1 …        calls  11,964 → 1.0 per request, mean 6.1 ms
Lanes:   load RAN · profiler RAN · db RAN
Hand-offs (candidates, not findings):
  - 50 queries per request on order_items, scaling with limit → n-plus-one-scan (database pack); oracle: query count at limit 2 vs 20
  - OrderMapper.toDto 17% → request-path-scan; settle with a benchmark inside the noise band before ranking
```

The block above is a shape: every number in a real run is copied from the artifact it names. A lane that could not run prints `SKIPPED (<reason>)` — no profiler permission, no database access — and the report says which claims that leaves unmeasured.

## False positives / gotchas

- Empty or tiny tables answer every query in about 0 ms; seed to the production row estimate and `ANALYZE` first.
- A laptop number is relative, not absolute; compare before and after on the same machine, never against a production dashboard.
- The first requests hit cold caches, unopened pool connections and an unoptimized JIT — that is what the warm-up discards.
- `-c` connections is not a rate. Only `-R` / `-q` / `constant-arrival-rate` fix the arrival rate.
- p99 averaged across runs or pods means nothing; keep each run's histogram, compare medians of percentiles.
- Lower latency with a higher error rate, or with smaller responses, is a regression in disguise (`precedents/performance.md` § 50).
- Sampling profilers attribute time spent waiting on I/O differently: CPU mode hides it, wall mode (`--idle`, `-e wall`) shows it. Say which mode the shares come from.

## Baseline registration

A profiled hot path stays guarded once it is registered in the behavioural-baseline registry (`.claude/baselines/main/manifest.json`, proposal §7) as kind `performance`:

```bash
bash .claude/scripts/baseline-capture.sh register --id=perf-orders-list-p95 --kind=performance \
  --engine=performance/profile-endpoint --scope='src/orders/**,src/db/**' \
  --command='bash scripts/perf/bench-orders-list.sh' --harness=scripts/perf/bench-orders-list.sh \
  --artifact=.claude/baselines/main/perf-orders-list-p95.samples.json --compare=perf --unit=ms --cadence=nightly
```

- The command prints **one** latency number per run, the p50 or the p95, from its own checkout. That is either a hot-path microbenchmark (`--bench=<name>` picks one out of several) or Step 1's fixed-rate run after a warm-up: start the release build, load at the stated `-R`, print the percentile, stop. G4 runs it in a worktree at the base sha too, which is why it is committed (not under `prof/`) and listed in `--harness`. `--artifact` is a samples file the capture writes.
- **Gate G4**, in CI, nightly, and at P5 for the hot paths a run touches: `behavior-diff.py --gate=G4` drives `perf-compare.py` under the rules of [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Performance, with runs and threshold from `THR-PERF-REGRESSION`. Procedure step 3's three-run band ranks a candidate. It is not the G4 sample. A refused verdict (`TOO-NOISY`, `INSUFFICIENT-RUNS`, `SUSPECTED-REGRESSION`) is UNVERIFIED, never a pass.
- `changes_baseline` explains G14 diffs only. A G4 `REGRESSION` needs a human waiver (`THR-WAIVER`). Re-recording the samples file needs an acceptance criterion naming `perf-orders-list-p95`, or `test-integrity.py` fails it (`undeclared-baseline-rewrite`).

## Related

- `load-test` — boundary: this skill diagnoses ONE slow subject at one rate; `load-test` runs the whole-system campaign (mix, ramp to breakpoint, headroom) and hands the subject at the knee back here.
- `memory-leak-hunt` — boundary: this skill profiles where time goes now; `memory-leak-hunt` holds load flat and hunts heap growth over time. RSS climbing during Step 4 goes there.
- `/profile-perf` — the command that dispatches this skill for one slow path and ranks the fixes.
- Detectors that receive the hand-offs: `request-path-scan` and `memory-growth-scan` (this pack); `n-plus-one-scan`, `index-coverage-scan` and `/optimize-query` *(database pack, when installed — without it, the database hand-offs are reported Unconfirmed with their settling probe)*.
