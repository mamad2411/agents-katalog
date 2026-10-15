---
name: cc-pr-review-ci
description: Comprehensive TypeScript/React PR review. Outputs structured review.json consumed by a posting script that creates a GitHub Review with inline comments. Agent runs read-only; the workflow script holds write permissions.
---

# PR Review (single-agent, CI-safe)

Review a PR across 10 domains sequentially, then write `review.json`. A separate posting script turns the JSON into GitHub inline review comments.

*If no PR number provided, diff against `origin/main` and print JSON to stdout.*

---

## Step 0 — Load prior dismissals (PR runs only)

Skip if no PR number provided.

Fetch all existing bot reviews on this PR:

```bash
gh api repos/{owner}/{repo}/pulls/$PR_NUMBER/reviews \
  --jq '[.[] | select(.body | test("<!-- cc-pr-review -->";  "i")) | {id: .id, submitted_at: .submitted_at}]'
```

For each bot review found, fetch its inline comments:

```bash
gh api repos/{owner}/{repo}/pulls/$PR_NUMBER/reviews/$REVIEW_ID/comments \
  --jq '[.[] | {id: .id, body: .body, path: .path, line: .line, reactions: .reactions}]'
```

Also fetch any reply threads on those inline comments:

```bash
gh api repos/{owner}/{repo}/pulls/$PR_NUMBER/comments \
  --jq '[.[] | select(.in_reply_to_id != null) | {id: .id, in_reply_to_id: .in_reply_to_id, body: .body}]'
```

Build **`SUPPRESSED_FINDINGS`**: a list of finding `id` values to skip this run.

A finding is suppressed if its prior inline comment has:
- A 👎 reaction (`.reactions["-1"] > 0`), **or**
- A human reply containing dismissal language: "intentional", "by design", "won't fix", "false positive", "ignore", "not applicable", "expected"

Extract the finding `id` from the prior comment body — each inline comment posted by the script contains an HTML comment `<!-- id: {finding-id} -->` in the first line.

**Escape hatch**: if the file + surrounding lines for a suppressed finding appear in the current diff (i.e. the code actually changed), remove it from `SUPPRESSED_FINDINGS` — the finding must be re-evaluated.

If no prior reviews or no dismissals: `SUPPRESSED_FINDINGS` is empty.

---

## Step 1 — Get the diff

- PR number given → `gh pr diff $PR_NUMBER`
- No PR number → `git diff origin/main`

---

## Step 2 — Run 10 domain reviews sequentially

Read the reference file for each domain, then analyze the diff. Record findings with their exact file path and line number.

**Before recording any finding**: check if its computed `id` (`{domain}-{kebab-title}`) is in `SUPPRESSED_FINDINGS` AND the relevant code lines have not changed in the current diff. If both conditions hold → skip silently.

1. **Security**         — `Read .claude/skills/cc-pr-review-ci/references/security.md`
2. **Performance**      — `Read .claude/skills/cc-pr-review-ci/references/performance.md`
3. **React/TypeScript** — `Read .claude/skills/cc-pr-review-ci/references/react-ts.md`
4. **Testing**          — `Read .claude/skills/cc-pr-review-ci/references/testing.md`
5. **DevOps/CI**        — `Read .claude/skills/cc-pr-review-ci/references/devops.md`
6. **Holistic**         — `Read .claude/skills/cc-pr-review-ci/references/holistic.md`
7. **Duplication**      — `Read .claude/skills/cc-pr-review-ci/references/duplication.md`
8. **Bug Hunting**      — `Read .claude/skills/cc-pr-review-ci/references/bug.md`
9. **Scope/Hygiene**    — `Read .claude/skills/cc-pr-review-ci/references/scope.md`
10. **Maintainability** — `Read .claude/skills/cc-pr-review-ci/references/thermo.md`

---

## Step 3 — Write review.json

1. Read `Read .claude/skills/cc-pr-review-ci/references/format.md` for the exact schema.

2. Merge all domain findings into a single `findings` array. Assign each finding a stable `id` following the `{domain}-{kebab-title}` convention.

3. Determine verdict:
   - Any `critical` → `CHANGES_REQUESTED`
   - `high` only → `APPROVED_WITH_SUGGESTIONS`
   - `observations` only or none → `APPROVED`

4. Write the JSON:
   - **PR run**: write to `$REVIEW_OUTPUT_PATH` (default `/tmp/review.json`)
   - **Local run (no PR number)**: print to stdout

**Do not call `gh` to post anything.** The workflow's `post-review.js` step handles all GitHub writes.
