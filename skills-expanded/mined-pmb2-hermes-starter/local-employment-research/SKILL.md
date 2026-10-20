---
name: local-employment-research
description: Find local job opportunities by scraping job boards via terminal/curl, parsing results, and compiling actionable walk-in leads. Covers service industry (server, bartender, host), retail, and general hourly positions.
version: 1.0.1
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [jobs, employment, research, service-industry, scraping]
    triggers: [find work, find a job, local jobs, side hustle, employment research, walk-in jobs]
    related_skills: [maps, local-market-elite-networking]
---

# Local Employment Research

Search and compile local job opportunities near a given location. Focuses on service-industry / hourly roles where walk-in applications are effective.

## When to use

User asks to find work, a gig, a job, or a side hustle in their area, especially:
- Restaurant/bar/service industry (server, bartender, host, barback, busser)
- Retail / hospitality
- "Something near me that's hiring"
- Any role where being presentable and in-person matters over a resume

## Workflow

### 1. Identify the location and radius

The user likely lives in a specific town/city. Use their profile or stated location. Default radius: 15-25 miles. Ask only if ambiguous.

### 2. Search Indeed via curl

Indeed returns ~20 job cards per page even with JS rendered. Use terminal + curl with a realistic User-Agent:

```bash
curl -sL "https://www.indeed.com/jobs?q=server+restaurant&l=LOCATION%2C+NY&radius=25&sort=date" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
```

Key query parameters:
- `q`: job keywords (server, bartender, host, fine dining)
- `l`: location (URL-encoded city, state)
- `radius`: search radius in miles
- `sort=date`: newest first

### 3. Parse job listings from HTML extract

Indeed's SSR HTML contains structured data extractable via regex:

```python
import sys, re
html = sys.stdin.read()
titles = re.findall(r'jobTitle[^>]*>.*?<span[^>]*title=\"([^\"]+)\"', html)
companies = re.findall(r'data-testid=\"company-name\"[^>]*>([^<]+)<', html)
locations = re.findall(r'data-testid=\"text-location\"[^>]*>([^<]+)<', html)
snippets = re.findall(r'belowJobSnippet[^>]*>(.*?)</div>', html, re.DOTALL)
```

Also try for salary info:
```python
pays = re.findall(r'salary-snippet[^>]*>([^<]+)<', html)
```

### 4. Filter and curate

- Prioritize locations closest to the user
- Highlight "Easily apply" listings
- Note evening/dinner shifts specifically
- Flag upscale vs casual establishments
- Separate corporate chains (run background checks) from independent restaurants (hire on presence)

### 5. Compile actionable leads

Format as a ranked list with:
- Restaurant name, location, distance from user
- Type of role (server, bartender, cocktail)
- Pay range if available
- Walk-in strategy recommendations

### 6. Walk-in strategy advice

For service industry jobs, walking in during **off-peak hours (2-4pm, Mon-Wed)** is the most effective method. Recommend the user:
- Go between 2-4pm (between lunch and dinner rush)
- Ask to speak to a manager or FOH manager
- Say they're local, presentable, people-person, want dinner rush only
- Independent restaurants rarely do formal background checks
- Corporate chains (LongHorn, Cracker Barrel, casino restaurants) almost always do

## Pitfalls

- Indeed pages are JS-heavy; the SSR HTML only has ~20 results even when "X jobs found" says more
- The `&` character in URLs will break terminal tool calls — URL-encode it as `%26` or use a data-only query
- Salary regex is fragile across Indeed's monthly UI updates — check for class changes
- ZipRecruiter and SimplyHired are fully JS-rendered and yield no useful data from curl alone
- For fine dining searches, add `fine dining` or `upscale` to query terms
- Track season (Saratoga: July-September) creates huge seasonal hiring demand — mention this
