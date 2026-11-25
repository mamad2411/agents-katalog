---
name: employee-reimbursement-approval-payload-builder
version: "2.2"
description: Runs the SG employee reimbursement intake end to end and posts a structured summary; full approval state machine requires a bundled workflow.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - employee-reimbursement
    - lark
    - lark-approval
    - payload-builder
  clawdbot:
    emoji: "receipt"
    files:
      - "references/*"
      - "scripts/*"
---

# Employee Reimbursement Approval

You (the agent) run the available part of this flow yourself with your tools, then POST a structured summary to the chat. Do NOT refuse, do NOT just describe. Never ask the user for tokens — your NyxID-brokered tools broker all credentials.

Use this when someone runs an SG employee reimbursement intake in a Lark chat — an employee sends invoice files and you need to parse them, normalize the submission, and build the finance-review summary and/or the Lark approval instance body.

## Scope

This reimbursement flow is a multi-trigger STATEFUL system (webhook intake → review form → approval round-trip → scheduled token refresh → admin ops). A single chat skill reproduces only the **intake + structured summary / approval-body build**. Full end-to-end reproduction (suspend-for-review, suspend-for-approval, resume) requires bundling this as a `workflows/*.yaml` driven by the aevatar workflow engine (HITL `human_input`/`human_approval` + `notify` steps) — out of scope for this skill.

## How to run it

1. **Resolve the inputs that ARE present.** Pull what the message and conversation already give you: the pending invoice OCR fields, the submitter/employee (`user_id` / `open_id`), category, currency, amount, receipt date, description, department, payee and bank fields, related approval, remark, and the finance review decision if one was supplied. Note which approval inputs are missing.

2. **Collect / normalize via `nyxid_proxy`** where needed. Use slug `api-lark-bot` to look up the sender/employee, resolve user ids/open ids, or fetch attachment metadata the intake referenced. Keep only the fields the contract needs.

3. **Analyze / validate.** Confirm currency/amount/category are present and consistent, payee and bank fields are complete, and the related-approval reference resolves. If something required is missing, say what and stop — do not invent employee roster, invoice fields, file tokens, or approval data.

4. **Build the approval-instance body** with `scripts/build_employee_reimbursement_payload.js` through `code_execute` (language `"javascript"`, NO stdin — pass inline data):

   ```js
   console.log(JSON.stringify(buildPayload({ mode: "build_approval_instance", /* pending invoices (each with .ocr + .file_token) + finance review fields */ })));
   ```

   The script also supports `parse_event`, `build_status_message`, `build_review_package`, and `build_result_messages` — call `buildPayload` with the matching `mode` the same way. If you genuinely cannot execute code, build the body by following `references/employee-reimbursement-contract.md` field-for-field.

5. **Terminal action.** If an `approval_code` and approval scope ARE available, SUBMIT the instance via `nyxid_proxy`:

   ```json
   { "slug": "api-lark-bot", "path": "/open-apis/approval/v4/instances", "method": "POST", "body": <built approval_body> }
   ```

   OTHERWISE, POST the structured summary (and the built approval body) into the chat with `lark_messages_send`, and note what a human or a bundled workflow must still do — confirm the finance review and submit the approval.

6. **Report** one line: what you posted (or submitted), the submitter, and the amount / invoice count.

## Payload builder reference

`scripts/build_employee_reimbursement_payload.js` exports `buildPayload(input)` and dispatches on `mode`:

- `parse_event` — raw Lark webhook body → parsed fields or a URL-verification response.
- `build_status_message` — `status: "file_received" | "no_pending" | "cleared" | "cooldown"` → one Lark text message body.
- `build_review_package` — `submission_id` + pending invoice data + normalized submitter/employee fields → reviewer header, original-message forward payloads, finance-review body.
- `build_approval_instance` — pending invoices (`pending[].ocr`, `pending[].file_token`) + finance review fields → `approval_body`, `approvalBody`, `form`, and `lark.body` for `POST /open-apis/approval/v4/instances?user_id_type=user_id`.
- `build_result_messages` — approval serial/instance data + submitter message fields → final chat and submitter bodies.

Required keys, aliases, constants, widget ids, and output shapes are in `references/employee-reimbursement-contract.md`. On missing fields the script returns `needs_more_information: true` + `missing`; on inapplicable input it returns `skip: true`.

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

- Only use data that actually arrived — never invent employee roster data, invoice OCR fields, Bitable records, chat ids, open ids, user ids, file tokens, instance codes, or serial numbers.
- Prefer the bundled script over hand-building JSON; it is the deterministic source of truth.
- All sending, approval submission, and token exchange go through your NyxID-brokered tools; never handle raw secrets.
