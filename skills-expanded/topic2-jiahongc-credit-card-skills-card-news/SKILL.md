---
name: card-news
description: Return material news about one major-US credit card from the last 3 months, including direct card changes, relevant issuer updates, and major approved-site coverage. Use when the user wants the latest card-specific developments.
argument-hint: [card name]
disable-model-invocation: true
allowed-tools: Read, Bash(curl -sS *)
---

# Card News

## Goal

Return the last-3-month news view of one exact card variant in compact format.

## Search Strategy: search-required

Fetch issuer newsroom + up to 5 secondary sources for recent coverage. Prefer Doctor of Credit, The Points Guy, One Mile at a Time, NerdWallet, and Bankrate. Run all searches in parallel.

## Workflow

1. Resolve the card using [../card-identity/SKILL.md](../card-identity/SKILL.md). If ambiguous, return a numbered choice list and stop.
2. Apply the 3-month lookback and inclusion rules from [../card-shared/recency-rules.md](../card-shared/recency-rules.md).
3. Run one Brave Search API call (see `search_method` in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml)):
   ```
   curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD+NAME+news+changes+CURRENT_YEAR&count=10&freshness=p3m" -H "X-Subscription-Token: $BRAVE_API_KEY"
   ```
   The `freshness=p3m` parameter limits results to the past 3 months, matching the lookback window. If `$BRAVE_API_KEY` is not set, fall back to WebSearch.
4. **Fetch pages** — pick up to 2 top article URLs (prefer doctorofcredit.com and thepointsguy.com) from the search results. Fetch in parallel:
   ```
   curl -sS -L "URL" | sed 's/<[^>]*>//g' | tr -s '\n' | head -200
   ```
   News snippets often lack dates and detail — the full article has the complete story and timeline.
5. Follow [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md).
5. Return compact markdown using the `card-news` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
6. YAML is internal only — do not include it in user-facing output.
7. Do not show a "Why It Matters" section.

## Required Sections

- `## 📅 News Window`
- `## 📰 Recent Updates`
- `## 📝 Summary`
- `## 📋 Confidence Notes`
- `## 🔗 Sources` — numbered list of URLs fetched, as markdown hyperlinks with short "Site - Topic" labels, e.g. `[Doctor of Credit - Amex Gold Changes](https://...)`

Omit `## Card Identity` when the match is confident. Use a numbered list for recent updates with a short summary line per item.
