---
name: generate-change-impact
description: "Generates a change impact assessment file (change-impact-CR-001.xlsx) for Phase 4 — Development. PM describes a scope change request; the agent classifies the change (scope / budget / timeline / resource), analyzes impact on project-plan.md and project-budget.xlsx, calculates timeline delta, budget delta, and risk level (Low / Medium / High), then produces a two-sheet xlsx artifact with a summary and detailed breakdown. PM reviews the draft and makes the final approval decision. Covers task #21 of the project management agent. Mode B: agent prepares draft, PM decides. If approved — updates project-plan.md via generate-project-plan. Triggers EN: 'scope change request', 'change impact assessment', 'generate change impact'."
---

# Skill: generate-change-impact

Generates a change impact assessment for Phase 4 — Development (task #21).
PM describes the change request; the agent classifies it, analyzes impact on
timeline and budget, calculates deltas and risk level. Output: `change-impact-{id}.xlsx`.
Mode B: agent prepares draft, PM makes the decision.

---

## Triggers

**Russian:** «запрос на изменение скоупа», «оценка изменения», «влияние изменения на проект», «изменение скоупа», «CR по проекту», «оцени изменение», «изменение требований», «корректировка скоупа»
**English:** "scope change request", "change impact assessment", "generate change impact", "change request analysis", "evaluate scope change", "change order impact"

---

## Language Detection

Determine the language of the user's request:
- If the request is in Russian → use templates with `-ru` suffix, respond in Russian
- Otherwise → use templates with `-en` suffix, respond in English

---

## Input

| Data | Required | Source |
|------|:--------:|--------|
| Change description | yes | PM writes in chat |
| Request ID (CR-001, etc.) | no | PM provides or agent assigns next in sequence |
| Requester | no | PM provides or leave blank |
| Project plan | no | `02-planning/project-plan.md` — deadlines and tasks |
| Project budget | no | `02-planning/project-budget.xlsx` — budget items |

## Output

| File | Project path | Format | Description |
|------|-------------|--------|-------------|
| `change-impact-{id}.xlsx` | `04-development/` | .xlsx | Change impact assessment |

File structure — 2 sheets (Summary, Impact Detail) — defined in `templates/change-impact-{lang}.md`.

---

## Instructions

### Step 1 — Validate Request

**Guard-rail — check request type.**
If the request concerns general change management (methodology, processes) or does not
describe a specific scope change → respond:
"generate-change-impact assesses the impact of a specific scope change request.
Describe the specific change: what needs to change, the rationale, and the expected impact.
The skill will produce a structured assessment for decision-making."
Do not start the workflow.

If the request contains a description of a specific change → proceed to Step 2.

---

### Step 2 — Collect Change Request Data

Extract from chat:
- **Change description** — what is changing (functionality, technology, scope of work)
- **Rationale** — why the change is needed
- **ID** — if PM provided one (CR-001, CR-002, etc.)
- **Requester** — who initiated the change (client, team, PM, external factor)

**If the change involves replacing a technology, architecture, or platform
(keywords: "rewrite", "replace platform", "migrate to", "entire [component]"):**
Ask a clarifying question before proceeding to Step 3:
"To calculate impact accurately, please clarify:
1. Does the change affect the entire [component] or only part of it?
2. Is the work planned in parallel with current sprint tasks or sequentially (after the current sprint)?"
Do not proceed to Step 3 without an answer.

**If the description is insufficient:**
Ask: "Please describe the change in more detail:
1. What exactly is changing in scope (features, requirements, scope of work)?
2. Why is this change needed?
3. Are there any known deadline or budget constraints for this change?"

**If no ID is provided:** assign the next in sequence (find the last CR-XXX in `04-development/`
or start with CR-001). Notify PM: "Request assigned ID: CR-001."

**Change category classification:**
Based on the description, determine the category:
- `scope` — adding or removing functionality or requirements
- `budget` — change in funding without altering functionality
- `timeline` — deadline shift without changing scope or budget
- `resource` — replacing, adding, or removing team members

If the change affects multiple categories — assign a primary one, list the rest as secondary.

---

### Step 3 — Read Project Data

Read project files for impact analysis:
- `02-planning/project-plan.md` — current deadlines, tasks, milestones
- `02-planning/project-budget.xlsx` — budget items and approved amounts

**If files are unavailable or not found:**
Ask PM a clarifying question:
"Files project-plan.md / project-budget.xlsx not found. For a more accurate assessment, please provide:
1. Approximate project completion date?
2. Approved budget (approximate amount)?
3. Dates of the nearest key milestones (if known)?
If this data is not available — I will generate the assessment based on the change description only."
Use the answers in the Step 4 analysis.
Mark the data source in the artifact: "data provided by PM (files not loaded)" or "estimate — no project files".

---

### Step 4 — Impact Analysis

Analyze across four dimensions. Record each value with an explicit data source
(from file or agent estimate based on PM description).

**4.1 Timeline Impact**
- Identify affected tasks and milestones from project-plan.md
- Calculate the shift in working days for each affected task
- Determine the total shift of the final deadline (if applicable)
- Identify critical path: does the change shift the project completion date?

**4.2 Budget Impact**
- Identify affected budget items from project-budget.xlsx
- Estimate the delta in monetary terms (absolute and %)
- If budget data is unavailable — mark as "to be confirmed by PM"

**4.3 Resource Impact**
- Determine whether additional or different team members are required
- Specify roles and time volume (if applicable)

**4.4 Risk Level and Overall Impact Level**
Determine the impact level using the matrix:

| Level | Criteria |
|-------|----------|
| Low | Shift ≤ 5 working days, budget delta ≤ 5%, does not affect critical path |
| Medium | Shift 6–15 working days OR budget delta 6–15% OR affects critical path |
| High | Shift > 15 working days OR budget delta > 15% OR changes architecture/core requirements |

Record the final level: **Low / Medium / High**.

---

### Step 5 — Confirm Data with PM

Show PM a brief impact summary in chat before generating the file:

```
CR-001 — [change title]
Category: [scope/budget/timeline/resource]
Timeline impact: [+X working days / "no impact"]
Budget impact: [+X / ±0 / "to be confirmed"]
Impact level: [Low/Medium/High]
```

Ask: "Is this data correct? Confirm or correct — I will generate the file."

**Do not create the file until PM confirms.**

---

### Step 6 — Create xlsx and Save

Follow the schema from `templates/change-impact-{lang}.md`.

1. Use the xlsx skill to create `change-impact-{id}.xlsx`.
2. Save to `{project}/04-development/change-impact-{id}.xlsx`.
3. Output in chat:
   - Confirmation: "File saved: 04-development/change-impact-{id}.xlsx"
   - Sheet 1 Summary as a Markdown table (key blocks only)
   - Question: "Assessment ready. Your decision: Approved / Rejected / Postponed?
     Add a comment if needed."
4. **Do not make the decision for PM** — this is always the human's call.

---

### Step 7 — Record Decision

After PM responds:
1. Record the decision (Approved / Rejected / Postponed + date + comment) in the
   "PM Decision Block" of the file (if xlsx is edited) or save separately in `logs/log.md`.
2. Update `project-state.md`: artifact `change-impact-{id}.xlsx` → "approved".
3. Write to `logs/log.md`: date, CR-ID, category, impact level, decision.
4. If decision is **Approved** → notify PM:
   "Change approved. To update the project plan, run generate-project-plan
   (task #7) using data from CR-{id}: [task shifts and budget delta]."

---

## Templates

| File | Purpose |
|------|---------|
| `templates/change-impact-ru.md` | xlsx artifact schema (RU) |
| `templates/change-impact-en.md` | xlsx artifact schema (EN) |

---

## Dependencies

**Reads:**
- Change description from chat (required)
- `02-planning/project-plan.md` — deadlines and tasks (optional)
- `02-planning/project-budget.xlsx` — budget items (optional)

**Passes data to:**
- `04-development/change-impact-{id}.xlsx` → `generate-project-plan` (#7)
  — on change approval, to update the project plan

**Calls:**
- `xlsx skill` — to create the .xlsx file

---

## Constraints

- Mode B: assessment is a draft for PM; approval decision is always made by the human
- One CR per invocation; for multiple CRs — run the skill separately for each
- If project-plan.md and project-budget.xlsx are unavailable — analysis is based on PM data, marked "estimate — no project files"
- Does not modify project-plan.md directly — only recommends running generate-project-plan after approval
- Does not create Jira tasks — use coordinate-executors for that
- Category classification is automatic based on description; PM can correct it at Step 5
