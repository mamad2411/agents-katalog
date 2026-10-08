---
name: url-article-summarizer
description: "Summarize any article or webpage from a URL. Use web_fetch for simple pages; use Apify URL-to-article summarizer or Firecrawl when configured for best results."
metadata: {}
---

# URL / Article Summarizer Skill

Summarize an article or webpage from a URL. Use **web_fetch** for public pages when that's enough; use an external API (Apify or Firecrawl) when the user needs clean extraction or the site is heavy/dynamic.

## When to use

- User says "summarize this link", "what does this article say?", "brief this URL", or pastes an article URL.
- Researcher or Koko needs a short, accurate summary of a page before reporting or deciding.

## Option 1: web_fetch (no API key)

For simple, static pages:

1. Use **web_fetch** with the URL.
2. If the response is HTML, extract the main text (e.g. look for `<article>`, `<main>`, or strip tags and take the largest text block).
3. Summarize in 3–5 bullets or a short paragraph.

If the page is behind JS, paywall, or returns little text, use Option 2.

## Option 2: Apify "URL to Article Summarizer" (when a tool exists)

When a dedicated tool (e.g. `apify_run`) is available and configured with an Apify token in `~/.picoclaw/config.json`, use it to run the "URL to Article Summarizer" actor. The **URL to Article Summarizer** actor extracts and summarizes in one call.

1. Use the tool with the actor ID and input `{ "url": "<user's URL>" }`.
2. If you must call the REST API directly (e.g. from a script), you would run the actor via:
   - Actor ID: look up "URL to Article Summarizer" or "any-website-url-to-article-summarizer" on Apify.
   - Input: `{ "url": "<user's URL>" }`.
3. Poll or wait for run completion, then read the dataset/output for the summary.
4. Return the summary to the user.

Example (adapt actor ID and endpoint from Apify docs):

```text
POST https://api.apify.com/v2/acts/ACTOR_ID/runs?token=APIFY_TOKEN
Body: {"url": "https://example.com/article"}
```

Then get the run output from the run URL or dataset.

## Option 3: Firecrawl (when a tool exists)

If a Firecrawl tool (e.g. `firecrawl_scrape`) is available and configured, use it. Otherwise Firecrawl's scrape endpoint (e.g. `POST https://api.firecrawl.dev/v1/scrape` with `{"url": "..."}` and optionally `"formats": ["markdown"]`). Then summarize the returned content yourself or use a follow-up summarization step.

## Summary

- Prefer **web_fetch** for quick, public pages.
- Use **Apify** or **Firecrawl** when a dedicated tool is configured for reliable extraction or complex pages. See docs/INTEGRATIONS_OPTIONAL_CONFIG.md.
