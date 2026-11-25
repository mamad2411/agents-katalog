---
name: review
description: Prepare an independent cross-model code review and check the Proof Ledger — bundles a task spec plus its diff into a review pack for a reviewer from a different model family, and reports which completed tasks carry real evidence (failing tests first, green gate, approved review, real execution, existing commit). Use when the user asks for an independent or second-opinion review of AI-written changes, wants to verify a task was really done, or asks for a proof, audit trail or PROOF.md of how the code was verified.
---

# RealityGate review and proof

## Cross-model review pack

The model that wrote the code shouldn't be its only reviewer, because AI review errors are
correlated within a model family.

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/realitygate.mjs" review-pack specs/R1/T-014-invite.md --base main
```

(Outside the plugin: `npx --yes realitygate review-pack <spec> --base <ref>`.)

This writes `.agent/review/<task>.md` with reviewer instructions, the spec, the diff and new
files (`.env*` excluded). Tell the user to paste it into a reviewer from a different model
family. When they paste back a `VERDICT:` line and findings, record them under `## Review` in
`.agent/journal/<task>.md`. `[REJECTED]` sends the task back to implementation with the
findings as the fix list.

If no second model is available, say so and leave the task in `AWAITING_REVIEW`. Never
review your own diff and record it as the independent verdict.

## Proof Ledger

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/realitygate.mjs" proof --md
```

This lists every DONE task in `.agent/STATE.json` and whether its journal has each piece of
evidence. It writes `PROOF.md` with a "tasks verified" badge. Report unverified tasks plainly.
A DONE task without evidence should be reopened, not hidden.
