---
name: memory-leak-hunter
description: Triage Android memory leaks from LeakCanary reports and heap dumps — lifecycle-bound listeners, static holders, retained Compose state, Bitmap leaks, coroutine scope leaks, and KMP shared-state holds. Use whenever the user mentions LeakCanary output, "leaked Activity", "leaked Fragment", "OOM", "heap dump", `.hprof`, or memory growth over time. Also use when reviewing code that registers listeners, observers, or callbacks across lifecycle boundaries.
---

# Memory Leak Hunter

Most Android leaks are one of five shapes. This skill helps you identify the shape from the evidence, then apply the standard fix for it.

## When to use

Triggers: "LeakCanary", "memory leak", "leaked Activity/Fragment", "OOM", "heap dump", `.hprof`, "memory keeps growing", "retained" callouts in profiler.

For OutOfMemoryError specifically from huge bitmaps (one image too big), the root cause is image sizing, not a leak — handle separately.

## Process

### Phase 1: Read the leak trace

LeakCanary gives you a chain like:

```
GC Root: System class
↓ static SomeManager.instance
↓ SomeManager.listener
↓ MyFragment.this$0
↓ MyFragment (leaking)
```

The leak source is at the top (the GC root); the victim is at the bottom. Read the chain from the root down — the **first reference you can break** is where you fix it.

If the dev only has a `.hprof`, open in Android Studio's Memory Profiler or `mat`. Look for instances of `Activity` / `Fragment` / `ViewModel` that have a count > 0 when they should be gone, and inspect their references.

### Phase 2: Match the leak shape

| Shape | Telltale | Fix |
|---|---|---|
| **Listener never unregistered** | A long-lived object (Manager, singleton, system service) holds a callback that captures a View/Activity/Fragment. | Unregister in `onStop`/`onDestroyView`. For Compose, use `DisposableEffect`. |
| **Static reference to context** | `static` field, `companion object`, or `object` holding `Context` / `View` / `Activity`. | Don't store `Context` statically. If you must cache something, store `applicationContext` only. |
| **Inner class capturing outer** | Non-static inner class, anonymous class, or lambda capturing `this` Activity, held by something long-lived. | Use a static (top-level or `companion`) class, or a `WeakReference` to the outer. |
| **Handler / Runnable still queued** | `Handler.postDelayed` with a Runnable that captures the Fragment. | Cancel pending posts in `onDestroyView`. Prefer `lifecycleScope.launch { delay(...) }`. |
| **Coroutine outliving scope** | `GlobalScope`, a custom `CoroutineScope` that's never cancelled, or `viewModelScope` referencing a view. | Use `viewModelScope` / `lifecycleScope`. Never reference Views from a coroutine inside a ViewModel. |
| **Compose `remember` leaking** | `remember { SomeObject(activity) }` where the object outlives the composition. | Hoist the object higher (ViewModel), or use `DisposableEffect` to release it on disposal. |
| **Drawable callback** | `View.setBackground(drawable)` where the drawable was created in a longer-lived scope. | Call `drawable.callback = null` or recreate per use. |
| **`Bitmap` not recycled / cached forever** | A Bitmap cache without size bounds. | Use `LruCache` with a size cap, or use an image loader. |

### Phase 3: Verify it's actually leaking

Some "leaks" aren't:

- **Retained Fragments / ViewModel scoped to NavGraph** survive configuration changes intentionally. LeakCanary doesn't usually flag these but heap dumps can be misleading.
- **Singletons holding `applicationContext`** are fine.
- **The Activity hasn't been GC'd yet** — force a GC in Profiler before concluding it's leaked.

If unsure, reproduce, rotate the device or pop the back stack, force a GC, then check if the instance is still alive. If it is, it's a leak.

### Phase 4: Fix and add a guardrail

Apply the fix from Phase 2, then add something that catches the regression:

- Keep LeakCanary in debug builds. It pays for itself.
- For critical screens, add an instrumented test that opens and closes the screen 50 times and asserts heap stays bounded (rough but effective).
- Code review: register/unregister calls should be paired in the same file, ideally adjacent.

## KMP note

In a KMP shared module, leaks usually come from:

- A `SharedFlow` or `MutableStateFlow` held by an `object` (singleton), accumulating subscribers from Android side because the cancellation never propagates from `lifecycleScope`.
- iOS retain cycles when a Swift class captures a Kotlin `Closeable` and forgets to close it. Audit interop with SKIE / KMP-NativeCoroutines patterns.

## Output

For each leak:

1. **Chain** — what holds what.
2. **Shape** — which category from Phase 2.
3. **Fix** — the specific code change.
4. **Guardrail** — what stops it coming back.

## Common pitfalls

- **Adding `WeakReference` everywhere.** Often masks the real lifecycle bug instead of fixing it. Prefer correct lifecycle handling.
- **Calling `System.gc()` in production code.** Doesn't fix leaks; can mask them in testing.
- **Trusting LeakCanary's "Suspected leak" without reading the chain.** Sometimes the suspect is a known false positive; the actual leak is one ref up or down.
- **Fixing only the first leak in a chain.** Often there are several copies of the same pattern — search the codebase for the offending API.
