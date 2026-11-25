---
name: generate-resource-plan
description: "Generates a resource allocation plan (resource-plan.md) for Phase 2 —
  Planning, based on project-plan.md and team-list.md. Produces a role-by-phase FTE
  matrix with person-month calculations, rates (when available), external resources
  section, and a phase-load summary. Covers task #8 of the project management agent.
  Mode B: agent prepares draft, PM reviews and approves. Required input for
  generate-budget (#9).
  Triggers RU: «составь ресурсный план», «распредели ресурсы по проекту», «кто и когда
  работает», «ресурсный план проекта», «загрузка команды по фазам», «generate-resource-plan».
  Triggers EN: 'generate resource plan', 'resource allocation plan', 'create resource plan',
  'team allocation by phase', 'staffing plan', 'who works when'."
---

# Skill: generate-resource-plan

Generates a resource allocation plan for an IT project during the planning phase (Phase 2).
Reads the project plan (phase durations) and team list (roles, FTE, rates), builds a
role-by-phase FTE matrix with person-month totals and cost estimates (when rates are
available). Output: `resource-plan.md` — the primary input for generate-budget. Mode B:
agent prepares draft, PM reviews.

---

## Triggers

**Russian:** «составь ресурсный план», «распредели ресурсы по проекту», «кто и когда работает», «ресурсный план проекта», «загрузка команды по фазам», «ресурсы на проект»
**English:** "generate resource plan", "resource allocation plan", "create resource plan", "team allocation by phase", "staffing plan", "who works when", "resource plan"

---

## Language Detection

Determine the language of the user's request:
- If the request is in Russian → use templates with the `-ru` suffix, respond in Russian
- Otherwise → use templates with the `-en` suffix, respond in English

---

## Input

| Data | Required | Source |
|------|:--------:|--------|
| Project plan | yes | `02-planning/project-plan.md` |
| Team list | yes | `input/team-list.md` |
| Project charter | no | `01-initiation/project-charter.md` — project name, PM, GTM scope |
| Preliminary estimate | no | `01-initiation/preliminary-estimate.xlsx` — aggregated team costs by phase (fallback) |
| Constraints | no | `input/constraints.md` — resource or headcount constraints |

---

## Output

| File | Project path | Format |
|------|-------------|--------|
| `resource-plan.md` | `02-planning/` | .md |

File structure — 4 sections (Internal Team, Allocation Matrix, External Resources, Summary)
— defined in `templates/resource-plan-{lang}.md`.

---

## Instructions

### Step 1 — Check Dependencies

**Guard-rail — check request type.**
If the request contains language related to budget calculation, cost totals, contingency
reserves, financial planning, or total project cost — even alongside a resource plan
request — respond:
"generate-resource-plan creates a role-by-phase allocation matrix, not a budget.
For the project budget use generate-budget (task #9) — it reads resource-plan.md
and produces project-budget.xlsx. Run generate-resource-plan first, then generate-budget."
Do not start the workflow.

If the request is about task decomposition, sprint planning, or WBS → respond:
"generate-resource-plan shows who is allocated at what FTE per phase, not a task breakdown.
For task-level planning use generate-project-plan."
Do not start the workflow.

Check for required files:
1. `02-planning/project-plan.md`
2. `input/team-list.md`

**If project-plan.md is not found:**
Stop. Respond:
"A project plan is required to generate the resource plan. Run generate-project-plan
(task #7) first — it defines phases, durations, and key activities that drive
resource allocation."

**If team-list.md is not found:**
Stop. Respond:
"A team list is required to generate the resource plan. Create input/team-list.md with
roles, team members, and FTE allocation per phase, then run this skill again."

**If both files are found:** proceed to Step 2.

---

### Step 2 — Extract Phase Data from project-plan.md

Read `02-planning/project-plan.md` and extract:

- List of phases (Phase 1 through Phase 6, or as defined in the plan)
- Duration of each phase (in weeks; convert to months: weeks / 4.3, round to 1 decimal)
- Key activities per phase — used to infer which roles are active
- Project name and PM (if present) — also check project-charter.md

Record the phase list and durations. This is the column structure for the allocation matrix.

---

### Step 3 — Extract Team Data from team-list.md

Read `input/team-list.md` and extract:

**Internal team (штатные / permanent):**
- Role, name, grade
- FTE allocation: use the percentage from team-list.md as the base allocation
  - If allocation is given as a single number for the whole project (e.g., "80%") →
    apply it uniformly across all phases where the role is active
  - If allocation varies by phase or period → record phase-specific values
- Rates:
  - If rates are given ($/month or ₽/month) → record for cost calculation
  - If rates are "—" or marked as штат/operational budget → record as "—",
    add note in assumptions: "Internal team salaries are included in the company's
    operational budget and are not reflected in the project budget."

**External resources (contractors, outsource):**
- Role, vendor/name, engagement period, budget (fixed sum), scope of work
- Map the engagement period to phases from Step 2

**From constraints.md (if available):**
- Any headcount limits, FTE caps, or team availability constraints → record in Assumptions.

---

### Step 4 — Build the Allocation Matrix

Construct the FTE allocation matrix: rows = roles, columns = phases.

For each role × phase combination:
1. Is the role active in this phase?
   - If project-plan.md or team-list.md explicitly states the phase → use it
   - If not explicitly stated: use the general project FTE from team-list.md, assume the
     role is active in phases where the key activities match the role's competency
   - PM / Project Manager is active across all phases at their stated FTE
2. Record FTE % per phase (e.g., 0.5 = 50%, 1.0 = 100%, 0 = not active)
3. Calculate person-months: `p-m = FTE × phase_duration_months`
   - Round to 1 decimal place
4. If rate is available: calculate `phase_cost = p-m × rate`

Row totals: sum of person-months across all phases for each role.
Column totals: sum of person-months across all roles for each phase.

---

### Step 5 — Compile Assumptions and Risk Notes

Write the Assumptions section (minimum 3 items):
1. Data source for phase durations (project-plan.md, which phase structure was used)
2. FTE allocation logic (uniform vs phase-specific; basis for inference if used)
3. Rate handling: "Rates taken from team-list.md" OR "Internal team on operational budget
   — cost columns left blank. External resources: contract amounts as stated in team-list.md"
4. Any phase-allocation assumptions made by the agent (e.g., "QA assumed active in
   phases 3–5 based on testing activities in project-plan.md")
5. If preliminary-estimate.xlsx was used as a fallback for aggregated team cost → state it

**Resource risks (if detected):**
- Any role allocated at 100% across multiple overlapping phases → flag as overallocation risk
- Any role that is the only resource in a critical competency area (e.g., sole developer,
  sole designer) and is heavily loaded (≥80% FTE) across all phases → flag as
  single-point-of-failure risk
- Critical path roles (e.g., sole developer) allocated below 50% on key phases → flag
- External resource engagement not aligned with phase dates → flag

---

### Step 6 — Create resource-plan.md and Save

Follow the schema in `templates/resource-plan-{lang}.md`:

1. Create `resource-plan.md` in `{project}/02-planning/`.
2. Show in chat:
   - Confirmation: "resource-plan.md saved to 02-planning/."
   - Allocation matrix as a markdown table (Section 2 summary).
   - List of assumptions.
   - Resource risk flags (if any).
   - Next step: "Resource plan is ready. Review FTE allocations and correct if needed.
     Once approved, use generate-budget (task #9) — it reads this file to calculate
     the project budget."
3. Write to `logs/log.md`: date, skill, file created, total person-months, rate coverage
   (e.g., "rates available for 2/5 roles").
4. Update `project-state.md`: artifact `resource-plan.md` status → "draft".

---

## Templates

| File | Purpose |
|------|---------|
| `templates/resource-plan-ru.md` | Artifact schema (RU) |
| `templates/resource-plan-en.md` | Artifact schema (EN) |

---

## Dependencies

**Reads:**
- `02-planning/project-plan.md` — phases, durations, key activities
- `input/team-list.md` — roles, FTE allocation, rates, external resources
- `01-initiation/project-charter.md` — project name, PM, GTM scope
- `01-initiation/preliminary-estimate.xlsx` — aggregated team costs (optional fallback)
- `input/constraints.md` — resource constraints (optional)

**Passes data to:**
- `generate-budget` (#9) — FTE, rates, person-months per phase → cost calculation

---

## Constraints

- Mode B: resource plan is a draft for PM review, not a final document
- Does not build a task schedule or WBS — use generate-project-plan
- Does not calculate the project budget — use generate-budget
- FTE values are taken from team-list.md; the skill does not validate them against
  calendar capacity or workday availability
- Internal team rates marked "—" are left blank in cost columns — this is intentional
- Operates on one project per invocation
- If project-plan.md is unavailable — skill does not run; no fallback
