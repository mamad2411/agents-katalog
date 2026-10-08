---
name: card-profile-recommend
description: >
  Analyze a multi-card portfolio and return graded card assessments plus
  2–3 concrete new-card recommendations with signup bonus strategy.
  Applies issuer application rules (Chase 5/24, Amex lifetime bonus,
  Amex 5-card limit, Citi 8/65 and 48-month, Capital One 2-card limit).
  Use when the user wants to know which cards to keep, drop, or add next.
argument-hint: "[card1], [card2], ..."
user-invocable: true
triggers:
  - card-profile-recommend
  - recommend cards
  - what cards should i add
  - credit card recommendations
  - optimize my wallet
  - what card should i get next
  - improve my card lineup
disable-model-invocation: true
allowed-tools: Read, Bash(curl -sS *)
---

# Card Profile Recommend

<!-- SKILL BOUNDARY — not user-facing
  /card-wallet    → audits what you have (overlaps, earning map, gaps). No grades, no recommendations, no issuer rules.
  /card-profile-recommend → grades each card (MVP / Keep / Consider Dropping), recommends 2–3 new additions,
                             applies issuer rules, and sequences applications to maximize signup bonuses.
  Use /card-wallet to understand your portfolio; use /card-profile-recommend to decide what to do about it.
-->

## Goal

Return a graded portfolio audit plus opinionated new-card recommendations with signup bonus strategy and issuer rule checks.

## Input Format

The user provides a comma-separated list of cards they currently hold:

- `/card-profile-recommend Chase Sapphire Preferred, Amex Gold, Citi Double Cash`

### Optional: opening dates

The user may provide opening dates per card. Dates can appear inline after
each card name (parenthesized) or as a separate list:

- `/card-profile-recommend CSP (Jan 2024), Amex Gold (Mar 2023), Double Cash (2021)`
- `/card-profile-recommend CSP, Amex Gold, Double Cash — opened: CSP Jan 2024, Gold Mar 2023, Double Cash 2021`

When opening dates are provided:
- **Calculate exact 5/24 count** — count how many of the listed cards (plus
  any cards the user notes as opened and since closed) were opened within
  the 24 months before today's date. Set `chase_524_status` to `clear`
  (count < 5), `blocked` (count ≥ 5), or `tight` (count = 4).
- **Factor dates into Consider Dropping decisions** — if a card was opened
  recently (< 12 months ago), closing it wastes the 5/24 slot it consumed
  (the slot counts against 5/24 whether the card is open or closed). Note
  this in the Consider Dropping rationale: "Opened [date] — closing now
  still counts against 5/24 until [date + 24 months]. Keep until it falls
  off or until the card justifies the slot."
- **Factor dates into Keep decisions** — a card opened > 20 months ago is
  about to fall off 5/24. If it's a Consider Dropping candidate, note the
  upcoming 5/24 relief: "Falls off 5/24 in [month/year] — consider
  waiting to close until after it drops to avoid wasting the slot."

When opening dates are NOT provided, set `chase_524_status: unknown` and
note: "Provide opening dates or check your 5/24 count via a free credit
report before applying for Chase cards."

## Search Strategy: search-required

Per card: issuer page + 1 secondary (parallel). Additional parallel search for new-card candidates. Up to 5 secondary sources total across the full run. Preferred secondaries: NerdWallet, The Points Guy, Doctor of Credit, One Mile at a Time, Upgraded Points. See [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml).

## Workflow

1. **Parse and resolve** — parse the card list (comma-separated). Resolve each card via [../card-identity/SKILL.md](../card-identity/SKILL.md). If any card is ambiguous, return a numbered choice list for that card and stop. Do not proceed until all cards are resolved.

2. **Research existing cards (parallel)** — for each card, run one Brave Search API call in parallel (see `search_method` in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml)):
   ```
   curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD+NAME+benefits+credits+annual+fee&count=10" \
     -H "X-Subscription-Token: $BRAVE_API_KEY"
   ```
   If `$BRAVE_API_KEY` is not set, fall back to WebSearch. Then fetch in parallel: the top issuer URL + 1 secondary per card (prefer thepointsguy.com):
   ```
   curl -sS -L "URL" | sed 's/<[^>]*>//g' | tr -s '\n' | head -200
   ```
   Per card, collect: annual fee, statement credits (amounts and redemption conditions), earning categories with rates, welcome offer status (eligible / lifetime_used / family_rule / unknown), and notable benefits (lounge access, hotel status, travel insurance).

3. **Research new-card candidates (parallel with step 2)** — run a parallel search targeting portfolio gap categories (anticipate gaps from training knowledge before full gap analysis):
   ```
   curl -sS "https://api.search.brave.com/res/v1/web/search?q=best+credit+card+CATEGORY+welcome+bonus+current+offer&count=10" \
     -H "X-Subscription-Token: $BRAVE_API_KEY"
   ```
   Fetch up to 2 secondary pages total (prefer nerdwallet.com and thepointsguy.com) for new-card shortlist context. Supplement with training knowledge on current best offers and historical bonus levels.

4. **Portfolio economics** — compute total gross annual fees, total claimable credits (note utilization assumptions for restricted credits such as Amex Gold dining credit), and net annual cost. Compute per-card net cost = annual fee − credits.

5. **Grade each card** — assign MVP / Keep / Consider Dropping per Grading Criteria below. One-line rationale per card.

6. **Determine point valuations** — before building the earning map, determine the **effective cents-per-point (cpp)** for each rewards currency in the wallet. Use TPG monthly valuations as the baseline (fetch from https://thepointsguy.com/loyalty-programs/monthly-valuations/ or use training knowledge of current values).

   **Transfer-access rule**: A points currency is only worth its full TPG
   valuation if the wallet contains a card that unlocks transfers or
   premium redemption for that currency. Without a transfer-enabling card,
   the points are worth **1.0¢ (cash back)**.

   | Currency | Transfer-enabling cards | Full TPG value |
   |----------|----------------------|----------------|
   | Chase UR | Sapphire Preferred, Sapphire Reserve, or any Sapphire-family card | ~2.0¢ |
   | Amex MR | Gold, Platinum, Green, or any MR-earning charge card | ~2.0¢ |
   | Capital One Miles | Venture X, Venture, Spark Miles (transfer via portal) | ~1.8¢ |
   | Citi TYP | Strata Premier, Strata Elite (NOT Custom Cash, Strata Basic, or Double Cash alone) | ~1.7¢ |
   | Bilt Points | Any Bilt card (Blue, Obsidian, Palladium — all can transfer) | ~1.8¢ |
   | World of Hyatt | Chase Hyatt card (direct earn into Hyatt program) | ~1.8¢ |
   | Marriott Bonvoy | Any Marriott co-brand (direct earn into Bonvoy program) | ~0.7¢ |
   | Atmos Rewards | Atmos Ascent or Summit (direct earn into Atmos program) | ~1.7¢ |
   | Cash back | Any cash-back card | 1.0¢ |

   If the wallet has only a Freedom card (CFU, CFF) with **no** Sapphire
   card, Chase UR points are worth 1.0¢ — not 2.0¢. Similarly, if the
   wallet has only a Citi Custom Cash or Citi Double Cash with **no**
   Strata Premier or Strata Elite, Citi TYP are worth 1.0¢.

   When a recommended new card would unlock transfers for an existing
   currency (e.g., recommending Citi Strata Premier when the user only has
   Custom Cash), note the value uplift: "Unlocks TYP transfers — existing
   Custom Cash points jump from 1.0¢ to 1.7¢."

7. **Build earning map with potential value** — for each major spend
   category, identify the best card and compute:
   `effective value per dollar = earn rate × cpp (from step 6)`
   Show the earning map as a table with columns: Category, Best Card,
   Rate, Currency, CPP, Effective Value. This lets the user see not just
   the multiplier but the actual cents-per-dollar-spent value.

8. **Identify portfolio gaps** — enumerate major spend categories not covered at a bonus rate (below 2x / 2% cash back) by any card in the wallet. Categories to check: dining, groceries, gas, travel, streaming, transit, drugstore, rent, hotel, airline, online shopping, wholesale clubs.

9. **Generate new-card recommendations** — select 2–3 new **personal** cards per Recommendation Logic below. **Do not recommend business cards** (e.g., Chase Ink, Amex Business Gold). Check all issuer application rules (see Issuer Rules section below). Exclude cards already in the wallet.

10. **Build signup bonus strategy** — order applications by priority per Signup Bonus Strategy section below. Flag timing constraints, combined spend requirement feasibility, and elevated offer windows.

11. **Apply confidence handling and assemble output** — follow [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md). Return compact markdown. YAML is internal only — do not include it in user-facing output. Do not show a "Why It Matters" section.

## Required Sections

- `## 🃏 Cards Entered` — echo back every card the user provided, numbered, with the resolved full official name (e.g., "Chase Sapphire Reserve" not "CSR") and opening date if provided. This confirms what was analyzed.
- `## 📊 Portfolio Summary` — total cards, gross annual fees, total claimable credits, net annual cost; note credit utilization assumption
- `## 🏅 Card Grades` — each card graded MVP / Keep / Consider Dropping with one-line rationale; sort MVP first, then Keep, then Consider Dropping. **Always use the full official card name** (e.g., "Chase Sapphire Reserve" not "CSR", "American Express Gold Card" not "Amex Gold").
- `## 🗺️ Earning Map` — best card per major spend category across the portfolio; table with columns: Category, Best Card, Rate, Currency, CPP, Effective Value (rate × cpp). CPP must reflect the transfer-access rule from step 6 — use 1.0¢ for currencies without a transfer-enabling card in the wallet. **Always use full official card names** in the Best Card column.
- `## 🔻 Consider Dropping` — only when one or more cards grade Consider Dropping; per card: annual fee drag, what would be lost, downgrade path if available; **omit this section entirely** when all cards grade MVP or Keep. **Unused card check**: after building the earning map, identify any cards that do not appear as the "Best Card" in any category. If a card never wins a single category in the earning map and has an annual fee, flag it here with a note: "This card does not win any category in your earning map — consider whether the benefits alone justify the fee, or downgrade/cancel."
- `## 🕳️ Portfolio Gaps` — spend categories not well covered (below 2x / 2%); numbered list
- `## ➕ Recommended Additions` — 2–3 new cards to add; per card: name, current welcome offer, annual fee, why it fits the portfolio, net first-year value estimate, issuer rule status; label each Top Pick / Strong Contender / Situational
- `## 🎯 Signup Bonus Strategy` — ordered application sequence with timing notes and spend requirement feasibility
- `## ⚖️ Issuer Rules Check` — only show rules relevant to the recommended cards; **bold** any blocking rule; omit issuers with no applicable rules
- `## 🔍 Confidence Notes`
- `## 🔗 Sources` — numbered list of all URLs fetched, as markdown hyperlinks with short "Site - Topic" labels, e.g. `[Chase - Sapphire Preferred](https://creditcards.chase.com/...)`

Omit `## Card Identity` when all card matches are confident. Never include YAML in user-facing output.

## Grading Criteria

### MVP

All of the following must be true:
- Net cost (annual fee minus fully claimable credits) is ≤ $50, OR the card provides a unique earning category (3x+ in a category no other held card matches) OR a unique high-value benefit not replicated elsewhere in the wallet (lounge access, hotel status, primary travel insurance)
- The card earns the best rate (or tied for best) in at least one major spend category
- No viable downgrade or duplicate card in the wallet renders it redundant

### Keep

One or more of the following, with no dominant reason to drop:
- Net cost is positive but the card provides a benefit or earning rate that partially justifies it
- The card holds long credit history that would materially hurt the credit score to close
- The card earns transferable points — diversification of UR, MR, TYP, Capital One Miles, or Bilt Points ecosystems
- The card is under 12 months old (welcome bonus spend may still be active)

### Consider Dropping

One or more of the following, with no dominant reason to keep:
- Net cost is negative (fees exceed realistically claimable credits) and no unique benefit justifies the drag
- All earning categories are duplicated by another card in the wallet at an equal or better rate
- Benefits are fully replicated by another card in the wallet
- A no-fee downgrade path exists that would preserve the credit line and history

**Hard rule**: Never grade Consider Dropping if the card is the sole source of a transferable-points program in the wallet (Chase UR, Amex MR, Citi TYP, Capital One Miles, Bilt Points). Always note the downgrade option before recommending a full cancel.

### 5/24 date-aware grading (when opening dates are provided)

When the user provides opening dates, factor them into grading:
- **Card opened < 12 months ago** — closing wastes the 5/24 slot (the
  account still counts against 5/24 whether open or closed for 24 months
  from open date). Bias toward Keep even if benefits overlap. Note:
  "Opened [date] — still counts against 5/24 until [date + 24 months].
  Dropping saves the fee but does not recover the 5/24 slot."
- **Card opened 12–20 months ago** — slot is mid-burn. Only grade Consider
  Dropping if the fee drag is severe and no downgrade path exists. Note
  the remaining 5/24 window.
- **Card opened > 20 months ago** — slot is about to expire from 5/24. If
  the card is a Consider Dropping candidate, note: "Falls off 5/24 in
  [month/year] — safe to close after that date without wasting the slot."
- **Card opened > 24 months ago** — no 5/24 impact. Grade purely on
  benefits and economics.

## Recommendation Logic

Select 2–3 new **personal** cards in this priority order. **Never recommend
business cards** (e.g., Chase Ink, Amex Business Gold, Capital One Spark).

1. **Fill the highest-value spend gap** — identify the category with the highest estimated annual spend earning below 2x; recommend a card earning 3x+ in that category with a strong welcome offer.

2. **Add a new transferable-points ecosystem** — if the portfolio is cash-back heavy or locked into a single ecosystem (e.g., only Chase UR), recommend a card that opens a complementary program (Amex MR, Citi TYP, etc.).

3. **Maximize the signup bonus window** — if the user has 5/24 headroom (under 4 new cards in 24 months), prioritize a Chase card for ecosystem value. If 5/24 is tight or unknown, consider Amex or Citi instead since their rules are more recoverable.

4. **Avoid worsening existing overlap** — do not recommend a card whose primary earning category is already covered at the same or better rate by an MVP card in the wallet.

5. **Prioritize elevated offers** — if the current public offer is at or near an all-time high per secondary source data, flag as "elevated offer" and note the timing signal.

6. **Diversify issuers** — do not recommend two Chase cards if 5/24 is a constraint; do not recommend an Amex if the user already holds 5 Amex credit cards.

7. **Churning value** — factor in credit card churning strategy. Consider
   cards where:
   - The welcome bonus alone exceeds the annual fee by 5x+ (high
     first-year ROI), making it worth opening even if the card is
     downgraded or cancelled after year one.
   - A no-fee downgrade path exists (e.g., Chase Sapphire Preferred →
     Freedom Flex, Citi Strata Premier → Citi Strata Basic), allowing
     the user to capture the bonus, keep the credit line, and eliminate
     the fee after the first year.
   - The card's bonus cooldown window is reasonable (e.g., Citi 48-month
     re-eligibility), making it a repeatable churn target in future
     cycles.
   - Note the churn path explicitly: "Churn path: apply → meet SUB →
     hold 12 months → downgrade to [no-fee card] → re-apply after
     [cooldown period]."
   - Do NOT recommend churning cards where cancellation would lose
     irreplaceable benefits (e.g., the user's only lounge-access card)
     or where the issuer is known to blacklist churners (e.g., Amex
     clawback risk on early cancellation).

Per recommended card, output: card name, why it fits the portfolio (1–2 sentences), current welcome offer (bonus amount, spend requirement, window), annual fee, net first-year value estimate, issuer rule status (clear / blocked / verify), priority label (Top Pick / Strong Contender / Situational), and churn path if applicable.

## Signup Bonus Strategy

Reason about the order and timing of applications. Output as a numbered list in `## 🎯 Signup Bonus Strategy`.

**Chase-first heuristic**: If 5/24 headroom exists, always recommend the Chase card first. Once 5/24 is breached, Chase cards are inaccessible for up to 2 years. Amex, Citi, and Capital One do not have an equivalent permanent gatekeeping rule and can be applied for after the Chase card.

**Amex lifetime bonus check**: Before recommending any Amex card, note whether the user is likely to have held that exact product before. If prior hold is probable, the welcome bonus is forfeit — downgrade the recommendation or suggest a different Amex product. Flag as unconfirmed in Confidence Notes when unknown.

**Spend requirement feasibility**: Check whether combined spend requirements across all recommendations are achievable simultaneously. Flag when total exceeds a reasonable 3-month budget (>$8,000 combined).

**Application spacing** — follow issuer-specific rules:
- Amex: at least 5 days between Amex applications
- Citi: at least 8 days between Citi applications; no more than 2 in 65 days
- Capital One: at least 6 months since last new account (any issuer)

**Elevated offer timing**: When a recommended card's current bonus is at or near an all-time high, note "elevated offer — apply sooner to capture it."

Output format — numbered ordered list:
```
1. [Card A] — apply first ([reason]); [timing note]
2. [Card B] — apply 3–4 weeks later ([reason]); [timing note]
3. [Card C] — apply after [condition] ([reason]); [timing note]
```

## Issuer Rules Reference

Check and apply the following rules. Only surface rules relevant to the recommended cards in `## ⚖️ Issuer Rules Check`. Bold any blocking rule.

| Issuer | Rule | Key Detail |
|---|---|---|
| Chase | 5/24 | Most Chase cards require fewer than 5 new personal credit cards opened across all issuers in the prior 24 months. Business cards generally do not count toward 5/24. When opening dates are provided, compute the exact count. |
| Chase | Same-day limit | Max 1 personal Chase card application per day. Do not recommend two Chase personal cards simultaneously. |
| Chase | Bonus cooldown | Must wait 48 months from last bonus receipt on the same Chase product to re-earn. |
| Amex | Once-per-lifetime bonus | Each Amex card's welcome bonus can only be earned once per lifetime per person. Amex surfaces a pop-up before checkout if ineligible. |
| Amex | 5-credit-card limit | May hold at most 5 Amex credit cards simultaneously. Charge cards (Platinum, Gold) do not count against this cap; co-branded Amex credit cards do. |
| Amex | 1-in-5-days rule | Cannot apply for more than 1 Amex card within a 5-day window. |
| Amex | 2-in-90-days rule | Cannot apply for more than 2 Amex cards within a 90-day window. |
| Citi | 8/65 rule | Cannot get approved for 2 Citi cards within 8 days; no more than 2 Citi cards within 65 days. |
| Citi | 48-month family rule | Cannot receive a welcome bonus if a card in the same Citi card family was opened or closed within the past 48 months. |
| Capital One | 2-card personal limit | May hold at most 2 Capital One personal credit cards simultaneously. Business cards do not count against this limit. |
| Capital One | 6-month cooling | Typically declines applicants who opened any new credit account in the last 6 months. |
| Bank of America | 2/3/4 rule | No more than 2 new BoA cards in 2 months, 3 in 12 months, 4 in 24 months (personal BoA cards). |
| Barclays | 6-month recency | Typically requires 6 months since the last new credit account (any issuer). |
| U.S. Bank | Inquiry sensitivity | Known to decline applicants with many recent hard inquiries. Recommend applying after other cards settle. |

When neither opening dates nor a 24-month count are provided, set
`chase_524_status: unknown` and note: "Provide opening dates or check your
5/24 count via a free credit report before applying for Chase cards."
