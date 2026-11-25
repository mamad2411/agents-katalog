---
name: research-domain
description: Learn about the company's products, market, competitors, and industry trends — via web research and user interview — and write durable briefings into the knowledge base so the whole team makes informed decisions. Use for benchmarks, trend briefings, competitor moves, or onboarding new product context.
---

# Research Domain — Product & Industry Learning

Owner: `bi-analyst` (research mode). Args scope the topic, e.g. `/research-domain churn benchmarks for B2B SaaS` or `/research-domain what changed in our industry this quarter`.

## Procedure

1. **Define the research question and its use.** Typical modes:
   - **Benchmarks:** industry-standard values for metrics (feeds `/define-kpis` targets)
   - **Trend briefing:** what's changing in {{INDUSTRY}} that affects our priorities
   - **Competitor scan:** notable competitor moves and what to watch in our data because of them
   - **Product onboarding:** internal — learn a product/feature so analyses use correct concepts

2. **Gather.**
   - *External:* web search and source fetching. Prefer primary and reputable sources (industry reports, regulator/statistical agencies, vendor benchmark studies, earnings/press releases). Note publication dates; discard stale numbers. Triangulate any figure you'll rely on across ≥2 independent sources, and record the spread when they disagree.
   - *Internal:* read product docs/repos if available ({{INTERNAL_DOC_SOURCES or "ask the user"}}); interview the user with batched, specific questions for tribal knowledge.

3. **Connect to our data.** The output must be usable by the team: for each finding, note the implication — "industry median churn is X% → our Y% is bottom-quartile; recommend target Z", "competitor launched a free tier → watch our signup mix and downgrade rate", "new regulation → metric M needs segment exclusion".

4. **Write the briefing** to `knowledge/industry-notes.md` (append, dated, newest first): topic, key findings with sources and dates, implications for our metrics/priorities, recommended actions or watches. Keep each briefing tight — a page, not a thesis.

5. **Propagate.**
   - Benchmark numbers → `metrics-steward` for the catalog's target/benchmark fields.
   - New jargon/product concepts → glossary in `knowledge/business-context.md`.
   - "Things to watch" → `performance-monitor`'s scan list (note in the catalog or scorecard config).
   - Anything decision-grade → tell the user directly in the summary, don't just file it.

6. **Cadence.** Suggested standing run: {{RESEARCH_CADENCE e.g. "monthly trend briefing + ad hoc"}}. Mark each briefing with a review-by date so stale intelligence is re-verified before reuse.

---

> Created by Colin Beck — https://www.linkedin.com/in/beckcolin/
