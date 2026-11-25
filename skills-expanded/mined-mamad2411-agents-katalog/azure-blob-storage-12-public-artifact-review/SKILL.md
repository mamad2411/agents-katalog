---
name: azure-blob-storage-12-public-artifact-review
description: Reviews Azure Blob Storage SDK v12 public or externally shared artifacts for data minimization, identity leakage, stable schemas, signed URLs, publication safety, and verification metadata.
license: MIT
compatibility: Requires repository access. Optional generated sample artifacts improve review quality.
---

# Azure Blob Storage 12 Public Artifact Review Skill

Use this skill when blobs are public, externally shared, downloadable by untrusted users, or used as verification artifacts.

## When To Use

Use when the task involves:

- Public containers or anonymous read access.
- Static website `$web` content.
- CDN/public origin content.
- External reports or downloadable artifacts.
- Signed URLs or SAS download links.
- Public manifests, JSON, CSV, XML, PDF, logs, exports, or generated files.
- Identity-like data in public artifact schemas.

## Required First Steps

1. Read `resources/public-artifact-sanitization-checklist.md`.
2. If scanning proposed or generated artifacts, run `scripts/azure-blob-storage-12-identity-leak-check.py --help` first.
3. Determine whether the artifact is truly public, externally shared, or only authenticated.
4. If the artifact is relied on as evidence, also activate the immutability review skill.

## Workflows

- `workflows/public-artifact-review-workflow.md`: Use for structured public artifact review.

## Resources

- `resources/public-artifact-sanitization-checklist.md`: Review checklist for public artifact content and publication.

## Scripts

- `scripts/azure-blob-storage-12-identity-leak-check.py`: Scans content for identity-like values and secret-bearing patterns.

## Examples

- `examples/public-artifact-patterns.md`: Safe patterns and anti-patterns.

## Review Rules

- Public artifacts must be intentionally public.
- Avoid identity-domain values unless explicitly required and approved.
- Prefer canonical schemas and minimization.
- Strip secrets and signed URL query strings.
- Add content hash, schema version, generation timestamp, and provenance metadata where useful.
