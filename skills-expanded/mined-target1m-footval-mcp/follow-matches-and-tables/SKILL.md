---
name: follow-matches-and-tables
description: Live football scores, results, fixtures, match centres, league tables and FootVal's predictions — today's games, a team's next or last matches, one match's event timeline, statistics and line-ups, the current standings, the model's prediction for any match (chances, likeliest score and scorers, predicted line-ups), its 10 most confident calls of the day with their track record, and each club's title and relegation chances. Use for "what's the score", "who plays tonight", "when is Galatasaray's next game", "show me the Süper Lig table", "who will win Arsenal vs Chelsea", "predicted line-ups for the derby", "what does FootVal predict today", "who will win the league", "who goes down".
---

# Scores, matches and tables

## Which tool

- Several matches → `get_matches` with `when` = `live`, `today`, `yesterday`, `tomorrow` or a
  `YYYY-MM-DD` date, optionally narrowed by `competition` or `team`.
- One match in depth → `get_match` with a `match_id` from `get_matches` or `get_team_fixtures`.
- One team's schedule → `get_team_fixtures` (`direction`: `next` or `last`, `count` 1–10; set
  `national: true` when a national team shares its name with a club).
- A table → `get_standings` (current season by default; `season` is the start year).
- One match's prediction → `get_match_prediction` with a `match_id`, a `team` (its next match) or a
  `league` (its upcoming matches); it carries the predicted line-ups too. `get_match` also shows the
  chances for a match FootVal predicts.
- The day's 10 most confident calls and the track record → `get_predictions` (`day`: `today`,
  `yesterday` or a `YYYY-MM-DD` date; `team` keeps only that team's matches).
- Who wins the league, the top-four race, the relegation battle → `get_season_projection` (`league`).

Full argument list:
[`../value-and-compare-players/references/tools.md`](../value-and-compare-players/references/tools.md).

## Time and dates

- `when` dates are **UTC days**. A late-evening kick-off in the Americas can fall on the next UTC
  day — if a match seems missing, check the adjacent day.
- Kick-off times are UTC timestamps. Convert them to the user's time zone when you know it and
  name the zone you used.

## Live data

- A score is live at the moment of the call. Never extrapolate or invent a score, scorer or
  minute; for an update, call again.
- A match that hasn't started has no events yet, and line-ups only appear shortly before
  kick-off.
- xG and some team statistics are not available for every competition — leave them out rather
  than estimating.

## Tables

- Qualification and relegation zones come with the table, along with each team's recent form.
- Some competitions return more than one table (groups) — present the one the user asked about.

## Predictions

- FootVal's statistical model predicts every match of the leagues it values from about a day and a
  half before kick-off (`get_match_prediction`); cups, other leagues and matches further ahead have
  no prediction — say so rather than inventing one.
- Every morning before the first kick-off the model also locks in its 10 most confident calls of the
  day (match result, double chance, total goals or both teams to score) and grades each one after
  the final whistle (`get_predictions`).
- Predicted line-ups come from each side's recent starters minus the injured and suspended; the
  official ones replace them about an hour before kick-off — call it "predicted", not "confirmed",
  until then.
- Season projections are probabilities from simulating the rest of the season; ties on points are
  split by goal difference (head-to-head rules aren't modelled).
- A prediction day runs 09:00 → 09:00 UTC, so a late match can belong to the previous day's list.
- Quote the model's probability as a probability ("the model gives it 85 %"), never as a
  certainty, and give the running hit rate alongside. FootVal shows no odds and gives no betting
  advice — don't present a call as a bet.
- A call still being played carries the live score and whether it is on course; for an update,
  call again.
