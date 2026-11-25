---
name: skillx-github-repo-analytics-skill
description: skillx family-level skill for SkillLearnBench task family github-repo-analytics.
allowed-tools:
- list_dir
- read_file
- write_file
- python
- shell
metadata:
  benchmark: skilllearnbench
  source_method: skillx
  source_dir: <SOURCE_DIR>
  family: github-repo-analytics
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `github-repo-analytics`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the visible instruction and nearby task files to extract the repository, PR creation window, optional minimum-files-changed filter, cutoff timestamp for status evaluation, required output path, and exact JSON schema; this prevents solving the wrong slice of GitHub data.
# step 2: Use the GitHub PR search/query tools to collect all pull requests created in the requested window for the target repository, handling pagination; this establishes the candidate PR set from authoritative metadata.
# step 3: For each candidate PR, fetch per-PR metrics if needed to obtain fields such as files changed, author login, created time, merged time, closed time, and merge state; this supplies the attributes needed for filtering and aggregation.
# step 4: Apply the task filters deterministically: keep only PRs meeting any size threshold, count all remaining PRs as total, mark a PR as merged only if it has a merge timestamp on or before the cutoff, and mark it as closed only if it was closed by the cutoff without being merged; this matches the task’s status definitions.
# step 5: Compute the derived metrics from the filtered set: average merge time in days from creation to merge for PRs merged by the cutoff, rounded to one decimal place, and the top contributor by PR count with lexicographic tie-break on login; this produces the requested summary values.
# step 6: Write the results to the required JSON file using the exact nested schema and field names; this satisfies the artifact contract expected by the task.
# step 7: Sanity-check that the file exists, the JSON shape is exact, counts are internally consistent, and no hidden or extraneous data was copied in; this catches schema or logic mismatches before finalizing.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
