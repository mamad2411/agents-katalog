---
name: wf-package
description: Build the Wavefoundry framework distribution pack with build_pack.py (Package Wavefoundry). Available only where the packaging prompt doc exists, normally the framework source repository.
---

# Package Wavefoundry (Wavefoundry skill)

This skill is a thin pointer: the workflow lives in `docs/prompts/package-wavefoundry.prompt.md`. Read that document and follow it; do not improvise the steps from this summary.

- Prefer `--release` for a published release; a bare `--version` build only packages. `build_pack.py` hard-fails without a matching `## [version]` CHANGELOG section, so write the changelog first.
- Gate reminder: publishing a release is operator-owned; never push tags or publish without explicit operator instruction in the current session.
- The ordered verification commands live in `docs/contributing/build-and-verification.md`.
