---
name: android-bug-hunting-kmp-defects
description: >
  Hunt for runtime defects specific to Kotlin Multiplatform projects: expect declarations
  without actual implementations across all active source sets, Android/JVM types leaking
  into commonMain, java.* APIs used in commonMain, suspend functions in commonMain that
  block on Apple targets due to the K/N memory model, Date/time misuse (java.util.Date,
  java.time in common), singleton patterns that don't work cross-platform, coroutine
  context assumptions, frozen-state issues in legacy Kotlin/Native, expect/actual signature
  mismatches, and Swift-interop hazards (default arguments, sealed hierarchies, suspend
  shape). Use this skill whenever the user asks to find bugs in a KMP / Kotlin Multiplatform
  project, an iOS-side issue with shared code, "commonMain problems", or any phrasing
  asking for defects in a shared Kotlin module. Trigger whenever a bug hunt covers a
  project containing commonMain, expect/actual, or KMP-specific Gradle setup.
---

# KMP Defect Hunter

## Purpose

Kotlin Multiplatform has its own family of bugs that don't appear in Android-only code:
platform leakage into `commonMain`, `expect`/`actual` mismatches, K/N runtime quirks, and
Swift-interop hazards. The bugs are specific and pattern-matchable; this skill enumerates
them.

**Output format.** Use the shared Bug Report Format. Read `.claude/skills/android-bug-hunting-dispatcher/references/report-format.md` before writing findings.

---

## Step 1 — Scope and orientation

```bash
# Identify source sets
find . -type d -name "commonMain" -o -name "androidMain" -o -name "iosMain" \
  -o -name "iosArm64Main" -o -name "iosX64Main" -o -name "iosSimulatorArm64Main" \
  -o -name "appleMain" -o -name "jvmMain" -o -name "jsMain" -o -name "nativeMain" \
  -o -name "linuxX64Main" -o -name "mingwX64Main"

# Find expect/actual declarations
grep -rEn "^\s*(public |internal |private )?\s*expect\s+(class|fun|object|interface|val|var)" \
  --include="*.kt" .

grep -rEn "^\s*(public |internal |private )?\s*actual\s+(class|fun|object|interface|val|var)" \
  --include="*.kt" .
```

Build a map: which source sets exist, and which `expect` declarations live in `commonMain`?

---

## Step 2 — Run each detector

---

### D1 — `expect` declaration missing `actual` in some active target

**Pattern.** For every `expect` in `commonMain`, every active platform source set must
have a matching `actual`. Hierarchical KMP with intermediate source sets (e.g. `appleMain`
satisfying iOS targets) makes this trickier — a single `actual` in `appleMain` can cover
all Apple targets.

**Method.**

1. List all `expect` declarations and their FQ names from `commonMain`.
2. List all active leaf targets from `build.gradle.kts` (look for `androidTarget`, `iosArm64`,
   `iosSimulatorArm64`, `iosX64`, `jvm`, `js`, etc.).
3. For each target, walk its source-set chain (e.g. `iosArm64Main` ← `iosMain` ← `appleMain`
   ← `nativeMain` ← `commonMain`) and check whether *some* level declares each `actual`.
4. Flag missing `actual`s.

This may not always be tractable from grep alone. If the project compiles, the compiler
already verifies this — flag only the specific cases the inspection surfaces, e.g.
intermediate source sets where `actual` placement is questionable.

**Severity.** Critical (compile failure when missing). Lower confidence here, since the
build will catch it; flag suspicious *placements* (e.g. `actual` in `iosArm64Main` only,
forcing duplication for `iosSimulatorArm64Main`).

**Recommended fix.** Move `actual` to the highest common ancestor source set that still
makes sense (e.g. `iosMain` covering all iOS targets).

---

### D2 — Android / JVM types in `commonMain`

**Pattern.**

```bash
grep -rEn "^\s*import\s+(android\.|androidx\.|java\.|javax\.|kotlinx\.coroutines\.android)" \
  $(find . -path "*/commonMain/kotlin*" -type d) 2>/dev/null
```

Any hit is a bug — `commonMain` cannot reference platform-specific types.

**Why it's a bug.** Build failure on non-JVM targets. If the project currently compiles,
it's because the offending files are accidentally in a JVM-leaning source set instead of
`commonMain`.

**Severity.** Critical when truly in `commonMain`. Often actually a misfiled file —
verify the source set first.

**Recommended fix.** Move the file out of `commonMain`, or replace the platform type
with an `expect`/`actual` abstraction.

---

### D3 — `java.util.Date` / `java.time.*` usage in `commonMain`

**Pattern.**

```bash
grep -rEn "java\.util\.Date|java\.time\.|java\.text\.SimpleDateFormat" \
  $(find . -path "*/commonMain/kotlin*" -type d) 2>/dev/null
```

**Severity.** Critical (won't compile on K/N).

**Recommended fix.** Use `kotlinx-datetime` (`Instant`, `LocalDate`, `LocalDateTime`,
`TimeZone`). If shared types must cross to platform code that uses `java.time`, do the
conversion at the platform boundary.

---

### D4 — `runBlocking` in `commonMain` shared code targeting iOS

**Pattern.**

```bash
grep -rEn "runBlocking" $(find . -path "*/commonMain/kotlin*" -type d) 2>/dev/null
```

**Why it's a bug.** Although `runBlocking` exists on K/N, calling it on the iOS main
thread deadlocks (the main dispatcher is the same thread doing the blocking). For a
shared library consumed from Swift, this is reachable from the main thread by default.

**Severity.** Critical when reachable from iOS main thread.

**Recommended fix.** Don't expose blocking shapes from shared code. For Swift consumers,
expose suspend functions and bridge with `KMP-NativeCoroutines` or SKIE.

---

### D5 — Suspending functions in `commonMain` that block the underlying thread

**Pattern.** Inside a `suspend fun` in `commonMain`, calling something that blocks
without `withContext(Dispatchers.IO/Default)`. On JVM `Dispatchers.IO` exists; on K/N
it depends on the coroutines version (newer versions provide `Dispatchers.IO`).

```bash
grep -rEnA10 "suspend fun" $(find . -path "*/commonMain/kotlin*" -type d) 2>/dev/null
```

For each, look for blocking calls (file I/O, networking via blocking client, `Thread.sleep`).

**Severity.** High. On iOS, blocking in a coroutine can stall the main runloop.

**Recommended fix.** Use suspending I/O libraries (Ktor client) and explicit dispatcher
switches. Verify dispatcher behaviour on K/N for the target coroutines version.

---

### D6 — Singletons declared as `object` in `commonMain` with mutable state

**Pattern.**

```bash
grep -rEnA5 "^object \w+" $(find . -path "*/commonMain/kotlin*" -type d) 2>/dev/null \
  | grep -E "var |MutableState"
```

**Why it's a bug.** Pre-1.7.20 K/N had the strict memory model where mutable state in
shared singletons required freezing or `@ThreadLocal`. Newer K/N versions relax this,
but cross-thread access patterns can still surprise. On Android the same singleton has
no such constraint.

**Severity.** Medium to High depending on K/N version.

**Recommended fix.** For the new memory model (default since 1.7.20), confirm Kotlin
version ≥ 1.7.20 and that `kotlin.native.binary.memoryModel=experimental` is *not*
needed. For older code, prefer immutable state or use `AtomicReference`.

---

### D7 — Coroutine `Dispatchers.Main` access from `commonMain` without target-specific
guard

**Pattern.**

```bash
grep -rEn "Dispatchers\.Main" $(find . -path "*/commonMain/kotlin*" -type d) 2>/dev/null
```

**Why it's a bug.** `Dispatchers.Main` requires a platform-specific dispatcher to be
provided. On Android, `kotlinx-coroutines-android` supplies it; on iOS, it's provided
by `kotlinx-coroutines-core` for K/N (since 1.6); on plain JVM, you need
`kotlinx-coroutines-swing` or similar. Missing artifacts produce `IllegalStateException`
at runtime — not at compile time.

**Severity.** High when reachable.

**Recommended fix.** Verify each target has the required Main dispatcher artifact in
the right source set. Document the requirement in shared module README.

---

### D8 — `expect`/`actual` signature mismatch tolerated by the compiler but semantically off

**Pattern.** Default-argument values declared on `actual` (illegal — must be on `expect`);
or `actual` widening visibility; or `actual` typealias to a Java type that doesn't honor
the contract `commonMain` expects (e.g. nullability differences).

This requires inspection rather than grep. Walk through each `expect`/`actual` pair and
look for:
- Default values on the `actual` side.
- `actual typealias Foo = SomePlatformType` where `SomePlatformType` has different
  nullability or method semantics than `expect Foo` implies.

**Severity.** Medium. Often subtle, surfaces as platform-specific runtime bugs.

---

### D9 — Swift-interop pitfalls in `iosMain` / `commonMain` exposed APIs

**Patterns:**

1. **`sealed class`/`sealed interface`** — pre-SKIE, sealed hierarchies expose to Swift
   as a regular class hierarchy, losing exhaustiveness. With SKIE, this is converted.
2. **Default arguments** — Kotlin defaults disappear in Swift; callers must supply all
   arguments. Often surprises iOS developers.
3. **`suspend fun`** — exposed as completion-handler functions in Swift; cancellation
   is one-way; structured concurrency is lost without SKIE / KMP-NativeCoroutines.
4. **`Flow<T>`** — not directly consumable from Swift without a bridge.
5. **Top-level functions in non-`Companion` files** — exposed as functions on a generated
   `Kt` class with awkward names.

**Method.** For each public API in `commonMain` or `iosMain`, check whether the project
uses SKIE or KMP-NativeCoroutines. If not, flag the unbridged shapes.

**Severity.** Medium. Mostly a usability defect that compounds into bugs in Swift call
sites — wrong cancellation, missed events, exhaustiveness lost.

**Recommended fix.** Adopt SKIE (or KMP-NativeCoroutines) and verify the generated Swift
API surface.

---

### D10 — `kotlinx.serialization` types crossing the Swift boundary

**Pattern.** `@Serializable` data classes exposed to Swift. By default these include
synthetic companion objects and serializers that can confuse Swift consumers.

```bash
grep -rEn "@Serializable" $(find . -path "*/commonMain/kotlin*" -type d) 2>/dev/null
```

**Severity.** Low. Mostly a polish issue; flag if iOS team has reported confusion.

---

### D11 — Resource access using Android-specific APIs in shared code

**Pattern.** `R.string.*`, `Resources.getSystem()`, anything from
`android.content.res` referenced outside `androidMain`.

```bash
grep -rEn "\bR\.|Resources\.getSystem|android\.content\.res" \
  $(find . -path "*/commonMain/kotlin*" -path "*/iosMain/kotlin*" -type d) 2>/dev/null
```

**Severity.** Critical when in `commonMain`.

**Recommended fix.** Localize per platform or use a multiplatform i18n library
(`moko-resources`, `compose-multiplatform` resources).

---

### D12 — Logging in `commonMain` using Android `Log`

**Pattern.**

```bash
grep -rEn "android\.util\.Log|Log\.[diwev]" \
  $(find . -path "*/commonMain/kotlin*" -type d) 2>/dev/null
```

**Severity.** Critical when in `commonMain`.

**Recommended fix.** Use a multiplatform logger (`co.touchlab:kermit`, `Napier`).

---

### D13 — Fragile `actual typealias` to platform types without wrapping

**Pattern.**

```bash
grep -rEn "actual typealias" --include="*.kt" .
```

For each, check whether the platform type's API is broader than the `expect`'s contract
and whether the broader API is being used through the typealias from `commonMain`.

**Severity.** Medium. Surfaces as code in `commonMain` that uses members not declared
on the `expect`, breaking on a new target.

---

### D14 — Different cinterop behaviour assumed across Apple targets

**Pattern.** Code in `iosMain` (or `appleMain`) assuming behaviour that differs between
`iosArm64` (device), `iosSimulatorArm64` (M-series simulator), `iosX64` (Intel
simulator). Common offenders: pointer sizes, byte ordering, file path assumptions.

**Severity.** Medium. Flag when cinterop or `kotlinx.cinterop` is used in shared Apple
code.

---

### D15 — KMP Gradle configuration errors that bite at runtime

**Patterns from `build.gradle.kts`:**

- Missing `dependsOn` declarations linking intermediate source sets.
- Hierarchical defaults disabled where they should be on (or vice versa).
- `iosX64` target enabled on Apple-Silicon-only CI (now uncommon).
- XCFramework export missing required transitive frameworks.

```bash
grep -rEn "kotlin\s*\{|dependsOn|XCFramework|iosArm64\(|iosSimulatorArm64\(|iosX64\(" \
  --include="*.kts" --include="*.gradle" .
```

**Severity.** Medium (build/runtime issues at CI/dev boundary).

---

## Step 3 — Write the report

Write findings to `<workspace>/findings-kmp-defects.md` in shared Bug Report Format.
Group by detector ID; the dispatcher will renumber and sort.

---

## Notes

- KMP toolchain is moving fast. Always look at the project's Kotlin version and the
  coroutines version before applying old advice (the new memory model, `Dispatchers.IO`
  on K/N, etc., have all changed recently).
- Many bugs surface only on iOS — pair static findings with the request that the team
  run their tests on an actual iOS target.
- For projects using SKIE or KMP-NativeCoroutines, the Swift-interop section's severity
  drops considerably; verify presence before flagging.
