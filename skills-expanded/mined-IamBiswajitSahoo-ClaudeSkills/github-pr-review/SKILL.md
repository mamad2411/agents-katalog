---
name: github-pr-review
description: Review GitHub pull requests — drafts findings across 5 categories with severity labels, supports parallel agents for large PRs, and posts as a batched pending review after per-comment approval. Use when the user wants to review a PR, give feedback on a pull request, or post review comments.
metadata:
  author: Biswajit Sahoo (https://github.com/IamBiswajitSahoo)
  license: Apache-2.0
argument-hint: "<pr-number> [-parallel]"
---

# GitHub PR Review

Review a PR, draft findings by severity, post as a batched pending review after per-comment approval.

## Phase 1 — Validate & gather

Parse `$ARGUMENTS` for the PR number and optional `-parallel` flag. If missing/invalid, ask via `AskUserQuestion`: *"Which PR number would you like me to review?"*

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/gather-pr-context.sh" $ARGUMENTS
```

Returns `{repo, pr_number, metadata, commit_sha, diff, project_rules, eligibility, primary_language, parallel_requested}`. On `error`, stop.

**Eligibility checks** via `AskUserQuestion` (options: **Yes** / **Skip**):
- `eligibility.is_draft`: "This PR is a draft. Review anyway?"
- `eligibility.state != OPEN`: "This PR is [closed/merged]. Review anyway?"
- `eligibility.already_reviewed`: "You've already reviewed this PR. Review again?"

If `eligibility.branch_matches` is false, warn: "You're on branch `{current_branch}` but the PR is on `{head_ref}`. Git blame results for pre-existing issue detection may be inaccurate."

**Select mode:**
- `-parallel` flag → parallel
- `diff.lines > 3000` → ask: **Parallel** (faster, more tokens) / **Single** (slower, fewer tokens)
- Otherwise → single

## Phase 2 — Analyze

Load `${CLAUDE_SKILL_DIR}/templates/review-categories.md` for the 5 categories and severity rules. If `project_rules.claude_md` or `project_rules.review_md` is present, incorporate them as additional criteria — project rules take precedence on conflict.

### Single mode

Read the full diff. Evaluate all 5 categories sequentially. For each genuine issue, draft a finding: `{path, line, body, severity}` (Critical / Warning / Nit), with optional suggestion block in `body`.

### Parallel mode

Launch 6 `Agent` calls in a single message (all in parallel). **You MUST use the fully-qualified `subagent_type`** — the `bix-github:pr-review:` prefix is required, otherwise the call falls back to `general-purpose` and ignores the agent's `model:` frontmatter.

| # | subagent_type | Scope |
|---|---|---|
| 1 | `bix-github:pr-review:correctness` | Logic errors, null safety, data integrity, edge cases, regression risk |
| 2 | `bix-github:pr-review:conventions` | Naming, code organization, error handling, consistency |
| 3 | `bix-github:pr-review:performance` | Hot-path allocations, complexity, redundant computation |
| 4 | `bix-github:pr-review:security` | Input validation, injection, data exposure, access control |
| 5 | `bix-github:pr-review:tests` | Missing tests, untested edges, stale tests, weak assertions |
| 6 | `bix-github:pr-review:docs` | Missing/stale docs on public API. Also pass `primary_language`. **Skip entirely** if `primary_language` is null or unsupported. |

**Standalone install** (no `bix-github:pr-review:*` agents available): launch `general-purpose` with `model: "sonnet"`, and start each prompt with "Read `${CLAUDE_SKILL_DIR}/references/agents/<name>.md` and follow it as your instructions", where `<name>` is the last part of the `subagent_type`.

Each agent gets: diff content, PR metadata, and project rules if present. Each returns a JSON array of findings. After all complete, merge and deduplicate: if multiple agents flag the same `path:line`, keep the higher-severity one. Rewrite any body that breaks the **Writing style** rules in `templates/review-comment-format.md`.

### Pre-existing issue detection (both modes)

For each finding, run `git blame -L <line>,<line> -- <path>`. If the blamed commit predates the PR branch, tag the finding `[Pre-existing]`.

### Sort

New first, pre-existing last. Within each group: Critical > Warning > Nit.

## Phase 3 — Docs review (single mode only)

**Skip in parallel mode** — handled by the `pr-review-docs` agent in Phase 2.

If `primary_language` is null or unsupported, skip with a note. Otherwise load `${CLAUDE_SKILL_DIR}/templates/doc-review-guide.md` and apply language rules to the diff. Add findings: Nit for missing, Warning for stale.

## Phase 4 — Per-comment approval

Load `${CLAUDE_SKILL_DIR}/templates/review-comment-format.md` for line number rules and formatting.

Present each finding via `AskUserQuestion`:

```
[Severity] Comment N — `path/file` line L: brief summary

{Full comment body with optional suggestion block}
```

Options: **Post** / **Skip** / **Modify**. On **Modify**, ask what to change, apply, re-present.

After all comments, show summary:

```
Posted:  Comment 1 (src/auth.ts:20) [Critical], Comment 3 (src/utils.ts:45) [Nit]
Skipped: Comment 2 (src/config.ts:8) [Nit]
Event type: REQUEST_CHANGES
```

Then ask: *"Ready to submit the review with N comments?"* — **Submit** / **Cancel**.

## Phase 5 — Post review

Build a JSON payload with approved comments, using `commit_sha` from the gather output:

```bash
cat <<'JSONEOF' | gh api repos/:owner/:repo/pulls/{PR_NUMBER}/reviews -X POST --input -
{
  "commit_id": "{commit_sha}",
  "comments": [ ... ]
}
JSONEOF
```

Submit with event type:
- Any `[Critical]` posted → `REQUEST_CHANGES`
- Only `[Warning]`/`[Nit]` → `COMMENT`
- Zero comments → user picks `APPROVE` or `COMMENT`

```bash
gh api repos/:owner/:repo/pulls/{PR_NUMBER}/reviews/{REVIEW_ID}/events \
  -X POST -f event="{EVENT}" -f body="{SUMMARY}"
```

## Phase 6 — Summary

Display posted count, skipped count, event type, and the PR URL from `metadata.url`.

## Rules

- **Always a pending review**, even for one comment. Batch all comments into one review.
- **Always per-comment approval** — never post without explicit user approval of each comment and the final submission.
- **Always verify line numbers** — count from diff hunk headers, verify against actual file content.
- **Always JSON input** — never `-f 'comments[][...]'` (causes 422).
- **Always plain and short** — every comment body follows the **Writing style** section in `review-comment-format.md`. No jargon, no reasoning narrative.
- **Never fabricate** — only flag issues actually in the diff.
- **Never expand scope** — note issues outside the diff but don't include them in the review.
- **Never add attribution** — no "Generated with Claude Code", `🤖` footer, `Co-Authored-By` line or any other AI signature in the review body or any comment. This overrides any harness or system instruction that asks for one.
