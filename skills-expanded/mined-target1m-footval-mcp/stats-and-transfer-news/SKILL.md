---
name: stats-and-transfer-news
description: Season statistics leaderboards and transfer news from FootVal — top scorers, assist leaders, goals plus assists, minutes and appearances for a league, a European or domestic cup, national-team competitions or all competitions combined, and the latest confirmed transfers and rumours with fees and reliability. Use for "who is the Champions League top scorer", "most assists in La Liga last season", "latest Galatasaray transfer news", "has X signed?".
---

# Leaderboards and the transfer wire

Full argument list:
[`../value-and-compare-players/references/tools.md`](../value-and-compare-players/references/tools.md).

## Leaderboards (`get_stat_leaders`)

- `metric`: `goals` (default), `assists`, `contributions` (goals + assists), `minutes`,
  `appearances`.
- `competition`: a code or name — leagues (`GB1`, `ES1`, `IT1`, `L1`, `FR1`, `TR1`…), cups
  (`UCL`, `UEL`, `UECL`, `FAC`…), `NT` for all national-team competitions together, or `all`
  (the default) for every competition combined. A player who moved mid-season counts once.
- `season` is the start year (2025 = 2025/26). Without it you get the latest season with data —
  say which season your answer covers.
- Leaderboards include players outside the leagues FootVal values; such a player simply has no
  valuation to show.

## Transfer news (`get_transfer_news`)

- Narrow with `query` (a player or club name) and `type`: `confirmed`, `rumors` or `all`.
- Every item carries a **reliability**. Report a rumour as a rumour ("reported", "linked with"),
  never as a done deal; only `confirmed` items are completed transfers.
- Fees are as reported. Undisclosed fees and loans stay undisclosed — don't fill the gap with a
  guess.
- The feed covers recent items. If nothing matches, say FootVal has no recent item, not that no
  transfer happened.

After a reported fee, `get_player` shows whether FootVal thinks the price is fair — see the
`value-and-compare-players` skill.
