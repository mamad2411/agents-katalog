---
name: verify-pr-comments
description: Fetch review comments on a GitHub PR (bots + humans) and verify each claim against the actual code, reporting which to accept / reject / defer with concrete evidence and fix drafts.
argument-hint: "<pr-number-or-url>"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main`
Current branch: !`git branch --show-current 2>/dev/null`

## Instructions

Verify every substantive review comment on a GitHub PR against the current codebase. Execute immediately without asking.

### Input

`$ARGUMENTS` is a PR number (e.g. `3841`) or a full GitHub PR URL (e.g. `https://github.com/owner/repo/pull/3841`).

### Process

1. **Fetch comments from all three endpoints**, since PR reviews are fragmented:
   - `gh api repos/<owner>/<repo>/pulls/<num>/reviews --paginate`, top-level reviews (the long summary bodies from `claude[bot]`, `cubic-dev-ai[bot]`, human reviewers). Each entry has `commit_id`.
   - `gh api repos/<owner>/<repo>/pulls/<num>/comments --paginate`, inline comments on specific file/line. Each entry has `path`, `line`, `commit_id`, `body`.
   - `gh api repos/<owner>/<repo>/issues/<num>/comments --paginate`, issue-level PR comments (where bots like `changeset-bot`, `vercel`, `greptile-apps` post status).
   - `gh pr view <num> --comments` returns a human-readable mix but lacks `commit_id` for staleness detection. Use it only as a fallback.

2. **Fetch resolution state for inline-comment threads** via GraphQL (REST does not expose this):
   ```bash
   gh api graphql -F owner=<owner> -F repo=<repo> -F num=<num> -f query='
     query($owner: String!, $repo: String!, $num: Int!) {
       repository(owner: $owner, name: $repo) {
         pullRequest(number: $num) {
           reviewThreads(first: 100) {
             nodes {
               isResolved
               comments(first: 10) { nodes { databaseId } }
             }
           }
         }
       }
     }'
   ```
   Build a map from inline comment ID to `isResolved`. Comments in resolved threads have already been addressed and should be filtered before verification.

3. **Determine the latest commit on the PR**:
   - `gh api repos/<owner>/<repo>/pulls/<num> --jq .head.sha`. This is the `commit_id` against which "fresh" comments are judged.

4. **Filter noise** by skipping entries whose body is metadata-only, not a review claim:
   - `changeset-bot`: changeset detection summary.
   - `vercel` / `vercel[bot]`: deployment URLs.
   - `greptile-apps` when body is just the `<!-- greptile_other_comments_section -->` footer.
   - Any comment whose body is entirely HTML attribution / CTA / badges with no prose claim. Strip `<!-- ... -->` markers and "Fix with …" buttons before reading.
   - Any inline comment in a resolved thread (per step 2).

5. **Classify each remaining comment by staleness**:
   - **Fresh**: `commit_id === latest head SHA`. Reviewer saw the current code; verify it.
   - **Stale**: `commit_id !== latest head SHA`. May already be addressed. Don't reverify unless the user asks; mark as "Stale (last seen at `<sha[:7]>`)" and move on.

6. **Verify each fresh, substantive comment**:
   - Use `Read` on the referenced file at its current state. Do NOT trust the reviewer's quoted diff; quoted snippets are often outdated after pushes.
   - **Treat ```` ```suggestion ```` blocks as the primary artifact.** Most reviewer bots embed concrete code suggestions in suggestion blocks (GitHub renders them as one-click "Commit suggestion" buttons). Read the suggestion first, then the surrounding prose as justification. Verify the suggestion in isolation: would applying it produce code that compiles and matches existing patterns?
   - Cross-check any factual claim ("type X already exists in module Y", "pattern Z is used in other-file.ts") with `Grep` before accepting it.
   - **Mentally apply the suggested fix** and verify types/callers/tests still pass. Bots frequently suggest fixes that fail type-check or break other callers; validating the suggestion is part of verification.
   - Assign one verdict:
     - **Confirmed**: claim correct and the suggested fix works as-is.
     - **Partial**: claim has merit but the suggested fix is wrong or incomplete; propose an adjusted fix.
     - **Refuted**: claim is incorrect. Explain why with code evidence.
     - **Out-of-scope**: claim may be valid but exceeds the PR's intent (architectural refactor, missing tests, etc.). Defer to follow-up.
     - **Stale**: already addressed (see step 5) or in a resolved thread (per step 2).

7. **Parallel verification**: run independent Read/Grep calls in parallel. Prefer direct tool calls to avoid burning context via agents.

8. **Report** in structured output:

   - **PR summary**: title, latest commit SHA, counts of fresh / stale / resolved / noise comments.
   - **Comment matrix** (one row per substantive comment):

     | # | Author | Location | Claim (short) | Verdict | Action |
     |---|--------|----------|---------------|---------|--------|
     | 1 | `claude[bot]` | `foo.ts:12` | "type is redundant" | Confirmed | inline `Pick<...>` |

   - **Per-comment detail** for each Confirmed / Partial entry: 2 to 3 line evidence plus a concrete fix draft (code snippet or `file:line` diff).
   - **Rejected / deferred comments**: one line each with the reason.
   - **Recommended actions**, a concise list the user can act on:
     - changes to make (with `file:line`).
     - comments to reply-to-reject (with draft reply text if helpful).
     - bots to re-trigger (e.g. "tag `@cubic-dev-ai`, its last review is stale on `<sha>`").

### Bot signature reference

Skim this when classifying authors:

| Bot | Typical shape | What's signal |
|-----|---------------|---------------|
| `claude[bot]` | Long structured review with sections like "Issues found", "Suggestions". Often inline + summary. | Section headings under "Issues" / "Critical"; suggestion blocks. |
| `cubic-dev-ai[bot]` | Either "**No issues found**" or specific findings, each with severity. Always carries a `<!-- cubic:attribution -->` marker (ignore the marker text). | Findings with `file:line`; ignore boilerplate and attribution. |
| `coderabbit-ai[bot]` / `coderabbitai[bot]` | Verbose walkthrough + an "Actionable comments" section + inline nitpicks. | The "Actionable comments posted" count and inline comments. Ignore the walkthrough summary. |
| `greptile-apps` | Short status comment plus separate inline comments. Summary often contains only `<!-- greptile_other_comments_section -->`. | Inline comments only; the summary is metadata. |
| `changeset-bot` | "🦋 Changeset detected" or a warning if missing. | Whether a changeset exists; nothing else. |
| `vercel[bot]` / `vercel` | Deployment URL or build status. | Always noise. |
| Human reviewer | Free-form prose, sometimes inline. | Take seriously; outweighs bots on disagreement. |

### Rules

- **Always read the current file state**, not the reviewer's quoted diff. Bots quote outdated code after a push.
- **Suggestion blocks first**: when a comment contains a ```` ```suggestion ```` block, that's the testable artifact. Verify by mental application; the surrounding prose is justification, not the proposal.
- **Verify suggested fixes by simulation**: if a bot says "replace X with `ThreadListItemRuntime`", check whether call-sites still type-check with that change. If the suggestion is structurally wrong, mark **Partial** and propose a correct variant (e.g. `Pick<ThreadListItemRuntime, "foo">`).
- **Distinguish "Critical Issues" from "Suggestions"**: review bots often split their output. Critical issues deserve Confirmed/Refuted judgments; plain suggestions can be marked Out-of-scope with a one-line reason.
- **Human > bot**: if a human reviewer contradicts a bot, weight the human's intent and note the bot's disagreement in the report.
- **Resolved threads are addressed**: if a thread is `isResolved=true`, treat it as Stale-equivalent. Do not re-verify unless the user explicitly asks.
- **Stale comments**: mark and move on. Don't spend tokens re-verifying a claim about code that no longer exists.
- **Never modify files** during verification. This skill is read-only analysis; fix work happens in a follow-up step.
- **Be concise**: evidence is `file:line` references, not code dumps. The matrix is the primary artifact.
- **Use the same language as the user's input** when reporting.
- **See also**: `/verify-pr` validates the PR itself (correctness, tests, conventions). This skill validates the comments left ON the PR. Use `/verify-pr` to decide whether to merge; use this one when responding to reviewers.
