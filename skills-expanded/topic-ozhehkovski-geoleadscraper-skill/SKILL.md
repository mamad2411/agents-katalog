---
name: collect-leads
description: Collect businesses (leads) from Google Maps, Yandex Maps or 2GIS for a query/location and analyze them. Use when the user wants to gather companies, places, restaurants, shops or leads from a map, optionally enrich them with website contacts (emails/phones/socials), and then filter, rank, summarize or export the results.
---

# Collect leads from maps

You collect businesses from maps via the **geoleadscraper** MCP server and then
analyze them for the user.

## Tools you have
- `collect_maps({ platform, query, limit?, extract_contacts?, timeout_seconds? })`
  — scrape businesses. `platform` is `google_maps` (default), `yandex_maps` or
  `gis`. Put the **location in the query** (e.g. `"dentists in Berlin"`).
  Set `extract_contacts: true` to also scrape website emails/phones/socials.
- `extract_website_contacts({ urls })` — scrape contacts from specific websites.
- `list_jobs()` — inspect recent collection jobs.

## How to handle a request
1. **Clarify** only if the query or location is missing. Otherwise act.
2. Call `collect_maps` with a query that includes the location. Pick a sensible
   `limit` (default 50–100; raise it if the user wants "all"/"as many as possible").
   Use `extract_contacts: true` when the user wants emails/phones/socials.
3. The call blocks while the extension scrapes (tens of seconds). If it returns a
   "timed out" / "make sure Chrome is open" error, tell the user to:
   - start the backend, and
   - keep Chrome open with the extension installed and its **Backend URL** set.
4. **Analyze** the returned `data` array per the user's intent — rank by rating,
   filter (open now, has website, min reviews), deduplicate, segment, or summarize.
5. **Deliver** results clearly. If the user wants a file, write a CSV/Markdown
   table; if they want contacts, surface email/phone/socials.

## Notes
- Each record may include: `title`, `address`, `phone`, `website`, `rating`,
  `review_count`, `categories`, `latitude`, `longitude`, and (with
  `extract_contacts`) `email`, `phones`, `socials`.
- Results depend on what the map publicly shows; missing fields are normal.
- Use responsibly and within the maps' terms of service and applicable laws.
