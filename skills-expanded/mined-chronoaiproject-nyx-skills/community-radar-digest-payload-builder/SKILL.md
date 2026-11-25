---
name: community-radar-digest-payload-builder
version: "2.2"
description: Runs the community-radar flow end to end and posts a digest to the chat.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - community-radar
    - lark
    - payload-builder
  clawdbot:
    emoji: "satellite"
    files:
      - "references/*"
      - "scripts/*"
---

You (the agent) run the WHOLE flow yourself with your tools, then POST the result to the current Lark chat. Do NOT refuse, do NOT just describe. If a data source or sink is unavailable, SKIP it and still post what you have.

# Community Radar

Use this when someone asks for a NyxID community radar run, community signal digest, or daily radar card.

## How to run it

1. **COLLECT via tools, using ONLY bound connectors.**
   - GitHub -> `nyxid_proxy` slug `api-github` (bound ✓).
   - Public web / RSS / Hacker News / forums / any other public endpoint -> `web_fetch` (no credential, ✓).
   - ⚠ `api-reddit` and `api-twitter` are NOT bound for this bot — do NOT depend on them. Use `web_fetch` on public endpoints instead where possible; otherwise SKIP that source and note `(<source> skipped — connector not bound)` in the message. NEVER fail the run because one source is unavailable.
   - Useful public sources: `https://hnrss.org/newest`, `https://community.n8n.io/latest.rss`, `https://community.home-assistant.io/latest.rss`, `https://discourse.ros.org/latest.rss`, `https://lobste.rs/rss`, and public Hacker News item JSON.

2. **ANALYZE with your own model.** Normalize entries into `title`, `url`, `platform`, `author`, `excerpt`, `pubDate`, and `hoursAgo`; dedupe URLs; summarize, score, rank, and judge NyxID fit. Keep useful `yes` / `maybe` items, mark skipped sources, and assign `freshness`, `category`, `angle_code`, `cohort`, `cta`, `batch_id`, `relevance_score`, `quality_score`, and `llm_verdict`.

3. **BUILD the message body by running `scripts/build_community_radar_payload.js` via `code_execute` with language `"javascript"`**. `code_execute` has NO stdin, so inline the collected data into the code: paste the whole script, then call its exported `buildPayload` and print the result. The script exports `module.exports = { buildPayload }`, so end the code with:
   ```javascript
   // ...full contents of scripts/build_community_radar_payload.js above...
   console.log(JSON.stringify(buildPayload({
     mode: "build_all",
     runTime: "<ISO timestamp>",
     chatId: "<current chat id when available>",
     cardUrl: "<optional base table URL>",
     items: [/* normalized radar items */]
   })));
   ```
   Use the script output `lark.sendMessage.content`, `lark_card`, or `summary` for the chat digest. If you cannot run code or the script returns `skip` / `needs_more_information`, fall back to `references/community-radar-contract.md` and build a concise digest from the collected items plus skipped-source notes.

4. **POST it to the CURRENT chat via `lark_messages_send`** (or `lark_messages_reply` / `reply_with_interaction`). THIS STEP ALWAYS HAPPENS — it is the demo output. If there are no valid items, post a plain "no valid new radar items" digest with the sources checked and skipped.

5. **OPTIONAL: write a Lark Bitable record best-effort ONLY.** Do this only if a target base `app_token` + `table` is actually provided; then use the script's `lark.createRecordRequests`. If no target Base is provided, SKIP Bitable and still post the chat message. Never block on a missing Bitable.

## Payload builder reference

The bundled script is `scripts/build_community_radar_payload.js`. It accepts:

- `build_records` (`records`, `base_records`) — build one Lark Base create-record request per valid radar item.
- `build_digest` (`digest`, `card`) — build the final Lark interactive card from already-written record fields; requires `runTime`.
- `build_all` — build Base records and the digest together; this is the default and requires `runTime`.

Input may be at the root or under `body`. Items may be plain objects or n8n-style `{ "json": { ... } }`. Connector ids can be passed as `appToken`, `tableId`, `chatId`, and `cardUrl`; exact aliases and output shapes are in `references/community-radar-contract.md`.

Script output is one of: `skip: true`; `needs_more_information: true` plus `missing`; `message_type: "lark_base_records"` with `lark.createRecordRequests`; `message_type: "lark_interactive_message"` with `lark.sendMessage`; or `message_type: "community_radar_lark_payloads"` with both.

## Guardrails

- Only use real returned data; never invent threads, record ids, URLs, statuses, verdicts, app tokens, table ids, or chat ids.
- Prefer running the bundled script; it is the deterministic source for Base fields and the Lark card.
- Credentials and sending must go through NyxID-brokered tools or Lark tools; never request or expose raw secrets.
- The primary demonstrable output is the current-chat digest message.
