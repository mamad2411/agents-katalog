---
name: tech-digest-aggregator-payload-builder
version: "2.2"
description: Runs the tech-digest aggregator flow end to end and posts a digest to the chat.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - tech-digest
    - lark
    - payload-builder
  clawdbot:
    emoji: "newspaper"
    files:
      - "references/*"
      - "scripts/*"
---

You (the agent) run the WHOLE flow yourself with your tools, then POST the result to the current Lark chat. Do NOT refuse, do NOT just describe. If a data source or sink is unavailable, SKIP it and still post what you have.

# Tech Digest Aggregator

Use this when someone asks for an AI / tech news digest, RSS roundup, GitHub trend digest, Hacker News tech digest, or "AI资讯小报 / AI干货小报 / 推特价值小报".

## How to run it

1. **COLLECT via tools, using ONLY bound connectors:**
   - GitHub → `nyxid_proxy` slug `api-github` (bound ✓).
   - Public web / RSS / Hacker News, and any other public endpoint → `web_fetch` (no credential, ✓).
   - ⚠ `api-reddit` and `api-twitter` are NOT bound for this bot. Do NOT depend on them. Use `web_fetch` on public endpoints instead where possible; otherwise SKIP that source and note `(<source> skipped — connector not bound)` in the message. NEVER fail the run because one source is unavailable.
   - Normalize collected rows into `rssItems` / `tweetItems`-compatible objects with `标题`, `内容`, `日期`, `链接`, `来源`, `板块`, `分类`, and optional `分类理由`.

2. **ANALYZE with your own model.** Summarize, score, classify, dedupe, rank, and choose any Top10 items yourself. Keep categories compatible with the builder contract where practical: `产品发布/更新`, `博客/研究/评论/深度报道`, or `其他（融资/社会舆论/人事变动等）`.

3. **BUILD the message body** by running `scripts/build_tech_digest_payload.js` via `code_execute` with language `"javascript"`. `code_execute` has NO stdin, so inline your collected/analyzed data into the code: paste the whole script, then append a call to its exported `buildPayload` and print the result. The script exports `module.exports = { buildPayload }`, so end the code with:
   ```javascript
   // ...full contents of scripts/build_tech_digest_payload.js above...
   console.log(JSON.stringify(buildPayload({
     mode: "build_messages",
     date: "<YYYY-MM-DD>",
     rssItems: [/* normalized rows */],
     tweetItems: [],
     top10: []
   })));
   ```
   Use the returned `messages[*].markdown`, `messages[*].card`, or `lark.sendMessages[*].content` as the digest body. If you cannot run code or the script needs clarification, fall back to `references/tech-digest-contract.md` field-for-field.

4. **POST it to the CURRENT chat** via `lark_messages_send`, `lark_messages_reply`, or `reply_with_interaction`. THIS STEP ALWAYS HAPPENS — it is the demo output. If the builder returns multiple digest messages, post the useful digest set in order or combine their Markdown into one current-chat summary. If no source produced items, post a short "no items found" digest plus any skipped-source notes.

5. **OPTIONAL:** writing a Lark Bitable record is best-effort ONLY. Do it only if a target base `app_token` plus table id is actually provided; if not, SKIP and still post the chat message. Never block on a missing Bitable.

## Payload builder reference

Run `scripts/build_tech_digest_payload.js` with `mode: "build_messages"` for chat output, or `mode: "build_all"` when a real Bitable target is also available. Inputs may be at the root or under `body`; aliases and exact output shapes are in `references/tech-digest-contract.md`.

The script can emit `needs_more_information`, `skip`, `messages`, `records`, and Lark-shaped request payloads. For the active playbook, the final visible result is always a Lark chat post, using the best digest body available from the script output or contract fallback.

## Guardrails

- Never invent fetched articles, GitHub records, public endpoint results, or connector credentials.
- Never wait for `api-reddit`, `api-twitter`, or Bitable availability before posting the chat digest.
- Prefer the bundled builder for final message structure; use your model for collection cleanup, summarization, scoring, and ranking.
