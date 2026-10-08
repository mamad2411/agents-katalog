---
name: generate-response-plan
description: "Generates an incident response plan (response-plan-{id}.md) for Phase 5 — Launch. Covers task #27 of the project management agent. Handles mixed incident types: Technical (system failures, critical bugs, infrastructure), Operational (deployment failures, process breakdowns), and Business (KPI collapse, PR crises, legal issues). Classifies severity (Critical / High / Medium / Low) from PM description; enriches the plan with team and stakeholder data from project files. The plan includes: incident description, impact assessment, response team, root cause analysis, action plan with owners, resolution timeline, escalation path, communication plan, and post-incident tasks. Mode B: agent prepares draft, PM reviews and approves. Triggers EN: 'incident response plan', 'incident occurred', 'system down'."
---

# Skill: generate-response-plan

Generates an incident response plan for Phase 5 — Launch. Supports Technical,
Operational, and Business incident types. Classifies severity from PM description,
reads project context files, and produces a structured response-plan-{id}.md.
Mode B: agent prepares a draft, PM reviews and approves.

---

## Triggers

**Russian:** «инцидент», «план реагирования», «произошёл инцидент», «сбой системы», «критическая ошибка», «проблема при запуске», «составь план реагирования», «что делать при инциденте»
**English:** "incident response plan", "incident occurred", "system down", "generate response plan", "launch incident", "critical bug response", "production issue"

---

## Language Detection

- Request in Russian → template `response-plan-ru.md`, responses in Russian
- Otherwise → template `response-plan-en.md`, responses in English

---

## Input

| Data | Required | Source |
|------|:--------:|--------|
| Incident description (what happened, when, where) | yes | PM in chat |
| Incident type and severity | no | Inferred from description or PM asked |
| Project name and current phase | no | `project-state.md` |
| Team composition and roles | no | `02-planning/resource-plan.md` or `project-state.md` |
| Escalation contacts | no | `01-initiation/stakeholder-map.md` |
| Current plan milestones | no | `02-planning/project-plan.md` |
| Registered risks | no | `01-initiation/risk-register.md` |

## Output

| File | Project path | Task |
|------|-------------|------|
| `response-plan-{INCIDENT_ID}.md` | `03-execution/` | #27 |

Incident ID format: `INC-YYYYMMDD-NNN` (sequential within the project).
File name example: `response-plan-INC-20260425-001.md`

---

## Instructions

### Step 1 — Guard-rail and Gather Incident Data

**Guard-rail — verify request type.**
If the request is about incident management methodology in general, not a specific incident
in a running project → respond:
"generate-response-plan creates an incident response plan for a specific incident in
Phase 5 (Launch). Describe what happened in your project — I'll generate the plan."
Do not start the workflow.

**Ask PM to describe the incident** if not provided in the request:
"To generate the response plan, tell me:
1. What happened? (brief description)
2. When was it detected?
3. What is affected? (system, process, users)"

Do not proceed to Step 2 until the PM provides at least a brief incident description.

---

### Step 2 — Classify Incident Type and Severity

**Determine incident type from description:**

| Indicators | Type |
|-----------|------|
| System failure, critical bug, infrastructure down, deployment error, data loss | Technical |
| Process breakdown, team blocker, deployment failure due to process, resource failure | Operational |
| KPI below threshold, PR/reputational crisis, legal issue, marketing campaign failure | Business |

If the description contains indicators of multiple types → use the primary type (most impactful).
If type is unclear → ask: "Is this primarily a technical failure, an operational issue, or a business-level problem?"

**Determine severity from description:**

| Severity | Criteria |
|----------|---------|
| Critical | System completely down, major data loss, legal/compliance breach, project fully blocked |
| High | Major functionality degraded, significant user impact, project at risk of delay |
| Medium | Partial service impact, workaround available, limited user impact |
| Low | Minor issue, minimal impact, no immediate threat to delivery |

If severity cannot be determined from description → ask:
"How would you rate the severity?
- Critical — system down / project blocked
- High — major degradation / at risk
- Medium — partial impact, workaround exists
- Low — minor, no immediate threat"

---

### Step 3 — Gather Context from Project Files

Read `project-state.md` to obtain:
- Project name
- Current phase

Read `02-planning/resource-plan.md` (if available) → extract team roles and names for the Response Team section.
Read `01-initiation/stakeholder-map.md` (if available) → extract Approver/Sponsor contacts for the Escalation Path.
Read `01-initiation/risk-register.md` (if available) → check if the incident matches a registered risk; if yes, note the risk ID.
Read `02-planning/project-plan.md` (if available) → extract current milestone/deadline to assess timeline impact.

**If files are unavailable:** continue with PM-provided data and placeholder values. Notify in chat:
"[Filename] not found — the corresponding section will use placeholders. Fill in manually after saving."

**Generate Incident ID:**
- Scan `03-execution/` for existing `response-plan-*.md` files.
- Increment the sequence number: if no files exist → 001; if files exist → next number.
- Format: `INC-{YYYYMMDD}-{NNN}` using today's date.

---

### Step 4 — Build the Response Plan

Load the template corresponding to the detected language:
- Russian → `templates/response-plan-ru.md`
- English → `templates/response-plan-en.md`

Populate the template:

**Incident overview (§1):**
- INCIDENT_ID — generated in Step 3
- PROJECT_NAME, DATE_REPORTED, REPORTED_BY, SEVERITY, INCIDENT_TYPE — from Step 2 and PM data
- Incident description — PM's description, normalized to 2–4 clear sentences

**Impact assessment (§2):**
- Fill AFFECTED_SYSTEMS, AFFECTED_PROCESSES from description
- AFFECTED_USERS — from stakeholder-map or PM's data
- Project blocked: Yes if Critical; otherwise infer from description
- SEVERITY_RATIONALE — 1–2 sentences explaining the severity classification

**Response team (§3):**
- PM_NAME — from project-state.md or resource-plan.md
- Technical Lead, Business Owner — from resource-plan.md if available; otherwise `[TBD]`
- Incident Lead — default to PM if no dedicated role; adjust if PM specifies someone else

**Root cause analysis (§4):**
- PROBABLE_CAUSE — based on PM's description; prefix with "Initial assessment:" if uncertain
- CONTRIBUTING_FACTORS — list 2–3 inferred factors; mark speculative ones with "(preliminary)"
- KNOWN_RISK — check risk-register.md result from Step 3

**Action plan (§5):**
- Generate 3–5 actions appropriate for the incident type and severity:
  - Technical: isolate → diagnose → fix → verify → restore service
  - Operational: identify blocker → escalate → reallocate resources → resume process
  - Business: assess scope → brief stakeholders → define response → execute corrective action
- Assign owners from team data if available; otherwise `[OWNER]`
- Set deadlines: Critical → hours, High → same day, Medium/Low → days; use `[TIME]` if unknown

**Resolution timeline (§6):**
- Fill "Incident detected" with the time from PM
- Set target times based on severity: Critical — resolution within 4–8h, High — within 24h, Medium — within 3 days

**Escalation path (§7):**
- Fill contacts from stakeholder-map.md if available; otherwise keep placeholders
- Adjust thresholds if PM specifies escalation policy

**Communication plan (§8):**
- Identify 3–4 key stakeholder groups from stakeholder-map.md or comm-plan.md
- Define what to communicate at each stage: immediate notification, status update, closure
- Set "Sender" to PM by default
- Method: reference comm-plan.md channels if available; otherwise Email/Call

**Post-incident tasks (§9):**
- Keep the 4 standard tasks from template
- Add project-specific tasks if PM mentions them

---

### Step 5 — Show Draft to PM

Output to chat:
- One-line summary: "Incident response plan INC-{ID} — {TYPE}, severity: {SEVERITY}"
- Sections §1 (Incident Description) and §2 (Impact Assessment) as preview

Ask:
"Draft is ready. Would you like to:
1. Save as is → I will create the file.
2. Adjust severity, type, or description → specify changes.
3. Update team or escalation contacts → provide the data."

**Do not create the file until PM responds.**

---

### Step 6 — Save File and Update State

1. Create `response-plan-{INCIDENT_ID}.md` in `{project}/03-execution/`.
2. Update `project-state.md`: add artifact record → status `draft`.
3. Write to `logs/log.md`:
   `{DATE}: generate-response-plan — created 03-execution/response-plan-{INCIDENT_ID}.md, type: {TYPE}, severity: {SEVERITY}`
4. Output to chat:
   - "File saved: 03-execution/response-plan-{INCIDENT_ID}.md"
   - Next step: "Response plan is ready. Review actions in §5 and confirm assignments with the team. After the incident is resolved, update §6 (timeline actuals) and §9 (post-incident tasks) in the file."

---

## Templates

| File | Purpose |
|------|---------|
| `templates/response-plan-en.md` | Incident response plan template (EN) |
| `templates/response-plan-ru.md` | Incident response plan template (RU) |

---

## Dependencies

**Reads (optional):**
- `project-state.md` — project name, current phase
- `02-planning/resource-plan.md` — team roles and contacts
- `01-initiation/stakeholder-map.md` — escalation and communication contacts
- `01-initiation/risk-register.md` — registered risks for cross-reference
- `02-planning/project-plan.md` — milestones and timeline impact assessment

**Passes data to:**
- `send-email` — for external stakeholder notifications per §8 (Communication Plan), autonomy level per `comm-plan.md`

---

## Constraints

- Mode B: PM reviews the draft before the file is created
- Requires at least a brief incident description from PM to start; does not generate a plan from empty input
- One incident per invocation; multiple incidents → separate skill calls, each with its own INC-ID
- Does not modify risk-register.md or project-plan.md — those are updated manually by PM post-incident
- Does not trigger send-email automatically — PM initiates notifications from §8 manually or by calling send-email
- Fallback if all project files are unavailable: generates a template-based plan with PM-provided data and placeholders
- Severity and type classification is explicit — agent states its reasoning and asks for confirmation if uncertain
