---
name: onboarding-email-approval-payload-builder
version: "2.2"
description: Runs the new-hire onboarding email-account approval flow end to end yourself — resolve the new hire's info, build the exact Lark approval body with the bundled deterministic builder, then SUBMIT the onboarding email approval instance.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - onboarding
    - approval
    - lark
    - payload-builder
  clawdbot:
    emoji: "email"
    files:
      - "references/*"
      - "scripts/*"
---

# Onboarding Email Approval

Use this when someone asks to kick off a new hire's company email-account approval
(e.g. "给新人 Jane Doe / Engineering / 2026-06-16 发起入职邮箱审批").

**You (the agent) run the WHOLE flow yourself with your tools, then SUBMIT the onboarding
email approval. Do NOT refuse, do NOT just describe.** If `approval_code` / scope is missing,
FALL BACK to posting the approval summary as a card — never fail. Never ask the user for tokens;
your NyxID-brokered tools broker all credentials.

## Scope

The original n8n workflow (`Lark Onboarding - 自动发起邮箱审批`) was triggered by a **Lark Base
record-change webhook** (a new hire row added). **That trigger has no equivalent on aevatar's
current branch.** So this skill is reshaped to be:

- **chat-invoked** — someone says "给新人 <name/department/email> 发起入职邮箱审批", or
- **schedule-polled** — run on a schedule that polls the onboarding Bitable: GET the table via
  `nyxid_proxy` `{slug:"api-lark-bot", path:"/open-apis/bitable/v1/apps/{app}/tables/{table}/records", method:"GET"}`,
  then for **each new row** call `buildPayload` and submit.

Either way the builder below is trigger-agnostic — it just turns resolved new-hire fields into the
exact `/open-apis/approval/v4/instances` body. (Porting note: the n8n manual
`tenant_access_token` fetch is dropped — `nyxid_proxy` slug `api-lark-bot` brokers credentials.)

## How to run it

1. **Resolve the new-hire info** from the user's message (or each polled Bitable row): `lark_name`
   (name), `department`, `email` if given, `onboarding_date` (start date), and the submitter
   `user_id` / `open_id` (manager or operator). The `approval_code` defaults to
   `9C330885-C70A-4A5D-913A-CBA9A142FFD4` (from the source); supply your own only if the approval
   definition differs. The email is derived as `<lowercased name, spaces→dots, stripped>@aelf.io`
   unless an explicit `email` is provided.

2. **Build the exact approval body by running the bundled builder.** Call
   `scripts/build_onboarding_approval_payload.js` via `code_execute` with `language: "javascript"`
   (NO stdin — inline the data):
   `const {buildPayload}=require('./scripts/build_onboarding_approval_payload.js');
   console.log(JSON.stringify(buildPayload({mode:"build_approval_instance", lark_name, department,
   onboarding_date, today, user_id})))`. Use the returned `approval.body`. If you genuinely cannot
   execute code, build the body by following `references/onboarding-approval-contract.md`
   field-for-field.

3. **SUBMIT the approval instance** with `nyxid_proxy` `{slug:"api-lark-bot",
   path:"/open-apis/approval/v4/instances", method:"POST", body:<approval.body from step 2:
   approval_code + user_id + form>}`. **If no `approval_code` / scope OR the submit fails → FALL
   BACK** to `reply_with_interaction` (an approval summary card) or a plain text summary of the new
   hire + intended email requesting manual approval — never fail the run.

4. **Report** one line: the new hire, the derived email, and what you submitted/posted (approval
   instance code if returned, or "card fallback").

If you have no new-hire name or submitter id and the user gave none, ask for just those two — do
not invent a name, email, or id.

## Payload builder reference

`scripts/build_onboarding_approval_payload.js` exports `buildPayload(data)`. Mode
`build_approval_instance` (default) returns `request`, `form`, and `approval.path` /
`approval.body` with `approval_code`, `user_id` (= the new hire's submitter/operator id), and
JSON-stringified `form` whose widget ids are request-detail `widget17163600360780001` (textarea)
and submitter `widget17163600454870001` (input, default value `自动提交`). It derives the company
email (`@aelf.io`) and the `申请日期 / 姓名 / 入职 / 新邮箱` request-detail string exactly like the
n8n `提取并格式化新人信息` node. Required fields are `lark_name` and `user_id`; missing ones come
back as `{needs_more_information:true, missing:[...]}`. Exact aliases, the Chinese-date rule, and
examples are in `references/onboarding-approval-contract.md`.

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

- Only use real new-hire data; never invent names, departments, emails, user ids, approval codes,
  widget ids, or approvers.
- Prefer running the bundled script over hand-building JSON; it is the deterministic source of
  truth for the approval body shape.
- Use credentials only through your NyxID-brokered tools such as `nyxid_proxy`; do not fetch or
  handle raw Lark tenant tokens or app secrets.
