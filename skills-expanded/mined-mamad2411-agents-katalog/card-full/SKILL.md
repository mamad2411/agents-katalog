---
name: card-full
description: Return a compact full report for one major-US credit card, covering fees, offer, earnings, redemption, credits, travel benefits, protections, mechanics, eligibility, and strategy. Use when the user wants the whole card picture.
argument-hint: [card name]
disable-model-invocation: true
allowed-tools: Read, Bash(curl -sS *)
---

# Card Full

## Goal

Return a compact, complete card framework for one exact card variant.

## Search Strategy: search-required

Fetch the issuer page first, then up to 5 secondary sources for current SUB/offer details. Prefer NerdWallet, The Points Guy, Doctor of Credit, Bankrate, and One Mile at a Time. Run searches in parallel.

## Workflow

1. Resolve the card using [../card-identity/SKILL.md](../card-identity/SKILL.md). If ambiguous, return a numbered choice list and stop.
2. Run one Brave Search API call (see `search_method` in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml)):
   ```
   curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD+NAME+review+benefits+welcome+offer&count=20" -H "X-Subscription-Token: $BRAVE_API_KEY"
   ```
   If `$BRAVE_API_KEY` is not set, fall back to WebSearch. Stop early if the contract is satisfied.
3. **Fetch pages** — pick the top issuer URL and up to 2 secondary URLs (prefer thepointsguy.com and nerdwallet.com) from the search results. Fetch in parallel:
   ```
   curl -sS -L "URL" | sed 's/<[^>]*>//g' | tr -s '\n' | head -200
   ```
   Search snippets are too shallow for full reports — the actual pages have complete credit lists, rate tables, and benefit details.
4. **Best public offer search** — run in parallel with steps 2–3. Search for `CARD NAME best public offer` or `CARD NAME elevated offer` to find any currently available elevated offers (via CardMatch, incognito, referral links, specific application URLs). Include the best available public offer in the Welcome Offer section, even if it matches the standard offer.
5. **Historical offers search** — run in parallel with steps 2–3. Search for `CARD NAME historical welcome offers` or `CARD NAME past bonus offers`. If results are found, include a compact table of notable past offers with approximate date ranges and amounts.
6. Follow section composition rules from [../card-shared/section-definitions.md](../card-shared/section-definitions.md).
7. Apply confidence handling from [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md).
8. Return compact markdown using the `card-full` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
9. YAML is internal only — do not include it in user-facing output.
10. Do not show a "Why It Matters" section.

## Required Sections

- `## 💰 Fees`
- `## 🎁 Welcome Offer` — includes current public offer, best available public offer (if elevated), and a historical offers table with dates
- `## 📈 Earning Rates`
- `## 🔄 Redemption`
- `## 🏷️ Credits`
- `## ✈️ Travel Benefits`
- `## 🛡️ Protections`
- `## ⚙️ Account Mechanics`
- `## ✅ Eligibility`
- `## 🧭 Strategy`
- `## 👤 Who Is This Card For?` — describe the ideal cardholder profile, who benefits most, and who should look elsewhere
- `## 🃏 Similar Cards` — 4-6 competing cards with annual fee and a one-line summary of why each is comparable
- `## 📋 Confidence Notes`
- `## 🔗 Sources` — numbered list of URLs fetched, as markdown hyperlinks with short "Site - Topic" labels, e.g. `[Chase - Sapphire Preferred](https://...)`

Omit `## Card Identity` when the match is confident. Each section should contain condensed facts in numbered lists where appropriate.

The `## 🏷️ Credits` section includes only statement credits, cash-back rebates, and complimentary subscriptions with concrete dollar values. It does NOT include enhanced earning rates (e.g., "5x on Lyft"), bonus point multipliers, or anniversary point bonuses — those belong in `## 📈 Earning Rates`.
