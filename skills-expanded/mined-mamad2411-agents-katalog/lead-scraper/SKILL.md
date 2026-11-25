---
name: lead-scraper
description: Build a targeted lead list — define the ideal prospect profile, identify the best free and paid sources to find them, produce a structured list format, and provide outreach-ready data organization. Use when the user needs to find potential clients, customers, or partners for outreach: defines who to target, where to find them, what data to collect, and how to organize it for use in a CRM or outreach sequence. Source: @the.wealth.lab "6 Favorite Claude Skills That Automate Almost Anything."
---

# Lead Scraper

Source: @the.wealth.lab "6 Favorite Claude Skills That Automate Almost Anything."

> Find targeted leads automatically, organize the list, collect business info, and produce outreach-ready data — without paying for an enterprise data platform.

## What this skill produces

- **Ideal Customer Profile (ICP)** distilled from the user's business description
- **Sourcing strategy**: 3–5 channels ranked by quality and effort for their specific ICP
- **Search queries and filters** for each channel — paste-and-run, not "go search for people"
- **List structure**: column schema for a spreadsheet or Airtable base
- **Enrichment checklist**: which fields to collect per lead and how to fill gaps
- **First-touch qualification**: 2–3 signals to check before adding a lead to the outreach queue

## Lead sources by ICP type

| ICP type | Best free sources | Best paid / semi-paid |
|---|---|---|
| B2B SaaS founders | LinkedIn, Twitter/X, ProductHunt, Indie Hackers | Apollo.io (free tier), Hunter.io |
| Local businesses | Google Maps, Yelp, Facebook Pages | D7 Lead Finder, Outscraper |
| Content creators | YouTube channel search, TikTok, Instagram, Substack | SparkToro, Modash |
| E-commerce stores | Shopify store directories, MyIP.ms, BuiltWith | SimilarWeb, Jungle Scout |
| Agencies / freelancers | LinkedIn, Clutch.co, UpWork profiles, G2 | Apollo.io, Clearbit |
| Newsletter operators | Substack Leaderboard, beehiiv discover, Twitter/X bio search | SparkToro |

## Copy-paste prompt to use

```
You are a B2B lead generation expert who helps service businesses build targeted prospect lists without enterprise data tools.

My offer: [DESCRIBE YOUR SERVICE OR PRODUCT IN ONE SENTENCE]
My ideal client: [BE SPECIFIC — job title, company type, industry, location if relevant, revenue size if relevant]
What problem do I solve for them: [ONE SENTENCE]
I currently have: [NO LIST / A PARTIAL LIST OF N CONTACTS / AN EXISTING CRM]
Budget for tools: [FREE ONLY / UP TO $X/MONTH]

Do the following:

1. Write my Ideal Customer Profile (ICP) in 5 bullet points — be specific, not broad
2. Name the 3 best sources to find my ICP and rank them by signal quality
3. Give me the exact search queries, filters, or navigation paths to use in each source — copy-paste ready
4. Design the lead list spreadsheet schema: column names, what data goes in each, which are required vs. nice-to-have
5. Give me a 5-point enrichment checklist: what to research about each lead before reaching out
6. List the 3 signals that make a lead worth contacting vs. skipping

Keep it actionable. I should be able to start building a list in the next 30 minutes using what you give me.
```

## Free toolstack for lead scraping

| Task | Free tool |
|---|---|
| LinkedIn filtering | LinkedIn basic search + Sales Navigator free trial |
| Email finding | Hunter.io (25/mo free), Snov.io free tier |
| Company info lookup | Clearbit Connect (Gmail plugin, free) |
| Google Maps leads | Google Maps + manual, or Outscraper free tier |
| List organization | Airtable free tier or Google Sheets |
| Email verification | Zerobounce (100 free/mo), NeverBounce trial |

## Automation option

For recurring or high-volume lead collection, an n8n workflow (see `n8n-agent-builder`) can automate:
- Scraping a source on a schedule
- Enriching each lead via API
- Deduplicating against an existing list
- Pushing qualified leads into a CRM

## Related skills

- **new-client-system**: Pair this skill (find the leads) with that skill (build the outreach system to contact them)
- **n8n-agent-builder**: Automate the scraping and enrichment steps with n8n
- **the-leverage-stack-auditor**: Check whether lead gen is the bottleneck or if sales conversion is — don't scale the list before fixing the pitch
- **product-marketing-context**: Define the ICP before running this skill — feeds the first input field directly
