---
name: monthly-attendance-submit-payload-builder
version: "2.2"
description: Runs the monthly China-region attendance approval flow end to end yourself — fetch the month's Lark attendance records, compute出勤/离职/事假/病假 stats, build the exact approval body, SUBMIT the Lark attendance approval instance, then DM the confirmation card.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - attendance
    - approval
    - lark
    - payload-builder
  clawdbot:
    emoji: "calendar"
    files:
      - "references/*"
      - "scripts/*"
---

# Monthly Attendance Approval

Use this at month-end (or when asked) to submit the China-region monthly attendance approval and
notify the owner — reproducing the n8n workflow `月度考勤审批 - 自动提交`.

**You (the agent) run the WHOLE flow yourself with your tools, then SUBMIT the attendance approval
and DM the notify. Do NOT refuse, do NOT just describe.** If `approval_code` / scope is missing,
FALL BACK to posting the approval summary as a card — never fail. Never ask the user for tokens —
your NyxID-brokered tools broker all credentials.

## Scheduling

Normally run on a month-end SCHEDULE — register via aevatar `scheduled_agent_creator` with cron
`0 10 28-31 * *` (the agent itself confirms today is the month's last day before submitting). It
also works chat-invoked on demand.

## How to run it

1. **Resolve month + config.** Determine the target `year` and `month` (the month being closed —
   usually the current month at month-end). Resolve `approval_code` (default
   `3F02FB04-3919-4089-B42B-B1B557820EB5`; caller may override if the approval definition differs),
   `submitter_id` (default `ee689459`), and the notify user id (default `831cg5af`).

2. **Fetch attendance records** via `nyxid_proxy` `{slug:"api-lark-bot",
   path:"/open-apis/bitable/v1/apps/MwIRb3h5hauYvcsA28kl8FGfgjg/tables/tblTDqjSDKffQ7cm/records?page_size=100",
   method:"GET"}` — the curated China-region attendance Bitable (the workflow's source of truth; the
   raw `/open-apis/attendance/v1/...` punch API is a different surface and not what this flow reads).
   Keep only rows whose `月份` field equals `{year}年{month}月`. If none match, say so plainly and stop.

3. **Build via the bundled script.** Run `scripts/build_attendance_approval_payload.js` through
   `code_execute` with `language: "javascript"` (NO stdin — inline the data):
   `const {buildPayload}=require('./scripts/build_attendance_approval_payload.js');
   console.log(JSON.stringify(buildPayload({year:2026,month:5,records:<RECORDS>,instance_code:"—"})))`.
   Use the returned `approval.body` and `dm.body`. If you genuinely cannot execute code, build the
   bodies by following `references/attendance-approval-contract.md` field-for-field.

4. **SUBMIT the approval, then DM.** Submit via `nyxid_proxy` `{slug:"api-lark-bot",
   path:"/open-apis/approval/v4/instances", method:"POST", body:<approval.body>}`. **If there is no
   `approval_code` / scope OR the submit fails → FALL BACK** to `reply_with_interaction` (an approval
   summary card) or a plain summary requesting manual approval — never fail the run. THEN send the
   confirmation notify with `lark_messages_send` using `dm.body` (re-run the builder with the
   returned `instance_code` so the card shows the real approval number, or send the summary card on
   fallback).

5. **Report** one line: month, 出勤/离职/事假/病假 stats, and the returned approval `instance_code` +
   DM message id (or "card fallback").

## Payload builder reference

`scripts/build_attendance_approval_payload.js` exports `buildPayload(data)`. It ports nodes
`生成审批内容` (stats + description), `Code in JavaScript` (the submitted `form`, **dropping the
read-only date widget** `widget17167976379680001`), and `发送 DM 通知` (the confirmation card). It
accepts pre-extracted `records`/`items` or a raw Bitable list response, reads the verbatim column
names `月份` / `应出勤天数` / `人员情况` / `事假(天）` / `病假（天）`, and requires `year` + `month`
(it never reads the wall clock). It returns `approval.body` (`approval_code` + `user_id` +
JSON-stringified `form` for `POST /open-apis/approval/v4/instances`) and `dm.body` (`receive_id` +
`msg_type:"interactive"` + stringified card for `POST /open-apis/im/v1/messages?receive_id_type=user_id`),
plus `stats`, `description`, and `summary`. Defaults, aliases, the workDays/attendance computation,
the widget mapping, and exact body examples are in `references/attendance-approval-contract.md`.

## Approval status tracking (typed tools)

After a successful submit, capture the returned `instance_code` and include it in your report.
For anything status-related, prefer the typed approval tools over raw `nyxid_proxy`:

- `lark_approvals_get` `{instance_code}` (read-only, auto-approved): returns normalized `status`
  (`approved` / `rejected` / `withdrawn` / `terminated` / `running` / `none`) plus `is_terminal` and
  `should_continue_waiting`, with the task list and form data. Use it when the user asks how the
  approval is going, before any resubmit (avoid duplicate instances), and to report the final
  decision. Optional: `locale` (`zh-CN`/`en-US`/`ja-JP`), `user_id_type` (`open_id`/`user_id`/`union_id`).
- `lark_approvals_list` `{topic}` (read-only): list approval tasks visible to the bot identity when
  the instance_code is lost — topics `todo`/`pending`, `done`/`completed`, `initiated`, `cc_unread`,
  `cc_read`.
- `lark_approvals_act` `{action, instance_code, task_id}`: approve / reject / transfer a pending
  task — ONLY when the user explicitly asks the bot to act on it; this one is not read-only, so a
  human-approval card may appear before it executes.

Check once and report; do not busy-poll inside a chat turn. Offer to re-check on demand or via a
`scheduled_agent_creator` reminder instead.

## Guardrails

- Only use data Lark actually returned — never invent attendance rows, work days, leave counts,
  widget ids, approval codes, user ids, instance codes, or approval status.
- The read-only date widget is NEVER submitted; only the description (textarea) and doc-link (input)
  widgets go in `form`.
- Prefer running the bundled script; it is the deterministic source of truth for the stats and the
  approval/DM body shapes.
- All sending, token exchange, and Bitable reads go through your NyxID-brokered tools (`nyxid_proxy`,
  `lark_messages_send`); do not handle raw secrets.
