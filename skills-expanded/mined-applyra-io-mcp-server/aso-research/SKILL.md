---
name: aso-research
description: Researches and improves an app's visibility on the App Store and Google Play with Applyra's data (keyword rankings and their history, keyword difficulty and traffic, store autocomplete, niche analysis, competitors, top charts, the ASO Health audit of a listing), and scores a draft title, subtitle, short description or keywords field before it ships. Use when the user asks why their app dropped in search, which keywords to target, how they rank against a competitor, what to write in their store listing, or anything about App Store Optimization for an app tracked in Applyra.
---

# ASO research with Applyra

Applyra tracks the user's apps on the App Store and Google Play every day. Its tools read that data,
and score listing text on the same engine that audits live listings. No tool publishes anything to
App Store Connect or Google Play: the user ships changes themselves.

## Ground rules

- **Start from `list_applications`.** It gives each app's numeric `id`, which every app-scoped tool
  takes, with its store, country and language. Never guess an ID. `add_application` and
  `add_competitor` are the exceptions: they take the store bundle ID.
- **Every number comes from a tool call.** Say which tool it came from, with the store, the country
  and the date of the data. Quote difficulty and traffic as the 0-100 scores Applyra returns.
- **Rankings are per store and per country.** Keep markets apart, never blend them into one figure.
- **Let `check_metadata` count lengths.** The stores count UTF-16 code units, not characters, so a
  count done by hand is wrong in many languages.
- **Ask before changing the account.** `track_keywords`, `untrack_keyword`, `set_keyword_favorite`,
  `add_application`, `add_competitor` and `remove_competitor` change what Applyra tracks, and
  `add_note`, `update_note` and `delete_note` change the notes on its charts. Every other tool only
  reads.
- **Reuse past work first.** `list_keyword_inspections`, `list_niche_analyses`,
  `list_metadata_simulations` and `list_autocomplete_history` return what was already run.

## What moved

1. `list_keywords` for the app: current rank, the apps just ahead and behind, the top 5.
2. `get_keyword_rank_history` on the keywords that moved, with the `keyword_id` from `list_keywords`.
   It covers the last 30 days unless a range is given.
3. Report before and after, largest drops first. A move of one or two places is daily noise: lead
   with the large ones.
4. When many keywords fell on the same day, `get_app_score_history` shows whether the app's overall
   visibility fell with them. A drop across the board on one date usually comes from the store, not
   from the listing: its `events.store_updates` list the store algorithm updates of the market.

## What a change did

1. `list_notes` shows what the user noted (a campaign, a metadata change, a launch); `compare_events`
   gives the visibility before and after each note and each app update, or, with `keyword_id`, one
   keyword's rank. 7 days on each side by default, 14 or 30 for a slower effect.
2. Read each comparison with its `alongside`: another event or a store algorithm update in the same
   days is mixed into it. Say so rather than credit the change with the whole move.
3. A user who describes something they did on a given day can have it noted with `add_note`, after
   asking.

## Keywords worth targeting

1. Collect candidates: `run_autocomplete` on the app's core terms (what people type), and
   `run_niche_analysis` on its topic (clusters of keywords with an opportunity score). A fresh niche
   analysis takes a few minutes.
2. `inspect_keyword` each candidate: difficulty, traffic, KEI, the 20 apps ranking for it.
3. Prefer real traffic at a difficulty the app can win. `get_aso_health` calibrates its targeting
   verdicts on the app's size (tier 1 Emerging, 2 Growing, 3 Established): the same keyword can be
   reachable for an established app and out of reach for a new one. Say so when recommending.
4. Propose a short list. Track it with `track_keywords` (up to 20 per call) once the user agrees.

## Rewriting a listing

1. `get_aso_health` first: the score, its three axes (coverage, targeting, appeal), the flags and the
   terms the listing targets today.
2. Draft the new text, then run `check_metadata` on it. An `error` means the store would refuse it.
   Google names the words it forbids, while Apple leaves them to a reviewer, so the same draft can be
   valid on one store and refused on the other.
3. Score it with `simulate_metadata` and the app's `id`: the fields left out are read from the live
   listing, so the gain or loss against the current score is meaningful. Without an `id`, the global
   score is not comparable to a real app's: compare the coverage axis instead.
4. On iOS, the keywords field is a comma-separated list: spend it on words that are not already in
   the title or the subtitle.
5. `get_metadata_simulation` re-reads a saved draft in full, to pick up where a past run left off.

## Competitors

- `list_competitors` returns each pair: the user's app, and the competitor with its full store metadata.
- `add_competitor` with the competitor's store bundle ID, when the user names one.
- Compare positions on shared keywords with the `ahead` and `behind` apps and the top 5 that
  `list_keywords` returns.

## Market context

`list_top_chart_categories`, then `top_charts` for a store, country, category and collection (free,
paid or grossing), with each app's movement since the day before.

## Recommended by ChatGPT and Gemini

With the AI Visibility option, Applyra asks ChatGPT and Gemini the user's prompts every day in each
market and records whether the answers name the app. These tools only read; an account without the
option gets `done: false`.

1. `list_ai_visibility_apps` first: its `id` (a UUID) is the `ai_app_id` the other AI Visibility
   tools take, not the numeric `id` of `list_applications`.
2. `get_ai_visibility` for how often each engine names the app against the previous window, and
   how its competitors compare. `list_ai_answers` with `app` set to a competitor and
   `outcome=missing` returns the answers that recommend it and leave the app out.
3. `get_ai_opportunities` lists the keywords ChatGPT searched the web for. Each carries the
   `application_id` (pass it as `app_id`), `store`, `country` and `lang` that `track_keywords` takes:
   offer to track the untracked ones, and ask before doing it.

## Reading the numbers

- **Difficulty** (0-100): how hard it is to reach the top results for a keyword.
- **Traffic** (0-100): how much a keyword is searched, relative to other keywords.
- **KEI**: traffic weighed against difficulty, with a level such as "good".
- **Visibility score** (0-100): how discoverable the app is across a stable set of keywords from its
  niche, so two dates compare directly.
- **ASO Health** (0-100): how well the listing is written, as opposed to how it ranks today.
