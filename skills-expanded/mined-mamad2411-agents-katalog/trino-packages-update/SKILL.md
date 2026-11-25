---
name: trino-packages-update
description: Update a local clone of a trino-packages fork to a newer Trino version. Covers the custom tarball, RPM, and custom Docker image packages, the per-version upstream checks, the build and verification steps, and the commit and README conventions. Use this when bumping trino-packages to a newer Trino release.
---

# Update trino-packages to a new Trino version

Use this skill to bump a local clone of a `trino-packages` fork from its current
Trino version to a newer one. Upstream is
[trinodb/trino-packages](https://github.com/trinodb/trino-packages), and it is
commonly forked, for example to `simpligility/trino-packages`. The skill is
fork-agnostic and operates on whatever clone you run it in. The repository
builds three packages on top of the upstream Trino release artifacts:

* **Custom tarball** — the `trino-server-custom/` Maven module,
  provisio-based.
* **RPM** — the `trino-server-rpm/` Maven module, provisio-based.
* **Custom Docker image** — the standalone `custom-docker/build.sh`, not a Maven
  module.

The heavy lifting was built during the 475 to 481 update: fetching artifacts
from GitHub releases, the move to Java 25, and the prefetch mechanism. A routine
bump to the next version is mostly version-string changes plus the per-version
upstream checks in Step 1.

For shared Trino facts — the versioning scheme, release-artifact distribution,
the Java version policy, and the contribution workflow — see the `trino` base
skill.

## How the artifacts are fetched

As of Trino 477 the server tarballs and plugin zips are published only on the
GitHub release and not to Maven Central, as covered in the `trino` base skill.
This project fetches them at build time:

* Both Maven modules run `src/main/script/prefetch.sh` in the Maven `validate`
  phase, wired through `exec-maven-plugin`. The script parses the active
  `<artifact>` entries from the provisio descriptor, downloads the matching
  files from the GitHub release, and installs them into the local Maven
  repository so provisio resolves them by GAV. Downloads are cached in
  `~/.m2/repository`, so repeated clean builds do not re-download the roughly
  300 MB core tarball.
* `custom-docker/build.sh` downloads plugin zips with the
  `downloadGithubTrinoPlugin` helper. The `downloadTrinoPlugin`,
  `downloadGavPlugin`, and `downloadUrlPlugin` helpers remain for
  Maven-repository or arbitrary-URL sources, for example an internal Nexus or
  Artifactory mirror.

## Prerequisites

* A local clone of a `trino-packages` fork or of upstream, on an up-to-date
  `main`.
* **Java 25** and Docker. Docker is required for the RPM `ServerIT` integration
  test and for the custom-docker build.
* The `gh` CLI authenticated, with network access to `github.com`.

## Step 0 — target version and branch

1. **Ask for the target version** when it is not given. Determine the current
   version from the `<dep.trino.version>` property in
   `trino-server-custom/pom.xml` and confirm the target is **newer** than the
   current one. Refuse or warn otherwise. The common case is the current version
   plus one, but a larger jump is allowed — call out that a larger jump raises
   the odds of upstream airbase, Java, or configuration changes to check in
   Step 1.

2. **Choose the branch.** Work on a feature branch and never commit the bump
   directly onto `main`. Check the current branch:
   * If it is already a suitable feature branch, ask whether to keep using it.
   * Otherwise create a new branch such as `update-<VERSION>`. Ask what to base
     it on. The default is `main`, which must be up to date first, but a tag or
     commit hash is also allowed.

## Step 1 — verify upstream release facts

Do these checks first, since they determine whether the bump is routine or needs
extra changes. Cite what you find.

1. **Confirm the release assets exist.** Check that the target version's GitHub
   release has the needed assets:

   ```bash
   gh release view <VERSION> --repo trinodb/trino --json assets \
     --jq '.assets[].name | select(test("trino-server|trino-server-core|trino-ai-functions|trino-blackhole|trino-faker|trino-jmx|trino-memory|trino-tpcds|trino-tpch"))'
   ```

   You need `trino-server-<VERSION>.tar.gz` for the RPM,
   `trino-server-core-<VERSION>.tar.gz` for the custom tarball, and the zips for
   every **active** plugin in the two provisio descriptors as well as the ones
   downloaded in `custom-docker/build.sh`.

2. **Check the airbase parent version.** Read the upstream Trino pom for the
   target version and note the `io.airlift:airbase` parent version:

   ```bash
   curl -sL https://raw.githubusercontent.com/trinodb/trino/<VERSION>/pom.xml \
     | grep -A2 '<artifactId>airbase'
   ```

   Compare it against the root `pom.xml` parent version. When it changed, bump
   it in Step 4. A new airbase version often re-enables or updates the
   **sortpom** verifier, so expect to re-sort the module poms.

3. **Check the Java version.** From the same upstream pom, note
   `project.build.targetJdk`, `air.java.version`, and the Temurin release name.
   Search the pom for `temurin` or `jdk-`. When the Java major version changed,
   also check the bundled `jvm.config` in the upstream `trino-server-core` or
   `trino-server` for flags that must be added or removed. For example, Java 25
   removed Security Manager support, so `-Djava.security.manager=allow` had to
   be dropped in the 481 bump.

4. **Check plugin availability.** To add newly available plugins, confirm their
   zips exist on the release before enabling them in the provisio descriptors or
   `build.sh`.

## Step 2 — custom tarball in `trino-server-custom/`

* In `trino-server-custom/pom.xml`, bump `<dep.trino.version>` to the new
  version.
* In `trino-server-custom/README.md`, update all version references: the
  configured-version line, the example tarball filename, the Java version when
  it changed, and the installation example directory.
* Only touch `src/main/provisio/trino-custom.xml` when adding or removing
  plugins.
* Only touch the `src/main/resources/etc/*.properties` files when the
  configuration needs to change. The `log.properties` file keeps `io.trino=WARN`
  together with `io.trino.server.Server=INFO` so the
  `======== SERVER STARTED ========` banner is logged.

## Step 3 — RPM in `trino-server-rpm/`

* In `trino-server-rpm/pom.xml`, bump `<dep.trino.version>`. When Java changed,
  also bump `<project.build.targetJdk>` and `<air.java.version>`.
* In `trino-server-rpm/src/test/java/io/trino/server/rpm/ServerIT.java`, update
  the Temurin release name and expected Java major version in
  `testInstallUninstall` to match upstream. These are the arguments in the
  `testInstall` and `testUninstall` calls, for example `jdk-25.0.3+9`,
  `/usr/lib/jvm/temurin-25`, and `25`.
* Change `trino-server-rpm/src/main/resources/dist/config/jvm.config` only when
  the upstream bundled `jvm.config` changed for this version.
* Leave `trino-server-rpm/src/main/resources/dist/config/log.properties` as is
  normally. It keeps the `io.trino.server.Server=INFO` override.
* In `trino-server-rpm/README.md`, update the version and Java references.
* Check the direct `docker-java-api` and `testcontainers` test dependencies
  against the `docker-java-bom` and `testcontainers-bom` versions in the
  upstream Trino root pom. Update both together when upstream changes them.
  These direct dependencies override the versions brought in by
  `trino-testing-containers`. A stale pair can prevent `ServerIT` from
  connecting to newer Docker daemons. Confirm the resolved versions with:

  ```bash
  ./mvnw dependency:tree -pl trino-server-rpm \
    -Dincludes=org.testcontainers,com.github.docker-java -Dverbose
  ```

## Step 4 — root pom and top-level README

* In the root `pom.xml`, bump the `io.airlift:airbase` parent version when
  Step 1 found a change.
* In the top-level `README.md`, add the new version to the top of the
  **Supported Trino versions** list, with a link to the matching release tag at
  `https://github.com/trinodb/trino-packages/releases/tag/<VERSION>`. Keep the
  existing older entries.

## Step 5 — custom Docker image in `custom-docker/`

* In `custom-docker/build.sh`, bump the default `TRINO_VERSION=` value and the
  `-r` help-text default.
* In `custom-docker/Dockerfile`, bump the placeholder `ARG TRINO_VERSION=`.
* In `custom-docker/README.md`, update the version references: the
  configured-version line, the `docker images` example tags, and the
  `docker run` tag.
* Confirm the `trinodb/trino-core:<VERSION>` base image has been published for
  the target version and the architectures you build before relying on the
  build.

## Step 6 — build and verify

Run these from the repo root unless noted.

* Run the full Maven build with the CI smoke tests, which include the tarball
  smoke test:

  ```bash
  ./mvnw clean verify -Pci
  ```

  A plain `./mvnw clean install` also works but skips the `ci`-profile smoke
  tests. The RPM `ServerIT` integration test requires Docker.

* Build the custom Docker image. A single architecture is enough to verify, and
  CI restricts this to amd64 to avoid QEMU emulation:

  ```bash
  cd custom-docker && ./build.sh -a amd64
  ```

* When sortpom fails after an airbase bump, let `sortpom` re-sort the offending
  poms and commit the re-sort as part of the relevant module commit.
* When the build fails on a new checkstyle, airstyle, or verifier rule from the
  airbase bump, fix it minimally to satisfy the rule. The 481 bump needed this
  for the `PathInfo` record formatting.

## Step 7 — commit and PR

Use **one commit per concern**, in this order, each with an imperative subject
and a body that explains what changed and why. Follow whatever commit
conventions the target repository already uses:

1. `Upgrade tarball to Trino <VERSION>`
2. `Upgrade custom Docker image to Trino <VERSION>`
3. `Upgrade RPM to Trino <VERSION>`
4. `Document supported Trino versions in top-level README`, when kept separate

The root pom airbase bump goes with whichever module commit first needs it. The
tarball commit did this in 481. Note in a commit body when a module is
intentionally left on the old version to be updated in a later commit.

Open a pull request against the upstream default branch once the build passes.
Use the pull request template from the target `trino-packages` repository for
the PR body.

## Gotchas from the 481 update

* The `trino-server-core` `<dependency>` was removed from
  `trino-server-custom/pom.xml`. The artifact is now resolved **only** through
  provisio after prefetch, so do not re-add it.
* `prefetch.sh` forces HTTP/1.1 and retries aggressively because GitHub release
  assets intermittently fail over HTTP/2. Leave those curl flags in place.
* Startup takes a few minutes. Readiness is confirmed by the
  `======== SERVER STARTED ========` banner, which appears in
  `var/log/server.log` for the custom tarball and in `/var/log/trino/server.log`
  for the RPM.
* `custom-docker` is **not** a Maven module. It is absent from the root pom
  `<modules>` list and is built separately through `build.sh` and its own CI
  job.
