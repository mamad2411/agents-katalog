# bkmr IntelliJ plugin

IntelliJ Platform plugin (Kotlin) that connects IDEs to the `bkmr lsp` language server and adds an
"Insert Filepath Comment" action. Supports IDE builds 2026.1.4 (261.26222) through 2026.2.x.

For dependency, IDE-range or toolchain upgrades, use the `upgrade-plugin` skill (`.claude/skills/upgrade-plugin`).

## Commands

```bash
make lint       # ktlint (engine pinned in build.gradle.kts)
make test       # unit tests: ./gradlew unitTest (plain JUnit, no IDE)
make check      # lint + compile + test + build: what CI's build job runs
make verify     # verifyPluginStructure + Plugin Verifier: downloads IDEs, slow
```

## Rules

- **`VERSION` is the single source of truth** for the version. Don't bump it in a PR: the maintainer
  releases with `make bump-patch|minor|major` locally, which bumps, tags, pushes and creates the
  GitHub release. Put changes under `## [Unreleased]` in `CHANGELOG.md`; the bump turns that heading
  into `## [<version>] - <date>` (configured in `.bumpversion.toml`). Never add version headings by hand.
- **`CHANGELOG.md` is the only place to write release notes.** The plugin's change notes are rendered
  from it at build time (Gradle Changelog Plugin, `changeNotes` in `build.gradle.kts`), and
  `make create-release` uses the version's section as the GitHub release notes.
- **`plugin.xml` must keep `<depends>com.intellij.modules.platform</depends>` and
  `<depends>com.intellij.modules.lsp</depends>`.** Without any `<depends>`, Marketplace rejects the
  plugin or treats it as IntelliJ IDEA-only. Never depend on `com.intellij.modules.ultimate`: the LSP API
  is available without a subscription.
- **Compile against the `sinceBuild` floor**, not the newest IDE: compiling against a newer platform
  can emit stubs for interface methods the floor lacks (`NoSuchMethodError` at runtime there).
- **`kotlin.stdlib.default.dependency = false`** (the IDE provides the stdlib at runtime), so unit tests
  need `testRuntimeOnly(kotlin("stdlib"))`. Don't remove it.
- Java 21 toolchain (`jvmToolchain(21)`); the Makefile pins `JAVA_HOME` to JDK 21.

## Claude Code on the web

- The SessionStart hook (`.claude/hooks/session-start.sh`) installs JDK 21.
- Sessions can push branches, open and merge PRs, but **cannot push tags or create releases** (HTTP 403).
  Releasing is done by the maintainer locally.
- Downloaded IDEs (~1.5 GB zipped, ~4 GB unpacked each) live in `~/.gradle/caches`. Changing the
  build's Gradle plugins unpacks every IDE again next to the old copies. On "No space left on device":
  `./gradlew --stop`, delete `~/.gradle/caches/<gradle-version>/transforms` and `build/` (recreated on
  demand), and IDE versions no longer referenced in `build.gradle.kts` from
  `~/.gradle/caches/modules-2/files-2.1/com.jetbrains.intellij.*`.
- Plugin Verifier IDE downloads sometimes fail with HTTP 429: wait a minute and retry.
- Run Gradle with `--max-workers=1` to keep memory use low.
