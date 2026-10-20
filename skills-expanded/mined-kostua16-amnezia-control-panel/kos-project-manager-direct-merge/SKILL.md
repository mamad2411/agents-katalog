---
name: kos-project-manager-direct-merge
description: Direct merge safety rules for project-manager fallback merge paths, including stalled ready PRs and the manual-only alignment review.
user-invocable: true
when_to_use: "When project-manager reviews or executes a direct merge fallback or an alignment review."
category: workflows
keywords: [project-manager, direct-merge, manual-only, alignment-review, finalizer, maintainer-rejection]
metadata:
  author: project-manager
  license: repo
  version: "2.0"
---

# Project Manager Direct Merge

Direct merge is the fallback path when PR-flow/finalizer stalls or cannot handle a manual-only PR. Manual-only PRs are closed by the alignment review when the `PM_ALIGNMENT_MODE` repo variable is `enforce`; when it is `off`, the legacy approval-or-8h gate applies.

## Merge allowed

Merge only when:

- Current head required checks passed.
- Current head review signals passed, or maintainer approval exists for manual-only fallback, or the PR is a Dependabot update with a `deps-review-manual` verdict that the alignment review clears.
- Project-manager read-only review returns exact `decision: "merge"`.
- No maintainer rejection exists.

## Alignment review (enforce mode)

- A ready manual-only PR is reviewed on the next project-manager cycle; there is no age-out wait.
- Verdicts: `merge`, `request_fixes` (posts findings + `/fix-review`, capped at 3 rounds per PR), `hold` (escalates via @mention comment + `pm-escalation` issue).
- A `merge` verdict on a PR touching `.github/**` starts a veto window (default 4h, `policy.json` → `projectManager.alignmentVetoWindowHours`); the merge happens on a later cycle after expiry unless a maintainer rejects. Maintainer approval skips the window.
- PRs touching protected merge-authority paths (`policy.json` → `projectManager.protectedMergeAuthorityPaths`) and cross-repository PRs are never auto-merged: always hold + escalate.
- A `needs-review` label applied by automation at PR creation (all labeled events within 15 min of creation) counts as manual-only classification, not rejection. Any later application or renewal blocks, and missing label-event data blocks (safe default).
- Escalations are deduped per head via `alignmentEscalatedAt`; fix rounds are counted per PR (they survive head changes).

## Legacy mode (`PM_ALIGNMENT_MODE` unset or `off`)

Manual-only PRs also require either maintainer approval or 8 hours since `ready_since`.

## Maintainer rejection

Any of these block direct merge (including during a veto window):

- Current-head maintainer `CHANGES_REQUESTED`.
- `do-not-merge`.
- `needs-review` added or renewed after `ready_since` (or of unknown origin).
- Maintainer comment containing exact text `project-manager: hold`.

## Failure behavior

- Invalid review JSON means hold.
- Merge command failure creates/reuses a workflow issue and `/fix`es it.
- Do not use `--auto`; direct merge uses squash merge.
