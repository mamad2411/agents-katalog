---
name: pre-release-pr-triage-worktree
description: Triage open PRs for a release in a dedicated git worktree, classify each into merge/candidate/supersede/defer, and work the loop end-to-end.
category: agents
version: 1.0.0
version_origin: extracted
tags: [release-management, git-worktree, gh-cli, triage, open-source]
source_type: extracted-from-git
source_url: https://github.com/jamiepine/voicebox.git
source_ref: main
source_commit: 476abe07fc2c1587f4b3e3916134018ebacd143d
source_project: voicebox
confidence: high
imported_at: 2026-04-18T00:00:00Z
---

# Pre-release PR triage (worktree)

## When to use
A solo maintainer (or small team) has accumulated 10+ open PRs and wants to land the critical subset before cutting a minor/major release — without losing the changelog narrative and without deep-reviewing everything.

## Steps
1. Create a dedicated PR-review worktree: `git worktree add ../<repo>-pr-review -b pr-review-<version> main`. Keep the main worktree for release prep (changelog, direct follow-ups); use the review worktree for `gh pr checkout` so HEAD moves without contaminating release work.
2. Bulk-gather metadata once: `gh pr list --state open --limit 50 --json number,title,author,mergeable,mergeStateStatus,additions,deletions,maintainerCanModify,files`. Capture size, mergeable state, file paths (for overlap detection), and whether maintainer can push to the fork.
3. Sort every PR into one of four tiers:
   - **Tier 1 (merge)**: small, mergeable, clean CI, low review cost.
   - **Tier 2 (candidate)**: 50-200 lines, needs a close read but looks sound.
   - **Supersede**: covered by something already merged — verify by diff, not by title similarity.
   - **Defer**: big features, dirty conflicts, draft PRs, anything risky.
4. Write `<VERSION>_PR_TRIAGE.md` with a Progress header, per-tier tables (with checkbox status columns), supersede table, defer list, and order-of-attack. The doc is your session state.
5. For each PR: `gh pr checkout N`, review via `git show HEAD` / `git show --stat HEAD` (NEVER `main..HEAD` on a stale branch — it lies), `git rebase origin/main` if behind, and `git push <author> HEAD:<branch> --force-with-lease` if `maintainerCanModify=true`. Then `gh pr merge N --squash`.
6. Batch obviously-correct one-liners in a loop: `for pr in ...; do gh pr merge $pr --squash; done`. Verify each with `gh pr view $pr --json state,mergeCommit`.
7. For partial-applies: `git checkout <pr-sha> -- <files>`, review staged, commit with a `Co-Authored-By:` trailer crediting the original author, then close the PR with a comment naming the applied commit.
8. Update `<VERSION>_PR_TRIAGE.md` after every action. If interrupted, the doc is the only source of truth.

## Counter / Caveats
- `main..HEAD` on a stale PR branch shows every main commit as deletions, turning a 3-line PR into what looks like a 700-line revert. **Always** review via `git show HEAD`.
- Squash-merging an unrebased branch reverts in-between work — rebase first or GitHub's squash computes a bad merge-base diff.
- `mergeable=UNKNOWN` is transient after a push; just try the merge and see.
- Route-ordering bugs (FastAPI-style `DELETE /history/failed` vs `DELETE /history/{id}`) are a class of bug that pairs of PRs frequently re-introduce — verify param-path routes land after the literal ones.

Source references: `.agents/skills/triage-prs/SKILL.md` (the full triage workflow that this skill extracts).
