---
name: twilio-conversation-memory
version: 1.0.0
description: Give a Twilio conversational agent durable memory and continuity across sessions and channels by persisting, summarizing, and retrieving conversation state keyed to participant identity.
author: matrixx0070
tags: [twilio, memory, ai-assistant, continuity, rag]
capabilities: []
---

## When to use

Use this when an assistant must remember prior turns, user facts, or open tickets across separate sessions or across channels (a user who started on SMS returns on WhatsApp and expects continuity). Reach for it when you need to decide what to store, how to key it to a stable identity, how to summarize long histories that exceed the model context window, and how to retrieve the right slice on each new turn while honoring retention/privacy rules.

**Not for:** raw wire-level Conversations REST calls (use twilio-conversations-classic-api), full support-system architecture (use twilio-customer-support-architect), or building/grounding the knowledge base itself (use twilio-enterprise-knowledge). Route the surrounding session/channel orchestration to twilio-conversation-orchestrator.

## Method

1. Pick a stable memory key. Prefer a durable participant identity over a channel address. For chat participants use the Conversations `Identity`; for SMS/WhatsApp the channel address (`MessagingBinding.Address`, +E164 or `whatsapp:`) is the only stable handle unless you map it to an internal user id. Decision point: if the same human uses multiple channels, maintain an identity-resolution table mapping each address/identity to one canonical `user_id` — memory keys on `user_id`, not the raw address.
2. Choose the persistence tier. AI Assistant **Sessions** carry short-horizon turn state automatically per assistant conversation. For anything that must outlive a session or cross channels, write to your own store (Postgres/Redis/DynamoDB) keyed by `user_id`. Decision point: session-only if continuity within one contiguous exchange is enough; own-store if continuity must survive session expiry or channel switches.
3. Define the memory schema. Persist: canonical `user_id`, channel bindings, a rolling `summary` (compacted history), a bounded `recent_turns` buffer (last N raw messages), and typed `facts` (name, plan, open ticket ids). Keep raw transcripts separate from derived facts so you can re-summarize without losing ground truth.
4. Summarize on threshold. When `recent_turns` token estimate exceeds your budget, summarize the oldest turns into `summary` and evict them from the buffer. Decision point: summarize by turn count (simple) or by token estimate (accurate for mixed media/long messages) — prefer tokens near model limits.
5. Retrieve on each new turn. Load `summary` + `recent_turns` + top-k relevant `facts`, inject them as system/context ahead of the user message. If the assistant also does RAG, keep memory context and knowledge citations in distinct blocks so the model can attribute correctly.
6. Write back after each turn. Append the new user+assistant turns to `recent_turns`, update `facts` on explicit new information, and bump `updated_at`. Do this write-through (at turn commit), not lazily, so a crash never drops the last exchange.
7. Enforce retention. Apply a TTL/retention window per your privacy policy, support hard delete on request (right-to-erasure), and never persist secrets (OTPs, card/PAN, full auth tokens) into memory.

## Example

```python
# Retrieve-then-generate on a new turn, memory keyed by canonical user_id.
def load_memory(store, user_id):
    m = store.get(user_id) or {"summary": "", "recent_turns": [], "facts": {}}
    return m

def build_context(mem):
    blocks = []
    if mem["summary"]:
        blocks.append(f"[CONVERSATION SUMMARY]\n{mem['summary']}")
    if mem["facts"]:
        blocks.append("[KNOWN FACTS]\n" + "\n".join(f"- {k}: {v}" for k, v in mem["facts"].items()))
    for t in mem["recent_turns"][-8:]:
        blocks.append(f"{t['role'].upper()}: {t['text']}")
    return "\n\n".join(blocks)

def commit_turn(store, user_id, mem, user_text, agent_text, token_budget=3000):
    mem["recent_turns"] += [{"role": "user", "text": user_text},
                            {"role": "assistant", "text": agent_text}]
    while estimate_tokens(mem["recent_turns"]) > token_budget and len(mem["recent_turns"]) > 4:
        oldest = mem["recent_turns"][:2]
        mem["summary"] = summarize(mem["summary"], oldest)   # your LLM call
        mem["recent_turns"] = mem["recent_turns"][2:]
    store.put(user_id, mem)  # write-through, at turn commit
```

## Pitfalls

- Keying memory on a channel address instead of a canonical identity fragments the same user across SMS/WhatsApp/chat. Resolve to one `user_id` first.
- Lazy (end-of-session) writes lose the last turn on crash. Write through at each turn.
- Unbounded `recent_turns` silently blows the context window; summarize on a token threshold, not a fixed message count.
- Mixing summary text and RAG citations in one block causes mis-attributed answers. Keep them separate.
- Persisting OTPs, PANs, or auth tokens into long-lived memory is a compliance breach. Redact before write.
- Trusting AI Assistant Sessions for cross-channel continuity — Sessions are session-scoped; cross-channel needs your own store.

## Output format

Return a memory record as JSON: `{ "user_id", "bindings": [{channel, address|identity}], "summary", "recent_turns": [{role, text, ts}], "facts": {}, "updated_at", "ttl" }`. On retrieval, emit the assembled context block(s) plus the resolved `user_id`. On erasure, return `{ "user_id", "deleted": true }`.

## Reference

- AI Assistants base: `https://assistants.twilio.com/v1`. Assistant Sessions provide per-conversation short-horizon state; they are not a cross-channel long-term store.
- Conversations identity handles (from the Conversations API, `https://conversations.twilio.com/v1`): chat participants carry `Identity`; SMS/WhatsApp participants bind via `MessagingBinding.Address` (+E164 or `whatsapp:<E164>`) and `MessagingBinding.ProxyAddress` (your Twilio number). These are the stable keys you map to a canonical `user_id`.
- Message body hard limit is 32KB per Conversations message; summaries and injected context must fit whatever the downstream model context window allows, independent of that transport limit.
- Media is stored via Twilio's Media Content Service (MCS); persist media SIDs/URLs in memory rather than re-embedding binaries.
- Retention/privacy: honor GDPR/CCPA erasure by hard-deleting the keyed record and any derived summaries; enforce a TTL so stale PII expires. Never store OTPs or payment data in memory.
