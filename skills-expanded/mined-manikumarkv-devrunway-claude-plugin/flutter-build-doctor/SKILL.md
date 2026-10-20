---
name: flutter-build-doctor
description: Triage a failing Flutter build — Gradle, Xcode, CocoaPods, codegen, dependency resolution, R8 and CI-only failures. Reads pasted build output or runs the build itself, names the failure class before suggesting any command, and never opens with flutter clean. Usage — /flutter-build-doctor [pasted output]
argument-hint: "[paste build output | android | ios | ci | <path-to-log>]"
arguments:
  - name: input
    description: "Pasted build output, a path to a build log, or a target to build and read — android | ios | ci. Default: read the output supplied in the message; if there is none, ask which build to run."
user-invocable: true
context: fork
effort: medium
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(flutter *)
  - Bash(dart *)
  - Bash(fvm *)
  - Bash(pod *)
  - Bash(./gradlew *)
  - Bash(xcodebuild *)
  - Bash(xcrun *)
  - Bash(java -version)
  - Bash(sw_vers)
  - Bash(git clone *)
  - Bash(git status *)
  - Bash(git rev-parse *)
  - Bash(git remote *)
  - Bash(gh run *)
  - Bash(gh workflow *)
  - Bash(ls *)
  - Bash(cat *)
  - Bash(head *)
  - Bash(tail *)
  - Bash(sed *)
  - Bash(awk *)
  - Bash(grep *)
  - Bash(mktemp *)
  - Bash(diff *)
  - Bash(rm -rf ios/Pods)
  - Bash(rm -rf ios/Podfile.lock)
---

# Flutter Build Doctor

## Read the first error, not the last

**Gradle and Xcode both bury the cause above a long summary. The last forty lines are noise.**
`FAILURE: Build failed with an exception`, `Exception: Gradle task assembleDebug failed with exit code 1`,
`** BUILD FAILED **`, `The following build commands failed` — every one of those is a *report* that
something failed, printed after the fact. The line that says *what* failed is higher up, often by
hundreds of lines. Scroll up.

This one rule saves more time than everything below it. Apply it before anything else — including
before deciding which section of this file applies.

---

## Step 0 — Get the output

`$ARGUMENTS` is pasted build output, a path to a log file, or a target to build.

**Pasted output or a log path:** use it as-is. Do not re-run the build to "see it yourself" — the
paste is the evidence, and a re-run costs minutes.

**A target (`android`, `ios`, `ci`) or nothing:** capture a log and read it.

```bash
LOG="${TMPDIR:-/tmp}/flutter-build-$(date +%s).log"

# Android
flutter build apk --debug 2>&1 | tee "$LOG"
# iOS — no signing needed to reproduce a compile or pod failure
flutter build ios --debug --no-codesign 2>&1 | tee "$LOG"
# CI
gh run view --log-failed | tee "$LOG"
```

Run the **plain** build first. `--verbose` multiplies the output by ten and makes the first error
harder to find, not easier. Reach for it only when the plain output names no error at all.

---

## Step 1 — Find the first error

```bash
# Dart, Gradle and Xcode errors, earliest first
grep -nE "^e: |^\s*Error: |error: |FAILURE:|\* What went wrong|Could not |^\S+\.dart:[0-9]+:[0-9]+" "$LOG" | head -20
```

Take the **first** hit that carries a file path or a named cause, and quote it verbatim in the
report — the exact line, with its position in the log. If the earliest hits are all summary lines
(`FAILURE:`, `Exception: Gradle task …`), keep looking upward:

```bash
# Gradle: the real message sits under "What went wrong", and Flutter often swallows it
sed -n '/\* What went wrong/,/^\* Try:/p' "$LOG"
cd android && ./gradlew assembleDebug --stacktrace 2>&1 | head -80

# Xcode: the failing compile command precedes the "build commands failed" summary
grep -nE "error:|warning: .* was built for|ld: " "$LOG" | head -20
```

---

## Step 2 — Three questions that classify almost everything

Ask these before opening any catalogue. They narrow the search more than the error text does.

| Fails… | Assume until disproven | First check |
|---|---|---|
| **Only for you** — CI is green, a teammate builds fine | Stale cache or local toolchain drift | Fresh clone into a temp directory (ladder rung 7) |
| **Only in CI** — green on your machine | Toolchain version or a missing secret | Diff CI's Flutter / JDK / Xcode against yours |
| **Only in release** — debug builds and runs | R8, obfuscation, or a missing keep rule | Rebuild release with shrinking off |

```bash
# Only for you → answer it in three minutes, before debugging the workspace
TMP=$(mktemp -d) && git clone --depth 1 "$(git remote get-url origin)" "$TMP/repo"
# then, in "$TMP/repo": git checkout <same branch> && flutter pub get && flutter build apk --debug

# Only in CI → enumerate differences, do not debug
flutter --version && java -version && xcodebuild -version          # yours
gh run view --log | grep -iE "flutter [0-9]|dart [0-9]|openjdk|Xcode [0-9]"   # theirs

# Only in release → is it the shrinker?
flutter build apk --release --no-shrink
```

If the no-shrink build succeeds, the bug is a missing keep rule, not your Dart code. Stop reading
Dart.

---

## Step 3 — Classify before cleaning

**Never open with `flutter clean`.** A Dart compile error does not improve with it, a resolution
conflict does not improve with it, and reaching for it first destroys the evidence of *which* cache
was actually stale — so the failure returns next week with nothing learned. Classification is free.
Cleaning costs eight minutes and an explanation.

| The first error contains | Class | Where to go |
|---|---|---|
| A `.dart` path with a line and column | **Your code** | Fix the code. No cleaning, no ladder. |
| `build_runner`, `.g.dart`, `.freezed.dart`, "conflicting outputs" | **Codegen** | Ladder rung 2 only |
| `version solving failed`, `Because … depends on` | **Resolution** | Read the constraint chain — the message names both ends of it |
| `:app:`, `AAPT`, `D8`, `R8`, `Gradle`, `mergeDex` | **Android native** | Step 5 |
| `xcodebuild`, `CocoaPods`, `Podfile`, `ld:`, `Module 'X' not found` | **iOS native** | Step 6 |
| `provisioning profile`, `code signing`, `no identity found` | **Credentials, not code** | Step 6, then `/flutter-signing` |

Name the class in the report **before** proposing a single command. If the class is "your code",
this file is finished with you — go fix the line the compiler named.

---

## Step 4 — The cleaning ladder

Only for cache-class failures: codegen, stale native artefacts, "it works for everyone else".
**One rung at a time, with a rebuild between rungs.** Cheapest first. Stop at the rung that fixes
it and record which one it was — that *is* the diagnosis, and it names the cache to distrust next
time.

| # | Rung | What it disproves |
|---|---|---|
| 1 | `flutter clean && flutter pub get` | Dart/Flutter build cache and package resolution |
| 2 | `dart run build_runner build --delete-conflicting-outputs` | Stale or half-written generated files |
| 3 | `rm -rf ios/Pods ios/Podfile.lock && (cd ios && pod install --repo-update)` | Stale pod install and stale spec repo |
| 4 | Remove `~/Library/Developer/Xcode/DerivedData` | Xcode's module cache and stale build products |
| 5 | `(cd android && ./gradlew clean && ./gradlew assembleDebug --refresh-dependencies)` | Gradle build cache and cached dependency metadata |
| 6 | `flutter pub cache repair` | A corrupted package in the global pub cache |
| 7 | **Fresh clone into a temp directory** | Whether the *repo* or the *workspace* is broken |

**Rung 7 is the rung that answers the question, so suggest it before deep workspace debugging, not
after.** If the fresh clone builds, the repository is fine and the workspace is dirty: stop
debugging code and find what is in the tree but not in git — `git status --ignored`, a stray
`local.properties` pointing at an old SDK, a hand-edited `Podfile.lock`. If the fresh clone fails
the same way, the failure is committed, and rungs 1–6 were never going to help.

Rungs 3 and 4 are macOS/iOS only. Rung 5 costs several minutes and a full dependency re-download —
never run it speculatively.

---

## Step 5 — Android catalogue

| First error says | Cause | Fix |
|---|---|---|
| `Unsupported class file major version 65` | The JDK is newer than this Gradle understands (61 = JDK 17, 65 = 21, 67 = 23) | Compare `java -version` with `android/gradle/wrapper/gradle-wrapper.properties`. Either raise the wrapper or point the build at the supported JDK (`flutter config --jdk-dir=…`). Pin the choice where CI reads it too. |
| `Could not find method xyz()` in a `build.gradle` | AGP ↔ Gradle mismatch, or a DSL that moved between AGP majors | Match the AGP version to the Gradle wrapper version, then re-read the block. Rewriting the syntax until the error disappears, without fixing the version pair, only moves the failure. |
| `Duplicate class com.x.Y found in modules a.jar and b.jar` | Two transitive dependencies ship the same class | `./gradlew :app:dependencies --configuration releaseRuntimeClasspath` to find both paths, then constrain to one version or `exclude group:` on the narrower one — with a comment naming the two modules in conflict. |
| `uses-sdk:minSdkVersion N cannot be smaller than version M declared in library` | A plugin raised the floor | Raise `minSdk` to M deliberately, recording which plugin forced it and which devices were just dropped. **Never** `tools:overrideLibrary` — it compiles and then crashes on the devices you still claim to support. |
| `Manifest merger failed` | Two manifests set the same attribute | Read the merger report it points at, decide which value wins, add `tools:replace` **with a comment naming the other manifest**. |
| `mergeDexRelease` / `Cannot fit requested classes in a single dex file` | Method-count ceiling | Enable multidex, or cut dependencies. Prefer cutting — multidex hides the growth that caused it. |
| Debug builds fine; release fails or crashes at runtime | R8 stripped or renamed something reached reflectively | Confirm with `--no-shrink`, then add a keep rule for that one class or package — never `-keep class **`. Serialization models, `MethodChannel` handlers and reflective plugin entry points are the usual victims. |
| `File google-services.json is missing` | Per-flavor Firebase config absent for this flavor | Add `android/app/src/<flavor>/google-services.json`. A single shared file at `android/app/` builds happily and points every flavor at one project. |
| `NDK at … did not have a source.properties` / NDK version mismatch | Plugins requesting different NDK versions | Set one `ndkVersion` explicitly in `android/app/build.gradle` and let the plugins inherit it. |

---

## Step 6 — iOS catalogue

| First error says | Cause | Fix |
|---|---|---|
| `Module 'X' not found` | Pods not installed for this configuration, or the build opened `.xcodeproj` | `pod install`, and build the `.xcworkspace`. If the module is a Flutter plugin, check the flavor's build configuration appears in the Podfile's configuration map — a custom configuration name CocoaPods does not know about installs nothing for it. |
| `CocoaPods could not find compatible versions` / `Unable to find a specification` | Incompatible pod constraints, or a stale local spec repo | `pod install --repo-update` first — the stale repo is the common case. If it survives that, read the two constraints and resolve them explicitly. |
| `compiling for iOS X, but module was built for iOS Y` | Deployment target disagreement across the Podfile `platform`, the project's `IPHONEOS_DEPLOYMENT_TARGET`, and a plugin podspec | Set the Podfile platform and the `post_install` override loop to the same integer as the project. Three places, one value. |
| Simulator build fails on Apple Silicon | `EXCLUDED_ARCHS[sdk=iphonesimulator*] = arm64`, left over from an Intel-era workaround | Remove it. It excludes the architecture the machine actually runs. |
| `No profiles for 'com.x.y' were found` | Bundle-ID mismatch between project and profile | Compare `PRODUCT_BUNDLE_IDENTIFIER` per configuration against the profile. Each flavor suffix needs its own profile. |
| `Provisioning profile doesn't include the … entitlement` | The capability was enabled in Xcode but not on the App ID | Enable it on the identifier, regenerate the profile, re-download. |
| `errSecInternalComponent` / `User interaction is not allowed` in CI | The keychain is locked, or is not the default | Unlock it and set it as default in the job, before the archive step. |
| `Certificate has expired` / `no identity found` | Expired or missing certificate | Rotate it — `/flutter-signing`. Do not paper over it by switching a release job to automatic signing. |
| Archive succeeds, upload rejected (`ITMS-90xxx`) | Store validation, not the build | Read the ITMS code literally. Missing `NS*UsageDescription` keys, a non-public API symbol, and a missing arm64 slice are the frequent three. |
| `Module compiled with Swift X cannot be imported by Swift Y` | Swift ↔ Xcode mismatch between a binary pod and the local toolchain | Match the Xcode version to the one the pod ships for, or move to a pod build for yours. Pin Xcode so CI and local agree. |

Signing failures are **credentials, not code**: nothing in Dart or Gradle fixes them, and the work
belongs to the account and certificate workflow in `/flutter-signing`.

---

## Step 7 — CI-only is always a difference

If it builds locally and fails in CI, **something differs**. Enumerate the differences; do not
debug the code. The list is short, and one of these is nearly always it.

| Difference | How to confirm | Fix |
|---|---|---|
| Unpinned toolchain — Flutter, JDK, Xcode, CocoaPods | Print all four in both places and diff them | Pin each one where CI reads the same file you do |
| Missing or empty secret | Assert each generated env file exists and is non-empty **by name**, before the build step | `[ -s .env_<flavor> ] || { echo "missing .env_<flavor>"; exit 1; }` — so the failure names the secret instead of surfacing minutes later as a confusing generator error |
| Case-sensitive filesystem | `import 'widgets/MyButton.dart'` for a file named `my_button.dart` | Fix the import. macOS forgave it; Linux will not |
| Gitignored generated files not regenerated per job | The failing job has no codegen step | Run codegen in every job that compiles, then `git diff --exit-code` over the generated paths |
| Cold caches resolving differently | CI resolves fresh where you have a warm lockfile | Resolve with the committed lockfile honoured, and commit the lockfile |
| A moved `-latest` runner image | The failure began with no code change | Pin to a dated runner label; check the runner image changelog for the date it broke |

The last row is the tell: **a CI failure with no corresponding code change is an environment
change, almost always.** Find what moved before reading a line of Dart.

---

## Step 8 — Report

Produce this, in this order. The class comes before any command.

```
Failure class:  Android native — R8, release-only
Evidence:       build.log:412 — "Missing class com.example.PaymentRequest (referenced from …)"
Question:       Fails only in release; debug builds and runs.
Cause:          R8 strips PaymentRequest — it is reached only reflectively, from the JSON codec.
One change:     Keep rule for com.example.model.** in proguard-rules.pro, commented
                "kept: reflectively constructed by the payment JSON codec".
Verify:         flutter build apk --release, install, exercise the payment path.
Still open:     The kept list needs re-checking when the codec is replaced.
```

If **Cause** cannot be filled in, say so and stop. A proposal you cannot explain is not a fix.

---

## Close the loop

A local green is half the answer.

1. `flutter clean && flutter pub get`
2. Codegen — `dart run build_runner build --delete-conflicting-outputs`
3. Build **both** platforms in debug
4. Confirm CI is green on the pushed branch

Skipping step 4 is how a fix that works only on one machine reaches the branch everyone builds.

---

## Rules that do not bend

- **Never propose a fix you cannot explain.** A pin, an exclusion or a `tools:replace` without a
  comment naming the conflict it resolves becomes permanent mystery config that nobody dares
  remove.
- **Version overrides and dependency exclusions are last resorts and carry an expiry note.** They
  mask a conflict that resurfaces at the next upgrade; the note says what is masked and when to
  revisit it.
- **Change one thing per rebuild, and record it.** "I ran several things and it worked" means the
  cause is still in the repository and you can no longer name it.
- **A recurring failure becomes a CI check, not a wiki note.** The second occurrence of a build
  failure is a missing assertion.
- **Never open with `flutter clean`.** Classify first — always.

---

## Boundary

This command owns **triage**: reading a failure, naming its class, and reaching a cause you can
explain.

- **Build and CI configuration** — the two flavor switches, per-flavor native identity, pinned SDKs
  and explicit API levels, the PR gate, `analysis_options.yaml`, CI input assertions, versioning,
  obfuscation with symbol upload, pinned runners and secret handling — belongs to the
  `ci/flutter-release` layer. When triage ends in "the toolchain is unpinned" or "CI does not
  assert its inputs", state the finding and hand off; do not restate that configuration here.
- **Keystores, certificates, provisioning profiles and store accounts** are `/flutter-signing`.
- **What to test once it builds** is `/flutter-verify`.
