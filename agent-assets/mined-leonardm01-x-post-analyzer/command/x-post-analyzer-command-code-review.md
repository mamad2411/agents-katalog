---
description: "Code review a GitHub pull request"
argument-hint: <pr-number-or-url>
allowed-tools:
  - Bash(gh pr view:*)
  - Bash(gh pr diff:*)
  - Bash(gh api:*)
  - Bash(gh pr comment:*)
  - Agent
---

You are running a multi-agent PR review. The goal is to post a single, well-structured review comment on the pull request with real issues only — no false positives, no filler.

## Step 1 — Resolve the PR

`$ARGUMENTS` is either a PR number or a full GitHub PR URL. Run:

```
gh pr view $ARGUMENTS --json number,title,body,baseRefName,headRefName,headRefOid,url
```

Extract: the repo (from the URL or `gh pr view` output), the PR number, the head SHA (`headRefOid`), the base branch, and the PR URL. You will need the full 40-character SHA later for permalink construction.

## Step 2 — Fetch the diff

```
gh pr diff $ARGUMENTS
```

Read the entire diff. Note every file path and every changed hunk. Do not truncate.

## Step 3 — Dispatch 5 parallel reviewers

In a **single message**, dispatch all five Agent tool calls simultaneously. Do not wait for one to finish before starting the next. Each reviewer receives: the full diff text, the PR title, the PR description, the base branch name, and the head SHA.

Assign each reviewer one domain. Use `subagent_type: "code-reviewer"` and `model: "sonnet"` for all five.

- Reviewer A — Correctness & logic: look for wrong conditions, off-by-one errors, incorrect state transitions, missing awaits, broken control flow.
- Reviewer B — Security: injection, authentication/authorization gaps, secrets in diffs, unvalidated input, OWASP Top 10.
- Reviewer C — Edge cases & error handling: null/undefined, empty collections, network failures, timeouts, concurrent access.
- Reviewer D — Performance & scalability: N+1 queries, missing indexes hinted by ORM usage, unbounded loops, blocking I/O in hot paths.
- Reviewer E — Maintainability & conventions: naming, duplication, complexity, adherence to patterns visible elsewhere in the diff, missing tests for non-trivial logic.

Each reviewer must return a JSON array (and nothing else) in this exact schema:

```json
[
  {
    "file": "src/foo/bar.ts",
    "line": 42,
    "severity": "critical|important|suggestion",
    "title": "Short title (no emoji)",
    "body": "What is wrong, why it matters, concrete fix. 2-4 sentences max.",
    "confidence": 85
  }
]
```

Return `[]` if no issues are found in the assigned domain.

## Step 4 — Collect and deduplicate

Merge all five arrays. Deduplicate: if two reviewers flag the same file+line for the same root cause, keep the one with higher confidence (or merge the bodies if they are complementary). Filter out any finding with `confidence < 80`.

## Step 5 — Score each finding

For each remaining finding, verify the confidence score is accurate using this rubric:

- **95–100** — The code is definitively wrong or insecure. No reasonable interpretation makes it correct. Example: SQL string interpolation from user input.
- **85–94** — Very likely a real problem. The scenario that triggers the bug is realistic and not contrived.
- **75–84** — Probable issue but depends on context not visible in the diff. Flag with a note.
- **60–74** — Speculative. Keep only if severity is critical and the risk is severe.
- **< 60** — Drop. Do not include.

Apply the threshold: drop findings with `confidence < 80` after re-scoring.

## Step 6 — False-positive check

Before posting, verify each finding is NOT one of these common false positives:

- Flagging a pattern as missing when it is clearly handled elsewhere in the diff (e.g., error handling present two hunks up).
- Complaining about a style choice that is consistent with other code visible in the diff.
- Treating a TODO comment as a bug.
- Flagging an intentional type assertion that is safe given the surrounding context.
- Raising a performance concern on a code path that runs once at startup.
- Assuming a variable is unvalidated when the diff shows validation earlier in the same function.

Remove any finding that matches a false-positive pattern above.

## Step 7 — Build the GitHub comment

Construct the comment body using exactly these templates.

### If findings remain after filtering:

```
## Code Review — {N} issue(s) found

| # | Severity | File | Line | Title |
|---|----------|------|------|-------|
| 1 | 🔴 Critical | `src/foo/bar.ts` | 42 | Short title |
| 2 | 🟡 Important | `src/baz.ts` | 17 | Short title |
| 3 | 🟢 Suggestion | `src/qux.ts` | 88 | Short title |

---

### 1. Short title
**File:** [`src/foo/bar.ts#L42`](https://github.com/{owner}/{repo}/blob/{HEAD_SHA}/src/foo/bar.ts#L42)
**Severity:** Critical | **Confidence:** 95

What is wrong and why it matters. Concrete suggested fix. Keep to 2–4 sentences.

---

### 2. Short title
**File:** [`src/baz.ts#L17`](https://github.com/{owner}/{repo}/blob/{HEAD_SHA}/src/baz.ts#L17)
**Severity:** Important | **Confidence:** 87

...

---

*Reviewed by 5 parallel agents (correctness, security, edge cases, performance, maintainability). Confidence threshold: 80. False-positive check applied.*
```

### If no findings remain after filtering:

```
## Code Review — No issues found

Reviewed by 5 parallel agents across correctness, security, edge cases, performance, and maintainability. All findings scored below the confidence threshold (80) or were ruled false positives.

*Confidence threshold: 80. False-positive check applied.*
```

Rules for the comment:
- Replace `{owner}/{repo}` with the actual org/repo from Step 1.
- Replace `{HEAD_SHA}` with the full 40-character head commit SHA from Step 1. Never use a short SHA.
- Use the full GitHub permalink format: `https://github.com/{owner}/{repo}/blob/{HEAD_SHA}/{file}#L{line}`.
- Severity order: Critical first, then Important, then Suggestion.
- No emoji in titles or body text — only in the severity column of the table.
- No trailing summary paragraph. No "happy to discuss" filler. Stop after the footer line.

## Step 8 — Post the comment

```
gh pr comment $ARGUMENTS --body "$(cat <<'REVIEW_EOF'
{comment body here}
REVIEW_EOF
)"
```

After posting, output only the PR URL so the user can navigate to it. Nothing else.
