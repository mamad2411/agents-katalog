---
name: sdlc-gates
description: Flow-control primitives for the SDLC pipeline — GATE (human approval), LOOP-GUARD (N tries then ask), and PRECONDITION (state guard). Apply whenever presenting an approval gate, running a fix/repair loop, or refusing an action based on sprint state. Used by the orchestrator (skills/sdlc) and the /sdlc-release, /sdlc-fix-ci, and /sdlc-sprint commands.
---

# SDLC Gates — flow-control primitives

Every "gate," fix-loop, and state refusal in the pipeline is an invocation of one of the three primitives below. Behavior is defined here once; the orchestrator and commands reference it by name instead of restating it.

## GATE — human approval

`GATE(artifact, unlocks, agent, [condition])`

1. **Conditional skip.** If `condition` is provided and evaluates **false**, skip the gate: record `auto-passed: <reason>` in the manifest and proceed to `unlocks`. (Outward-facing gates never take a `condition` — see Invariants.)
2. **Present.** Show `artifact` to the user in full.
3. **Decide.** `AskUserQuestion`:
   - **Approve** → proceed to `unlocks`.
   - **Request changes** → `SendMessage` the feedback to `agent` (it keeps its context), then re-run `GATE` on the revised artifact.
   - **Cancel** → stop, summarize, update the manifest.
4. **Record.** Update the manifest's gate status after every outcome.

**Never reach `unlocks` without an explicit Approve or a conditional auto-pass.**

### Same-session collapse (③ + ④)
On a **standalone run** (Notion disabled) that proceeds from the review sign-off (`GATE ③`) directly into `/sdlc-release` within the **same session**, present `GATE ③` and `GATE ④` as a **single "Approve & ship" confirmation** instead of two. In every other path — Notion mode, or a release run in a separate session — ③ and ④ stay distinct.

## LOOP-GUARD — bounded retry

`LOOP-GUARD(maxTries = 3)`

Wrap a repeating act→check cycle (fix→inspect, patch→re-run). After `maxTries` cycles **without** a clean pass, stop and `AskUserQuestion`:
- **Continue** another cycle ·
- **Accept** the remainder ·
- **Intervene / Stop**.

On escalation in Notion mode, set the ticket `Status = Blocked`.

## PRECONDITION — state guard

`PRECONDITION(check, onFail)`

Evaluate `check` before an action. **Silent** when it holds; when it fails, refuse with the `onFail` message and stop. A `PRECONDITION` is **not** a gate — it asks nothing when satisfied. Instances:

| Name | check | onFail |
|------|-------|--------|
| Ready-to-start | every ticket in the sprint has `Ready = true` | "Run `/sdlc-plan` to refine tickets to the Definition of Ready first (override with `--skip-planning`)." |
| Single-active-sprint | no other sprint is `Active` | "Close the active sprint first." |
| Release-when-not-active | no sprint is `Active` | "Production release happens after the sprint is closed and UAT'd on staging." |
| Backlog-intake-stop | request is not a new Notion item | Capture to the backlog and stop (don't run phases). |

## Invariants
- **Never remove the only approval of a thing.** A `condition` may auto-pass a gate only when that thing was already approved elsewhere (e.g. requirements at `/sdlc-plan`).
- **Outward actions are never automatic.** `GATE ④` (deploy/publish/push) is never given a `condition`.
