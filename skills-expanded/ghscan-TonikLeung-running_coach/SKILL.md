---
name: plan-running-week
description: Build an adaptive one-week running plan after reading athlete context, training, recovery, Intervals.icu load, and calendar conflicts, then optionally write the reviewed plan to Intervals.icu only after explicit human confirmation. Use for requests such as “根据最近训练安排下周训练”, “给我下周跑步计划”, “未来一周怎么跑”, “确认写入计划”, or requests for a concrete day-by-day running week and approved Calendar synchronization.
---

# Plan Running Week

Generate plans through the project Running Coach; never create a template directly from a race goal and never inspect REST endpoints or raw Intervals.icu JSON.

Codex uses native Running MCP reads and the existing `WeeklyPlanner`
through the read-only helper below. Numerical planning remains in program code.

## Runtime policy

```json
{"tools":["get_training_summary","get_training_history","get_wellness","get_training_load","get_training_calendar","get_recovery_summary"],"first_tools":["get_training_summary","get_training_calendar"],"required_tools":["get_training_summary","get_training_calendar"]}
```

## Tool adapter

From the project working directory, invoke:

Read current evidence before planning:

The summary and Calendar are independent required reads and may be requested in one native tool-call batch. Complete both successfully before building the draft; supplementary tools are not a default batch.

1. `get_training_summary({"weeks": 12})` for 7/28/42-day state, complete weeks, Long Runs, and 12-week trend.
2. `get_training_calendar({"days_before": 1, "days_after": 14})` for conflicts and existing workouts.
3. Add history, wellness, load, or recovery summary only when the primary summary leaves a specific gap. Do not repeat information already present.

The application supplies a draft from the existing deterministic planner after successful summary and Calendar reads. Explain that exact draft; do not silently replace its dates, distances, targets, or Calendar changes with model-generated values.

For Codex local mode, call the two native MCP tools above, then pass their complete
success envelopes as `{"summary": SUMMARY_ENVELOPE, "calendar": CALENDAR_ENVELOPE}`
on stdin to `.venv/bin/python scripts/preview_week.py`, or supply private envelope
files via `--summary` and `--calendar`. This helper invokes the same planner and
reads local Athlete Context; it never queries APIs, stages approvals or writes.
Do not invent omitted/truncated evidence fields. Explain the exact returned draft.
The helper does not stage or approve changes. Only after an explicit write request,
stage the complete draft with `running-calendar-approval stage PRIVATE_PLAN_FILE`.
The user must run `running-calendar-approval approve APPROVAL_ID` in their own
interactive terminal, review the exact snapshot and type its exact confirmation.
Codex must never run approve, simulate human input or edit approval files.
Execute only persisted approved operations through native MCP; never invent IDs.

Do not generate a plan if the summary or calendar call fails. Do not call activity streams.

## Workflow

1. Read Athlete Context: race, race date, goal, weekly availability, preferred Long Run day, injury/current pain, strength training, and preferences. Reuse known values. List missing context and lower confidence; do not invent it.
2. Establish current status from six weeks and the 12-week trend. Compare complete weeks only.
3. Combine load and recovery. Missing HRV, resting HR, or sleep is uncertainty—not normal recovery.
4. Inspect Calendar. Never silently stack a generated workout on an existing plan.
5. Select Base, Build, Specific, Peak, Taper, or Recovery. If race context is missing, label phase provisional and keep confidence low.
6. Choose one or two cycle focuses. Never materially increase weekly volume, Long Run, Threshold, and VO2max together.
7. Generate seven explicit days with workout type, duration/distance, intensity/RPE target, and purpose.
8. Return weekly mileage, quality-session count, Long Run, key workout, change versus previous complete week, rationale, conflicts, and adaptive rules.
9. When explicitly asked to write, stage an immutable Calendar preview and show all changes. Do not call a write tool in this turn.
10. Execute only after the user reviews the snapshot and enters the exact `确认写入 <approval_id>` phrase in the human-operated approval CLI, then confirms that approval to Codex.
11. After writes, call `get_training_calendar` again and verify created event IDs in the returned Calendar.

## Write tools and approval

- `create_workout({"approval_id": "...", "operation_id": "..."})`: create one approved workout after a same-day conflict check.
- `update_workout({"approval_id": "...", "operation_id": "..."})`: update only the event and payload stored in an approved snapshot.
- `delete_workout({"approval_id": "...", "operation_id": "..."})`: delete only the event stored in an approved snapshot.

Never pass arbitrary workout fields to write tools. The immutable approval snapshot is the source of the write payload. Never interpret “好的”, “可以”, or a new planning request as approval. Approval expires after 24 hours.

## Planning rules

- Prefer long-term consistency over maximum short-term stimulus.
- Preserve Intervals.icu classifications. If Threshold versus VO2max is unavailable, use a conservative generic quality label rather than pretending certainty.
- Reduce stimulus when multiple recovery signals worsen, Easy performance declines, subjective fatigue is high, current pain exists, or load evidence is concerning.
- Sparse recovery data alone lowers confidence and prevents aggressive progression.
- A good state does not justify increasing every variable.
- Never diagnose illness, injury, or overtraining.
- For chest pain, fainting, severe shortness of breath, abnormal rhythm, or persistent acute pain, stop planning and recommend appropriate professional medical evaluation.

## Output

Lead with the plan's meaning, then provide:

1. Phase and confidence
2. Cycle focus
3. Daily plan
4. Weekly mileage, quality sessions, Long Run, and key workout
5. Change from the previous complete week
6. Why this load fits current training and recovery
7. Adaptive rules and data limitations

For each running day, give a concrete default. Do not answer only “根据身体状态决定”; put adjustment conditions after the default prescription.

## Failure handling

- On missing athlete context, produce only a conservative provisional plan when training and calendar data are available; list exactly what is missing.
- On sparse wellness, avoid claiming recovery is good and do not increase quality density.
- On an empty Calendar, state that no existing planned workouts were found.
- On Calendar conflicts, let the existing item occupy that day and do not generate a second workout. Mark weekly mileage partial when the existing item has no distance.
- On empty history, report insufficient baseline and avoid a race-specific plan.
- On partial write failure, list successful and failed dates/types separately. Continue untouched operations once, do not retry the failed operation, and never roll back successful creates automatically.
- If post-write Calendar reread fails or an event ID is absent, report it as unverified rather than assuming success.
