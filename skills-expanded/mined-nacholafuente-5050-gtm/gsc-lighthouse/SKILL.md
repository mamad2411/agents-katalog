---
name: gsc-lighthouse
description: Pull Google Search Console health (sitemap status, indexing coverage, 28-day search analytics) for a verified GSC property, then run Lighthouse via the PageSpeed Insights API on the top 10 pages by clicks. Outputs a single combined report grouped by theme, surfacing real problems and skipping the noise. Use when the user says "/gsc-lighthouse", "search console check", "lighthouse audit", "indexing status", or "is the site healthy in Google's eyes". One-shot, no warehouse, no cron.
---

# GSC + Lighthouse health check

Pulls Google Search Console (sitemap status, per-URL index coverage, 28-day search analytics) and runs Lighthouse via the PageSpeed Insights API on the top 10 pages by clicks. Produces a single report a non-technical person can read.

The point: most "SEO audit" tools throw a hundred warnings at you. This one tells you what's actually broken, calibrates against false positives, and groups fixes by theme so you can ship a single PR instead of a hundred.

## Step 1: Ask the user 2 questions

1. **What's your GSC property?** (the verified site in Search Console)
   - `sc-domain:example.com`, Domain property (covers all subdomains and protocols)
   - `https://example.com/`, URL-prefix property (one specific protocol + host)
   - If they don't know, link them to https://search.google.com/search-console and ask them to copy the property URL from the sidebar.

2. **Do you have a `PAGESPEED_API_KEY` configured?** (`.env` or shell env)
   - `yes` → Lighthouse step runs.
   - `no / skip` → Lighthouse step is skipped, GSC report still ships. (See `README.md` "Setup: PSI API key" for the 3-command setup, ~30 seconds.)

That's it. No other config needed.

## Step 2: Run the audit

```bash
cd skills/gsc-lighthouse
python audit.py --site "sc-domain:example.com"
```

Add `--no-lighthouse` to skip the PSI step. Add `--top N` to audit a different number of pages (default 10).

The script writes a JSON dump to `./out/audit-<date>.json` and prints the structured report to stdout.

## Step 3: Report

Read `audit.py`'s stdout straight back to the user. Don't reformat unless they ask; the script's output is already structured for direct read.

If the user wants a TL;DR, summarize in this shape:

```
## GSC + Lighthouse: {today}

Sitemap:        {N URLs, errors/warnings}
Indexing:       {indexed} / {total}
Search (28d):   {clicks}, {±%} vs prior 28d
Lighthouse:     median perf {score}, median LCP {seconds}

Top 3 fixes (impact-ordered):
1. {theme}, {N pages affected}, est. {savings}
2. ...
3. ...

Bottom line: {one sentence}
```

## Calibration: don't cry wolf

Apply these mental filters before flagging anything as a "problem":

- **Sitemap submitted < 7 days ago + many "URL is unknown to Google"** → normal queue, not a problem.
- **0 indexed in sitemap stats panel on a Domain property** → known GSC reporting quirk, not real. Trust per-URL inspection results, not the panel counter.
- **"Discovered - currently not indexed"** → only an issue if it's been > 14 days since submission. Younger pages are just queued.
- **Single-run Lighthouse perf swing of ±10 points** → variance, not regression. Re-run after warming the origin.
- **TBT spike > 300ms with stable LCP/FCP** → cold-start signature on serverless platforms (Cloud Run, Lambda@Edge). Warm with a curl loop, re-run.
- **Lab Lighthouse green but field CWV (CrUX) yellow/red** → trust field data. Lab is synthetic; CrUX is what real users experience and what Google ranks on.

Real problems worth flagging:
- Sitemap errors > 0 or warnings > 0
- Canonical mismatches (Google chose a different canonical than declared)
- Pages stuck "Crawled - currently not indexed", Google decided not to index, quality signal
- Pages stuck "Discovered - currently not indexed" > 14 days
- Soft 404s on pages that should be real content
- Sudden traffic drops > 30% week-over-week
- Sitemap URLs returning 404 or redirecting
- LCP > 4s on top traffic pages (poor band, ranking penalty)
- Console errors from third-party tags

## Output style guide

When you write the report (Step 3), follow these rules:

- **Group fixes by theme, not by page.** "10 pages need image optimization" beats listing the same fix 10 times.
- **Sort by impact × ease.** A 3KB CSS purge that saves 200ms across all pages beats a 1MB image swap on one low-traffic page.
- **No emoji unless something is genuinely broken.** This is a diagnostic report, not a slide.
- **Be specific in ms / KB savings** when PSI gives them. "Reduce unused JS (-1050ms)" beats "Reduce unused JavaScript".
- **If nothing is broken, say so directly.** Don't pad.

## Setup: PSI API key

Anonymous PageSpeed Insights API hits get rate-limited fast (a single IP shares a small daily quota). With a free API key, the limit is 25,000/day, far more than you'll ever need.

```bash
# 1. Enable the API on a GCP project (any project, even a fresh one)
gcloud services enable pagespeedonline.googleapis.com --project=YOUR_GCP_PROJECT

# 2. Create the API key
gcloud beta services api-keys create \
  --display-name="PageSpeed Insights" \
  --project=YOUR_GCP_PROJECT \
  --format='value(response.keyString)'

# 3. (Recommended) Restrict the key to PSI-only via the GCP Console:
#    https://console.cloud.google.com/apis/credentials → click the key → API restrictions
#    → "Restrict key" → select "PageSpeed Insights API" only.

# 4. Add to .env in the repo root or wherever you run the script
echo "PAGESPEED_API_KEY=<paste-keyString>" >> .env
```

## Setup: GSC auth (Application Default Credentials)

Google Search Console doesn't accept service-account emails on Domain properties (known limitation). Use ADC bound to your verified Google Account:

```bash
gcloud auth application-default login --scopes=\
https://www.googleapis.com/auth/webmasters.readonly,\
https://www.googleapis.com/auth/webmasters,\
openid,\
https://www.googleapis.com/auth/userinfo.email
```

Sign in with the Google Account that owns the GSC property. Credentials are saved to `~/.config/gcloud/application_default_credentials.json` and any Python script using `google.auth.default()` picks them up automatically.

If a 401 surfaces during the run, the script will print a clear "re-auth needed" hint with the exact command above.
