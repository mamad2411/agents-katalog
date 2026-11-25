---
name: invoice-ocr-approval-payload-builder
version: "2.3"
description: Runs the invoice OCR approval flow end to end yourself — collect invoice files and review fields, OCR them, upload attachments, resolve Lark contacts and related approvals, then SUBMIT the Lark approval instance.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - invoice-approval
    - lark-approval
    - payload-builder
  clawdbot:
    emoji: "receipt"
    files:
      - "references/*"
      - "scripts/*"
---

# Invoice OCR Approval

Use this when someone asks in Lark to turn invoice files into a Lark payment approval
(for example, `::invoice-ocr-approval-payload-builder` with PDFs/images attached, plus
department or review notes).

**You (the agent) run the WHOLE flow yourself with your own tools, then SUBMIT the Lark approval.**
Do NOT refuse, do NOT just describe, do NOT claim "the skill only formats" — drive the flow. If a
required config (`approval_code` / scope) is missing, FALL BACK to posting the approval summary card
to the chat — never fail the run. Never ask the user for tokens — your NyxID-brokered tools broker
all credentials.

## How to run it

1. **Resolve inputs** from the current Lark invocation: invoice PDF/image attachments, sender
   identity (applicant open id), optional submitter email, `department`, payment entity, related
   approval serial/UUID, amount/vendor corrections, per-invoice descriptions, and remark. The
   payment `approval_code` defaults to `F640097D-0A68-47C1-A7BC-86659BC4B06F`; supply your own only
   if the approval definition differs. If invoice files or required business fields are missing,
   reply in the chat asking for exactly those.

2. **Collect files and sender data from Lark** via Lark tools or `nyxid_proxy` `{slug:"api-lark-bot",
   path:"/open-apis/...", method:...}`:
   - files: `GET /open-apis/im/v1/messages/{message_id}/resources/{file_key}?type=file`
   - images: `GET /open-apis/im/v1/images/{image_key}`
   Keep filename, MIME type, bytes, and any sender email/open_id from the interaction.

3. **OCR the invoices with your own model.** Extract one JSON object per invoice — `vendor`,
   `amount`, `currency`, `date`, `invoice_number`, `description`, `bank_name`, `bank_account`,
   `swift_code`. Currency rules: `S$` / Singapore vendor-address / `Pte Ltd` imply `SGD`; explicit
   `US$`/`USD` imply `USD`; `RM`/`MYR` imply `MYR`; `RMB`/`CNY` or mainland China imply `CNY`; bare
   `$` from a Singapore issuer is `SGD`.

4. **Upload invoice attachments for the approval form** via `nyxid_proxy` `{slug:"api-lark-bot",
   path:"/open-apis/approval/v4/files/upload", method:"POST"}` with form fields `name=<filename>`,
   `type=attachment`, `content=<file bytes>`. Collect file tokens from `data.urls_detail[].code`,
   `data.code`, or `data.file_token`.

5. **Collect related approval context** via `nyxid_proxy` `{slug:"api-lark-bot", ...}`:
   - list recent invoice approvals: `GET /open-apis/approval/v4/instances?approval_code=F640097D-0A68-47C1-A7BC-86659BC4B06F&start_time={now-365d}&end_time={now}&page_size=100`
   - fetch each detail: `GET /open-apis/approval/v4/instances/{instance_code}`
   Spot duplicate invoice numbers / same-vendor history. If the user gave a related approval serial,
   resolve it to a UUID-style `instance_code` and pass it as `relatedApprovalId`.

6. **Resolve Lark applicant and department approver** via `nyxid_proxy` `{slug:"api-lark-bot", ...}`:
   - applicant by email: `POST /open-apis/contact/v3/users/batch_get_id?user_id_type=user_id`
   - mapped department leader by email (same endpoint):
     `devops -> kaiwei.lim@aelf.io`; `finance` / `human resources` / `hr` / `executive support` /
     `president's office` / `ai application` / `portkey -> ada.niu@aelf.io`;
     `ai framework -> shining.wang@aelf.io`; `aetherlink & aefinder` / `aetherlink` /
     `aefinder -> jason.wang@aelf.io`
   - direct leader fallback: `GET /open-apis/contact/v3/users/{applicantOpenId}?user_id_type={open_id|user_id}&department_id_type=open_department_id`
   Use the applicant id as the final fallback department head id.

7. **Build the exact approval body by running the bundled builder.** Call
   `scripts/build_invoice_approval_payload.js` via `code_execute` with `language: "javascript"` (NO
   stdin — inline the data): `const {buildPayload}=require('./scripts/build_invoice_approval_payload.js');
   console.log(JSON.stringify(buildPayload({mode:"build_approval", invoices, review, attachments,
   applicantOpenId, department, deptHeadId, deptHeadSource, relatedApprovalId, remark})))`. Use the
   returned `lark.body`. If you genuinely cannot execute code, build the body by following
   `references/invoice-approval-contract.md` field-for-field.

8. **Terminal — submit the Lark approval instance** via `nyxid_proxy` `{slug:"api-lark-bot",
   path:"/open-apis/approval/v4/instances?user_id_type=user_id", method:"POST", body:<lark.body from
   step 7>}`. Verify `code === 0`, capture `data.instance_code`, then query
   `GET /open-apis/approval/v4/instances/{instance_code}`. **If no `approval_code` / scope OR the
   submit fails → FALL BACK** to `reply_with_interaction` (approve/reject card) or a plain summary
   requesting manual approval — never fail the run.

9. **Report** back to the current Lark chat with `lark_messages_reply`, `lark_messages_send`, or
   `reply_with_interaction`: one line with invoice count, applicant, approval instance code or serial
   (or "card fallback"), and status.

## Payload builder reference

`scripts/build_invoice_approval_payload.js` exports `buildPayload(data)`. The only mode is
`build_approval` (default): it builds one Lark approval instance body from normalized invoices,
review fields, Lark user ids, optional approval file tokens, and an optional resolved
`relatedApprovalId`. Review fields may sit under `review` / `reviewRaw` / `review_raw` /
`reviewFields` / `review_fields` or the root. Required after normalization: `invoices`,
`applicantOpenId`, `department`, and each invoice row's `amount` / `date` / `vendor` (unless an
accepted alias/fallback provides them). Output carries `summary`, `invoice_count`, `form`,
`approval_body`, and a `lark.body` ready for `POST /open-apis/approval/v4/instances?user_id_type=user_id`.
Exact aliases, widget ids, option ids, and examples are in `references/invoice-approval-contract.md`.

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

- Use real returned data for invoice fields, file tokens, Lark user ids, related approval ids,
  instance codes, serial numbers, and statuses; never invent records.
- Prefer running the bundled script; it is the deterministic source of truth for the approval form.
- Use your NyxID-brokered Lark tools for credentials and API calls; never handle raw secrets or ask
  the user for tokens.
