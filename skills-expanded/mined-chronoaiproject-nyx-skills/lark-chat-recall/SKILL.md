---
name: lark-chat-recall
version: "1.2"
description: Recall and summarize Lark conversations — pull a chat's history over a time window through the real im/v1 history API, reconstruct discussions, and answer "who said what" with quoted evidence. Use for "总结这个群今天聊了什么 / 上周谁提过X / 找一下关于Y的讨论". Requires the bot tenant scope im:message.group_msg; reports the exact missing scope verbatim when absent.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - lark
    - messages
    - recall
    - summary
---

# Lark Chat Recall

Use this when someone wants to find, reconstruct, or summarize past Lark messages: a digest of a
busy group, a half-remembered decision, everything about a topic.

**You (the agent) pull real history yourself.** Everything is read-only. Never invent quotes:
every claim in your answer must trace to a really-returned message. If history is unavailable,
say exactly why (quote the error) — do NOT fill the gap from your own conversation context and
present it as a search result; clearly label any context-only fallback as "仅基于当前可见上下文,
非完整历史".

> **Companion skill.** Raw send / reply / react / read one message / chat lookup live in
> `lark-im-ops`; this skill is the read-only recall + summarize specialization layered on the same
> `im/v1` history pull. Use im-ops to act on a chat, this to reconstruct one.

## How to run it

1. **Frame the ask.** Scope = the CURRENT chat unless the user names another (then resolve its
   chat_id via `lark_chats_lookup`). Convert "今天/上周/这个月" into a concrete time window
   (Asia/Shanghai unless stated otherwise).

2. **Pull history (primary, real endpoint).** NyxID-brokered call:
   `nyxid_proxy` `{slug:"api-lark-bot", method:"GET",
   path:"/open-apis/im/v1/messages?container_id_type=chat&container_id={chat_id}&start_time={unix_s}&end_time={unix_s}&sort_type=ByCreateTimeAsc&page_size=50"}`
   — follow `page_token` until the window is covered (cap ~10 pages and say so if truncated).
   This requires bot tenant scope `im:message.group_msg` (group chats). On `230027` quote the
   `need scope: ...` text verbatim and tell the user to grant that scope to the bot app in the
   Lark developer console — that is the fix, not "token 过期".

3. **Hydrate details when needed.** For specific messages (cards, rich posts), call
   `lark_messages_batch_get` `{message_ids:[om_...]}` (≤50, real endpoint) for full content.

4. **Do NOT rely on `lark_messages_search`.** Known platform defect as of 2026-06-11: that tool
   calls `im/v1/messages/search`, which does not exist in the Lark OpenAPI — the gateway returns a
   misleading `99991663 Invalid access token`. If you try it and see that signature, it is NOT a
   token problem; fall back to step 2 and mention the defect once. Keyword "search" = pull the
   window via step 2, then filter/match locally yourself.

5. **Answer in one of three shapes:**
   - **Fact recall** — the answer plus evidence: sender, time, and the quoted message line.
   - **Thread reconstruction** — chronological `[time] 人名: 内容`, trimmed to the relevant exchange.
   - **Digest** — group by topic, 3-6 bullets per topic, each bullet noting how many messages it
     covers; close with visible action items / open questions. Only include events that appear in
     the pulled messages — no inferred items.

6. **Honesty.** History covers what the bot identity can see (bot must be IN the chat). If the
   window returned nothing, say so with the exact filters used. Resolve sender ids to names via
   chat member info when available; otherwise show the id, never guess a name.

## Guardrails

- Read-only: never send, react, or forward while in this skill; deliver in the current chat.
- When recalling OTHER chats, summarize rather than bulk-quote, and name the source chat for every
  quote.
- Quote verbatim, attribute correctly, keep timestamps; never reorder events to fit a narrative.
- Never ask the user for tokens — your NyxID-brokered tools handle all credentials.
