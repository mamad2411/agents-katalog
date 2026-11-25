---
name: engineer-bump
description: Bump the project's semver version
---

Let's prepare this for a release by bumping the version number.

Follow these rules for x.y.z (semver) versioning:

- **x (major)**: increment for incompatible API/feature changes. Examples: breaking changes to a public API (removing or renaming methods), major rewrites or refactors that change behavior, changes that require users to update their code or dependencies to stay compatible.
- **y (minor)**: increment for backwards-compatible new features or improvements. Examples: new methods, endpoints, or features; deprecating a feature (without removing it yet); improvements that don't break existing behavior.
- **z (patch)**: increment for backwards-compatible bug fixes or small updates. Examples: fixing a bug without changing intended behavior, small performance improvements, documentation/metadata updates.

Detect which package manager this project uses and bump the version accordingly:

- **Python** (`pyproject.toml` present): update the `version` field, then run `uv sync --all-extras` to regenerate the lock file (or the equivalent command for whatever tool the project actually uses — Poetry, pip-tools — if it's not `uv`).
- **Node/TypeScript** (`package.json` present): run `npm version <major|minor|patch> --no-git-tag-version` (or the equivalent `pnpm version`/`yarn version` command matching the project's package manager), which updates `package.json` and the lock file together.

If the project has both, ask the user which one to bump, or whether both should move in lockstep.

If neither file exists, ask the user how this project tracks its version (a different manifest like `Cargo.toml` or `go.mod`, a `VERSION` file, git tags) rather than assuming — don't silently fail or guess a convention that isn't there.
