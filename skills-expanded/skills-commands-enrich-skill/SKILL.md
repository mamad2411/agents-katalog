---
name: enrich
description: "Enrich a CSV or XLSX prospect list by filling missing columns through an interview-driven workflow. Interviews the user to understand what each empty or new column should contain, how it should be formatted, and in what priority order to research it. Then uses a Clay-style waterfall research strategy (Apollo MCP, web search, company websites, LinkedIn) to populate every row with sourced, validated data. Adds a resource column with hyperlinks to all sources. Runs the humanizer skill on any conversational or sentence-style outputs. Use this skill whenever the user says 'enrich this CSV', 'enrich this list', 'fill in missing columns', 'enrich prospects', 'add data to my spreadsheet', 'research these companies', 'fill in the blanks', 'enrich my export', 'add enrichment columns', or has an Apollo/prospect CSV with empty columns they want populated. Also trigger when the user uploads or references a CSV/XLSX of contacts or companies and wants additional data added to it."
---

# CSV Enrichment Pipeline

Interview-driven enrichment for prospect lists. Takes a CSV/XLSX with missing or empty columns, interviews the user to understand exactly what each column needs, then researches and fills every row using a waterfall strategy with full source attribution.

## Before You Start

### 1. Load and Inspect the File

Read the file the user provides. Accept `.csv` or `.xlsx` only — if they provide another format, ask them to export as CSV or XLSX first.

Inspect the data:
- List all column headers
- Count total rows
- Identify which columns have missing/empty values and what percentage is empty
- Show a preview of the first 3-5 rows so the user can confirm it's the right data
- Note any columns that look like they came from Apollo (e.g., `Organization Name`, `Title`, `Email`, `LinkedIn Url`, `# Employees`, `Industry`)

### 2. Interview: Understand Each Column

This is the most important step. For each column that has missing values, and for any new columns the user wants to add, ask these questions. Group them into a single structured interview rather than asking one-at-a-time — present all the columns at once and let the user respond in bulk.

**For each column, clarify:**

1. **What does this column represent?** — What specific information should go here? (e.g., "Pain Points" could mean company-level operational pain, or the individual contact's personal frustrations — these require very different research)
2. **What format should the output be in?** — Short phrase, full sentence, bullet list, URL, number, date, boolean, comma-separated tags? If sentence/conversational, it will automatically be run through the humanizer skill.
3. **Where should we look first?** — Apollo data, company website, LinkedIn, news articles, job postings, social media? The user may know the best source for certain columns.
4. **What's the fallback if we can't find it?** — Leave blank, use a default value, mark as "Not Found", or infer from other data?
5. **Any specific instructions?** — Character limits, tone, things to avoid, specific angles to take?

**Always ask about new columns the user wants to add.** Common additions for outbound enrichment:
- Pain points / challenges
- Recent news or triggers
- Personalized opener line
- Tech stack gaps
- Hiring signals
- Competitive landscape
- Recent funding / growth signals

**Ask about priority order.** Which columns matter most? This determines the order of research — high-priority columns get researched first when token budget is tight. If the user doesn't have a strong preference, default to: identifying information > company context > pain signals > personalization hooks.

### 3. Confirm the Enrichment Plan

Before researching anything, present a summary back to the user:

```
Enrichment Plan
===============
File: [filename] — [X] rows

Columns to enrich (in priority order):
1. [Column Name] — [what it means] — Format: [format] — Source: [primary source] — Fallback: [fallback]
2. [Column Name] — ...
3. ...

New columns to add:
- Resources — hyperlinks to all sources used for each row's enrichment

Estimated Apollo credits: [X] (if Apollo enrichment needed)
Estimated research scope: [light/moderate/deep] per row

Proceed?
```

Wait for user confirmation before starting any research.

---

## Enrichment Strategy

### Waterfall Research

For each row, research columns in priority order using this source hierarchy. Stop at the first source that returns confident, usable data for each column — don't burn tokens re-researching what you already found.

**Source priority (waterfall):**

1. **Existing file data** — Check if other columns in the same row already contain the answer. Cross-reference before hitting external sources. For example, if the user wants "Industry" enriched but the company description column already mentions the industry, extract it from there.

2. **Apollo MCP** — Use `apollo_organizations_enrich` for company-level data (industry, revenue, employee count, tech stack, funding). Use `apollo_people_match` for contact-level data (title, email, LinkedIn, employment history). Apollo is the most reliable source for structured firmographic data.
   - **Credit awareness:** Each enrichment call costs 1 credit. Before making Apollo calls, check how many rows actually need Apollo data vs. what can be sourced elsewhere. Always confirm credit spend with the user if it exceeds 10 credits.
   - **Batch when possible:** Use `apollo_organizations_bulk_enrich` for company data (up to 10 domains per call) to save on API overhead.

3. **Web search** — Search for the company name + relevant keywords for the column being researched. Good for: recent news, press releases, blog posts, product launches, hiring pages, pain signals, competitive landscape.

4. **Company website** — Fetch the company's homepage, about page, careers page, or blog directly. Good for: mission/values, product descriptions, team size indicators, job postings (hiring signals), customer testimonials.

5. **LinkedIn** — Search for the person's LinkedIn activity or company page. Good for: recent posts, engagement topics, career history, mutual connections, content they've published.

**Fallback chain:** If the primary source returns nothing, move to the next source in the waterfall. If all sources fail, apply the fallback the user specified during the interview (blank, default value, "Not Found", or inferred).

### Processing Approach

Process rows in batches of 5-10 to balance thoroughness with token efficiency:

1. **Batch Apollo calls first** — Collect all domains that need enrichment, deduplicate, and run bulk enrichment. This gets the structured data upfront.
2. **Web research in parallel** — For columns that need web research (pain points, news, personalization), spawn background research agents splitting the rows between them (3-5 rows per agent). Each agent researches all web-dependent columns for its assigned rows.
3. **Fill and validate** — After research completes, fill each cell. For any column marked as sentence/conversational format, run the output through the `/humanizer` skill before writing it to the cell.
4. **Source tracking** — For every piece of researched information, record the source URL. Aggregate all source URLs for each row into the `Resources` column as a comma-separated list of hyperlinks.

### Source Attribution

Every enriched cell must be traceable. Maintain a `Resources` column (add it if it doesn't exist) that contains hyperlinks to the sources used for that row's enrichment.

Format for the Resources column:
```
[Apollo](https://app.apollo.io/#/people/...), [Company Blog](https://example.com/blog/post), [LinkedIn](https://linkedin.com/in/...)
```

If a cell's value was inferred from existing data (not externally researched), note the source column instead:
```
Inferred from "Company Description" column
```

If a cell uses the fallback value, mark it:
```
Fallback: [reason not found]
```

### Humanizer Integration

Any column whose format is "sentence", "paragraph", "conversational", or any natural-language prose (as opposed to structured data like numbers, tags, URLs, or short phrases) must be run through the `/humanizer` skill before being written to the file.

This applies to columns like:
- Personalized opener lines
- Pain point summaries
- Company descriptions (if rewritten)
- Outreach angle descriptions
- Any "summary of..." column

Short factual phrases ("Series B, $12M raised") do NOT need humanizing. Use judgment — if it reads like something a human would write in a cold email or CRM note, humanize it.

---

## Writing the Output

### Same File, Enriched

Write the enriched data back to the **same file** the user provided. If it's a CSV, write CSV. If XLSX, write XLSX.

Before overwriting:
1. Create a backup copy at `[filename]_backup_[timestamp].[ext]` in the same directory
2. Confirm with the user: "I'll write the enriched data back to [filename]. A backup has been saved at [backup path]. Proceed?"

### Progress Reporting

After enrichment is complete, present a summary:

```
Enrichment Complete
===================
Rows processed: [X]
Columns enriched: [list]
New columns added: [list]

Fill rates:
- [Column 1]: [X]% filled ([Y] rows enriched, [Z] fallbacks used)
- [Column 2]: [X]% filled ...

Apollo credits used: [X]
Sources referenced: [total unique URLs]

Backup saved at: [path]
Output written to: [original path]
```

If any rows had particularly low fill rates or relied heavily on fallbacks, flag them so the user can review manually.

---

## Email Verification

After enrichment, if the CSV contains an email column, offer to verify emails via MillionVerifier. This catches invalid addresses before the user wastes time personalizing dead leads.

### Running Verification

Use the bundled script at `scripts/verify_emails.py`:

```bash
python /home/jared/.claude/commands/enrich/scripts/verify_emails.py <csv_path> --email-column "Email"
```

This requires the `MILLIONVERIFIER_API_KEY` environment variable. If it's not set, tell the user:
> "To verify emails, set your MillionVerifier API key: `export MILLIONVERIFIER_API_KEY=your_key`. Get one at https://app.millionverifier.com/api"

The script:
1. Extracts all emails from the specified column
2. Uploads them to MillionVerifier's bulk API
3. Polls until verification completes (usually 1-2 minutes for <50 emails)
4. Downloads results and adds an `Email Status` column to the CSV

**Email Status values:** `ok`, `catch_all`, `unknown`, `invalid`, `disposable`

After verification, report the results:
```
Email Verification Complete
===========================
OK (safe to send):    [X]
Catch-all (proceed):  [X]
Unknown (risky):      [X]
Invalid (drop):       [X]
Disposable (drop):    [X]
```

Recommend the user drop `invalid` and `disposable` rows before outreach. `catch_all` is generally safe but deliverability varies. `unknown` should be sent cautiously or verified individually.

---

## Master Outreach CSV

Every enriched and verified prospect should be logged to a master outreach CSV that persists across batches. This is the single source of truth for the entire outbound pipeline.

### Master CSV Location

```
/home/jared/docs/Documents/2. Areas/2.1 Startup & Business/Riven/6. Customer Validation/Apollo Prospecting/outreach_master.csv
```

### Master CSV Columns

| Column | Description | Set By |
|--------|-------------|--------|
| First Name | Contact first name | Apollo/enrich |
| Last Name | Contact last name | Apollo/enrich |
| Email | Verified email | Apollo/enrich |
| Email Status | MillionVerifier result | verify script |
| Title | Job title | Apollo/enrich |
| Company | Company name | Apollo/enrich |
| Website | Company domain | Apollo/enrich |
| Industry | Company industry | Apollo/enrich |
| # Employees | Company size | Apollo/enrich |
| LinkedIn Url | Contact LinkedIn | Apollo/enrich |
| Pain Points | Researched pain signals | enrich |
| Personalized Opener | Cold email first line | enrich |
| Outreach Status | `ready` / `sent` / `replied` / `bounced` / `opted_out` | manual/tracking |
| Date Added | When prospect was enriched | enrich (auto) |
| Date First Sent | When first email was sent | manual |
| Touch Count | Number of outreach attempts | manual (increment) |
| Last Touch Date | Date of most recent touch | manual |
| Channel | `email` / `linkedin` / `both` | manual |
| Response | Brief note on reply content | manual |
| Batch ID | Which enrichment batch this came from | enrich (auto) |
| Resources | Source URLs from enrichment | enrich |

### Appending to Master CSV

After enrichment and verification are complete:

1. **Check if master CSV exists.** If not, create it with the headers above.
2. **Deduplicate.** Check the master CSV for existing emails — don't add duplicates. Report any skipped: "3 prospects already in master CSV, skipped."
3. **Set auto fields:**
   - `Date Added` = today's date (YYYY-MM-DD)
   - `Batch ID` = `batch_YYYYMMDD_N` (increment N if multiple batches same day)
   - `Outreach Status` = `ready` (if email is ok/catch_all) or `hold` (if unknown) or `invalid` (if invalid/disposable)
   - `Touch Count` = 0
4. **Append rows** to the master CSV.
5. **Report:** "Added X prospects to master outreach CSV. Y skipped (duplicates). Master total: Z prospects."

### Updating the Master CSV

When the user reports touchpoints ("I sent emails to batch X", "got a reply from Sarah"), update the relevant rows:
- Increment `Touch Count`
- Update `Last Touch Date`
- Update `Outreach Status` (`sent`, `replied`, `bounced`, `opted_out`)
- Add `Response` notes

The master CSV is append-only for new prospects and update-in-place for status changes. Never delete rows — mark them `opted_out` or `invalid` instead.

---

## Important Notes

- **Never enrich without confirming the plan.** The interview and confirmation step is mandatory — don't skip it even if the columns seem obvious.
- **Apollo credits cost real money.** Always surface credit usage before and after. Use bulk enrichment to minimize calls.
- **Token efficiency matters.** Don't research 50 rows sequentially — batch Apollo calls and parallelize web research. For large lists (30+ rows), suggest splitting into priority tiers and enriching the top tier first.
- **The humanizer skill is not optional for prose.** If a column produces natural language, it must go through `/humanizer`. This is what makes the outbound actually sound human.
- **Validate before writing.** Spot-check a few enriched rows and show them to the user before writing the full file. This catches systematic issues early (wrong column interpretation, bad formatting, irrelevant research).
- **Source everything.** The Resources column is not optional. Every row must have source attribution. This builds trust with the user and lets them verify the data before using it in outreach.
