---
name: card-compare
description: Return a side-by-side comparison of two major-US credit cards across fees, earning rates, credits, transfer partners, and key benefits. Use when the user is deciding between two cards.
argument-hint: "[card A] vs [card B]"
disable-model-invocation: true
allowed-tools: Read, Bash(curl -sS *)
---

# Card Compare

## Goal

Return a compact side-by-side comparison of two exact card variants.

## Search Strategy: search-required

Fetch both issuer pages in parallel + up to 5 secondary sources total for current offer details. Prefer NerdWallet, The Points Guy, Doctor of Credit, One Mile at a Time, and Bankrate.

## Workflow

1. Parse two card names from the input (separated by "vs", "versus", "or", or a comma).
2. Resolve each card using [../card-identity/SKILL.md](../card-identity/SKILL.md). If either is ambiguous, return a numbered choice list for the ambiguous card and stop.
3. Run one Brave Search API call (see `search_method` in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml)):
   ```
   curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD_A+vs+CARD_B+compare&count=10" -H "X-Subscription-Token: $BRAVE_API_KEY"
   ```
   If `$BRAVE_API_KEY` is not set, fall back to WebSearch.
4. **Fetch pages** — pick the issuer URL for each card and up to 2 secondary URLs (prefer nerdwallet.com and thepointsguy.com) from the search results. Fetch in parallel:
   ```
   curl -sS -L "URL" | sed 's/<[^>]*>//g' | tr -s '\n' | head -200
   ```
   Search snippets are too shallow for accurate comparisons — the actual pages have complete rate tables, credit lists, and benefit details.
5. Apply confidence handling from [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md).
5. Return compact markdown using the `card-compare` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
6. YAML is internal only — do not include it in user-facing output.
7. Do not show a "Why It Matters" section.

## Required Sections

- `## 💰 Fees`
- `## 📈 Earning Rates`
- `## 🏷️ Credits`
- `## 🔄 Transfer Partners`
- `## ✈️ Key Benefits`
- `## 🏆 Bottom Line`
- `## 📋 Confidence Notes`
- `## 🔗 Sources` — numbered list of URLs fetched, as markdown hyperlinks with short "Site - Topic" labels, e.g. `[NerdWallet - CSR vs Amex Gold](https://...)`

Omit `## Card Identity` when both matches are confident. Use a two-column format (Card A | Card B) for the comparison sections. The Bottom Line section should give a concise factual summary of which card wins in each major dimension — not a recommendation.
