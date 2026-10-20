---
name: android-bug-hunting-lifecycle-leak-hunter
description: >
  Hunt for memory leaks and lifecycle violations in Android code: Activity/Fragment/View/Context
  references held past their lifecycle, ViewBinding accessed after onDestroyView, listeners
  registered without symmetric unregister (LocationManager, BroadcastReceiver, sensors,
  EventBus, callbacks), inner classes with implicit outer references, Handler.postDelayed
  outliving its owner, LiveData observed with the wrong LifecycleOwner in Fragments,
  RxJava Disposables not disposed, and singletons holding non-Application Context. Use
  this skill whenever the user asks to find memory leaks, leak audits, lifecycle bugs,
  retained-instance issues, "why is my app using more memory after rotation", or any phrasing
  that asks for memory or lifecycle defects in Android. Trigger whenever a bug hunt covers
  Activities, Fragments, Services, or Views.
---

# Lifecycle Leak Hunter

## Purpose

Memory leaks on Android almost always come from a small set of patterns: holding a reference
to something with a short lifecycle from something with a longer one. This skill looks for
the specific patterns that cause leaks, not for general "code smells."

**Output format.** Use the shared Bug Report Format. Read `.claude/skills/android-bug-hunting-dispatcher/references/report-format.md` before writing findings.

---

## Step 1 — Scope

```bash
# Identify Android components and view-handling code
grep -rEln "extends? (Activity|FragmentActivity|AppCompatActivity|Fragment|Service|\
ContentProvider|BroadcastReceiver)|: (Activity|FragmentActivity|AppCompatActivity|Fragment|\
Service|ContentProvider|BroadcastReceiver)\b" --include="*.kt" --include="*.java" .

# Singleton patterns
grep -rEln "object \w+|companion object" --include="*.kt" .

# Anything View-shaped
grep -rEln "ViewBinding|DataBinding|findViewById" --include="*.kt" --include="*.java" .
```

---

## Step 2 — Run each detector

---

### D1 — Static / `object` / `companion object` field holding `Context`, `Activity`, `View`, or `Fragment`

**Pattern.**

```bash
grep -rEn "^\s*(private |internal |public )?\s*(var|val)\s+\w+\s*:\s*\
(Context|Activity|FragmentActivity|AppCompatActivity|Fragment|View|TextView|Button|\
ImageView|RecyclerView)\b" --include="*.kt" .
```

For each hit, check whether it sits inside `object X { … }` or `companion object { … }`,
or is a `static` field in Java.

**Why it's a bug.** Singletons live for the whole process. Holding an `Activity` or `View`
reference there leaks the entire view hierarchy on every rotation. Holding a `Context` is
fine *only* if it's the application context — almost never enforced in code.

**Severity.** Critical when the field is an `Activity` or `View`. High for `Context` if
it might be non-application. Medium for `Fragment`.

**Recommended fix.** Either remove the singleton-state pattern, or store
`applicationContext` only. For UI references, scope to the lifecycle owner.

---

### D2 — Singleton accepting `Context` without `.applicationContext`

**Pattern.** `class Foo private constructor(context: Context) { … }` followed by usage
that does not call `.applicationContext` on the passed context.

```bash
grep -rEnB1 -A5 "fun getInstance\(.*Context|companion object.*Context" --include="*.kt" .
```

For each hit, look for `context.applicationContext` inside the singleton's storage logic.
If absent, flag it.

**Why it's a bug.** Activity passes `this` to `Foo.getInstance(this)` → singleton retains
Activity → rotation leaks Activity.

**Severity.** Critical.

**Recommended fix.**

```kotlin
class AnalyticsManager private constructor(context: Context) {
    private val appContext = context.applicationContext  // ← critical
    // …
}
```

---

### D3 — Fragment ViewBinding accessed after `onDestroyView`

**Pattern.** Fragment has a `_binding` and `binding` getter, but functions outside
`onCreateView`/`onViewCreated` access `binding!!` without checking `_binding == null`,
or there's no nulling-out in `onDestroyView`.

```bash
grep -rEn "private var _binding" --include="*.kt" .
```

For each fragment with `_binding`, verify:
1. `onDestroyView` sets `_binding = null`.
2. No coroutine collected on `lifecycleScope` (rather than `viewLifecycleOwner.lifecycleScope`)
   accesses `binding`.
3. No callback registered on a long-lived object accesses `binding`.

**Why it's a bug.** Fragment instances outlive their views (e.g. when on the back stack).
`binding` after `onDestroyView` references a destroyed view hierarchy.

**Severity.** Critical if accessed after view destruction (NPE or stale view update).

**Recommended fix.**

```kotlin
private var _binding: FooBinding? = null
private val binding get() = _binding!!

override fun onDestroyView() {
    super.onDestroyView()
    _binding = null
}
```

Also: collect Flows on `viewLifecycleOwner.lifecycleScope`, not `lifecycleScope`.

---

### D4 — `LiveData.observe(this, …)` inside a Fragment

**Pattern.**

```bash
grep -rEn "\.observe\s*\(\s*this\s*," --include="*.kt" --include="*.java" .
```

For each hit inside a Fragment, the first arg should be `viewLifecycleOwner`, not `this`.

**Why it's a bug.** Fragment outlives its view. Observing with `this` keeps re-running
the observer after `onDestroyView` and re-attaches a stale observer when the view is
recreated, causing duplicate updates.

**Severity.** High. Manifests as ghost UI updates and duplicate event handling.

**Recommended fix.** `viewModel.foo.observe(viewLifecycleOwner) { … }`.

---

### D5 — Listeners / receivers / sensors / callbacks registered without unregister

**Patterns and their pairs:**

| Register | Unregister |
|---|---|
| `LocationManager.requestLocationUpdates` | `removeUpdates` |
| `Context.registerReceiver` | `unregisterReceiver` |
| `SensorManager.registerListener` | `unregisterListener` |
| `addOnGlobalLayoutListener` | `removeOnGlobalLayoutListener` |
| `PhoneStateListener.LISTEN_*` | `LISTEN_NONE` |
| `addOnPropertyChangedCallback` | `removeOnPropertyChangedCallback` |
| `setOnApplyWindowInsetsListener` (custom owners) | symmetric remove |
| `viewTreeObserver.add*` | symmetric remove |
| `EventBus.register` | `EventBus.unregister` |
| `ContentResolver.registerContentObserver` | `unregisterContentObserver` |

**Search.**

```bash
grep -rEn "register(Receiver|Listener|ContentObserver|OnSharedPreferenceChangeListener)|\
addOn\w+Listener|requestLocationUpdates|EventBus\.getDefault\(\)\.register" \
  --include="*.kt" --include="*.java" .
```

For each register call, look in the same class for the symmetric unregister in
`onPause`/`onStop`/`onDestroy`/`onDestroyView` (whichever matches the registration
lifecycle).

**Why it's a bug.** The system holds the listener reference. The listener (often an inner
class or lambda) holds a reference to the Activity/Fragment/View. Result: leak that
persists for the lifetime of the system service.

**Severity.** Critical for system-service registrations (location, sensors, broadcasts).
High for view-tree observers and EventBus.

**Recommended fix.** Add the symmetric call in the matching teardown callback. Consider
DefaultLifecycleObserver or a `lifecycle.addObserver` wrapper that auto-unregisters.

---

### D6 — Inner / anonymous class with implicit outer reference held by long-lived object

**Pattern A — Handler in Activity/Fragment.**

```bash
grep -rEn "object\s*:\s*Handler\(|inner class \w+\s*:\s*Handler" --include="*.kt" .
grep -rEn "new\s+Handler\s*\(" --include="*.java" .
```

If the Handler instance is a non-static inner class, it holds the outer Activity. Posting
delayed messages then leaks the Activity until the messages are processed.

**Pattern B — `postDelayed` with long delay from a non-static inner Runnable.**

```bash
grep -rEn "postDelayed\s*\(" --include="*.kt" --include="*.java" .
```

For each, check the runnable: anonymous class? lambda capturing `this`? Long delay
(seconds, minutes)?

**Why it's a bug.** Pending messages keep the Handler alive; the Handler keeps the
Activity alive until the delay fires. With a 30s delay, every rotation leaks an Activity
for 30s.

**Severity.** High.

**Recommended fix.**

```kotlin
// Use a static inner class with WeakReference, or:
class MyFragment : Fragment() {
    private val handler = Handler(Looper.getMainLooper())
    private val task = Runnable { /* … */ }

    override fun onDestroyView() {
        handler.removeCallbacks(task)
        super.onDestroyView()
    }
}
```

---

### D7 — `lifecycleScope` used in a Fragment where `viewLifecycleOwner.lifecycleScope` was needed

**Pattern.**

```bash
grep -rEn "(?<!viewLifecycleOwner\.)lifecycleScope\.launch" --include="*.kt" .
```

(If your grep doesn't support look-behind, just grep `lifecycleScope.launch` and inspect
the surrounding context.)

For each hit in a Fragment, ask: does the launched coroutine touch `binding`, `view`,
`requireView()`, or anything view-derived?

**Why it's a bug.** `lifecycleScope` is the Fragment's own scope — it lives across
view destroy/recreate. View references inside it may dangle.

**Severity.** High when view-touching, otherwise Medium.

**Recommended fix.** `viewLifecycleOwner.lifecycleScope.launch { … }` for view-bound
work; `lifecycleScope` only for fragment-scoped work that survives view recreation.

---

### D8 — RxJava `Disposable` not added to a `CompositeDisposable`

**Pattern.** `subscribe(…)` whose return value is ignored, or `Disposable` stored in
a field but never `dispose()`d in the right teardown.

```bash
grep -rEn "\.subscribe\s*\(" --include="*.kt" --include="*.java" .
```

For each, check whether the return value is `add`'d to a `CompositeDisposable` or stored
and disposed.

**Why it's a bug.** Subscriptions leak the observer, which usually leaks the Activity.
Streams keep emitting (and updating dead UI).

**Severity.** Critical.

**Recommended fix.** Use a `CompositeDisposable` cleared in `onDestroy`/`onDestroyView`.
Consider `RxLifecycle` or migrate to coroutines.

---

### D9 — `bindService` without `unbindService`

**Pattern.**

```bash
grep -rEn "bindService\s*\(" --include="*.kt" --include="*.java" .
```

For each hit, search the same class for `unbindService`.

**Why it's a bug.** ServiceConnection leaks both the connection callback (which usually
references the binding context) and a binding count for the system. Repeated bind/no-unbind
cycles leak everything.

**Severity.** Critical.

**Recommended fix.** Symmetric `unbindService` in `onStop` (for STARTED-tied bindings)
or `onDestroy`.

---

### D10 — Cursor / Stream / Reader stored in a long-lived field

**Pattern.** A `Cursor`, `InputStream`, `OutputStream`, `Reader`, or `Writer` held as a
class property of an Activity/Fragment/Service/ViewModel.

```bash
grep -rEn "(var|val)\s+\w+\s*:\s*(Cursor|InputStream|OutputStream|Reader|Writer)" \
  --include="*.kt" .
```

**Why it's a bug.** These resources are precious; holding them as fields tends to leak
file descriptors and memory. Even when closed, the field reference may keep buffers alive.

**Severity.** High to Medium depending on usage.

**Recommended fix.** Open and close inside a `use { }` block at the call site. If you
truly need a long-lived stream, document it and ensure deterministic teardown.

(Note: this overlaps with `android-bug-hunting-resource-leaks`. Flag here when the *holder* is the lifecycle
violation; flag in `android-bug-hunting-resource-leaks` when the resource lifecycle itself is the issue.)

---

### D11 — `Activity.this` or implicit Activity reference passed to callbacks/threads

**Pattern.** Java `new Thread(new Runnable() { run() { … context … } }).start()` —
the anonymous class holds the outer Activity.

```bash
grep -rEn "new Thread\s*\(" --include="*.java" .
```

In Kotlin: `Thread { … context … }.start()` — same problem when started from an
Activity field initializer or `onCreate` and the thread runs longer than the Activity.

**Severity.** Critical when the thread is long-running.

**Recommended fix.** Use coroutines tied to a proper scope, or pass `applicationContext`
to a static helper.

---

### D12 — `WeakReference` misuse

**Pattern.** Code that creates a `WeakReference<T>` and then holds onto its referent
strongly anyway (assigning `weakRef.get()` to a long-lived field).

```bash
grep -rEn "WeakReference" --include="*.kt" --include="*.java" .
```

**Severity.** Medium. Often a sign that the author *thought* about leaks but didn't
finish the job.

**Recommended fix.** Either keep the strong reference and bind it to a lifecycle, or
re-fetch from the WeakReference at use site (and handle `null`).

---

### D13 — `ViewModel` holding `Context`, `Activity`, `View`, or `Fragment`

**Pattern.**

```bash
grep -rEnB1 -A2 "class \w+ViewModel\b" --include="*.kt" .
```

For each ViewModel class body, check fields for `Context`, `Activity`, `View`, `Fragment`.

**Why it's a bug.** ViewModels are deliberately retained across config changes. If the
ViewModel holds a Context other than `Application`, it leaks the Activity.

**Severity.** Critical for `Activity`/`View`. High for raw `Context`.

**Recommended fix.** If the VM truly needs a Context (rare), inject `Application` (via
`AndroidViewModel` or DI). Better: move Context-using logic out of the VM into a
repository or a domain helper that takes Context per call.

---

### D14 — Long-running operations in `onCreate` without scope binding

**Pattern.** Network/database calls in `onCreate`/`onStart` that schedule callbacks but
the callback holds Activity reference.

Inspect Activity/Fragment `onCreate` bodies for callback-style APIs (especially older
Java SDKs) that take a callback parameter without an unregister mechanism.

**Severity.** High when reachable.

**Recommended fix.** Move to ViewModel + coroutines/Flow with proper scope.

---

## Step 3 — Write the report

Write findings to `<workspace>/findings-lifecycle-leak-hunter.md` in shared Bug Report
Format. Group by detector ID for traceability.

---

## Notes

- LeakCanary catches many of these at runtime; this skill is the static-analysis
  complement that finds them before the build.
- Reading the *teardown* callback (`onDestroyView`, `onStop`, `onDestroy`) is often the
  fastest way to confirm a leak — every register/observe/post needs a partner there.
- ViewModel fields are a common false-positive source: many ViewModels legitimately hold
  `applicationContext`. Verify before flagging.
