---
name: card-value
description: Estimate first-year value for one major-US credit card given an optional spending breakdown. Returns welcome bonus + estimated earn + credits minus annual fee. Use when the user wants a quick value check.
argument-hint: "[card name] [optional spend breakdown]"
disable-model-invocation: true
allowed-tools: Read, Bash(curl -sS *)
---

# Card Value

## Goal

Return a compact first-year value estimate for one exact card variant.

## Input Format

The user provides a card name followed by an optional spending breakdown:

- `/card-value Chase Sapphire Preferred` — uses a reasonable default annual spend estimate
- `/card-value Chase Sapphire Preferred $500/mo dining, $200/mo travel, $3000/mo other` — uses the provided breakdown

If no breakdown is given, use a default moderate-spender profile ($500/mo dining, $200/mo travel, $100/mo streaming, $200/mo groceries, $2000/mo other).

## Search Strategy: search-required

Fetch the issuer page + up to 5 secondary sources for current SUB details. Prefer NerdWallet, The Points Guy, Bankrate, One Mile at a Time, and Doctor of Credit. Run searches in parallel.

## Workflow

1. Resolve the card using [../card-identity/SKILL.md](../card-identity/SKILL.md). If ambiguous, return a numbered choice list and stop.
2. Run one Brave Search API call (see `search_method` in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml)):
   ```
   curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD+NAME+welcome+offer+annual+fee+value&count=10" -H "X-Subscription-Token: $BRAVE_API_KEY"
   ```
   If `$BRAVE_API_KEY` is not set, fall back to WebSearch.
3. **Fetch pages** — pick the top issuer URL and up to 2 secondary URLs (prefer nerdwallet.com and thepointsguy.com) from the search results. Fetch in parallel:
   ```
   curl -sS -L "URL" | sed 's/<[^>]*>//g' | tr -s '\n' | head -200
   ```
   Search snippets are too shallow for value calculations — the actual pages have complete credit values, earning rates, and offer details.
4. Research: annual fee, welcome offer (bonus + spend requirement), earning rates by category, and statement credits.
4. Compute: `first_year_value = welcome_bonus_value + annual_earn_value + total_credits - annual_fee`.
5. Use 1 cpp as the baseline point value unless the card has a known portal or transfer premium (note the assumed valuation in confidence notes).
6. Apply confidence handling from [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md).
7. Return compact markdown using the `card-value` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
8. YAML is internal only — do not include it in user-facing output.
9. Do not show a "Why It Matters" section.

## Required Sections

- `## 💳 Spend Profile`
- `## 🎁 Welcome Bonus`
- `## 📈 Annual Earn`
- `## 🏷️ Credits` — statement credits and complimentary subscriptions only; not enhanced earn rates or point multipliers
- `## 💰 Net First-Year Value`
- `## 📋 Confidence Notes`
- `## 🔗 Sources` — numbered list of URLs fetched, as markdown hyperlinks with short "Site - Topic" labels, e.g. `[Chase - Sapphire Preferred](https://...)`

Omit `## Card Identity` when the match is confident. The Net First-Year Value section should show the math clearly in one compact block.
