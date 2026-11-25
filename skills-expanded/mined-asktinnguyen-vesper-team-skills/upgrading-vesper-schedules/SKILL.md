---
name: upgrading-vesper-schedules
description: Upgrade and repair legacy Vesper schedules after scheduler refactors. Use when users ask to migrate old schedules, fix broken schedule delivery/session bindings, translate legacy `yolo_loop` behavior into the current reliable runtime model, or audit whether existing schedules still match the latest scheduler architecture.
---

# Upgrading Vesper Schedules

Upgrade legacy schedules with a repeatable, low-risk workflow that combines Vesper's built-in normalization with explicit inspection, repair, and verification steps.

Treat this skill as the default migration playbook for packaged-app agents: inspect first, separate deterministic repairs from behavior changes, and only mutate after clear user approval.

## Use This Skill When

Apply this skill when the user asks to:

- upgrade or migrate old schedules after scheduler refactors
- fix schedules that stopped delivering or lost their session bindings
- translate older `yolo_loop` concepts into the current reliable runtime model
- audit whether legacy schedules still match current runtime, routing, and continuity behavior
- clean up old `targetSessionId`, `scheduleSessionId`, `deliveryPolicy`, or `deliveryRoute` problems

Typical prompts include:

- "upgrade my old schedules"
- "migrate legacy Vesper schedules"
- "repair broken schedule bindings"
- "why did this old schedule stop posting?"
- "convert my old yolo loop schedules"

## Quick Start

1. Run `schedule_list` before any mutation.
2. Run `schedule_repair` with `apply=false` to identify deterministic repair opportunities.
3. Use `schedule_list({ scheduleId, includePrompt: true })` for any schedule that needs detailed inspection.
4. Use `schedule_forecast` after timing changes or route/session rebinding that could affect cadence.
5. Use `schedule_update` only after explicit user confirmation for behavioral changes.

## Upgrade Workflow

### 1. Inspect Current State

Start with a read-only inventory.

- Call `schedule_list` for the current workspace.
- Group schedules into:
  - already healthy
  - deterministically repairable
  - user-decision upgrades
- Treat `schedule_repair(apply=false)` as the canonical health audit.

Do not assume a legacy schedule is broken just because it uses older concepts. Vesper already auto-normalizes some schema/runtime fields on load and update.

### 2. Translate Legacy Concepts

Use the mapping in [references/scheduler-upgrade-cheatsheet.md](references/scheduler-upgrade-cheatsheet.md) when explaining changes.

Apply this mental model:

- Legacy `executionMode: "yolo_loop"` maps to reliable runtime with `executionMode: "issue_run"` and `executionStrategy: "loop"`.
- Legacy single-session continuity often becomes two concepts:
  - `targetSessionId` for delivery/routing
  - `scheduleSessionId` for continuity/appends
- `deliveryPolicy: "session-bound"` is the safe default for old in-app/session-following behavior.
- `deliveryPolicy: "thread-bound"` requires an explicit `deliveryRoute`.
- `schedule_get` does not exist; use `schedule_list({ scheduleId, includePrompt: true })` instead.

### 3. Separate Deterministic Repairs From Product Decisions

Treat the following as deterministic repair candidates:

- missing or stale `targetSessionId`
- missing or stale `scheduleSessionId`
- missing owner metadata that can be inferred from a live bound session
- disconnected delivery/session references that `schedule_repair` can rebind or disable safely

Treat the following as user-decision upgrades:

- changing timing or cadence
- switching between `session-bound` and `thread-bound`
- choosing `executionContextMode`
- changing persona or prompt behavior
- converting a legacy schedule to reply directly in the real chat instead of using an internal worker

Do not silently change semantics when the schedule is still functional.

### 4. Propose an Upgrade Plan

Summarize findings in three buckets:

- auto-normalized by Vesper already
- safe deterministic repairs available now
- choices that need user approval

For each schedule, explain:

- what is wrong or outdated
- whether Vesper already compensated for it
- whether `schedule_repair` can fix it
- whether `schedule_update` is needed for an intentional behavior change

### 5. Apply Repairs Carefully

If the user approves, apply in this order:

1. Run `schedule_repair(apply=true)` for deterministic repairable issues.
2. Run targeted `schedule_update` calls for approved semantic changes.
3. Avoid broad rewrites when only one or two fields need adjustment.

Prefer narrow, explicit changes. Preserve prompt text, persona, and timing unless the user asked to change them or the current configuration is invalid.

## Mutation Policy

Follow these rules every time:

- Never mutate schedules before inspecting with `schedule_list`.
- Default `schedule_repair` to audit-only mode first.
- Never use docs alone as evidence that a migration is complete; inspect the actual schedule records.
- Do not clear `targetSessionId`, `scheduleSessionId`, or `deliveryRoute` unless the user approved the new routing model.
- If a schedule is `thread-bound` and lacks `deliveryRoute`, either repair it to a valid explicit route or recommend switching back to `session-bound`.
- If multiple messaging bindings make owner inference ambiguous, stop and surface the ambiguity instead of guessing.

## Verification

After any approved repair or upgrade:

1. Re-run `schedule_list` for the touched schedules.
2. Re-run `schedule_repair(apply=false)` to confirm no critical repair issues remain.
3. Run `schedule_forecast` if timing, cadence, timezone, or enablement changed.
4. Summarize the before/after state in plain English.

Confirm at least:

- runtime contract is coherent
- delivery routing is explicit enough for the chosen policy
- continuity session still exists
- next run windows look plausible

## Escalation Rules

Pause and ask for direction when:

- a schedule is healthy but uses an older concept that still behaves correctly
- a repair would change where messages appear
- a schedule can be rebound to multiple candidate sessions
- a thread-bound route exists but may point to the wrong topic/thread
- the user appears to want product redesign, not migration

## Reference

Load [references/scheduler-upgrade-cheatsheet.md](references/scheduler-upgrade-cheatsheet.md) when explaining old-to-new field mapping or deciding between `schedule_repair` and `schedule_update`.
