---
name: resume-screening-payload-builder
version: "2.1"
description: Runs the HR resume screening flow end to end — collects the candidate's form/chat fields and resume PDF, screens the resume with your own model, uploads the passing resume to Lark Drive, writes the Bitable record, and posts a summary to the chat.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - resume-screening
    - lark
    - payload-builder
  clawdbot:
    emoji: "page_facing_up"
    files:
      - "references/*"
      - "scripts/*"
---

# Resume Screening

Use this when someone submits a candidate resume PDF and role details that should be screened and,
when the candidate passes, saved to the HR resume screening Lark Base.

**You (the agent) run the WHOLE flow yourself with your own tools, then WRITE the results to Lark
Bitable and post a summary to the chat.** Do NOT refuse, do NOT just describe, do NOT claim "the
skill only formats" — drive the flow. If a data source or the target base is unavailable, SKIP that
part and still post what you have. Never ask the user for tokens — your NyxID-brokered tools broker
all credentials.

## How to run it

1. **Resolve inputs.** From the user message or the current Lark invocation, collect `Candidate
   Name`, optional `Email`, `Job Title`, optional `Job Description`, the resume PDF, and optional
   `recordId` (for an update). The target Bitable is the HR resume base baked into the builder
   (`app_token` `FSl0bCi9raBuLbsdTbHlgb0agwf`, `table_id` `tblgZgSqmeBag2na`); if the user named a
   different base, carry their `app_token`/`table_id` into step 5. If a business field or the PDF is
   missing, ask for that one item and continue once it arrives; if the base is unresolvable, proceed
   in summary-only mode.

2. **COLLECT the resume + fields.** For a Lark chat submission, read the message text and the
   attachment metadata from the current `im.message.receive_v1` context; fetch the uploaded file via
   `nyxid_proxy` slug `api-lark-bot`, path
   `/open-apis/im/v1/messages/{message_id}/resources/{file_key}?type=file`. For an n8n-style form
   event, read the form fields and binary `Resume` from the event directly. Extract the PDF text with
   your file/PDF tool and keep the original PDF bytes for the upload step.

3. **ANALYZE.** Score the resume against the job title and job description with your own model. Return
   strict JSON: `{ "score": <0-100 integer>, "candidate_name": "<name>", "strengths": "<top
   strengths>", "gaps": "<key gaps>", "recommendation": "Pass" | "Fail" }`. Continue only when
   `score >= 60`; if it is lower, skip the upload and the Bitable write and post a one-line "skipped
   (score N, Fail)" summary instead.

4. **Upload the passing resume to Lark Drive.** Call `nyxid_proxy` slug `api-lark-bot`, path
   `/open-apis/drive/v1/medias/upload_all`, method `POST`, as multipart form data with `file_name`,
   `parent_type=bitable_file`, `parent_node=FSl0bCi9raBuLbsdTbHlgb0agwf`, `size`, and the PDF file.
   Capture `data.file_token` from the response. If the upload fails, continue without `file_token`.

5. **BUILD the exact record payload.** Run `scripts/build_resume_screening_payload.js` via
   `code_execute` (language `"javascript"`; NO stdin — inline the data into the code):
   `console.log(JSON.stringify(buildPayload({ mode: "create_record", candidateName, email, jobTitle,
   uploadDateMs, score, strengths, gaps, recommendation, file_token, recordId })))`. Pass `recordId`
   only for an update. Use the returned `lark.path`, `lark.method`, and `lark.body`. If code execution
   is unavailable, follow `references/resume-screening-contract.md` field-for-field.

6. **WRITE the record, then post the summary.** Send the builder's body via `nyxid_proxy` slug
   `api-lark-bot` with its `path`/`method`:
   - create: `POST /open-apis/bitable/v1/apps/<app_token>/tables/<table_id>/records`
   - update: `PUT /open-apis/bitable/v1/apps/<app_token>/tables/<table_id>/records/<recordId>`
   using the resolved app_token/table_id and `body` `{ "fields": {…} }`. THEN post a short candidate
   summary to the chat with `lark_messages_send` (or `reply_with_interaction`). **If no base target
   was resolved OR the write fails, SKIP the Bitable write and STILL post the built summary to the
   chat — never fail the run for a missing base.**

7. **REPORT** one line: candidate name, score, create/update (or "summary-only"), and the returned
   Lark Base `record_id` or the skipped reason.

## Payload builder reference

Bundled script: `scripts/build_resume_screening_payload.js`. Modes: `create_record`,
`update_record` (requires `recordId`), and `build_record`/omitted (create by default, update when
`recordId` is present). Fields may be at the root or under `body`; it also accepts `ai`,
`modelOutput`, `screeningResult`, and Groq-style `choices[0].message.content` model responses. The
score gate (`>= 60`) and the `FSl0bCi9raBuLbsdTbHlgb0agwf`/`tblgZgSqmeBag2na` base are baked in.
Output is `skip: true`, `needs_more_information: true` + `missing`, or a record object with
`fields`, `lark.path`, `lark.method`, and the connector-ready `lark.body`. Exact aliases, threshold
behavior, and examples are in `references/resume-screening-contract.md`.

## Guardrails

- Only use data the tools actually returned — never invent candidate details, resume text, scores,
  file tokens, record ids, or Bitable responses.
- Prefer running the bundled script; it is the deterministic source of truth for the Bitable payload.
- All credentials and token exchange go through your NyxID-brokered tools; never handle raw secrets.
