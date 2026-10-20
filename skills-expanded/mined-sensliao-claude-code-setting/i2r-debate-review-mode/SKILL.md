---
name: i2r-debate-review-mode
description: Dual-reviewer review/debate machinery for i2r-completeness-critic and scope debate; governs the santa-loop, Reader Test Gate, and bounded repair loop.
when_to_use: Always loaded by i2r-completeness-critic for stage-07 review; also loaded during scope debate (03b) when debate_mode is active.
user-invocable: false
---

# i2r-debate-review-mode

## Role in the pipeline

This skill governs two distinct but related operations:

1. **Stage-07 review (santa-loop)** — `i2r-completeness-critic` (Reviewer A) plus
   Codex adversarial review (Reviewer B) independently review the full requirements
   bundle and each produce a `07-review.*.json` (schema: `schemas/07-review.schema.json`).
   Both must PASS for `gate.check` to emit READY.

2. **Scope debate (03b)** — when `debate_mode != "not_required"`, a structured
   multi-agent debate produces `03b-scope-debate.json`
   (schema: `schemas/03b-scope-debate.schema.json`) before downstream stages run.

## Output contract — stage-07 review

| File | Owner agent |
|------|-------------|
| `07-review.json` | `i2r-completeness-critic` (Reviewer A, fresh context, never an author) |
| `07-review.codex.json` | Codex `/codex:adversarial-review` (Reviewer B, double-blind) |

Must include `_meta.skills_used: ["i2r-debate-review-mode"]`.

Required fields (both files, per schema):
- `reviewer` ∈ `{ claude, codex, fallback-critic }`
- `verdict` ∈ `{ PASS, FAIL }`
- `failed_stage` — the specific stage where the blocking defect lives (or `"none"`)
- `iteration` — integer, 1–3
- `findings[]` — zero or more defect records (see `references/defect-taxonomy.md`)
- `gsd_ambiguity_precheck` — four dimension scores + weighted aggregate
- `reader_test` — Reader Test Gate result (see §Reader Test Gate below)

## Santa-loop protocol

Detailed rules: `references/santa-loop.md`. Summary:

```
Reviewer A (i2r-completeness-critic, fresh context)
    reads: requirements.json + PRD.md (assembled bundle)
    produces: 07-review.json
    MUST NOT be an author of any upstream stage in this run

Reviewer B (Codex /codex:adversarial-review, double-blind)
    reads: same assembled bundle
    produces: 07-review.codex.json
    MUST NOT share context with Reviewer A

Codex unavailable (quota / rate-limit)?
    → fallback: 2nd fresh-context i2r-completeness-critic (opus)
    → reviewer field: "fallback-critic"
    → log fallback in run-log.md

Gate rule: BOTH verdicts must be PASS.
If either is FAIL → enter repair loop (see §Repair loop below).
```

## Reader Test Gate

Detailed rules: `references/santa-loop.md §reader-test`. Summary:

A **third fresh context** (no run folder, no intermediate files) receives ONLY
`PRD.md`. It must independently infer and record:
- `inferred_goals` — the business purpose
- `inferred_boundary` — what is in/out of scope
- `inferred_constraints` — non-functional ceilings and hard limits
- `inferred_acceptance` — what constitutes success

If any dimension cannot be inferred → `reader_test.verdict: "FAIL"` →
`READER_TEST_FAIL` finding (severity BLOCKER) is added to `findings[]` →
`gate.check` emits BLOCKED.

The reader test is run as part of Reviewer A's pass and recorded in
`07-review.json.reader_test`. Reviewer B also runs it and records in
`07-review.codex.json.reader_test`.

## GSD ambiguity precheck

Scores four dimensions of the PRD against a 0–1 ambiguity scale.
Weights and target from CONTRACT §10:

```
goal       × 0.35
boundary   × 0.25
constraint × 0.20
acceptance × 0.20
─────────────────
score      (weighted sum, target ≤ 0.20)
```

Score > 0.20 → MAJOR finding (not BLOCKER, but blocks READY in gate).
Recorded in `gsd_ambiguity_precheck` of both review files.

## Defect classification

Every finding must carry a `defect_class` from the fixed set in CONTRACT §7
and `references/defect-taxonomy.md`. Severity must be classified as BLOCKER, MAJOR,
or MINOR per the severity table in that reference.

## Scope debate protocol (03b)

When `debate_mode != "not_required"` in `00-mode-routing.json`:

1. `i2r-scope-architect` writes initial `03-scope.json`.
2. The debate produces `03b-scope-debate.json` with `positions[]` from at least
   two named agents, a `resolution` string, and optional `changes_requested[]`.
3. `reinterpretation_risk` ∈ `{ high, medium, low }` is recorded.
4. If `changes_requested[]` is non-empty, `i2r-scope-architect` rewrites
   `03-scope.json` and marks the previous version STALE (via `i2r.py mark-stale`).
5. `03b-scope-debate.json` must be present before downstream stages run
   (enforced by `i2r-mode-gate` hook).

## Repair loop

Detailed rules: `references/repair-loop.md`. Summary:

```
If verdict == FAIL (either reviewer):
    iteration += 1
    if iteration > 3:
        STOP — surface to human; do not attempt a 4th repair
    else:
        i2r.py repair.plan → writes 08-repair-notes.json
            fields: iteration, failed_stage, findings[], repair_prompt,
                    previous_attempt_hash, new_attempt_required
        rerun ONLY the failed_stage (not the full pipeline)
        re-review from stage 07
```

`08-repair-notes.json` schema: `schemas/08-repair-notes.schema.json`.
Owner: `i2r-orchestrator` (not the critic — the orchestrator writes the plan,
the relevant stage-owner executes the repair).

## Hard rules

- Reviewers are never authors of the artifacts they review in the same run.
- Both reviewers use fresh context (no memory of authoring decisions).
- Reviewer B is always Codex or fallback-critic — never the same instance as Reviewer A.
- Max 3 repair iterations; iteration 4 is a hard stop to the human.
- `READER_TEST_FAIL` is always BLOCKER; never downgrade it.
- The `gsd_ambiguity_precheck` score > 0.20 is always at minimum MAJOR.

## References

- `references/defect-taxonomy.md` — defect classes, severity table, completeness checklist
- `references/santa-loop.md` — dual-reviewer protocol, Reader Test Gate, Codex fallback
- `references/repair-loop.md` — bounded repair loop, 08-repair-notes.json contract

Vendored sources: AutoGen multi-agent debate; Superpowers review loop; /code-review report shape (severity/evidence/blocking/fix); Anthropic doc-coauthoring reader test discipline.
