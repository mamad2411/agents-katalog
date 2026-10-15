---
name: curate-photonic-example-case
description: >-
  Copies legacy or nonconforming photonic simulation cases into isolated
  staging, removes non-library content, completes traceable metadata, validates
  artifacts, and prepares ExampleCandidates for Human G3 review without
  modifying source cases. Use when importing, cleaning, migrating, normalizing,
  reviewing, or adding existing cases to the folder Example Library.
---

# Curate photonic example case

Normalize an existing case for the folder-backed Example Library. Never modify,
rename, format, or delete source-case content.

Read [CLEANING_POLICY.md](CLEANING_POLICY.md) and
[REPORT_FORMAT.md](REPORT_FORMAT.md) before preparing a candidate.

## Workflow

1. Resolve the source and library root.
   - Explicit `--library-root` wins.
   - Otherwise use `PHOTONIC_EXAMPLE_LIBRARY_ROOT`.
   - Otherwise use `<project-root>/example-library/`.
   - Refuse a staging root located inside the source case.

2. Inspect the source read-only:

```text
python scripts/curate_case.py inspect \
  --source <case-dir> \
  --candidate-id <candidate-id> \
  --mode paper_reproduction|free_design \
  [--library-root <library-root>] \
  --target-version 1.0.0
```

The command emits `SourceSnapshot`, file decisions, blockers, and required
questions. Inspection must write nothing to the source or library.

3. Present the cleaning plan before copying. Classify every file as:
   `include`, `transform`, `exclude`, `blocked`, or `needs_human_input`.
   Stop on credentials, unknown license, path escape, symlinks/junctions,
   collisions, or an existing target version.

4. Prepare an isolated copy only after the user accepts the plan:

```text
python scripts/curate_case.py prepare \
  --source <case-dir> \
  --candidate-id <candidate-id> \
  --mode paper_reproduction|free_design \
  [--library-root <library-root>] \
  --target-version 1.0.0 \
  --plan <inspection.json> \
  [--metadata <answers.json>]
```

Use `--dry-run` for a zero-write preview. Never add an in-place or delete-source
option.

5. Clean only the staging copy:
   - remove approved exclusions;
   - preserve necessary logs and raw data;
   - normalize relative references and structured documents;
   - add only computed or traceably extracted fields;
   - record every transformation and exclusion.

6. Validate and scan:

```text
python scripts/validate_candidate.py --candidate-dir <staging-dir>
python scripts/scan_sensitive.py --candidate-dir <staging-dir>
```

Do not fabricate missing physical, execution, convergence, license, reviewer,
or quality evidence. Missing RunManifest/ValidationReport limits the candidate
to `archived`.

7. Produce `example-candidate.json`, the curation reports, and `g3-review.md`.
Keep status `pending_review`.

8. Pause for Human G3. Publication requires an approved G3 decision bound to
the exact candidate SHA-256. If staging changes, request a new decision.

9. Publish through `FolderExampleLibrary.publish()`. Never write a final version
directory or edit `catalog.json` directly.

## Intake starting from a human-reviewed case

A prior human review is useful evidence but cannot authorize a different
normalized byte snapshot. A generic historical "human review passed" record is
publication provenance only; it is not automatically an
`ExpertEvidenceAttestation` or a `confirmed` scientific review.

1. Inspect and prepare the reviewed source with the normal read-only/staging
   workflow.
2. Preserve the prior review document under staging reports.
3. Run schema, integrity, license, and sensitivity checks after normalization.
4. Compute the final `example-candidate.json` SHA-256.
5. When missing legacy numerical evidence is checked manually, require a
   separately signed `ExpertEvidenceAttestation` bound to the Run,
   ValidationReport, or candidate hash. It may approve `screened`, or
   `corroborated` when it contains a quantitative comparison; it cannot
   override known integrity/basic-physics failures. Screening must separately
   cover data integrity, units, coordinate axes, and applicable basic physics;
   every check cites a hash-bound source.
   For derived topological integrals, verify the paper-defined integration
   region and the coordinate/handedness/phasor convention before classifying a
   mismatch. Reprocessing retained fields without a solver rerun is permitted
   only when raw field columns are preserved, corrected transforms are
   hash-bound, and boundary sensitivity remains visible as a limitation.
6. Ask the reviewer to confirm or re-sign a `G3ReviewDecision` containing the
   exact final candidate hash, review outcome, accepted failures/limitations,
   and permitted uses. If normalization or an attestation changed content, the
   earlier G3 decision is stale.
7. Publish:

```text
python scripts/publish_reviewed.py \
  --candidate-id <candidate-id> \
  --decision <g3-review-decision.json> \
  [--validation-report <validation-report.json>] \
  [--library-root <library-root>]
```

An `archived` case may be published without a solver ValidationReport when G3
explicitly approves archival. Every other quality requires its corresponding
numerical evidence. `provisionally_reviewed` requires a `limited` G3 decision;
`reviewed` requires `confirmed`, code/model review, and at least one
quantitative paper, experimental, analytical, cross-solver, or partial
convergence basis.

## Format-2 metadata migration

For the six existing library cases, prepare metadata-only packages with:

```text
python scripts/migrate_quality_model.py prepare \
  --library-root <library-root>
```

This command never changes published examples or copies large artifacts.
Conservative `executed` cases receive unsigned attestation templates. Use
`finalize` after signing evidence; it recomputes the candidate hash and
invalidates any earlier G3 decision. Run `apply` only after all six exact
candidates have fresh G3 approvals. It creates a SHA-256 metadata backup,
preserves each historical G3 record, atomically replaces formal metadata, and
updates the catalog to format 2. The migration lock prevents concurrent apply
operations.

## Completion states

- **Inspected**: source snapshot and plan only; no staging writes.
- **Prepared**: source copied and cleaned in staging; source unchanged.
- **Review pending**: schema, integrity, license, and sensitivity reports exist.
- **Published**: immutable folder version and catalog entry created after G3.

Always report one state, remaining blockers, required human answers, source
snapshot hash, and candidate hash.
