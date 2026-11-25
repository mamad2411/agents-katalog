---
name: vibe-prospecting
description: "Vibe Prospecting MCP wrapper — fetch-entities, enrich-prospects, export-to-csv. Actor 2 in lead-gen-ai pipeline AND SOURCE 2 in hmz-daily-leads sweep. Find any business type in any city worldwide."
allowed-tools: Read, Bash, Write
---

# Vibe Prospecting — Business Entity Extraction

## Triggers
"vibe prospecting" / "fetch entities" / "enrich prospects" / "find businesses" / "business search mcp" / "entity extraction" / "hmz leads" / "daily leads"

---

## MCP Tools Available

```
mcp__Vibe_Prospecting__fetch-entities          → search businesses by type + location
mcp__Vibe_Prospecting__enrich-prospects        → add email, phone, social profiles
mcp__Vibe_Prospecting__enrich-business         → enrich a single company
mcp__Vibe_Prospecting__fetch-businesses-events → buying signals: funding, hiring, news
mcp__Vibe_Prospecting__match-business          → exact company match by name/domain
mcp__Vibe_Prospecting__match-prospects         → find specific person
mcp__Vibe_Prospecting__export-to-csv           → download dataset as CSV
mcp__Vibe_Prospecting__estimate-cost           → check credit cost before running
mcp__Vibe_Prospecting__get-dataset             → retrieve saved datasets
mcp__Vibe_Prospecting__fetch-entities-statistics → market size data for a niche
mcp__Vibe_Prospecting__autocomplete            → autocomplete business/location
```

---

## USE CASE 1 — General Lead Extraction (lead-gen-ai pipeline)

```
1. fetch-entities(type="dental clinic", location="Dubai", limit=20)
2. enrich-prospects(entity_ids=[...])   → adds email, phone, LinkedIn, Instagram, Facebook
3. export-to-csv(dataset_id=...)        → ~/Downloads/leads.xlsx via Actor 4 (openpyxl)
```

**Output columns:** name, address, phone, email, website, linkedin, instagram, facebook, google_rating, review_count, source

---

## USE CASE 2 — HMZ Daily Leads Sweep (B2B prospect hunting)

Runs as SOURCE 2 inside `hmz-daily-leads` scheduled task (7 AM PKT daily):

```python
# Buying signal search — these companies are actively expanding
fetch-businesses-events(
    event_types=["funding", "hiring", "product_launch"],
    industries=["ecommerce", "saas", "lead_gen", "health_wellness"],
    countries=["US", "GB", "CA", "AU", "AE"],
    date_range="past_7_days"
)
# → returns companies with fresh buying signals

# Enrich the top candidates
enrich-business(company_id=...)  → full profile: revenue, employees, tech stack, contacts

# Find decision maker
match-prospects(
    company_domain="example.com",
    title_keywords=["CMO", "Marketing Manager", "Founder", "Head of Growth"]
)
→ returns name, email, LinkedIn, phone
```

**Integration path:**
```
Vibe fetch-businesses-events → companies with buying signals
→ enrich-business → full company profile
→ match-prospects → decision maker contact
→ apollo_people_match → verified email
→ Lead card scored (0-100 gate: ≥80 only)
→ ~/Downloads/Leads/HMZ-Leads-Daily.xlsx + HMZ-Elite-Leads-[DATE].html
→ Gmail draft to hmzainjamil@gmail.com
```

---

## USE CASE 3 — Website Agency Client Prospecting (website-lead-agency)

Find businesses that need a website → build demo → pitch:

```
fetch-entities(
    type="local business",   # restaurant, clinic, gym, law firm, etc.
    location="[CITY]",
    filters={"has_website": false OR "website_quality": "poor"}
)
→ enrich-prospects → get owner name + email + social
→ Pass to Actor 5 (website-builder) → build demo site
→ Pass to Actor 9 (Kimi K2.5) → personalized cold pitch
```

---

## Scheduled Sweep Integration

| Sweep | Time | Uses Vibe For |
|---|---|---|
| `hmz-daily-leads` | 7 AM PKT | B2B prospect hunting via fetch-businesses-events |
| `hmz-bdm-morning-sweep` | 9 AM PKT | Supplementary company enrichment |
| `hmz-bdm-evening-sweep` | 9 PM PKT | Supplementary company enrichment |
| On-demand | Any time | Lead gen for any niche + city |

**State tracking:** `python3 /Users/mc/.claude/bin/hmz-bdm-state-update hmz-daily-leads` (run after each sweep)

---

## Combined MCP Stack (all used together)

```
Vibe Prospecting   → company/business discovery + buying signals
Apollo MCP         → B2B contact enrichment + email verification
Apify MCP          → web scraping signals (Meta Ad Library, LinkedIn, Shopify)
Gmail MCP          → draft + send reports
WebSearch          → buying signal verification, job posting analysis
```
