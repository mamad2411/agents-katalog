---
name: github-publication-bundle
description: Copilot-native public package release skill. Use when a workflow package needs readiness checks, source-of-truth updates, verification, and GitHub surface sync before push.
argument-hint: "<package or release goal>"
---

# github-publication-bundle

Use this skill when preparing a public workflow package for release from the `.github` surface.

## Goal

Ship only packages that an external user can actually place, use, and verify.

## Workflow

1. Confirm the package is user-authored or explicitly labeled as a wrapper/projection.
2. Run a readiness preflight:
   - README covers install, use, verify, and limits
   - manifest matches runtime support
   - example exists
   - private paths, credentials, and internal labels are absent
3. Update source-of-truth files together:
   - package README
   - package manifest
   - root README
   - `REGISTRY.md`
   - `registry.yaml`
4. Run checks:
   - package validation
   - public-safety scan
   - example and doc consistency review
5. Push only when the readiness verdict is `pass` or `pass with limitations`.
6. Report any manual GitHub UI follow-up separately.

## Output

```text
Package:
Readiness Verdict:
Changed Files:
Checks Run:
Installability Gaps:
Push Status:
Manual GitHub UI Steps:
```
