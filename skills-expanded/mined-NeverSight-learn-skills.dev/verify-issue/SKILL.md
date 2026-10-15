---
name: verify-issue
description: Fetch a GitHub issue and verify its claims against the codebase with concrete evidence.
argument-hint: "<issue-number-or-url>"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main`

## Instructions

Verify a GitHub issue against the current codebase. Execute immediately without asking.

### Input

`$ARGUMENTS` is an issue number (e.g. `3766`) or a full GitHub issue URL (e.g. `https://github.com/owner/repo/issues/3766`).

### Process

1. **Fetch issue**: Use `github-repos` MCP (`get_issue`) if available, otherwise `gh issue view $ISSUE_NUMBER --json title,body,labels,state,author`. Extract the title, body, and every technical claim.

2. **Categorize claims**: Sort each claim into one of three buckets, because each is verified differently:
   - **Codebase claim**, about how a specific file, function, type, or behavior works. Verify by reading the code.
   - **Scope claim**, about what is or isn't handled anywhere in the project. Verify by full-repo search, not just the named file.
   - **External claim**, about web standards, ARIA specs, third-party library behavior, or browser conventions. Verify against authoritative sources and judge how load-bearing the claim is to the conclusion.

3. **Search for prior art** (parallel with step 4): Run `gh pr list --search "<keywords>" --state all` and `gh issue list --search "<keywords>" --state all` to surface duplicate issues, in-flight PRs, or already-merged fixes. An exact-match open PR usually answers whether the issue is still actionable; pull its diff and CI status. Skipping this step is the most common way a verification report becomes obsolete on arrival.

4. **Verify each claim**: Gather concrete evidence (file paths, line numbers, exact snippets) using Read/Grep/Glob in parallel. Prefer direct tool calls over agents to keep context tight. For codebase claims, widen the search beyond the named file to confirm the behavior isn't compensated for elsewhere (e.g. if the issue says "key X is unhandled in file Y", grep the whole repo for that key). Note whether any tests cover the affected code path; absent coverage often explains how the bug slipped through.

5. **Report**: Present findings in this structure:

   - **Issue summary**, one line on what the issue requests.
   - **Verification table**, one row per claim:

     | # | Claim | Result | Evidence |
     |---|-------|--------|----------|
     | 1 | description | Confirmed / Refuted / Partial | `file:line`. Brief explanation. |

   - **Prior art**, any related open or merged PRs/issues found in step 3, with number, state, and a one-line summary of the diff if the PR is open.
   - **Conclusion**, whether the issue is valid. Call out any inaccurate framing in the issue body that doesn't change the practical outcome (e.g. an overstated spec citation that still describes a real UX expectation).
   - **Extra findings**, adjacent gaps surfaced during verification that aren't in the issue itself.
   - **Possible fix directions**, brief suggestions if the issue is valid and no covering PR exists. If a covering PR was found, recommend reviewing it instead of proposing a new fix.

### Rules

- Always read the actual source code before making a judgment. Never guess from type names or file names alone.
- Distinguish codebase claims from external/spec claims. Flag inaccurate framing of standards even when the practical conclusion still holds; do not let a polished writeup smuggle in unverified citations.
- Browser testing via Chrome DevTools MCP or Playwright is rarely necessary. Reach for it only when the bug depends on real DOM, CSS, or focus behavior that jsdom can't reproduce; bugs purely in logic verify from code reading plus unit tests.
- If a claim references a specific version, verify against the current code and note version differences.
- Use the same language as the user's input when reporting.
- Be concise. Evidence is file:line references, not full code dumps.
- If `github-repos` MCP is unavailable, fall back to `gh` CLI.
