---
name: release
description: Cut a NeuralAgent release. Writes the CHANGELOG.md section from the commits since the last tag, bumps the version with set-version, verifies, tags and pushes so CI publishes, then checks the update manifest. Use when the user says "release", "neue Version", "ship X.Y.Z" or asks for a changelog for the next version.
---

# Release NeuralAgent

Runbook with background: `docs/RELEASING.md`. Rules: `AGENTS.md`. Commit, tag, push and deploy
only when the user asked for a release in this session. Otherwise stop after step 3 and show the notes.

## 1. Pick the version
- `git describe --tags --abbrev=0` gives the last tag. `grep -m1 '^version' Cargo.toml` gives the current version.
- New features → minor (0.3.0); only fixes → patch (0.2.2). Ask the user if unsure.
- Check `docs/HANDOFF.md`: if an earlier tag is still unpublished (Actions blocked), say so.

## 2. Write the changelog
- Material: `git log --no-merges --format='--- %s%n%b' <lasttag>..HEAD`, plus what is already
  under `## [Unreleased]` in `CHANGELOG.md`, plus `docs/notes/*.md` touched since the tag
  (`git diff --stat <lasttag>..HEAD -- docs/notes`).
- Write under `## [Unreleased]`. You can add an optional one-line summary, then only
  `### New` / `### Improved` / `### Fixed`.
- Write in user language: what they notice, one line each, no file names, D-numbers or hashes.
  Merge duplicates. Drop refactors, CI, docs and tests. Bold feature names (`**Claude view**`).
- `node scripts/changelog.mjs json` must parse. Show the user the section if they want to review it.

## 3. Bump and verify
```
node scripts/set-version.mjs X.Y.Z        # Unreleased → ## [X.Y.Z] - today + new empty Unreleased; refuses without notes
node scripts/changelog.mjs check X.Y.Z
node scripts/changelog.mjs notes X.Y.Z    # exactly what the update dialog / release notes show
pnpm typecheck && pnpm test && pnpm lint:tokens && pnpm check:docs
cargo test --workspace 2>&1 | grep -E "test result|FAILED|error" | tail -20
pnpm --filter @neuralagent/web build 2>&1 | tail -5
```
Fix failures before going on. Never edit a version's section after its tag is pushed.

## 4. Tag and push (only with the user's go)
```
git add -A && git commit -m "Release X.Y.Z"
git tag vX.Y.Z && git push && git push origin vX.Y.Z
gh run list --workflow release.yml -L 1     # then: gh run watch <id>
```
If Actions refuse to start (billing), stop and tell the user. See "While GitHub Actions is
blocked" in `docs/RELEASING.md`. Do not move the tag and do not upload by hand.

## 5. Check and deploy
- `curl -s https://agent.neuralhub.dev/api/releases/latest` should show X.Y.Z and the notes.
- Deploy the relay and website only when asked: skill `deploy-web` (background in
  `docs/RELEASING.md`). That publishes `/changelog` and makes web remotes offer the reload.
- Update `docs/HANDOFF.md` (what was released, anything unpublished).
- Never restart the user's installed app or daemon to "test" the update.
