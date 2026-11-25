---
name: sim-debug
description: >
  Structured simulator debugging for iOS/visionOS apps. Use when user says
  "debug this on simulator", "the app is doing X wrong", "run the app and check",
  "sim-debug", "why is the UI showing X", "something is broken in the simulator",
  "figure out why X happens", or describes visual/behavioral bugs in a running app.
  Also use when resuming with "resume debugging" or "pick up where we left off".
  Do NOT use for build errors without runtime behavior, unit test failures without
  simulator, or general code questions.
---

# Simulator Debugging

Hypothesis-driven debugging for iOS/visionOS simulator issues. Text-first observation, persistent state tracking, single-hypothesis testing. Prevents context waste and regression across sessions.

Implements the `superpowers:systematic-debugging` four-phase process with simulator-specific tooling. Core rule: **no fixes without root cause investigation first.**

## Entry Modes

**New bug:** User describes a problem → Phase 1.
**Resume:** User says "resume" or state file exists at `.claude/cache/debug-state.md` → read it, skip to "Next Steps", check "Dead Ends" before proposing anything.
**Agent mode:** For deep investigations (5+ cycles), spawn the `sim-debugger` agent instead. It gets its own context window and writes to the same state file.

## Two Toolchains

You have XcodeBuildMCP (build, run, LLDB) and AXe CLI (interact, inspect, reproduce). Use both.

| Task | XcodeBuildMCP | AXe CLI |
|------|--------------|---------|
| Build and launch | `build_run_sim` | — |
| Console logs | `start_sim_log_cap` / `stop_sim_log_cap` | — |
| View hierarchy | `snapshot_ui` | `axe describe-ui --udid <UDID>` |
| LLDB debugging | `debug_attach_sim`, `debug_variables`, etc. | — |
| Tap/swipe/type | — | `axe tap --id X`, `axe gesture`, `axe type` |
| Scripted reproduction | — | `axe batch --step ... --step ...` |
| Screenshot | `screenshot` | `axe screenshot --output path.png` |
| Video recording | — | `axe record-video --udid <UDID> --output bug.mp4` |

Get simulator UDID with `axe list-simulators`. Prefer `--id`/`--label` taps over coordinates.

## Phase 1: Observe

No code changes. Gather evidence only.

1. `build_run_sim` to launch the app
2. `axe list-simulators` to get UDID
3. `start_sim_log_cap` BEFORE triggering the bug
4. Trigger the bug — either manually or write an `axe batch` reproduction script (see `references/axe-reproduction.md`)
5. `stop_sim_log_cap` for console output
6. `axe describe-ui --udid <UDID>` for accessibility tree (or `snapshot_ui` for view hierarchy)
7. Write symptoms to state file — see `references/state-file-format.md`

**Observation costs:** see `references/tool-costs.md`. Text-first observation gives ~3x more debug cycles before context pressure.

## Phase 2: Hypothesize

1. List 2-3 possible causes ranked by likelihood
2. Each must have a specific, falsifiable test
3. Write to state file BEFORE touching code

## Phase 3: Test

One hypothesis at a time. No exceptions.

1. Minimum change — prefer log/breakpoint over logic change
2. Build and run
3. Reuse the reproduction script from Phase 1 if you wrote one
4. Capture evidence (text-first)
5. Record in state file: `confirmed` / `eliminated` / `inconclusive`
6. If LLDB needed, see `references/lldb-workflow.md`

## Phase 4: Fix

Only after hypothesis confirmed.

1. Implement fix (root cause, not symptom)
2. Build, run, verify with Phase 1 method
3. Run reproduction script — bug should be gone
4. Remove debug logging
5. Update state file: `status: resolved`

## Context Preservation

After 5 test cycles or context above 50%: ensure state file is current, write `context-forward.md`, suggest `/clear` + `/sim-debug resume`.

## Escalation

5 eliminated hypotheses → ask user for more context.
3 failed fixes → question the architecture, don't try fix #4.
