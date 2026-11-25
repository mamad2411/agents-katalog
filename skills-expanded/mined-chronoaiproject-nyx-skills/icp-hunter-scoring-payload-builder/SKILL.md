---
name: icp-hunter-scoring-payload-builder
version: "2.3"
description: Runs the NyxID ICP Hunter scoring flow end to end — searches ICP evidence, enriches and scores candidates with your own model, writes the new candidates to the ICP Hunter Lark Base, and posts the run report card.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - icp-hunter
    - lark
    - payload-builder
  clawdbot:
    emoji: "dart"
    files:
      - "references/*"
      - "scripts/*"
---

# NyxID ICP Hunter Scoring

Use this when someone asks to run ICP Hunter — score likely NyxID ICP users, write new candidates to
the ICP Hunter Lark Base, and post the run report.

**You (the agent) run the WHOLE flow yourself with your own tools, then WRITE the results to Lark
Bitable and post a summary to the chat.** Do NOT refuse, do NOT just describe, do NOT claim "the
skill only formats" — drive the flow. If a data source or the target base is unavailable, SKIP that
part and still post what you have. Never ask the user for tokens — your NyxID-brokered tools broker
all credentials.

## How to run it

1. **Resolve run context.** Use today's date, compute `weekTag` as ISO week (`YYYY-Www`), make a
   `batchId` like `icp-<timestamp>`, default `max_results` to `5`. Target Bitable: the ICP Hunter
   base baked into the builder (`app_token` `BASE_APP_TOKEN_PLACEHOLDER_2`, `table_id`
   `TABLE_ID_PLACEHOLDER_3`, chat `oc_PLACEHOLDER_CHAT_ID_1`); if the user supplies a real
   `app_token`/`table_id`/`chat_id`, carry them into steps 6–8. Run the ICP query set: Claude
   Code/Codex/Cursor + MCP/API-key/credential pain, `.mcp.json` leaks/rotation, GitHub MCP config
   credentials, Home Assistant/Homelab credential pain, HA Forum agent/API-key threads, and n8n Forum
   credential-rotation threads.

2. **DISCOVER the search service, then COLLECT evidence.** Do NOT hardcode a slug. First call
   `nyxid_services` `{action:"list"}` and pick the caller's Tavily-compatible search service — match a
   service whose endpoint is `https://api.tavily.com`, or whose `slug`/`label` contains `tavily` or
   `search`. Use THAT service's `slug` for the search call: `nyxid_proxy` `{slug:"<discovered-slug>",
   path:"/search", method:"POST", body:{ query, search_depth:"advanced", max_results:5,
   include_raw_content:true, include_domains }}`. Keep `title`, `url`, `content`, `raw_content`, and
   `score` per result.
   - **If no search service is found, do NOT fail.** Include a one-line hint in the final run report
     telling the caller to connect a Tavily search service in NyxID (endpoint `https://api.tavily.com`,
     bearer auth; an org admin can share it team-wide via `nyxid service add --custom --org <org>`).
     **NEVER ask the caller to paste an API key into chat** — credentials are configured by the user in
     NyxID, never handled by this skill. Then continue with `web_fetch` public-forum evidence only
     (degraded) and mark the search source as skipped.

3. **ENRICH platform evidence with what is actually bound.**
   - GitHub: `nyxid_proxy` slug `api-github` for `GET /users/{login}` and
     `GET /users/{login}/repos?sort=updated&per_page=5`.
   - Public Discourse forums: `web_fetch` the public topic JSON, e.g.
     `https://community.home-assistant.io/t/{slug}/{id}.json`,
     `https://community.n8n.io/t/{slug}/{id}.json`, `https://discourse.ros.org/t/{slug}/{id}.json`.
   - ⚠ `api-reddit` and `api-twitter` are NOT bound — SKIP Reddit/X enrichment and note it in the
     report; score those candidates from the Tavily `content`/`raw_content` and public web evidence
     instead. Do not block the run on them.

4. **ANALYZE/score with your own model.** Score the enriched evidence against NyxID ICP fit and emit
   grounded candidate JSON with `users`: username, priority, cohort, platform, profile/evidence URLs,
   scores, score breakdown, contact channel, language/timezone, raw evidence, recommended action,
   post date, thread role. Validate every username against the enriched author fields before keeping
   it; drop placeholders. For P0 users, draft outreach from the user's own raw evidence and keep it in
   `outreach_draft`.

5. **READ existing Lark Base records** (for dedupe) via `nyxid_proxy` `{slug:"api-lark-bot",
   path:"/open-apis/bitable/v1/apps/<app_token>/tables/<table_id>/records/search", method:"POST",
   body:{ page_size:500, field_names:["用户ID","平台","证据链接","Profile 链接"],
   automatic_fields:false }}`. Use the returned records as `existingRecords` (empty array if the base
   is unavailable).

6. **BUILD the exact payloads.** Run `scripts/build_icp_hunter_payload.js` via `code_execute` (language
   `"javascript"`; NO stdin — inline the data into the code):
   `console.log(JSON.stringify(buildPayload({ mode: "build_payloads", users, existingRecords, runTime,
   weekTag, batchId, appToken, tableId, receiveId })))` (`runTime` = ISO timestamp, `receiveId` = the
   target chat_id). If your model output needs parsing first, run the same script with
   `mode: "parse_scoring"`. Use the output for every Base write and the report card. If code execution
   is unavailable, follow `references/icp-hunter-contract.md` field-for-field.

7. **WRITE the Base records.** For each `createRecordPayloads[]`, call `nyxid_proxy`
   `{slug:"api-lark-bot", path:"/open-apis/bitable/v1/apps/<app_token>/tables/<table_id>/records",
   method:"POST", body:<that payload's `body`, i.e. `{ fields: {…} }`>}` using the resolved
   app_token/table_id.

8. **POST the run report.** Send the interactive card to the chat with `lark_messages_send` (or
   `reply_with_interaction`) using `sendMessagePayload.content` from the builder. **If no base target
   was resolved OR the writes fail, SKIP the Bitable writes and STILL post the built run-report card /
   summary to the chat — never fail the run for a missing base.**

9. **REPORT** one line: records written (or "summary-only"), P0/P1/P2 counts, and where the report was
   posted. If the builder returns `skip: true` or no source yields usable candidates, say so plainly.

## Payload builder reference

Bundled script: `scripts/build_icp_hunter_payload.js`. Modes:

- `parse_scoring` — accepts model output at root or under `scoringResponse`/`geminiResponse`/
  `response`; parses the first JSON object with `users`; drops placeholder usernames.
- `build_payloads` — accepts scored users plus optional existing Base records; returns Base
  create-record payloads (`createRecordPayloads`), `stats`, and the Lark interactive report
  (`sendMessagePayload`). Required: `users` and `runTime` (plus `fallbackPostDate` when a kept user
  has no post date). Optional: `existingRecords`, `weekTag`, `batchId`, `appToken`, `tableId`,
  `receiveId` (base defaults `BASE_APP_TOKEN_PLACEHOLDER_2`/`TABLE_ID_PLACEHOLDER_3`, chat
  `oc_PLACEHOLDER_CHAT_ID_1`).

Output may be `skip: true`, `needs_more_information` + `missing`, parsed users, or the full payload
object. Exact aliases, enums, dedupe rules, and examples are in `references/icp-hunter-contract.md`.

## Guardrails

- Only use data the tools actually returned — never invent users, scores, outreach drafts, record
  ids, app tokens, table ids, chat ids, or records.
- Prefer running the bundled script; it is the deterministic source for field mapping, dedupe, stats,
  and the report card.
- All credentials and token exchange go through your NyxID-brokered tools; never handle raw secrets.
