---
name: build-feature
description: Walk the feature-build protocol when adding/creating/building/implementing a new feature — classify type, run near-match scan, FCPSS, tier-correct review.
---

# /build-feature

Substance lives in [`markdowns/protocols/build-feature.md`](../../../markdowns/protocols/build-feature.md).

Steps:

1. **Discriminate kickoff vs iteration** per [`auto-trigger-discriminator.md`](../../../markdowns/protocols/auto-trigger-discriminator.md). If iteration / polish / investigation, exit silently. Explicit `/build-feature` invocation bypasses and walks the full protocol.
2. **Classify the feature.** Note the stake tier from [`stake-matrix.md`](../../../markdowns/protocols/stake-matrix.md).
3. **Run the near-match scan.** Up to 5 nearest existing helpers by file proximity + name-token overlap + signature shape. For each candidate, answer: would extension be ≥70% applicable? Extension wins by default; if rejecting extension, document the reason.
4. **Draft FCPSS coverage** per [`fcpss-gate.md`](../../../markdowns/protocols/fcpss-gate.md).
5. **Implement.** Pre-commit hooks are the syntactic gate; FCPSS + tests are the semantic gate.
6. **Review per tier** per [`stake-matrix.md`](../../../markdowns/protocols/stake-matrix.md) and [`supervision.md`](../../../markdowns/protocols/supervision.md): Tier 1/2 = cross-vendor mandatory + chat-checkpoint + wait for "ship it"; Tier 3 = same-vendor self-review; Tier 4 = pre-commit only.
7. **Ship gate.** FCPSS clean, tests pass, pre-commit clean, tier-correct review done.

If the scan in step 3 surfaces a candidate where extension wins, enter [`refactor-extraction.md`](../../../markdowns/protocols/refactor-extraction.md) at the Execute phase directly (authoring-time near-match bypasses the mechanical-signal gate).
