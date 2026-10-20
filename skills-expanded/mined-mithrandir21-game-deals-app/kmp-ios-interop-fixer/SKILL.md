---
name: kmp-ios-interop-fixer
description: Diagnose Swift/Kotlin interop issues in KMP — name mangling, sealed class bridging, suspend/Flow exposure, generics erasure, default arguments, `@HiddenFromObjC`, and Objective-C header readability. Use whenever the user mentions "Swift can't see my Kotlin API", "interop", "Objective-C header", "@HiddenFromObjC", "the iOS team is frustrated", "function name mangled", "weird Swift API", or "how do I expose this to iOS". Also use for SKIE configuration questions.
---

# KMP iOS Interop Fixer

The Kotlin → Swift interop layer is generated. When the result is ugly, the fix is usually upstream — in the Kotlin API shape — not on the Swift side. This skill diagnoses the most common interop problems and applies the standard fix.

## When to use

Triggers: "Swift can't see this", "weird name in Swift", "method renamed in interop", "mangled", "interop", "Objective-C header", "@HiddenFromObjC", "expose to iOS", "SKIE", "KMP-NativeCoroutines", "Swift completion handler".

For "I'm setting up a shared module" use `kmp-shared-module-architect`. This skill is for fixing specific interop problems on an existing module.

## Process

### Phase 1: Look at what Swift actually sees

Before guessing, read the generated header.

```
./gradlew :shared:linkDebugFrameworkIosSimulatorArm64
```

The framework is at `:shared/build/bin/iosSimulatorArm64/debugFramework/Shared.framework/`. Open `Headers/Shared.h` — that's the ObjC header Swift consumes.

Look for the Kotlin class in question. Common ugly outcomes:

- Method renamed (`fetchUserWithCompletionHandler:` instead of `fetchUser`).
- Class with a long prefix (`SharedFooBar` instead of `FooBar`).
- Sealed class subclasses as plain classes, not enum cases.
- Type-erased generics (`KotlinArray` instead of `[Foo]`).
- Functions that don't appear at all.

### Phase 2: Match the symptom

**Method overloads collapse / get renamed**

Kotlin allows overloads; ObjC doesn't. When two Kotlin methods would have the same ObjC name, they get suffixes.

```kotlin
fun process(input: String): Result
fun process(input: Int): Result
// In Swift: process(input: String) vs. process(input: Int32) — usually fine,
// but adding a third overload breaks things.
```

Fix: rename one to be Swift-friendly (`processText`, `processNumber`), or use `@ObjCName("processText")` on the Kotlin side.

**Default arguments missing**

Kotlin defaults don't bridge. Swift sees all parameters as required.

```kotlin
fun greet(name: String, greeting: String = "Hello"): String
// Swift sees: greet(name:greeting:) — must pass both.
```

Fix:
- Add `@JvmOverloads`-style overloads manually:
  ```kotlin
  fun greet(name: String) = greet(name, "Hello")
  fun greet(name: String, greeting: String): String
  ```
- Or use SKIE, which preserves default arguments in Swift.

**Sealed classes look wrong**

By default, a Kotlin sealed class becomes an ObjC base class with subclasses. Swift sees them as classes you'd check with `is` and downcast. Not idiomatic.

Fix:
- With SKIE: sealed classes become Swift enums automatically.
- Without SKIE: live with it, or expose a different surface (a function that returns separate optional fields).

**`Flow` / `StateFlow` doesn't appear in Swift in a usable form**

Raw KMP exposes `Flow` as a Kotlin class that you can collect via callback. No `async`/`await`, no `AsyncSequence`.

Fix:
- SKIE: `Flow` becomes `AsyncSequence`. `StateFlow` exposes `.value` plus a sequence.
- KMP-NativeCoroutines: annotate `@NativeCoroutines` on declarations; gets Swift extensions with `AsyncSequence`.
- Manual: write a wrapper that takes a closure and returns a cancellation token. Tedious but no dependency.

**`suspend` functions force completion handlers**

Default interop turns `suspend fun fetch(): Foo` into a Swift method with a completion handler, not a Swift `async` function.

Fix:
- SKIE: makes them Swift `async`.
- KMP-NativeCoroutines: same.
- Without either: Swift writes its own `withCheckedContinuation` wrapper.

**Functions disappear from the header**

Reasons:
- Top-level functions in a file are visible via `<FileName>Kt.method`. Sometimes that's not what you want.
- `internal` Kotlin code isn't exposed.
- `@HiddenFromObjC` is applied (intentionally or by SKIE for things it can't bridge).

Fix:
- Put top-level functions inside an `object` if you want them grouped:
  ```kotlin
  object UserApi {
      fun fetch(): Foo
  }
  // Swift: UserApi().fetch() — still ugly. Use companion or class.
  ```
- Make sure the visibility is `public` and not `internal`.
- Check whether SKIE auto-hid it because of an unsupported feature; the SKIE report (`build/skie/`) lists what was hidden.

**Generic parameters look like `Any` in Swift**

ObjC has limited generics. `List<Foo>` becomes `NSArray`; type info is lost at the boundary.

Fix:
- Use concrete collection types in the public API where possible.
- Or wrap collection-returning APIs in typed wrappers: `class FooList(val items: List<Foo>)`.
- SKIE preserves some generics better than raw interop.

**Long class names with prefixes**

```
SharedFooManager  // Kotlin: FooManager
```

The framework's `baseName` becomes the prefix. Swift can usually drop it via `typealias` or by accessing through the module name.

Fix:
- In Swift, use `import Shared; FooManager()` — module name handles it.
- Or set `binaries.framework { baseName = "App" }` to something short.

**`Result<T>` doesn't bridge**

Kotlin's `Result` is `@JvmInline`-style and doesn't translate cleanly.

Fix: define your own sealed outcome type.
```kotlin
sealed interface Outcome<out T> {
    data class Success<T>(val value: T) : Outcome<T>
    data class Failure(val error: Throwable) : Outcome<Nothing>
}
```

With SKIE, this becomes a Swift enum.

**Throwing functions**

Kotlin functions that throw need `@Throws(...)` to be visible to Swift as throwing functions:

```kotlin
@Throws(MyException::class)
fun parse(input: String): Result
```

Without `@Throws`, the exception crashes the iOS app instead of being thrown to Swift.

### Phase 3: Apply the fix

Pick the smallest change that improves the experience:

1. **Adopt SKIE first.** It fixes most categories above automatically.
2. **Rename / overload** when SKIE doesn't apply.
3. **Reshape the API** if a Kotlin idiom (e.g. `Flow<Result<T>>`) is fighting interop. Sometimes a thin wrapper is the right answer.
4. **Hide from Swift** with `@HiddenFromObjC` for Kotlin-internal helpers that don't need to be public to iOS.

### Phase 4: Verify

- Regenerate the framework and re-read the header.
- Have iOS open the call site and confirm autocomplete shows the expected API.
- Run an iOS test that exercises the API and confirms it behaves.

### Phase 5: Add guardrails

To catch future regressions:

- An iOS test target that calls every public entry point of the shared module. Compilation failure = interop regression.
- Treat changes to the shared module's public API like a published library — version it, document changes.
- SKIE has a "validation" report you can fail the build on if any types get hidden unexpectedly.

## Output

For each interop issue:

1. **Symptom** — what Swift sees / can't do.
2. **Cause** — which interop limitation.
3. **Fix** — Kotlin change, SKIE config, or workaround.
4. **Verified** — header check + iOS call site works.

## Common pitfalls

- **Fixing it on the Swift side.** Writing wrapper extensions in Swift to hide ugly Kotlin APIs is sometimes pragmatic, but it hides the cost from the Kotlin side. Push fixes upstream.
- **Adding `@ObjCName` everywhere.** Renames pile up; better to design the Kotlin API to be naturally interop-friendly.
- **Ignoring SKIE's "hidden" report.** SKIE silently hides things it can't bridge. Without checking the report, you don't know what's gone.
- **Exposing internal types.** Anything you can `import Shared.X` from Swift, you have to maintain. Limit the surface area aggressively.
- **Using `Throwable` instead of typed exceptions with `@Throws`.** Causes crashes that look like iOS bugs but are really uncaught Kotlin exceptions.
