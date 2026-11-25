---
name: worldcup-match-report
description: Generate source-backed Chinese PDF reports for World Cup or international football match previews, combining viewing guide, mobile-friendly squads, tactical lineups, referee and environment effects, odds, score modeling, risks, and a concentrated fixed-budget lottery plan. Use when the user asks in Chinese or English for “输出xx vs xx分析”, “xx 对 xx 赛前分析”, “世界杯观赛与购彩报告”, or wants a phone-readable match analysis PDF.
---

# World Cup Match Report

## Purpose

Produce a polished, phone-readable Chinese PDF report for one football match. The report must connect verified match evidence to score-range analysis and a concentrated, high-variance fixed-budget lottery plan. Keep user-facing copy formal, clear, neutral, and explicit about uncertainty.

## Resources

- Read `references/report-spec.md` before generating or revising a report.
- Read `references/betting-model.md` before producing score analysis or a lottery plan.
- Use `assets/known-good-brazil-vs-morocco-2026-06-14.html` only as a legacy visual-density reference. Do not copy its match facts or section order.
- Use `assets/reference-mobile-roster-*.png` as the required visual direction for parallel team rosters and the vertical combined pitch.
- Use `scripts/render_pdf.py` to render the final PDF from a temporary print-ready HTML file.

## Workflow

1. Parse the requested match, date, competition, and user budget. If the date is missing, search current fixtures and state the inferred date; ask only if multiple plausible matches remain.
2. Collect live evidence. Browse official or primary sources first, then reputable secondary sources. Verify current squads, injuries, odds, ranking, venue, exchange rate, coach, lottery rules, assigned referee, tournament-to-date referee statistics, venue surface or roof, weather, local kickoff conditions, travel, and rest.
3. Build a source ledger while researching. Track what each source proves, the retrieval date, and whether the information is verified, unavailable, or inference.
4. Prepare the match data model: teams, staff, full squad, player photos, Chinese names, aliases, club names in Chinese, market values in RMB, predicted starters, tactics, odds, probability estimates, referee profile, tournament officiating baseline, environment, score-impact adjustments, risks, and the default 100 RMB plan unless the user gives another budget.
5. Establish an odds-derived baseline, then explicitly adjust the expected score range using referee and environment evidence. Keep verified observations separate from inferred effects.
6. Create a concentrated plan with no more than three selections. Prefer one core path plus one or two high-payout score or handicap paths; do not spread the budget across every available play.
7. Generate a temporary print-ready HTML file, then render the final PDF under `output/worldcup-betting-assistant/` using a clear slug such as `argentina-vs-algeria-2026-06-17.pdf`. The PDF is the deliverable; do not deliver HTML unless the user explicitly asks for it.
8. Render the PDF to PNG pages and inspect it. Check page order, text size, line breaks, roster columns, player photos, combined pitch, betting plan prominence, source readability, absence of clipped or blank content, and clear vertical separation between every player name, age/value line, and extended-details line.

## Evidence Rules

- Use current web verification by default. Do not rely on memory for current squads, odds, fixture time, injuries, coaches, market values, exchange rates, or lottery availability.
- Prefer FIFA, ESPN, official team or federation pages, Transfermarkt, TheSportsDB, RotoWire, Opta-style previews, established news outlets, and the Chinese Sports Lottery website where reachable.
- Use tournament-to-date officiating statistics only when the completed-match sample and retrieval cutoff are stated. Treat small samples as context, not proof.
- Verify the assigned referee from an official source when possible. If only reputable reporting is available, label the assignment `待官方复核`.
- For weather, state the forecast provider, stadium coordinates or city, local kickoff time, and retrieval date. Forecast impact is always inference.
- If China Sports Lottery fixed odds or endpoints cannot be verified, say so in the report and base betting analysis on verified overseas odds plus explicit caveats.
- Mark conclusions as one of: `已核验`, `未核验`, or `推断`. Predictions for starters, tactics, score, and betting allocation are always `推断` unless an official lineup has been published.
- Include a source list with direct links. Do not include unsourced trivia, rumors, or player attributes.

## Report Contract

The report must include:

- Hero with competition, match title, local time, venue, concise disclaimer, and a full-width responsive team comparison strip.
- Notice with report update date, exchange rate basis, and lottery verification status.
- One-page conclusion cards with tags for verified facts and inferred recommendations.
- A concentrated lottery decision section near the front of the report, including the score thesis, referee and environment adjustments, selected plays, budget, payout thresholds, and cancellation conditions.
- Referee and match-environment analysis: assigned referee, tournament-to-date fouls/cards/penalties/red cards, venue, surface or roof, weather, kickoff conditions, travel/rest, and explicit score impact.
- Event background: format, group context, match importance, time and venue.
- Team overview: history, head-to-head, notable stories, ranking, value, style, and risks.
- Full rosters in two parallel team columns, grouped by head coach, forwards, midfielders, defenders, and goalkeepers. Every player must show a real avatar, Chinese name, age, RMB market value, shirt number, position, height, weight, and Chinese club name in compact rows; do not move required details into a separate dense table.
- Predicted starters on one vertical combined green pitch, with the two teams facing each other from opposite halves. Place substitute groups after the pitch.
- Tactical prediction table connecting football observations to betting implications.
- Odds and probabilities, including plain-language rules for moneyline, handicap, and totals when those appear.
- Risk section and source list.

## PDF Standards

- Use a standalone print-ready HTML file only as an intermediate artifact.
- Deliver a portrait PDF optimized for phone reading. Prefer A5 portrait or another narrow portrait page size with readable body text and limited horizontal tables.
- Preserve the “World Cup match command center” feel: stadium-green background, gold accent, scoreboard-like metric cards, tactical-board pitch, compact data tables, and NBA-style player cards.
- Avoid generic landing-page layout. The first screen should be the report itself, not marketing copy.
- Put the lottery decision within the first three PDF pages.
- Use the reference screenshot roster style: two pale team panels, position-group headings, compact circular or cutout avatars, bold Chinese names, and muted age/value text.
- Use one vertical combined pitch for the two predicted lineups. Do not place two small pitches side by side.
- Avoid dense desktop tables for the roster and betting plan. Use stacked cards and parallel columns.
- Do not show a “常用叫法” field when the value is empty.
- All money values must be RMB. If a source gives EUR, USD, or GBP, convert and state the exchange-rate source/date.

## Betting Guardrails

- Treat the report as entertainment-oriented analysis, not investment advice or a guaranteed-return promise.
- Do not recommend exceeding the stated budget.
- Default to a concentrated high-variance plan with one to three selections. State clearly that concentration increases the probability of losing the entire budget.
- Do not add low-payout favorites or hedges merely to make the plan look balanced. Recommend `不购买` when prices do not justify the modeled path.
- Attach a minimum acceptable fixed-bonus or odds threshold and clear cancellation conditions to every recommended selection.
- Do not claim positive expected value unless odds, probability, and vig removal are explicitly calculated and sources support the inputs.
- If using overseas odds for probability and Chinese lottery for execution, state that payout rules and fixed bonuses differ.

## Final Response

After creating or revising a report, give the PDF path, summarize the key evidence and checks, and mention any unavailable data. Keep the final user response short.
