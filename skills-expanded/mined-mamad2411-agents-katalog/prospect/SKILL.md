---
name: prospect
description: "Full-pipeline Apollo prospecting — searches for ICP-matching companies via Apollo MCP, deduplicates against existing vault prospects, enriches companies and contacts, web-researches each prospect for pain signals and outreach triggers, then writes everything into the Obsidian vault (company files, Pipeline Tracker, Batch Log). Use this skill whenever the user says 'find prospects,' 'prospect,' 'run apollo,' 'find more companies,' 'build a list,' 'outbound research,' 'find leads,' 'enrich prospects,' 'prospecting run,' or wants to add new outreach targets to their pipeline. Also trigger when the user says 'find more DTC companies,' 'B2C SaaS prospects,' or any variation of wanting to discover and research potential customers for outreach."
---

# Apollo Prospecting Pipeline

End-to-end skill for discovering, enriching, researching, and documenting outreach prospects using Apollo MCP tools and web research. One invocation runs the full pipeline: search → deduplicate → enrich → research → write to vault.

## Before You Start

### 1. Read ICP and Existing State

Read these files to understand the current ICP filters and what's already been prospected:

- **ICP Definition:** Read the Consumer Profile or product-marketing-context to extract target company size, revenue range, tech stack signals, buyer personas, and keyword tags. Look for these in the Riven domain docs.
- **Apollo Query Playbook:** `Apollo Prospecting/Apollo Query Playbook.md` — contains pre-defined search parameters. Use these as defaults unless the user specifies different filters.
- **Pipeline Tracker:** `Apollo Prospecting/Pipeline Tracker.md` — scan existing prospect rows to know which companies are already tracked.
- **Batch Log:** `Apollo Prospecting/Batch Log.md` — check the credit usage summary to know remaining credits.
- **Existing company files:** Glob `Apollo Prospecting/Companies/*.md` to get the list of already-prospected companies.

The default vault path is:
```
/home/jared/docs/Documents/2. Areas/2.1 Startup & Business/Riven/6. Customer Validation/Apollo Prospecting/
```
Use a different path only if the user explicitly points elsewhere.

### 2. Confirm Parameters with the User

Before running searches, confirm:
- **Vertical:** DTC e-commerce, B2C SaaS, or both?
- **Revenue range:** Default from ICP docs (typically $500K-$10M), but user may want to narrow
- **Target batch size:** Default ~10 companies, ~14 contacts (1-2 per company)
- **Credit budget:** Check remaining credits in Batch Log. Company enrichment = 1 credit each, contact enrichment = 1 credit each. A full batch of 10 companies + 14 contacts = ~24 credits.
- **Any specific filters:** Tech stack requirements, geography, company size, role titles

If the user's request is clear enough (e.g., "find 10 more DTC companies"), skip the confirmation and proceed.

---

## Pipeline Steps

### Step 1: Search Apollo

Run `apollo_mixed_people_api_search` using filters from the Query Playbook or user overrides.

**For DTC E-commerce:**
- `currently_using_all_of_technology_uids`: ["shopify", "klaviyo"]
- `currently_using_any_of_technology_uids`: ["gorgias", "zendesk", "intercom", "freshdesk"]
- `q_organization_keyword_tags`: ["e-commerce", "DTC", "direct to consumer"]
- `person_titles`: ops/marketing/growth directors and managers
- `person_seniorities`: ["director", "manager", "vp"]
- `contact_email_status`: ["verified"]

**For B2C SaaS:**
- `currently_using_any_of_technology_uids`: ["mixpanel", "amplitude", "heap"]
- `currently_not_using_any_of_technology_uids`: ["shopify"] (to separate from DTC)
- `q_organization_keyword_tags`: ["B2C", "consumer", "subscription", "mobile app"]
- `person_titles`: ops/marketing/growth directors
- `person_seniorities`: ["director", "vp"]
- `contact_email_status`: ["verified"]

Request `per_page: 50` to get a good pool to select from. Search is free — no credits consumed.

### Step 2: Deduplicate

Compare search results against:
1. **Existing company files** in `Companies/` — match by company name (case-insensitive)
2. **Existing Pipeline Tracker rows** — match by company name or domain

Remove any companies already tracked. Report to the user: "Found X results, Y are new (Z already in pipeline)."

### Step 3: Select Top Companies

From the deduplicated results, select the ~10 best companies based on:
- **Stack depth:** More ICP-matching tools = higher priority
- **Role fit:** Director/VP of ops/marketing/growth > individual contributors
- **Multiple contacts found:** Companies with 2+ relevant people are stronger
- **Has email:** Contacts with `has_email: true` preferred

Present the shortlist to the user for approval before spending enrichment credits: "Here are the top 10 new companies. Want me to enrich all of them, or should I adjust?"

### Step 4: Enrich Companies

For each approved company, run `apollo_organizations_enrich` with the company domain.

Extract and record:
- Company name, domain, industry, employee count, revenue, location, founded year
- Funding stage and total funding
- Full technology stack (every tool with its UID and category)
- Company description

**Stack validation:** After enrichment, verify each company actually has the ICP tech stack. Remove companies that don't match (e.g., Apollo's keyword tags were misleading). Report removals to the user.

Credits consumed: 1 per company.

### Step 5: Enrich Contacts

For the best 1-2 contacts per company (prioritize ops/marketing directors over C-suite), run `apollo_people_match` using their Apollo ID.

Extract and record:
- Full name, title, verified email, LinkedIn URL
- Employment history (current + previous roles)
- City, state, country
- Notable background details (ex-companies, career trajectory)

Credits consumed: 1 per contact.

### Step 6: Web Research (Parallel)

Launch 2-3 background research agents in parallel, splitting the contacts between them. Each agent should research 4-7 people.

**Research brief for each person:**
Search the web for their LinkedIn activity, recent posts, interviews, podcast appearances, conference talks, or published content. Also search for their company's recent news, press, job postings, or social media that reveals operational challenges or growth pains.

**Look for pain signals related to:**
- Tool fragmentation / "too many dashboards"
- Analytics or attribution challenges
- Cross-platform data issues
- Manual reporting / spreadsheet frustration
- Churn analysis difficulties
- Operational scaling pains
- Hiring for data/analytics roles (= buying signal)
- Recent funding or leadership changes (= reporting pressure)

**For each person, produce:**
1. **LinkedIn headline and positioning** — what they care about
2. **Recent activity or posts** — pain signals, topics they engage with
3. **Background relevance** — why their experience makes them likely to feel the pain
4. **Potential trigger for outreach** — specific angle for personalization
5. **Outreach channel recommendation** — email first, LinkedIn first, or both
6. **Personalized opener draft** — a 1-2 sentence first line for outreach

### Step 7: Write to Vault

Create/update these files:

#### Company Files (`Companies/{company-slug}.md`)

Use lowercase-hyphenated filenames. Each file follows this structure:

```yaml
---
type: area
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
tags:
  - riven/validation
  - riven/prospecting
  - riven/prospect-company
vertical: dtc-ecommerce | b2c-saas
status: enriched
---
```

Sections:
- **Company Profile** — table with domain, LinkedIn, industry, employees, revenue, location, founded, funding
- **Tech Stack** — table with tool name, category, confirmed source (Apollo)
- **Contacts** — table with name, title, email, LinkedIn, status. Include contact notes with background highlights.
- **Trigger-Offer Fit Assessment** — best trigger, signal tier (Tier 1/2/3), one-sentence fit, research notes, outreach approach, personalized opener draft
- **Outreach Log** — empty table (date, channel, action, response)
- **References** — links to [[Pipeline Tracker]], [[Outreach Messaging SOP]]

#### Pipeline Tracker

Read the existing Pipeline Tracker. Append new rows to the appropriate vertical table (DTC or B2C SaaS). Each row:

```
| # | Name | Company | Role | Domain | Status | Channel | Date Sourced | Date Contacted | Signal/Trigger | Quality | Notes |
```

- Set status to `enriched`
- Date Sourced = today
- Signal/Trigger = key tech stack + employee count + revenue
- Quality = leave blank for user to assess
- Notes = brief company description + vertical context
- Company name should wiki-link to the company file: `[[company-slug|Company Name]]`

Update the Pipeline Summary counts.

#### Batch Log

Append new batch entries for:
1. The search run (0 credits, results count, filters used)
2. The company enrichment run (N credits, companies listed)
3. The contact enrichment run (N credits, contacts count)

Update the Credit Usage Summary row for the current month.

### Step 8: Prioritize and Present

After all vault writes are complete, present a prioritized summary to the user:

**Tier 1 (strongest triggers):** Prospects with Tier 1 pain signals — hiring for data roles, public pain admissions, operational failures, time-sensitive events (funding, leadership changes)

**Tier 2 (strong fit):** Prospects with Tier 2 behavioral signals — new to role, multi-channel expansion, stack sprawl

**Tier 3 (good fit, less urgent):** Prospects with Tier 3 demographic signals — right stack, right size, but no specific trigger found

For each Tier 1 prospect, include the personalized opener and recommended channel.

Report credit usage: "X credits spent this run, Y remaining."

---

## Important Notes

- **Never enrich without user approval.** Searches are free but enrichments cost credits. Always present the shortlist before enriching.
- **`apollo_mixed_people_api_search` does NOT return emails.** The enrichment step (`apollo_people_match`) is mandatory to get contact details.
- **Technology UIDs use underscores** for spaces/periods: `shopify`, `klaviyo`, `google_analytics`, `wordpress_org`
- **Apollo revenue data is approximate.** The enrichment may show $2M for a company doing $50M. Use web research to cross-reference.
- **Prioritize people in the weeds** over C-suite. Directors of Operations, Marketing Directors, and Heads of Growth feel the tool fragmentation pain daily and can champion a purchase. CEOs and COOs at larger companies (50+ employees) may be too removed from the tools.
- **Run web research in parallel** using background agents to save time. Split prospects across 2-3 agents.
- **Write vault files atomically** — use a single background agent to write all company files, Pipeline Tracker updates, and Batch Log entries to avoid conflicts.
