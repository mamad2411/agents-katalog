---
name: agent-plugin-integrity
description: Use when plugin or asset bundles need deterministic SHA-256 hashing per file and at bundle level, with reproducible integrity verification output.
---

# Agent Plugin Integrity

## Specialization

Produce deterministic integrity evidence for text-based plugin bundles by computing SHA-256 digests per artifact and an aggregate SHA-256 digest for the full bundle.

## Trigger Conditions

- A plugin manifest needs integrity metadata.
- A bundle release requires independent verification guidance.
- Consumers need to confirm artifacts were not modified after distribution.
- A maintenance update needs integrity re-baselining.

## Inputs

- Bundle identifier and version.
- Root path for included artifacts.
- Ordered include and exclude patterns.
- Canonical path rules (relative path base, path separator policy).
- Manifest output path.
- Verification report output path.

## Required Outputs

- File digest table with one row per included artifact.
- Aggregate digest computed from canonicalized, sorted file digest entries.
- Manifest-ready integrity payload containing algorithm, per-file digests, and aggregate digest.
- Verification playbook with reproducible commands and expected outputs.
- Drift result indicating match or mismatch against a prior manifest.

## Workflow

1. Resolve input boundaries and normalize all artifact paths relative to one root.
2. Enumerate included artifacts and apply exclusions deterministically.
3. Sort artifact list by canonical relative path.
4. Compute SHA-256 for each artifact.
5. Build canonical digest lines using `<relativePath>:<sha256>` format.
6. Compute aggregate SHA-256 over the joined canonical digest lines.
7. Emit a manifest payload with `digestAlgorithm`, `artifactEntries`, and `aggregateDigest`.
8. Emit verification instructions so users can recompute and compare results.
9. If a prior manifest exists, compare each file digest and aggregate digest and record drift.

## Guardrails

- Use SHA-256 only for integrity output.
- Reject weak hash selections for integrity checks.
- Fail if duplicate canonical paths are detected.
- Fail if any referenced artifact is missing at computation time.
- Keep outputs deterministic: same inputs must produce identical digest outputs.

## Deterministic Output Contract

- `digestAlgorithm`: `SHA-256`
- `artifactEntries[]`: ordered by canonical relative path
- `artifactEntries[].path`: canonical relative path
- `artifactEntries[].sha256`: lowercase hex digest
- `aggregateDigest`: lowercase hex digest over canonical digest lines
- `generatedAtUtc`: ISO-8601 UTC timestamp

## Done Criteria

- Every included artifact has a SHA-256 digest.
- Aggregate digest is present and reproducible.
- Verification playbook can be executed independently.
- Drift comparison is explicit when previous manifest data exists.
- Output contains no unresolved paths or missing artifacts.

## References

- references/source-catalog.md
- references/verification-manifest-template.md
- references/scripts/invoke-agent-plugin-integrity.ps1
- references/templates/plugin-manifest.schema.json
- references/templates/readme-verification-snippet.md
