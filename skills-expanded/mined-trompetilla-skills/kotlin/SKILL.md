---
name: Kotlin
description: Build robust Android and multiplatform apps with Kotlin idioms, coroutines, and null safety.
metadata: {"clawdbot":{"emoji":"🟠","requires":{"bins":["kotlin"]},"os":["linux","darwin","win32"]}}
---

# Kotlin Development Rules

## Null Safety
- `?.` safe call chains — `user?.address?.city` returns null if any is null
- `?:` Elvis for defaults — `name ?: "Unknown"` is cleaner than if-else
- `!!` asserts non-null — crashes on null, use only when you've already checked
- `let` for null-scoped operations — `user?.let { doSomething(it) }` only runs if non-null
- Platform types from Java are risky — add null checks or use `@Nullable`/`@NonNull` annotations

## Coroutines
- `suspend` functions only callable from coroutines — don't block, use `withContext(Dispatchers.IO)` for IO
- `launch` for fire-and-forget — `async/await` when you need the result
- `viewModelScope` auto-cancels on ViewModel clear — don't use `GlobalScope` in Android
- `flow` for reactive streams — collect in lifecycle-aware scope with `repeatOnLifecycle`
- Structured concurrency: child coroutine failure cancels parent — use `supervisorScope` to isolate failures

## Collections
- `listOf` is immutable — use `mutableListOf` if you need to modify
- `map`, `filter`, `reduce` are lazy on Sequences — use `.asSequence()` for large chains
- `first()` throws on empty — use `firstOrNull()` for safe access
- `associate` and `groupBy` replace manual map building — cleaner than forEach with mutableMap
- Destructuring: `for ((key, value) in map)` — also works with data classes

## Data Classes
- `data class` auto-generates `equals`, `hashCode`, `copy`, `toString` — don't write manually
- Only constructor properties in `equals`/`hashCode` — body properties ignored
- `copy()` for immutable updates — `user.copy(name = "New")` keeps other fields
- Prefer data classes for DTOs and state — but not for entities with identity beyond data

## Scope Functions
- `let` for null checks and transformations — `value?.let { use(it) }`
- `apply` for object configuration — `MyObject().apply { prop = value }` returns object
- `run` for scoped computation — `val result = obj.run { compute() }` returns result
- `also` for side effects — `value.also { log(it) }` returns original
- Don't nest scope functions — readability drops fast, extract to named functions

## Extension Functions
- Extend existing classes without inheritance — `fun String.isEmail(): Boolean`
- Keep extensions close to usage — don't scatter across codebase
- Extension on nullable: `fun String?.orEmpty()` — can be called on null
- Extensions are resolved statically — not polymorphic, receiver type matters at compile time

## Sealed Classes
- Exhaustive `when` — compiler ensures all subclasses handled
- Perfect for state machines and results — `sealed class Result<T> { Success, Error }`
- Subclasses must be in same file (or same package in Kotlin 1.5+) — intentional restriction
- `sealed interface` for multiple inheritance — when you need to implement other interfaces

## Common Mistakes
- `==` is structural equality in Kotlin — `===` for reference, opposite of Java
- String templates: `"$var"` or `"${expr}"` — no concatenation needed
- `lateinit` can't be primitive — use `by lazy` for computed initialization
- `object` is singleton — `companion object` for static-like members, not instance
- SAM conversion only for Java interfaces — Kotlin interfaces need explicit `fun interface`

## Interop with Java
- `@JvmStatic` for companion methods callable as static — without it, need `Companion.method()`
- `@JvmOverloads` generates overloads for default params — Java doesn't see defaults otherwise
- `@JvmField` exposes property as field — without getter/setter for Java callers
- Nullability annotations propagate — annotate Java code for Kotlin safety
