---
name: docker-29-image-security
description: Reviews Docker Engine 29 image supply chain security. Use when scanning images, evaluating Docker Scout findings, choosing base images, updating image tags, generating SBOM/provenance attestations, or triaging CVEs.
license: MIT
compatibility: Docker Scout CLI is optional and may require authentication. Static review works without Scout.
---

# Docker 29 Image Security

This skill helps the agent evaluate Docker image supply chain posture for Docker Engine 29 projects.

## When to Use

Use this skill for:

- Selecting or updating base images.
- Reviewing vulnerability scan output.
- Running Docker Scout quick checks.
- Deciding whether to rebuild with patched base images.
- Planning SBOM and provenance attestations.
- Documenting accepted image risk.

## Principles

1. Prefer trusted, maintained base images.
2. Use specific tags and record digests for releases.
3. Rebuild images regularly so patched base layers are used.
4. Generate SBOM and provenance attestations for release images when supported.
5. Treat vulnerability scans as triage input. Confirm exploitability, fix availability, and runtime exposure.
6. Do not hide findings without an explicit accepted-risk note.
7. Do not publish images before the user approves target tags and registry.

## Workflow Selection

- Use `workflows/image-security-review-workflow.md` for general image security review.
- Use `workflows/base-image-update-workflow.md` when updating base image tags or digests.

## Resources and Examples

- `resources/image-security-checklist.md`
- `examples/scout-ci-example.md`

## Scripts

Run with `--help` first:

```bash
skills/docker-29-image-security/scripts/docker-29-scout-scan.sh --help
```

The script is non-destructive and only runs Docker Scout analysis for a supplied image or local filesystem target.
