---
name: filter-steam-wishlist
description: Filter a public Steam wishlist by Steam Store sale or historical-low state, release state, Steam Demo availability, and pricing country, or screen which wishlist games have Steam bundle companions with ITAD bundle history; localize titles and optionally hand selected app IDs to evaluate-steam-games. Use to list or filter a wishlist, find its on-sale, historical-low, unreleased, Early Access, full-release, demo, or bundled-companion games, or analyze selected wishlist games. Accept SteamID64, numeric or custom profile URLs, and exact custom profile IDs; requires a resolvable profile with a public wishlist.
---

# Filter Steam Wishlist

Filter a public Steam wishlist and localize its titles. Hand selected IDs to `evaluate-steam-games` only for analysis. Do not check MCP readiness; this skill does not use that server. Limit price filtering to the Steam Store, excluding third-party key sellers.

## Protect repository state during execution

- Treat the repository as read-only during Steam workflow execution except when creating or updating `config.json` after explicit user confirmation. A separate bundle update may modify tracked repository files only after the user explicitly approves an available update and the update-safety policy authorizes the operation.
- Never modify an existing Python file or create helper scripts in the repository. Report bundled-script failures instead.
- Keep temporary state outside the repository. If repository-local state is unavoidable, use one uniquely named, tracked path; remove it on success, failure, or cancellation after verifying the cleanup target and report any residue.
- Run bundled scripts with Python 3 and `-B`. Do not install dependencies into the repository.

## Follow the bundle update policy

Set `<repo-root>` to three directories above this skill directory. At the start of the first Steam Purchase Advisor workflow in the current conversation or agent run, read and follow:

`<repo-root>/.agents/references/bundle-update-policy.md`

Treat this policy as required workflow instructions. Do not load or apply it again when the current context shows that a sibling Steam Purchase Advisor skill already followed the bundle update policy.

## Resolve paths and configuration

Resolve the wishlist script at `scripts/get_wishlist_appids.py` relative to this `SKILL.md`, the bundle companion script at `<repo-root>/.agents/skills/evaluate-steam-games/scripts/steam_bundle_companions.py`, shared helpers under `<repo-root>/.agents/lib/steam_purchase_advisor/`, and user config at `<repo-root>/config.json`.

After the first-workflow update-policy gate above, run this at the start of every wishlist request:

```text
python -B <repo-root>/.agents/lib/steam_purchase_advisor/config_status.py
```

The helper exposes only configuration presence, field errors, countries, and whether the ITAD key exists. Use it even in unfiltered mode. When all required fields are valid, stay silent about configuration and do not run the update helper. Never open `config.json` or expose `itad_api_key`. Request-supplied profile or country values override config only for that request; never persist them automatically.

If `config_error` is non-null, stop. Request overrides and the update helper cannot bypass or repair an unreadable file, invalid JSON, or a non-object root because the wishlist script, title resolver, and update helper must parse the file first. Report the concise error and ask the user to repair or remove `config.json` manually; never open or overwrite it.

## Guide first-use configuration

When `config_error` is null and `config.json` is absent or a relevant field is missing or invalid:

1. Explain in the user's language that the file is local and Git-ignored. Ask only for what the request needs:
   - `steam_id`: required unless this request supplies one of the profile identifiers accepted below; the wishlist must be public.
   - `report_country`: required for title localization; use an uppercase ISO 3166-1 alpha-2 code and ask for a language when the country is multilingual.
   - `pricing_country`: required only for an active price filter or when screening wishlist games for Steam bundle companions.
   - `itad_api_key`: optional for basic listing; without it, `on-sale` and `historical-low` filtering and Steam bundle companion screening are unavailable. Return the wishlist with `--price-state any` while preserving any explicit release-state and demo-state filters, and state that price filtering was not applied.
   - `unreleased`, `early-access`, `full-release`, `available` demo, and `unavailable` demo filtering use Steam Store metadata and do not require ITAD configuration.
2. Resolve request-supplied Steam identity input before discussing persistence:

```text
python -B <repo-root>/.agents/lib/steam_purchase_advisor/steam_identity.py --steam-profile <STEAMID64-OR-PROFILE>
```

   Use the returned `steam_id` for the request and any save offer. Store only the resolved 17-digit SteamID64, never the custom ID or URL.
3. Offer one combined confirmation to create or repair only the missing or invalid non-secret fields. Include `steam_id` only when `steam_id_configured` is false. If it is already configured, keep request-supplied identity input temporary and do not offer replacement unless the user explicitly asks to replace it.
4. After confirmation, use the shared secret-safe update helper; pass the resolved numeric ID, not a custom ID or URL:

```text
python -B <repo-root>/.agents/lib/steam_purchase_advisor/update_config.py [--steam-id <STEAMID64>] [--report-country <CC>] [--pricing-country <CC>]
```

The helper atomically creates the standard shape, preserves `itad_api_key` and unrelated settings, emits no values, and refuses to replace valid fields. Use `--replace-existing` only after the user requests replacement and separately confirms exact field names. Rerun status after updates. If persistence is declined, use request-only overrides without asking again.

For an ITAD key, direct the user to `https://isthereanydeal.com/apps/` to register an app and edit local config. The scripts ignore OAuth Client ID and Client Secret; link `https://docs.isthereanydeal.com/` for API documentation. Never request the key in chat or CLI. Rerun status and report only configured or not configured.

## Resolve the Steam profile and require a public wishlist

- Accept a 17-digit SteamID64; a Steam Community `/profiles/<SteamID64>` or `/id/<custom-id>` URL using HTTP, HTTPS, or no scheme; or an exact bare custom ID such as `your-custom-id`.
- Treat a bare nonnumeric value only as an exact custom profile ID, never as a display-name search.
- If the identity helper already resolved the request input, pass its numeric result to `--steam-profile`. Otherwise pass the original accepted input; the wishlist script extracts numeric profile URLs locally, resolves custom IDs through Steam Community, and validates the returned SteamID64. Follow the first-use rules above for persistence.
- If no profile identifier is available, stop and explain the accepted forms in the user's language.
- If resolution fails, give the concise reason and offer `https://steamid.io/lookup/` for manual lookup, followed by the resulting SteamID64 in chat. Do not imply Valve affiliation.
- If the script returns `wishlist_unavailable`, stop and give its concise, non-sensitive reason.
- Treat a successful empty JSON array as an empty public wishlist.
- If Steam returns no usable items field, ask the user to verify the SteamID64 and wishlist visibility; do not report an empty wishlist.

## Select filters

Map each dimension independently, apply only explicitly requested filters, and AND-combine them.

Price intent:

| Price intent | Argument |
| --- | --- |
| Not requested, generic list/show, or explicit complete wishlist | `--price-state any` |
| Currently on sale | `--price-state on-sale` |
| At the Steam Store historical low | `--price-state historical-low` |

Release intent:

| Release intent | Argument |
| --- | --- |
| Not requested | `--release-state any` |
| Unreleased / upcoming / coming soon | `--release-state unreleased` |
| Early Access | `--release-state early-access` |
| Full release | `--release-state full-release` |

Demo intent:

| Demo intent | Argument |
| --- | --- |
| Not requested | `--demo-state any` |
| Steam Demo available | `--demo-state available` |
| Steam Demo unavailable / explicitly without a demo | `--demo-state unavailable` |

Run the script using the canonical command shape, always passing all three state arguments explicitly:

```text
python -B <skill-dir>/scripts/get_wishlist_appids.py \
  --price-state any|on-sale|historical-low \
  --release-state any|unreleased|early-access|full-release \
  --demo-state any|available|unavailable \
  [--steam-profile <profile-or-id>] \
  [--country <CC>]
```

Demo semantics: Filtering is based only on the Steam AppDetails `demos` field. When describing results to the user, use precise phrasing like "Steam Demo available" rather than implying broader trial access.

`--steam-id` remains a backward-compatible alias for `--steam-profile`.

Sale and historical-low filters restrict results to Steam Store deals (`shop_id=61`, `vouchers=false`). The `historical-low` state compares each Steam deal's current price against its per-store low, not a cross-store historical low.

When `price-state` is `any`, do not require ITAD configuration or pass `--country`.

For price filtering, pass `pricing_country` to Steam AppDetails as `cc`; treat it as a regional selector, never pass a currency, convert currencies, or reuse another country's result. The script exact-matches Steam currency and initial/final minor-unit amounts against ITAD, preferring `app/<appid>` and accepting base-price packages only when they resolve unambiguously to one identity. It omits ambiguous or unmatched products and never selects by response order or title.

Missing `price_overview` means unpriced and not on sale; a complete undiscounted price is also not on sale. Malformed currency or minor-unit amounts produce `price_data_unavailable` with reason `steam_price_metadata_malformed` and no partial price-filtered result.

The script uses shared Steam metadata and preserves wishlist order. `store_metadata_unavailable` (exit code 5) is a hard stop: report that Steam Store metadata was unavailable, do not treat it as an ITAD failure, do not rerun with dropped filters, and do not present a partial result. `release_state_data_unavailable` is also a hard stop; do not present a partial result. Demo metadata normalizes missing values to `False`, so there is no demo-specific unavailable error.

Parse successful stdout internally as a JSON array of numeric app IDs. Resolve titles for list requests; hand selected IDs to `evaluate-steam-games` for analysis. Before handing off any complete price-unfiltered wishlist, including a fallback, report its size and require confirmation of all games or a subset.

## Resolve and present titles

For every non-empty result, run:

```text
python -B <repo-root>/.agents/lib/steam_purchase_advisor/resolve_steam_titles.py --appids <appid> [<appid> ...] [--report-country <CC>] [--language <steam-language>] [--max-workers <1-8>]
```

- Use the request or config `report_country`; ask for it when missing or invalid. For a multilingual country, ask for the report language and pass the matching Steam language with `--language`.
- Treat Steam's returned title as authoritative. Preserve the publisher's original title when Steam has no localization; never machine-translate it.
- Preserve result order. On an individual lookup failure, retain the game as linked `AppID <appid>`.
- Present successful results as linked localized titles with AppIDs. Do not return a bare AppID array when title resolution succeeds.
- Keep the resolver's default concurrency of four and maximum of eight; lower it only for throttling or local constraints. Its retry policy is code-enforced. Preserve specific failures, including `steam_title_not_returned` and `steam_invalid_response`.

## Screen wishlist games for bundled Steam companions

When the user asks which games on their wishlist have Steam bundle companions with bundle history (for example, asking which wishlist games are in Steam bundles whose other games have been bundled):

1. Require a resolvable public wishlist (`steam_id` or `--steam-profile`), `report_country` (and `report_language`), `pricing_country`, and `itad_api_key`. If `itad_api_key` is unconfigured, explain that ITAD configuration is required to check companion bundle history, direct the user to `https://isthereanydeal.com/apps/`, and stop without running companion screening.
2. Run `scripts/get_wishlist_appids.py` (using `--price-state any --release-state any --demo-state any` unless the user also requested an explicit price, release, or demo filter) to obtain the candidate wishlist AppIDs in wishlist order. If the list is empty, report that and stop.
3. Run the companion checker in batch mode across the wishlist AppIDs:

```text
python -B <repo-root>/.agents/skills/evaluate-steam-games/scripts/steam_bundle_companions.py --appids <appid> [<appid> ...] [--country <CC>]
```

4. Interpret the batch output (`only_found` is applied by default):
   - `checked_count` and `checked_appids` record the wishlist games inspected.
   - `matched_count`, `matched_appids`, and `results[]` contain only the wishlist games that have at least one regional Steam Store `/bundle/<bundleid>` combination whose companion game has confirmed ITAD bundle history (`itad_status: "found"`).
   - Inside each matched wishlist game's `bundles[]`, only `found` Steam combinations and only `found` companion games (`other_games[]`) with confirmed `occurrence: "occurred"` ITAD bundle records (`itad_records[]`) are returned.
5. When `results[]` is non-empty, collect all `matched_appids` and all `found` companion `appid`s from `results[].bundles[].other_games[]`, and resolve their localized titles in one `resolve_steam_titles.py` call with `--report-country <CC>` and `--language <steam-language>`.
6. Present the localized response in `report_language`:
   - State how many wishlist games were checked (`checked_count`) and how many matched (`matched_count`).
   - When `results[]` is empty (`matched_count == 0`), state that none of the checked wishlist games currently have Steam bundle companions with recorded ITAD bundle history.
   - For each matched wishlist game (preserving wishlist order), show a clear table or structured list containing:
     - **Wishlist game:** `[Localized title](https://store.steampowered.com/app/<target_appid>/)`
     - **Steam bundle(s):** `[Bundle title](https://store.steampowered.com/bundle/<bundleid>/)`
     - **Bundled companion game(s):** `[Localized companion title](https://store.steampowered.com/app/<appid>/)`
     - **Companion bundle history:** total confirmed bundle count (`itad_record_count`), any `active` bundle (`details_url`, `offer_url`, provider, expiry), and up to the three most recent `expired` bundles (`details_url`, provider, dates, and material tier/selection notes from `qualifying_tiers` and `note`). When the same companion game appears across multiple Steam bundles for a wishlist game, group or cross-reference those Steam bundles rather than repeating identical history.
   - Never mention unbundled companion games or non-game bundles. Disclose any entries in top-level `errors[]` concisely.

## Degrade when ITAD is unavailable

Price filtering (`on-sale` and `historical-low`) requires `itad_api_key` and `pricing_country`.

- If the key is configured but the country is missing or invalid, ask for an uppercase two-letter country code and pass `--country <CC>`.
- If a price-filtered run returns `price_data_unavailable` because of missing or invalid configuration, an ITAD request, authentication, network, response, or rate-limit failure, or malformed regional Steam price metadata, explain that current price, discount, and historical-low data are unavailable. Honor `Retry-After` once when practical.
- Rerun with `--price-state any` after any unresolved `price_data_unavailable`, preserving the exact selected `--release-state` and `--demo-state` selections. State prominently that the price filter was not applied and never describe the fallback as price-filtered.
- Present fallback list requests through the title resolver.

Release-state filtering uses Steam Store metadata independently of ITAD. When it returns `release_state_data_unavailable`, do not rerun without `--release-state`, do not treat unknown metadata as full release, and do not present a partial release-state result.

## Preserve request limits

Treat ITAD's 1,000 requests per rolling five minutes as one shared API-key budget. ITAD is used only when price-state is on-sale or historical-low, or when screening wishlist games for Steam bundle companions; price-state any without companion screening uses no ITAD requests, including release-state-only and demo-state-only filtering. Let P be the number of distinct app and eligible base-package products discovered for wishlist games that Steam reports as discounted. Estimate a price-filtered run's upper bound as 2 * ceil(P / 200) ITAD requests: one product-lookup pass and one price pass. `steam_bundle_companions.py --appids ...` shares the same rolling five-minute API-key budget via the locked local request ledger, batches companion `app/<appid>` identity lookups (up to 200 products per request), and deduplicates UUID bundle-history queries across the entire wishlist batch. Reserve a safety margin, honor rate limits, and pass known prior consumption to evaluate-steam-games on handoff.

Start one AppDetails fetch operation per original wishlist AppID when any metadata filter is active, using at most four concurrent operations with bounded retries. Reuse each resulting snapshot across combined filters; all-`any` starts no AppDetails fetches.
