---
name: geocode-addresses
description: Turn addresses into coordinates or coordinates into addresses without sending them to an online service. Use when the user wants to geocode, reverse geocode, validate or map addresses, enrich a CSV or list with latitude and longitude, or asks for a geocoder that works offline or needs no API key.
---

Use the `gridpin` MCP tools. They run on this computer, and only `download_sheet` uses the network.

1. Work out which country the addresses are in. If they span several countries, group them and repeat these steps for each. Call `list_countries` to see what is covered, the size of each country's file and whether it is already downloaded. If the country is not covered, say so instead of guessing with another country's file.
2. If the file is missing, tell the user its size, then call `download_sheet`. The largest file is over 1 GB and can outlast a client's tool timeout. If that happens, have the user run `uvx --from gridpin-mcp==0.7.0 gridpin-fetch <country>` in a terminal, then call the tool again.
3. Call `geocode` for one address, `batch` for up to 1000 addresses per call, and `reverse` for coordinates. For a longer list, split it into chunks of 1000 and keep the input order. Pass each address as the person wrote it, including city and postcode when known.

Read the result before reporting it:

- `precision` says what the answer points to. `house` is the address itself, `interp` is estimated along the street, and `street` and `city` are only approximate. Report the level with the coordinates, and never present a street or city answer as the exact address.
- `weak: true` means the engine itself says the answer needs checking. List these rows for the user rather than dropping the flag.
- An empty result means no answer. Count and report these rows. Do not fill them in from memory.
- `reverse` is approximate: each result carries `distance_m` from the given point. Report that distance.
- `kind` (engine 0.9 and later) says what the call came to. `clarify`: the street exists in several far-apart places and the query named none; ask the user which one (`clarify.options`, each with a label) and call `geocode` again with that city or region added. Do not pick one yourself. `none`: no answer, and `reason` says why: `no_street` (check the spelling), `no_house` (the street is there, the number is not), `city_unknown`, `outside_sheet` (wrong country file), `unparsed` (not an address). Tell the user what to add.
- A query can also be a coordinate (decimal, degrees-minutes-seconds, UTM, MGRS, Plus Code), a crossing ("Main St & Elm St, Springfield": precision `intersection`) or a PO box (the answer is its town, `weak`).
- `extras` asks for more per result: `h3`, `geohash`, `placekey`, `codes` (Plus Code, MGRS), `street_point`, `links` (map links to check by eye), `provenance` (the file's source, date and licence), `place` (the address as a person writes it).

When you report results to the user, show them as a short table (the address, `precision`, the coordinates, and "weak" where it applies) rather than raw JSON; keep the JSON when a program or a file is the consumer, or when the user asks for the raw answer.

When you finish a list, give the counts by `precision`, plus the weak and empty counts, so the user can judge the result. Quality differs by country and by how messy the input is; measured results, including where other geocoders do better, are at https://gridpin.dev/bench.
