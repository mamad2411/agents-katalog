---
name: refactor-extract
description: Walk the 4-phase refactor extraction protocol when a mechanical signal fires (duplication cluster, file-size warn or fail) or an authoring-time near-match surfaces. Tier 1.
---

# /refactor-extract

Substance lives in [`markdowns/protocols/refactor-extraction.md`](../../../markdowns/protocols/refactor-extraction.md).

Steps:

1. **Discriminate kickoff vs iteration** per [`auto-trigger-discriminator.md`](../../../markdowns/protocols/auto-trigger-discriminator.md). If iteration / polish / investigation, exit silently. Explicit `/refactor-extract` invocation bypasses; mechanical signals (duplication / file-size) and authoring-time near-match are kickoff by definition.
2. **Detect.** Cite the mechanical signal (duplication cluster `file:line ↔ file:line` from `jscpd` or similar, file-size LOC warn or fail). No mechanical signal, no advance — the duplication policy is the gate.
3. **Decide.** Produce a structured rationale (the 4+ duplicates that justify extraction, the proposed helper signature, the ≥70% applicability check, the FCPSS coverage). Run cross-vendor `plan-review` against the rationale markdown via `scripts/cross-vendor-review.sh`. Iterate to a clean pass (Tier 1: no decline path).
4. **Execute.** Write the helper / land the split + test pin first. Migrate callers one at a time with the suite green between each. Verify the signal cleared (re-run the duplication checker, re-count file size). No half-migration.
5. **Prevent regression.** The test pin is the durable guard; the duplication checker + file-size hook keep watching the surface; the duplication policy in root [`AGENTS.md`](../../../AGENTS.md) Definition of Done is the steady-state authoring rule.

Execution diff goes through standard cross-vendor code review at PR time per [`cross-vendor-review.md`](../../../markdowns/protocols/cross-vendor-review.md). Supervision pattern per [`supervision.md`](../../../markdowns/protocols/supervision.md).
