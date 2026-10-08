---
name: generate-checklist
description: "Generates project management checklists for Phase 5 (Launch) and Phase 6 (Closure): launch readiness checklist (launch-checklist.md), technical readiness checklist (tech-readiness-checklist.md), and handover-to-operations checklist (handover-checklist.md). Covers tasks #22, #24, and #32 of the project management agent. Mode B: agent pre-populates base items from PMBoK-aligned templates and enriches with data from project-plan.md if available; PM reviews and finalizes. Checklist type is inferred from context; if ambiguous, agent asks. Triggers EN: 'launch checklist', 'tech readiness checklist', 'handover checklist'."
---

# Skill: generate-checklist

Generates three types of project checklists for the Launch (Phase 5) and Closure (Phase 6) phases.
Populates base items from PMBoK-aligned templates; enriches with project-plan.md data when available.
Mode B: agent prepares a draft, PM reviews and finalizes.

---

## Triggers

**Russian:** «чек-лист запуска», «чек-лист технической готовности», «чек-лист передачи», «подготовь чеклист», «проверка готовности к запуску», «список для передачи в эксплуатацию»
**English:** "launch checklist", "tech readiness checklist", "handover checklist", "generate checklist", "readiness checklist", "deployment checklist", "closure checklist"

---

## Language Detection

- Request in Russian → templates with `-ru` suffix, responses in Russian
- Otherwise → templates with `-en` suffix, responses in English

---

## Input

| Data | Required | Source |
|------|:--------:|--------|
| Checklist type (launch / tech readiness / handover) | no | Inferred from context or PM question |
| Project name | no | `project-state.md` or PM in chat |
| Responsible person | no | PM specifies or left blank |
| Task and milestone data | no | `02-planning/project-plan.md` — for auto-population |
| Launch / handover date | no | PM specifies or from project-plan.md |

## Output

| File | Project path | Type | Task |
|------|-------------|------|------|
| `launch-checklist.md` | `03-execution/` | Launch checklist | #22 |
| `tech-readiness-checklist.md` | `03-execution/` | Tech readiness checklist | #24 |
| `handover-checklist.md` | `04-closure/` | Handover checklist | #32 |

File structure is defined in the corresponding template from `templates/`.

---

## Instructions

### Step 1 — Determine Checklist Type

**Guard-rail — verify request type.**
If the request concerns checklist methodology in general, not a specific project checklist → respond:
"generate-checklist creates three types of project checklists: launch (#22, Phase 5), technical readiness (#24, Phase 5), and operations handover (#32, Phase 6). Specify which checklist you need or describe the context."
Do not start the workflow.

**Infer type from request context:**

| Context / keywords | Checklist type |
|-------------------|---------------|
| "launch", "go-live", "market release", task #22 | launch-checklist |
| "tech readiness", "deploy", "infrastructure", task #24 | tech-readiness-checklist |
| "handover", "operations", "closure", task #32 | handover-checklist |

If type cannot be determined unambiguously → ask:
"Which checklist do you need?
1. Launch checklist (#22) — confirming overall product/project readiness for launch.
2. Technical readiness checklist (#24) — verifying technical and infrastructure readiness.
3. Operations handover checklist (#32) — documenting project transfer to the support/operations team."
Do not proceed to Step 2 without an answer.

---

### Step 2 — Gather Context Data

Read `project-state.md` to obtain:
- Project name
- Current phase and launch date (if specified)

If `02-planning/project-plan.md` is available — read and extract:
- Planned launch / handover date
- Key milestones of Phase 5 or Phase 6
- Task list and owners for the phase (for auto-populating checklist items)
- Team composition (PM, tech lead, business owner)

**If files are unavailable:** continue with template base items. Output to chat:
"project-plan.md not found — generating checklist from PMBoK template. Add specific tasks, dates, and owners manually."

---

### Step 3 — Build the Checklist

Load the corresponding template:

| Type | Template (RU) | Template (EN) |
|------|--------------|--------------|
| launch-checklist | `templates/launch-checklist-ru.md` | `templates/launch-checklist-en.md` |
| tech-readiness-checklist | `templates/tech-readiness-checklist-ru.md` | `templates/tech-readiness-checklist-en.md` |
| handover-checklist | `templates/handover-checklist-ru.md` | `templates/handover-checklist-en.md` |

Populate template placeholders:
1. Project name, date, responsible — from project-state.md or PM's data
2. Checklist items — base items from template (PMBoK Best Practice) + specifics from project-plan.md
3. Owners per item — from project plan if available; otherwise `[PM]` as placeholder
4. Due dates — from project plan if available; otherwise `[date]` as placeholder

**Enrichment rule:** if project-plan.md contains specific Phase tasks, add them as additional items under the matching template section, marked `[from plan]`.

---

### Step 4 — Show Draft to PM

Output to chat:
- Brief summary: checklist type, number of sections, number of items
- First 2 sections as preview (markdown)

Ask:
"Draft checklist is ready. Would you like to:
1. Save as is → I will generate the file.
2. Add / remove items → describe your changes.
3. Update owners or dates → specify."

**Do not create the file until PM confirms.**

---

### Step 5 — Create File and Save

1. Create file per the table in the Output section.
2. Save to the corresponding project folder.
3. Update `project-state.md`: add/update artifact record → status `draft`.
4. Write to `logs/log.md`: date, skill, checklist type, file path.
5. Output to chat:
   - "File saved: {path}"
   - Next orchestration step (see table below)

**Post-creation orchestration:**

| Checklist type | Next step |
|---------------|-----------|
| launch-checklist (#22) | Run tech-readiness-checklist (#24) in parallel; after both → coordinate-executors (#23) |
| tech-readiness-checklist (#24) | Run in parallel with launch-checklist (#22); both complete → launch phase active |
| handover-checklist (#32) | After completion → generate-closure-report (#31) |

---

## Templates

| File | Checklist type |
|------|--------------|
| `templates/launch-checklist-ru.md` | Launch checklist (RU) |
| `templates/launch-checklist-en.md` | Launch checklist (EN) |
| `templates/tech-readiness-checklist-ru.md` | Tech readiness checklist (RU) |
| `templates/tech-readiness-checklist-en.md` | Tech readiness checklist (EN) |
| `templates/handover-checklist-ru.md` | Handover checklist (RU) |
| `templates/handover-checklist-en.md` | Handover checklist (EN) |

---

## Dependencies

**Reads:**
- `project-state.md` — project name, phase (optional)
- `02-planning/project-plan.md` — tasks, milestones, owners (optional)

**Feeds data to:**
- `03-execution/launch-checklist.md` → coordinate-executors (#23)
- `03-execution/tech-readiness-checklist.md` → activates launch phase
- `04-closure/handover-checklist.md` → generate-closure-report (#31)

---

## Constraints

- Mode B: draft for PM; PM reviews and approves
- One checklist type per invocation; for multiple types — separate skill calls
- Without project-plan.md — base template items only; placeholders for project-specific data
- Does not modify project-plan.md or other artifacts
- Does not create Jira tasks — use coordinate-executors for that
- Base items follow PMBoK 8 and Agile best practice; PM adapts to project specifics
