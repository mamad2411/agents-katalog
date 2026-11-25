---
name: cut-release
description: "Cut a git flow release of the kit: version bump, changelog, gates, then tag, GitHub release and gemini branch after owner approval. Use for cut a release, release X.Y.Z, ship a version."
---

# cut-release

1. Check git flow is set up: `git flow version` and `git config --get gitflow.branch.develop`. If git flow is missing, stop and tell the owner to install it with `brew install git-flow`; never hand-roll it. If uninitialized, run the init commands in [Maintaining the kit](../../../docs/maintaining.md#release).
2. Check `git status --porcelain`, fetch origin, and compare the starting branch with its origin ref. Stop on a dirty tree or a branch behind/diverged from origin; never stash or reset the owner's work. Require the starting branch to be up to date before proceeding.
3. Use the supplied X.Y.Z version; otherwise propose one from the `## Unreleased` entries in `CHANGELOG.md` (semver: fixes only → patch, new features → minor) and stop for the owner to confirm it. Stop if the version is already tagged (`git tag --list vX.Y.Z`) or lacks changelog content. Do not guess a version.
4. Switch to synchronized `develop`; run `git flow release start X.Y.Z`. Bump only `plugins/trust-before-scale/.claude-plugin/plugin.json`, run `node scripts/build-harness.mjs`, and rename `## Unreleased` in `CHANGELOG.md` to `## X.Y.Z` (add a one-line summary under it, as earlier sections have). Follow [Release](../../../docs/maintaining.md#release), including its Codex generation limitation.
5. Run the `run-gates` skill, review and commit all release changes, then run it again on that exact clean head. Stop for the owner's explicit go-ahead before finishing or publishing.
6. With that go-ahead, run `git flow release finish -m vX.Y.Z X.Y.Z`, then push `main`, `develop`, and `vX.Y.Z`. Check `gh release view vX.Y.Z` before any manual creation: if absent, distinguish a genuine not-found from an authentication/network error. When the workflow cannot run and the release is confirmed absent, create it with `gh release create vX.Y.Z --title vX.Y.Z --notes-file <release-notes-file>` using only the matching changelog section.
7. Publish the Gemini tree using the export and leak-check steps in [Release](../../../docs/maintaining.md#release). Never copy `.leakcheck.local` into a committed file. Report the version, gate evidence, pushes and release URL.

Tagging, pushing `main`/tags, creating a release and publishing the `gemini` branch need the owner's explicit go-ahead in that session. Stop before each unless that session's explicit go-ahead covers it.
