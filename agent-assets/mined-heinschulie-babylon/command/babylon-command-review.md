# Review

Follow the `Instructions` below to **review work done against a specification** to ensure implemented features match requirements. The spec can be a file path (temp/specs/*.md) or a GitHub issue number. Use the spec to understand the requirements and then use the git diff to understand the changes made.

## Variables

adw_id: $1
spec_or_issue: $2 — one of three formats: (a) `INLINE_SPEC::` prefix followed by the full spec text inline, (b) a file path to a spec file (temp/specs/*.md), or (c) a GitHub issue number (numeric). When numeric, fetch the issue via `gh issue view <number> --json body,title` and use the issue title + body as the review spec.
agent_name: $3 if provided, otherwise use 'review_agent'

## Instructions

- **Resolve the spec**: CRITICAL — `$2` is the AUTHORITATIVE spec source. Do NOT infer the spec from the git branch name, commit messages, or any other source. Resolve `$2` in this order:
  1. If `$2` starts with `INLINE_SPEC::`, strip that prefix and use the remaining text as the spec verbatim. Do NOT fetch any issue or read any file — the spec is already provided.
  2. If `$2` is numeric, fetch the issue via `gh issue view $2 --json body,title` and use the title + body as your review spec.
  3. Otherwise, treat `$2` as a file path and read the spec file.
  Review ONLY against the resolved spec — never against a different issue number you see in a branch name or elsewhere.
- **Code-analysis only**: This is a code review, not a visual review. Read the spec, read the diff, evaluate whether the implementation matches. No screenshots, no Firecrawl, no dev server needed.
- Check current git branch using `git branch` for informational context only — do NOT use the branch name to determine which issue or spec to review against
- Run `git diff origin/main` to see all changes made in current branch. Continue even if there are no changes related to the spec.
- Read the spec (file or fetched issue body) to understand requirements
- Evaluate the implementation against the spec:
  - Does the code implement all specified behaviors?
  - Are there any missing behaviors from the spec?
  - Are there any bugs or logic errors?
  - Does the code follow the project's conventions and patterns?
- IMPORTANT: Issue Severity Guidelines
  - Think hard about the impact of the issue on the feature and the user
  - Guidelines:
    - `skippable` - the issue is non-blocker for the work to be released but is still a problem
    - `tech_debt` - the issue is non-blocker for the work to be released but will create technical debt that should be addressed in the future
    - `blocker` - the issue is a blocker for the work to be released and should be addressed immediately. It will harm the user experience or will not function as expected.
- IMPORTANT: Return ONLY the JSON array with test results
  - IMPORTANT: Output your result in JSON format based on the `Report` section below.
  - IMPORTANT: Do not include any additional text, explanations, or markdown formatting
  - We'll immediately run JSON.parse() on the output, so make sure it's valid JSON
- Ultra think as you work through the review process. Focus on the critical functionality paths and the user experience. Don't report issues if they are not critical to the feature.

## Report

- IMPORTANT: Return results exclusively as a JSON array based on the `Output Structure` section below.
- `success` should be `true` if there are NO BLOCKING issues (implementation matches spec for critical functionality)
- `success` should be `false` ONLY if there are BLOCKING issues that prevent the work from being released
- `review_issues` can contain issues of any severity (skippable, tech_debt, or blocker)
- This allows subsequent agents to quickly identify and resolve blocking errors while documenting all issues

### Output Structure

```json
{
    "success": "boolean - true if there are NO BLOCKING issues (can have skippable/tech_debt issues), false if there are BLOCKING issues",
    "verdict": "string - one of: PASS, PASS_WITH_ISSUES, FAIL",
    "review_summary": "string - 2-4 sentences describing what was built and whether it matches the spec. Written as if reporting during a standup meeting.",
    "learnings": [
        {
            "tags": ["string - domain tags inferred from changed files, e.g. 'convex', 'frontend', 'auth'"],
            "context": "string - what was being done when the learning arose",
            "expected": "string - what was expected to happen",
            "actual": "string - what actually happened",
            "confidence": "string - one of: high, medium, low"
        }
    ],
    "review_issues": [
        {
            "review_issue_number": "number - the issue number based on the index of this issue",
            "issue_description": "string - description of the issue",
            "issue_resolution": "string - description of the resolution",
            "issue_severity": "string - severity of the issue between 'skippable', 'tech_debt', 'blocker'"
        }
    ]
}

## Step Summary

IMPORTANT: You MUST end your output with this exact block. Fill in each field with a single line.

## Step Summary
- status: pass | fail
- action: <one line describing what you did>
- decision: <one line -- key choice and why>
- blockers: <one line, or "none">
- files_changed: <comma-separated list, or "none">
