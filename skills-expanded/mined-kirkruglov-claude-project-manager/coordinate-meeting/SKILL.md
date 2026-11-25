---
name: coordinate-meeting
description: "Coordinates project meetings: generates a structured agenda, creates a Google Calendar event, and prepares a protocol template. Covers 5 meeting types across the full project lifecycle — tasks #6, #15, #17, #20, #26. Meeting types: Go/No-Go (Phase 1, #6), Client Demo (Phase 3, #15), Sprint Planning (Phase 4, #17), Sprint Demo (Phase 4, #20), Launch Status Meeting (Phase 5, #26). Reads project context files (stakeholder-map, project-plan, progress reports) to auto-populate participants and agenda topics. Mode B: agent prepares a draft agenda, PM confirms before the Calendar event is created. Triggers EN: 'coordinate meeting', 'prepare agenda', 'schedule meeting'."
---

# Skill: coordinate-meeting

Coordinates project meetings for all 5 types across the project lifecycle.
Generates an agenda, creates a Google Calendar event (with fallback), and
prepares a protocol template. Mode B: PM confirms the draft before the
Calendar event is created and files are saved.

---

## Triggers

**Russian:** «организуй встречу», «подготовь повестку», «запланируй встречу», «повестка для встречи», «Go/No-Go», «демо заказчику», «планирование спринта», «демо спринта», «статусная встреча по запуску»
**English:** "coordinate meeting", "prepare agenda", "schedule meeting", "go no go meeting", "client demo", "sprint planning", "sprint demo", "launch status meeting"

---

## Language Detection

- Request in Russian → template `meeting-agenda-template-ru.md`, all outputs in Russian
- Otherwise → template `meeting-agenda-template-en.md`, all outputs in English

---

## Meeting Types

| Key | Description | Phase | Task |
|-----|-------------|-------|------|
| `go-no-go` | Go/No-Go gate: approve project initiation | 1 | #6 |
| `demo-client` | Prototype demo to the client | 3 | #15 |
| `sprint-planning` | Sprint planning (repeating) | 4 | #17 |
| `sprint-demo` | Sprint review / demo (repeating) | 4 | #20 |
| `launch-status` | Launch status review (repeating) | 5 | #26 |

---

## Input

| Data | Required | Source |
|------|:--------:|--------|
| Meeting type | yes | PM in chat (inferred or asked) |
| Date and time | yes | PM in chat |
| Participants | no | `01-initiation/stakeholder-map.md` or PM |
| Project name, current phase | no | `project-state.md` |
| Sprint number (sprint-planning / sprint-demo) | no | `project-state.md` or PM |
| Meeting objectives | no | Derived from type and project context |

## Output

| File | Project path | Task |
|------|-------------|------|
| `agenda-{type}-{YYYY-MM-DD}.md` | `meetings/` | #6 / #15 / #17 / #20 / #26 |
| `protocol-{type}-{YYYY-MM-DD}.md` | `meetings/` | #6 / #15 / #17 / #20 / #26 |
| Google Calendar event | external action | all types |
| `email-tpl-meeting-status.md` | `meetings/` | #26 only |

---

## Instructions

### Step 1 — Guard-rail and Determine Meeting Type

**Guard-rail:** If the request is about meeting facilitation methodology in general
(not a specific project meeting) → respond:
"coordinate-meeting organizes a specific project meeting. Tell me what's happening
in your project right now — I'll determine the right meeting type."
Do not start the workflow.

**Determine meeting type from PM's request:**

| Cues | Meeting type |
|------|-------------|
| "go/no-go", "project approval", "charter review", "project gate" | `go-no-go` |
| "client demo", "demo to client", "prototype presentation", "show client" | `demo-client` |
| "sprint planning", "plan the sprint", "start sprint", "next sprint" | `sprint-planning` |
| "sprint demo", "sprint review", "end of sprint", "sprint results" | `sprint-demo` |
| "launch status", "launch meeting", "go-live status", "launch sync" | `launch-status` |

If type is unclear → ask:
"Which type of meeting do you need?
1. Go/No-Go — project initiation gate (Phase 1)
2. Client Demo — prototype presentation (Phase 3)
3. Sprint Planning — plan the upcoming sprint (Phase 4)
4. Sprint Demo — review sprint results (Phase 4)
5. Launch Status Meeting — launch progress review (Phase 5)"

If date/time is not provided → ask: "When is the meeting? (date and time)"

---

### Step 2 — Gather Context from Project Files

Always read (if available):
- `project-state.md` → project name, current phase, sprint number

Read based on meeting type:

| Meeting type | Additional files to read |
|-------------|--------------------------|
| `go-no-go` | `01-initiation/project-charter.md`, `01-initiation/risk-register.md` |
| `demo-client` | `project-state.md` (prototype readiness), `03-execution/comparison-table.xlsx` |
| `sprint-planning` | `02-planning/project-plan.md` (backlog, next sprint milestones) |
| `sprint-demo` | last `reports/progress-report-*.md`, `02-planning/project-plan.md` |
| `launch-status` | last `reports/weekly-status-*.md`, `03-execution/launch-checklist.md` |

Always read for participants:
- `01-initiation/stakeholder-map.md` → determine participant list by role/type

**If files are unavailable:** continue with PM-provided data and placeholder values.
Notify in chat: "[Filename] not found — placeholders used. Fill in before the meeting."

---

### Step 3 — Determine Participants

Use the following defaults; enrich with stakeholder-map.md if available:

| Meeting type | Required participants |
|-------------|----------------------|
| `go-no-go` | PM, Project Sponsor, Client / Decision-Making Stakeholders |
| `demo-client` | PM, Prototype Team, Client, Key Stakeholders |
| `sprint-planning` | PM, Development Team, Tech Lead |
| `sprint-demo` | PM, Development Team, Client, Key Stakeholders |
| `launch-status` | PM, Dev Lead, Marketing Lead, Ops Lead, Client |

If stakeholder-map.md is available → replace roles with actual names and contacts.
If not available → keep role placeholders.

---

### Step 4 — Build Agenda

Load the template matching the detected language:
- Russian → `templates/meeting-agenda-template-ru.md`
- English → `templates/meeting-agenda-template-en.md`

Default meeting durations — use these values for `{DURATION}` in the template unless PM specifies otherwise:

| Meeting type | Default duration |
|-------------|-----------------|
| `go-no-go` | 60 min |
| `demo-client` | 90 min |
| `sprint-planning` | 90 min |
| `sprint-demo` | 60 min |
| `launch-status` | 60 min |

Populate the template with meeting-type-specific agenda items:

**go-no-go (60 min):**
1. Welcome and objectives (5 min)
2. Project charter status — key parameters and constraints (15 min)
3. Risk overview — top 3 risks (10 min)
4. Open questions from stakeholders (15 min)
5. Go / No-Go vote and decision (10 min)
6. Next steps if Go (5 min)

**demo-client (90 min):**
1. Welcome and agenda overview (5 min)
2. Project status since last meeting (10 min)
3. Prototype demonstrations — per variant (40 min)
4. Comparison overview if comparison-table exists (15 min)
5. Client feedback and discussion (15 min)
6. Decision / next steps (5 min)

**sprint-planning (60–90 min):**
1. Previous sprint recap — completed vs planned (10 min)
2. Next sprint goals and success criteria (10 min)
3. Backlog review — candidate items (20–30 min)
4. Task assignment and estimation (15–20 min)
5. Sprint commitment confirmation (5 min)

**sprint-demo (60 min):**
1. Sprint goals recap (5 min)
2. Demonstration of completed items (30 min)
3. What was not completed and why (10 min)
4. Feedback from stakeholders (10 min)
5. Retrospective highlights (optional, 5 min)

**launch-status (60 min):**
1. Overall launch status — RAG (5 min)
2. Dev stream status (10 min)
3. Marketing stream status (10 min)
4. Ops/infrastructure status (10 min)
5. Blockers, risks, escalations (15 min)
6. Decisions and action items (10 min)

Fill in from project context:
- PROJECT_NAME — from project-state.md
- SPRINT_NUMBER — from project-state.md or PM
- Key risks/blockers — from risk-register.md or progress report
- Materials for preparation — list relevant files PM should review before the meeting

---

### Step 5 — Show Draft to PM (Mode B)

Output to chat:
- Summary line: "Meeting: {Type} | {Date and Time} | Participants: {N}"
- Full agenda draft

Ask:
"Draft is ready. Confirm or request changes?
1. Confirm → I will save files and create the Calendar event.
2. Change participants / agenda items / time → specify edits."

**Do not create files or the Calendar event until PM confirms.**

---

### Step 6 — Create Calendar Event

**If PM confirms:**

Attempt to create the event via Google Calendar MCP:
- **Title:** `[{MeetingType}] {ProjectName} — {ShortDescription}`
  Example: `[Sprint Planning] ClientBoard — Sprint 3`
- **Date/time:** from agenda
- **Participants:** email addresses from stakeholder-map.md (if available); otherwise skip
- **Description:** agenda items (brief, bulleted) + link to agenda file path

**Fallback if Calendar MCP is unavailable:**
Add section "Calendar Event Parameters" to the saved agenda file:
```
Title: [as above]
Date/Time: {DATE} {TIME}
Duration: {DURATION} min
Participants: {LIST}
Description: [paste agenda items]
```
Notify PM: "Calendar MCP unavailable. Event parameters saved in the agenda file — create the event manually."

---

### Step 7 — Save Files and Update State

1. Create `meetings/agenda-{type}-{YYYY-MM-DD}.md`.
2. Create `meetings/protocol-{type}-{YYYY-MM-DD}.md` (blank template for post-meeting use).
3. For `launch-status` only: create `meetings/email-tpl-meeting-status.md` by populating the matching language template (`templates/email-tpl-meeting-status-en.md` or `ru.md`). Pre-fill PROJECT_NAME, PM_NAME, meeting date, next meeting date. Leave decisions/tasks as placeholders — PM fills after the meeting.
4. Update `project-state.md`: add artifact records with status `draft`.
5. Write to `logs/log.md`:
   `{DATE}: coordinate-meeting — type: {TYPE}, created meetings/agenda-{type}-{DATE}.md + meetings/protocol-{type}-{DATE}.md`
6. Output to chat:
   - "Files saved: meetings/agenda-{type}-{DATE}.md, meetings/protocol-{type}-{DATE}.md"
   - "After the meeting, fill in the protocol: decisions, tasks, owners, deadlines."
   - For `launch-status`: "Use meetings/email-tpl-meeting-status.md to send the meeting status via send-email."

---

## Templates

| File | Purpose |
|------|---------|
| `templates/meeting-agenda-template-en.md` | Agenda + protocol template (EN) |
| `templates/meeting-agenda-template-ru.md` | Agenda + protocol template (RU) |
| `templates/email-tpl-meeting-status-en.md` | Launch status email template E8 (EN) |
| `templates/email-tpl-meeting-status-ru.md` | Launch status email template E8 (RU) |

---

## Dependencies

**Reads (optional):**
- `project-state.md` — project name, phase, sprint number
- `01-initiation/stakeholder-map.md` — participants
- `02-planning/comm-plan.md` — communication preferences
- `02-planning/project-plan.md` — milestones and backlog
- `01-initiation/risk-register.md` — top risks (go-no-go)
- `03-execution/comparison-table.xlsx` — prototype comparison (demo-client)
- `reports/progress-report-*.md` — latest progress (sprint-demo)
- `reports/weekly-status-*.md` — latest status (launch-status)
- `03-execution/launch-checklist.md` — launch readiness (launch-status)

**External actions:**
- Google Calendar MCP — event creation (primary path)
- Fallback: parameters saved in agenda file for manual creation

**Passes data to:**
- `generate-meeting-protocol` — protocol file for post-meeting notes (task #16)
- `send-email` — email-tpl-meeting-status.md for launch-status distribution (E8, level 3)

---

## Constraints

- Requires meeting type and date/time to start
- Calendar event created only after PM confirmation (Mode B)
- Skill does not conduct the meeting or fill the protocol — PM fills protocol after the meeting
- One invocation = one meeting; recurring meetings → separate invocations per occurrence
- For `sprint-planning`/`sprint-demo`/`launch-status`, include sprint number or specific date in file name
- Email distribution after `launch-status` is executed via `send-email`, not automatically
- Fallback mode (no Calendar MCP) does not block agenda/protocol file creation
