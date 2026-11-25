---
name: pr-review-summarizer
description: Use when reviewing a code pull request or merge request. Reads a unified diff (or fetches one from GitHub/GitLab) and produces a structured review — risk-ranked summary, files changed, hotspots, suggested test coverage, and reviewer questions. Vendor-neutral; works with any AI agent runtime that can run shell commands.
---

# PR Review Summarizer

## When to invoke
- "Summarize this PR for me before I review."
- "What's the risk in this diff?"
- "Generate reviewer questions for PR #482."

## Inputs needed
1. **Diff source** — local unified diff file, GitHub PR URL, or GitLab MR URL.
2. **Context** (optional) — service name, runtime, test framework.

## Workflow
1. **Fetch / read** the diff.
2. **Classify** changes: code, tests, docs, config, dependencies.
3. **Score risk** per file using heuristics: lines changed, security-sensitive paths, lack of tests, schema changes.
4. **Summarize** intent in plain language.
5. **Produce** a review brief: TL;DR, risk hotspots, missing test coverage, suggested questions.

## Output format
```
## TL;DR
## Risk hotspots (ranked)
## Files changed (summary)
## Missing test coverage
## Reviewer questions
## Suggested follow-ups
```

## Guardrails
- Never approve or merge — the skill produces a review, not a verdict.
- Flag schema, auth, crypto, and migration changes as **High** by default.
- Cite exact file + line numbers from the diff for every risk claim.

## Reference code
`review.py` reads a unified diff file or fetches via `gh pr diff` / `glab mr diff` and produces the brief.
