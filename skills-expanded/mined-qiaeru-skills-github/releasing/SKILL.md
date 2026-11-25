---
name: releasing
description: Cut a new version of one of the owner's public GitHub repos. Use when the owner asks to publish, ship, tag, bump, or release a version (patch, minor, major). Promotes the CHANGELOG, commits, tags, and publishes the GitHub Release with gh, in the repo's language.
---

# Release procedure

Pick the bump per semantic versioning: patch for bug-fixes only, minor for any new user-visible feature or deprecation, major for breaking changes that require user or operator action. Read it off the repo rather than from memory of the session: the headings under `[Unreleased]` (a `Removed` or a change users must adapt to means major; otherwise any `Added` or `Deprecated` means minor, and `Fixed` or `Security` alone means patch; a `Changed` counts as minor when it gives users something new and as patch when it only adjusts existing behavior), or without a CHANGELOG the commit types since the last tag (only `fix:` means patch, a `feat:` means minor, a `!` or a `BREAKING CHANGE:` footer means major). A pre-release (`X.Y.Z-rc.N`, `-beta.N`) follows the naming of the repo's existing tags, is published with `--prerelease` (step 4), and leaves `[Unreleased]` unpromoted unless the CHANGELOG already carries pre-release sections. Read today's date from the shell (`date +%F` or `Get-Date -Format yyyy-MM-dd`, since the bare commands print a locale-dependent format), not from memory: a wrong date in a release heading is public and permanent once the tag is pushed.

The CHANGELOG bullets and the Release notes follow the repo's language, per `committing` step 0. The release commit follows `committing` step 1 (straight to `main` by default, a pull request when the repo requires one, and in that case tag only after the merge), and with `gh` authenticated you publish the Release and check the CI runs yourself. The owner's request to release is the approval to tag and publish; do not ask again, only run the checks in step 4.

## 1. Pre-flight: run the `committing` checklist

A release ships the docs as well as the code, so before bumping anything run the `committing` pass over everything since the last release: the range `<last-tag>..HEAD`, with `<last-tag>` from `git describe --tags --abbrev=0`, or the whole history on a first release. If that range is empty, there is nothing to release: stop and tell the owner rather than publishing an empty version. Confirm the docs are current and no change left an existing doc stale, update any `CLAUDE.md` the work invalidated or extended, and prune comments to the strictly useful. Then, when the repo carries a `CHANGELOG.md`, make sure `[Unreleased]` is complete: every user-visible change since the last tag has a bullet, there are no duplicates, and it reads cleanly for a human.

If the project has a typecheck, build, or validation step (a lint script or a repo-invariants check counts), run it now and confirm it passes before you bump anything. When publishing the Release triggers a build (step 5), a broken build is cheap to find before the tag and painful after. When the real build only runs in Docker or CI, run the cheapest equivalent checks instead (syntax check the changed sources, parse any JSON or config they touch) and tell the owner the actual build will run in CI when the tag is pushed, so they know it is still unverified at tag time.

## 2. Bump the version

Find where the version lives and bump it:

- Node: run `npm version X.Y.Z --no-git-tag-version`, which bumps `package.json` and the two `version` keys of `package-lock.json` (the top object and `packages.""`) without committing or tagging. In a workspace monorepo add `--workspaces --include-workspace-root` so every workspace `package.json` and its `packages.<workspace>` lockfile node move too; miss those and `npm ci` rejects the lockfile as out of sync, which breaks any Docker build that runs it. Several independent packages side by side, each with its own lockfile and no workspaces (say a root package and a `server/` package): run the command in each folder. Then check `git diff` touches only `version` keys. When `npm` is unavailable, edit those same keys by hand and never blind-replace the old version string across the lockfile: a dependency can carry the same number by coincidence. No dependency changes belong in a release commit.
- Other ecosystems: `pyproject.toml` / `Cargo.toml` / `*.csproj` / `composer.json` and their lockfiles, as applicable.
- Claude Code plugin: bump `version` in `.claude-plugin/plugin.json`, then validate the manifest (`claude plugin validate .`, or `npx -y @anthropic-ai/claude-code plugin validate .` when the CLI is not on PATH).
- Content-only repos (docs, dotfiles, config): there is no manifest. The tag is the version; there is nothing to bump.

## 3. Promote the CHANGELOG

In `CHANGELOG.md`, rename `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD` and add a fresh empty `[Unreleased]` section above it. Re-read every bullet in the section being promoted and apply the tightening rule from `committing` step 5 (short sentences, no implementation detail, grouped under the standard English change-type names). Never rewrite already-released sections.

For example, a `## [Unreleased]` carrying this session's bullets becomes `## [1.4.0] - 2026-05-27` (today's date), with a new empty `## [Unreleased]` inserted above it.

A repo without a `CHANGELOG.md` skips this step; its Release notes (step 4) are written from the commits instead.

## 4. Commit, tag, and publish

Make one commit, `chore(release):` followed by a subject in the repo's language shaped like the previous release commit (`git log --grep="^chore(release)" -1`), for example `chore(release): cut version X.Y.Z`, with the `Co-Authored-By` trailer per `committing` step 1. When steps 2 and 3 changed nothing (no manifest, no CHANGELOG), there is no release commit: tag the current `HEAD`. Before tagging, confirm the tag number, the manifest version(s) just bumped, and the new CHANGELOG heading (whichever exist) all carry the same `X.Y.Z`; a mismatch here is the classic release-day bug and is painful to fix once the tag is public. Also confirm the working tree is clean (`git status`) and `HEAD` is the commit you mean to tag, since a public tag is cheap to create and costly to move. When the repo has immutable releases enabled, the tag cannot move at all once the Release is published (the title, the notes, and the pre-release and latest flags stay editable), so a wrong release can only be fixed by a new patch version.

1. Once the release commit is on `main` (directly, or after the pull request merged and a `git switch main && git pull`), tag it with `git tag -a vX.Y.Z -m "vX.Y.Z"` and push `main` and the tag together: `git push origin main vX.Y.Z`. The tag message is just the version; the story lives in the CHANGELOG and the Release notes.
2. Publish the Release with `gh release create vX.Y.Z --verify-tag --notes-file <file>`, plus `--prerelease` for a pre-release version. Without `--verify-tag`, a tag missing on the remote (a push that silently failed) makes gh create it on the default branch's latest commit, which may not be the release commit; with it, gh aborts instead. The notes are the CHANGELOG section just promoted minus its `## [X.Y.Z] - YYYY-MM-DD` line, verbatim: the Release title already carries the version, so repeating the heading only clutters the page. Without a `CHANGELOG.md`, write the notes from the commits since the last tag, grouped under the same English change-type names, and match the shape of the previous Release's notes (`gh release view <last-tag>`), such as a recurring intro line. Without `--title`, gh uses the tag name, which is fine. Without `gh`, give the owner the notes to paste on the Releases page under the tag just pushed.

Some publishing workflows create the Release themselves on the tag push (step 5), so `gh release create` can lose the race and report that the Release already exists. Do not delete it: set the notes with `gh release edit vX.Y.Z --notes-file <file>`. If instead the tag pushed but no Release exists, the tag is fine: do not retag, re-run `gh release create` (or the Releases page). A second tag for the same version is the thing to avoid.

When immutable releases are on (`gh api repos/{owner}/{repo}/immutable-releases --jq .enabled`) and the Release carries files, nothing can be attached after publication. Pass `--draft` to `gh release create`, upload with `gh release upload vX.Y.Z <files>`, then publish with `gh release edit vX.Y.Z --draft=false`. A workflow that attaches files has to do it on a draft too, so one that uploads after publication fails here: tell the owner rather than retry it.

## 5. Confirm the release automation

If there is no workflow under `.github/workflows/`, skip this step. Workflows that only validate (a `push` or `pull_request` trigger, no `tags:` filter and no `release:` event) are CI, not release automation: confirm their run on the release commit passed and move on.

Many of these repos publish on a tag or Release event (a Docker image, an npm package, a GitHub Pages build). Read the `on:` trigger of the publishing workflow, because it decides when the automation fires and what to watch:

- `on: push: tags:` fires when you push the tag (step 4), before the Release exists. The Release you publish next is only a notes wrapper, and the build is likely already running or finished by then. If the workflow creates the Release itself (a release action, or its own `gh release create`), step 4's race applies.
- `on: release: types: [published]` fires only when you publish the Release; nothing runs at the tag push.

Either way, confirm the run succeeded rather than only telling the owner it was triggered. Find its ID with `gh run list --workflow=<file> --commit <sha> --json databaseId,status`, retrying for a few seconds if the list is still empty right after the trigger. `<sha>` must be the full hash (`git rev-parse HEAD`): an abbreviated one matches nothing, so the list stays empty forever. Then run `gh run watch <id> --exit-status`. Without an ID, `gh run watch` prompts for a run, which fails in a non-interactive shell; without `--exit-status`, a failed run still exits 0. On a tag trigger especially, a failed build means the image or package never publishes even though the tag and Release already exist, so without this check the failure goes unnoticed.

When the repo is a Claude Code plugin, the release does not propagate on its own: remind the owner that each machine with the plugin installed picks it up through `/plugin update <name>` or Claude Code's automatic update.
