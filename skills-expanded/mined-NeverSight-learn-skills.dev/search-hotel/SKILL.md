---
name: search-hotel
description: Search for hotels by location and dates. Use this skill whenever the user wants to find a place to stay, look for accommodation, search for hotels, or asks questions like "find me a hotel in X", "where can I stay in Y", "show me hotels near Z", or provides a destination plus check-in/check-out dates. Always use this skill before book-hotel or search-room since those require a sessionId from this search.
license: MIT
---

# search-hotel

Search hotels using the `travel-cli`. Returns a list of matching hotels with prices, ratings, and the IDs you need to book or look at room options.

## When to use

Trigger this skill when the user wants to find accommodation. Examples:

- "Find me a hotel in Tokyo from May 1 to May 5"
- "Show me 4-star hotels in Paris with ocean view"
- "Where can I stay near Shibuya next weekend"
- "I need a place for 2 adults and 1 child in Bangkok"

Do NOT use this skill for flights, tours, restaurants, or non-accommodation travel queries.

## Prerequisites

The `travel-cli` CLI must be available. Run via `npx`:

```bash
npx @tvl-justin/travel-cli@latest search-hotel ...
```

If the user has installed it globally (`npm install -g @tvl-justin/travel-cli`), call `travel-cli` directly.

## How to call

The full command:

```bash
npx @tvl-justin/travel-cli@latest search-hotel \
  --location "<city or destination>" \
  --checkin <YYYY-MM-DD> \
  --checkout <YYYY-MM-DD> \
  --rooms "<occupancy>" \
  --limit 5
```

### Parameter rules

- **`--location`** (required) — A city, neighborhood, or destination name. Use the most specific one the user gave. If the user only said "Tokyo" use `"Tokyo"`; if they said "Shinjuku, Tokyo" use `"Shinjuku, Tokyo"`.
- **`--checkin` / `--checkout`** (required) — `YYYY-MM-DD` format. Resolve relative dates ("next weekend", "tomorrow") against today's date before calling. If the user only gave a single date and a duration ("3 nights from May 1"), compute the checkout date.
- **`--rooms`** — Occupancy string. Format:
  - `"2"` = 1 room, 2 adults
  - `"2,5"` = 1 room, 2 adults + 1 child age 5
  - `"2,3,8"` = 1 room, 2 adults + children ages 3 and 8
  - Multiple rooms separated by `;`: `"2;2,5"` = room 1 has 2 adults, room 2 has 2 adults + child age 5
  - Default if user doesn't specify: `"2"`.
- **`--limit`** — How many hotels to return. Default 5. Increase to 10 if the user wants more options.
- **`--min-price` / `--max-price`** — Price per night in USD. Always convert other currencies to USD before passing. E.g. "under 2 million VND" → `--max-price 80`.
- **`--filters`** — Comma-separated. Allowed values: `free_breakfast`, `swimming_pool`, `ocean_view`, `all_inclusive`. Only include filters the user explicitly asked for.
- **`--lat` / `--lng`** — Optional coordinates for precision. Use them when you know the coordinates of a well-known city.

## Asking for missing info

If the user gave a destination but not the dates, ask once for both check-in and check-out (or check-in plus duration). Don't ask for occupancy unless the question implies a non-default party (e.g. "for my family of 4").

## Output

The CLI prints JSON to stdout:

```json
{
  "sessionId": "abc123",
  "hotels": [
    {
      "hotelId": "h_001",
      "name": "Park Hyatt Tokyo",
      "rating": 9.2,
      "star": 5,
      "pricePerNight": 450,
      "totalPrice": 1800,
      "currency": "USD",
      "packageId": "pkg_001",
      "refundability": "free_cancellation_until_2026-04-29"
    }
  ]
}
```

**Important** — Save the `sessionId`. The user will need it for any follow-up call (search-room, book-hotel).

## Presenting results to the user

Show a clean, scannable list — name, price/night, rating, and one notable feature. Don't dump the raw JSON. Example:

> Found 5 hotels in Tokyo for May 1–5:
> 1. **Park Hyatt Tokyo** — $450/night · 9.2/10 · Free cancellation until Apr 29
> 2. **Hotel Gracery Shinjuku** — $180/night · 8.5/10 · Free breakfast
> 3. ...
>
> Want to see room options for any of these, or shall I go ahead and book one?

Always offer a clear next step: see rooms (`search-room` skill) or book directly (`book-hotel` skill).

## Common errors

- `Network error` — Travel API unreachable. Tell the user and ask if they want to retry.
- `400 Bad Request` — Usually invalid dates (checkout before checkin, dates in the past). Re-validate inputs and re-prompt.
- `No hotels found` — Try a broader location or different dates.
