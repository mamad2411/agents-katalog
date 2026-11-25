---
name: leeway-application-final-review
description: Runs the final evidence-bound application review before release, combining requirement coverage, security, accessibility, data integrity, operations, rollback, documentation, and unresolved-risk checks. Use at a release candidate or formal acceptance gate.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  source-class: normalized-drive-candidate
---

# LeeWay Application Final Review

Map every acceptance requirement to inspectable evidence. Verify tests, security findings, accessibility, migrations, backups, observability, support ownership, rollback, licenses, and known risks. Return `READY`, `CONDITIONALLY_READY`, or `BLOCKED` with evidence links and owners. A checklist without execution evidence is not a pass.
