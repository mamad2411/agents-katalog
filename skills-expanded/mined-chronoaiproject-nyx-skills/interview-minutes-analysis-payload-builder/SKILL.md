---
name: interview-minutes-analysis-payload-builder
version: "2.1"
description: Runs the interview-minutes analysis flow end to end — scans the ATS Bitable, reads the Lark Minutes transcript, analyzes the interview with your own model, writes the AI notes back to the ATS record, and posts the HR card.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - interview
    - lark
    - payload-builder
  clawdbot:
    emoji: "memo"
    files:
      - "references/*"
      - "scripts/*"
---

# Interview Minutes Analysis

Use this when someone asks to analyze pending Lark Minutes interview records and notify HR.

**You (the agent) run the WHOLE flow yourself with your own tools, then WRITE the results to Lark
Bitable and post a summary to the chat.** Do NOT refuse, do NOT just describe, do NOT claim "the
skill only formats" — drive the flow. If a data source or the target base is unavailable, SKIP that
part and still post what you have. Never ask the user for tokens — your NyxID-brokered tools broker
all credentials.

## How to run it

1. **Resolve inputs and target.** Use the flow's ATS Bitable and HR recipient unless the user
   overrides them: target Bitable `app_token` `FSl0bCi9raBuLbsdTbHlgb0agwf`, `table_id`
   `tblgZgSqmeBag2na`; HR `open_id` `ou_4473a6a9feeca68d2eeaf2cb95416f37`. If the user named a
   specific record or Minutes URL, use it; otherwise process the first pending ATS record. If the
   ATS base is unresolvable, proceed in summary-only mode.

2. **COLLECT the ATS record.** Read the ATS Bitable via `nyxid_proxy` `{slug:"api-lark-bot",
   path:"/open-apis/bitable/v1/apps/<app_token>/tables/<table_id>/records?page_size=100&filter=<urlencode('CurrentValue.[Minutes URL]!=\"\"')>",
   method:"GET"}` (or the equivalent `lark_*` tool). Pick the first item whose `Minutes URL`
   contains `/minutes/` and whose `AI Interview Notes` is empty. Keep `record_id`, `Minutes URL`,
   `Candidate Name`, `Job Title`, `Job Description`, and `Interviewer`. If there is no pending
   record, post that and stop.

3. **COLLECT the Minutes transcript.** Extract `minute_token` with `/minutes/([a-z0-9]+)/i`, then
   read Minutes via `nyxid_proxy` slug `api-lark-bot` (or `lark_minutes`):
   `/open-apis/minutes/v1/minutes/{minute_token}` and
   `/open-apis/minutes/v1/minutes/{minute_token}/transcript?need_speaker=true&need_timestamp=true&file_format=txt`.
   Use the returned title, else `<candidate_name> 面试`. If the transcript is empty, post that it may
   still be processing and stop.

4. **ANALYZE.** With your own model, classify the role as `技术岗`, `商业/职能岗`, or `家政/个人助理岗`
   from the title/JD/transcript, run the role-specific veto checks, and return valid JSON with
   `veto_check`, `overall`, `score`, `summary`, `strengths`, `red_flags`, `key_moments`,
   `culture_fit`, `culture_fit_reason`, `next_step`, `suggested_questions`, and `veto_count`.
   - 商业/职能岗: AI 实质改造、具体 AI 案例、独立贡献、从 0 到 1、思维深度。
   - 技术岗: AI 编程实质、Agent/AI 技术栈、系统设计能力、独立交付能力，`v5` 填 `N/A`。
   - 家政/个人助理岗: 诚信核查、稳定性、核心技能，`v4` 和 `v5` 填 `N/A`。
   Any VETO caps `score` at 2; multiple VETOs normally mean `score: 1` and `overall: "Strong Pass"`.
   Base every judgment on transcript evidence.

5. **BUILD the exact payloads.** Run `scripts/build_interview_analysis_payload.js` via `code_execute`
   (language `"javascript"`; NO stdin — inline the data into the code):
   `console.log(JSON.stringify(buildPayload({ mode: "build_payload", analysis, hrOpenId, atsAppToken,
   atsTableId, recordId, generatedAt, candidateName, jobTitle, minuteTitle })))`, where `generatedAt`
   is the current Asia/Singapore timestamp. Use the output's `lark.bitableUpdate.body` and
   `lark.cardMessage.body`. If code execution is unavailable, follow
   `references/interview-analysis-contract.md` field-for-field.

6. **WRITE the notes, then post the card.** Update the ATS record via `nyxid_proxy`
   `{slug:"api-lark-bot",
   path:"/open-apis/bitable/v1/apps/<app_token>/tables/<table_id>/records/<record_id>", method:"PUT",
   body:<lark.bitableUpdate.body>}`. THEN send the HR interactive card with `lark_messages_send` (or
   `reply_with_interaction`); the equivalent is `nyxid_proxy`
   `POST /open-apis/im/v1/messages?receive_id_type=open_id` with `lark.cardMessage.body`. **If no ATS
   target was resolved OR the update fails, SKIP the Bitable write and STILL post the analysis card /
   summary to the chat — never fail the run for a missing base.**

7. **REPORT** one line: candidate, job title, score/overall, ATS record updated (or "summary-only"),
   HR card sent.

## Payload builder reference

Bundled script: `scripts/build_interview_analysis_payload.js`. Accepts `mode: "build_payload"` (or
omitted); other modes return `skip: true`. Required after alias normalization: `analysis`,
`hrOpenId`, `atsAppToken`, `atsTableId`, `recordId`, `generatedAt`. Optional: `candidateName`,
`jobTitle`, `minuteTitle`. `analysis` may be a direct object or a Groq-style
`choices[0].message.content` string. Output includes `notes_text`, `card`, `lark_card_json`,
`lark.bitableUpdate` (PUT), and `lark.cardMessage` (POST to `open_id`). Exact aliases, fallback
parsing, card fields, and request bodies are in `references/interview-analysis-contract.md`.

## Guardrails

- Only use the Lark records, Minutes metadata, transcript text, and analysis evidence the tools
  actually returned — never invent ids, records, statuses, quotes, or candidate details.
- Prefer running the bundled script; it is the deterministic source of truth for payload shape.
- All Lark access, sends, and credential exchange go through your NyxID-brokered tools or Lark
  tools; never handle raw secrets.
