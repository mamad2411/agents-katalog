---
name: self-merge
description: "Low-risk self-merge lane: merge a PR touching only allowed paths (tests, briefs, notes, eval cases) once its gate and review logs are green on the exact head. Also clears owed reviews at session start."
---

# The self-merge lane

Off until the owner accepts it (`selfMerge.enabled` in `.agents/trust-before-scale.json` (falling back to `.claude/trust-before-scale.json`)).

1. Write the evidence on the PR's head:
   `{ echo "HEAD=$(git rev-parse HEAD)"; <gate>; } > gate.log 2>&1; echo "EXIT=$?" >> gate.log`
   `{ echo "HEAD=$(git rev-parse HEAD)"; scripts/codex-review.sh <branch>; } > review.log 2>&1; echo "EXIT=$?" >> review.log`
2. Post any `selfMerge.requiredComments` evidence: each configured pattern must match a line in a PR comment that
   itself carries `head <sha>` with the current head’s first 7–40 lowercase hex characters (case-sensitive `head`).
   Acme Flutter requires both the Codex local review and `/routine` evidence comments. Fix or answer every finding before merging.
3. `node scripts/tbs/self-merge.mjs <pr> --gate gate.log --review review.log --dry-run`: every refusal names its reason.
4. Without `--dry-run` it labels the PR `self-merged`, comments that review is owed, then merges with
   `--match-head-commit`. Delete the branch and worktree yourself afterwards.
5. **Owed reviews:** `node scripts/tbs/self-merge.mjs --owed`. Read each; label `reviewed-after-merge`, or revert.
   Review hook skips printed since the oldest owed PR, or all logged skips if no PR review is owed.

The block-list always wins over the allow-list: product code, rules, functions, payments, auth, release config,
`.agents/`, `.claude/` and agent instructions never take this lane.

New eval files may use the lane. Modifying, deleting or renaming an existing `evals/**` file (including
`result.json`) needs the project's normal review: changing an existing eval case can loosen a gate.
