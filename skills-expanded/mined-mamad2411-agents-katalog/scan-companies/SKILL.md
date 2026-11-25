---
name: scan-companies
description: Scan target company career pages for matching roles, score against profile, write new matches to inbox
argument-hint: [--dry-run]
user-invocable: true
allowed-tools: Bash(*), Read(*), Write(data/inbox.md), Write(data/scan-targets.yaml)
---

# Scan Target Company Career Pages

Scan all active companies in `data/scan-targets.yaml`, fetch open roles from their career pages (via ATS APIs or Playwright), score each role against `data/profile.md` and `data/goals.md`, deduplicate against `data/job-pipeline.md`, and write new matches to `data/inbox.md`.

## Arguments

`$ARGUMENTS` accepts an optional `--dry-run` flag. When passed, the scanner fetches and scores roles but does not write to inbox. Useful for previewing results or calibrating scores.

## Instructions

### Step 0: Profile Guard

Verify both `data/profile.md` and `data/goals.md` exist and contain real content (not just TODO placeholders).

- If `data/profile.md` is missing or empty: STOP. Tell the user: "data/profile.md is missing or incomplete. Run `/import-cv` first to populate your profile, or manually create data/profile.md with your name, background, and career context."
- If `data/goals.md` is missing or all TODOs: STOP. Tell the user: "data/goals.md is missing or incomplete. Copy framework/templates/goals.md to data/goals.md and fill in your search thesis and target criteria before running skills."

### Step 1: Verify Scan Targets

Read `data/scan-targets.yaml`. If the file does not exist or contains no active companies (all have `active: false`), tell the user:

"No active scan targets configured. Edit `data/scan-targets.yaml` to add companies. See Step 5 below for how to find ATS slugs and configure entries."

Then stop.

### Step 2: Run Scanner

Execute the scanner CLI:

```bash
PYTHONIOENCODING=utf-8 python3 tools/career_scanner/cli.py --repo-root .
```

If the user passed `--dry-run`, add that flag:

```bash
PYTHONIOENCODING=utf-8 python3 tools/career_scanner/cli.py --repo-root . --dry-run
```

The CLI outputs JSON to stdout with keys: `total_fetched`, `new_roles`, `skipped_dupes`, `companies_scanned`, `top_roles`.

Status messages appear on stderr (scanning progress per company).

### Step 3: Present Results

Parse the JSON output. Present results as a formatted table sorted by score descending:

```markdown
## Scan Results - [date]

**Companies scanned:** N | **Total roles fetched:** N | **Duplicates skipped:** N | **New roles:** N

| Score | Role | Company | Location | Link |
|-------|------|---------|----------|------|
| 8/10  | Strategy & Ops Manager | Northwind | New York, NY | [View](url) |
| 7/10  | Business Operations Lead | Notion | San Francisco | [View](url) |
| ...   | ... | ... | ... | ... |
```

Show all roles per D-05 (no filtering threshold). If `--dry-run` was used, note that results were not written to inbox.

If zero new roles were found, report that clearly and suggest the user review their `role_filters` in scan-targets.yaml or add more target companies.

### Step 4: Offer Next Actions

For roles scoring 7 or higher, suggest next actions:

- "Run `/research-company [company]` to build a dossier before applying"
- "Run `/generate-cv [company] [role]` to tailor your resume"
- "Run `/pipe add [company] [role]` to add to your pipeline"

For lower-scoring roles, no specific suggestions needed, but remind the user they can review all roles in `data/inbox.md`.

### Step 5: Managing Targets

If the user asks to add or remove companies, edit `data/scan-targets.yaml` directly. **Adding a company crosses the promotion gate documented at the top of that file** (added 2026-08-26): answer *"is there anyone on this team who has done the commercial or delivery craft before?"* and record it as `bench: yes|thin|unknown`. It is a **sort signal, not a veto** - `thin` and `unknown` still get added, they rank lower, and the deciding read needs a conversation. Note this is a COMPANY-level property settled at promotion, so do NOT re-check it per-role on every scan; that is the wrong layer.

**ATS options and how to find slugs:**

| ATS | URL pattern | Example |
|-----|-------------|---------|
| Greenhouse | `boards.greenhouse.io/SLUG` | `slug: northwind` |
| Lever | `jobs.lever.co/SLUG` | `slug: netflix` |
| Ashby | `jobs.ashbyhq.com/SLUG` | `slug: contoso` |
| Generic | Full careers page URL | `careers_url: "https://example.com/careers"` |

**Entry format:**
```yaml
- name: Company Name
  ats: greenhouse       # greenhouse, lever, ashby, or generic
  slug: company-slug    # for ATS types (not needed for generic)
  careers_url: "..."    # only for generic type
  active: true          # set false to temporarily skip
  role_filters:         # empty list = all roles shown
    - "operations"
    - "strategy"
```

To find a company's ATS: visit their careers page and check the URL. If it redirects to `boards.greenhouse.io/`, `jobs.lever.co/`, or `jobs.ashbyhq.com/`, the slug is the path segment after the domain. Otherwise, use `ats: generic` with the full URL.
