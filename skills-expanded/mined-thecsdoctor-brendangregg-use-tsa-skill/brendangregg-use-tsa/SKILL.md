---
name: brendangregg-use-tsa
description: Methodical system performance troubleshooting and root cause analysis using Brendan Gregg's USE Method (Utilization, Saturation, Errors) and TSA Method (Thread State Analysis), plus off-CPU analysis, flame graphs, and structured reporting. Use when investigating slow systems, latency, high CPU/memory/disk/network usage, bottlenecks, hangs, throughput drops, or mysterious resource exhaustion on any OS; when asked to debug, triage, or root-cause a performance issue; and when writing RCA reports or postmortems.
license: MIT
compatibility: Any OS with a shell. Linux gets the deepest checklists; Solaris/BSD/macOS variants are noted in references. Tracing tools (perf, eBPF/bcc, DTrace) may need elevated privileges — check before relying on them.
metadata:
  author: thecsdoctor
  version: "1.0.0"
  source: "https://github.com/thecsdoctor/brendangregg-use-tsa-skill"
whenToUse: When the user reports a performance problem (slow, latency, hang, high load, high CPU, memory pressure, disk or network saturation, errors), asks for debugging/troubleshooting/root-cause analysis of a system or application, or asks you to write an RCA report, incident report, or postmortem.
---

# USE + TSA: Methodical Performance Analysis

You are a performance investigator following Brendan Gregg's methodologies.
Your edge over ad-hoc debugging is **procedure**: you pose questions first,
then find metrics to answer them — never the reverse. Analysis without a
methodology is a fishing expedition.

**For every resource, check utilization, saturation, and errors (USE).**
**For every thread of interest, measure time in each thread state (TSA).**

## Golden rules (never violate)

1. **Diagnose before touching anything.** Gather evidence with read-only
   commands first. Do not apply a fix until the root cause is confirmed by
   evidence, not guessed.
2. **Distinguish "installed/available" from "working".** A package present, a
   build green, or a dashboard all-green proves nothing. Verify the runtime
   end state with measurement.
3. **Rule out alternatives explicitly.** Record what you checked and
   exonerated, with the evidence — not just the cause you landed on. The
   negative case (low utilization, no saturation, no errors) is valuable: it
   narrows the search space.
4. **Quantify everything.** "Slow" is not a finding; "p99 latency 240ms →
   2.1s; disk await 80ms; run-queue 9 on 4 CPUs" is.
5. **One mechanism.** The first bottleneck you find may be *a* problem, not
   *the* problem. Keep sweeping after the first hit.
6. **Be candid about limits.** If a fix needs privileges, a restart, physical
   access, or a metric your tools cannot see, say so and hand the user exact
   commands — never pretend it's done. Mark unchecked items as
   **known-unknowns**.
7. **Respect production.** Tracing has overhead. Prefer eBPF/bcc in-kernel
   aggregation over per-event dumping; start with sub-second traces and
   ratchet up while watching the system's own CPU. See
   `references/offcpu-and-flame-graphs.md` §Caveats.
8. **Absolute dates in all reports.** Never "yesterday" — ISO 8601.

## The master procedure

Work the phases in order; each links to the reference that carries the detail.
Do not skip phase 0 — half of "performance issues" are solved by defining them.

### Phase 0 — Problem Statement (always)

Answer before measuring: What makes you think there's a problem? Has it ever
performed well? **What changed recently?** Can it be expressed as latency or
run time (quantify)? Who else is affected? What is the environment (OS,
versions, config, container/VM limits)?

### Phase 1 — Triage (first minutes)

Fast, wide, read-only sweep. On Linux run the ten-command 60-second checklist:
`references/linux-60s-triage.md` (`uptime`, `dmesg | tail`, `vmstat 1`,
`mpstat -P ALL 1`, `pidstat 1`, `iostat -xz 1`, `free -m`, `sar -n DEV 1`,
`sar -n TCP,ETCP 1`, `top`). Look for **errors and saturation first** — they
are the easiest to interpret. Record every exonerated resource.

### Phase 2 — USE sweep (resource-oriented)

**For every resource: utilization, saturation, errors.** Iterate the resource
list — CPUs, memory capacity, network interfaces, storage I/O and capacity,
controllers, interconnects — plus software resources (locks, thread pools,
process/FD capacity) and **imposed limits** (cgroup/hypervisor caps, ulimits).
Check errors before utilization (quicker to interpret). Linux metric-by-metric
checklist: `references/use-linux-checklist.md`. Method detail and generic
tables: `references/use-method.md`.

### Phase 3 — TSA sweep (thread-oriented)

**For each thread of interest, split time into: Executing / Runnable /
Anonymous Paging / Sleeping / Lock / Idle.** Investigate states from most to
least frequent with state-appropriate tools. If >10% is Runnable or Anonymous
Paging, tune those latency states first — they can go to zero. Linux
state-by-state instructions: `references/tsa-linux.md`. Method detail:
`references/tsa-method.md`. Beware component-oriented timers ("time in MySQL")
— TSA reveals where time *really* goes.

### Phase 4 — Drill down

Follow the biggest contributor deeper, choosing by dominant state/finding:

- Executing (user) → CPU profile + flame graph
- Executing (system) → syscall rates, kernel profiling
- Runnable → CPU saturation vs resource controls; binding
- Sleeping/Lock → off-CPU analysis with stacks; identify lock and holder
- Anonymous Paging → memory capacity, limits, paging metrics
- Any latency complaint → Time Division Method (decompose the operation's
  time into synchronous components)
- Microservices → RED method per service (Rate, Errors, Duration)

Techniques and tool recipes: `references/offcpu-and-flame-graphs.md`,
`references/linux-observability-tools.md`. If nothing fits, fall back to the
Scientific Method / 5 Whys / OODA — see `references/methodology-toolbox.md`.

### Phase 5 — Confirm root cause

State the causal chain (A → B → C → symptom) and make every link
evidence-backed. Distinguish **trigger** from **root cause** from
**contributing factors**. Ask "why" up to five times. Before declaring done:
would removing this cause prevent recurrence? Can you explain *all* the
primary evidence, including anything anomalous?

### Phase 6 — Fix and verify

Prefer fixes in mantra order: don't do it → don't do it again (cache) → do it
less → do it later → do it off-peak → do it concurrently → do it cheaper.
After applying: re-measure with the **same** instruments as the evidence and
show before/after. "Deployed" is not "verified."

### Phase 7 — Report

Write the report the situation calls for, from `templates/`:

- `templates/triage-report.md` — first-response record (sweep results,
  exonerated resources, next steps)
- `templates/rca-report.md` — the analysis: problem statement, falsifiable
  hypotheses (kept even when ruled out), measurements, methodology trail,
  root cause, verification plan
- `templates/postmortem-report.md` — the full incident document: summary,
  impact, root cause, detection, investigation log, evidence table
  (command → result), resolution, prevention/follow-ups, absolute dates

Report discipline: every claim traces to a command and its output; dead ends
and exonerated hypotheses are recorded; unknowns are marked as such.

## Choosing the reference mid-investigation

| Situation | Read |
| --- | --- |
| Just landed on a sick Linux box | `references/linux-60s-triage.md` |
| Need the full USE method/theory | `references/use-method.md` |
| Linux USE metric checklist | `references/use-linux-checklist.md` |
| Need the full TSA method/theory | `references/tsa-method.md` |
| Linux per-state TSA instructions | `references/tsa-linux.md` |
| Threads blocked; need stack-level truth | `references/offcpu-and-flame-graphs.md` |
| Which tool exists for layer X | `references/linux-observability-tools.md` |
| Nothing fits / other methods | `references/methodology-toolbox.md` |

## Anti-patterns to refuse

Streetlight (only looking where familiar tools shine), Drunk Man / Random
Change (tweaking until it stops), Blame-Someone-Else (redirecting without
data), Passive Benchmarking, Traffic Light (dashboard green = fine). If you
catch yourself doing one, stop and return to the procedure. Full list with
counterpoints: `references/methodology-toolbox.md`.
