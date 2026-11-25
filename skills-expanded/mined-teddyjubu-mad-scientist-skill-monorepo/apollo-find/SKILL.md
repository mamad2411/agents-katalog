---

name: apollo-find
description: Search for B2B contacts and companies using the Apollo.io API. Use this skill when the user wants to find leads, prospects, or business contacts — including filtering by job title, seniority, location, company size, revenue, industry, or technology stack. Also handles company/organization search and people enrichment (emails/phones). Triggers on phrases like "find contacts", "search Apollo", "find leads", "look up companies", "B2B prospecting", "find [job title] at [company type]", "enrich a contact", or any Apollo.io data request.

---
Search Apollo.io's B2B database for people and companies. API key stored in `.secrets/apollo.env`.

## What This Skill Does

This skill Search for B2B contacts and companies using the Apollo.io API. Use this skill when the user wants to find leads, prospects, or business contacts — including filtering by job title, seniority, location, company size, revenue, industry, or technology stack. Also handles company/organization search and people enrichment (emails/phones). Triggers on phrases like "find contacts", "search Apollo", "find leads", "look up companies", "B2B prospecting", "find [job title] at [company type]", "enrich a contact", or any Apollo.io data request.

## Auth

```bash
source /data/.openclaw/workspace/.secrets/apollo.env
# $APOLLO_API_KEY is now available
```

## Endpoints

| Action | Method | URL |
|---|---|---|
| People Search | POST | `https://api.apollo.io/api/v1/mixed_people/api_search` |
| Organization Search | POST | `https://api.apollo.io/api/v1/mixed_companies/search` |
| People Enrichment | POST | `https://api.apollo.io/api/v1/people/match` |

All requests require header: `x-api-key: $APOLLO_API_KEY` and `Content-Type: application/json`.

## Workflows

### 1. People Search (no credits consumed)

Use to find net new prospects. Does **not** return emails/phones — use enrichment for that.

```bash
curl -s -X POST https://api.apollo.io/api/v1/mixed_people/api_search \
  -H "x-api-key: $APOLLO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "person_titles": ["real estate investor", "property manager"],
    "person_locations": ["maryland", "virginia", "washington dc"],
    "person_seniorities": ["owner", "c_suite", "director"],
    "organization_num_employees_ranges": ["1,50"],
    "page": 1,
    "per_page": 25
  }' | python3 -m json.tool
```

**Key filters:**
- `person_titles[]` — job titles (partial match OK)
- `person_seniorities[]` — owner, founder, c_suite, partner, vp, head, director, manager, senior, entry, intern
- `person_locations[]` — cities, US states, countries
- `organization_locations[]` — HQ location (different from person location)
- `organization_domains[]` — up to 1,000 domains
- `organization_num_employees_ranges[]` — e.g. `"1,50"`, `"51,200"`
- `revenue_range[min]` / `revenue_range[max]` — no symbols, just numbers
- `q_keywords` — free-text keyword filter
- `currently_using_any_of_technology_uids[]` — filter by tech stack (use underscores)
- `page` / `per_page` — pagination (max 100/page, up to 500 pages)

### 2. Organization Search (consumes credits)

```bash
curl -s -X POST https://api.apollo.io/api/v1/mixed_companies/search \
  -H "x-api-key: $APOLLO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "organization_locations": ["maryland"],
    "organization_num_employees_ranges": ["10,500"],
    "revenue_range": {"min": 500000, "max": 50000000},
    "q_organization_keyword_tags": ["real estate"],
    "page": 1,
    "per_page": 25
  }' | python3 -m json.tool
```

**Key filters:**
- `organization_domains[]` — domain names
- `organization_num_employees_ranges[]` — headcount ranges
- `organization_locations[]` — HQ location
- `organization_not_locations[]` — exclude locations
- `revenue_range[min]` / `revenue_range[max]`
- `q_organization_keyword_tags[]` — industry keywords
- `q_organization_name` — company name (partial match OK)
- `currently_using_any_of_technology_uids[]` — tech stack

### 3. People Enrichment (consumes credits)

Use to get emails/phones for a known person.

```bash
curl -s -X POST https://api.apollo.io/api/v1/people/match \
  -H "x-api-key: $APOLLO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Smith",
    "organization_name": "Acme Corp",
    "domain": "acme.com",
    "reveal_personal_emails": true,
    "reveal_phone_number": true
  }' | python3 -m json.tool
```

**Tips:** More data = better match. At minimum provide name + domain or email.

## Scripts

Use `scripts/apollo_search.py` for structured searches with CSV export.

```bash
cd /data/.openclaw/workspace/skills/apollo-find
python3 scripts/apollo_search.py \
  --titles "real estate investor" "property manager" \
  --locations "maryland" "virginia" \
  --seniority "owner" "c_suite" \
  --employees "1,200" \
  --pages 3 \
  --output results.csv
```

See `references/api_docs.md` for full parameter reference and response schema.

## Output Format

When presenting results to Charles, format as:
- **Name** | Title | Company | Location
- Total count found
- Offer to enrich top results for emails/phones (note: costs credits)
- Offer to export as CSV
