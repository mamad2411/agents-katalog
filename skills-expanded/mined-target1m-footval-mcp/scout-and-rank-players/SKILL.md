---
name: scout-and-rank-players
description: Scout and rank footballers with FootVal — shortlist players by league, club, national team, position, age, preferred foot and value range; list the most valuable, most undervalued or overvalued players, the biggest risers and wonderkids; and open club squads, league overviews and national-team squads. Use for scouting briefs and "who is the best / cheapest / most underrated…" questions ("left-footed centre-backs under 23 in Serie A", "most undervalued players in the Premier League", "Turkey's strongest squad").
---

# Scout, rank, and read squads

## Which tool

- A brief with attributes → `find_players`.
- A ranking question → `get_rankings` with `type`: `top_value`, `undervalued`, `overvalued`,
  `risers`, `fallers` or `wonderkids`.
- A club → `get_club`. A league overview → `get_league` (for the points table use
  `get_standings`). A nation → `get_national_team`. What is covered → `list_leagues`.

Full argument list:
[`../value-and-compare-players/references/tools.md`](../value-and-compare-players/references/tools.md).

## Turning a brief into `find_players` filters

- `league`, `club` and `nation` take names or codes ("Serie A" or `IT1`, "Turkey" or `TUR`).
- `position` is a group (`GK`, `DF`, `MF`, `FW`) or an exact role (`CB`, `LB`, `RB`, `DM`, `CM`,
  `AM`, `LM`, `RM`, `LW`, `RW`, `SS`, `ST`). "Full-back" means two calls, `LB` and `RB`; "winger"
  means `LW` and `RW`; "striker" is `ST` (or `FW` for any forward).
- Ages are inclusive: `max_age: 23` is 23 or younger. Values are euros: €30M is `30000000`.
- `sort`: `value` (default), `market_value`, `undervalued`, `overvalued`, `youngest`,
  `performance`, `rising`. "Bargains" means `undervalued`.
- `limit` is at most 25. If a filter set returns nothing, relax one constraint and say which.

## Reading rankings

- `undervalued` and `overvalued` only include players worth **€10M or more** (small values make
  percentages noisy). For cheaper players use `find_players` with `sort: "undervalued"` and a
  `max_value`, and say why.
- `risers` and `fallers` are recent moves in FootVal's own value, not in the market's.
- `wonderkids` are 21 and under.

## National teams

`get_national_team` builds the strongest 26-player squad FootVal can assemble from the players who
represent that nation (3 GK, 8 DF, 8 MF, 7 FW by value). It is **not** the official call-up —
call it "FootVal's strongest squad by value".
