---
name: generate-estimate
description: "Generates a preliminary timeline and budget estimate for an IT project
  (Phase 1 — Initiation). Reads available project files (client questionnaire, project
  charter, constraints, team list), applies analogy-based estimation using built-in
  agent knowledge of typical IT projects, and produces a three-scenario (optimistic /
  realistic / pessimistic) preliminary-estimate.xlsx artifact. Covers task #4 of the
  project management agent. Mode B: agent prepares draft, PM reviews and corrects.
  Triggers RU: «сформируй оценку сроков», «подготовь предварительную оценку бюджета»,
  «оцени сроки проекта», «сделай оценку по аналогам», «предварительная оценка».
  Triggers EN: 'generate estimate', 'preliminary estimate', 'estimate timeline and
  budget', 'create project estimate', 'ballpark estimate'."
---

# Skill: generate-estimate

Generates a preliminary timeline and budget estimate for an IT project at the Initiation phase (Phase 1). Uses analogy-based estimation with built-in knowledge of typical IT project benchmarks. Output: `preliminary-estimate.xlsx` with three scenarios (optimistic / realistic / pessimistic). Mode B: agent prepares draft, PM reviews and adjusts.

---

## Triggers

**Russian:** «сформируй оценку сроков», «подготовь предварительную оценку», «оцени сроки проекта», «сделай оценку по аналогам», «нужна предварительная оценка», «оцени бюджет», «ballpark-оценка»
**English:** "generate estimate", "preliminary estimate", "estimate timeline and budget", "create project estimate", "ballpark estimate", "rough estimate"

---

## Language Detection

Determine the language of the user's request:
- If the request is in Russian → use templates with the `-ru` suffix
- Otherwise → use templates with the `-en` suffix
- All output (headings, labels, agent messages) must match the detected language.

---

## Input

| Data | Required | Source | Notes |
|------|:--------:|--------|-------|
| Project name and type | yes | CLAUDE.md, project-charter.md, or command | Types: MVP / redesign / integration / GTM / feature set / internal tool |
| Scope / key deliverables | yes | questionnaire-client.md, project-charter.md, or command | Used to determine phases |
| Constraints (budget, deadline) | no | constraints.md or command | If present — adjust analogue accordingly |
| Team composition | no | team-list.md or command | Roles and headcount. If absent — agent derives from analogue |
| Role rates | no | CLAUDE.md or command | If not provided — use rates from `estimate-analogues.md` |
| GTM in scope | no | project-charter.md, questionnaire-client.md | Affects presence of Budget Section C |

---

## Output

| File | Project path | Format |
|------|--------------|--------|
| `preliminary-estimate.xlsx` | `{project}/01-initiation/` | .xlsx |

File structure — 3 sheets (Summary, Timeline, Budget) — described in `templates/preliminary-estimate-{lang}.md`.

---

## Instructions

### Step 1 — Collect Input Data

**Guard-rail — check for out-of-scope requests first.**
If the request asks for task-level detail — WBS, man-hours per task, work breakdown, hour-by-hour schedule, or detailed task list — respond:
"generate-estimate creates a phase-level preliminary estimate using the analogy method. For task-level breakdown and man-hour estimates, use generate-project-plan after this estimate is approved by the PM."
Do not start the estimate workflow. Do not ask for input data.

**Check for inline data in the user's command.**
Before checking files, scan the command for explicitly provided fields:
- Project type → present / absent
- Main deliverables → present / absent
- Constraints (deadline, budget ceiling) → present / absent
- Team composition → present / absent

If project type AND main deliverables are both present in the command — proceed directly to Step 2 using that data. Ask only for fields that are genuinely absent.

**Check for files** (supplement or replace inline data):
1. `01-initiation/questionnaire-client.md`
2. `01-initiation/project-charter.md`
3. `input/constraints.md`
4. `input/team-list.md`

Extract from available files:
- Project type and primary goals
- Key deliverables and scope
- Known constraints (deadline, budget ceiling)
- Team composition (roles, FTE)
- Whether GTM is in scope

**If no files exist AND inline data is incomplete** — ask only for missing fields in one block:
```
I need a few more details to build the estimate:
[list only the fields that are absent from the command and files]
```
Wait for response. Do not proceed without at least the project type.

---

### Step 2 — Identify Project Type and Apply Analogue

1. Read `templates/estimate-analogues.md`.
2. Match the project to the closest type in the analogues table.
3. Retrieve baseline ranges: duration and rates.
4. If project data includes explicit constraints — adjust:
   - Hard deadline → optimistic scenario must not exceed it.
   - Hard budget ceiling → record in assumptions. Calculate the estimate using the standard analogue (do not adjust numbers to fit the ceiling). If the realistic scenario total exceeds the ceiling, add a risk flag to the Summary sheet and show in chat: "Warning: Realistic scenario [$X] exceeds the stated budget ceiling [$Y]. Recommend reviewing scope, phasing delivery, or adjusting team composition — consult PM before proceeding." Do not silently reduce the estimate to fit the ceiling.
5. Determine whether GTM (Phase 5) is in scope. If not — zero out Budget Section C.

---

### Step 3 — Build Phase Timeline (Sheet 2: Timeline)

For each phase (1–6), determine duration in weeks across three scenarios.
Baseline: analogue from Step 2. Adjust based on project data:

| Factor | Adjustment |
|--------|-----------|
| Team smaller than analogue | +10–20% to duration |
| Team larger than analogue | −5–10% to duration |
| Hard constraints | Set realistic = constraint, pessimistic → risk flag |
| Complex external interface / legacy | +20–30% to development phase |
| No prototyping in scope | Zero out Phase 3 |

Record key deliverables for each phase from the project scope.

---

### Step 4 — Calculate Budget (Sheet 3: Budget)

**Section A: Team**

1. Determine team composition (from team-list.md or analogue).
2. For each role: FTE × scenario duration × rate.
3. Rates: from project data → if absent, from `estimate-analogues.md`.
4. Apply rate ranges by scenario: optimistic → opt rate; realistic → real rate; pessimistic → pest rate.

**Section B: Infrastructure**

1. Identify project type → take range from `estimate-analogues.md`.
2. Calculate: monthly item × number of months in scenario + one-time costs.
3. If specific tools are known (from questionnaire-client.md) — use those instead.

**Section C: Marketing/GTM**

1. Include only if GTM is in scope.
2. Take range from `estimate-analogues.md` based on project size.
3. If GTM is not in scope — zero out rows and add note.

---

### Step 5 — Fill Sheet 1 (Summary)

1. Enter header data: project, PM, date, project type.
2. Record assumptions (minimum 3):
   - Estimation basis (analogy method)
   - Team composition (from data or analogue)
   - Constraints, if any
3. Fill in the scenario summary table.
4. Add a one-line agent recommendation — which scenario to treat as baseline and why.

---

### Step 6 — Generate xlsx File and Save

1. Use the xlsx skill to create `preliminary-estimate.xlsx` following the template structure.
2. Save to `{project}/01-initiation/preliminary-estimate.xlsx`.
3. Show in chat:
   - What was created: "Estimate saved as preliminary-estimate.xlsx in 01-initiation/."
   - Summary scenario table as a chat table.
   - List of assumptions.
   - Next step: "Estimate ready. Recommended: verify rates and team composition, then pass data to generate-budget (detailed budget)."
4. Log to `logs/log.md`: date, skill, created file, project type, baseline scenario.

---

## Templates

| File | Purpose |
|------|---------|
| `templates/preliminary-estimate-ru.md` | xlsx artifact schema (RU) |
| `templates/preliminary-estimate-en.md` | xlsx artifact schema (EN) |
| `templates/estimate-analogues.md` | Analogue benchmarks and rate reference |

---

## Dependencies

**Reads:**
- `01-initiation/questionnaire-client.md` — scope, constraints, project type
- `01-initiation/project-charter.md` — deliverables, goals, constraints
- `input/constraints.md` — hard constraints on deadline / budget
- `input/team-list.md` — team composition and roles

**Passes data to:**
- `generate-budget` — detailed budget is built on top of this estimate
- `generate-resource-plan` — resource allocation across phases

**Calls:**
- `xlsx skill` — for generating the .xlsx file

---

## Constraints

- Mode B: estimate is a draft for the PM — not a final document
- Method is analogy-based, not bottom-up; ±30–50% accuracy is normal at initiation stage
- Does not build a detailed WBS or task schedule
- Does not account for holidays, vacations, part-time availability — unless specified in constraints
- Does not auto-update after scope changes — recalculation is triggered manually
- Handles one project per invocation

---

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-04-06 | 1.0 | Skill created. Analogy method, 3 scenarios, 3 budget categories. Artifact templates + analogues reference. |
| 2026-04-06 | 1.1 | Post-eval fixes (2/6 → 6/6 expected): added inline-data guard in Step 1 (scan command before asking); added WBS out-of-scope guard-rail in Step 1; clarified budget ceiling behavior in Step 2 (flag risk, never silently compress). |
