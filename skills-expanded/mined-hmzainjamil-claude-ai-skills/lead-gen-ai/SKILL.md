---
name: lead-gen-ai
description: "Automated lead extraction system — Vibe Prospecting MCP + Apollo MCP + Excel export + outreach sequences. Also orchestrates hmz-daily-leads, hmz-bdm-morning-sweep, hmz-bdm-evening-sweep, hmz-indeed-mcp-sweep scheduled pipelines."
allowed-tools: Read, Bash, Write, Agent
---

# Lead Gen AI — Automated Lead Extraction System
## Triggers: lead generation, find leads, extract leads, lead gen, vibe prospecting, find contacts, scrape leads, dental clinic leads, business directory, find emails, find phone numbers, contact scraping, automated leads, apollo leads, clay leads, hmz leads, daily leads, elite leads, lead sweep, bdm sweep

---

## THE SYSTEM — One prompt → full contact dataset

**Name, phone, email, website, LinkedIn, Instagram, Facebook, Google rating**
Runs 24/7. Works for ANY niche, ANY location worldwide.

PLUS: Autonomous daily sweeps running on schedule for HMZ elite B2B leads.

---

## MASTER AGENT WORKFLOW — 5 ACTORS (General Lead Gen)

### ACTOR 1 — Brief Generator (Kimi 8K)
```
Input: "find 20 dental clinics in Dubai"
Output: structured prompt → business type + location + data fields + output format
```

### ACTOR 2 — Vibe Prospecting Extractor (MCP)
```
mcp__Vibe_Prospecting__fetch-entities          → search by type + location
mcp__Vibe_Prospecting__enrich-prospects        → email, phone, social profiles
mcp__Vibe_Prospecting__fetch-businesses-events → buying signals (funding, hiring)
mcp__Vibe_Prospecting__match-business          → exact company match
mcp__Vibe_Prospecting__export-to-csv           → download dataset
```

### ACTOR 3 — Apollo Enricher (MCP)
```
apollo_mixed_companies_search   → find companies by industry + filters
apollo_people_match             → find decision makers by name + company
apollo_contacts_search          → filter contacts by title, industry, location
apollo_organizations_enrich     → full company profile + tech stack
apollo_people_bulk_match        → batch enrich 100+ contacts
```

### ACTOR 4 — Data Formatter + Excel Export (Python/openpyxl)
```python
import openpyxl
from pathlib import Path

def export_leads_to_excel(leads: list[dict], filename: str = "leads"):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Leads"
    headers = ["Business Name", "Address", "Phone", "Email", "Website",
               "LinkedIn", "Instagram", "Facebook", "Google Rating", "Reviews", "Source"]
    for col, h in enumerate(headers, 1):
        ws.cell(1, col, h).font = openpyxl.styles.Font(bold=True)
    for row, lead in enumerate(leads, 2):
        for col, key in enumerate(["name","address","phone","email","website",
                                    "linkedin","instagram","facebook","rating","reviews","source"], 1):
            ws.cell(row, col, lead.get(key, ""))
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = 20
    out = Path.home() / "Downloads" / f"{filename}.xlsx"
    wb.save(out)
    return str(out)
```

### ACTOR 5 — Outreach Sequence Generator (Kimi K2.5)
```
Input: lead list
Output:
  - Personalized email subject + body per lead
  - LinkedIn connection request message
  - Cold DM for Instagram/Facebook
  - Mailchimp/GetResponse import-ready CSV
```

---

## HMZ DAILY SWEEP PIPELINE — Autonomous B2B Lead System

Four scheduled tasks that run automatically, all using the same MCP stack:

### SWEEP 1 — Elite Leads (7 AM PKT daily)
**Task:** `hmz-daily-leads`
**File:** `/Users/mc/.claude/scheduled-tasks/hmz-daily-leads/SKILL.md`

Sources (run in parallel):
| Source | Tool | What it finds |
|---|---|---|
| Apollo MCP | `apollo_mixed_companies_search` | B2B companies by industry + size |
| Vibe MCP | `fetch-businesses-events` | Funding/hiring signals = buying signals |
| Apify MCP | `call-actor` | Meta Ad Library scrape, LinkedIn signals, Shopify stores |
| Meta Ad Library | WebSearch | Confirmed active ad spenders |
| Reddit/Twitter | WebSearch | Companies expressing PPC pain right now |
| Job postings | WebSearch | Companies posting PPC roles = have budget |

Gate system (ALL must pass):
- GATE 1: Real + active business
- GATE 2: Spends on ads (or clearly needs to)
- GATE 3: Has a problem Zulqarnain solves
- GATE 4: Can pay ($5k+ ad spend/mo signal)
- GATE 5: Can hire globally/remote

Scoring threshold: **≥80 only** (0-100 scale)

Output:
- `/Users/mc/Downloads/Leads/HMZ-Leads-Daily.xlsx` — appended (never wiped)
- `/Users/mc/Downloads/HMZ-Elite-Leads-[DATE].html` — gold/green color-coded cards
- Gmail draft → hmzainjamil@gmail.com

### SWEEP 2 — Morning Job Sweep (9 AM PKT daily)
**Task:** `hmz-bdm-morning-sweep`
**File:** `/Users/mc/.claude/scheduled-tasks/hmz-bdm-morning-sweep/SKILL.md`

10 platforms in parallel: LinkedIn · WeWorkRemotely · Remotive · Remote.co · Wellfound · Contra · Pangian · Himalayas · X/Twitter · Jobspresso

Filters: Meta/Google Ads scope · $15+/hr · GEO whitelist (USA/UK/CA/AU/AE/EU) · GEO blacklist (IN/PK/BD/PH/IL) · <48h · Remote + PK-eligible
Threshold: **≥65 score**

Output: `/Users/mc/Downloads/HMZ-BDM-Morning-[DATE].html` + Gmail draft

### SWEEP 3 — Evening Job Sweep (9 PM PKT daily)
**Task:** `hmz-bdm-evening-sweep`
**File:** `/Users/mc/.claude/scheduled-tasks/hmz-bdm-evening-sweep/SKILL.md`

Same 10 platforms + Reddit value comments (3 max, strict cap)

Output: `/Users/mc/Downloads/HMZ-BDM-Evening-[DATE].html` + Reddit drafts + Gmail

### SWEEP 4 — Indeed MCP Sweep (on-demand / scheduled)
**Task:** `hmz-indeed-mcp-sweep`
**File:** `/Users/mc/.claude/scheduled-tasks/hmz-indeed-mcp-sweep/SKILL.md`

8 Indeed MCP queries via `search_jobs` + `get_job_details` — structured data only, no WebSearch

Output: `/Users/mc/Downloads/HMZ-Indeed-MCP-[DATE]-[TIME].html` + Gmail draft

---

## State Tracking

All sweeps must call this on completion:
```bash
python3 /Users/mc/.claude/bin/hmz-bdm-state-update [sweep-name]
# sweep-name: hmz-daily-leads | hmz-bdm-morning-sweep | hmz-bdm-evening-sweep | hmz-indeed-mcp-sweep
```

Catch-up script (run if a sweep was missed):
```bash
python3 /Users/mc/.claude/bin/hmz-bdm-catchup
```

---

## COMBINED MCP STACK (all wired, all available)

```
Vibe Prospecting MCP  → business discovery, enrichment, buying signals
Apollo MCP            → B2B contacts, company enrichment, email sequences
Apify MCP             → web scraping (Meta Ad Library, LinkedIn, Shopify)
Gmail MCP             → create_draft, send reports
Indeed MCP            → structured job search via search_jobs + get_job_details
WebSearch             → real-time signals (Reddit, Twitter, job boards)
```

---

## QUICK START PROMPTS

```
# General lead extraction
"Find top 20 dental clinics in Dubai. Get phone, email, Instagram, Google rating. Export Excel."

# Run daily elite leads sweep now
"Run hmz-daily-leads sweep — find 10 elite B2B leads for Zulqarnain, score ≥80 only"

# Morning job sweep now
"Run HMZ morning BDM sweep — all 10 platforms, strict filters, score ≥65"

# Enrich with decision makers
"For each business, find the owner/marketing manager name + email using Apollo"

# Generate outreach
"Write personalized cold email + LinkedIn DM for each lead. Export CSV for Mailchimp."
```

---

## OUTPUT FILES

| File | Path | Format |
|---|---|---|
| General leads | `~/Downloads/leads.xlsx` | 11-column Excel |
| Elite B2B leads (daily append) | `~/Downloads/Leads/HMZ-Leads-Daily.xlsx` | Score, company, DM, pain point, entry angle |
| Morning job report | `~/Downloads/HMZ-BDM-Morning-[DATE].html` | Scored job cards |
| Evening job report | `~/Downloads/HMZ-BDM-Evening-[DATE].html` | Scored cards + Reddit drafts |
| Indeed MCP report | `~/Downloads/HMZ-Indeed-MCP-[DATE].html` | Structured job cards |
| Elite leads HTML | `~/Downloads/HMZ-Elite-Leads-[DATE].html` | Gold/green lead cards |
| Outreach CSV | `~/Downloads/outreach.csv` | Mailchimp import-ready |

---

## EMAIL AUTOMATION

After export → upload to:
1. **Mailchimp** — drag CSV → create campaign → auto-personalize subject
2. **GetResponse** — autoresponder sequence → drip campaign
3. **Apollo sequences** — `apollo_emailer_campaigns_add_contact_ids` via MCP

Template:
```
Subject: Increase your [BUSINESS] appointments with [SERVICE]

Hi [NAME],

I noticed [SPECIFIC OBSERVATION].
We help [NICHE] businesses in [CITY] get [RESULT] in [TIMEFRAME].
[PROOF — client result or free audit offer]

Would a quick 15-min call this week make sense?
```
