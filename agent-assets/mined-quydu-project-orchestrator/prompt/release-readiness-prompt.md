---
mode: agent
description: Assess whether the current Skills Orchestrator candidate is ready for internal release or a live demo.
---

# Release Readiness

Run `/deployment-review` using the current candidate, repository status, release manifest, security evidence, cross-platform evidence, documentation, installation path, demo workflow, and rollback plan.

Classify the result as `ready`, `conditional`, or `blocked`. Check that:

- The candidate is identified by exact commit and version.
- `npm run check` and candidate verification have current evidence.
- Security findings and architecture findings are closed or explicitly accepted by a named owner.
- Signing, SBOM, provenance, checksums, independent review, and current cross-platform evidence are present when required.
- Internal-only licensing and repository access match the intended audience.
- A clean clone can verify, install, create a project, and run the documented workflows.
- The live demo has a rehearsal procedure, prerequisites, and rollback plan.

Write `reports/deployment-review.json` and `reports/deployment-review.md`. This is a read-only assessment. Do not publish, deploy, sign, change repository visibility, or alter release blockers.
