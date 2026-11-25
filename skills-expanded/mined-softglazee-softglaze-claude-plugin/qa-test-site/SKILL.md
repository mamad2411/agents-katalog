---
name: qa-test-site
description: "Opens the user's own site or ad landing page in SoftGlaze Browser profiles from several countries and reports the differences (QA, geo testing, ad verification). Use when the user wants to see how their site or ad looks from other countries."
argument-hint: "<url> <country codes, comma separated>"
arguments: [url, countries]
---

# Test a site from several countries

Follow the softglaze-browser skill: read `softglaze://memory/workspace` and
`softglaze://guide/how-softglaze-works` first and follow them. Anything that changes something asks
the user for approval in the SoftGlaze app, so tell them what you are about to change and why first.
Stop every profile you start when you are done.

Page: $url. Countries: $countries (two-letter codes). If either is empty, ask the user.

This is QA of the user's own site or ad, so read only: do not log in, buy, submit forms or click ads.

1. For each country, find a profile whose proxy is in that country (list_profiles and list_proxies;
   the proxy's country must match). If a country has none, tell the user and skip it.
2. Check each chosen profile's proxy with check_proxy so the exit country is confirmed today.
3. Start the profiles a few at a time (start_profile). In each, page_navigate to the URL, then take
   page_screenshot and page_extract_text.
4. Compare: language, currency, prices, banners, consent notices, redirects (final URL), blocked or
   missing content, and load errors.
5. Report a table per country and a list of the differences that matter, with screenshots
   referenced by country.
6. Stop every profile you started.
