---
name: openvan-travel
description: Answer road-trip, campervan, motorhome, RV and vanlife travel questions with live OpenVan.camp data — a whole-trip plan between places, fuel prices by country, toll roads and vignettes, ferry crossings and timetables, visa and vehicle-import rules for a passport, customs at the border, public and school holidays, travel hazards and wildfires, power plugs, weather for travelling and sleeping in a van, food costs, currency, vanlife events and news, license plates. Use when the user plans a trip by car or campervan, or asks about any of these for a country or route.
license: MIT
metadata:
  author: OpenVan.camp
  homepage: https://openvan.camp/ai
---

# OpenVan.camp travel data

Live, read-only travel data for 200+ countries from the OpenVan.camp MCP server
(`https://mcp.openvan.camp/mcp`, no key; installed together with this plugin).
If the `openvan` MCP tools are not available, call the REST API instead — the mapping is in
[references/rest-api.md](references/rest-api.md).

## Rules that matter

1. **Pass `locale` on every call** — the language the user writes in (`en`, `ru`, `de`, `fr`,
   `es`, `pt`, `tr`). Place names, units and the interactive cards follow it.
2. **A trip from A to B (or several stops) → `plan_road_trip` first, once.** It returns the whole
   trip: route, day-by-day plan, budget (fuel, tolls, vignettes, ferries), and for every country
   on the way the entry and vehicle rules, holidays, hazards and power. Give the user the roadbook
   link it returns. Do not rebuild a trip out of single-topic tools; use those only for
   follow-up questions about one country or one topic.
3. **"No data" is not "nothing applies".** A tool that says it has no data for a country, a
   `covered: false` answer, an empty vehicle-import result, a toll estimate flagged as partial or
   a ferry with no open timetable means OpenVan.camp does not know — not that the border is open, the road is free, nothing is
   restricted or there are no holidays. Say so and point to the official source of that country.
4. **Visa and vehicle rules:** quote the allowed stay *and* how the days are counted (per entry
   or a rolling window such as 90 in 180), say whether the vehicle may stay as long as the person,
   and give `source_url`. The rule depends on the passport, not on where the person lives. When
   `confidence` is not `high`, tell the user to confirm with the embassy. Never present it as
   legal advice.
5. **Prices are approximate.** They are converted with fresh exchange rates; quote them with the
   currency, the unit and a link to the source page. A grade's unit and currency can differ from
   the country's (Colombia sells petrol by the gallon; Venezuela prices petrol in VES and diesel
   in USD) — the tools already account for it, so do not "fix" the numbers.
6. **Hazards are the situation now, not a forecast.** Weather scores (0–100) rate how good the
   weather is for travelling and sleeping in a van, not how warm it is.
   Weather tools cover today and the coming 7 days. For a later date or "when is the best time to
   go", `get_city_climate` gives the typical weather (climate, ERA5 2021–2025): say it is what the
   weather is usually like on that date, not a forecast.
7. **License plates:** explain formats and region codes; never try to identify a vehicle owner.
8. **Sources:** each tool result carries the URL of the page it comes from; include it where the
   user would want to check details or read more.

## Which tool

| The user asks | Tool |
|---|---|
| Plan a trip A → B (→ C …), budget, what to know on the way | `plan_road_trip` |
| Everything about driving into one country | `get_country_travel_brief` |
| Fuel price in a country / compare countries / cheapest in a region | `get_fuel_prices` / `compare_fuel_prices` / `find_cheapest_fuel` |
| Tolls and vignettes in a country / toll cost of a route | `get_toll_rates` / `estimate_route_tolls` |
| Visa for a passport / for a whole route / foreign-plated vehicle | `check_visa_rules` / `get_route_visa_rules` / `get_vehicle_import_rules` |
| Customs limits at the border | `get_customs_rules` |
| Public, school holidays, peak traffic days | `get_holidays` |
| Is it safe now, disasters / wildfires near a place | `get_travel_hazards` / `get_active_fires` |
| Ferries to an island or across a sea, strait or river / next departure, crossing time | `find_ferries` (bbox, narrow with `query` = port or operator), then `get_ferry_schedule` with its id |
| Sockets, voltage, campsite hook-up | `get_power_plugs` |
| Weather for one city / a country / where to go for good weather | `get_city_travel_weather` / `get_country_travel_weather` / `list_best_weather_countries` (`period=week` for this week: the OpenVan.camp ranking) |
| Usual weather on a later date, sea temperature in a month, best month to go | `get_city_climate` (city or lat/lng; omit `date` for the 12 months) |
| How expensive food is / compare / rank | `get_country_food_prices` / `compare_food_prices` / `rank_food_prices` |
| Convert money | `get_currency_rate` |
| Vanlife events, festivals, expos | `list_events`, then `get_event` |
| News about campervans and road travel | `search_stories` |
| What a plate looks like / which region a code is / draw a plate | `get_license_plate_country` / `check_license_plate` / `get_license_plate_image` |

## Answer shape

Lead with the answer (the number, the rule, the plan), then the details the user needs to act
on it, then the source link. Keep currency, unit and date next to every price.
