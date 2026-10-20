---
name: gh-contribution-report
description: 從 GitHub 組織抓取 commits 與 PRs，生成詳細月報與年報至 Obsidian vault。觸發關鍵詞：「貢獻報告」、「contribution report」、「年報」、「月報產出」、「GitHub 貢獻」。
metadata:
  version: 1.0.1
---

# GitHub Contribution Report Generator

Generate detailed monthly and annual reports from GitHub contributions across multiple organizations.

## Overview

This skill fetches commit and PR data from GitHub organizations via `gh` CLI, organizes them by month, and generates structured Obsidian Markdown reports with:
- Per-commit detail tables
- PR listings with status and links
- Weekly/phase-based activity analysis
- Cross-organization statistics
- Annual summary with monthly navigation

## Input

User provides:
- **Organizations**: one or more GitHub org names (e.g., `gorilla-ai sq-postevent sq-icctv`)
- **Year**: target year (e.g., `2025`)
- **Report type** (optional): `annual`, `monthly`, or `both` (default: `both`)
- **Specific months** (optional): generate only certain months (e.g., `03 04 05`)

### Usage Examples

```
/gh-contribution-report gorilla-ai sq-postevent sq-icctv 2025
/gh-contribution-report gorilla-ai 2025 monthly 03-06
/gh-contribution-report sq-postevent 2025 annual
```

## Configuration

- **GitHub username**: `ricky1698` (from CLAUDE.md)
- **Reports directory**: `Areas/reports/`
  - Monthly: `Areas/reports/Monthly/YYYY-MM.md`
  - Annual: `Areas/reports/Annual/YYYY.md`
- **Monthly report template**: `./Templates/Monthly Report Template.md` (if exists)

## Workflow

### Phase 1: Data Collection

1. **Fetch commits** for each organization, handling the 100-result API limit by splitting date ranges:

   ```bash
   # First half of year
   gh search commits --author=ricky1698 \
     --committer-date=2025-01-01..2025-06-30 \
     --limit 100 \
     --json repository,sha,commit \
     -- "org:<org-name>"

   # Second half of year
   gh search commits --author=ricky1698 \
     --committer-date=2025-07-01..2025-12-31 \
     --limit 100 \
     --json repository,sha,commit \
     -- "org:<org-name>"
   ```

   > [!important] Pagination Strategy
   > The GitHub search API returns max 100 results per query.
   > If a query returns exactly 100 results, split the date range further
   > (e.g., by quarter or month) to ensure complete data.

2. **Fetch PRs** for each organization:

   ```bash
   gh search prs --author=ricky1698 \
     --created=2025-01-01..2025-12-31 \
     --limit 100 \
     --json repository,title,state,createdAt,url \
     -- "org:<org-name>"
   ```

3. **Sort and parse** results using `jq`:

   ```bash
   # Sort commits by date and extract fields
   | jq -r '.[] | "\(.commit.committer.date[:10])|\(.repository.fullName)|\(.commit.message | split("\n")[0])"' | sort

   # Sort PRs by date and extract fields
   | jq -r '.[] | "\(.createdAt[:10])|\(.repository.fullName)|\(.state)|\(.title)|\(.url)"' | sort
   ```

4. **Run all org queries in parallel** to minimize wait time.

### Phase 2: Data Organization

1. **Group by month**: parse dates and bucket commits/PRs into `YYYY-MM` groups.
2. **Group by repository** within each month.
3. **Classify commit types** from conventional commit prefixes:
   - `feat:` → feat
   - `fix:` → fix
   - `chore:` → chore
   - `docs:` → docs
   - `refactor:` → refactor
   - `test:` → test
   - `Merge pull request` → — (merge)
   - No prefix → — (general)

### Phase 3: Monthly Report Generation

For each month with activity, generate or update `Areas/reports/Monthly/YYYY-MM.md`.

#### New Monthly Report Structure

```markdown
# Monthly Report - YYYY-MM

> [!info] Owner: <owner> | Period: YYYY-MM-01 ~ YYYY-MM-DD

## Summary

<1-2 sentence summary of the month's focus areas>

---

## <org>/<repo>

### Commits (N)

| Date | Type | Description |
|------|------|-------------|
| MM-DD | feat | commit message |
| MM-DD | fix | commit message |

### Pull Requests (N)

| Date | Status | Title | Link |
|------|--------|-------|------|
| MM-DD | ✅ Merged | PR title | [PR #N](url) |
| MM-DD | ❌ Closed | PR title | [PR #N](url) |
| MM-DD | 📌 Open | PR title | [PR #N](url) |

### Key Activities

<Narrative description organized by week or theme>

---

## <next org/repo section>

...

---

## Statistics

| Organization | Repository | Commits | PRs |
|---|---|---|---|
| org | repo | N | N |
| **Total** | | **N** | **N** |
```

#### Key Activities Writing Guidelines

- **If >= 10 commits**: organize by **week** (`Week 1 (MM-DD ~ MM-DD): Theme`)
- **If large project milestones**: organize by **phase** (e.g., Phase 1-5)
- **If < 10 commits**: use bullet points per activity
- Include **technical context**: why decisions were made, what problems were solved
- Use bold for key terms and feature names

#### Updating Existing Monthly Reports

When a monthly report already exists (e.g., contains Crypto Analysis Objectives data):

1. **DO NOT overwrite** the existing content
2. **Append** a new section before `## Notes`:

   ```markdown
   ---

   ## GitHub Contributions

   ### <org>/<repo>

   | Date | Type | Description |
   |------|------|-------------|
   ...

   ### Key Activities
   ...

   ### Statistics

   | Organization | Repository | Commits | PRs |
   |---|---|---|---|
   ...
   ```

3. Preserve all existing Objectives, Key Achievements, Issues/Blockers, Learned, Notes sections.

### Phase 4: Annual Report Generation

Generate `Areas/reports/Annual/YYYY.md` as a high-level summary.

#### Annual Report Structure

```markdown
# Annual Report - YYYY

> [!info] Owner: <owner> (<gh-handle>) | Period: YYYY-01 ~ YYYY-12

---

## Summary

<Overall narrative: how many orgs, major themes, total commits/PRs>

---

## GitHub Contribution Overview

| Organization | Repositories | Commits | PRs (Merged/Open/Closed) |
|---|---|---|---|
| org | N | N | N (M/O/C) |
| **Total** | **N** | **N** | **N (M/O/C)** |

---

## Project Highlights by Organization

### <org> — <project/theme>

> <1-line project description>

#### Q1 (Jan–Mar): <Theme>
- bullet points of key work

#### Q2 (Apr–Jun): <Theme>
...

#### Key Technical Decisions
- decision rationale pairs

---

## Cross-Organization Themes

### 1. <Theme Name>
- patterns observed across orgs

---

## Monthly Reports

| Month | Focus | Commits | PRs |
|-------|-------|---------|-----|
| [[YYYY-01\|01]] | summary | N | N |
...

---

## Statistics

### Commits by Month (<org>/<repo>)

| Month | Commits | Focus Area |
|-------|---------|------------|
...
```

#### Annual Report Writing Guidelines

- **Quarterly grouping** for project narratives (Q1/Q2/Q3/Q4)
- **Cross-org themes**: identify patterns (e.g., CI/CD, observability, modernization)
- **Monthly Reports table**: wikilinks to each monthly report with focus summary
- **Research/exploration**: if applicable, link to monthly reports with research content

### Phase 5: Validation

After generating all reports:

1. **List all created/updated files** with summary
2. **Verify monthly report count** matches months with activity
3. **Cross-check totals**: sum of monthly commits should ≈ annual total
4. **Check for wikilink consistency**: all monthly report wikilinks use shortest form (e.g. `[[YYYY-MM\|MM]]`) and point to existing files

## Important Notes

### API Limitations

- `gh search commits` returns max **100 results** per query
- If any query returns exactly 100, **split the date range** and re-query
- Run queries for different orgs and date ranges **in parallel**
- PR search also has 100-result limit (rarely hit for individual authors)

### Commit Message Parsing

- Extract only the **first line** of multi-line commit messages
- Strip conventional commit prefix for the Type column
- Merge commits (starting with "Merge pull request") get Type `—`

### PR Status Icons

| State | Icon |
|-------|------|
| merged | ✅ Merged |
| closed | ❌ Closed |
| open | 📌 Open |

### Obsidian Compatibility

- Use `[[YYYY-MM\|MM]]` for wikilinks with display text in tables (Quartz shortest form; no path prefix)
- Use `> [!info]`, `> [!important]`, `> [!note]` for callouts
- Tags: `#project/<name>`, `#status/<state>`
- Keep all reports in `Areas/reports/` directory hierarchy

### Idempotency

- Running the skill again for the same period should produce consistent results
- New data (e.g., merged PRs since last run) will be reflected in updated reports
- Existing non-GitHub content in monthly reports is preserved
