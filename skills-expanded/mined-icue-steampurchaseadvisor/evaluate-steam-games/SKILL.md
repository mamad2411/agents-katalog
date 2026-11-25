---
name: evaluate-steam-games
description: Evaluate specified Steam games before purchase. Use when the user supplies app IDs or game names and asks whether to buy, analyze, compare, or screen them, or when filter-steam-wishlist hands off resolved app IDs. Produce localized reports from regional current and historical-low pricing, current and past bundles, Steam bundle companion history, US subscription context, full or user-approved proportional or balanced recent Steam review sampling without a language filter, recent forums, product health, and developer-stated Early Access timelines. Requires a connected Steam Review and Forum MCP server; ITAD is optional.
---

# Evaluate Steam Games

Produce one localized purchase report per specified game. SteamID and wishlist visibility do not affect this skill.

## Protect repository state during execution

- Treat the repository as read-only during Steam workflow execution except when creating or updating `config.json` after explicit user confirmation. A separate bundle update may modify tracked repository files only after the user explicitly approves an available update and the update-safety policy authorizes the operation.
- Never modify Python files or create helper scripts in the repository. Report bundled-script failures instead.
- Keep temporary state outside the repository. If unavoidable, use one uniquely named path, verify it before cleanup, remove it on success, failure, or cancellation, and report residue.
- Run bundled scripts with Python 3 and `-B`. Do not install dependencies into the repository.

## Follow the bundle update policy

Set `<repo-root>` to three directories above this skill directory. At the start of the first Steam Purchase Advisor workflow in the current conversation or agent run, read and follow:

`<repo-root>/.agents/references/bundle-update-policy.md`

Treat this policy as required workflow instructions. Do not load or apply it again when the current context shows that a sibling Steam Purchase Advisor skill already followed the bundle update policy.

## Resolve inputs, paths, and configuration

1. Accept one or more app IDs, game names, or IDs handed off by another skill.
2. Resolve every game to one app ID using canonical Steam Store `/app/<appid>/` URLs, preferring the official result; ask when a supplied name remains ambiguous.
3. Resolve bundled scripts and `references/` relative to this `SKILL.md`, shared helpers under `<repo-root>/.agents/lib/steam_purchase_advisor/`, and user config at `<repo-root>/config.json`.

After the first-workflow update-policy gate above, run this at the start of every evaluation:

```text
python -B <repo-root>/.agents/lib/steam_purchase_advisor/config_status.py
```

The helper exposes only presence, field errors, countries, and whether the ITAD key exists. When all request-required fields are valid, stay silent about configuration and do not update it. A request-supplied country overrides config only for that request. Never persist overrides automatically or open, print, quote, or expose `itad_api_key`.

If `config_error` is non-null, stop. Request overrides and the update helper cannot bypass or repair an unreadable file, invalid JSON, or a non-object root because the pricing script, title resolver, and update helper must parse the file first. Report the concise error and ask the user to repair or remove `config.json` manually; never open or overwrite it.

When `config_error` is null and config is absent or a relevant field is missing or invalid:

1. Explain in the user's language that it is local and Git-ignored. Ask only for `report_country`, plus `pricing_country` when ITAD is configured or the user wants pricing. Never request `steam_id`.
2. Use supplied values for the request. Offer one combined confirmation to create or repair only missing or invalid non-secret fields; do not offer to replace valid configured values merely because the request supplied overrides.
3. After confirmation run:

```text
python -B <repo-root>/.agents/lib/steam_purchase_advisor/update_config.py [--report-country <CC>] [--pricing-country <CC>]
```

The helper atomically creates the standard shape, preserves `itad_api_key` and unrelated settings, emits no values, and refuses to replace valid fields. Use `--replace-existing` only after the user requests replacement and separately confirms exact field names. Rerun status after updates. If persistence is declined, use request-only values without asking again.

For an ITAD key, direct the user to `https://isthereanydeal.com/apps/` to register an app and edit local config. The scripts ignore OAuth Client ID and Client Secret; link `https://docs.isthereanydeal.com/` for API documentation. Never request the key in chat or CLI. Rerun status and report only configured or not configured.

## Gate all work on MCP readiness

Complete this gate once per evaluation before review preflight, ITAD queries, corpus creation, or per-game workers. Prefer unprefixed tools on a top-level MCP server; only when absent there, check connected MCP hubs, gateways, or aggregators for one prefixed or routed toolset exposing this skill's tools before treating any tool as missing, and bind every MCP call in this skill to that resolved target.

1. Call `get_server_info` with no arguments (`{}`). Its `name` and `version` identify the currently running MCP server process. Require a valid semantic version of at least **1.1.0**; compare versions semantically, not as strings. Use the reported version as the compatibility check.
2. If `get_server_info` is missing, the call fails, the version is absent or invalid, or it is below the minimum, stop evaluation. Report the observed version or verification failure and the required minimum, then read and follow [the MCP setup procedure](references/mcp-setup.md) completely. Continue only after reconnecting and repeating this gate successfully.
3. After the version check passes, confirm that the MCP advertises `get_steam_game_info`; probe one resolved app ID and reuse its metadata. A returned `game_info` record with missing or null app metadata is not a server outage.
4. If the metadata tool is missing or the probe fails from transport, connection, or timeout, read and follow the MCP setup procedure. If readiness remains unavailable or configuration is declined, stop without review preflight, ITAD queries, corpus creation, per-game workers, or a report.

After readiness, obtain or reuse the `game_info` object from `get_steam_game_info` once per game and derive exactly one release state before preflight or workers:

- `unreleased` when `game_info.release_date_coming_soon` is `true`;
- `early-access` when it is `false` and the English `game_info.genres` array contains exact value `Early Access`;
- `full-release` when it is `false`, `game_info.genres` is available, and lacks `Early Access`;
- `unknown` when required metadata is absent, malformed, or unavailable.

Treat explicit current Steam metadata as authoritative. Never infer Early Access or abandoned development from version numbers, cadence, roadmaps, or community assumptions. For verified `early-access`, retain `game_info.release_date_display` as the current Steam-listed start; mark it unavailable when absent or unparseable and do not treat it as immutable history.

## Select countries, language, and titles

- Use `pricing_country` for Steam AppDetails `cc` and ITAD regional prices and bundles. ITAD subscription access always uses the US catalog. Ask only when ITAD is configured and `pricing_country` is missing or invalid. Never configure a currency or perform conversion.
- Use `report_country` to choose the report language. Ask when missing or invalid and ask for a specific language for multilingual countries.
- Resolve one exact runtime `report_language` and matching Steam language code before preflight or workers.

Resolve titles together:

```text
python -B <repo-root>/.agents/lib/steam_purchase_advisor/resolve_steam_titles.py --appids <appid> [<appid> ...] --report-country <CC> [--language <steam-language>]
```

Prefer Steam's selected-language title; otherwise preserve the publisher's original. Never machine-translate titles. Review retrieval is independent of report language: always use `languages: ["all"]` and report only languages observed in the retrieved evidence. Each returned review's `language` remains a scalar metadata field.

## Preflight review volume and choose modes

Run coordinator-level preflight after country and title resolution, before ITAD, corpora, or analysis workers.

1. For each app ID call `get_steam_review` three times with `review_type` respectively `"all"`, `"positive"`, and `"negative"`. Keep `filter: "recent"`, `languages: ["all"]`, `purchase_type: "all"`, `cursor: "*"`, `num_per_page: 1`, `filter_offtopic_activity: false`, `fetch_all: false`, and `include_review_metadata: false` identical across the calls.
2. Record each response's `game_reviews.total_matching` as respectively `total_reviews`, `total_positive`, or `total_negative`; record unknown when absent, not a non-negative integer, or the call fails. Do not substitute `query_summary` score totals for filtered matching counts; score fields are available only on the first mixed-sentiment page and missing fields are not zero. Treat the sentiment breakdown as known only when both polarity counts are valid, their sum is positive, and it equals `total_reviews` when that count is known. If counts disagree, disclose the inconsistency and make proportional allocation unavailable. These are Steam-reported matching counts, not a fixed-time snapshot.
3. Select `full` automatically for a known `total_reviews` at or below 2,000.
4. For every game above 2,000 or with unknown `total_reviews`, require the user to choose one review mode:
   - `full`: retrieve all matching reviews.
   - `proportional-recent`: require a user-specified total sample size `X` and a known sentiment breakdown. Allocate `X` across positive and negative corpora in proportion to `total_positive : total_negative`, then retrieve the newest reviews within each polarity.
   - `balanced-recent`: require a user-specified total sample size `X`. Split `X` as evenly as integer quotas allow between positive and negative corpora, then retrieve the newest reviews within each polarity.
   - For multiple games, allow a per-game mapping of mode and sample size.
5. Present one localized confirmation for all affected games. Show the known total and polarity counts, explain the three modes briefly, and request `X` for every sampled game. Do not create corpora or start analysis until every affected game has a mode and every sampled game has a valid `X`; stop if the required choice is not made. Do not invent a sample size.
6. Require `X` to be an integer of at least 2. When `total_reviews` is known, require `X < total_reviews`; if the user requests `X >= total_reviews`, explain that full retrieval covers the known population and require either `full` or a smaller `X`.
7. For `proportional-recent`, let `S = total_positive + total_negative`. Compute raw quotas `X * total_positive / S` and `X * total_negative / S`, floor both, then assign any remaining slots by largest fractional remainder until the integer quotas sum exactly to `X`. Break equal fractional remainders in favor of the positive quota. A zero quota means no corpus for that polarity.
8. For `balanced-recent`, set `positive_quota = ceil(X / 2)` and `negative_quota = floor(X / 2)`.

Apply the threshold per game, never to a combined total. Parallel preflight workers may return only app ID, resolved title, total count or unknown, positive count or unknown, negative count or unknown, and a concise failure reason.

## Coordinate multiple games

After modes are fixed, use one parallel worker per game when supported; otherwise run sequentially. Pass app ID, resolved MCP target, countries, exact languages, title, release state, reused metadata, mode, total/positive/negative population counts, sample size and per-polarity quotas when sampled, skill path, and shared ITAD budget. Keep each game's review and forum work in one worker and one report. Keep MCP setup, release classification, preflight, quota calculation, and confirmation in the coordinator.

## Single-game workflow

### 1. Check optional price, bundle, and subscription evidence

Read [the pricing, bundle, and subscription contract](references/pricing-contract.md) completely, then run after MCP readiness:

```text
python -B <skill-dir>/scripts/historical_low_checker.py --appid <appid> [--country <CC>] [--report-country <CC>]
```

When `itad_api_key` and `pricing_country` are available, also check native Steam bundle companions and their ITAD bundle history:

```text
python -B <skill-dir>/scripts/steam_bundle_companions.py --appid <appid> [--country <CC>]
```

When `steam_bundle_companions.py` returns any companion game with `itad_status: "found"`, resolve localized titles for those `found` companion app IDs with `resolve_steam_titles.py` using the runtime `report_country` and `--language`.

Apply every rule in that contract. Treat ITAD and companion-lookup failures as non-fatal. When the key is absent, skip `steam_bundle_companions.py`, explain that local `itad_api_key` configuration enables pricing, bundles, subscription data, and Epic giveaway context, mark that evidence unavailable, and continue.

### 2. Analyze reviews

Use the coordinator-selected mode and `languages: ["all"]`. Pass only parameters advertised by the connected tools; review input schemas reject unknown keys. Recent traversal has no implicit date window, so full mode covers historical reviews as well as recent ones.

#### Full mode

1. Call `create_steam_review_corpus` with app ID, `languages: ["all"]`, `review_type: "all"`, `purchase_type: "all"`, `max_reviews: null`, `traversal_mode: "recent"`, `include_review_metadata: true`, and `include_offtopic_activity: true`.
2. Poll `get_steam_review_corpus_status` to completion or failure.
3. Use `aggregate_steam_review_corpus` for overall, positive, negative, trend, and observed-language counts.
4. Page through `query_steam_review_corpus` with bounded `limit` and increasing `offset` until every stored review is processed.
5. Require an uncapped corpus with `status: "completed"`, `progress.stopped_reason: "exhausted"`, and every stored review processed before calling traversal exhaustive. Compare `progress.total_reviews_exported` with `progress.total_reviews_expected` and the available preflight population; disclose unknown or mismatched counts and do not claim exact population coverage when they cannot be reconciled. `completed` or `corpus_complete: true` alone does not establish exhaustive retrieval; a cap or missing cursor can also complete a job.

#### Sampled modes

For either sampled mode, use the coordinator-calculated positive and negative quotas. For each nonzero quota, create a separate corpus with `languages: ["all"]`, the matching `review_type`, `purchase_type: "all"`, `max_reviews` equal to that polarity's quota, `traversal_mode: "recent"`, `include_review_metadata: true`, and `include_offtopic_activity: true`; create no corpus for a zero quota. Poll every corpus to completion or failure, aggregate each separately, and page through every stored review. Record each stop reason; `max_reviews` is expected when a quota is reached and does not mean the polarity's population was exhausted.

- For `proportional-recent`, treat the result as a recent sentiment-stratified sample with proportional allocation, never as a random sample. The quota ratio comes from preflight population counts; infer neither population rating nor theme prevalence from the retrieved positive-to-negative ratio. Report population sentiment counts or shares only from recorded preflight totals. State that a small minority-polarity quota limits discovery coverage.
- For `balanced-recent`, use every available review when either polarity has fewer reviews than its quota and never transfer unused quota. Treat the result as a recent sentiment-stratified sample with balanced allocation, never as a random or proportional sample. The corpus counts are deliberately reweighted for strength and issue discovery; never interpret cross-polarity raw counts as population voice, rating, or prevalence.

For every mode:

- All review fetches share one request lane and rate-limit cooldown. `running` can mean queued; `waiting` is resumable cooldown, not terminal failure. Honor the UTC `next_retry_at` before polling again, retain the same corpus ID, and never create extra corpora to bypass the queue or cooldown. Direct `STEAM_REVIEW_RATE_LIMITED` errors also carry `next_retry_at`.
- Review corpora require schema 2. For `UNSUPPORTED_CORPUS_VERSION` or `not_found`, recreate the affected corpus with the same approved mode and parameters; report repeated errors instead of recreating indefinitely. Treat failed jobs, `INVALID_STEAM_REVIEW_RESPONSE`, and `MISSING_REVIEW_METADATA` as unavailable or partial evidence, never as a successful empty corpus. Query and aggregate results cover only committed chunks.
- Completed corpora are saved snapshots; status, queries, and aggregates do not refresh them. Create a new corpus for a new evaluation. Retention defaults to 24 hours from the last manifest save and completed reads do not extend it; Steam may cache anonymous responses for up to 10 minutes. State material freshness limits and do not promise a simultaneous multi-page snapshot.
- Query at least `review`, `voted_up`, `language`, `timestamp_created`, and `author.playtime_at_review`.
- Playtime values and thresholds are minutes. Retain refunded reviews without exclusion or reweighting; `refunded` is optional evidence and `null` means unknown. If helpfulness is inspected, `weighted_vote_score` is numeric; it is not a population or theme-frequency weight.
- Maintain four evidence groups: strengths and weaknesses in positive reviews, and weaknesses and strengths in negative reviews.
- Weight recurring, recent, cross-language, and higher-playtime observations over anecdotes; translate or paraphrase into the report language.
- Attach `strong`, `moderate`, or `limited` evidence only when supported by those factors. These labels measure evidence, not quality.
- Report total/positive/negative population counts or unknown, exact mode, requested sample size and quotas when sampled, retrieved counts, stop reasons, observed languages, failures, and material limitations. `languages: ["all"]` does not guarantee every language appears in a sample.
- Claim exact theme counts only when counted in retrieved material. In sampled modes, do not extrapolate retrieved theme counts to the full population.
- When a sampled polarity has a zero quota, state explicitly that no reviews from that polarity were inspected and do not infer themes for that polarity.

### 3. Build the Early Access timeline and inspect current health

For each `early-access` game run:

```text
python -B <skill-dir>/scripts/early_access_duration_extractor.py --appid <appid>
```

On success read `answer` and `url` from stdout JSON. On nonzero exit preserve structured `reason` and `message` from stderr and continue.

Use the English Store Q&A answer, reused `release_date_display`, and runtime evidence date:

1. Prefer an explicit developer-stated full-release date or window. Otherwise derive a target only from a clear Early Access duration plus a parseable Steam-listed start; add calendar months or years, not fixed day counts.
2. Preserve precision and force: ranges, approximations, conditions, and bounds. Never turn broad or conditional language into an exact date or use unrelated time spans.
3. Compare usable targets with evidence date at matching precision and state only upcoming, within window, or past the stated date or bound. Treat the fetched Store Q&A as current but undated.
4. Preserve explicit targets without a start date. Preserve duration without deriving a date when only the start is missing.
5. Treat extraction failure as non-fatal missing evidence. Distinguish request failure, missing Early Access section, missing standard question, and empty answer; never call these developer refusal.
6. Treat a retrieved but uncalculable answer separately: summarize it and state that no defensible target follows.
7. Use verified official roadmaps or announcements as independent evidence. Identify sources, report unresolved conflicts, and prefer neither unless one explicitly supersedes the other.

Then inspect current discussions and official activity:

1. Call `list_steam_forum_sections`; inspect page 1 of the main board and relevant active sections with `list_steam_forum_topics`. Inspect active `eventcomments` for fixes or operational support and, for Early Access, progress and roadmaps.
2. Treat listing `last_activity_timestamp` and `last_activity_display` only as reply or listing activity. For publication-time claims open the topic with `get_steam_forum_topic` and use `topic.original_post_timestamp`; report unknown when null. Calculate material Early Access update gaps only from verified original-post timestamps.
3. For every game open enough relevant topics to support every material claim about current bugs, crashes, performance, content, servers, shutdowns, and operational support.
4. For `early-access`, also inspect roadmap progress, verified update gaps, developer communication, closure or layoffs, end-of-development notices, and recurring unfinished-game complaints.
5. For `full-release`, treat sparse updates as neutral. Do not search for routine update gaps, developer silence, missed roadmaps, or halted-development risk. Put material server or support availability, degradation, or shutdown under current issues.
6. For `unknown` or `unreleased`, omit Early Access-only judgments and state the metadata gap only when it limits the recommendation.
7. Separate official evidence from community speculation. Only for `early-access`, classify halted-development risk as `none found`, `low`, `medium`, `high`, or `confirmed`.
8. Preserve direct URLs for opened topics, events, and announcements; prefer direct evidence over section or listing links.

If individual forum calls fail while MCP remains healthy, mark coverage partial and continue.

### 4. Produce the localized report

Immediately before composing each report, read and apply [the purchase report contract](references/report-contract.md) completely. Audit the localized report before delivery.
