---
name: greenhouse-match
description: Match a resume against open Databricks positions to find best-fit roles. Use when someone wants to find matching job openings for a candidate or referral.
user-invocable: true
---

# Greenhouse Resume Matcher

Match a resume against open Databricks job positions and return a tiered list of best-fit roles. Uses the public Greenhouse Boards API — no authentication required.

## Step 1: Parse Arguments

The user may invoke this skill with arguments:

```
/greenhouse-match ~/resumes/jane.pdf
/greenhouse-match ~/resumes/jane.pdf --department=Engineering --location=Austin
/greenhouse-match   (no args — interactive mode)
```

Parse any provided arguments to extract:
- **Resume source:** A file path (any argument not starting with `--`)
- **Filters:** `--department=<name>` and/or `--location=<name>`

If no resume source was provided, ask the user:

> **Please provide a path to the resume file** (PDF, plain text, or DOCX if pandoc is installed):

If no filters were provided, ask:

> **Would you like to filter by department or location?** (Press Enter to search all open positions)
>
> - Department: (e.g., Engineering, Field Engineering, Sales, Product)
> - Location: (e.g., San Francisco, Austin, Remote)

## Step 2: Load Resume Content

Use the Read tool to read the file at the provided path.

- PDF files and plain text files are supported natively by the Read tool.
- If the file appears to be a DOCX file (ends in `.docx`), first try the Read tool. If it returns garbled content, attempt conversion via Bash:

```bash
pandoc "/path/to/file.docx" -t plain
```

If pandoc is not installed, tell the user:

> **DOCX files require pandoc for conversion.** Either:
> - Install pandoc: `brew install pandoc`
> - Or convert the resume to PDF or plain text and try again

Then STOP.

After reading the file, extract and summarize these attributes from the resume content:
- **Name** of the candidate
- **Skills and technologies** (programming languages, tools, frameworks, certifications)
- **Job titles and roles** held
- **Years of experience** (total and per role)
- **Industries and domains** worked in
- **Education** (degrees, institutions, fields of study)
- **Location** (if mentioned)

Hold this summary as the **candidate profile** for use in later steps.

## Step 3: Fetch Open Jobs from Databricks

Fetch all open Databricks positions from the Greenhouse public boards API. No authentication is required.

**Fetch the summary job list:**

```bash
curl -s "https://boards-api.greenhouse.io/v1/boards/databricks/jobs"
```

The response is a JSON object with a `jobs` array. Each job object contains:
- `id` — job ID
- `title` — job title
- `location.name` — location string
- `metadata` — array of metadata objects
- `absolute_url` — direct link to the job posting
- `updated_at` — last update timestamp

**Extracting department:** The department is in the `metadata` array. Look for the object where `name` is `"Career Page Posting Category"` — its `value` field contains the department name (may be a list).

**From each job, extract and store:**
- `id` — job ID (needed for fetching full description later)
- `title` — job title
- Department — from `metadata` where `name == "Career Page Posting Category"`
- `location.name` — location string
- `absolute_url` — job post URL

Tell the user how many open jobs were found:

> **Found [N] open positions at Databricks.**

If zero jobs found (unlikely but possible):
> **No open positions found. The Greenhouse API may be temporarily unavailable — try again in a few minutes.**
Then STOP.

## Step 4: Pre-Filter Jobs (Coarse Pass)

Narrow the full job list down to ~20-30 candidates for deep analysis.

### 4a: Apply Hard Filters

If the user specified `--department` or `--location`:

- Filter the job list to only include jobs where the department matches the department filter (case-insensitive substring match)
- Filter the job list to only include jobs where `location.name` matches the location filter (case-insensitive substring match)

If a filter matches zero jobs, check for fuzzy matches. Collect all unique department or location values from the full job list and present them:

> **No jobs found in department "[X]". Available departments:**
> - Engineering
> - Field Engineering
> - Sales
> - Product
> - ...
>
> **Did you mean one of these?**

Wait for the user to clarify, then re-apply the filter.

Report after hard filtering:

> **After applying filters: [N] positions remain.**

### 4b: Coarse Match Against Candidate Profile

Now review the remaining jobs against the candidate profile from Step 2. For each job, evaluate based on its title, department, and location:

**Keep the job if ANY of these are true:**
- The job title relates to the candidate's career track (e.g., candidate is a software engineer and job is "Senior Backend Engineer")
- The job's department aligns with the candidate's industry or domain experience
- The job title contains skills or keywords that appear in the candidate's profile
- You are uncertain whether the candidate is a fit — when in doubt, keep it

**Remove the job ONLY if ALL of these are true:**
- The job function is clearly unrelated to the candidate's career track (e.g., candidate is an engineer, job is "Senior Accountant" or "Graphic Designer")
- The seniority level is clearly misaligned (e.g., "VP of Engineering" for a candidate with 2 years of experience, or "Intern" for a candidate with 15 years)
- There is no reasonable transferable skill overlap

**Target: ~20-30 jobs.** If more than 30 remain, tighten the coarse criteria slightly. If fewer than 10 remain, loosen them — the deep matching step will handle precision.

Report:

> **Pre-filter complete: [N] positions selected for detailed analysis.**

## Step 5: Fetch Full Job Descriptions for Shortlisted Positions

For each shortlisted job from Step 4, fetch the full job details:

```bash
curl -s "https://boards-api.greenhouse.io/v1/boards/databricks/jobs/<JOB_ID>"
```

Insert a 200ms pause between requests to be respectful of the public API.

From each job response, extract:
- `title` — the job title
- `content` — the full HTML job description
- `location.name` — location string
- `absolute_url` — direct link to the job posting (save for detailed report)

**Important: The `content` field is double HTML-entity-encoded.** Before using it, decode HTML entities twice to get clean text, then strip any remaining HTML tags. Use Bash:

```bash
python3 -c "
import html, re, sys, json
data = json.load(sys.stdin)
content = data.get('content', '')
decoded = html.unescape(html.unescape(content))
plain = re.sub(r'<[^>]+>', ' ', decoded)
plain = re.sub(r'\s+', ' ', plain).strip()
print(plain)
"
```

If a job returns an error or empty content, skip it and note it was excluded.

## Step 6: Deep Match & Score

Now perform detailed matching. Process the shortlisted jobs in batches of 5-10 (use smaller batches when job descriptions are long, larger batches when they are short).

**For each batch of up to 5-10 jobs**, evaluate each job against the candidate profile across these dimensions:

### Scoring Rubric

**Skills Alignment (0-30 points):**
- 25-30: Candidate has nearly all required skills and several preferred skills
- 15-24: Candidate has most required skills, missing some preferred
- 5-14: Candidate has some required skills, significant gaps
- 0-4: Minimal skill overlap

**Experience Level (0-25 points):**
- 20-25: Years of experience and seniority match well
- 10-19: Reasonable match with minor seniority gap
- 5-9: Notable seniority mismatch but not disqualifying
- 0-4: Major seniority mismatch

**Domain Relevance (0-25 points):**
- 20-25: Same industry/domain, directly relevant experience
- 10-19: Related domain, transferable experience
- 5-9: Different domain but some transferable knowledge
- 0-4: Unrelated domain

**Location Fit (0-20 points):**
- 20: Remote role, or candidate is in the same city/region
- 15: Candidate is in a nearby region or role offers relocation
- 10: Different region but role may support remote
- 0-5: Location mismatch with no remote option mentioned

**Total: 0-100 points**

### Tier Assignment

- **Strong Fit (75-100):** Candidate meets most or all requirements
- **Possible Fit (50-74):** Meaningful overlap with notable gaps
- **Stretch (25-49):** Some transferable skills but significant gaps
- **Drop (below 25):** Do not include in results

For each job, record:
- The composite score
- The tier
- A one-line rationale summarizing the key reason for the score (e.g., "Strong Python/Go overlap, 7+ years matches requirement, distributed systems experience")

After scoring all batches, select the **top 10 highest-scoring jobs** and group them by tier.

## Step 7: Present Results

Display the top 10 matches grouped by tier. Only show tiers that have jobs in them.

**Format:**

```
## Resume Match Results for [Candidate Name]

**[N] open positions analyzed, [M] shortlisted, top 10 shown.**

### Strong Fit

1. **[Job Title]** ([Location])
   Score: [XX] | Department: [Department Name]
   → [One-line rationale]

2. **[Job Title]** ([Location])
   Score: [XX] | Department: [Department Name]
   → [One-line rationale]

### Possible Fit

3. **[Job Title]** ([Location])
   Score: [XX] | Department: [Department Name]
   → [One-line rationale]

...

### Stretch

8. **[Job Title]** ([Location])
   Score: [XX] | Department: [Department Name]
   → [One-line rationale]

---

To see a detailed analysis for any position, ask:
"Show me the detailed report for #3"
```

**Numbering is continuous across tiers** (1-10, not restarting per tier).

If no jobs scored above 25:

> **No positions scored above the minimum fit threshold.**
>
> This could mean:
> - The resume doesn't align well with currently open positions
> - Filters were too narrow — try removing department/location filters
> - The resume may be missing key details — ensure it includes skills, experience, and education

## On-Demand: Detailed Report

When the user asks for a detailed report on a specific match (e.g., "Show me the detailed report for #3"), generate the following analysis using the job data already in context from Step 5. **Do not make any additional API calls.**

**Format:**

```
## Detailed Match Report: [Job Title] (#[Rank])

**Score:** [XX]/100 | **Tier:** [Strong Fit / Possible Fit / Stretch]
**Department:** [Department] | **Location:** [Location]
**Apply:** [absolute_url from the job data]

### Strengths
- [Specific skill/experience that matches a job requirement]
- [Another strength with reference to both resume and job post]
- ...

### Gaps
- [Skill or experience the job requires that the candidate lacks]
- [Another gap, with severity: minor/moderate/significant]
- ...

### Talking Points
Highlights to emphasize in an application or referral note:
- [Concrete achievement from the resume that maps to a job requirement]
- [Transferable experience that may not be obvious]
- ...

### Score Breakdown
| Dimension        | Score | Notes                          |
|-----------------|-------|--------------------------------|
| Skills Alignment | XX/30 | [Brief note]                  |
| Experience Level | XX/25 | [Brief note]                  |
| Domain Relevance | XX/25 | [Brief note]                  |
| Location Fit     | XX/20 | [Brief note]                  |
| **Total**        | **XX/100** |                          |
```

## Error Handling Reference

Throughout execution, apply these error handling rules:

### API Errors
- **Network error / timeout:** Retry the request once. If it fails again, report the error and suggest checking connectivity.
- **Unexpected JSON / non-JSON response:** Report the raw response and suggest trying again in a few minutes — the public API may be temporarily unavailable.
- **HTTP 429 (rate limit):** Back off 10s → retry. If 429 again, 30s → retry. Third 429 → STOP and report. This is unlikely with the public API but handle it gracefully.

### Input Errors
- **File not found:** Tell the user the path doesn't exist and ask them to check it.
- **Unreadable file content:** Suggest converting to PDF or plain text.
- **DOCX without pandoc:** Suggest `brew install pandoc` or converting to PDF.

### Processing Edge Cases
- **Zero open jobs:** Report clearly — the API may be temporarily unavailable.
- **Zero open jobs after filters:** Suggest relaxing filters, show available departments/locations.
- **Zero matches above threshold:** Report with suggestions (broaden filters, review resume).
- **Job detail fetch failure:** Skip that job silently — note it was excluded.
- **Very large job pool (500+):** This is handled naturally by pre-filtering. Log the counts for user visibility.
