---
name: version-governance
description: Use when a user proposes changes that may require patch, minor, or major version changes, release notes, changelog updates, or version confirmation.
---

# Version Governance

Use this skill when a change is release-visible and needs release classification, version selection, release notes, or confirmation. Do not use it to name or unblock drafting a spec.

## Default Rule

Use semantic versioning:

- Patch: typo fixes, copy edits, docs-only refinements, small bug fixes, dependency patch updates, non-behavioral cleanup.
- Minor: backward-compatible features, new optional workflows, new templates, new docs sections, non-breaking config additions.
- Major: breaking changes, removed behavior, renamed public commands, incompatible schema/API changes, governance model changes.

## Workflow

1. Confirm that the change is release-visible; otherwise stop without version ceremony.
2. Detect current version from package metadata, plugin manifests, the release changelog, or release tags.
3. Classify the requested change as patch, minor, or major.
4. Explain the reason in one sentence.
5. Propose the exact next version.
6. Ask the user to confirm the version before release work or public changelog updates.
7. After confirmation, update the manifest/package metadata and `CHANGELOG.md`.

## Examples

- `0.1.0` plus copy-only docs fix -> `0.1.1`.
- `0.1.0` plus a new migration skill -> `0.2.0`.
- `0.2.3` plus a changed governance file layout that breaks old repos -> `1.0.0` or next major.

## Rules

- Do not silently publish a version bump.
- Do not block spec drafting or couple a spec file name to the proposed release version.
- If multiple changes differ in severity, use the highest required bump.
- If the repo already has versioning rules, use them unless the user asks to adopt OpenArc defaults.
- Optionally record release impact in an existing relevant spec or plan. The release manifest, release changelog, and tags remain authoritative; do not create or rename a spec or plan solely to record a version decision.
