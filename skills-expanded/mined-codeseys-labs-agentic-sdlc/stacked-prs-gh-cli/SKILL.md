---
name: stacked-prs-gh-cli
description: |
  Use when managing dependent GitHub pull requests with plain `gh` and git, especially when
  a parent changes or merges, a child must change base, a branch is being rewritten, or
  governance/check evidence is incomplete. The tool-agnostic restack doctrine lives in
  stacked-prs; this skill is its plain-`gh` flavor.
---

# Stacked PRs with plain `gh` + git

Use GitHub's explicit base-branch fields; `gh` has no stack command. Every outward mutation
requires operation-specific authorization and fresh readback. Missing governance data,
unsupported fields, or HTTP 403 is UNKNOWN, never approval.

Author each layer's commit and PR text with `../change-writing/SKILL.md` (output-only); this skill
keeps sole ownership of base-branch topology, restack leases, and readback.

## Create and record boundaries

```sh
git switch main && git switch -c feat-a
# commit A
git push -u origin feat-a
gh pr create --base main --head feat-a --title 'A'

git switch -c feat-b
# commit B
git push -u origin feat-b
gh pr create --base feat-a --head feat-b --title 'B'
```

Before each PR and before each mutation, save the old boundary: PR number, branch, base/head
names, local tip, and exact remote OID. Query `gh pr view <pr> --json baseRefName,headRefName,state,statusCheckRollup`
and record the result. A target/base/head/state drift invalidates the candidate; stop,
re-query, re-gate, and re-review.

## Parent merge, abandonment, or rename

Do not assume a forge changes a child target. After the parent operation:

1. Re-query the parent result and identify each **immediate child** from open PR data.
2. Explicitly retarget each immediate child, one at a time, with
   `gh pr edit <child-pr> --base <verified-replacement-base>`.
3. Re-query `baseRefName`, `headRefName`, and `state` for each child.
4. Preserve every old parent boundary in an old-parent map and maintain a new-parent map.
   For each descendant, cascade bottom-up from the rewritten parent to its nearest child, using
   `git rebase --onto <new-parent> <saved-old-parent> <child>`; then use that rewritten child
   as the next layer's new parent. This replays only the child's commits; never replay an
   ancestor range.
5. Run required gates and obtain fresh review for every rewritten or retargeted PR. Do not
   merge or delete while any layer is stale.

A child still using a branch as its base keeps that branch alive. Before deletion, re-query
all open PRs and `baseRefName`; do not delete a branch while any open PR still uses it as a
base. If the query is incomplete, absent, unsupported, or returns HTTP 403, governance is
UNKNOWN and deletion stops. Perform a final race check immediately before deletion: re-read
open-child usage, PR base/head/state, the saved remote OID, required checks, and governance.
Only after that final readback may deletion proceed, with the exact saved-OID lease:

```sh
git push --force-with-lease=refs/heads/<branch>:<saved-remote-oid> origin :refs/heads/<branch>
```

Never use ordinary unleased deletion, an unqualified lease, or `--force`. A changed final
readback or lease failure is a stop, not a retry. Governance is UNKNOWN when evidence is
missing or stale; UNKNOWN is not approval.

## Restack and exact rewrite lease

For each rewritten branch, preserve its saved old parent and save its remote OID. Rebase,
inspect the diff, gate, and obtain fresh review. **Immediately before the push**, repeat the
full race check: re-query PR base/head/state, open-child usage, required checks, governance,
and the remote branch OID. Push only if every value still matches the reviewed candidate,
using the exact saved-boundary lease:

```sh
git push --force-with-lease=refs/heads/<branch>:<saved-remote-oid> origin <branch>
```

Never use a stale saved OID. A lease failure or changed readback is a stop: preserve evidence,
re-query, and start a new authorized candidate.

## Verification checklist

- `gh pr view <pr> --json baseRefName,headRefName,state,statusCheckRollup` matches the saved
  boundary and intended new base. The final readback occurs immediately before mutation.
- `gh pr checks <pr> --required` is interpreted with repository policy; no checks, absent
  evidence, unsupported governance fields, and HTTP 403 are UNKNOWN, not success.
- `gh pr diff <pr>` contains only the intended layer after restack.
- Every descendant is re-gated and re-reviewed after a parent rewrite or squash.
- The final race check passes immediately before any branch deletion or rewrite.
