---
license: CC-BY-4.0
compatibility: >-
  spec-kit extension catalogs, catalog schema_version "1.0"; publishing guide,
  community catalog, and issue templates read at v1.0.12 on 2026-09-29.
description: >-
  Publish and distribute a GitHub spec-kit extension — cut a GitHub release, write
  the catalog entry, and register it in a catalog. Defaults to the team catalog
  nq-rdl/spec-kit-extensions; also covers the public community catalog submission.
  Use when releasing/distributing/sharing a spec-kit extension, adding a catalog
  entry, or when the user runs /speckit-dev:publish.
argument-hint: "Which extension to publish, and where? (default target: nq-rdl/spec-kit-extensions)"
user-invocable: true
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Publish a spec-kit extension

> **Verify-canonical guard.** Publishing/catalog facts re-read at spec-kit v1.0.12
> (catalog schema_version 1.0, 2026-09-29). Confirm against `references/publishing.rst` and the
> live [publishing guide](https://raw.githubusercontent.com/github/spec-kit/main/extensions/EXTENSION-PUBLISHING-GUIDE.md).

## Where to publish?

**Team default:** the team catalog **`nq-rdl/spec-kit-extensions`** — add a
catalog entry there (installable, `install_allowed: true`). Consumers wire it via
`.specify/extension-catalogs.yml` (see `/speckit-dev:manage`).

**Public community catalog** (`github/spec-kit`): submit via the
**`extension_submission.yml` issue template — NOT a direct PR** to
`catalog.community.json`. Review 3–7 business days.

The `/speckit-dev:publish` invocation also triggers the `speckit-publish-target`
hook, which reminds you of the default target.

## Steps

1. Tag a GitHub release `vX.Y.Z` in the extension repo → archive at
   `.../archive/refs/tags/vX.Y.Z.zip`.
2. Compute `sha256` of the archive (recommended; verified before install).
3. Write the catalog entry (schema in `references/publishing.rst`; sample in
   `assets/catalog-entry.json`).
4. **Team:** open a PR/commit adding the entry to
   `nq-rdl/spec-kit-extensions`'s `catalog.json`.
   **Community:** file the submission issue template.

## Canonical sources

See `references/publishing.rst` and `references/canonical-sources.rst`.
