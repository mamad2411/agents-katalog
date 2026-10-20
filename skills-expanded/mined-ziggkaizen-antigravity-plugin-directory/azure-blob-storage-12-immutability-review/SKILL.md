---
name: azure-blob-storage-12-immutability-review
description: Reviews Azure Blob Storage SDK v12 immutability, WORM, legal hold, version-level retention, soft delete, lifecycle, and tamper-evidence needs for public or externally relied-on artifacts.
license: MIT
compatibility: Requires repository access. Azure resource context is useful when reviewing live immutability settings.
---

# Azure Blob Storage 12 Immutability Review Skill

Use this skill when artifacts must be protected from overwrite/delete or when consumers rely on blobs as evidence.

## When To Use

Use when a task involves:

- Immutable or WORM storage.
- Legal holds or time-based retention.
- Version-level immutability.
- Container-level immutability.
- Evidence-like public artifacts.
- Tamper-evident manifests, signatures, or hashes.
- Lifecycle rules that may delete or archive protected data.
- Soft delete, versioning, retention, and recovery review.

## Required First Steps

1. Read `resources/immutability-decision-matrix.md`.
2. If scanning code/config, run `scripts/azure-blob-storage-12-immutability-policy-check.py --help` first.
3. Confirm whether the requested protection is legal/compliance immutability, application-level tamper evidence, operational recovery, or public verification.
4. Do not recommend immutability without retention duration, release/rollback, deletion, and lifecycle implications.

## Workflows

- `workflows/immutability-review-workflow.md`: Use for structured immutability design and review.

## Resources

- `resources/immutability-decision-matrix.md`: Decision guide for WORM, versioning, soft delete, hash/signature, and lifecycle choices.

## Scripts

- `scripts/azure-blob-storage-12-immutability-policy-check.py`: Scans proposed or existing content for public artifact publication without tamper-evidence or immutability indicators.

## Examples

- `examples/immutability-policy-notes.md`: Notes and anti-patterns.

## Review Rules

- Immutability protects against modification/deletion; it does not sanitize data.
- Time-based retention and legal hold behavior must be deliberate.
- Container-level policies and version-level policies have different operational effects.
- Account-level or container-level choices may affect unrelated workloads; consider separate containers/accounts.
