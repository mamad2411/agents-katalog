---
name: fabric-release
description: Release a Fabric mod - semantic versioning, changelogs, reproducible jars, and publishing to Modrinth, CurseForge and GitHub Releases from GitHub Actions with tokens kept in GitHub Secrets. Use when preparing a release, bumping a version, writing release automation, or when asked to "publish", "upload to Modrinth" or "make a release".
---

# Fabric release

A release is a jar that someone else will run. It must be built by CI from a tagged commit,
with a clear version and changelog, and published without any credential ever touching the
repository.

## Versioning

Use Semantic Versioning for the **mod** and put the Minecraft version in build metadata:

```
<major>.<minor>.<patch>+<minecraft_version>     e.g. 1.4.2+26.3
```

- **major**: breaking change for users or dependent mods (config format reset, removed
  feature, changed public API, world-data incompatibility).
- **minor**: new feature, new Minecraft version port, backwards-compatible.
- **patch**: bug fix only.
- Pre-releases: `1.5.0-beta.1+26.3`. Mark them as beta/alpha on Modrinth as well.
- `fabric.mod.json` gets the version through `processResources` (`"version": "${version}"`);
  set it in one place, `gradle.properties`:

```properties
mod_version=1.4.2
minecraft_version=<...>
```

```groovy
version = "${project.mod_version}+${project.minecraft_version}"
```

## Changelog

Keep `CHANGELOG.md` in "Keep a Changelog" format (https://keepachangelog.com): an
`## [Unreleased]` section that every PR updates, renamed to `## [1.4.2] - YYYY-MM-DD` at
release time, with `Added / Changed / Fixed / Removed` groups written for players, not for
developers. CI can extract the section for the release body.

## Reproducible builds

Same commit -> byte-identical jar. Add to `build.gradle`:

```groovy
tasks.withType(AbstractArchiveTask).configureEach {
    preserveFileTimestamps = false
    reproducibleFileOrder = true
}
```

Also:

- Commit the Gradle wrapper (`gradlew`, `gradle/wrapper/*`) and verify it in CI
  (`gradle/actions/wrapper-validation` or the `setup-gradle` action's built-in validation).
- Pin every dependency to an exact version in `gradle.properties` - no `+`, `latest.release`
  or `-SNAPSHOT` in a release build (the template's `loom_version` uses `-SNAPSHOT`; that is
  acceptable for the build plugin, but pin it if you need bit-for-bit reproducibility).
- Build releases only in CI from a tag, never from a developer machine.
- The artifact to publish is `build/libs/<name>-<version>.jar` from the `jar` task on 26.1+, or
  from `remapJar` on older versions. Never publish `-sources` or `-dev` jars as the main file.

## Secrets - the non-negotiable part

- Tokens (Modrinth PAT, CurseForge API token) live **only** in GitHub -> Settings -> Secrets
  and variables -> Actions, referenced as `${{ secrets.MODRINTH_TOKEN }}`,
  `${{ secrets.CURSEFORGE_TOKEN }}`. GitHub's own token is `${{ secrets.GITHUB_TOKEN }}`.
- Never put a token in `gradle.properties`, `build.gradle`, a workflow file, `.env`, a commit
  message, or a log line. If one was ever committed, **revoke it immediately** - deleting the
  commit does not un-leak it.
- Give tokens the minimum scope (Modrinth: create/write versions for the project only) and
  give the workflow minimal `permissions:`.
- Workflows triggered by `pull_request` from forks do not get secrets; never switch to
  `pull_request_target` to "fix" that for a publish job.
- Pin third-party actions to a full commit SHA (with the version in a comment) so a
  compromised tag cannot steal your token.

## Publishing workflow (GitHub Actions)

Triggered by pushing a tag like `v1.4.2`. Look up the current major versions / commit SHAs of
each action before using this; the ones below are placeholders to fill in.

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags: ["v*"]

permissions:
  contents: write        # create the GitHub Release

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>            # vX
      - uses: actions/setup-java@<sha>          # vX
        with:
          distribution: temurin
          java-version: "25"                    # what your MC version requires
      - uses: gradle/actions/setup-gradle@<sha> # vX (also validates the wrapper)

      - name: Check tag matches mod_version
        run: |
          v=$(grep '^mod_version=' gradle.properties | cut -d= -f2)
          test "v$v" = "${GITHUB_REF_NAME}" || { echo "Tag ${GITHUB_REF_NAME} != mod_version $v"; exit 1; }

      - run: ./gradlew build

      - name: Publish to Modrinth, CurseForge and GitHub
        uses: Kir-Antipov/mc-publish@<sha>      # vX - check its README for current inputs
        with:
          modrinth-id: <MODRINTH_PROJECT_ID>
          modrinth-token: ${{ secrets.MODRINTH_TOKEN }}
          curseforge-id: <CURSEFORGE_PROJECT_ID>
          curseforge-token: ${{ secrets.CURSEFORGE_TOKEN }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
          files: |
            build/libs/!(*-@(dev|sources|javadoc)).jar
          loaders: fabric
          version-type: release
          changelog-file: CHANGELOG.md
          dependencies: |
            fabric-api(required)
```

Alternatives:

- **Minotaur** (`com.modrinth.minotaur`, Modrinth's official Gradle plugin) - publish from a
  Gradle task; read the token from `System.getenv("MODRINTH_TOKEN")`, never from a property
  file. Docs: https://github.com/modrinth/minotaur
- **GitHub only**: `gh release create "$GITHUB_REF_NAME" build/libs/*.jar --notes-file notes.md`
  with `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}`.

Project ids (Modrinth slug/id, CurseForge numeric id) are public and may be committed; tokens
may not.

## Release checklist

1. All changes merged; `main` is green in CI.
2. `mod_version` bumped; `CHANGELOG.md` section dated; README "supported versions" updated.
3. `fabric.mod.json` `depends` ranges are correct for the target Minecraft version(s).
4. `./gradlew build` locally, then `runClient` (and `runServer` for non-client-only mods) on the
   built jar in a clean instance with only required dependencies.
5. Commit: `chore(release): 1.4.2`; tag: `git tag -a v1.4.2 -m "v1.4.2"`.
6. Push the tag **only with the maintainer's approval**; CI builds and publishes.
7. Verify the Modrinth / CurseForge / GitHub pages: correct file, game versions, loader, and
   dependencies; download and launch the published jar once.

## Common mistakes

- Putting `modrinth.token=...` in `gradle.properties` (even "local" ones get committed) or
  echoing a secret in a workflow step.
- Publishing from a laptop instead of CI; publishing an untagged commit.
- Uploading the `-dev`, `-sources` or a non-remapped jar.
- Version in the jar (`fabric.mod.json`) not matching the tag or the Modrinth version number.
- Declaring every Minecraft version since 1.20 as compatible on Modrinth without testing.
- Forgetting to mark Fabric API as a required dependency on Modrinth/CurseForge.
- Changelog written as commit hashes instead of user-facing changes.
- Using `pull_request_target` or unpinned third-party actions in a job that has publish tokens.
- Reusing a version number for a different jar (Modrinth and players' launchers cache by
  version).
