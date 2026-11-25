---
name: web-research-brief
version: "1.0"
description: Structured web research from chat — multi-source search, fetch and cross-check, then a compact cited brief (背景 / 关键发现 / 分歧与不确定性 / 来源列表). Uses discovery-first search service resolution plus web_fetch; long reports land as a Lark doc. Use for "帮我调研X / 对比A和B / 这个说法靠谱吗 / 最近关于Y有什么新进展".
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - research
    - web
    - citations
    - brief
---

# Web Research Brief

Use this when someone wants researched answers, not a single-link reply: technology comparisons,
claim verification, market/landscape scans, "最新进展" roundups.

**You (the agent) run the research yourself.** Every claim in the brief must carry a source you
actually fetched. If sources disagree, show the disagreement — do not average it away. Never pad
with prior knowledge stated as if sourced; mark unsourced background explicitly as 背景常识.

## How to run it

1. **Scope.** Restate the question in one line + 2-4 sub-questions. Time-sensitive topics get an
   explicit recency requirement (prefer sources from the last 12 months; date every source).

2. **Resolve a search capability, discovery-first.** Use `web_search` if visible. Otherwise list
   connected services with `nyxid_services` and pick a search/enrichment service by its
   endpoint/label semantics (do NOT hardcode slugs), calling it via `nyxid_proxy`. If no search
   service exists, say so, suggest `nyxid-service-doctor`, and continue with direct `web_fetch` on
   URLs you can justify (official docs, known primary sources).

3. **Search wide, fetch deep.** 2-4 queries (different phrasings/angles), then `web_fetch` the 3-6
   most load-bearing results — prefer primary sources (official docs, papers, release notes,
   filings) over aggregators. For each: capture title, publisher, date, and the 1-3 facts you take
   from it.

4. **Cross-check.** Any number, ranking, or strong claim needs 2 independent sources or an explicit
   `[单一来源]` mark. Note conflicts as `来源分歧: A说X(date), B说Y(date)` and prefer the newer
   primary source.

5. **Compose the brief:**
   - **一句话结论**
   - **关键发现** — 3-7 bullets, each ending with `[n]` source refs
   - **分歧与不确定性** — what is contested or thinly sourced
   - **来源** — numbered list: title — publisher, date, URL
   Keep it under ~40 lines in chat; if it must run longer, create a Lark doc with
   `lark_docx_create`, send the link, and keep a 5-line summary in chat.

6. **Offer continuity.** For recurring topics offer a `scheduled_agent_creator` watch (cron + this
   skill + the standing question).

## Guardrails

- Cite or mark: no naked claims. Quote numbers exactly as the source states them, with units.
- Respect recency: never present an undated or old page as current state; always print dates.
- Read-only on the web; deliver only into the current chat (plus the doc link if created).
- Never ask the user for tokens — your NyxID-brokered tools handle all credentials.
