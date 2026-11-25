---
name: price-check
description: "Compares the prices or content a page shows in different countries using SoftGlaze Browser profiles with proxies in those countries (market research). Use when the user asks to compare prices or offers by country."
argument-hint: "<url> <country codes, comma separated>"
arguments: [url, countries]
---

# Compare prices by country

Follow the softglaze-browser skill: read `softglaze://memory/workspace` and
`softglaze://guide/how-softglaze-works` first and follow them. Anything that changes something asks
the user for approval in the SoftGlaze app, so tell them what you are about to change and why first.
Stop every profile you start when you are done.

Page: $url. Countries: $countries (two-letter codes). If either is empty, ask the user.

Read only: do not log in, add to cart, or submit anything, and visit the page once per country.

1. For each country pick a profile with a proxy in that country (check_proxy confirms the exit
   country).
2. Start it, page_navigate to the URL, wait for the price to appear (page_wait_for), and read it with
   page_extract_text (pass a selector for the price area if you can find one with page_snapshot).
3. Record: price, currency, tax or shipping notes, availability, and any country-specific offer.
4. Report a table with the price in each currency and, if the user asks, converted to one currency
   (say which rate and date you used).
5. Stop every profile you started. Respect the site's terms; if it forbids automated access, tell
   the user instead of continuing.
