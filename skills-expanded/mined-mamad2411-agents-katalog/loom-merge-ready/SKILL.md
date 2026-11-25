---
name: loom-merge-ready
description: Confirm current-head host attestation, hosted delivery gate, required checks, and mergeability.
---

# Loom Merge Ready

Use `loom merge-ready` for explicit preflight or `loom merge check` as the
controlled-merge read path. All inputs must identify the same PR/current head
and typed Work Item.

Merge-ready consumes:

- the authenticated current-head review artifact;
- the hosted `loom-delivery-gate` result for that head;
- GitHub required/triggered checks and mergeability;
- the formal branch/worktree binding.

Create the retained gate input from the public command, not from the raw
workflow evaluator:

```bash
loom pr gate <pr> \
  --work-item <owner/repo/work_item/id> \
  --attestation-artifact-input <attestation-artifact.json> \
  --full-output --json
```

Keep that complete `loom-delivery-gate-readback/v1` JSON in a repo-relative,
ignored workstation file and pass it with `--pr-gate-result-file`. Raw
`loom-delivery-gate/v1` JSON is not a merge-ready input.

```bash
loom merge-ready \
  --target <repo> \
  --item <owner/repo/work_item/id> \
  --pr <pr> \
  --attestation-artifact-input <attestation-artifact.json> \
  --pr-gate-result-file <repo-relative-ignored-gate.json> \
  --json
```

The gate and merge-ready steps consume the same current-head attestation.

It performs zero mutations and does not read or write repo review, current,
status, progress, shadow, freeze, or closeout carriers. Reinforced governance
only strengthens host review/validation. Removed carrier backends cannot be
enabled.

Pass allows `loom ship` or `loom merge run --apply`; it never replaces the host
merge action.
