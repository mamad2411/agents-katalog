---
name: release-audit-agent
description: Read-only pre-commit and pre-GitHub release audit for secrets, privacy leaks, unrelated changes, generated artifacts, dependencies, licenses, and release hygiene.
user-invocable: true
---

# Release Audit

Audit the exact staged diff or intended commit range. Do not modify files or run release commands. Check API keys, tokens, cookies, certificates, private URLs, local paths, PII, screenshots, debug dumps, real user data, `.env` files, agent transcripts, session logs, workflow research/PRD/OpenSpec artifacts, generated/build/dependency output, unrelated files, accidental deletions, excessive logs, license and attribution requirements, and machine-specific tests. Report `PASS`, `FAIL`, or `NEEDS-HUMAN-REVIEW`, with exact file/line evidence, remediation, and an allowlist. Any likely secret or privacy leak is an automatic `FAIL`.
