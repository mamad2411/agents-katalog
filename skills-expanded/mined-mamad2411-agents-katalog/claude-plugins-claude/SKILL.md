# CLAUDE.md — maintenance notes for this marketplace

This repo is a Claude Code plugin marketplace (`name: aimfeld`) that currently ships one plugin, `codebase-audit`. This file captures the non-obvious bits of maintaining and releasing plugins here, so future changes don't have to re-derive any of it. User-facing install/use docs live in the root `README.md` and per-plugin `plugins/<name>/README.md`.

## Repo layout

- `.claude-plugin/marketplace.json` — marketplace catalog. Lists plugins by name + relative `source` path.
- `plugins/<name>/.claude-plugin/plugin.json` — per-plugin manifest (name, version, author, keywords).
- `plugins/<name>/CHANGELOG.md` — Keep a Changelog format, one per plugin.
- `plugins/<name>/skills/<skill>/SKILL.md` + `references/` — skill content the plugin exposes.
- `plugins/<name>/examples/` — published sample outputs referenced from the README.

Paths in `marketplace.json` resolve relative to the marketplace root (the directory that contains `.claude-plugin/`), not relative to the JSON file itself. Don't use `../` in a `source` path — the marketplace treats it as out-of-tree and it won't install.

## How a release actually reaches users

- Marketplace clients cache by **plugin version**. If two commits share the same `plugin.json` version, Claude Code treats them as identical and skips the update. **Bumping `version` is what publishes a release.** No bump, no propagation.
- `version` lives in `plugins/<name>/.claude-plugin/plugin.json` only. Do not also set it in the marketplace entry — `plugin.json` silently wins and a split version is a footgun. (From the reference docs: *"If also set in the marketplace entry, `plugin.json` takes priority. You only need to set it in one place."*)
- **Third-party marketplaces have auto-update OFF by default.** From the docs: *"Official Anthropic marketplaces have auto-update enabled by default. Third-party and local development marketplaces have auto-update disabled by default."* This is a per-user, per-marketplace toggle — there is **no way** for a marketplace author to flip this default for consumers. Users must enable it themselves in `/plugin` → Marketplaces → `aimfeld` → Enable auto-update.
- After a tagged release lands on `main`, users pick it up in one of three ways:
  - **Auto-update, opted in:** Claude Code refreshes the marketplace at startup and updates installed plugins. When something actually updated, the user is prompted to run `/reload-plugins`.
  - **Manual, on demand:** `/plugin marketplace update aimfeld` followed by `/reload-plugins`.
  - **Fresh install:** `/plugin install codebase-audit@aimfeld` picks up the current version.
- **Native marketplace auto-update requires Claude Code ≥ 2.0.70.** Older clients can only update manually.
- **There are known bugs in the update path** (tracked upstream): stale marketplace clones not fast-forwarding, installed plugin not actually reloading after marketplace update, npm-sourced plugins using stale caches, etc. Expect the occasional report of "I ran update but nothing changed" — workaround is usually `rm -rf ~/.claude/plugins/cache/aimfeld && /plugin marketplace update aimfeld` and then a Claude Code restart. See upstream issues [#26744](https://github.com/anthropics/claude-code/issues/26744), [#17361](https://github.com/anthropics/claude-code/issues/17361), [#29071](https://github.com/anthropics/claude-code/issues/29071), [#46594](https://github.com/anthropics/claude-code/issues/46594).

## Release playbook

Assume PRs with user-visible changes are already merged to `main`. To cut a release:

1. **Decide the version bump** (semver, plugin-scoped):
   - **Major** — breaking changes to skill output shape or invocation surface that downstream consumers likely depend on.
   - **Minor** — new user-visible capability (e.g. a new grading dimension, a new skill).
   - **Patch** — refinements/fixes to existing behavior with no new surface (e.g. more accurate probing inside an existing dimension).
2. **Bump** `plugins/<name>/.claude-plugin/plugin.json` → `"version": "X.Y.Z"`.
3. **Update** `plugins/<name>/CHANGELOG.md` with a new `## [X.Y.Z] — YYYY-MM-DD` section using `### Added / Changed / Fixed` groups, each entry linking the PR that introduced it. Also add the release-tag link at the bottom.
4. **Open a PR from a release branch** — direct push to `main` is blocked for this repo. Name the branch `release/<name>-vX.Y.Z`.
5. **Squash-merge the PR.**
6. **Tag the squash-merge commit** as `<plugin-name>-vX.Y.Z` (e.g. `codebase-audit-v0.2.0`). The plugin-name prefix is non-negotiable — future plugins in this marketplace will tag independently and share the tag namespace.
7. **Publish a GitHub release** with `gh release create <tag>` and notes built from the CHANGELOG entry. This isn't required for the update mechanism but is the discoverable record.

Verification after a release:

- `/plugin marketplace update aimfeld` — client should report a version change.
- `/plugin` — confirm the plugin lists the new version.
- Invoke the skill on a throwaway repo and spot-check the user-visible change is actually present in the output.

## Repo conventions

- **Branch protection:** direct push to `main` is denied. Every change goes through a PR.
- **Merge strategy:** squash-merge. The merge commit is what gets tagged.
- **Commit message co-author trailer:** `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>` — matches existing history.
- **Changelog discipline:** every user-visible PR should either update `CHANGELOG.md` directly or the release PR should translate it into an entry. Link every entry to its PR.

## Caveats worth remembering

- **Seeded/containerized installs don't auto-update.** If anyone consumes this marketplace via `CLAUDE_CODE_PLUGIN_SEED_DIR`, bumping the version here does nothing for them — the seed image has to be rebuilt. Not in scope today, but flag it if a user reports "I pushed v0.x.y but a colleague still sees the old one."
- **Private-marketplace auto-updates need a token in the environment.** Irrelevant while this repo is public; relevant if we ever flip it private (need `GITHUB_TOKEN` in the user's shell for background updates to work).

## Not automated yet (deliberate)

- No GitHub Actions release workflow. Manual bump + tag is enough at one plugin, low merge frequency. Revisit `release-please` / `changesets` once a second plugin lands or releases become frequent — at that point the tag-prefixing convention above already supports per-plugin release trains.
- No CHANGELOG linter. Rely on PR review.
