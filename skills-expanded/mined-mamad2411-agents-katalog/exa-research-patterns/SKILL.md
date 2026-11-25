---
name: exa-research-patterns
description: Research workflows on Exa - layered search plans, domain and date filtering, company deep dives, citation-safe highlights, and when to use deep types or Websets. Use when the user asks for research, competitive analysis, or a standing watchlist.
---

# Exa Research Patterns

## Layer the search, do not one-shot it

1. **Scout** with `type: "fast"`, `numResults` 10 to 25, no contents:
   cheap map of who covers the topic.
2. **Filter** the second pass with what you learned: `category`,
   `includeDomains`, `startPublishedDate`.
3. **Harvest** contents only for the survivors: `highlights` +
   `summary`, `text` capped with `maxCharacters` for the few pages you
   will quote.
4. **Synthesize** yourself, or hand one `deep` / `deep-reasoning` query
   the refined question when multi-source synthesis is worth the latency.

This costs a fraction of requesting `text: true` on 100 results up front.

## Freshness and scope control

- News-shaped questions: `category: "news"` +
  `startPublishedDate` in the last 7 to 30 days.
- Evergreen technical questions: drop date filters entirely; the best
  explanation is often years old.
- Trust tiers via domains: run one pass with
  `includeDomains` pinned to primary sources (official docs, .gov, .edu,
  vendor blogs) and a second unrestricted pass; disagreements between the
  two are your open questions.
- `excludeDomains` for SEO farms that keep polluting a topic.

## Company research recipe

1. `category: "company"`, query describing the company: homepage and
   profile pages surface first.
2. `category: "news"` + date window + company name: funding, launches,
   incidents.
3. `category: "financial report"` for public companies.
4. `includeDomains: ["linkedin.com"]` or `category: "people"` for team and
   hiring signals.
5. Competitor sweep: query "companies similar to {X} that {do Y}" with
   `type: "auto"`; neural retrieval is strong at this analogy shape.

Pull `highlights` for every claim you keep so each fact carries its source
URL.

## Citation discipline

- Quote from `highlights` (relevance-scored, tied to `url`), not from
  `summary` (generated text, may compress away nuance).
- Keep `publishedDate` next to each cited fact; stale citations are the
  top research failure mode.
- If two sources conflict, prefer the one whose `url` is the primary
  source, then the more recent `publishedDate`.

## Standing research: Websets

When the ask is a living list, not an answer, move to Websets
(`/websets/v0`): natural language search defines the target set, Exa
verifies each candidate against your criteria, `enrichments` extract typed
fields (text, number, date, boolean) per row, `monitors` keep the set
updated on a schedule, webhooks notify downstream systems. Typical uses:
prospect lists, competitor trackers, grant or paper watchlists.

## Cost and latency budgeting

- Tight agent loops: `fast` or `instant`, small `numResults`, `highlights`
  only.
- One-off human-facing reports: `auto` passes plus a final `deep` query.
- Never place `deep-reasoning` inside a retry loop; it is the most
  expensive and slowest type. Check `costDollars` on responses while
  tuning.
