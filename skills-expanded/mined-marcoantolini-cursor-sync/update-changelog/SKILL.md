---
name: update-changelog
description: >-
  Maintains CHANGELOG.md per Keep a Changelog 1.1.0. Two workflows: refresh
  [Unreleased] from git (update-changelog command), or cut a semver release and
  bump version manifests (update-changelog-release command). Use when the user
  invokes those commands, asks to update the changelog, refresh Unreleased, or
  release a new version with aligned package versions.
disable-model-invocation: true
---

# Update changelog

Specs: [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) · [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html)

Stack-agnostic. Use **git** for source-of-truth on changes and **KAC** for changelog prose.

## Command routing

| User invokes | Run |
|--------------|-----|
| **`/update-changelog`** | [Workflow A — Unreleased only](#workflow-a--unreleased-only) |
| **`/update-changelog-release`** | [Workflow A](#workflow-a--unreleased-only), then [Workflow B — Release](#workflow-b--release) (includes version manifest bumps) |

Do **not** cut a release or bump `package.json` / `thunderstore.toml` / etc. unless the user used **`update-changelog-release`** (or explicitly asked for a full release in the same message).

---

## Shared preparation

1. **Locate changelog** — default `CHANGELOG.md` at repo root; accept a user-provided path. Read the full file.
2. **Ensure KAC header** exists (add if missing, keep if present):

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
```

3. **Ensure `## [Unreleased]`** exists as the **first** version section (create empty section if missing).
4. **Gather changes** (parallel when possible):
   - `git status`
   - `git diff` and `git diff --staged`
   - `git log -1 --oneline`
   - **Only for Workflow A with `commits` argument** (see command file): also `git log` since last release tag or since the newest `## [X.Y.Z]` in the changelog, plus matching `git diff`.

---

## Keep a Changelog rules (required)

- Use only these section headings under a version (omit empty sections):
  - `### Added` · `### Changed` · `### Deprecated` · `### Removed` · `### Fixed` · `### Security`
- **No** custom sections (“Documentation”, “Misc”, “Internal”).
- Bullets: concise, **user impact**, not file paths. Link `#123` / PRs when known.
- **Merge** with existing `[Unreleased]` bullets; refine duplicates instead of repeating.

| Signal | Section |
|--------|---------|
| New feature, option, API | Added |
| Behavior or config change | Changed |
| Bug fix | Fixed |
| Removed feature / option | Removed |
| CVE / security fix | Security |
| Soon removed | Deprecated |

| Conventional commit | Usually |
|--------------------|---------|
| `feat` | Added (or Changed) |
| `fix` | Fixed |
| `docs` | Changed if user-facing; else skip |
| `refactor`, `perf` | Changed |
| `!` / `BREAKING CHANGE` | Changed + breaking note, or Removed |
| `chore`, `ci`, `build` | Skip unless user-visible |

Details: [reference.md](reference.md)

---

## Workflow A — Unreleased only

**Goal:** Document work in progress under `[Unreleased]`. **Do not** rename the section or bump package versions.

1. Complete [Shared preparation](#shared-preparation).
2. Update **`## [Unreleased]`** from git (working tree by default; include recent commits only if the command says so).
3. **Do not** edit released version sections.
4. In the reply, show the full updated **`## [Unreleased]`** block.
5. If `[Unreleased]` is non-empty, add a short **suggested next version** line (e.g. “Likely **0.3.0** (MINOR) when you release — use `/update-changelog-release`.”). Do **not** cut the release in this workflow.

---

## Workflow B — Release

**Goal:** Ship what is in `[Unreleased]` as a dated version and align product version fields across the repo.

### B1 — Refresh Unreleased

Run [Workflow A](#workflow-a--unreleased-only) first so `[Unreleased]` matches current git state (including uncommitted work that belongs in this release).

### B2 — Choose semver

1. Read the **latest released** version from the changelog (first `## [X.Y.Z]` or `## [X.Y.Z] - date` below `[Unreleased]`).
2. Classify everything under `[Unreleased]` using [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html):
   - **PATCH** — backwards-compatible fixes only.
   - **MINOR** — backwards-compatible features.
   - **MAJOR** — incompatible API/behavior users must react to.
   - **`0.y.z`** — MINOR may include breaking changes; document breaks in bullets.
3. Compute **newVersion** = bumped latest (e.g. `0.2.0` + MINOR → `0.3.0`).
4. State **newVersion** and **rationale** in the reply before editing files.

If `[Unreleased]` is empty, stop and tell the user there is nothing to release.

### B3 — Cut changelog

1. Rename `## [Unreleased]` → `## [newVersion] - YYYY-MM-DD` (ISO 8601; use today unless the user gave a date).
2. Move all `### Added` / `### Changed` / … content under the new heading (unchanged bullets).
3. Insert a new empty `## [Unreleased]` **above** the new version (still below the intro blurb).

### B4 — Bump version manifests

Discover and **edit** every **product semver** field in the repo so it matches **newVersion**. See [reference.md](reference.md) for common paths.

**Process:**

1. Search the repo for the **current** version string (from B2’s “latest released”) in likely manifests.
2. Update only fields that hold the **package / app version** (not schema or API format versions).
3. Prefer precise edits (same string format: quoted semver, no `v` prefix unless the file already uses it).
4. If multiple packages exist (monorepo), bump only the package(s) this changelog describes; ask if unclear.

**Do not bump:** `schemaVersion`, `apiVersion`, `lockfile` dependency versions, tool config schema ids.

**Thunderstore / tcli:** `[package]` `versionNumber = "X.Y.Z"` only — never `[config]` `schemaVersion`.

### B5 — Reply summary

Include:

1. **newVersion** and semver rationale  
2. The new **`## [newVersion] - date`** section (copy from file)  
3. Table: **file · key · old → new** for every manifest updated  
4. Reminder: run `git-commit` and your project’s publish/tag workflow if not asked to commit here  
5. **Do not** `git commit`, `git push`, or `git tag` unless the user explicitly requested it in the same message

---

## Monorepos

- One changelog per package, or ask which path the release is for.
- Bump only manifests for that package.

## What not to do

- Invent changelog bullets not supported by git or existing `[Unreleased]` text.
- Cut a release in Workflow A.
- Leave version manifests on the old number after Workflow B.
- Rewrite history in released changelog sections.

## Additional reference

- Manifest table, bump examples, checklist: [reference.md](reference.md)
