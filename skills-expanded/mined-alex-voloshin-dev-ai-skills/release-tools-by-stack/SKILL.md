---
name: release-tools-by-stack
description: Use this skill when the agent is picking a release tool for a stack or running version bump + changelog generation inside the `/release` workflow — for the release tooling reference covering release-please, semantic-release, Changesets, GoReleaser, cargo-release, JReleaser, plus monorepo per-package versioning via Changesets, Lerna, and Nx, including detection markers, per-tool version-bump + changelog commands, and per-stack release conventions for Node, Go, Rust, and Java.
disable-model-invocation: true
---

# Release Tools by Stack

Per-tool and per-stack reference for the `/release` workflow. Covers detection of existing release tooling, the version-bump and changelog commands each tool exposes, and monorepo per-package versioning approaches. Knowledge skill — never invoked directly; loaded as context by `/release`.

## Tool Detection Table

Before running any inline release flow, check whether the repo already has release tooling configured. If so, route to it; the team's choice supersedes anything inline.

| Marker file present | Tool |
|---|---|
| `release-please-config.json` or `.release-please-manifest.json` | release-please (Google) |
| `.releaserc*` (`.json`/`.yml`/`.js`) or `release.config.js` | semantic-release |
| `.changeset/` directory + `.changeset/config.json` | Changesets (monorepo Node) |
| `.goreleaser.yaml` / `.goreleaser.yml` | GoReleaser |
| `Cargo.toml` with `[workspace.metadata.release]` or local `release.toml` | cargo-release |
| `jreleaser.yml` | JReleaser (JVM polyglot) |

If a tool is detected:
1. Inspect its config for current state (next version, release branch, prerelease suffixes).
2. Run its release command (or open a PR / merge a release-please PR depending on tool).
3. Skip the inline version-bump + changelog + tag steps; the tool handles all three.
4. Continue at the `/release` Memory Write step so the release is recorded in `runs.jsonl`.

## Per-tool commands

### release-please

Releases happen via the GitHub Action on PR merge. Check for an open release-please PR; review and merge it instead of cutting manually. The action proposes a release PR that bumps versions and updates `CHANGELOG.md`; merging it creates the tag and GitHub Release.

Detection: `release-please-config.json`, `.release-please-manifest.json`.

### semantic-release

Releases happen in CI on push to the release branch. Verify the next release will fire; do not bump manually. Commit-message conventions (Conventional Commits) drive the version bump and changelog generation automatically.

Detection: `.releaserc*` (`.json`/`.yml`/`.js`), `release.config.js`, or a `semantic-release` entry in `package.json`.

### Changesets

Monorepo Node release tool. Per-package versioning workflow:

- `npx changeset` — for each affected package, record an intent file (`<random>.md` with package name + bump type + summary).
- `npx changeset version` — rewrites all affected `package.json` versions and changelogs based on accumulated intent files.
- `npx changeset publish` — tags and publishes (typically via CI).

Detection: `.changeset/` directory + `.changeset/config.json`.

### GoReleaser

Go release automation — builds binaries, creates archives, generates checksums, pushes to GitHub Releases / Docker registries.

Command: `goreleaser release --clean` (CI usually drives it on tag push).

Detection: `.goreleaser.yaml` or `.goreleaser.yml`.

### cargo-release

Rust release automation for crates.

Command: `cargo release <level>` — e.g., `cargo release minor`, `cargo release patch`, `cargo release major`.

Detection: `Cargo.toml` with `[workspace.metadata.release]`, or local `release.toml`.

### JReleaser

JVM polyglot release tool (Java, Kotlin, Scala, etc.).

Command: `jreleaser release` (Maven and Gradle plugins also available).

Detection: `jreleaser.yml`.

## Monorepo per-package versioning

If `.changeset/`, `pnpm-workspace.yaml`, `lerna.json`, or `nx.json` is present, the repo uses per-package versioning. Different bump strategy applies — pick by tool present:

### Changesets (Node monorepo)

For each affected package:

1. `npx changeset` — records an intent file (`<random>.md`) with package name + bump type + summary.
2. `npx changeset version` — rewrites all affected `package.json` versions and updates per-package changelogs.
3. `npx changeset publish` — tags and publishes (or via CI).

Use when: Node monorepo with independent per-package versions; team wants explicit human-authored intent files; pnpm/yarn workspaces.

### Lerna

- `npx lerna version <minor|patch|major>` — bumps versions across affected packages.
- `npx lerna version --conventional-commits` — derives bumps from commit history.
- `npx lerna publish from-package` — releases the bumped packages.

Use when: existing Lerna workspace; Conventional Commits already in use.

### Nx release

- `npx nx release` — replaces Lerna for Nx workspaces 17+.

Use when: Nx workspace (17+); team has standardized on Nx tooling for build + release.

For monorepos, fall back to per-package single-package flow only when the team has decided to handle one package outside the workspace tooling.

## Per-stack release conventions

If no release tool is detected, the inline `/release` flow updates version files per stack:

| Stack | Files to Update |
|---|---|
| Node.js | `package.json` (`version` field) |
| Java/Maven | `pom.xml` (`<version>`) |
| Java/Gradle | `build.gradle` (`version`) |
| Python | `pyproject.toml` (`version`) |
| .NET | `*.csproj` (`<Version>`) |
| Go | Git tag only (no version file) |

## When this applies

| Phase | Apply this knowledge |
|---|---|
| `/release` detection (Step 0a) | Pick tool from the detection table |
| `/release` version bump (Step 3) | Run the per-tool command, or fall back to per-stack file edits |
| `/release` changelog (Step 4) | Use the per-tool changelog output (release-please / semantic-release / Changesets generate it; GoReleaser / cargo-release / JReleaser emit release notes) |
| `/release` monorepo flow (Step 3a) | Route to Changesets / Lerna / Nx based on workspace marker |

## Integration

- **Used by**: `/release` (orchestrator — detection + bump + changelog stages)
- **External references**:
  - release-please: https://github.com/googleapis/release-please
  - semantic-release: https://semantic-release.gitbook.io
  - Changesets: https://github.com/changesets/changesets
  - GoReleaser: https://goreleaser.com
  - cargo-release: https://github.com/crate-ci/cargo-release
  - JReleaser: https://jreleaser.org
