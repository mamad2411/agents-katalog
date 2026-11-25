---
name: github-repo-analytics-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for github-repo-analytics using latest full-instruction v2 family injection.
allowed-tools:
  - github_api_query
  - github_pr_metrics
  - github_pr_search
  - list_dir
  - read_file
  - run_python
  - run_shell
  - time_window_filter
  - write_file
  - write_json
metadata:
  benchmark: SkillLearnBench
  generator: Manus
  baseline: manus_familytools_fullinstr_v2
  generation_constraints: slb_no_instance_memory_familytools_v2
  allowed_gold_input: familytools_full_instruction_v2
  skill_injection_scope: family_scoped
  date: "2026-05-23"
---

# Skill: GitHub Repository Analytics

## 1. When to use this skill
Use this skill for the `github-repo-analytics` family in SkillLearnBench. It applies when tasks require analyzing GitHub pull request (PR) activity for a specific repository over a defined time period. Typical requests involve counting total PRs, determining merged versus closed-unmerged PRs by a cutoff date, calculating average time-to-merge, and identifying the top contributor.

## 2. Visible input and artifact inventory
The primary source of truth is the visible instruction file (e.g., `instruction.md`). It contains the repository name, date range, PR filters (like minimum changed files), cutoff date, and exact output JSON schema. Other visible files may include `Dockerfile`, `docker-compose.yaml`, and `task.toml`. The expected output is usually a `report.json` file in a specified directory like `/app/`.

## 3. Execution procedure for the current task
1. Read the visible instruction file to extract the target repository, date range, PR filters, cutoff date, and output JSON schema.
2. Use GitHub API tools to query the repository for PRs created within the date range. Apply any necessary filters.
3. Analyze the filtered PRs to compute metrics: total matching PRs, merged by cutoff date, closed without merging by cutoff date, average time-to-merge in days (rounded as specified), and top contributor (resolving ties lexicographically).
4. Format the metrics into the exact JSON structure specified and write it to the required output path.

## 4. Family tool routing and useful placeholder snippets
Prioritize family-specific tools over ad hoc shell scripts:
- `github_pr_search`: Retrieve PRs based on repository and date range.
- `github_pr_metrics`: Extract relevant data points from retrieved PRs.
- `time_window_filter`: Separate PRs based on creation, merge, and close timestamps relative to cutoff dates.
- `write_json`: Ensure the final output is correctly formatted and written.

## 5. Validation checks before final submission
- Ensure the output file exists at the exact path specified (e.g., `/app/report.json`).
- Verify the JSON structure perfectly matches the requested schema, including keys and data types.
- Confirm the logic for "merged" and "closed without merge" aligns with the cutoff date.
- Check that average time-to-merge is rounded correctly.
- Ensure ties for top contributor are resolved lexicographically.

## 6. Common failure modes and repair actions
- **Misinterpreting "closed"**: Ensure "closed" strictly means "closed without merge" by the cutoff date. Re-evaluate filtering logic if counts are incorrect.
- **Incorrect rounding**: Verify the rounding implementation if schema validation fails on the float value.
- **Missing output file**: Check directory structure and ensure the file was written to the absolute path requested.

## 7. Finalizer capsule
If nearing the maximum step limit without completing the full analysis, construct a minimal valid JSON artifact matching the required schema. Populate fields with default values (e.g., 0 for counts, 0.0 for averages, empty string for contributor) to ensure an artifact of the correct shape exists at the required path, preventing complete failure.
