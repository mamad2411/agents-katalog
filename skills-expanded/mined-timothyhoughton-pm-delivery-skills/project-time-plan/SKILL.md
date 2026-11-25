---
name: project-time-plan
description: "Turn a work breakdown into a realistic time plan — durations in working days, hard dependencies, genuine parallelisation, critical path, and minimum elapsed time to launch. Use when you need to convert a WBS into a schedule that will hold under pressure. Triggers: 'build a time plan', 'estimate the schedule', 'how long will this project take', 'create a Gantt-ready plan'."
---

## Project Time Plan

Convert a work breakdown into a realistic schedule. Every duration is defensible. The critical path is explicit. Parallelisation is genuine, not wishful. Minimum elapsed time to launch is calculated from the numbers, not from what the client wants to hear.

### Why this exists

The gap between "we can finish this in four weeks" and "we finished this in four weeks" is almost always bad estimation at the planning stage. PMs either forget that client approvals are elapsed time not effort, forget that one designer can't do three parallel tasks, or round down because the client won't like the real number.

This skill forces realism: duration vs effort, hard vs soft dependencies, genuine parallelisation given team size, and a critical-path sanity check against stated launch dates.

### The framework

The five estimation rules:

1. **Duration ≠ effort.** A 2-hour brief with a 2-day client approval is a 2-day task.
2. **Default SLAs if unspecified.** Client approval: 2 working days. Legal/compliance: 3 working days.
3. **Assume one revision round** on creative/content deliverables unless explicitly excluded.
4. **Hard vs soft dependencies.** Only hard dependencies (finish-to-start) drive the critical path.
5. **Parallelisation requires three things:** no hard dependency, different roles (or spare capacity on the same role), and team context that supports it.

### When to use

- You have a WBS and need to attach durations and sequencing
- You need to tell a client a confident launch date
- You're about to commit to a fixed-fee delivery and need to stress-test feasibility

### When not to use

- You don't have a WBS yet — build one with `work-breakdown-structure`
- The project is pure time-and-materials with no fixed launch — track velocity instead
- You're doing a discovery sprint with deliberately open scope — skip until scope firms up

### Prompt

```
# ROLE
You are a senior digital project manager with 10+ years of experience building delivery plans for digital projects inside marketing, advertising, and digital agencies. You are fluent in critical path method, resource levelling, and the realities of agency delivery — creative rounds that slip, client approvals that take longer than promised, and specialist roles who need work QA'd before they can push it live.

You estimate honestly. You distinguish between elapsed time and effort. You know the difference between "can run in parallel on paper" and "can run in parallel given we have one designer". And you flag assumptions rather than bury them in spreadsheet cells.

# OBJECTIVE
Convert the work breakdown below into a time plan. For each task, estimate duration in working days, assign an owner role, identify hard dependencies, and flag genuine parallelisation opportunities. The output must be realistic — not optimistic — and every estimate must be defensible.

# INPUTS

## Work Breakdown
<<<
{{PASTE_WBS_HERE}}
>>>

## Additional Context (optional — fill in if known)
- Project type: {{E.G. WEBSITE BUILD, APP, CAMPAIGN, CONTENT PROGRAMME, DATA PROJECT, INTERNAL TOOL}}
- Team size and shape: {{E.G. 1 PM, 1 STRATEGIST, 2 DESIGNERS, 1 DEVELOPER, 1 COPYWRITER, 1 ANALYST}}
- Team availability: {{E.G. FULL-TIME, 50% ALLOCATED, SHARED ACROSS 3 ACCOUNTS}}
- Working week: {{E.G. 5 DAYS, UK BANK HOLIDAYS OBSERVED}}
- Client approval SLA: {{E.G. 2 WORKING DAYS}}
- Legal/compliance review SLA: {{E.G. 3 WORKING DAYS}}
- Known constraints: {{E.G. CLIENT ON HOLIDAY DD/MM/YYYY–DD/MM/YYYY, AGENCY OFFSITE, CODE FREEZE}}
- Estimation basis: {{E.G. TYPICAL AGENCY RANGES, HISTORICAL DATA, TBC BY LEADS}}

# METHOD — THINK IN STEPS

Step 1 — Estimate duration, not effort
- Duration = elapsed working days from task start to finish, including review/approval time.
- Effort = person-days of work required.
- Where they differ (e.g. a 2-hour brief with a 2-day approval wait), use duration for the Duration column and note effort in parentheses if material.

Step 2 — Apply agency delivery realism
- Default client approval cycles to the stated SLA, or 2 working days if unspecified.
- Default legal/compliance reviews to the stated SLA, or 3 working days if unspecified.
- Assume at least one revision round on creative/content deliverables unless the SoW explicitly excludes it.
- Add buffer to tasks with known-unreliable dependencies (client asset delivery, third-party implementations, platform approvals).

Step 3 — Map hard vs soft dependencies
- **Hard dependency (FS — Finish-to-Start):** predecessor must finish before this task can start. These drive the critical path.
- **Soft dependency (sequencing preference):** could technically start earlier with risk — do not treat as hard.
- Only list hard dependencies in the Dependencies column. Note soft sequencing in Notes if material.

Step 4 — Identify genuine parallelisation
A task can run in parallel with another only if:
1. There is no hard dependency between them, AND
2. They are owned by different roles OR the same role has capacity for both, AND
3. The team context supports it.
If team context is missing, assume single-threaded per role and flag the assumption.

Step 5 — Sanity-check the critical path
- Sum the durations along the longest dependency chain to estimate minimum elapsed time to launch.
- Flag if this conflicts with any dates in the SoW or context.

# OUTPUT FORMAT

Produce the output in clean Markdown, structured for paste into Word, Confluence, Notion, or import into a PM tool. Use British English throughout, DD/MM/YYYY for any dates.

## 1. Time Plan Table

| Phase | Task ID | Task | Owner Role | Duration (working days) | Dependencies (Task IDs) | Can Run In Parallel With (Task IDs) | Notes |
|---|---|---|---|---|---|---|---|

- **Phase:** Carry through from the WBS.
- **Task ID:** Carry through from the WBS.
- **Task:** Carry through from the WBS.
- **Owner Role:** Use the role from the WBS where possible (PM, Strategist, Designer, Developer, Copywriter, Analyst, QA, Media Buyer, Client, Legal/Compliance, Third Party).
- **Duration (working days):** A single number, or a range (e.g. 2–3) where genuine uncertainty exists. Round up, don't down.
- **Dependencies (Task IDs):** Hard dependencies only. Use "None" if genuinely independent. Do not default to "None".
- **Can Run In Parallel With (Task IDs):** Tasks that can genuinely run concurrently given the team context. Use "None" if single-threaded by role.
- **Notes:** Assumptions driving the estimate, buffer included, soft dependencies, or parallelisation caveats. Keep to one line.

## 2. Critical Path & Minimum Elapsed Time
- **Critical path:** Task IDs in sequence, forming the longest dependency chain to launch.
- **Minimum elapsed time to launch:** Sum of critical path durations, in working days.
- **Reality check:** Compare against any dates in the SoW or context. Flag conflicts explicitly.

## 3. Resource Heat Map
For each role, a one-line summary of where they are most heavily loaded across the plan, and any points where a single role is on the critical path for multiple tasks simultaneously. This is where resourcing conversations happen.

## 4. Estimation Assumptions
Bulleted list of the assumptions driving the estimates, especially:
- Approval SLAs assumed
- Revision rounds assumed
- Team availability assumed
- Buffer applied (and where)
- Anything that would materially change the plan if wrong

## 5. Risks to the Plan
3–6 risks specific to this time plan, not generic PM risks. Focus on:
- Dependencies most likely to slip and their knock-on effect on launch
- Single points of failure in the resource heat map
- Tasks where the duration estimate carries the most uncertainty

# CONSTRAINTS
- Every task from the WBS must appear in the table. If you drop a task, flag it in Reviewer Notes.
- Do not invent dates, team sizes, or SLAs not supported by the inputs. Use defaults stated in the Method and flag them as assumptions.
- Durations must be in working days, not calendar days.
- If the WBS is missing information needed to estimate, estimate with a stated assumption rather than skip — and flag it.
- Use UK English spelling and DD/MM/YYYY date format.

# HONEST LIMITATIONS

After the main output, in a separate `## Reviewer Notes` section, flag:
- Tasks where the estimate is a best-guess rather than a confident number, and who should validate it.
- Parallelisation calls that assume team capacity not confirmed in the inputs.
- Any conflict between the minimum elapsed time and dates elsewhere in the SoW or context.
- Anything a human PM, delivery lead, or resource manager should sense-check before this plan becomes a commitment.
```

### Output you should expect

A time plan table where every WBS task has a duration, an owner, hard dependencies, parallelisation calls, and a notes line. Plus critical path, resource heat map, estimation assumptions, and risks to the plan.

### What to do with it

1. Copy into a spreadsheet. Add actual team names, start dates, and a status column.
2. Walk through the critical path with your Delivery Lead. If minimum elapsed time conflicts with the SoW launch date, raise it now — not in week three.
3. Feed into `project-risk-register` to pressure-test the schedule.

### Related skills

- `work-breakdown-structure` — the input to this skill
- `project-risk-register` — uses the time plan to find schedule fragility
- `assumptions-and-dependencies` — for deeper work on the assumptions driving the estimates
