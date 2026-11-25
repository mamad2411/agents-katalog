---
name: value-and-compare-players
description: Explain what a footballer is worth with FootVal — the estimated transfer value next to the market value, whether the market under- or overvalues the player, and the factors behind the gap — and compare two to four players. Use when the user asks what a player is worth, whether a price is fair, who is better value, or why a value moved ("is Osimhen overpriced?", "Güler or Wirtz?", "what is Lamine Yamal worth?").
---

# Value a player, then explain the number

Tools: `get_player` (one profile), `compare_players` (2–4 players), and `search_football` only
when a name is ambiguous or partial — `get_player` and `compare_players` take plain names
directly. Full argument list: [`references/tools.md`](references/tools.md).

## Read the two numbers correctly

- **FootVal value** is our estimate; **market value** is the public consensus figure it is
  anchored to. The gap (`deltaPct`) is the point: positive means FootVal sees more than the market
  (the market *undervalues* the player), negative means the market *overvalues* him.
- Inside **±5 %** the verdict is **fair** — say "in line with the market", not "slightly
  undervalued".
- Values are in **euros**. Quote them the way the card does (€85M, €1.2M). Convert only when
  asked, and say that it is a conversion.
- It is an estimate, not a price tag and not a forecast of a fee — clubs pay what a negotiation
  produces. Never present it as betting or investment advice.

## Explain the gap with the factors

Each factor multiplies the value: above ×1.00 pushes it up, below pulls it down. Explain the two
or three that move most, in plain words:

- **performance** — output against price inside the player's position and league-strength
  cohort. Performing above his price lifts the value; below it, discounts it. With few minutes
  the effect is deliberately scaled down.
- **potential** — where players of the same age, position and price have historically gone
  next: young players read above their price (less so the pricier they already are), players
  past their prime below it.
- **contract** — close to expiry the selling club loses leverage (a soft Bosman discount).
- **durability** — injuries over the last two seasons.
- **reputation** — international caps and trophies; a small band.
- **form** — the latest season against the previous one, capped at ±15 %. FootVal currently runs
  with it switched off, so most breakdowns don't list it.

When a player has little or no recent data, FootVal keeps the value close to the market. Say so
instead of inventing reasons for a gap that isn't there.

## Comparing

`compare_players` puts 2–4 players on one card. Lead with the value-for-money story — value
against market, age, contract — rather than reading every row aloud. If a name can't be resolved
the tool says which; offer the `search_football` matches for that one.

## Follow-ups that work

- "Who is similar?" → the `similar` list in the `get_player` result.
- "Is he cheaper than X?" → `compare_players`.
- "Who in his league is undervalued?" → the `scout-and-rank-players` skill.
