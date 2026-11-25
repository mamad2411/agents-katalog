---
name: audit-dependencies
description: Dependency and supply-chain checklist. Use when a change adds or upgrades packages, or edits manifests, lockfiles, Dockerfiles, or CI workflows — missing or bypassed lockfiles, unpinned versions, known-vulnerable packages, typosquats, dependency confusion, mutable action or image tags, curl-pipe-shell installs.
---

Read `../audit/references/input-api-dependency/dependencies.md` and apply its
checklist to the code the user specified (or the current diff if none was
given). If the target is larger than a diff — a module, service, or whole repo —
follow `../audit/references/methodology/scope.md` first. Verify each candidate
with `../audit/references/methodology/verify.md` before reporting. Report
surviving findings with `file:line` references and a severity assigned per
`../audit/references/methodology/severity.md`; if nothing survives, say the
checklist came back clean. Report only — do not change code unless the user asks
for a fix.
