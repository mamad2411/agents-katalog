---
name: generate-approval-letter
description: "Generates an approval-letter.md email body and an email-tpl-approval.md
  template for Phase 2 — Planning. Reads project-plan.md, project-budget.xlsx, and
  resource-plan.md to compose a formal approval request addressed to all Approver-level
  stakeholders from stakeholder-map.md. Produces two artifacts: the letter email body
  (approval-letter.md) and the send-email template (email-tpl-approval.md). Covers
  task #12 of the project management agent. Mode B: agent prepares draft, PM reviews
  and confirms before sending. Email level 3 — requires PM confirmation.
  Triggers RU: «отправь план на согласование», «письмо на согласование плана», «согласуй
  план с заказчиком», «запроси утверждение плана», «generate-approval-letter», «составь
  письмо на согласование».
  Triggers EN: 'send plan for approval', 'approval letter for project plan', 'request
  plan approval', 'generate approval letter', 'plan sign-off email', 'get plan approved'."
---

# Skill: generate-approval-letter

Generates a project plan approval request for Phase 2 — Planning. Reads the project
plan, budget, and resource plan; extracts Approver-level stakeholders from the
stakeholder map; and produces two artifacts: the approval letter email body
(approval-letter.md) and the send-email template (email-tpl-approval.md).
Mode B: agent prepares draft, PM reviews and confirms before sending (level 3).

---

## Triggers

**Russian:** «отправь план на согласование», «письмо на согласование плана», «согласуй план с заказчиком», «запроси утверждение плана», «составь письмо на согласование», «нужно согласовать план»
**English:** "send plan for approval", "approval letter for project plan", "request plan approval", "generate approval letter", "plan sign-off email", "get plan approved"

---

## Language Detection

- Request in Russian → templates with `-ru` suffix, responses in Russian
- Otherwise → templates with `-en` suffix, responses in English

---

## Input

| Data | Required | Source |
|------|:--------:|--------|
| Stakeholder map | yes | `01-initiation/stakeholder-map.md` |
| Project plan | yes | `02-planning/project-plan.md` |
| Project budget | no | `02-planning/project-budget.xlsx` |
| Resource plan | no | `02-planning/resource-plan.md` |
| Project charter | no | `01-initiation/project-charter.md` — name, PM, sponsor |

## Output

| File | Project path | Format | Description |
|------|-------------|--------|-------------|
| `approval-letter.md` | `02-planning/` | .md | Email body — formal approval request |
| `email-tpl-approval.md` | `02-planning/` | .md | send-email template: To, Subject, Body, Attachments |

---

## Instructions

### Step 1 — Check Dependencies

**Guard-rail — check request type.**
If the request is about updating the plan, replanning, or modifying artifacts →
respond: "generate-approval-letter composes an approval request for the ready plan,
not the plan itself. Use generate-project-plan to update the plan first, then run
generate-approval-letter again."
Do not start workflow.

Check for required files:
1. `01-initiation/stakeholder-map.md`
2. `02-planning/project-plan.md`

**If stakeholder-map.md not found:**
Stop. Report: "To identify recipients, the stakeholder map is required.
Run generate-stakeholder-map (task #3) first, then run generate-approval-letter."

**If project-plan.md not found:**
Stop. Report: "To compose the letter, the project plan is required.
Run generate-project-plan (task #7) first, then run generate-approval-letter."

**If both files found:** proceed to Step 2.

---

### Step 2 — Extract Data from Input Files

**From stakeholder-map.md:**
- All stakeholders with status `Approver` (or equivalent: Утверждающий, Sign-off authority, Decision maker)
- For each: name, role/title, email (if available)
- If no Approver found: ask PM — "No Approvers found in stakeholder map. Please specify
  who should receive the letter." Record PM's answer as the recipient list. In Steps 3–4,
  use this data instead of stakeholder-map.md.

**From project-plan.md:**
- Project name, PM
- Number of phases, overall duration (start date → end date)
- 3–5 key milestones with dates
- Current phase and status

**From project-charter.md (if available):**
- Project name (if not found in project-plan.md)
- Project sponsor — add to CC

**From project-budget.xlsx (if available):**
- Total budget amount
- Risk reserve (if present)

**From resource-plan.md (if available):**
- Total person-months or FTE summary — one line

---

### Step 3 — Compose Email Body (approval-letter.md)

Follow the schema from `templates/approval-letter-{lang}.md`.

**Letter structure:**
1. **Greeting** — to addressees (by name if single recipient; formal greeting if multiple)
2. **Context** — 2–3 sentences: project name, Phase 2 complete, package ready for review
3. **Document package** — list with brief description of each document
4. **Key project parameters** — compact summary: start, end, milestones, budget (if available)
5. **Call to action** — clear request: what to do, response deadline (default: 3 business days)
   Response options: "Approved" / "Requires revision" (with comments)
6. **Signature** — PM name, title, contact

**Tone:** formal, concise. Length: 200–350 words.

---

### Step 4 — Compose send-email Template (email-tpl-approval.md)

Follow the schema from `templates/email-tpl-approval-{lang}.md`.

**email-tpl-approval.md structure:**
```
To: [Approver list from stakeholder-map]
CC: [Sponsor if found]
Subject: [Project Name] — Request for Plan Approval
Attachments:
  - project-plan.docx (convert from project-plan.md)
  - project-budget.xlsx (if available)
  - resource-plan.docx (convert from resource-plan.md, if available)
Body: [content of the letter composed in Step 3]
Autonomy level: 3 — send only after PM confirmation
```

---

### Step 5 — Show Draft and Save

1. Create `approval-letter.md` in `{project}/02-planning/`.
2. Create `email-tpl-approval.md` in `{project}/02-planning/`.
3. Show in chat:
   - Confirmation: "Files saved to 02-planning/."
   - Full content of `approval-letter.md` for PM review.
   - Recipient list (To) and attachments for review.
   - Question: "Letter ready. Confirm to send via Gmail, or provide edits."
4. **Do not trigger send-email without explicit PM confirmation** — autonomy level 3.
5. On PM confirmation: hand off to `send-email` skill with `02-planning/email-tpl-approval.md`.
   On Gmail unavailable: save draft, notify PM with manual send instructions.
6. Write to `logs/log.md`: date, skill, files created, recipients, status.
7. Update `project-state.md`: `approval-letter.md` → "pending approval".

---

## Templates

| File | Purpose |
|------|---------|
| `templates/approval-letter-ru.md` | Email body schema (RU) |
| `templates/approval-letter-en.md` | Email body schema (EN) |
| `templates/email-tpl-approval-ru.md` | send-email template schema (RU) |
| `templates/email-tpl-approval-en.md` | send-email template schema (EN) |

---

## Dependencies

**Reads:**
- `01-initiation/stakeholder-map.md` — Approver stakeholders (required)
- `02-planning/project-plan.md` — phases, milestones, timeline (required)
- `01-initiation/project-charter.md` — project name, PM, sponsor (optional)
- `02-planning/project-budget.xlsx` — total budget (optional)
- `02-planning/resource-plan.md` — FTE summary (optional)

**Passes data to:**
- `send-email` — email-tpl-approval.md → Gmail (level 3)

---

## Constraints

- Mode B: letter is a draft for PM review; sending requires PM confirmation (level 3)
- Does not modify project-plan.md or any other source files
- If no Approver in stakeholder-map: asks PM for clarification, does not stop
- Default response deadline: 3 business days; PM may adjust before confirmation
- Without project-budget.xlsx and resource-plan.md: letter is generated without those data points
- Gmail MCP unavailable fallback: save to file, PM sends manually
- Single project per invocation
