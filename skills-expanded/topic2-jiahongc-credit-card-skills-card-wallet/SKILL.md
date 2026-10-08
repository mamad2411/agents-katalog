---
name: card-wallet
description: Audit a multi-card wallet for overlap, gaps, and total annual cost. Given a list of cards the user holds, identifies redundant benefits, uncovered spend categories, and net fee burden. Use when the user wants to evaluate their full card lineup.
argument-hint: "[card1], [card2], ..."
disable-model-invocation: true
allowed-tools: Read, Bash(curl -sS *)
---

# Card Wallet

## Goal

Return a compact wallet audit for a set of cards the user holds.

## Input Format

The user provides a comma-separated list of card names:

- `/card-wallet Chase Sapphire Preferred, Amex Gold, Citi Double Cash`

## Search Strategy: knowledge-first

Use training knowledge plus one issuer page fetch per card. Do NOT search secondary sources. Do NOT spawn a subagent — answer directly.

## Workflow

1. Parse the card list from the input (comma-separated).
2. Resolve each card using [../card-identity/SKILL.md](../card-identity/SKILL.md). If any card is ambiguous, return a numbered choice list for that card and stop.
3. For each card, run one Brave Search API call (see `search_method` in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml)):
   ```
   curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD+NAME+benefits+credits&count=10" -H "X-Subscription-Token: $BRAVE_API_KEY"
   ```
   If `$BRAVE_API_KEY` is not set, fall back to WebSearch. Run all calls in parallel. Supplement with training knowledge.
4. **Fetch pages** — for each card, fetch the top issuer URL from search results. Optionally fetch 1 secondary URL (prefer thepointsguy.com) for cross-checking:
   ```
   curl -sS -L "URL" | sed 's/<[^>]*>//g' | tr -s '\n' | head -200
   ```
   Run fetches in parallel. Search snippets alone miss detailed credit and rate info.
5. For each card, collect: annual fee, top earning categories, statement credits, and key benefits.
5. Identify: overlapping earning categories (where two cards cover the same spend at different rates), uncovered spend categories (common categories not covered at a bonus rate by any card), redundant benefits (same benefit on multiple cards), and total annual fee burden.
6. Apply confidence handling from [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md).
7. Return compact markdown using the `card-wallet` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
8. YAML is internal only — do not include it in user-facing output.
9. Do not show a "Why It Matters" section.

## Required Sections

- `## 💰 Annual Cost`
- `## 📈 Earning Map`
- `## 🏷️ Credits Stack` — statement credits and complimentary subscriptions only; not enhanced earn rates or point multipliers
- `## 🔁 Overlap`
- `## 🕳️ Gaps`
- `## 📋 Confidence Notes`
- `## 🔗 Sources` — numbered list of URLs fetched, as markdown hyperlinks with short "Site - Topic" labels, e.g. `[Chase - Sapphire Preferred](https://...)`

Omit `## Card Identity` when all matches are confident. The Earning Map should show the best card for each major spend category. Overlap and Gaps should be concise numbered lists.
