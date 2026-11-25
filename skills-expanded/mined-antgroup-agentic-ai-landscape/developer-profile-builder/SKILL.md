---
name: developer-profile-builder
description: Build Top N GitHub developer profile CSVs for a project set using ClickHouse community_openrank, gh_user_info, location_info, and GitHub API fallback.
license: MIT
metadata:
  author: llm-oss-landscape
  version: "1.0"
---

Build developer profile datasets for a CSV of GitHub projects.

Use this skill when the user asks to analyze developer profiles, contributors, community OpenRank leaders, geographic distribution, company distribution, or Top N developers for a project set.

**Script**

Use `scripts/build_developer_profiles.py`.

The input CSV must include `repo_id`. Prefer repo IDs over repo names to survive repository renames.

**Default Data Sources**

- `opensource.events`: count distinct developers over a requested period.
- `opensource.community_openrank`: rank developers by monthly contribution OpenRank and identify each developer's highest-contribution repository in that month.
- `opensource.gh_user_info`: enrich profile fields.
- `opensource.location_info`: normalize raw location to city/country.
- GitHub API: only call when `gh_user_info` has no row for the actor ID.

**Output Columns**

The script writes one CSV with:

`actor_id`, `actor_login`, `openrank_YYMM`, `top_repo_name_YYMM`, `top_repo_openrank_YYMM`, `location`, `standard_city`, `standard_country`, `bio`, `email`, `company`, `name`, `created_at`, `profile_source`

**Common Command**

```bash
.venv/bin/python scripts/build_developer_profiles.py \
  --input-csv data/2605_agentic_projects.csv \
  --openrank-month 2026-04 \
  --period-start 2026-01-01 \
  --period-end 2026-05-01 \
  --limit 1000 \
  --output-csv data/2605_agentic_developer_profiles_top1000.csv
```

**Options**

- `--input-csv`: project CSV with `repo_id`; defaults to `data/agentic-ai-projects.csv`.
- `--openrank-month`: `YYYY-MM`; defaults to the previous completed month.
- `--period-start`: inclusive `YYYY-MM-DD`; defaults to Jan 1 of the OpenRank month year.
- `--period-end`: exclusive `YYYY-MM-DD`; defaults to first day after the OpenRank month.
- `--limit`: Top N developers; defaults to `1000`.
- `--output-csv`: output CSV path; if omitted, generated from input stem, Top N, and month.
- `--exclude-bots`: excludes bot-looking logins. Omit it when the user wants bots retained.
- `--no-github-fallback`: disable GitHub API fallback.
- `--schema`: inspect ClickHouse table schemas.

**Workflow**

1. Confirm project CSV, OpenRank month, period, Top N, bot inclusion, and output path.
2. Run `--schema` only when table fields are uncertain.
3. Run the build command with explicit parameters for reproducibility.
4. Report the CSV path, period, developer count, row count, and profile source counts from script stdout.
