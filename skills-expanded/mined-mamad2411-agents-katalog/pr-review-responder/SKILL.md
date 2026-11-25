---
name: pr-review-responder
description: Fetches all PR comment types (inline, review, discussion) via gh api for team review workflow. Use when addressing PR review feedback with fix-vs-decline rules — stricter than built-in /babysit.
disable-model-invocation: true
---


# PR Review Responder

## Subagents (default)

Fetch + reply via **Task** — `shell` for `gh`/`fetch_pr_comments`; `generalPurpose` for fix-vs-decline analysis. Main chat owns tracking table. See `reference/subagents.md`.

## When to use

- User asks to handle PR reviews or respond to review comments
- Need flat JSON of all comment types for tracking table
- Team rules: reply to every comment, fix-vs-decline matrix

## Instructions

1. Run `python scripts/fetch_pr_comments.py --pr <number> --project-root <root>`.
   For evals/CI without `gh`: add `--fixture path/to/comments.json`.
2. Build tracking table — every comment gets a response.
3. Inline comments: reply in thread via `gh api .../comments/ID/replies`.
4. Post summary only after all individual replies.

## Requires

- `gh` CLI authenticated (`GH_TOKEN` in cloud)
