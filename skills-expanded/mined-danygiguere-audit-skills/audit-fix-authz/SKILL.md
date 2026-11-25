---
name: audit-fix-authz
description: Remediation patterns for authorization findings. Use after an audit confirms an authz or IDOR issue and the user asks for a fix — policy checks, ownership scoping.
---

Read `../audit/references/remediation/authz-patterns.md` and apply its patterns to fix the
confirmed findings the user referenced. Make the smallest change that restores
the invariant, and keep style consistent with the surrounding code.
