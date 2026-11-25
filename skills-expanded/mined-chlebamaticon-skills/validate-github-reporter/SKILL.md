---
name: validate-github-reporter
description: Publish a synthesized validation report as a Pull Request summary and inline GitHub comments on eligible changed code. Use during a validation cycle after synthesis completes.
---

# Validate GitHub reporter

Read [the shared validation contract](../validate/validation-contract.md) and [GitHub report templates](github-report-templates.md). The caller supplies `RUN_DIR` containing `context.json` and `synthesis.json`.

## Select the Doom status-bar face

From final findings in `synthesis.json`, compute the majority severity and pick the 48×48 face per [Doom status-bar face prefix](github-report-templates.md#doom-status-bar-face-prefix). Use that same face on the PR summary and every inline comment. Record the chosen key (`god` | `hurt-light` | `hurt-heavy` | `dead`) as `face` in `github-report.json`.

## Publish the summary

Parse `synthesis.json`; reject malformed data or a missing change summary. Using the PR in `context.json`, post one Markdown PR comment using the [summary template](github-report-templates.md#pr-summary-comment) (face prefix first). Use `gh pr comment <number> --body-file ...` and capture the resulting comment URL. Resolve `owner/repo` once with `gh repo view --json nameWithOwner --jq .nameWithOwner`.

## Publish eligible inline comments

For each final `blocking` or `important` finding with a location, verify that exact path and line are in the PR's changed-file diff. Post one inline comment using `gh api repos/{owner}/{repo}/pulls/{pr}/comments` with the pinned `head_sha`, `path`, `line`, and `side: RIGHT`. Format the body with the [inline template](github-report-templates.md#inline-review-comment) (same face prefix, then `[validation:{id}]`). If GitHub rejects the location, retain the summary-only report and record the rejection; never guess a nearby line.

Write `github-report.json` atomically with `summary_url`, `face`, `inline_comments` (`id`, `url`), and `unpublished` (`id`, `reason`).

**Done when:** one summary comment URL is recorded, `face` matches the majority selection, every eligible finding has either an inline-comment URL or a recorded GitHub rejection, and `github-report.json` is valid JSON.
