---
name: monitor-progress
description: "Monitors project progress across 6 operational modes: sprint progress report, deviation check (schedule vs budget), launch stream synchronization, actual data collection for project closure, weekly status report (scheduled), and daily deviation check (scheduled). Reads project-plan, project-budget, and Jira data to produce structured reports. Triggers email notifications via send-email for deviations (level 2 draft) and weekly status (level 1 autonomous). Falls back to file-only output if Jira MCP is unavailable. Covers PM tasks #18, #19, #25, #28 and scheduled tasks weekly-status (Р1) and daily-deviation (Р2). Triggers EN: 'check progress', 'project status', 'weekly report'."
---

# Skill: monitor-progress

Monitors project execution across 6 modes — from sprint progress tracking to
stream synchronization and final data collection. Reads Jira, project-plan, and
project-budget. Generates structured reports; triggers email notifications for
deviations and weekly status. Falls back gracefully when Jira is unavailable.

---

## Triggers

**Russian:** «проверь прогресс», «статус проекта», «отчёт по прогрессу», «еженедельный отчёт», «проверь отклонения», «отклонения по срокам/бюджету», «синхронизация потоков», «собери фактические данные», «данные для закрытия»
**English:** "check progress", "project status", "progress report", "weekly status", "check deviations", "deviation report", "sync streams", "collect actual data", "closing data"

---

## Language Detection

- Request in Russian → templates `*-ru.md`, all outputs in Russian
- Otherwise → templates `*-en.md`, all outputs in English

---

## Modes

| Mode | Task | Phase | Trigger type | Output |
|------|------|-------|-------------|--------|
| `progress-report` | #18 | 4 | command | `progress-report-{date}.md` |
| `deviation-check` | #19 | 4 | command / schedule (daily) | `deviation-report-{date}.md` + email E4 |
| `sync-streams` | #25 | 5 | command / schedule (weekly Mon, phase 5 only) | `sync-report-{date}.md` + email E5 |
| `actual-data` | #28 | 6 | command | `actual-data-report.xlsx` (schema) |
| `weekly-status` | Р1 | 3–5 | scheduled (Mon 9:00) | `weekly-status-{date}.md` + email E7 |
| `daily-deviation` | Р2 | 3–5 | scheduled (Mon–Fri 9:00) | `daily-deviation-{date}.md` |

---

## Input

| Data | Required | Source |
|------|:--------:|--------|
| Mode (explicit or inferred) | yes | PM in chat or scheduled task prompt |
| project-state.md | yes | project root |
| project-plan.md | yes (most modes) | `02-planning/` |
| project-budget.xlsx | for deviation/closure | `02-planning/` |
| Jira sprint data | preferred | Jira MCP (fallback: PM provides manually) |
| Stream reports (sync-streams) | yes | `reports/` — latest progress-report-*.md |
| All Jira data (actual-data) | yes | Jira MCP (fallback: PM provides) |

## Output

| File | Path | Mode |
|------|------|------|
| `progress-report-{date}.md` | `reports/` | progress-report |
| `deviation-report-{date}.md` | `reports/` | deviation-check, daily-deviation |
| `sync-report-{date}.md` | `reports/` | sync-streams |
| `actual-data-report.xlsx` | `06-closure/` | actual-data |
| `weekly-status-{date}.md` | `reports/` | weekly-status |
| Email E4 (deviation deadline) | via send-email | deviation-check (level 2) |
| Email E5 (stream sync) | via send-email | sync-streams (level 2) |
| Email E7 (weekly status) | via send-email | weekly-status (level 1) |

---

## Instructions

### Step 1 — Determine Mode

Determine the mode from the PM's request or the scheduled task prompt.

| Cues | Mode |
|------|------|
| "progress", "sprint tasks", "what's done", "task status" | `progress-report` |
| "deviations", "overdue", "behind schedule", "over budget" | `deviation-check` |
| "stream sync", "launch streams", "dev/marketing/ops status" | `sync-streams` |
| "actual data", "closing data", "final figures", "project closure" | `actual-data` |
| "weekly status", "weekly report", "статус недели", "еженедельный отчёт" — or scheduled prompt contains "weekly-status" | `weekly-status` |
| "daily check", "daily deviation", "ежедневная проверка" — or scheduled prompt contains "daily-deviation" | `daily-deviation` |

If mode is ambiguous and the request came from PM in chat → ask:
"Which report do you need?
1. Sprint progress — task completion status (Phase 4)
2. Deviation check — schedule and budget deviations (Phase 4)
3. Stream sync — dev/marketing/ops synchronization (Phase 5)
4. Actual data — final figures for project closure (Phase 6)"

**Phase validation:**
- `sync-streams`: only available in Phase 5. If current phase ≠ 5 → inform PM and stop.
  Message: "sync-streams is only available in Phase 5 (Launch). Current phase: {PHASE}. If you need current sprint progress data, use progress-report mode instead."
- `actual-data`: only available in Phase 6. If current phase ≠ 6 → inform PM and stop.
  Message: "actual-data collection is only available in Phase 6 (Closure). Current phase: {PHASE}."

---

### Step 2 — Read Project Context

Always read:
- `project-state.md` → project name, current phase, sprint number, last update date

Read per mode:

| Mode | Files to read |
|------|---------------|
| `progress-report` | `02-planning/project-plan.md` |
| `deviation-check`, `daily-deviation` | `02-planning/project-plan.md`, `02-planning/project-budget.xlsx` |
| `sync-streams` | latest `reports/progress-report-*.md` (last 1–2), `03-execution/launch-checklist.md` |
| `actual-data` | `02-planning/project-plan.md`, `02-planning/project-budget.xlsx` |
| `weekly-status` | `02-planning/project-plan.md`, latest `reports/progress-report-*.md` (if exists) |

If files are not found → continue with available data, note missing files in the report with placeholder `[DATA NOT AVAILABLE — fill manually]`.

---

### Step 3 — Query Jira (if available)

Attempt to retrieve data via Jira MCP:

| Mode | What to query |
|------|--------------|
| `progress-report` | Current sprint tasks — status, assignee, completion % |
| `deviation-check`, `daily-deviation` | Overdue tasks, tasks at risk (due within 3 days) |
| `sync-streams` | Open tasks by epic/label per stream (dev, marketing, ops) |
| `actual-data` | All closed tasks: actual hours, completion dates, story points |
| `weekly-status` | Sprint velocity, completed vs planned, overdue count |

**Fallback if Jira MCP unavailable:**
- Continue without Jira data
- Mark all Jira-dependent fields with the language-matched placeholder:
  - EN: `[JIRA DATA UNAVAILABLE — fill manually]`
  - RU: `[JIRA НЕДОСТУПЕН — заполнить вручную]`
- Notify in chat (match detected language):
  - EN: "Jira MCP unavailable — report generated with placeholders. Fill in Jira sections manually."
  - RU: "Jira MCP недоступен — отчёт сгенерирован с плейсхолдерами. Заполни разделы Jira вручную."

---

### Step 4 — Generate Report

Load the template matching mode and language:

| Mode | Template (EN) | Template (RU) |
|------|--------------|---------------|
| `progress-report` | `templates/progress-report-template-en.md` | `templates/progress-report-template-ru.md` |
| `deviation-check`, `daily-deviation` | `templates/deviation-report-template-en.md` | `templates/deviation-report-template-ru.md` |
| `sync-streams` | `templates/sync-report-template-en.md` | `templates/sync-report-template-ru.md` |
| `actual-data` | `templates/actual-data-report-schema.md` | (same, bilingual schema) |
| `weekly-status` | `templates/weekly-status-template-en.md` | `templates/weekly-status-template-ru.md` |

Populate all template sections with data from Step 2 + Step 3.

**Deviation assessment rules:**
- Schedule deviation: task overdue by >0 days → flag as deviation
- Budget deviation: actual spend > planned by >5% → flag as deviation
- Critical threshold: >10% schedule delay or >10% budget overrun → mark as `CRITICAL`
- No deviations found → for `deviation-check` and `daily-deviation`: write to `logs/log.md` "no deviations" and STOP (do not generate report file)

**For `actual-data` mode:**
- Output is an xlsx schema — generate the schema structure per `templates/actual-data-report-schema.md`
- Save as `06-closure/actual-data-report.xlsx` (structure only; PM fills actual values from populated template or Jira export)

---

### Step 5 — Handle Email (where applicable)

| Mode | Email template | Autonomy level | Condition |
|------|---------------|---------------|-----------|
| `deviation-check` | `email-tpl-deviation-deadline-{lang}.md` | 2 (draft for PM) | Deviations found |
| `sync-streams` | `email-tpl-deviation-sync-{lang}.md` | 2 (draft for PM) | Desync detected |
| `weekly-status` | `email-tpl-weekly-status-{lang}.md` | 1 (autonomous) | Always |
| `daily-deviation` | — | — | None (no email) |

**Level 1 (autonomous):** Generate email draft → pass to `send-email` for immediate dispatch.
**Level 2 (draft):** Generate email draft in `reports/email-draft-{mode}-{date}.md` → notify PM: "Email draft ready — review and confirm before sending via send-email."

Load the matching email template, populate with report key findings, recipients from `01-initiation/stakeholder-map.md` (or `comm-plan.md`).

---

### Step 6 — Save Files and Update State

1. Save the report file to the correct path (see Output table).
2. For `actual-data` mode: save `06-closure/actual-data-report.xlsx` schema.
3. Update `project-state.md`:
   - Add artifact record with status `completed` and date.
   - For `weekly-status`: update field `last_weekly_report`.
   - For `deviation-check`/`daily-deviation`: update field `last_deviation_check`.
4. Write to `logs/log.md`:
   `{DATE}: monitor-progress [{MODE}] — {RESULT}. Saved: reports/{FILENAME}`
   - RESULT examples: "3 deviations found", "no deviations", "report generated", "Jira unavailable — manual fill needed"
5. Output to chat:
   - File saved path
   - Key findings summary (2–5 bullet points)
   - Email action (if applicable): "Email draft ready at reports/email-draft-{mode}-{date}.md"
   - If deviations are critical: "⚠️ CRITICAL deviation detected — immediate PM attention required."

---

## Templates

| File | Purpose |
|------|---------|
| `templates/progress-report-template-en.md` | Sprint progress report (EN) — Task #18 |
| `templates/progress-report-template-ru.md` | Sprint progress report (RU) — Task #18 |
| `templates/deviation-report-template-en.md` | Deviation report (EN) — Task #19, Р2 |
| `templates/deviation-report-template-ru.md` | Deviation report (RU) — Task #19, Р2 |
| `templates/weekly-status-template-en.md` | Weekly status report (EN) — Р1 |
| `templates/weekly-status-template-ru.md` | Weekly status report (RU) — Р1 |
| `templates/sync-report-template-en.md` | Stream sync report (EN) — Task #25 |
| `templates/sync-report-template-ru.md` | Stream sync report (RU) — Task #25 |
| `templates/actual-data-report-schema.md` | xlsx schema for actual data collection — Task #28 |
| `templates/email-tpl-deviation-deadline-en.md` | Email E4 — deviation notification (EN) |
| `templates/email-tpl-deviation-deadline-ru.md` | Email E4 — deviation notification (RU) |
| `templates/email-tpl-deviation-sync-en.md` | Email E5 — stream desync notification (EN) |
| `templates/email-tpl-deviation-sync-ru.md` | Email E5 — stream desync notification (RU) |
| `templates/email-tpl-weekly-status-en.md` | Email E7 — weekly status distribution (EN) |
| `templates/email-tpl-weekly-status-ru.md` | Email E7 — weekly status distribution (RU) |

---

## Dependencies

**Reads (required):**
- `project-state.md` — project name, phase, sprint number
- `02-planning/project-plan.md` — planned milestones, tasks, deadlines
- `02-planning/project-budget.xlsx` — budget plan (deviation modes)

**Reads (optional):**
- `01-initiation/stakeholder-map.md` — email recipients
- `02-planning/comm-plan.md` — communication preferences
- `reports/progress-report-*.md` — previous reports for trend comparison
- `03-execution/launch-checklist.md` — launch readiness (sync-streams)

**External actions:**
- Jira MCP — sprint and task data (fallback: PM provides manually)
- `send-email` skill — email dispatch (E4 level 2, E5 level 2, E7 level 1)

**Writes:**
- `reports/progress-report-{date}.md`
- `reports/deviation-report-{date}.md`
- `reports/sync-report-{date}.md`
- `reports/weekly-status-{date}.md`
- `reports/daily-deviation-{date}.md`
- `06-closure/actual-data-report.xlsx`
- `project-state.md` (status update)
- `logs/log.md` (action record)

---

## Constraints

- `sync-streams` mode is only available in Phase 5
- `actual-data` mode is only available in Phase 6
- Does NOT make decisions about deviations — generates report and notifies PM
- Does NOT update project-plan.md — PM decides how to respond to deviations
- For `deviation-check` and `daily-deviation`: if no deviations found, logs the check and stops — no report file created
- Fallback mode does not block report generation — produces report with placeholders
- One invocation = one mode; do not combine modes in a single run
- Email for `weekly-status` (E7, level 1) is sent autonomously — no PM confirmation required
- Email for `deviation-check` (E4) and `sync-streams` (E5) are level 2 — PM must confirm before sending
