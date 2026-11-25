---
name: release-workflow
description: Prepare and verify a software release when the user asks to ship, tag, publish, deploy, or cut a release.
---

# Release workflow

Inspect the repository's existing release process, branch, versioning, CI, changelog, artifacts, and deployment target. Identify the exact release candidate and its changes. Run the required gates, verify generated artifacts and configuration, and prepare concise release notes and a rollback path.

Keep the candidate reviewable before irreversible actions. Publish, deploy, tag, or push only when the user has authorized that action. After release, verify the live version and key health signals; report the shipped version, evidence, and any follow-up.
