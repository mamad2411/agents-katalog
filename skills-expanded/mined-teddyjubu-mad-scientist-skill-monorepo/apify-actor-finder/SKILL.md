---
name: apify-actor-finder
description: "Finds the best Apify actor for a web scraping or data extraction task, runs it via the Apify API, and delivers the results as a CSV file. Use this skill whenever a user wants to scrape a website or extract data from any platform (e.g. Google Maps, Twitter/X, Instagram, Facebook, TikTok, LinkedIn, Amazon, real estate sites, etc.). This skill handles the full workflow: finding the actor, running it, and returning results."
---

# Apify Actor Finder & Executor

This skill finds the best Apify actor for the user's task, runs it, and saves the results to a CSV file.

**API Key:** stored in `~/.hermes/skills/apify-actor-finder/.env` as `APIFY_API_KEY`. The SKILL.md never contains raw keys.

---

## What This Skill Does

This skill Finds the best Apify actor for a web scraping or data extraction task, runs it via the Apify API, and delivers the results as a CSV file. Use this skill whenever a user wants to scrape a website or extract data from any platform (e.g. Google Maps, Twitter/X, Instagram, Facebook, TikTok, LinkedIn, Amazon, real estate sites, etc.). This skill handles the full workflow: finding the actor, running it, and returning results.

## Full Workflow

### Step 1 — Search for the best actor

Translate the user's request into a search term and run:

```bash
export $(cat ~/.hermes/skills/apify-actor-finder/.env | xargs)
python3 ~/.hermes/skills/apify-actor-finder/scripts/search_actors.py \
  "$APIFY_API_KEY" \
  "<search query>" --limit 5
```

| User Request | Search Query |
|---|---|
| Scrape Google Maps reviews | `Google Maps reviews scraper` |
| Get tweets about a topic | `Twitter X tweet scraper` |
| Scrape an Instagram profile | `Instagram scraper` |
| Scrape Facebook Ads Library | `Facebook Ads Library scraper` |
| Crawl a website for content | `website content crawler` |

Select the best actor by: (1) relevance, (2) highest `totalUsers`, (3) rating ≥ 4.0, (4) pricing. Note the `actor_id` (format: `username~actor-name`).

If results are poor, retry with `--sort popularity` or different keywords.

---

### Step 2 — Inspect the actor's required inputs

Run the info script to understand what the actor needs:

```bash
export $(cat ~/.hermes/skills/apify-actor-finder/.env | xargs)
python3 ~/.hermes/skills/apify-actor-finder/scripts/get_actor_info.py \
  "$APIFY_API_KEY" \
  "<actor_id>"
```

This prints the actor's description, README summary, and example input JSON. Read this output carefully to identify what information is required from the user.

---

### Step 3 — Ask the user for any missing information (REQUIRED before running)

**ALWAYS complete this step before running the actor.** Based on the actor's example input and README, determine what the user must provide and ask for it explicitly.

**Common required inputs by actor type:**

| Actor Type | What to Ask the User |
|---|---|
| URL-based scrapers (Instagram, TikTok, LinkedIn, website crawlers) | "Please provide the URL(s) you want to scrape." |
| Search-based scrapers (Google Maps, Twitter, Amazon) | "What search term, keyword, or location should I use?" |
| Profile scrapers | "Please provide the username(s) or profile URL(s)." |
| E-commerce scrapers | "Please provide the product URL(s) or search query." |
| Ad library scrapers | "What brand, keyword, or page name should I search for?" |

**Decision rule:**
- If the user's original request already contains the required information (e.g. they said "scrape coffee shops in Austin"), proceed directly to Step 4.
- If any required input is missing or ambiguous, **stop and ask the user** before proceeding. Do not guess or invent URLs or search terms.

**Example prompt to user:**
> "I've selected the **Instagram Scraper** for this task. To run it, I need the Instagram profile URL(s) or username(s) you want to scrape. Could you provide those?"

---

### Step 4 — Run the actor and download results as CSV

Once all required inputs are confirmed, construct the input JSON and run:

```bash
export $(cat ~/.hermes/skills/apify-actor-finder/.env | xargs)
python3 ~/.hermes/skills/apify-actor-finder/scripts/run_actor.py \
  "$APIFY_API_KEY" \
  "<actor_id>" \
  '<input_json>' \
  --output ~/<descriptive_filename>.csv \
  --timeout 300 \
  --max-items 100
```

Always include `"proxyConfig": {"useApifyProxy": true}` in the input JSON when the actor supports it — it significantly improves success rates.

**Examples:**

Google Maps — "coffee shops in Austin":
```bash
export $(cat ~/.hermes/skills/apify-actor-finder/.env | xargs)
python3 ~/.hermes/skills/apify-actor-finder/scripts/run_actor.py \
  "$APIFY_API_KEY" \
  "compass~crawler-google-places" \
  '{"searchStringsArray": ["coffee shops in Austin TX"], "maxCrawledPlacesPerSearch": 20, "proxyConfig": {"useApifyProxy": true}}' \
  --output ~/coffee_austin.csv --timeout 300 --max-items 100
```

Instagram — user-provided profile URL:
```bash
export $(cat ~/.hermes/skills/apify-actor-finder/.env | xargs)
python3 ~/.hermes/skills/apify-actor-finder/scripts/run_actor.py \
  "$APIFY_API_KEY" \
  "apify~instagram-scraper" \
  '{"directUrls": ["https://www.instagram.com/nasa/"], "resultsLimit": 50}' \
  --output ~/nasa_instagram.csv --timeout 300 --max-items 100
```

**Timeout guidance:**
- Social media / search results: 120–300s
- Google Maps / e-commerce: 300–600s
- Large datasets: increase `--timeout` accordingly

---

### Step 5 — Deliver the CSV to the user

Once the script prints `Saved N rows to: <path>`, attach the CSV file in the result message. Always include:
- Which actor was used and why it was selected
- How many rows were returned
- Direct link to the actor: `https://apify.com/<username>/<actor-name>`

---

## Error Handling

| Error | Fix |
|---|---|
| HTTP 400 on run | Input JSON does not match the actor's schema; re-check `get_actor_info.py` output and correct the fields |
| Run status `FAILED` | Try a different actor from Step 1 results, or reduce `--max-items` |
| 0 rows in CSV | Actor ran but found nothing; verify search terms with user or try a different actor |
| Timeout | Increase `--timeout` or reduce the scope of the input |
