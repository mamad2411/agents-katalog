---
name: versioning
description: Version and tag releases by SemVer. Use before any version bump, release tag, changelog entry, release notes, pre-release, or change to a manifest version, and when adopting the scheme in a repository that already has versions.
---

# Versioning and release tags

One standard for every repository: applications, libraries, CLIs, services, plugins and skill packages, API and tool contracts, and versioned governance documents (constitutions, policies). A repository's own documented policy or a hard ecosystem requirement may differ: expose the conflict and follow the stricter rule or ask.

## Version numbers

- [SemVer 2.0.0](https://semver.org/) for every released artifact; no date-based or arbitrary numbers unless the ecosystem requires them.
- **Phase 0, `0.y.z`**, until the owner declares the first public stable release: MINOR for breaking or incompatible changes; PATCH for every compatible change (features, additions, fixes, wording).
- **Stable, `≥1.0.0`**: MAJOR for breaking changes; MINOR for backward-compatible features or additions; PATCH for backward-compatible fixes, clarifications and wording.
- `1.0.0` and every later MAJOR need an explicit owner decision. Feature completeness, a template default or a skill's instruction never implies one.
- **Breaking** is judged against the documented public surface: API and SDK signatures, CLI commands and flags, MCP tools and schemas, configuration keys, data and migration formats, wire protocols, and principles of a governance document. A change that needs consumers to act is breaking; deprecate first, remove at the next breaking bump.
- Skills or templates with their own bump rules (for example Spec Kit's constitution command) map onto these: in phase 0, MAJOR becomes MINOR and MINOR becomes PATCH.

## Cadence

**Advisory (agent judgment):** Talk to the user in the language they are using, including questions and option labels; keep command names, flags, file paths, skill names and other technical names unchanged.

- One bump per release, never per commit, PR, task or amendment. Unreleased changes accumulate into one pending bump, and its release notes (or a Sync Impact Report for a governance document) list every change in it.
- An agent never cuts a release on its own. A release usually follows each finished spec: propose one when a spec is merged, summarizing what has accumulated, and let the owner decide. In phase 0 a spec's compatible changes bump the last digit; MINOR only when something breaks.
- Before proposing a release, review everything that describes the product against what ships: diagrams, the README, docs, and in-product help with its feature map. Update what drifted, or say in the proposal why not (advisory, agent judgment).
- In a plugin or skill repository, that review includes the README checklist of `plugin-packaging` (its `references/readme.md` and `readme_check.py`): run it on the release branch, fix each failure in the release pull request or record per item why not, list the owner decisions it leaves in the proposal, and rerun it on the commit you tag (advisory, agent judgment).
- A product release is a tag. A governance document is released when it merges to the default branch. A release is two pull requests: the release (version and dated changelog), then the bump to the next `-dev`, so the default branch never carries a released version as its build.
- Between releases, builds report the next expected version with `-dev` (`0.4.0-dev`); build metadata such as `+<short-sha>` may follow and never affects precedence.
- Pre-releases use `-alpha.N`, `-beta.N`, `-rc.N`, N from 1. A release candidate is the final bytes except the version string; any other change makes a new candidate.

## Single source of truth

- Each artifact has one authoritative version location: the git tag for Go modules; `package.json`, `pyproject.toml`, `Cargo.toml` or the plugin or skill manifest elsewhere. Every other copy (embedded constants, docs, catalogs, a second manifest) is derived from it or checked against it by CI or the release script.
- The manifest version equals the tag without its leading `v`.

## Tags

- Format `vX.Y.Z`, pre-release `vX.Y.Z-rc.1`. A repository releasing several components prefixes the component path: `<path>/vX.Y.Z`, one tag per released component.
- Annotated tags with the message `Release vX.Y.Z` and a short summary; signed where signing is configured.
- Tag only a commit on the default branch, or on a maintenance branch `release/X.Y` for older lines (created and fed as `commit-messages` "Branches" says), after required CI and release gates pass on that exact commit.
- Published tags are **immutable**: never move, delete or reuse one. A bad release is superseded by a new version and marked (release note, Go `retract`, npm `deprecate`).
- Go modules at major version 2 or later need the `/vN` module path suffix; plan it with the MAJOR decision.

## Release notes

- `CHANGELOG.md` in [Keep a Changelog](https://keepachangelog.com/) form, with an `Unreleased` section updated in each merged change that alters the public surface. A release moves those entries under the version heading with its date, in the date format the file already uses; a new file uses ISO 8601 (`2026-11-01`).
- Keep each entry to one or two sentences: the change and any consumer action. The reasons live in the skill, the commit and the pull request.
- Every breaking entry names the consumer action needed.
- The forge release body comes from the same changelog section.
- In a repository that ships upgrade notes (as `update` does in its `references/upgrades.json`), the release pull request writes or updates the entry for its version, as part of the documentation review; a test fails when a released manifest version has none.
- **Advisory (agent judgment):** After the tag and GitHub release, and only with the owner's explicit go for that repository (name it and the fields it changes first; the target is read from the user's marketplace entry, so the owner confirms it), open a pull request in the catalog repository that entry points to, moving `ref` to the new tag in every host catalog there that pins the plugin (a host catalog left unpinned installs the default branch, so `/update` would report a release its refresh does not install) and syncing name, description and keywords with the default-branch manifests. The catalog's CI enforces the content against the raw default-branch files, which can lag a few minutes.
- **Advisory (agent judgment):** When the release is done (the tag, the forge release, the bump to the next `-dev` and, where the owner said go, the catalog pull request), invoke `tidy` before any other work: save the handover, write back the release's owner decisions and lessons, and rename or retire the session; start the next release's work in a fresh session.

## Authority

Creating or pushing a tag, publishing a release or package, and changing a published version need explicit owner authority for that release. Preparing the bump, changelog and release notes for review needs none.

## Adoption in existing repositories

A repository that used higher numbers without any public release renumbers once onto this scheme and records the old→new mapping in its changelog. Publicly released versions are never rewritten; the next release continues from them.
