---
name: usage-monitor-release
description: Prepare and publish a versioned release for the usage-monitor repository, including picking the next version, local verification, annotated tag creation, and the GitHub Actions workflow that publishes Windows, Linux, and macOS artifacts. Use when Codex needs to cut, ship, publish, or troubleshoot a release for this project.
---

# Usage Monitor Release

Release this repository in a way that stays aligned with the current build, installer, and GitHub Actions workflow.

## Workflow

1. Read [AGENTS.md](../../../AGENTS.md), [README.md](../../../README.md), [build.gradle.kts](../../../build.gradle.kts), and [.github/workflows/release-linux.yml](../../../.github/workflows/release-linux.yml) first.
2. Invoking this skill already means "cut and publish the release". Do not ask for confirmation to commit, tag, or push — go through the whole flow, including step 8, and only report the result.
3. Confirm the release type from the request:
   - `patch`
   - `minor`
   - `major`
4. Verify that `main` is clean and matches `origin/main` — the tag must point to a commit that is
   already on the remote `main`, or `verify-version` refuses the release:
   - `git fetch origin && git status --short --branch`
   - `git log --oneline -5`
5. Pick the version. **There is no version bump commit** (#344): the version comes from the tag.
   - Current version: `git describe --tags --abbrev=0 --match "v[0-9]*" --exclude "*-beta*"`;
     compute the next `X.Y.Z` from the release type. Beta tags (`vX.Y.Z-beta.N`, issue #355) are
     never the base: without `--exclude` a beta would become the "current" stable version. If an open
     beta series `vX.Y.Z-beta.N` exists, releasing it as stable means tagging that same `X.Y.Z`.
     Beta releases have their own skill, `usage-monitor-release-beta`.
   - **Open beta series?** (`git -c versionsort.suffix=- tag --sort=-version:refname --list "v*-beta.*" | head -n 1`
     with no stable of the same `X.Y.Z`). Promoting it is `usage-monitor-release-beta promote`. A
     stable **lower** than the series (a `patch` of the previous stable while `X.Y.Z-beta.N` is open)
     is fine for everyone else but **never reaches the testers** — `X.Y.Z-beta.N` is higher. Say so
     in the report, and if the fix matters to them, follow it with a `next` beta.
   - `build.gradle.kts` resolves `version` from `-PappVersion` (the release workflow passes the tag)
     and, without it, from that same `git describe` — never edit a version literal there or in
     `src/installer/UsageMonitor.nsi` (its `!ifndef` default only serves direct `makensis` runs).
6. Keep release-related packaging aligned:
   - The Gradle `buildNsisInstaller` task passes `/DPRODUCT_VERSION=$appVersion` to NSIS.
   - The local helper [build-with-icon.ps1](../../../build-with-icon.ps1) is Windows-only and exists for icon-patched local packaging.
   - The official GitHub release artifacts come from the tag-driven workflow in [.github/workflows/release-linux.yml](../../../.github/workflows/release-linux.yml), which builds Linux, Windows, and macOS.
   - macOS `.dmg` files come from the `build-macos` job (`macos-latest` for arm64, `macos-15-intel` for x64). They are unsigned: no Apple Developer ID, no notarization. `packageDmg` cannot run on Windows or Linux, so there is no local validation path for it.
7. Run the local verification that must pass before the tag exists:
   - `gradlew.bat allTests` — mandatory. The tag is what triggers the release; a broken suite discovered after the push means a burned tag on the remote.
   - Do not package locally as a release gate. `build-windows` already runs `packageInstaller`, and `build-linux`/`build-macos` cover the other two OSes. Local packaging duplicates CI and proves only one platform.
   - `gradlew.bat packageInstaller` only when the task is debugging the installer itself (see the `usage-monitor-nsis-installer` skill).
8. Publish. Invoking this skill **is** the request to publish — never stop to ask for confirmation:
   - create the annotated tag with the temporary agent git identity:
     `git -c user.name=claude -c user.email=claude@anthropic.com tag -a vX.Y.Z -m "vX.Y.Z"`
     (annotated is mandatory — `verify-version` rejects lightweight tags)
   - push **only the tag**: `git push origin vX.Y.Z`. Nothing is pushed to `main`, so a release
     no longer triggers `CI` or `CodeQL` there.
9. Watch the GitHub Actions workflow `Release Desktop Packages` and report the outcome. `verify-version` checks that the tag is `vX.Y.Z`, annotated and on `main`; `verify` runs `allTests` and the installer scenarios in parallel with the builds; `publish-release` requires both. To rebuild an existing tag without publishing, dispatch the workflow with `publish: false`. The published release must carry every artifact family:
   - Windows: `UsageMonitor-Setup-X.Y.Z.exe`, the only Windows artifact. The `.msi` was dropped after v37 — both installers wrote to the same `%LOCALAPPDATA%\Usage Monitor` and an MSI install could never update itself.
   - Linux: `.deb`, `.rpm`, and `usage-monitor_X.Y.Z_linux_x64.tar.gz`
   - macOS: `usage-monitor_X.Y.Z_macos_arm64.dmg` and `usage-monitor_X.Y.Z_macos_x64.dmg`
   A release missing either DMG is incomplete and must be reported as such.
10. The published GitHub Release should include a short changelog built from commits between the previous `v*` tag and the new tag. That changelog is generated by the workflow's `Generate release notes` step; do not create it manually with `gh release create`.

## Guardrails

- Do not release from a dirty tree unless the user explicitly wants that risk.
- Do not ask the user to confirm the tag or the push. The skill invocation is the authorization; asking again is unwanted friction.
- Do not forget that release artifacts are published by CI from `v*` tags.
- Do not reintroduce local packaging as a release gate; CI owns packaging for all three OSes.
- Do not forget that the GitHub Release body should show the commit summary for the new version.
- Do not treat a macOS-only job failure as acceptable: the `build-macos` matrix blocks `publish-release`, and a green release without both DMGs means the workflow was edited or skipped.
- Prefer current code and workflow files over older notes in `.agents`, `.claude`, or `docs/research.md` when they disagree.
