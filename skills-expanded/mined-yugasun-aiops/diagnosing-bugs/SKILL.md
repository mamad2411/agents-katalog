---
name: diagnosing-bugs
description: Diagnosis loop for hard bugs and performance regressions. Use when the user says diagnose/debug, or reports broken/failing/slow behavior.
---

# Diagnosing Bugs

Skip phases only when explicitly justified. Read `CONTEXT.md` and local ADRs for module context.

## Phase 0 — Code graph query (optional, if available)

If `graphify-out/graph.json` exists, briefly tell the user "查询代码图谱了解影响范围" then query the code graph before starting diagnosis:

1. `/code-graph query impact <suspected-file>` — find all modules affected by the suspected code area
2. `/code-graph query deps <suspected-module>` — understand what the suspected module depends on
3. `/code-graph query hotspot` — check if the bug area is also a known hotspot (high coupling + frequent changes)

Use these results to narrow the hypothesis space in Phase 3. If no graph exists, skip silently.

## Phase 1 — Build a tight feedback loop

**This is the skill.** A tight pass/fail signal that goes red on *this* bug beats staring at code.

Try in order: failing test → curl/script → CLI fixture → headless browser → replay trace → throwaway harness → fuzz → bisect harness → differential old/new → HITL script.

Then tighten: faster, sharper assertion, more deterministic.

Non-deterministic bugs: raise reproduction rate until debuggable. If no loop is possible, stop — list what you tried, ask for env access or captured artifacts. **No red-capable command, no Phase 2.**

Done when one agent-runnable command is red-capable, deterministic, fast, and already run once (paste invocation + output).

## Phase 2 — Reproduce + minimise

Loop goes red on the **user's** symptom. Shrink repro one cut at a time — every remaining piece must be load-bearing.

## Phase 3 — Hypothesise

3–5 ranked, falsifiable hypotheses before testing. Show the list to the user when possible.

## Phase 4 — Instrument

One variable at a time. Debugger > targeted logs. Tag logs `[DEBUG-xxxx]` for cleanup. Perf: measure baseline, then bisect.

## Phase 5 — Fix + regression test

Regression test before fix **only at a correct seam** (real bug pattern at call site). No seam → document as architectural finding.

## Phase 6 — Cleanup

Remove debug tags, delete throwaway harnesses, re-run Phase 1 loop, state winning hypothesis in commit message.

**Post-fix:** if prevention needs architectural change (no test seam, tangled coupling), recommend `/aiops` with **Architecture health** — after the fix, with specifics.
