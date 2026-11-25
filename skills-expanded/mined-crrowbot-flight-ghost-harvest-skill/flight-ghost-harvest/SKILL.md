---
name: flight-ghost-harvest
description: Use when collecting Ctrip flight search results in a logged-in desktop Chrome session with Ghost OS. This skill is for browser-only harvesting of airfare and itinerary data from Ctrip result pages, including domestic and international flows, when Playwright or direct HTTP scraping is blocked, especially when you need to verify search state, open result cards and fare drawers, capture visible itinerary fields and rule text, and save raw plus cleaned JSON.
---

# Flight Ghost Harvest

Use this skill to collect Ctrip flight search results from the real desktop Ctrip flow in Chrome with Ghost OS.

Do not use Playwright for this workflow. Prefer the user's already logged-in Chrome window, especially when Ctrip uses queue pages, login refreshes, dynamic price cards, or fare-rule drawers that render only after interaction.

## Environment Requirements

- macOS desktop session
- Desktop Google Chrome
- Logged-in session for Ctrip
- [Ghost OS](https://github.com/ghostwright/ghost-os) available through MCP
- Permission to control Chrome and read the screen
- `python3` available locally for post-processing scripts

This skill is not designed for headless environments.

## Core Rules

- Use Chrome on the desktop, not Playwright.
- Use Ghost OS perception first: `ghost_context`, `ghost_read`, `ghost_annotate`.
- Confirm the search state before harvesting:
  - origin city or airport
  - destination city or airport
  - departure date
  - return date when round trip
  - passenger mix and cabin when visible
- Work from the Ctrip result list page rather than checkout or booking-detail pages.
- Prefer result cards that expose headline fare plus expandable booking options when the user wants bookable flights.
- If Ctrip shows login refresh, queue, SMS verification, or a forced redirect, stop and ask the user to complete it manually, then resume.
- Collect raw page text before aggressive cleanup.
- Save both raw and normalized JSON.
- Do not stop at a single departure date when the user wants price coverage. Default to harvesting the next 30 days unless the user narrows the date window.
- Sync final normalized output into the global SQLite database so later queries can reuse prior harvests.
- Maintain a dedicated route refresh table in SQLite so the agent can check last-refresh state without scanning all flight rows.
- Unless the user explicitly says one-way only, check both one-way and round-trip markets. Users usually return, so default to covering `one_way` and `round_trip`.
- For round-trip coverage, do not guess the return gap. Ask the user for an approximate stay length first, such as `3 days`, `1 week`, or `around 10 days`.
- If the user only says a route like `上海 -> 东京`, proactively ask how many days they plan to stay, then use that answer to search outbound plus return options.
- Keep temporary files under `/tmp/flight-harvest`.
- Save final deliverables in the task workspace, not `/tmp/flight-harvest`.
- Keep timestamps in ISO 8601 where possible.
- Keep money values numeric when possible and preserve the original price string.
- Never invent baggage, refundability, terminal, or fare-rule data when the page does not expose it.
- Treat each visible Ctrip booking option as a separate fare candidate when total price or rule text differs.
- When the search is round trip, capture the return-leg list too.

## When To Use

- The user wants current Ctrip flight listings, fares, or calendar prices.
- Ctrip blocks direct scraping or API use.
- The user already has a working Chrome session and Ghost OS is available.
- A dynamic browser workflow is required to open Ctrip result cards, transfer panels, baggage drawers, or refund/change rules.

## Limitations

- Flight prices are volatile. Treat captures as time-stamped observations, not durable truth.
- Ctrip lazily loads more results while scrolling and may reorder cards after filters change.
- Some fare rules are hidden behind drawers or secondary pages and may not be visible for every booking option.
- Calendar prices and card prices can disagree because of inventory refresh timing.
- This skill is optimized for Ctrip one-way and round-trip result pages, including international result URLs such as `/online/list/oneway-sha-tyoa`.

## Workflow

### 1. Preflight

- Confirm Chrome has an open tab on:
  `https://flights.ctrip.com/online/channel/domestic`
- International result pages under `https://flights.ctrip.com/online/list/` are also valid entry points.
- Ensure `/tmp/flight-harvest` exists.
- Run `ghost_context app:"Google Chrome"` to confirm the URL and window title.
- If Ghost OS is misbehaving, run `ghost doctor` before continuing.
- If the page is a queue, verification, or login gate, stop and wait for the user to clear it.

### 2. Verify Search State

Do not start harvesting until all visible search parameters match the request.

Capture:

- `source_site` as `ctrip`
- `trip_type`
- `origin`
- `destination`
- `departure_date`
- `return_date`
- `segment_type`
- `passengers`
- `cabin`
- visible filters such as direct-only, airline, departure window, and sort mode

If the page drifted into a fare-detail, booking-detail, or checkout flow, navigate back to the result list and re-verify the state.

### 2a. Ctrip Search-State Checks

Do not start harvesting until all of the following are true:

- the page shows the intended route
- the page shows the intended departure date
- if round trip, the intended return date is visible
- any user-requested filter is visibly active
- the page is a result list, not the booking submit page

If the user did not request filters, harvest the default visible ordering and store any active sort or filters in raw metadata.

### 2b. Check Database Freshness First

Before harvesting, check the global SQLite database. Read the route refresh table first so you can avoid redundant crawling:

```bash
python3 scripts/check_db_freshness.py SHA TYOA
```

The freshness script should read `route_refresh_state` first and only fall back to the `flights` table if the refresh table has not been built yet.
If you need to inspect the SQLite database directly, read `references/database-guide.md` first.

Prefer using the unified planner when possible:

```bash
python3 scripts/plan_harvest_run.py SHA TYOA --stay-days 5
```

Add `--execute` only after the current Chrome tab is ready for harvesting.
The planner defaults to conservative browser actions: `--expand-limit 0` and `--scroll-steps 0`. Increase them only when you need deeper fare rows or more on-page results.

Use this policy:

- If no route data exists, harvest the next 30 days.
- If route data exists and the latest update is 24 hours old or more, harvest the next 7 days.
- If route data exists and the latest update is less than 24 hours old, harvest only the current day.
- Unless the user explicitly wants one-way only, evaluate both `one_way` and `round_trip`.
- For round-trip searches, first get the user's approximate stay length, then capture both the outbound list and the corresponding return-leg list.
- If the user does not provide a stay length, do not invent one. Continue with `one_way` coverage and tell the user you still need an approximate trip length to search round trips well.
- Example: if the user says `看下上海到东京的机票`, first ask `大概去几天？` and only then run the round-trip search.

When you need cached data instead of a new crawl:

- read `route_refresh_state` for route freshness
- read `flights` for row-level itinerary data
- read `harvest_runs` for run provenance
- prefer `check_db_freshness.py` over handwritten SQL when deciding refresh scope

### 3. Capture Visible Result Cards

- Use `ghost_annotate app:"Google Chrome"` to identify visible result cards or list items.
- Prefer clicking the itinerary card or headline fare row, not ad banners or sticky filter chips.
- Read the updated page text with `ghost_read` after each click.
- Deduplicate records by the combination of:
  - `source_site`
  - `origin`
  - `destination`
  - `departure_date`
  - `airline`
  - `flight_numbers`
  - `depart_time_local`
  - `arrive_time_local`
  - `price_total`
- Keep a `source_step` or scroll index in raw output.
- Keep a `page_section` when Ctrip segments results by recommendation or time window.

### 4. Extract Structured Fields

For each visible itinerary, extract as many of these fields as the page exposes:

- `source_site`
- `trip_type`
- `search_url`
- `captured_at`
- `origin`
- `destination`
- `origin_airport`
- `destination_airport`
- `departure_date`
- `return_date`
- `segment_type`
- `airline`
- `marketing_airline`
- `operating_airline`
- `flight_numbers`
- `depart_time_local`
- `arrive_time_local`
- `depart_terminal`
- `arrive_terminal`
- `duration_minutes`
- `stops`
- `stop_airports`
- `cabin`
- `fare_brand`
- `seat_left`
- `baggage_allowance`
- `refund_change_rules`
- `price_currency`
- `price_total`
- `price_base`
- `taxes_fees`
- `booking_channel`
- `booking_link`
- `sort_mode`
- `active_filters`
- `card_text_raw`
- `rules_text_raw`

If the page exposes separate rule drawers or detail dialogs, open them and collect the text into `rules_text_raw`.

### 4a. Ctrip Card Reading Rules

- Prefer the card that contains the route times, airport names, carrier, stop badge, and headline price in one visible block.
- If a card contains multiple fare rows under one itinerary, keep one raw record per fare row when price or fare family differs.
- If a fare row requires expansion to expose baggage or refund rules, open it and reread the card text.
- If a card shows a transfer city or overnight badge, preserve that text in `card_text_raw` even when you also derive structured fields.

### 4b. Fare Rule Extraction

- Look for Ctrip text that corresponds to refundability, change fee, baggage allowance, and seat availability.
- Store the original visible rule text in `rules_text_raw`.
- Normalize only lightly in the final JSON. Do not paraphrase away fee conditions.
- If the rule text changes after selecting a different booking option, treat that as a separate record.

### 5. Scroll Strategy

- Scroll inside the result list area rather than the full page when Ctrip uses a virtualized list.
- After each scroll:
  - rerun `ghost_annotate`
  - collect newly visible cards
  - stop after several consecutive scrolls yield no new itineraries
- If Ctrip exposes pagination instead of infinite scroll in the current flow, finish the current page before moving to the next.

### 6. Calendar And Price Grid Mode

When the user asks for the cheapest days rather than specific itinerary cards:

- Open the calendar or fare grid view.
- Capture one cell per visible date.
- Store:
  - `date`
  - `price_total`
  - `price_currency`
  - `calendar_label`
  - `is_lowest_visible` when clearly marked
- Save these as raw records with `record_type: "calendar_price"`.
- Do not mix calendar cells with itinerary cards in the same normalized output file unless the user explicitly wants both.

### 7. Output

Prefer two outputs:

1. Raw harvest JSON with every captured card or calendar cell.
2. Normalized JSON with one object per itinerary or calendar price record.

Use deterministic snake_case filenames such as:

- `ctrip_sha_ckg_2026-04-12_one_way_raw.json`
- `ctrip_sha_ckg_2026-04-12_one_way_normalized.json`
- `ctrip_sha_ckg_2026-04-12_to_2026-04-19_round_trip_calendar_raw.json`

## Post-Processing

Use the helper script in this repository to normalize raw records:

```bash
python3 scripts/normalize_flights.py raw.json normalized.json
```

To capture the currently open Ctrip result page from Chrome:

```bash
python3 scripts/harvest_ctrip_chrome.py out/ctrip_raw.json --expand-limit 1
python3 scripts/normalize_flights.py out/ctrip_raw.json out/ctrip_normalized.json
```

To capture more than the first screen of results:

```bash
python3 scripts/harvest_ctrip_chrome.py out/ctrip_raw.json --expand-limit 1 --scroll-steps 4 --scroll-pixels 900
python3 scripts/normalize_flights.py out/ctrip_raw.json out/ctrip_normalized.json
```

For round trips, prefer:

```bash
python3 scripts/harvest_ctrip_chrome.py out/ctrip_round_raw.json --capture-return-leg --date-span-days 30 --expand-limit 4 --scroll-steps 4
python3 scripts/normalize_flights.py out/ctrip_round_raw.json out/ctrip_round_normalized.json
```

Unified planner example:

```bash
python3 scripts/plan_harvest_run.py SHA TYOA --stay-days 5 --output-dir out
python3 scripts/plan_harvest_run.py SHA TYOA --stay-days 5 --output-dir out --execute
```

For one-way searches over the next month:

```bash
python3 scripts/harvest_ctrip_chrome.py out/ctrip_month_raw.json --date-span-days 30 --expand-limit 4 --scroll-steps 4
python3 scripts/normalize_flights.py out/ctrip_month_raw.json out/ctrip_month_normalized.json
python3 scripts/sync_flights_db.py out/ctrip_month_normalized.json --raw-path out/ctrip_month_raw.json
```

The global SQLite database defaults to:

- `~/.local/share/flight-harvest/flights.db`

## Anthropic Compatibility

This repository includes an Anthropic Claude Code compatible subagent at:

- `.claude/agents/flight-ghost-harvest.md`

To install it into another project:

```bash
python3 scripts/install_anthropic_agent.py /path/to/target-project --with-references --with-scripts
```

For site-specific extraction differences, read:

- `references/flight-schema.md`
- `references/ctrip-domestic.md`
