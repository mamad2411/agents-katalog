---
name: card-rate
description: Return earning rates, caps, exclusions, activation requirements, and merchant-coding caveats for one major-US credit card. Use when the user wants the earn-side details only.
argument-hint: [card name]
disable-model-invocation: true
allowed-tools: Read, Bash(curl -sS *)
---

# Card Rate

## Goal

Return the earning-structure view of one exact card variant in compact format.

## Search Strategy: knowledge-first

Use training knowledge plus one issuer page fetch + one secondary source for merchant-coding caveats. Do NOT spawn a subagent — answer directly.

## Workflow

1. Resolve the card using [../card-identity/SKILL.md](../card-identity/SKILL.md). If ambiguous, return a numbered choice list and stop.
2. Run one Brave Search API call (see `search_method` in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml)):
   ```
   curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD+NAME+earning+rates+categories&count=10" -H "X-Subscription-Token: $BRAVE_API_KEY"
   ```
   If `$BRAVE_API_KEY` is not set, fall back to WebSearch.
3. **Fetch pages** — pick the top issuer URL and top 1 secondary URL (prefer bankrate.com, then thepointsguy.com) from the search results. Fetch both in parallel:
   ```
   curl -sS -L "URL" | sed 's/<[^>]*>//g' | tr -s '\n' | head -200
   ```
   Search snippets are too shallow for earning details — the full page has complete rate tables and caps.
4. Combine the fetched page content + search snippets + training knowledge to fill all required sections.
5. Follow [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md). Flag any detail that may have changed since training data.
6. Return compact markdown using the `card-rate` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
7. YAML is internal only — do not include it in user-facing output.
8. Do not show a "Why It Matters" section.

## Required Sections

- `## 📊 Rate Summary`
- `## 📈 Earning Categories`
- `## 🚫 Caps And Exclusions`
- `## 📋 Confidence Notes`
- `## 🔗 Sources`

Omit `## Card Identity` when the match is confident. Use short category lines and a compact exclusions/caps block.
