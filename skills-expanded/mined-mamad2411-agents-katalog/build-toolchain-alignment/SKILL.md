---
name: "build-toolchain-alignment"
description: "Technology-agnostic rule for aligning the build/runtime toolchain to the TSA-specified version before building: provision/select the matching JDK/Node/Python/Go/.NET, pin the compiler release, and treat version-matching as required (not a forbidden downgrade)."
version: 1
created: "2026-06-10T03:34:24+05:30"
updated: "2026-06-26"
---
## When to Use
Use before compiling, packaging, or running any generated project, in ANY language. Apply whenever a build fails with a toolchain/version error, or whenever the ambient runtime might differ from `tsa.technology.application.language_version`. This skill is stack-independent: resolve the language and version from the TSA, then make the build toolchain match it.

## Core principle (resolves the "never downgrade" trap)
"Never downgrade the language version" means **never go BELOW the version the TSA specifies**. It does NOT forbid aligning the *build runtime* to the TSA version. If the ambient runtime is newer than the TSA target (e.g. ambient JDK 25 but `language_version`=17), **selecting/provisioning the TSA-matching runtime is REQUIRED alignment, not a downgrade.** Running a build on a newer-major runtime with an older compiler/plugin is a defect to fix, not a constraint to preserve.

## Procedure
1. **Read the target version** from `tsa.technology.application.{language, language_version, framework_version, build_tool}`.
2. **Detect the ambient runtime** (`java -version`, `node -v`, `python --version`, `go version`, `dotnet --list-sdks`). Record major version.
3. **If ambient major ≠ target major, provision/select the matching runtime** using whatever is available in the environment, then point the build at it:
   - **JVM (Java/Kotlin):** install/select the target JDK via `sdkman` (`sdk install java 17...`), `apt`/`apk`, `asdf`, or an existing install under `/usr/lib/jvm`; export `JAVA_HOME` + prepend `$JAVA_HOME/bin` to `PATH`. Prefer the TSA major exactly (17), not "newest available".
     - **Alpine Linux (musl libc) — critical:** detect Alpine via `/etc/alpine-release` (or `ldd --version` reporting musl). On Alpine, install the JDK with the distro package manager: **`apk add openjdk17`** (musl-native; `JAVA_HOME=/usr/lib/jvm/java-17-openjdk`). **Do NOT** download generic glibc JDK tarballs (Eclipse Temurin/Oracle/`sdkman` binaries) — they are glibc-linked and fail on musl with loader/`libc`/`Exec format` errors (a downloaded Temurin 17 will not run). Use `apk` (or a musl-specific build) only.
   - **Node:** `nvm install/use <major>` or `fnm`/`volta`.
   - **Python:** `pyenv install/local <version>` or the matching `pythonX.Y` interpreter + venv.
   - **Go:** install the `go<version>` toolchain or set `GOTOOLCHAIN`.
   - **.NET:** install the matching SDK; pin via `global.json`.
4. **Pin the compiler/target in the build file** so it cannot float:
   - Maven: `maven-compiler-plugin` with `<release>${java.version}</release>` (= TSA version), or a `maven-toolchains-plugin` `<jdk><version>17</version>`. If the ambient JDK is newer than the plugin supports, **bump `maven-compiler-plugin`** to a version that runs on it (rather than downgrading the JDK below target) — but prefer running the build on the TSA-matching JDK.
   - Gradle: `java { toolchain { languageVersion = JavaLanguageVersion.of(17) } }`.
   - Node/Python/Go/.NET: set `engines`/`requires-python`/`go` directive/`TargetFramework` to the TSA version.
   - **Annotation processors on a newer ambient JDK (e.g. ambient JDK 25, TSA target 17):** if you cannot provision the target JDK and must compile on the newer ambient JDK, pin `maven-compiler-plugin` `<release>` to the TSA version AND bump build-time annotation processors to versions that support the ambient JDK — use the **newest Lombok release that lists support for the *ambient* JDK** (Lombok 1.18.30 throws `java.lang.ExceptionInInitializerError: com.sun.tools.javac.code.TypeTag :: UNKNOWN` on JDK 21+; for **JDK 25 a 1.18.34 bump is NOT enough** — use the latest 1.18.x that documents JDK 25 support). Prefer provisioning the TSA-matching JDK (on Alpine: `apk add openjdk17`); the Lombok bump is the no-install fallback and may still fail if no Lombok build yet supports the ambient JDK — in that case provisioning the TSA JDK is the only path.
5. **Rebuild from the project root** and confirm exit 0. If a toolchain truly cannot be provisioned (no network, locked registry), return **STATUS=BLOCKED** naming the exact missing toolchain — never silently build on the wrong major version.

## Patterns
- `JAVA_HOME` pinned to the TSA major; `$JAVA_HOME/bin` first on `PATH`
- Maven/Gradle toolchains or explicit `release`/`sourceCompatibility`
- `global.json` / `.nvmrc` / `.python-version` / `go` directive matching the TSA
- Provision-then-verify: re-run `--version` after selecting the runtime

## Anti-Patterns
- Building on the ambient runtime when its major ≠ the TSA target
- Treating "select JDK 17 (TSA) while ambient is 25" as a forbidden downgrade
- Rewriting source to dodge a toolchain mismatch instead of fixing the toolchain
- Letting compiler `release`/source float to the ambient runtime
- Bumping the source language version above the TSA target to satisfy a newer runtime
- Leaving an outdated annotation processor (e.g. Lombok 1.18.30) when building on a newer ambient JDK — it crashes the compiler (`TypeTag :: UNKNOWN`); bump it to a build that supports the ambient JDK, or build on the TSA JDK
- On **Alpine/musl**, downloading a glibc JDK tarball (Temurin/Oracle/sdkman) — it won't execute (musl ≠ glibc); use `apk add openjdk17` instead

## Tool Selection
- JVM: sdkman / apt / asdf / maven-toolchains-plugin / Gradle toolchains
- Node: nvm / fnm / volta
- Python: pyenv / venv
- Go: GOTOOLCHAIN / go install
- .NET: dotnet-install / global.json

## Validation Rules
- Active runtime major == `tsa.technology.application.language_version` before the final build
- Compiler `release`/target == TSA version (not the ambient version)
- Build returns exit 0 on the TSA-matching runtime, or BLOCKED with the exact missing toolchain
- No source-level feature exceeds the TSA `language_version`

## RAG Sources
- spring-boot-docs
