---
name: search-room
description: Get room types and rate packages for a specific hotel. Use this skill after search-hotel when the user wants to explore room options, see different rate plans, compare meal plans (breakfast included vs not), check refundability, or pick a specific room before booking. Triggers on phrases like "show me the rooms at hotel X", "what room types are available", "I want a different rate plan", "is breakfast included".
license: MIT
---

# search-room

Get all room types and rate packages for one specific hotel. Use this when the user wants to explore alternatives beyond the default package returned by `search-hotel`.

## When to use

After the user has run `search-hotel` and wants to drill into a specific hotel:

- "Show me the rooms at Park Hyatt Tokyo"
- "What room types does hotel #2 have?"
- "I want a refundable rate"
- "Is there a package with breakfast included?"

Do NOT use this skill if the user hasn't already searched for hotels — run `search-hotel` first to obtain a `sessionId`.

## Prerequisites

You need both:

1. A `hotelId` from a prior `search-hotel` result
2. The `sessionId` from that same search

Both are in the JSON output of `search-hotel`. Don't ask the user — pull them from the previous tool output in your conversation.

## How to call

```bash
npx @tvl-justin/travel-cli@latest search-package \
  --hotel-id "<hotelId>" \
  --session-id "<sessionId>" \
  --checkin <YYYY-MM-DD> \
  --checkout <YYYY-MM-DD>
```

`--checkin` and `--checkout` are required by the CLI — reuse the dates from the prior `search-hotel` call.

### Optional overrides

If the user wants different dates or occupancy than the original search, pass them explicitly:

```bash
npx @tvl-justin/travel-cli@latest search-package \
  --hotel-id "h_001" \
  --session-id "abc123" \
  --checkin 2026-05-02 \
  --checkout 2026-05-06 \
  --rooms "2,8"
```

## Output

```json
{
  "sessionId": "abc123",
  "hotelId": "h_001",
  "hotelName": "Park Hyatt Tokyo",
  "options": [
    {
      "packageId": "pkg_a",
      "roomName": "Park Deluxe King",
      "mealType": "Breakfast included",
      "totalPriceAllRoomsUSD": 1800,
      "totalPricePerNightAllRoomsUSD": 450,
      "refundability": "Refundable",
      "nights": 4,
      "availableRooms": 3
    }
  ]
}
```

## Presenting to the user

List packages sorted by price. Highlight what differs (meal type, refundability). Example:

> Park Hyatt Tokyo — 4 nights, May 1–5:
> 1. **Park Deluxe King** — $450/night · Breakfast included · Free cancellation
> 2. **Park Deluxe King** — $400/night · Room only · Non-refundable
> 3. **Park Suite** — $720/night · Breakfast + dinner · Free cancellation
>
> Which one would you like to book?

Save each `packageId` — that's what `book-hotel` needs.

## Edge cases

- If `options` is empty, the hotel has no availability for those dates. Suggest alternatives (different dates or run `search-hotel` again).
- Some packages have a `cancellation.time_remaining_human` field. Surface it when refundability matters: "Free cancellation expires in 18 hours."
