---
name: generate-budget
description: "Generates a detailed project budget (project-budget.xlsx) for Phase 2 —
  Planning, based on preliminary-estimate.xlsx and resource-plan.md. Produces a single
  baseline scenario structured by project phases and cost categories (team, infrastructure,
  GTM), with a contingency reserve as a separate line item. Covers task #9 of the project
  management agent. Mode B: agent prepares draft, PM reviews and approves.
  Triggers RU: «сформируй бюджет проекта», «подготовь детальный бюджет», «сделай бюджет
  по фазам», «бюджет проекта», «детализируй бюджет».
  Triggers EN: 'generate project budget', 'create budget', 'project budget',
  'detailed budget', 'budget by phase', 'budget breakdown'."
---

# Skill: generate-budget

Generates a detailed IT project budget during the planning phase (Phase 2). Reads the
preliminary estimate (preliminary-estimate.xlsx) and resource plan (resource-plan.md),
builds a line-item budget by phase and cost category. Output: `project-budget.xlsx` —
one baseline scenario with a contingency reserve. Mode B: agent prepares draft, PM reviews.

---

## Triggers

**Russian:** «сформируй бюджет проекта», «подготовь детальный бюджет», «сделай бюджет по фазам», «бюджет проекта», «детализируй бюджет»
**English:** "generate project budget", "create budget", "project budget", "detailed budget", "budget by phase", "budget breakdown"

---

## Language Detection

Determine the language of the user's request:
- If the request is in Russian → use templates with the `-ru` suffix, respond in Russian
- Otherwise → use templates with the `-en` suffix, respond in English

---

## Input

| Data | Required | Source |
|------|:--------:|--------|
| Preliminary estimate | yes | `01-initiation/preliminary-estimate.xlsx` |
| Resource plan | yes | `02-planning/resource-plan.md` |
| Project charter | no | `01-initiation/project-charter.md` |
| Hard constraints | no | `input/constraints.md` |
| Risk register | no | `01-initiation/risk-register.md` — for reserve calibration |

---

## Output

| File | Project path | Format |
|------|-------------|--------|
| `project-budget.xlsx` | `02-planning/` | .xlsx |

File structure — 3 sheets (Summary, Budget Detail, Resource Detail) — defined in
`templates/project-budget-{lang}.md`.

---

## Instructions

### Step 1 — Check Dependencies

**Guard-rail — check request type.**
If the request contains: WBS, task decomposition, man-hours per task, work breakdown by
assignee — respond:
"generate-budget produces a line-item budget by phase and cost category, not a detailed
WBS. For task decomposition use generate-project-plan — it builds a plan with tasks,
timelines, and assignees. Once the plan is approved, generate-budget will calculate the
financial side based on the resource plan."
Do not start the workflow. Do not check for files.

Check for required files:
1. `01-initiation/preliminary-estimate.xlsx`
2. `02-planning/resource-plan.md`

**If preliminary-estimate.xlsx is not found:**
Stop. Respond:
"A preliminary estimate is required to generate the budget. Run the generate-estimate
skill (task #4) — it will create preliminary-estimate.xlsx with baseline timeline and
cost data."

**If resource-plan.md is not found:**
Stop. Respond:
"A resource plan is required to generate the budget. Run the generate-resource-plan
skill (task #8) — it will create resource-plan.md with team composition, roles, and
rates by phase."

**If both files are found:** proceed to Step 2.

---

### Step 2 — Extract Data from Sources

**From preliminary-estimate.xlsx (realistic scenario):**
- Duration of each phase (weeks or months)
- Total costs by category (team, infrastructure, GTM)
- Assumptions recorded in the estimate
- Risk flags (if budget exceeds constraints)

**From resource-plan.md:**
- Team composition: roles, FTE allocation per phase
- Rates per role (if specified)
- Total person-months per phase

**From project-charter.md (if available):**
- Project name, PM, objectives
- Whether GTM is in scope — determines whether Section C is populated

**From risk-register.md (if available):**
- Number of HIGH-level risks → reserve calibration:
  - 0–2 HIGH risks: 10% reserve
  - 3–5 HIGH risks: 15% reserve
  - 6+ HIGH risks: 20% reserve, add PM warning

**From constraints.md (if available):**
- Hard budget ceiling — record in assumptions.

---

### Step 3 — Calculate Costs by Phase

**Section A: Team** (for each phase 1–6)

For each role:
```
Cost = FTE × Phase duration (months) × Rate ($/month)
```
- FTE and duration: from resource-plan.md
- Rates: from resource-plan.md → if not available, from preliminary-estimate.xlsx
- If rates are unavailable at role level in both resource-plan.md and preliminary-estimate.xlsx,
  and the estimate contains only aggregated team costs by phase: use the aggregate as
  Section A total for that phase without role breakdown. Record in assumptions:
  "Role-level rates unavailable — aggregated data from estimate used.
  Update rates in resource-plan.md for improved accuracy."
  In Sheet 3, column "Rate" — mark as "from estimate (aggregated)".

Phase total (team) = Σ costs of all roles in the phase.

**Section B: Infrastructure** (for each phase)

Take data from preliminary-estimate.xlsx (realistic scenario, infrastructure row by phase).
If data is unavailable — use default ranges from `templates/project-budget-{lang}.md`
(§ Default Infrastructure).

**Section C: Marketing/GTM** (for each phase)

- If GTM is in scope: take from preliminary-estimate.xlsx → Section C by phase.
- If GTM is not in scope: set to zero, add note "GTM is not in scope".

---

### Step 4 — Calculate Reserve and Totals

1. **Baseline budget** = Σ (Team + Infrastructure + GTM) across all phases.
2. **Contingency Reserve**:
   - Percentage: determined in Step 2 from the risk register (10%, 15%, or 20%).
   - If risk-register.md is unavailable: 10% default, add note "Risk register unavailable —
     standard 10% reserve applied".
   - Reserve = Baseline budget × %
3. **Grand Total** = Baseline budget + Reserve.
4. **Constraint check**: if Grand Total > Ceiling (from constraints.md):
   - Add risk flag to Summary: "Grand Total [$X] exceeds stated budget ceiling [$Y].
     Recommended: revise scope, reduce team, or phase the project funding."
   - Do not adjust numbers to fit the ceiling.

---

### Step 5 — Populate xlsx Sheets

Follow the schema in `templates/project-budget-{lang}.md`:

**Sheet 1 — Summary:**
- Header: project, PM, date, version
- Assumptions (minimum 3): calculation method, data sources, rates, GTM status, reserve %
- Phase summary table: A (Team) + B (Infra) + C (GTM) = Total per phase
- "Contingency Reserve" row: % and amount
- **Grand Total**
- Risk flag (if budget > ceiling)

**Sheet 2 — Budget Detail:**
- Rows: phase → category → cost line item
- Columns: Unit | Qty | Rate | Total
- Example row: "Phase 2 | Team | Product Manager | person-month | 2 | $5,000 | $10,000"

**Sheet 3 — Resource Detail:**
- Rows: role
- Columns: Phase 1 | Phase 2 | ... | Phase 6 | Total (p-m) | Rate | Total ($)
- Source: resource-plan.md

---

### Step 6 — Create xlsx and Save

1. Use the xlsx skill to create `project-budget.xlsx` following the template schema.
2. Save to `{project}/02-planning/project-budget.xlsx`.
3. Show in chat:
   - Confirmation: "Budget saved as project-budget.xlsx in 02-planning/."
   - Sheet 1 Summary as a markdown table.
   - List of assumptions.
   - Risk flags (if any).
   - Next step: "Budget is ready. Review rates and team composition. Once approved by PM,
     use generate-approval-letter to send it for stakeholder approval."
4. Write to `logs/log.md`: date, skill, file created, grand total, reserve %.
5. Update `project-state.md`: artifact `project-budget.xlsx` status → "draft".

---

## Templates

| File | Purpose |
|------|---------|
| `templates/project-budget-ru.md` | xlsx artifact schema (RU) |
| `templates/project-budget-en.md` | xlsx artifact schema (EN) |

---

## Dependencies

**Reads:**
- `01-initiation/preliminary-estimate.xlsx` — realistic scenario (team, infra, GTM by phase)
- `02-planning/resource-plan.md` — roles, FTE, rates by phase
- `01-initiation/project-charter.md` — project name, PM, GTM scope status
- `input/constraints.md` — budget ceiling (if any)
- `01-initiation/risk-register.md` — for reserve calibration

**Passes data to:**
- `monitor-progress` (#19) — budget deviation tracking
- `generate-change-impact` (#21) — scope change impact on budget
- `generate-plan-fact-report` (#29) — plan vs. actual budget

**Calls:**
- `xlsx skill` — to generate the .xlsx file

---

## Constraints

- Mode B: budget is a draft for PM review, not a final document
- Single scenario (baseline) — scenario analysis is done in generate-estimate, not here
- Does not update automatically on scope changes — re-run manually via generate-change-impact
- Does not build a detailed WBS or calculate task-level effort — use generate-project-plan
- Operates on one project per invocation
- If preliminary-estimate.xlsx is unavailable — skill does not run; no fallback
