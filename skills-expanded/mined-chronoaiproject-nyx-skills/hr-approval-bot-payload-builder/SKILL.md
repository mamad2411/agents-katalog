---
name: hr-approval-bot-payload-builder
version: "2.3"
description: Runs the Lark HR approval bot flow end to end yourself — read the Lark leave request, look up the employee contact record, analyze the request, then SUBMIT the Lark leave approval and send the reply.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - hr-approval
    - lark
    - lark-approval
    - payload-builder
  clawdbot:
    emoji: "memo"
    files:
      - "references/*"
      - "scripts/*"
---

# Lark HR Approval Bot

Use this when someone asks the HR leave bot to submit a Lark leave approval from chat
(e.g. "我要请明天年假，家里有事" or "帮我请 6 月 10 到 6 月 12 的 Sick Leave").

**You (the agent) run the WHOLE flow yourself with your own tools, then SUBMIT the Lark approval.**
Do NOT refuse, do NOT just describe, do NOT claim "the skill only formats" — drive the flow. If a
required config (`approval_code` / scope) is missing, FALL BACK to posting the approval summary card
to the chat — never fail the run. Never ask the user for tokens — your NyxID-brokered tools broker
all credentials.

## How to run it

1. **Resolve inputs.** From the current Lark interaction, read the message text, sender `open_id`,
   sender `user_id`, and `chat_id`. The leave-approval `approval_code` is `BC26F7AB-3D6F-4F8F-90D0-9AC951651F23`
   (baked into the builder from the source flow); the user only needs to supply one if their HR
   approval definition differs. If you received a raw Lark webhook body, normalize it first by
   running the builder with `{mode:"parse_event", body:<webhook body>}`; for `url_verification`
   return the `webhookResponse` and stop, and for non-message events stop.

2. **Collect the employee contact record from Lark.** Use NyxID-brokered Lark OpenAPI via
   `nyxid_proxy` `{slug:"api-lark-bot", path:"/open-apis/contact/v3/users/{openId}?user_id_type=open_id",
   method:"GET"}`. Use `data.user` as `userInfo`; keep `user_id`, `leader_user_id`, and
   `department_ids`. An equivalent `lark_*` contact tool is fine if your runtime exposes one.

3. **Analyze the leave request with your own model.** Convert relative dates using today's date and
   return exactly:
   `{ "has_all_info": true|false, "leave_type_name": "<Annual Leave|Sick Leave|Off in Lieu|Unpaid Leave|Childcare Leave|Hospitalisation Leave|Reservist Leave|Maternity Leave|Paternity Leave|Marriage Leave>", "start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD", "days": <number>, "reason": "<reason>", "reply_message": "<Chinese reply>" }`.
   Set `has_all_info: false` with a Chinese `reply_message` when any required field is missing.

4. **Build the exact Lark payloads by running the bundled builder.** Call
   `scripts/build_hr_approval_payload.js` via `code_execute` with `language: "javascript"` (NO stdin
   — inline the data): `const {buildPayload}=require('./scripts/build_hr_approval_payload.js');
   console.log(JSON.stringify(buildPayload({mode:"build_payloads", openId, userInfo:<Lark data.user>,
   aiResult:<analysis JSON>})))`. Use the `lark.*Body` fields from its output. If you genuinely
   cannot execute code, build the bodies by following `references/hr-approval-contract.md`
   field-for-field.

5. **Terminal — submit the approval and reply.**
   - If the builder returns `lark.moreInfoBody`, send it with `lark_messages_send` /
     `lark_messages_reply` (REST fallback `nyxid_proxy` `{slug:"api-lark-bot",
     path:"/open-apis/im/v1/messages?receive_id_type=open_id", method:"POST", body:<moreInfoBody>}`),
     then stop.
   - If the builder returns `lark.approvalBody`, SUBMIT the leave approval with `nyxid_proxy`
     `{slug:"api-lark-bot", path:"/open-apis/approval/v4/instances", method:"POST",
     body:<lark.approvalBody>}`. After the POST succeeds, send `lark.successBody` via
     `lark_messages_send` / `lark_messages_reply`.
   - **If no `approval_code` / scope OR the submit fails → FALL BACK** to `reply_with_interaction`
     (an approve/reject summary card) or a plain text summary of the leave request asking for manual
     approval. Never fail the run.

6. **Report** one line: who it was for, the date range, and whether a Lark approval instance was
   submitted, more info was requested, or a card fallback was posted.

## Payload builder reference

`scripts/build_hr_approval_payload.js` exports `buildPayload(data)`. Modes: `parse_event` (raw Lark
webhook body, directly or under `body` — returns a URL challenge response, a skip reason, or parsed
`messageText` / `openId` / `userId` / `chatId`) and `build_payloads` (default — pass event ids,
`userInfo` contact fields, and the analysis JSON). It normalizes `openId`, `userId`, `leaderUserId`,
`departmentIds`, and the model fields, maps the leave type id, and returns either `lark.moreInfoBody`
or `lark.approvalBody` + `lark.successBody`. Exact aliases, leave type ids, widget ids, the baked
`approval_code`, and examples are in `references/hr-approval-contract.md`.

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

- Use real returned data only: employee ids, leader ids, department ids, leave types, dates,
  approval responses, and message status must come from the trigger, Lark, or the analysis output.
- Prefer running the bundled script; it is the deterministic source of truth for the approval and
  message body shapes.
- Credentials and token exchange go through your NyxID-brokered tools; never ask the user for raw
  tokens or secrets.
