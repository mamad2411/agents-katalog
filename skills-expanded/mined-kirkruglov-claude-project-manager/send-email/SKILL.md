---
name: send-email
description: "Internal service skill for delivering project emails via Gmail MCP. Activated automatically when any project management skill needs to send an email: deadline reminders (E6), weekly status reports (E7), approval requests (E3), client questionnaires (E1), deviation alerts (E4, E5), or meeting notifications (E8). Handles three autonomy levels: Level 1 sends immediately without confirmation, Level 2 sends with PM copied, Level 3 shows a draft and waits for PM approval. Converts .md attachments to .docx for external recipients using the Cowork docx skill. Falls back to a saved .md draft when Gmail is unavailable. Not triggered directly by users — activated by other agent skills passing email_type, recipients, body, and autonomy_level. RU triggers (from calling skills): 'отправить письмо', 'send-email', 'уведомить стейкхолдеров'. EN triggers: 'send email', 'notify stakeholders', 'deliver report'."
---

# Skill: send-email

Internal service skill for sending project emails via Gmail MCP. Called exclusively by other agent skills — not directly by the user. Receives a rendered email from the calling skill, applies autonomy level rules, converts attachments if needed, and delivers via Gmail or saves a fallback draft.

---

## Activation Context

This skill is activated when another agent skill instructs Claude to send an email. The calling skill provides all content; send-email handles delivery, autonomy logic, and fallback.

**Calling skills:** generate-questionnaire, generate-approval-letter, monitor-progress, coordinate-meeting, coordinate-executors.

---

## Language Detection

Determine language from `project-state.md` field `language`. If absent: scan project artifacts for Cyrillic → RU. Default: EN.

---

## Input

Parameters passed by the calling skill:

| Parameter | Required | Description |
|-----------|:--------:|-------------|
| `email_type` | yes | E1–E8 (email type from artifacts registry) |
| `to` | yes | Recipient email(s) |
| `subject` | yes | Email subject (already filled by caller) |
| `body_md` | yes | Email body in Markdown (already rendered by caller) |
| `autonomy_level` | yes | 1 / 2 / 3 |
| `attachments` | no | File paths (.md, .xlsx) |
| `convert_to_docx` | no | Convert .md attachments to .docx. Default: false |
| `cc_pm` | no | PM email for Level 2 (if absent — read from project-state.md) |

## Output

| Result | Path | Condition |
|--------|------|-----------|
| Email sent via Gmail | — (external) | Level 1/2, Gmail available; Level 3 confirmed |
| `drafts/email-draft-{type}-{YYYY-MM-DD}.md` | `drafts/` | Level 3 pending; Gmail unavailable |
| Log entry in `logs/log.md` | `logs/` | Always |

---

## Instructions

### Step 1 — Guard-rail

If called directly by a user (not as part of a skill chain):
Detection: input is natural language without structured parameters — at least one of `email_type`, `to`, `subject`, `body_md`, `autonomy_level` is absent.
Respond: "send-email is an internal service skill activated automatically during email delivery. To send a project email, trigger the relevant skill (e.g., coordinate-executors for reminders, generate-approval-letter for approvals)."

**Caller contract (for calling skills):** `body_md` MUST be fully rendered Markdown text — not a file path, template variable, or reference. The calling skill is responsible for loading its own template from `templates/`, populating all placeholders, and passing the result as a string. send-email has no `templates/` folder of its own.

### Step 2 — Validate Parameters

1. Check required fields: `email_type`, `to`, `subject`, `body_md`, `autonomy_level`.
   - If any field is missing → ask PM for the missing data.
2. If `email_type` is unknown or outside E1–E8 → default to autonomy level 3.
3. Read `project-state.md`: get `pm_email`, `project_name`, `language`.

### Step 3 — Convert Attachments

If `attachments` is set AND `convert_to_docx = true`:
- Level 1/2: convert here, before sending.
- Level 3: defer conversion until PM confirms — perform at the start of Step 5.

For each file (when converting):
- `.md` files → convert via Cowork docx skill → produce `.docx` (same filename).
- `.xlsx` files → use as-is.
- Other formats → attach as-is, warn PM in chat.
- On conversion error → log error, attach original `.md`, notify PM.

### Step 4 — Apply Autonomy Level

| Level | Email Types | Action |
|-------|------------|--------|
| 1 — auto | E6, E7 | Send immediately, no preview |
| 2 — CC PM | E4, E5 | Add PM to CC, send immediately |
| 3 — confirm | E1, E2, E3, E8 | Show draft, wait for PM approval |

**Level 3 flow:**

1. Save draft to `drafts/email-draft-{email_type}-{YYYY-MM-DD}.md`.
2. Display in chat:
   ```
   Draft ready ({email_type}):
   — To: {to}
   — Subject: {subject}
   — Attachments: {list or "none"}
   [body preview: first 5 lines or full if < 15 lines]

   Confirm: type "send" / "отправить" — or provide edits.
   ```
3. Wait for PM response:
   - `"send"`, `"отправить"`, `"confirm"`, `"подтвердить"` → proceed to Step 5.
   - Edit text → apply changes, update draft, show again.
   - `"cancel"`, `"отмена"` → log "cancelled by PM", end skill.

### Step 5 — Send via Gmail MCP

**Primary path (Gmail available):**

Call Gmail MCP:
- `to`: recipient list from `to` parameter
- `subject`: from `subject` parameter
- `body`: `body_md` content
- `cc`: PM email (Level 2 only) or empty
- `attachments`: converted files (if any)

On success → proceed to Step 6.

**Fallback (Gmail unavailable or MCP error):**

1. Save draft to `drafts/email-draft-{email_type}-{YYYY-MM-DD}.md`
   (for levels 1/2 this is the first time the draft is created; for level 3 it is overwritten).
   Use format from the Email Type Registry section: header (To, Subject, CC, Attachments) + body + attachment paths.
   ```
   # Email Draft: {email_type}
   Date: {YYYY-MM-DD}
   To: {to}
   Subject: {subject}
   CC: {cc or "—"}
   Attachments: {list or "—"}
   ---
   {body_md}
   ```
2. Notify PM: "Gmail unavailable. Draft saved at `drafts/email-draft-{email_type}-{YYYY-MM-DD}.md`. Please send manually."
3. Proceed to Step 6.

### Step 6 — Log

Write to `logs/log.md`:
- Sent: `{DATE}: send-email — sent {email_type} → {to} (level {N})`
- Fallback: `{DATE}: send-email — fallback, draft saved drafts/email-draft-{type}-{DATE}.md`
- Cancelled: `{DATE}: send-email — cancelled by PM, {email_type} not sent`

---

## Email Type Registry

| Type | Purpose | Level | Convert to docx |
|------|---------|-------|-----------------|
| E1 | Client questionnaire | 3 | yes |
| E2 | Team lessons questionnaire | 2 | no (.md) |
| E3 | Document approval request | 3 | yes |
| E4 | Deadline deviation alert | 2 | yes |
| E5 | Stream sync deviation alert | 2 | yes |
| E6 | Deadline reminder | 1 | no (no attachment) |
| E7 | Weekly status report | 1 | yes |
| E8 | Meeting status distribution | 3 | yes |

---

## Constraints

- Does NOT generate email content — receives rendered content from calling skill
- Does NOT select recipients — set by calling skill
- Does NOT update `project-state.md` — updated by calling skill
- Mass send (>10 recipients) requires explicit PM confirmation regardless of level
- Level 3 draft awaits confirmation within the current session; if session closes, draft remains in `drafts/`
- Direct user invocation is not supported
