---
name: apify
description: Dynamic Apify actor selection and execution for research tasks. Searches Apify store to find best actors, prefers pay-per-result pricing. Use when needing web scraping, data extraction, or research automation.
---

# Apify Skill

Dynamic research automation using Apify actors. Searches the Apify store to find the best actor for any research need, with a registry of validated actors for common tasks.

## When to Activate

- User needs to scrape websites, job boards, or social media
- Research requires data that's not available via standard APIs
- Outreach campaigns need EDP data from external sources (job postings, company news, etc.)
- User mentions "scrape", "extract", "job postings", "LinkedIn search", or similar research needs

## Core Philosophy

### 1. Dynamic Actor Selection

When a research need arises:
1. Check the actor registry for known good actors
2. If not found, search Apify store for appropriate actors
3. Prefer pay-per-result/event/usage pricing over flat subscription
4. Always ask user before building new research pipelines

### 2. Pay-Per-Result Preference

**Always prefer actors with:**
- Pay per result
- Pay per event
- Pay per usage

**Avoid when possible:**
- Flat monthly subscriptions
- High minimum costs

### 3. Build on Demand

When no suitable actor exists in the registry:
1. Search Apify store
2. Present options to user with pricing
3. Ask: "Should I add this to the registry for future use?"

---

## Actor Registry

Known, validated actors for common research tasks. See [modules/ACTOR_REGISTRY.md](modules/ACTOR_REGISTRY.md) for full registry.

### Quick Reference

| Use Case | Actor | ID | Pricing |
|----------|-------|-----|---------|
| LinkedIn Jobs | fantastic-jobs/advanced-linkedin-job-search-api | vIGxjRrHqDTPuE6M4 | Pay per result |
| YouTube Transcripts | karamelo/youtube-transcripts | - | Pay per result |
| People Database | apify/people-database | IoSHqwTR9YGhzccez | Pay per result |

---

## Usage

### Run a Known Actor

```bash
# LinkedIn Jobs Search
uv run .claude/skills/apify/scripts/run_actor.py \
  --actor "vIGxjRrHqDTPuE6M4" \
  --input '{"searchQuery": "operations manager", "location": "United States", "maxResults": 100}' \
  --output jobs.json

# Or use the alias
uv run .claude/skills/apify/scripts/linkedin_jobs.py \
  --query "operations manager" \
  --location "United States" \
  --company-size "11-50,51-200" \
  --max-results 100
```

### Search Apify Store

```bash
# Find actors for a research need
uv run .claude/skills/apify/scripts/search_store.py \
  --query "linkedin job postings" \
  --pricing "pay_per_result"
```

### Build New Research Pipeline

When the system identifies a gap (like Tier 1 EDP needing job data):

1. **Identify the need:** "We need job posting data for agencies hiring ops roles"
2. **Check registry:** Is there a known actor for this?
3. **Search store:** If not, find candidates
4. **Ask user:** "Should I build this research capability using [actor name]?"
5. **Build & register:** Create script and add to registry

---

## Scripts

| Script | Purpose |
|--------|---------|
| `run_actor.py` | Run any Apify actor by ID |
| `search_store.py` | Search Apify store for actors |
| `linkedin_jobs.py` | LinkedIn Jobs search (uses vIGxjRrHqDTPuE6M4) |

---

## Integration with Outreach V2

For Tier 1 EDP data that requires external research:

```
/outreach-v2 → Phase 4 (List Criteria) → Identifies gap
                                        ↓
                           Apify skill fills the gap
                                        ↓
                           LinkedIn Jobs search → Company list
                                        ↓
                           Prospeo enrichment → Verified contacts
```

**Example flow:**
1. Tier 1 needs agencies posting "Operations Manager" roles
2. Apify LinkedIn Jobs actor searches for these postings
3. Returns company names with the EDP verified
4. Prospeo enriches with decision-maker contacts

---

## Environment Variables

```bash
APIFY_API_KEY=your_api_key_here
```

Get your API key from: https://console.apify.com/account/integrations

---

## Building New Research Capabilities

When you encounter a research need not in the registry:

### Step 1: Search Store
```bash
uv run .claude/skills/apify/scripts/search_store.py --query "your research need"
```

### Step 2: Evaluate Options
- Check pricing model (prefer pay-per-result)
- Check reviews and usage stats
- Verify output format matches needs

### Step 3: Ask User
"I found [actor name] for this research need. It costs [pricing]. Should I add this to our research toolkit?"

### Step 4: If Approved, Build Script
Create a purpose-built script in `scripts/` and add to registry.

---

## Quality Standards

Before using an actor:
- [ ] Verified pricing model (prefer pay-per-result)
- [ ] Tested with small sample
- [ ] Output format documented
- [ ] Added to registry if reusable

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| **find-leads** | Apify provides EDP data, find-leads enriches contacts |
| **pvp-list-criteria** | Identifies when Apify research is needed |
| **outreach-v2** | Orchestrates the full pipeline |
