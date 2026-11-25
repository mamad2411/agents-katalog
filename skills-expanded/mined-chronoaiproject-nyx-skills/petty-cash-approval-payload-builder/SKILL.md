---
name: petty-cash-approval-payload-builder
version: "2.2"
description: Runs the petty-cash approval flow end to end yourself — collect Lark DM/sheet/image context, extract receipt details, build the exact approval body, then SUBMIT the Lark approval instance.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - petty-cash
    - lark-approval
    - payload-builder
  clawdbot:
    emoji: "money_with_wings"
    files:
      - "references/*"
      - "scripts/*"
---

# Petty Cash Approval

Use this when someone asks to process an Alex / P4 petty-cash DM, receipt image, session command,
or recharge request that should create a Lark approval instance.

**You (the agent) run the WHOLE flow yourself with your own tools, then SUBMIT the Lark approval.**
Do NOT refuse, do NOT just describe, do NOT claim "the skill only formats" — drive the flow. If a
required config (`approval_code` / scope) is missing, FALL BACK to posting the approval summary card
to the chat — never fail the run. Never ask the user for tokens — your NyxID-brokered tools broker
all credentials.

## How to run it

1. **Resolve inputs.** From the current Lark interaction, webhook event, or the user's plain-text
   command, identify the requester `open_id` (`userId`), amount, currency, reason, and sheet URL.
   The recharge `approval_code` defaults to `A258D96B-567C-4327-9C5B-C53500C0AED2`; supply your own
   only if the approval definition differs. To classify a raw event, run the builder once with
   `{mode:"parse_event", body:<event body>}` (recognizes `im.message.receive_v1`,
   `card.action.trigger`, `approval_instance`; answer URL verification with the returned `challenge`).

2. **Collect from Lark** via NyxID-brokered access `nyxid_proxy` `{slug:"api-lark-bot", path:"/open-apis/...",
   method:...}`. Use the workflow constants unless a live response gives newer values: spreadsheet
   `NmIisfa2KhgPlHtMWXrlneXFgvb`, main sheet `34d718`, allowlist `472Rq0`, sessions `1xoQVO`,
   template `1xoQVP`, Drive folder `NcI2fgbV9lkINqd8Bacl1NjtgPd`, Bitable app
   `L0PibpG6La5Vr0sBZNZlJpvRgaf`, session table `tblBTQzP6iaFwPWj`, expense details table
   `tblqwAD9XzuKGjPB`.
   - sheet rows: `GET /open-apis/sheets/v2/spreadsheets/NmIisfa2KhgPlHtMWXrlneXFgvb/values/{sheet_id}!A1:J5000?valueRenderOption=UnformattedValue`
   - receipt image: `GET /open-apis/im/v1/messages/{messageId}/resources/{imageKey}?type=image`
   - preserve a receipt: `POST /open-apis/drive/v1/files/upload_all` under folder
     `NcI2fgbV9lkINqd8Bacl1NjtgPd`
   - sheet/tab setup: `POST /open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/sheets_batch_update`
     and `PUT /open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/values`
   - Bitable state: `POST /open-apis/bitable/v1/apps/{appToken}/tables/{tableId}/records` and the
     matching record update/search endpoints.

3. **Analyze receipts and actions with your own model/vision tools.** Extract the receipt JSON —
   `amount`, `currency`, `merchant`, `category`, `item`, `date`, `confidence`, `warnings`. For plain
   recharge text such as `申请充值 3000 SGD 月度备用金补足`, normalize amount, currency, requester
   open id, reason, and sheet URL.

4. **Build the exact approval body by running the bundled builder.** Call
   `scripts/build_petty_cash_payload.js` via `code_execute` with `language: "javascript"` (NO stdin
   — inline the data): `const {buildPayload}=require('./scripts/build_petty_cash_payload.js');
   console.log(JSON.stringify(buildPayload({mode:"build_approval_instance", amount, currency:"SGD",
   reason, sheetUrl, userId})))` (route a raw event with `buildPayload({mode:"parse_event",
   body:<event>})`). Use the returned `lark.body`. If you genuinely cannot execute code, build the
   body by following `references/petty-cash-contract.md` field-for-field.

5. **Terminal — act on the parsed kind.**
   - `request_cash_in`: SUBMIT the approval instance with `nyxid_proxy` `{slug:"api-lark-bot",
     path:"/open-apis/approval/v4/instances", method:"POST", body:<lark.body from step 4: approval_code +
     user_id + form>}`. **If no `approval_code` / scope OR the submit fails → FALL BACK** to
     `reply_with_interaction` (approve/reject card) or a plain summary requesting manual approval —
     never fail the run.
   - `image`, `submit`, or card confirmation: use the collected sheet/image/OCR data to append or
     update the sheet, create or patch Bitable records, then send/update the card with
     `reply_with_interaction`, `lark_messages_send`, or `lark_messages_reply`.
   - `new_batch`, `close_row`, `switch_session`, `add_remark`, `reset_remark`, `ensure_tab`: update
     the relevant sheet/Bitable state through the paths above, then reply in the current chat with
     `lark_messages_reply`.

6. **Report** one line: what you processed and submitted/posted, plus any returned approval instance
   code, message id, sheet row, or Bitable record id (or "card fallback").

## Payload builder reference

`scripts/build_petty_cash_payload.js` exports `buildPayload(data)`. Modes: `parse_event` (routes URL
verification, IM messages, card actions, approval callbacks; parses allowlisted P2P messages into
`image`, `submit`, `request_cash_in`, `new_batch`, `close_row`, `switch_session`, `add_remark`,
`reset_remark`, `ensure_tab`, or `text_other`) and `build_approval_instance` (connector-ready Lark
approval request). `build_approval_instance` returns `request`, `form`, and `lark.path` / `lark.body`
with `approval_code`, `user_id`, and JSON-stringified `form` whose widget ids are reason
`widget17167786766400001`, amount `widget17167786834600001`, sheet URL `widget17167786925010001`.
Exact aliases, defaults, and examples are in `references/petty-cash-contract.md`.

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

- Only use real returned data; never invent open ids, chat ids, image keys, sheet ids, rows, record
  ids, approval status, OCR fields, approval codes, widget ids, or approvers.
- Prefer running the bundled script; it is the deterministic source of truth for parsing and the
  approval payload shape.
- Use credentials only through your NyxID-brokered tools such as `nyxid_proxy` and the Lark helpers.
