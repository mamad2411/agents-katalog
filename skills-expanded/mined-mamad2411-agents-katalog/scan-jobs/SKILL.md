---
name: scan-jobs
description: Scan a job portal for matching projects/roles, assess fit against profile, track evaluated ads
argument-hint: <portal-url-or-name> [search query]
user-invocable: true
allowed-tools: WebFetch(*), mcp__exa__web_fetch_exa, mcp__exa__web_search_exa, Read(*), Edit(.claude/skills/scan-jobs/cache.md), Write(.claude/skills/scan-jobs/cache.md), Read(data/job-pipeline.md), Write(data/job-pipeline.md)
---

# Scan Job Portal

Scan a job portal for projects/roles matching the candidate's profile, deduplicate against a persistent cache of already-evaluated ads, assess fit for new listings, and output a ranked table with links.

## Arguments

- `$ARGUMENTS`: `<portal> [search query]`
  - **Portal** (required): Domain or URL of the job portal to scan (e.g. `upwork.com`, `indeed.com`, or a full search URL)
  - **Search query** (optional): Search terms. If omitted, derive a default query from the candidate's top skills.

Examples:
- `/scan-jobs upwork.com` — scan with auto-derived query
- `/scan-jobs upwork.com "project manager" OR "product owner"`
- `/scan-jobs indeed.com "data engineer" remote`
- `/scan-jobs https://www.example.com/jobs?q=frontend&type=contract` — full search URL

## Instructions

### Step 1: Load Profile

Read the candidate's profile to build a matching baseline. Read in parallel:
- `data/project-index.md` — project overview for matching
- `data/skills.md` — skill inventory with experience levels
- `data/certifications.md` — active certifications
- `data/profile.md` — languages, location, availability, rates

**Build a mental profile summary** from these files:
- Core technologies (Expert + Advanced rated skills)
- Active certifications
- Domain experience (from project industries)
- Languages spoken
- Location and availability constraints
- Contract type preferences (if stated in profile)

**Derive disqualifiers** from the profile:
- Languages not spoken by the candidate
- Technologies marked as absent or not listed at all
- Contract types not matching (e.g., if profile says "freelance only", skip permanent positions)

If no search query was provided, **derive a default query** from the top 2-3 Expert-rated skills, joined with OR.

### Step 2: Read Cache & Calculate Lookback Window

Read the evaluated ads cache:
```
.claude/skills/scan-jobs/cache.md
```

**Parse two things:**
1. **Already-evaluated ads:** Build a list from the table. The dedup key is the **Title + Company** combination (case-insensitive, fuzzy — e.g. "Senior Software Engineer / Backend" matches "Senior Software Engineer/Backend").
2. **Lookback window:** Read the "Last updated" date from the top of the cache file. Calculate the number of days between that date and today, then **add 1 day as buffer**. Use this for any date-based filter the portal supports. Minimum: 1 day. Maximum: 14 days. If the cache has no date or is unparseable, default to 7 days.

### Step 3: Navigate the Portal

#### Step 3a: If the board is ATS-hosted, use the ATS API — do NOT fetch the page

**Check this FIRST, before any WebFetch or Exa call.** Most company job boards are
hosted by an ATS that renders listings in JavaScript. A fetch of the rendered page
returns a title-only shell or a partial list, and **that result is indistinguishable
from a genuinely empty board** — which is how a scan records "no roles at X" when the
board actually has fifty.

**This repo already has parsers for the three major ATSes.** Do not write new fetch
logic and do not reach for WebFetch on these hosts — import or shell out to:

| Host in the URL | Parser | Endpoint it uses |
|---|---|---|
| `jobs.ashbyhq.com/<slug>` | `tools/career_scanner/ashby.py` → `fetch_ashby(slug)` | `api.ashbyhq.com/posting-api/job-board/<slug>` |
| `boards.greenhouse.io` / `job-boards.greenhouse.io/<slug>` | `tools/career_scanner/greenhouse.py` → `fetch_greenhouse(slug)` | `boards-api.greenhouse.io/v1/boards/<slug>/jobs?content=true` |
| `jobs.lever.co/<slug>` | `tools/career_scanner/lever.py` → `fetch_lever(slug)` | `api.lever.co/v0/postings/<slug>?mode=json` |

These return full JSON: title, department, location, complete description, and comp
band where posted. That is strictly more than a page fetch can give you, and it
removes the separate detail-fetch in Step 4b for these listings.

Add `?includeCompensation=true` to the Ashby endpoint when calling it directly by
curl — the comp band is otherwise omitted.

**The slug is not always the company name.** When a direct slug guess 404s or returns
`[]`, the board is often embedded as an iframe on the company's own careers page.
Recover the real slug rather than concluding the board is empty:

1. Open the company's careers/jobs page in Chrome (`mcp__claude-in-chrome__navigate`).
2. Read the iframe sources:
   `[...document.querySelectorAll('iframe')].map(f=>f.src)`
3. The ATS slug is in that URL.

Worked shape (a real case, company generalised): `example.com/careers` is a culture
page carrying no listings at all, and the obvious slug guess (`.../example`) 404s. The
real board is `jobs.ashbyhq.com/examplelabs` — a different slug — embedded as an iframe
on `example.com/jobs`, with dozens of roles behind it. Two fetch-based passes had recorded that
company as "inconclusive, JS-rendered." Note the two separate traps: the careers page is
not the board, and the slug is not the company name.

**A slug that returns `[]` is NOT evidence of an empty board.** Per `data/scan-targets.yaml`'s
own warning: a wrong slug returns `[]` and looks exactly like an empty board. Say
"could not enumerate the board" — never "no roles found" — until a parser has
returned rows.

> **Origin, 2026-09-14.** A target company's careers check was run three times across
> three weeks and each time recorded as "a handful of roles, all engineering; the
> non-engineering filter categories are empty." The ATS API returned an order of magnitude
> more, including several in-lane seats. The board was never empty; it was never being read.
> The parsers above already existed in this repo the whole time and were not used.
> Two failure modes compounded: reaching for a generic fetch tool before checking for
> existing infrastructure, and recording an unreadable result as a negative finding.

#### Step 3b: Everything else

**If a full search URL was provided:** Fetch it directly.

**If only a portal domain was provided:**
1. Fetch the portal's job search or browse page
2. Identify the URL structure and search parameters
3. Construct a search URL applying relevant filters:
   - Contract type: match the candidate's preferences from `data/profile.md` (e.g. freelance, contract, permanent — if the portal supports this filter)
   - Remote work: match the candidate's work-model preference from `data/profile.md` (remote, hybrid, onsite — if the portal supports this filter)
   - Region: match the candidate's profile location/target market
   - Recency: filter to the lookback window if the portal supports date filtering
   - Query: use the provided or auto-derived search terms

**WebFetch prompt — use this exact prompt to maximise data extraction:**
```
Extract ALL project/job listings from this page as a structured list. For each listing extract:
1. EXACT project title
2. Company/intermediary name
3. Start date
4. Duration
5. Location and remote percentage
6. ALL skills/technologies mentioned
7. Daily/hourly rate if shown
8. Industry/sector
9. The href URL path for the project detail page (look for <a> tags linking to detail pages)

Number each listing. Extract every single one on the page.
```

If WebFetch returns a 403, an empty result, or a bot-gate/login wall (common on job boards), retry the same URL with `mcp__exa__web_fetch_exa` before giving up; Exa's fetch gets past gates that block WebFetch (per the Exa A/B verdict, 2026-05-19, reconfirmed 2026-06-01). If the portal still cannot be parsed or requires authentication even via Exa, inform the user and suggest they provide a direct search URL with results visible.

### Step 4: Deduplicate Against Cache

Compare each ad from the search results against the cache (match by Title + Company, case-insensitive, fuzzy). If already evaluated, skip it entirely.

Report: "Found X total, Z already in cache, **N new ads to evaluate**."

If there are zero new ads, report that and stop — do not re-evaluate cached ads.

### Step 4b: Fetch Detail Pages

**Skip this step for any listing already retrieved via Step 3a** — the ATS parsers return the complete description, so there is nothing further to fetch and a second call would only re-render the same content worse.

For every other new (non-cached) ad, fetch its detail page to read the **actual listing text**. Do NOT assess fit based only on the search result tags — the detail page contains the real requirements, which often differ from the tag summary.

**Fetch all detail pages in parallel** (they are independent). Use this WebFetch prompt:
```
Extract the COMPLETE listing text in the original language. Include every section: description, tasks/responsibilities, requirements/qualifications, nice-to-haves, location/remote details, and any other content. Do not summarize — reproduce the full text. Also extract: contract type, start date, duration, rate if shown, and language requirements.
```

If a detail URL was not extracted from the search results, skip that ad's detail fetch — assess it from search results only (note this limitation in the assessment).

### Step 5: Assess Fit for New Ads

For each new (uncached) ad, assess fit against the candidate's profile **using the detail page text from Step 4b**:

**Fit scoring guidelines:**
- **80-100%:** Core stack match, relevant domain, matching contract type → **shortlisted**
- **60-79%:** Strong partial match, one gap is learnable or minor → **maybe** (leaning yes)
- **40-59%:** Some overlap but significant gaps or wrong emphasis → **maybe** (leaning no)
- **20-39%:** Marginal overlap, mostly wrong stack/domain → **skip**
- **0-19%:** No meaningful overlap → **skip**

**Automatic disqualifiers (mark as skip regardless of tech match):**
- Requires languages the candidate doesn't speak
- Contract type mismatch (permanent when freelance-only, employee leasing, etc.)
- Primary stack is a technology the candidate has no experience with
- Requires deep expertise in tools the candidate doesn't know

**Status values:**
- `applied` — application sent
- `shortlisted` — worth applying, high fit
- `maybe` — borderline, worth exploring
- `skip` — not a match
- `dead` — was a match but disqualified (e.g. requirement discovered later)

### Step 6: Output Results Table

Present results as a markdown table:

```markdown
## Job Scan — [portal] — [date]

Query: [query] | Period: last N days | Filter: [filters applied]
Found: X total | Z cached | **N new**

### New Listings

| # | Role | Company | Start | Duration | Key Skills | Fit | Status | Link |
|---|------|---------|-------|----------|------------|-----|--------|------|
| 1 | ... | ... | ... | ... | ... | 80% | shortlisted | [Details](URL) |

### Shortlist (including previously cached high-fit ads)

| Priority | Role | Company | Fit | Status | Link |
|----------|------|---------|-----|--------|------|
| 1 | ... | ... | 80% | shortlisted | [Details](URL) |
```

The **Shortlist** section should include ALL ads with status `shortlisted` or `applied` from both new evaluations AND the cache — this gives a running view of actionable opportunities.

### Step 7: Update Cache

Append all newly evaluated ads to the cache file. Use the Edit tool to add rows to the table in `cache.md`.

**Important:**
- Preserve all existing cache entries
- Add new entries at the bottom of the table
- Update the "Last updated" date at the top
- Use the **ad's posting date** (from the listing) for the "Ad Date" column, not the scan date
- Store the **detail page URL** in the "URL" column as a markdown link. Use `—` if no URL was extracted.
- If an existing cached ad needs a status change (e.g., user says "I applied to this one"), update that row

### Step 7b: Pipeline Auto-Propose

After updating the cache, collect all **newly-evaluated** roles (scored in this run) with fit ≥80%.

1. Read `data/job-pipeline.md` (skip silently if it doesn't exist).
2. Filter shortlisted roles to those NOT already in the pipeline:
   - Match by company name substring (case-insensitive) — if the role's company appears anywhere in the pipeline's Company column, it's already tracked.
3. If no untracked shortlisted roles remain, skip silently.
4. If any untracked shortlisted roles remain, display a prompt **before** the Summary section:

   ```
   📋 [N] shortlisted role(s) not yet in pipeline:
   1. [Company] — [Role] (fit: N%) — Add to pipeline? (Y/N)
   2. [Company] — [Role] (fit: N%) — Add to pipeline? (Y/N)
   ```

5. For each role where user answers Y:
   - Append a new row to the Active section of `data/job-pipeline.md`:
     - **Company**: company name from the listing
     - **Role**: role title from the listing
     - **Stage**: `Researching`
     - **Date Added**: today (YYYY-MM-DD)
     - **Date Updated**: today
     - **CV Used**: `—`
     - **URL**: listing URL if available
     - **Notes**: `Added by /scan-jobs on [today's date]`
   - Write the updated `data/job-pipeline.md`.
   - Confirm: "✅ [Company] — [Role] added to pipeline [Researching]."

6. For roles where user answers N: skip, no changes.
7. If `data/job-pipeline.md` doesn't exist and user answers Y: create it with the standard header before adding the first entry.

### Step 8: Summary

End with a brief summary:
- How many new ads found
- How many worth applying to
- Any notable trends, but only if the lookback window covers multiple days (e.g., "strong demand for [skill] this week", "thin market for [technology]-only roles"). Skip trend observations for short lookback windows where the sample is too small.
- Remind user they can update ad status with: "mark [title] as applied"
