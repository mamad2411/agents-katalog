---
name: lark-meeting-payload-builder
version: "2.1"
description: Runs the Lark Meeting v2 flow end to end — extracts tasks from meeting notes (or reads the Base task records), analyzes them with your own model, writes the task records to Lark Bitable, and posts the task list / reminder to the Lark group.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - meeting
    - lark
    - payload-builder
  clawdbot:
    emoji: "spiral_calendar_pad"
    files:
      - "references/*"
      - "scripts/*"
---

# Lark Meeting

Use this when someone asks to extract tasks from meeting notes, post a meeting task list to the
Lark group, save meeting tasks into Lark Base, or send the scheduled meeting-task reminder.

**You (the agent) run the WHOLE flow yourself with your own tools, then WRITE the results to Lark
Bitable and post a summary to the chat.** Do NOT refuse, do NOT just describe, do NOT claim "the
skill only formats" — drive the flow. If a data source or the target base is unavailable, SKIP that
part and still post what you have. Never ask the user for tokens — your NyxID-brokered tools broker
all credentials.

## How to run it

1. **Resolve mode and inputs.** Use `build_task_payloads` when the user gives meeting notes, a
   transcript, or asks to extract/post tasks. Use `build_reminder_payload` for the Monday weekly
   summary, the Wednesday reminder, the Friday reminder, or any task reminder. Use today's date as
   deterministic `today` in `YYYY-MM-DD`. The target Bitable and group chat are baked into the
   builder (`app_token` `Z1FSb2bmFaDdlWsTen8lwtKLgyh`, `table_id` `tblCIDFBnAfPPUi7`, chat
   `oc_922f242b5105f8f32c737c003d2f1b22`); if the user named a different base, carry their
   `app_token`/`table_id` into step 4.

2. **COLLECT.** For task mode, read `Meeting Transcript`, `Meeting Date`, `Your Name`, and `Minutes
   URL` from the current Lark message/interaction. If the user pasted the transcript, use it; if they
   gave a Lark Minutes URL, fetch the transcript/summary via the `lark_minutes` tools or `nyxid_proxy`
   slug `api-lark-bot` (`/open-apis/minutes/...`) and continue with the returned text. For reminder
   mode, read the task records: `nyxid_proxy` `{slug:"api-lark-bot",
   path:"/open-apis/bitable/v1/apps/Z1FSb2bmFaDdlWsTen8lwtKLgyh/tables/tblCIDFBnAfPPUi7/records?page_size=50",
   method:"GET"}`; keep `data.items`.

3. **ANALYZE (task mode).** Extract a JSON task array with your own model. Each item has `task`,
   `task_type`, `owner`, `owner_role`, `deadline`, `priority`, `inferred_fields`, `infer_reason`,
   and `source_quote`, grounded in the transcript. If no tasks are present, post a plain "no tasks
   found" note and stop.

4. **BUILD the exact payloads.** Run `scripts/build_meeting_payload.js` via `code_execute` (language
   `"javascript"`; NO stdin — inline the data into the code):
   - task mode: `console.log(JSON.stringify(buildPayload({ mode: "build_task_payloads", meetingDate,
     today, tasks })))`
   - reminder mode: `console.log(JSON.stringify(buildPayload({ mode: "build_reminder_payload", today,
     records })))`
   Use the script output. If code execution is unavailable, follow `references/meeting-contract.md`
   field-for-field.

5. **WRITE the records, then post the message.** In task mode, create one Bitable record per
   `lark.base.bodies[]` item via `nyxid_proxy` `{slug:"api-lark-bot",
   path:"/open-apis/bitable/v1/apps/<app_token>/tables/<table_id>/records", method:"POST",
   body:<each body exactly>}`. THEN, unless the builder returned `skip: true`, post `lark.message.body`
   to the group with `lark_messages_send` (or `lark_messages_reply` in-thread); its `body` already
   carries `receive_id: "oc_922f242b5105f8f32c737c003d2f1b22"`. **If no base target was resolved OR a
   write fails, SKIP the Bitable write and STILL post the built task list / reminder to the chat —
   never fail the run for a missing base.**

6. **REPORT** one line: task mode — meeting date, records written (or "summary-only"), posted task
   count; reminder mode — reminder type/date and unfinished count.

## Payload builder reference

Bundled script: `scripts/build_meeting_payload.js`. Modes:

- `build_task_payloads` — input `meetingDate`, `today` (or `weekFriday`), and tasks via `tasks`,
  `aiTasks`, `modelOutput`, or a Groq-style `choices[0].message.content`. Output: normalized
  `tasks`, `lark.base.bodies`, `message`, and `lark.message.body`.
- `build_reminder_payload` — input `today` and records via `records`, `items`, or `data.items`.
  Output: `reminderMessage`, `unfinishedCount`, and `lark.message.body`.

Constants baked in: Base path
`/open-apis/bitable/v1/apps/Z1FSb2bmFaDdlWsTen8lwtKLgyh/tables/tblCIDFBnAfPPUi7/records`, message
path `/open-apis/im/v1/messages?receive_id_type=chat_id`, group chat
`oc_922f242b5105f8f32c737c003d2f1b22`, suffix `【via lark-cli (auto-generated)】`. Exact aliases,
output shapes, and examples are in `references/meeting-contract.md`.

## Guardrails

- Only use data the tools actually returned — never invent meeting tasks, owners, deadlines,
  records, ids, or statuses.
- Prefer running the bundled script; it is the deterministic source of truth for payload shape.
- All credentials, Base access, and message sends go through your NyxID-brokered tools or Lark
  tools; never handle raw secrets.
