# ScraperCity - B2B Lead Generation

## START HERE (no API key needed)
Call the `start_here` tool first (API: `GET https://app.scrapercity.com/api/v1/start?query=...`). Give it who your user wants to reach, what they sell, their website, or an exact order. With no key it answers with a guided tour: what ScraperCity is, how to sign up and get a key, the plans and the trial with their live terms, and real searches with live counts. With a key it plans for the account and returns `next_call`, the exact call that pulls the records.

**The trial, plainly:** The trial is real usage, not a demo or a free tier: $5 of credit for 7 days that works on every tool and database at the normal prices, so you can pull real records on day one and judge the data. A card is required at signup. When the 7 days end, the plan picked at signup starts; cancel before then from billing and nothing more is charged. If the credit runs out sooner, database pulls wait (nothing is charged for them); a scraper run that goes past the credit starts the plan early. Planning searches and checking counts are free. start_here returns the live terms.

## Setup
```bash
export SCRAPERCITY_API_KEY="your_key"   # get from app.scrapercity.com/dashboard/api-docs
npx scrapercity wallet                   # verify balance
```
Writing code instead? Use an SDK with the same tools as the MCP server: `npm install scrapercity` (`import { callTool } from 'scrapercity'`) or `pip install scrapercity` (`ScraperCity().call_tool(...)`, plus LangChain and OpenAI Agents tools). Guide: https://scrapercity.com/sdk

## Core Pattern
Every scraper follows: **start → poll → download**
```
POST /api/v1/scrape/{slug}  →  { runId }
GET  /api/v1/scrape/status/{runId}  →  { status, handled, outputUrl }
GET  /api/downloads/{runId}  →  CSV file
```
Auth: `Authorization: Bearer $SCRAPERCITY_API_KEY` on all requests.

## Pricing (auto-generated from the live catalog — do not edit)

<!-- GENERATED:pricing:start -->
| Tool | Endpoint | Price |
|------|----------|-------|
| `scrape_apollo` | /api/v1/scrape/apollo | $0.0039 per lead |
| `scrape_website_finder` | /api/v1/scrape/website-finder | $0.0499 per contact found |
| `find_people` | /api/v1/scrape/skip-trace | $0.0199 per result (searches with 0 matches are billed as 1 result) |
| `scrape_distress_list` | /api/v1/scrape/distress-list | $0.05 per property |
| `validate_emails` | /api/v1/scrape/email-validator | $0.0017 per email |
| `scrape_maps` | /api/v1/scrape/maps | $0.0099 per business |
| `scrape_airbnb` | /api/v1/scrape/airbnb-email | $0.019 per result ($19.00 per 1,000) |
| `scrape_bizbuysell` | /api/v1/scrape/bizbuysell-scraper | $0.0099 per listing |
| `scrape_crexi` | /api/v1/scrape/crexi-scraper | $0.029 per property |
| `scrape_angi` | /api/v1/scrape/angi-angies-list-scraper | $0.0099 per listing |
| `scrape_yelp` | /api/v1/scrape/yelp-scraper | $0.0099 per result |
| `scrape_zillow_agents` | /api/v1/scrape/zillow-agents | $0.029 per agent |
| `scrape_property_lookup` | /api/v1/scrape/property-lookup | $0.15 per property (+$0.10 for owner contact) |
| `search_criminal_records` | /api/v1/scrape/criminal-records | $1.00 per search (only charged if records found) |
| `scrape_store_leads` | /api/v1/scrape/store-leads | $0.0039 per lead |
| `scrape_builtwith` | /api/v1/scrape/techstack | $4.99 per technology |
| `scrape_signals` | /api/v1/scrape/signals | $0.0094 per company running ads, $0.0009 per website per platform checked, $0.0043 per company hiring; minimum charge per search |
| `scrape_ucc_filings` | /api/v1/scrape/ucc-filings | $0.0028 per filing |
| `scrape_facebook_pages` | /api/v1/scrape/facebook-pages | $0.0012 per page from page links, $0.0028 per page from a search |
| `scrape_website_contacts` | /api/v1/scrape/website-contacts | $0.004 per website with an email or phone found |
| `find_job_posts` | /api/v1/scrape/job-scraper | $0.0009 per job post, decision maker included; minimum charge per search |
| `scrape_instagram_leads` | /api/v1/scrape/instagram-leads | $0.0023 per profile found by keyword or hashtag, $0.0006 per profile from your own list |
| `find_linkedin_post_engagers` | /api/v1/scrape/linkedin-post-engagers | $0.004 per person |
| `find_emails` | /api/v1/scrape/email-finder | $0.05 per email found (FREE if not found) |
| `find_mobiles` | /api/v1/scrape/mobile-finder | $0.25 per number found (FREE if not found) |
<!-- GENERATED:pricing:end -->

## All Scrapers (POST to /api/v1/scrape/{slug})

| Slug | Input | Cost | Speed |
|------|-------|------|-------|
| `apollo` | `{url, count, fileName}` | $0.0039/lead | usually 15-30 min (use webhook) |
| `maps` | `{searchStringsArray:["query"], locationQuery, maxCrawledPlacesPerSearch}` | $0.01/place | 5-30 min |
| `email-validator` | `{emails:["a@b.com"]}` | $0.0036/email | 1-10 min |
| `email-finder` | `{contacts:[{first_name,last_name,domain}], autoValidateEmails, autoFindMobiles}` | $0.05/contact | 1-10 min |
| `mobile-finder` | `{inputs:["linkedin.com/in/x","email@co.com"]}` | $0.25/input | 1-5 min |
| `people-finder` | `{name:[], email:[], phone_number:[], street_citystatezip:[], max_results}` | $0.02/result | 2-10 min |
| `store-leads` | `{platform, countryCode, totalLeads, emails:true, phones:true}` | $0.0039/lead | instant |
| `builtwith` | `{technology}` | $4.99 flat | 1-5 min |
| `criminal-records` | `{name, state, dob}` | $1.00 if found | 2-5 min |
| `airbnb-email` | `{mode:"city", city:["Miami, FL"], maxResults:100}` | $0.0001/listing | 10-30 min |
| `youtube-email` | `{channels:["@Handle","https://youtube.com/@X"]}` | per channel | 5-15 min |
| `website-finder` | `{domains:["acme.com"], jobTitle:"CEO"}` | per domain | 5-15 min |
| `yelp-scraper` | `{searchTerms:["plumbers"], locations:["Denver, CO"], searchLimit:10}` | $0.01/listing | 5-15 min |
| `angi-angies-list-scraper` | `{keyword, zipCodes:["80202"], maxItems:100}` | $0.01/listing | 5-15 min |
| `zillow-agents` | `{location:"Denver, CO", specialty, searchLimit:10}` | per agent | 5-15 min |
| `bizbuysell-scraper` | `{startUrls:["<search-url>"], maxItems:100}` | $0.01/listing | 5-15 min |
| `crexi-scraper` | `{startUrls:["<search-url>"]}` | $0.029/listing | 5-15 min |
| `property-lookup` | `{addresses:["123 Main St, City, ST 12345"], includeOwnerContact:false}` | $0.15/address | 2-10 min |

## ⚠ Apollo Delivery
Apollo scrapes usually take **15-30 minutes** to deliver; some lists take longer. Do NOT poll in a loop.
- Set up a webhook at `app.scrapercity.com/dashboard/webhooks`
- Webhook fires when results are ready with `{runId, fileName, leadsCount}`
- If you must poll, start after 15 minutes and check every few minutes, not in a tight loop

## Other Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/v1/wallet` | Balance, plan, billing |
| GET | `/api/v1/runs?hours=24&limit=50` | Recent runs |
| POST | `/api/v1/scrape/cancel/{runId}` | Cancel running job |
| GET | `/api/v1/scrape/logs/{runId}` | Run logs |
| GET | `/api/v1/apollo-status` | Apollo service health: `{status: "url-based" or "legacy", message, timestamp}` |
| GET | `/api/v1/database/leads?title=CTO&country=United%20States&hasEmail=true&limit=100` | Lead DB (included on $149/mo and up, 100k new leads/day; on a trial or $49 each new lead is paid from credits, see `billing` in the answer). Optional: `excludeDelivered=true` (only leads you don't have yet), `after=0` then `pagination.next_after` (cursor paging), `replaceLeftContacts=true` (adds `replacement.run_id`: a run that swaps contacts who have left for the person in that role now; $0.02 per contact replaced, free on the $649 plan). Company filters: `keywords`, `revenueMin`/`revenueMax`, `companyCountry`/`companyState`/`companyCity`. Exclusions: `notTitle`, `notKeywords`, `notIndustry`. Website technologies: `technologies` (any of), `technologiesAll` (all of), `notTechnologies` (none of). `url=<people-search URL>` searches with that URL's filters. POST with a JSON body takes the same parameters (use it for a long `url`) |
| GET | `/api/v1/database/local-businesses?category=Dentist&country=US&hasContact=true&limit=100` | Local biz DB (included on $149/mo and up, 100k new businesses/day; per record from credits below it). Search like Google Maps: `keyword` (repeat; names and categories, any keyword) and `location` (repeat; cities, states, countries, postal codes), with `searched_as` in the response and `lead_database` when nothing is found but the Lead Database has 100+ people. Filters: `category`, `country`, `state`, `city`, `postalCode`, `query`, `minRating`/`maxRating`, `minReviews`/`maxReviews`, `hasEmail`, `hasPhone`, `hasWebsite`, `hasContact` (only businesses with a named contact person), `maxLocations` (skip businesses with over that many locations: businesses with the same website; skips chains), `title` (business name), `box=minLat,minLng,maxLat,maxLng` (a map area). Exclusions: `notCategory`. `url=<Google Maps search URL>` searches with that URL's keyword and place. POST with a JSON body takes the same parameters (use it for a long `url`). Same optional `excludeDelivered` / `after`, and `replaceLeftContacts=true` (adds `replacement.run_id`: a run that swaps contact people who have left for the person in that role now; $0.02 per contact replaced, free on the $649 plan) |
| GET | `/api/v1/database/ecommerce?...` | Ecommerce DB (included on $149/mo and up; per record from credits below it). Same optional `excludeDelivered` / `after`, and `replaceLeftContacts=true` (adds `replacement.run_id`: a run that swaps store contact people who have left for the person in that role now; $0.02 per contact replaced, free on the $649 plan). Technologies: `technologies` (any of), `technologiesAll` (all of), `notTechnologies` (none of) |
| POST | `/api/v1/database/plan` | Free on every plan, trials included (GET with `?query=` also works). `{ "query": "dentists in Austin", "database"?: "leads" or "local" or "ecommerce" }` -> ready-to-run searches: `{ targeting, searches: [{ database, name, filters, count, apiEndpoint, apiParams, link }] }`. Send `apiParams` as they are to `/api/v1/<apiEndpoint>` |
| POST | `/api/v1/autoleads/lookalike` | Every plan, $0.01 per site read. `{ "domains": ["acme.com", "mike@globex.com", ...] }` (websites or work emails, at least 3 company sites) -> 202 `{ job }`. Then GET `/api/v1/autoleads/lookalike?id=<job id>` until `job.status` is `done`: `job.groups` = `[{ name, description, sites, database, filters, count, tool }]`. Send a group's `filters` to that database's endpoint. 402 = balance under $0.01 x every site; 409 = a job is already running. Add `&format=csv` to the GET for every site as a CSV (no extra charge) |

## Status Values
`RUNNING` → `SUCCEEDED` or `FAILED` or `CANCELLED`

## Error Codes
- `401` - bad or missing API key
- `402` - insufficient balance (check wallet first)
- `403` - account cancelled or charge processing
- `409` - duplicate request (same search submitted recently)
- `429` - rate limited / duplicate within 30s
- `503` - service temporarily unavailable

## CLI Shorthand
```bash
scrapercity maps -q "plumbers" -l "Denver, CO" --limit 500
scrapercity yelp -q "dentists" -l "Austin, TX"
scrapercity airbnb --city "Miami, FL" --limit 200
scrapercity youtube-email @MrBeast @PewDiePie
scrapercity website-finder acme.com example.com --title "CEO"
scrapercity angi -q "electricians" --zips "90210,90211"
scrapercity zillow-agents -l "Denver, CO"
scrapercity bizbuysell <bizbuysell-search-url>
scrapercity crexi <crexi-search-url>
scrapercity property-lookup "123 Main St, Denver, CO 80202" --owner-contact
scrapercity poll <runId>          # polls until done
scrapercity download <runId>      # saves CSV
```

## Tips
- Always check `wallet` before large scrapes to avoid 402 errors
- Apollo URL must be from apollo.io People search - other pages rejected
- Maps: split large metro areas into sub-cities for better coverage
- Email validator: dedupes automatically, only charges for unique emails
- Store leads: zero COGS (cached DB), instant results
- Yelp/Angi: can also pass directUrls instead of search terms
- YouTube: accepts both @handles and full channel URLs
- Website finder: domains only, no https:// prefix needed
- Property lookup: full address with city, state, zip required
- Downloads return CSV with all available fields
- Before sending outreach to leads from any database: every record carries `email_check_status` (our checker: valid, valid_catch_all, invalid, unknown, not_checked); send ONLY to `valid` emails checked in the last 30 days (`email_checked_on`); put every other email through `validate_emails` and send only to the ones it returns valid. For people (Lead Database), set `replaceLeftContacts=true` and send the CSV from that run (`check_run_status`, then `download_results`): every email is checked and people who have left are swapped for the person in that role now. At minimum, run the emails through `validate_emails` and send only to the valid ones
