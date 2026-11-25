---
name: generate-comparison-table
description: "Generates a prototype comparison table (comparison-table.xlsx) for Phase 3 — Prototyping. PM describes 2–4 prototypes in chat; the agent structures evaluation criteria (standard set: technical feasibility, UX quality, cost, timeline, risk), proposes weights (customisable by PM), scores each prototype on a 1–5 scale, calculates weighted totals and provides a recommendation. Output: two-sheet xlsx file with a summary and a detailed scoring matrix. PM reviews the draft and makes the final selection decision. Covers task #14 of the project management agent. Mode B: agent prepares draft, PM decides. Triggers EN: 'compare prototypes', 'prototype comparison table', 'evaluate prototype options'."
---

# Skill: generate-comparison-table

Generates a prototype comparison table for Phase 3 — Prototyping (task #14).
PM describes prototypes in chat; the agent defines criteria with weights, assigns scores,
calculates weighted totals, and provides a recommendation. Output: `comparison-table.xlsx`.
Mode B: agent prepares the draft, PM makes the final selection decision.

---

## Triggers

**Russian:** «сравни прототипы», «сравнительная таблица прототипов», «подготовь таблицу сравнения», «оцени варианты прототипов», «какой прототип выбрать», «таблица отбора»
**English:** "compare prototypes", "prototype comparison table", "evaluate prototype options", "generate comparison table", "which prototype to choose", "score prototypes"

---

## Language Detection

Determine the language of the user's request:
- If the request is in Russian → use templates with `-ru` suffix, respond in Russian
- Otherwise → use templates with `-en` suffix, respond in English

---

## Input

| Data | Required | Source |
|------|:--------:|--------|
| Prototype descriptions | yes | PM provides in chat (2–4 prototypes) |
| Evaluation criteria | no | standard set — PM confirms or adjusts |
| Criteria weights | no | proposed by agent (sum = 100%) — PM adjusts |
| Project charter | no | `01-initiation/project-charter.md` — project name, PM |
| Project plan | no | `02-planning/project-plan.md` — project context |

## Output

| File | Path in project | Format | Description |
|------|----------------|--------|-------------|
| `comparison-table.xlsx` | `03-prototyping/` | .xlsx | Prototype comparison table |

File structure — 2 sheets (Summary, Score Detail) — defined in `templates/comparison-table-{lang}.md`.

---

## Instructions

### Step 1 — Validate the request

**Guard-rail — check request type.**
If the request is about creating or developing prototypes → respond:
"generate-comparison-table prepares a comparison table for ready prototypes.
To assign prototype creation tasks, use coordinate-executors (task #13).
Once prototypes are ready — return to generate-comparison-table."
Do not start the workflow.

If the request includes descriptions of multiple options/prototypes → proceed to Step 2.

---

### Step 2 — Collect prototype data

Extract prototype descriptions from chat. Each prototype must include:
- Name (A / B / C or a specific name)
- Brief description (1–3 sentences)
- Key characteristics: stack, architectural approach, UX specifics

**If data is insufficient for a meaningful assessment:**
Ask: "Describe each prototype — name, 2–3 key features (technology, UX approach, implementation complexity). Minimum 2 prototypes."
Do not proceed to Step 3 without at least 2 descriptions.

**Acceptable range:** 2–4 prototypes. If 5+ — ask PM: "You have 5+ prototypes — please narrow the list or select 4 final candidates for comparison."

---

### Step 3 — Confirm criteria and weights

Present PM with the standard criteria set:

| # | Criterion | Weight | Direction |
|---|-----------|--------|-----------|
| 1 | Technical Feasibility | 25% | 5 = very easy to implement |
| 2 | UX Quality | 25% | 5 = excellent UX |
| 3 | Development Cost | 20% | 5 = minimal cost |
| 4 | Delivery Timeline | 15% | 5 = fastest delivery |
| 5 | Risk Level | 15% | 5 = minimal risk |

Ask: "Confirm the criteria and weights or adjust them. The sum of weights must equal 100%."

**Weight adjustment rules:**
- If PM changes weights with numbers — verify sum = 100%. If not — notify and ask to clarify.
- If PM states a qualitative priority without numbers ("X is more important", "focus on Y") —
  propose a specific redistribution: "Based on your priority, I suggest:
  [criterion X] 35%, [criterion Y] 25%, others reduced proportionally. Sum = 100%. Confirm?"
  Do not proceed to Step 4 without explicit PM confirmation.
- If PM adds a criterion — request its weight (if not stated); reduce each existing criterion
  proportionally to free up the required percentage (sum always = 100%).
  Example: adding a criterion with weight 30% → reduce each of the 5 standard criteria by 6%
  (25→19, 25→19, 20→14, 15→9, 15→9; total 70% + 30% = 100%).
  Show PM the final distribution and request confirmation before proceeding to Step 4.
- If PM removes a criterion — redistribute its weight proportionally among the remaining ones.
  Show PM the final distribution and request confirmation before proceeding to Step 4.

Lock the final criteria and weights only after explicit PM confirmation.
Proceed to Step 4.

---

### Step 4 — Score prototypes

For each (prototype × criterion) pair, assign a score 1–5:
- Score is strictly based on PM's descriptions from Step 2.
- Scale: 1 = very poor, 3 = neutral/average, 5 = very good.
- For each criterion: "5" = best possible outcome for that criterion
  (see "Direction" column in Step 3 table).

**Scoring principles:**
- If PM provided sufficient data for a reasoned score → assign a numeric score + brief rationale.
- If data is insufficient for a specific criterion → assign 3 (neutral) + mark
  "insufficient data" in Notes on the Score Detail sheet.

**Weighted score formula:**

`Weighted Score = Σ (Weight_i × Score_i / 100)`

Result range: 1.00 – 5.00.

Identify the winner (highest Weighted Score) and formulate the agent's recommendation:
1–2 sentences based on the data, without implying that the agent is making the decision.

---

### Step 5 — Create xlsx and save

Follow the schema from `templates/comparison-table-{lang}.md`.

1. Use the xlsx skill to create `comparison-table.xlsx`.
2. Save to `{project}/03-prototyping/comparison-table.xlsx`.
3. Output in chat:
   - Confirmation: "File saved: 03-prototyping/comparison-table.xlsx"
   - Summary sheet as a Markdown table.
   - Agent's recommendation.
   - Question: "The table is ready. Review the results and indicate your decision:
     which prototype is selected for development?"
4. **Do not make the selection on behalf of PM** — this is always a human decision.
5. After PM's response: record the decision in `logs/log.md`.
6. Update `project-state.md`: artifact `comparison-table.xlsx` → "draft";
   upon receiving PM's decision → "approved".

---

## Templates

| File | Purpose |
|------|---------|
| `templates/comparison-table-ru.md` | xlsx artifact schema (RU) |
| `templates/comparison-table-en.md` | xlsx artifact schema (EN) |

---

## Dependencies

**Reads:**
- Prototype descriptions from chat (required)
- `01-initiation/project-charter.md` — project name, PM (optional)
- `02-planning/project-plan.md` — project context (optional)

**Passes data to:**
- `03-prototyping/comparison-table.xlsx` → `generate-meeting-protocol` (#16)
  — as input for the demo meeting protocol

**Calls:**
- `xlsx skill` — to create the .xlsx file

---

## Constraints

- Mode B: table is a draft for PM; selection decision is made by the human only
- Minimum 2 prototypes to start; maximum 4 per invocation
- Standard criteria are the default proposal; PM confirms before scoring
- Scoring is based on PM's descriptions; insufficient data → neutral score (3) with a note
- Does not create prototypes or assign tasks — use coordinate-executors (#13) for that
- One project per invocation
