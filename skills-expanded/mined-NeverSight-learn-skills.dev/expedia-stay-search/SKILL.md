---
name: expedia-stay-search
description: Use this skill when the user wants to search for hotels on Expedia by destination and dates, find available stays, check hotel pricing, or get a Hotel-Search URL. Triggers on "find a hotel", "search Expedia", "look up hotels in <city>", "book a stay", "hotel availability", or any request that implies Expedia stay search. Requires an authenticated Tabby browser session for the `expedia` profile; not usable as a generic hotel search tool for sites other than Expedia.
---

# Expedia Stay Search

Search Expedia for available hotels by destination and dates using an authenticated Tabby browser session. Returns a Hotel-Search URL and extracted listings (name, nightly price, total price, rating, reviews, refundable flag, link).

This skill drives the real Expedia site inside a Tabby-managed browser via CDP (Chrome DevTools Protocol) instead of a Python HTTP client. That is intentional: Expedia sits behind Akamai, which blocks non-browser TLS fingerprints. Do not try to port the operations to `httpx` or `requests` — you will get 429 Too Many Requests.

## Prerequisites

Before invoking any operation:

1. **Tabby is running with the `expedia` profile.** Verify with `.venv/bin/python cli/main.py tabby session ensure --profile expedia` from the `noui/` directory. If that command fails, the user needs to re-run `/noui-record-login` for the `expedia` profile first — do not try to proceed without a live session.
2. **`PROFILE_SLUG=expedia` is exported** in the shell that runs the operation. This is the slug, not the DB UUID. The runtime reads it (or the `--profile-slug` flag) to fetch live credentials from Tabby.
3. **The Expedia profile is ACTIVE.** Check with the Tabby admin endpoint if in doubt — a STAGING profile returns empty credentials and the operation fails with "Tabby returned empty credentials for profile 'expedia'".

## Operations

### `search_hotels`

Search Expedia for hotels in a destination, on given check-in / check-out dates, for a given number of guests and rooms. Returns up to 25 listings extracted from the first page of results.

**When to use:** The user asks for hotel availability, prices, or a link to Expedia results for a specific city and date range.

**Command:**

```bash
python operations/search_hotels.py \
  --destination "Paris" \
  --check-in 2026-05-01 \
  --check-out 2026-05-04 \
  --guests 2 \
  --rooms 1
```

Prints a JSON object to stdout on success. Exits non-zero on failure with a diagnostic on stderr.

**Arguments:**

| Name | Type | Required | Default | Notes |
|---|---|---|---|---|
| `--destination` | string | yes | — | City or place name. Expedia typeahead resolves it to a region ID. |
| `--check-in` | string | yes | — | `YYYY-MM-DD`. |
| `--check-out` | string | yes | — | `YYYY-MM-DD`. Must be after `--check-in`. |
| `--guests` | integer | no | `2` | Adult guests. |
| `--rooms` | integer | no | `1` | Number of rooms. |
| `--profile-slug` | string | no | `$PROFILE_SLUG` or `expedia` | Tabby profile slug. Override only if testing against a non-default profile. |

**Output shape:**

```json
{
  "search_url": "https://www.expedia.com/Hotel-Search?...",
  "destination": "Paris, France",
  "region_id": "178279",
  "check_in": "2026-05-01",
  "check_out": "2026-05-04",
  "guests": 2,
  "rooms": 1,
  "listings_count": 25,
  "listings": [
    {
      "name": "Hotel Le Example",
      "price_per_night": "$245",
      "price_total": "$735",
      "rating": "8.4/10",
      "rating_label": "Very Good",
      "reviews_count": "1,234",
      "refundable": true,
      "url": "https://www.expedia.com/..."
    }
  ]
}
```

## Troubleshooting

- **`No Expedia browser session found. Is Tabby running?`** — no Tabby CDP target found at `localhost:9222` matching `expedia.com`. Run `tabby session ensure --profile expedia` and retry.
- **`Expedia API returned 429: ...`** — Akamai is rate-limiting even through the browser. This is rare via CDP; if it happens repeatedly the Tabby session may need to rotate IPs or the profile needs re-recording.
- **Empty `listings`, non-zero `listings_count`** — Expedia changed its DOM. The DOM-scrape selectors in `search_hotels.py` (`[data-stid="lodging-card-responsive"]`) need updating. Report to the NoUI maintainers; do not guess at selectors.
- **`auth_plan.json missing profile_slug`** — this skill was mis-installed. The `auth_plan.json` file sitting next to `noui_runtime/` must have `profile_slug: "expedia"`. Reinstall the skill.

## Notes

- This skill performs **DOM scraping** after navigation, not pure API calls. Results reflect what Expedia renders to a logged-in user, which may include personalized pricing.
- There is a ~7-second wait for the SPA to render results; a single invocation can take 10–15 seconds end-to-end.
- This skill is the reference sample for the NoUI skills-generation pipeline. Generated skills from real recordings will share the same layout (`SKILL.md`, `operations/`, `noui_runtime/auth.py`, `manifest.json`, `auth_plan.json`) but will vary in operation count and complexity.
