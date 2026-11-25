---
name: fetch-coderabbit-threads
description: Use when the user asks to fetch / list / read / show unresolved CodeRabbit review threads on a GitHub PR. Pulls thread URL, file:line, author, and full comment body for every thread CodeRabbit opened that is not yet resolved, plus CodeRabbit's review-summary nitpicks.
---

**Preflight:** run `la-doctor --plugin <this skill's base directory>` once per session before using any `la-*` or `dr-*` command; if it fails, stop and show the user its output.

# Fetch unresolved CodeRabbit review threads from a PR

## How to run

```bash
la-fetch-coderabbit-threads <PR_NUMBER> [--repo OWNER/REPO] [--all-authors]
```

Works in any repo; it does not read `living-architecture.yaml`.

- `<PR_NUMBER>` — required, the PR number.
- `--repo OWNER/REPO` — optional; defaults to the repo of the current git directory (auto-detected via `gh repo view`).
- `--all-authors` — include unresolved threads from any author, not just CodeRabbit.

## Output

Always emits **both** formats side-by-side:

- **Markdown to stdout** — one section per inline thread (URL, file:line, author, resolved/outdated, each comment body), followed by `## CodeRabbit review-summary nitpicks` and `## CodeRabbit outside-diff-range comments` sections.
- **JSON file** — full filtered payload at `${TMPDIR:-/tmp}/coderabbit-threads-<pr>-<utc-timestamp>.json`. The path is printed on the last line, prefixed `JSON: `.

The JSON schema is:

```json
{"pr": 63, "repo": "owner/name", "threads": [...], "nitpicks": [...], "outside_diff": [...]}
```

## Steps

1. Run the script with the PR number the user gave (or, if they didn't say, infer from `gh pr view --json number -q .number`).
2. Read the Markdown output and present a concise summary to the user — count, files touched, visible severity. Re-parse the JSON file (no extra API call) if you need structured data.
3. **Never** call any "resolve" mutation or click "Resolve" on threads. Only read — CodeRabbit and reviewers manage thread resolution.

## Why this skill

Fetching unresolved CodeRabbit threads needs `gh api graphql` (the REST API doesn't expose `isResolved`) and a separate `gh api .../pulls/N/reviews` call to pick up nitpicks that live in review bodies, not threads. This skill bundles both. Always use it instead of hand-rolling `gh api graphql` queries.
