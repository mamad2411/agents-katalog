---
name: cho-weekly-goal-audit-payload-builder
version: "2.1"
description: Runs the CHO weekly goal audit / weekend review flow end to end — parses the employee's Lark goal message, audits or reviews it with your own model, writes the Base record, and posts the employee reply plus the CHO diagnosis to Lark.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - weekly-goal-audit
    - lark
    - payload-builder
  clawdbot:
    emoji: "dart"
    files:
      - "references/*"
      - "scripts/*"
---

# CHO Weekly Goal Audit

Use this when an employee sends a weekly goal (audit) or a weekend review message to the CHO bot,
and the goal/review should be scored, written to Lark Base, and answered.

**You (the agent) run the WHOLE flow yourself with your own tools, then WRITE the results to Lark
Bitable and post a summary to the chat.** Do NOT refuse, do NOT just describe, do NOT claim "the
skill only formats" — drive the flow. If a data source or the target base is unavailable, SKIP that
part and still post what you have. Never ask the user for tokens — your NyxID-brokered tools broker
all credentials.

## How to run it

1. **Resolve inputs.** Take the raw Lark event from the current invocation, plus deterministic
   metadata: `weekKey` (ISO week `YYYY-Www`), `submitTime` (ISO), and `attemptId`. The target Bitable
   is baked into the builder (`app_token` `BASE_APP_TOKEN_PLACEHOLDER_1`, `table_id`
   `TABLE_ID_PLACEHOLDER_4`) and the CHO recipient defaults to `ou_PLACEHOLDER_OPEN_ID_1`; if the
   user/host supplies a real `app_token`/`table_id`/`choOpenId`, carry them into steps 4–6. If the
   base is unresolvable, proceed in summary-only mode (still answer the employee).

2. **PARSE the event.** Run `scripts/build_weekly_goal_audit_payload.js` with `mode: "parse_event"`
   to normalize the event into `openId`, `employeeDisplayName`, `goalsForAudit`, `messageId`,
   `intent` (`audit` vs weekend `review`), etc. Honor its result: if it returns `skip: true` (URL
   challenge, duplicate, bot/non-target event), do exactly that. If a goal message references a PDF,
   download + OCR it with your own file/PDF tool and feed the extracted text forward.

3. **ANALYZE with your own model.**
   - audit intent: score the weekly goals (0–10) and produce highlights, red flags, per-goal
     rewrites, and value dimensions (only `风险降低 / 效率提升 / 收入创造 / 成本降低 / 长期资产 /
     主动发现与改善`).
   - review intent: produce the completion status, blockers, hidden wins, the employee echo, and the
     CHO individual-momentum diagnosis.
   If the goals are written in English, also translate the employee-facing reply and pass it through.

4. **BUILD the exact payloads.** Run `scripts/build_weekly_goal_audit_payload.js` via `code_execute`
   (language `"javascript"`; NO stdin — inline the data into the code):
   - audit: `console.log(JSON.stringify(buildPayload({ mode: "build_audit_payloads", openId,
     employeeDisplayName, employeeEmail, weekKey, submitTime, attemptId, messageId, goalText,
     goalsForAudit, auditOutput, translatedReply })))`
   - review (read the goal record first): for the latest record run `{ mode: "build_review_search",
     openId, weekKey }` and read it via step 5's Base search, then
     `console.log(JSON.stringify(buildPayload({ mode: "build_review_payloads", openId,
     employeeDisplayName, goalText, recordId, reviewOutput, choOpenId })))`.
   Use the script output. If code execution is unavailable, follow
   `references/weekly-goal-audit-contract.md` field-for-field.

5. **WRITE the Base record.** For audit, create the record via `nyxid_proxy` `{slug:"api-lark-bot",
   path:"/open-apis/bitable/v1/apps/<app_token>/tables/<table_id>/records", method:"POST",
   body:<lark.createRecord.body>}`. For review, first search
   (`POST .../records/search` with `lark.searchRecords.body`) to resolve `recordId`, then update via
   `PUT /open-apis/bitable/v1/apps/<app_token>/tables/<table_id>/records/<recordId>` with
   `lark.updateRecord.body`.

6. **POST the messages.** Send the employee reply (`lark.employeeMessage`) — and, for review, the CHO
   diagnosis (`lark.choMessage`) — via `lark_messages_send` to the relevant `open_id`; the equivalent
   is `nyxid_proxy` `POST /open-apis/im/v1/messages?receive_id_type=open_id`. **If no base target was
   resolved OR the Base write fails, SKIP the Bitable write and STILL post the built employee reply
   (and CHO diagnosis) to the chat — never fail the run for a missing base.**

7. **REPORT** one line: intent (audit/review), employee, score or completion status, record
   written/updated (or "summary-only"), and which messages were posted.

## Payload builder reference

Bundled script: `scripts/build_weekly_goal_audit_payload.js`. Modes: `parse_event`,
`build_review_search`, `build_audit_payloads`, `build_review_payloads`; unsupported modes return
`skip: true`. The employee roster (user_id → name/email), the allowed value dimensions, and the
target base `BASE_APP_TOKEN_PLACEHOLDER_1`/`TABLE_ID_PLACEHOLDER_4` (overridable via
`appToken`/`tableId`) are baked in; the CHO recipient defaults to `ou_PLACEHOLDER_OPEN_ID_1`
(overridable via `choOpenId`). LLM/audit/review/translation text and OCR text must be passed as
input — the script never calls a model or the network. Output is one of `skip`,
`needs_more_information` + `missing`, the normalized event, the Base search payload, the audit
payloads (`employeeMessage` + `createRecord`), or the review payloads (`updateRecord` +
`employeeMessage` + `choMessage`). Exact aliases, field mapping, and examples are in
`references/weekly-goal-audit-contract.md`.

## Guardrails

- Only use data the tools actually returned — never invent goals, employee data, Base records, open
  ids, OCR text, translated replies, or model analysis.
- Prefer running the bundled script; it is the deterministic source of truth for payload shape.
- All token exchange, Base access, and Lark sends go through your NyxID-brokered tools; never handle
  raw secrets.
