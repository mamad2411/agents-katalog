---
name: github-pr-review
description: Review a GitHub pull request diff with a structured checklist — correctness, security, scope creep — and produce ready-to-post comments plus a clear approve / request-changes call. Use when the user says "review this PR", "check this diff", "should I merge this", "is this PR safe", or pastes a PR link/diff. Don't use for creating your own branch/commit/PR — use git-ship-flow.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Builder Dev, GitHub, Code Review, Quality]
    related_skills: [git-ship-flow, bug-triage-protocol, env-secrets-hygiene, changelog-release-notes]
---

# GitHub PR Review

Turns "looks fine I guess 🤷" into a real review. Reads the actual diff, runs a fixed checklist (correctness → security → scope), drafts comments the author can act on, and ends with an explicit verdict. A review that doesn't say approve or request-changes isn't finished.

## When to Use

- User shares a PR URL, PR number, or a pasted diff and wants it reviewed.
- User asks "is this safe to merge?" — including PRs written by AI agents.
- User wants help writing review comments that are firm but kind.
- User received a review verdict on their own PR and wants help interpreting or responding to it.
- A quick pre-merge sanity pass on their own PR before asking a human teammate to look.
- **Not for:** making your own commits or opening a PR — use `git-ship-flow`. Not for debugging a bug the PR claims to fix — use `bug-triage-protocol`.

## Quick Reference

| Action | Command / Call |
|---|---|
| Fetch PR overview | `gh pr view <number> --json title,body,files,additions,deletions` |
| Get the full diff | `gh pr diff <number>` (no `gh`: `curl -s https://patch-diff.githubusercontent.com/raw/<owner>/<repo>/pull/<n>.diff`) |
| Check CI status | `gh pr checks <number>` |
| Grep diff for secrets | `gh pr diff <number> \| grep -nEi "(api[_-]?key\|secret\|password\|token)\s*[:=]"` |
| Post a comment | `gh pr comment <number> --body "..."` |
| Approve | `gh pr review <number> --approve --body "..."` |
| Request changes | `gh pr review <number> --request-changes --body "..."` |

## Procedure

1. **Precheck** — `command -v gh && gh auth status`. If `gh` is missing/unauthed, ask for the diff pasted or use the raw `.diff` URL; you can still review, just not post.
2. **Context first** — read the PR title/body and file list. Write one sentence: "This PR claims to X by touching Y." If you can't write that sentence, ask the author what the PR is for — that's finding #1.
3. **Correctness pass** — read the diff hunk by hunk. Check: does the code do what the description says; edge cases (empty input, null/undefined, zero, error paths); anything removed that something else might still use; tests updated or a stated reason why not; CI green (`gh pr checks`).
4. **Security pass** — grep the diff for secrets (table above); check new endpoints/queries for missing auth checks, user input reaching SQL/HTML/shell unescaped, new dependencies (are they needed? real packages?), loosened permissions or RLS/policy changes, `.env` or config files in the diff.
5. **Scope pass** — flag changes unrelated to the stated goal: drive-by refactors, formatting churn burying real changes, "while I was here" features. Scope creep is a request-changes offense on its own when it hides risk.
6. **Draft comments** — one comment per finding, formatted `file:line — [blocking|suggestion|question] — what + why + concrete fix`. Blocking = correctness or security. Suggestion = better way, author's call. Question = you need info before verdict.
7. **Verdict** — apply the criteria strictly: **Request changes** if any blocking finding, any unrotated secret, or you can't tell what the PR does. **Approve** if zero blocking findings and CI is green (suggestions alone don't block). **Comment-only** if questions remain that change the verdict.
8. **Confirm before posting** — show the user the full review (comments + verdict). Post to GitHub only on explicit yes; posting a review is a visible action on someone's work.

## Output Template

```
## PR Review: #<n> — <title>
Claim: <one-sentence what/how>
CI: pass | fail | none
Diff size: +<add>/−<del> across <n> files  (>400 lines changed → note "large PR, consider splitting")

### Findings
1. [BLOCKING] src/api/user.ts:42 — deletes without auth check — any logged-out call can… — fix: guard with session check
2. [SUGGESTION] …
3. [QUESTION] …

### Verdict: APPROVE ✅ | REQUEST CHANGES ❌
Because: <the one or two findings that decided it>
```

## Pitfalls

- **Reviewing the description instead of the diff** — the body says "adds validation" but the diff doesn't. Recovery: every claim in the PR body gets located in the diff; unlocatable claims become QUESTION comments.
- **Secret found in the diff** — recovery: request changes immediately and tell the author the key must be **rotated**, not just removed — it's already in the branch history. Point them to `env-secrets-hygiene`.
- **Huge PR, review fatigue** — 1,500-line diffs get rubber-stamped after file 3. Recovery: review the riskiest files first (auth, payments, data writes), then honestly say "reviewed X of Y files closely" and ask for a split rather than fake-approving.
- **Nitpick storm, no verdict** — 12 style comments and no decision helps nobody. Recovery: max ~3 suggestions unless blocking; always end with an explicit approve/request-changes and the reason.
- **AI-generated code that "looks right"** — plausible code with invented APIs or packages. Recovery: spot-check that imported packages exist (`npm view <pkg> version`) and called methods are real before approving.

## Verification

- [ ] Read the actual diff, not just the PR description
- [ ] All three passes ran (correctness, security, scope) with at least a "clear" note each
- [ ] Secret-pattern grep ran on the diff
- [ ] Every comment names file + line and a concrete fix
- [ ] Review ends in an explicit verdict with the deciding reason
- [ ] Nothing posted to GitHub without the user's explicit confirmation
