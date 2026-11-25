---
name: cn-reimbursement-approval-payload-builder
version: "2.2"
description: Runs the CN reimbursement intake end to end and posts a structured summary; full approval state machine requires a bundled workflow.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - cn-reimbursement
    - lark
    - lark-approval
    - payload-builder
  clawdbot:
    emoji: "receipt"
    files:
      - "references/*"
      - "scripts/*"
---

# CN Reimbursement Approval

You (the agent) run the available part of this flow yourself with your tools, then POST a structured summary to the chat. Do NOT refuse, do NOT just describe. Never ask the user for tokens — your NyxID-brokered tools broker all credentials.

Use this when someone runs a CN reimbursement intake in a Lark chat — a submitter sends receipts and you need to parse them, normalize the submission, and build the finance-review summary and/or the Lark approval instance body.

## Scope

This reimbursement flow is a multi-trigger STATEFUL system (webhook intake → review form → approval round-trip → scheduled token refresh → admin ops). A single chat skill reproduces only the **intake + structured summary / approval-body build**. Full end-to-end reproduction (suspend-for-review, suspend-for-approval, resume) requires bundling this as a `workflows/*.yaml` driven by the aevatar workflow engine (HITL `human_input`/`human_approval` + `notify` steps) — out of scope for this skill.

## How to run it

1. **Resolve the inputs that ARE present.** Pull what the message and conversation already give you: receipt OCR fields, the submitter (`open_id` / `user_id`), the CNY total, subbrand splits, purpose, category, detail-sheet URL, and the finance review decision if one was supplied. Note which approval inputs are missing.

2. **Collect / normalize via `nyxid_proxy`** where needed. Use slug `api-lark-bot` to look up the sender, resolve open ids/user ids, or fetch attachment metadata that the intake referenced. Keep only the fields the contract needs.

3. **Analyze / validate.** Confirm subbrand values are in the allowed set, the CNY total reconciles with the splits, and required payee/category fields are present. If something required is missing, say what and stop — do not invent roster, receipts, file codes, or approval data.

4. **Build the approval-instance body** with `scripts/build_cn_reimbursement_payload.js` through `code_execute` (language `"javascript"`, NO stdin — pass inline data):

   ```js
   console.log(JSON.stringify(buildPayload({ mode: "build_approval_instance", /* reviewed reimbursement data, row splits/rows, receipt OCR, approval upload file codes */ })));
   ```

   The script also supports `parse_event`, `build_status_message`, `build_review_package`, and `build_submitter_link_message` — call `buildPayload` with the matching `mode` the same way. If you genuinely cannot execute code, build the body by following `references/cn-reimbursement-contract.md` field-for-field.

5. **Terminal action.** If an `approval_code` and approval scope ARE available, SUBMIT the instance via `nyxid_proxy`:

   ```json
   { "slug": "api-lark-bot", "path": "/open-apis/approval/v4/instances", "method": "POST", "body": <built approval_body> }
   ```

   OTHERWISE, POST the structured summary (and the built approval body) into the chat with `lark_messages_send`, and note what a human or a bundled workflow must still do — confirm the finance review and submit the approval.

6. **Report** one line: what you posted (or submitted), the submitter, and the CNY total / item count.

## Payload builder reference

`scripts/build_cn_reimbursement_payload.js` exports `buildPayload(input)` and dispatches on `mode`:

- `parse_event` — raw Lark webhook body → parsed fields or a challenge response.
- `build_status_message` — a `status` value → one Lark text message body.
- `build_review_package` — `submission_id` + submitter `open_id` + receipts + totals + payee → reviewer message, invoice-forward payloads, submitter acknowledgement.
- `build_approval_instance` — reviewed data + row splits/rows + receipt OCR + upload file codes → `approval_body` and `lark.body` for `POST /open-apis/approval/v4/instances?user_id_type=user_id`.
- `build_submitter_link_message` — Lark approval instance result + receipt summary → submitter confirmation body.

Required keys, aliases, constants, widget ids, and output shapes are in `references/cn-reimbursement-contract.md`. On missing fields the script returns `needs_more_information: true` + `missing`; on inapplicable input it returns `skip: true`.

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

- Only use data that actually arrived — never invent CN roster data, receipt OCR fields, open ids, user ids, approvers, file codes, instance codes, or serial numbers.
- Prefer the bundled script over hand-building JSON; it is the deterministic source of truth.
- All sending, approval submission, and token exchange go through your NyxID-brokered tools; never handle raw secrets.
