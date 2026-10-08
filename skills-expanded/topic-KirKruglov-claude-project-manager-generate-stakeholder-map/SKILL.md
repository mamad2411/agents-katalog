---
name: generate-stakeholder-map
description: "Generates a structured stakeholder map for IT project management (Phase 1 —
  Initiation). Reads available project files (client questionnaire, project charter,
  team list), extracts stakeholder data, and produces a stakeholder-map.md file with
  a summary table and narrative blocks per stakeholder. Triggers RU: «создай карту
  стейкхолдеров», «сформируй карту стейкхолдеров», «идентифицируй стейкхолдеров»,
  «подготовь карту заинтересованных сторон», «кто стейкхолдеры проекта». Triggers EN:
  'generate stakeholder map', 'create stakeholder map', 'identify stakeholders', 'stakeholder
  analysis', 'map project stakeholders', 'who are the stakeholders'."
---

# Skill: generate-stakeholder-map

Generates a stakeholder map for IT projects (Phase 1 — Initiation). Reads available project files, extracts stakeholder data, and produces a structured `stakeholder-map.md` with a summary table and narrative blocks per stakeholder.

---

## Triggers

**Russian:** «создай карту стейкхолдеров», «сформируй карту стейкхолдеров», «идентифицируй стейкхолдеров», «подготовь карту заинтересованных сторон», «кто стейкхолдеры проекта», «нужна карта стейкхолдеров»
**English:** "generate stakeholder map", "create stakeholder map", "identify stakeholders", "stakeholder analysis", "map project stakeholders", "who are the stakeholders"

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
| Client answers | no | `01-initiation/questionnaire-client.md` | Primary source: Block 5 + stakeholder mentions throughout |
| Project charter | no | `01-initiation/project-charter.md` | Secondary source (artifact from generate-charter MVP skill) |
| Team list | no | `input/team-list.md` | Org structure, roles, contacts |
| Manual input | no | Chat | If no files found — request data directly |

If none of the files is available — ask a clarifying question (see Step 1).

---

## Output

| File | Project path | Mode |
|------|--------------|------|
| `stakeholder-map.md` | `01-initiation/` | generate |

---

## Instructions

### Step 1 — Locate Available Data Sources

Before checking files: if the request includes tasks outside this skill's scope
(generating a communications plan, contacting stakeholders, creating a risk register, etc.)
— complete the stakeholder map first, then explicitly note at the end of Step 4:
"[Task X] is outside this skill's scope. Use [relevant skill] for that."
Do not attempt to perform out-of-scope tasks.

Check for files in the following order:
1. `01-initiation/questionnaire-client.md`
2. `01-initiation/project-charter.md`
3. `input/team-list.md`

If the user's message already contains stakeholder data (names, roles, influence/interest levels)
— skip the A/B prompt and proceed directly to Step 2.

If none of the files exist AND no inline data is provided — show in chat:

```
No project input files found. Stakeholder data is needed to create the map.
Choose an option:
A) Provide a path to a file with stakeholder data
B) Enter data directly: name, role, influence level, and interest for each stakeholder
```

Wait for user response. Do not proceed without data.

---

### Step 2 — Extract Stakeholder Data

Read available files and extract the following per stakeholder:

| Field | Sources | Priority |
|-------|---------|----------|
| Name | questionnaire-client.md Block 5, project-charter.md | questionnaire > charter |
| Role / Title | questionnaire-client.md, team-list.md | questionnaire > team-list |
| Organization | questionnaire-client.md | — |
| Category | Determine independently (see list below) | — |
| Influence level | Infer from context | — |
| Interest level | Infer from context | — |
| Contact / Email | questionnaire-client.md, team-list.md | — |
| Interests and expectations | questionnaire-client.md Block 5, Block 2 | — |
| Concerns and risks | questionnaire-client.md Block 4 | — |
| Communication frequency | questionnaire-client.md Q20 equivalent | — |

**Stakeholder categories:**
- Sponsor
- Client
- Project Team
- Decision Maker
- External User
- Pilot Client
- Consultant / Regulator

**Influence and interest levels:** High / Medium / Low.

**Power/Interest quadrant** — determine automatically:
- High Power + High Interest → Manage Closely
- High Power + Low Interest → Keep Satisfied
- Low Power + High Interest → Keep Informed
- Low Power + Low Interest → Monitor
- Medium Power + High Interest → Keep Informed
- Medium Power + Low Interest → Monitor
(Treat Medium as the lower tier for quadrant assignment.)

If data for a field is insufficient:
- Mark `[clarify]` in the corresponding table cell (e.g., the Contact column) AND in the narrative block.
- Add a row to Section 5 (Open Questions) with: the missing field description, the stakeholder name, Status = Open.

---

### Step 3 — Generate the Stakeholder Map

1. Determine language → select template `stakeholder-map-{lang}.md`.
2. Fill in metadata:

| Placeholder | Source |
|-------------|--------|
| `{{project_name}}` | Project CLAUDE.md or user request |
| `{{pm_name}}` | CLAUDE.md (if available) |
| `{{date}}` | Current date (YYYY-MM-DD) |
| `{{version}}` | `1.0` |

3. Fill in the summary stakeholder table — one row per stakeholder.
4. Fill in the narrative block per stakeholder (role, expectations, concerns, strategy, frequency).
5. If there are more than 15 stakeholders — group minor ones (Monitor quadrant) into a single entry "Other Interested Parties".

---

### Step 4 — Save and Report

1. Save file: `01-initiation/stakeholder-map.md`.
2. Show in chat:
   - What was created: "Stakeholder map saved as [filename] in [path]."
   - Number of stakeholders, quadrant distribution
   - If Section 5 has rows — list them: "Open questions requiring clarification: [list]."
   - Next step: "Stakeholder map ready. Suggested next steps: generate-risk-register (risk register) or generate-comm-plan (communications plan — after project plan is approved)."
   - If the original request included out-of-scope tasks — note each one explicitly: "[Task X] is outside this skill's scope. Use [relevant skill] for that."
3. Log to `logs/log.md`: date, skill, created file, number of stakeholders.

---

## Templates

| File | Purpose |
|------|---------|
| `templates/stakeholder-map-ru.md` | Artifact template (RU) |
| `templates/stakeholder-map-en.md` | Artifact template (EN) |

---

## Dependencies

**Reads:**
- `01-initiation/questionnaire-client.md` — primary source (from generate-questionnaire)
- `01-initiation/project-charter.md` — secondary source (from generate-charter, MVP)
- `input/team-list.md` — org structure

**Passes data to:**
- `generate-comm-plan` — communications plan is built on the stakeholder map
- `coordinate-meeting` — attendee lists for meetings
- `generate-approval-letter` — approval addressees

---

## Constraints

- Mode B: agent prepares a draft, human reviews and approves
- Does not send communications to stakeholders — that is the task of generate-comm-plan and send-email
- Does not generate a communications plan — only the stakeholder map
- No Miro integration (MCP does not exist as of April 2026)
- Handles one project per invocation
- If stakeholder data is insufficient — marks `[clarify]`, does not fabricate
- Maximum 15 stakeholders in detailed blocks; additional ones grouped as "Other Interested Parties"

---

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-04-06 | 1.0 | Skill created. Three data sources: questionnaire-client, project-charter, team-list. Template: table + narrative blocks. No Miro. |
| 2026-04-06 | 1.1 | Post-eval fixes (3/6 → 6/6 expected): added inline-data detection in Step 1 (skip A/B when data provided); added Medium Power quadrant rules; added [clarify] to Contact column + Section 5 auto-fill; added out-of-scope guard rail in Steps 1 and 4; added Section 5 open questions reporting. |
