---
name: card-credits
description: Return statement credits and cash-like credits for one major-US credit card, including trigger rules, cadence, enrollment requirements, restrictions, and practical usage notes. Use when the user wants the credits picture only.
argument-hint: [card name]
disable-model-invocation: true
allowed-tools: Read, Bash(curl -sS *)
---

# Card Credits

## Goal

Return the credits view of one exact card variant in compact format.

## What Counts as a Credit

A "credit" is a statement credit, cash-back rebate, or complimentary subscription with a concrete dollar value that directly offsets cost. Examples: "$300 travel credit," "$50 hotel credit," "complimentary DashPass membership ($120 value)."

**Not credits**: enhanced earning rates (e.g., "5x on Lyft"), bonus point multipliers, anniversary point bonuses, or any benefit that only increases points earned per dollar. Those belong in card-rate, not card-credits.

## Search Strategy: knowledge-first

Use training knowledge plus one issuer page fetch + one secondary source for credit trigger details. Do NOT spawn a subagent — answer directly.

## Workflow

1. Resolve the card using [../card-identity/SKILL.md](../card-identity/SKILL.md). If ambiguous, return a numbered choice list and stop.
2. Run one Brave Search API call (see `search_method` in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml)):
   ```
   curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD+NAME+credits+benefits&count=10" -H "X-Subscription-Token: $BRAVE_API_KEY"
   ```
   If `$BRAVE_API_KEY` is not set, fall back to WebSearch.
3. **Fetch pages** — pick the top issuer URL and top 1 secondary URL (prefer thepointsguy.com, then bankrate.com) from the search results. Fetch both in parallel:
   ```
   curl -sS -L "URL" | sed 's/<[^>]*>//g' | tr -s '\n' | head -200
   ```
   Search snippets are too shallow for credits — the full page has the complete credit list.
4. Combine the fetched page content + search snippets + training knowledge to fill all required sections.
5. Follow [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md). Flag any detail that may have changed since training data.
6. Return compact markdown using the `card-credits` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
7. YAML is internal only — do not include it in user-facing output.
8. Do not show a "Why It Matters" section.

## Required Sections

- `## 💳 Credits Overview`
- `## 🏷️ Credit Details`
- `## 📏 Usage Rules`
- `## 📋 Confidence Notes`
- `## 🔗 Sources` — numbered list of URLs fetched, as markdown hyperlinks with short "Site - Topic" labels, e.g. `[Chase - Sapphire Preferred](https://...)`

Omit `## Card Identity` when the match is confident. Use a numbered list for credits with amount, cadence, trigger, and restriction in one compact line per item.
