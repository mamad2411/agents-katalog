---
name: android-bug-hunting-main-thread-violations
description: >
  Hunt for main-thread (UI thread) violations in Android code: blocking I/O, network calls,
  Room DAO calls without suspend/Flow, file reads, SharedPreferences.commit(), heavy
  computation in composables or onCreate, synchronous database calls during startup,
  blocking Bitmap decodes, JSON parsing on Main, and other patterns that cause jank or ANR.
  Use this skill whenever the user asks to find ANR causes, jank, "main thread" issues,
  startup performance problems, frame drops, or wants an audit for blocking operations
  on the UI thread. Trigger whenever a bug hunt covers Android code that performs I/O
  or computation, even if not asked by name.
---

# Main-Thread Violation Hunter

## Purpose

ANRs and jank almost always trace to one cause: blocking work on the main thread. The
patterns are concrete and pattern-matchable. This skill enumerates them and looks for
each.

**Output format.** Use the shared Bug Report Format. Read `.claude/skills/android-bug-hunting-dispatcher/references/report-format.md` before writing findings.

---

## Step 1 — Scope

```bash
# Anything that smells like I/O or heavy work
grep -rEln "Room|@Dao|@Query|@Insert|@Update|@Delete|HttpURLConnection|FileInputStream|\
FileOutputStream|FileReader|FileWriter|BufferedReader|BufferedWriter|ObjectInputStream|\
SharedPreferences|BitmapFactory|JSONObject|JSONArray|Gson|Moshi|ContentResolver" \
  --include="*.kt" --include="*.java" .
```

---

## Step 2 — Run each detector

---

### D1 — Room DAO methods returning non-suspend, non-Flow types

**Pattern.**

```bash
grep -rEnB2 -A2 "@(Query|Insert|Update|Delete|Transaction)" --include="*.kt" .
```

For each annotated method, check the signature:
- `suspend fun` → fine.
- `fun foo(): Flow<…>` → fine.
- `fun foo(): LiveData<…>` → fine (Room handles dispatch).
- `fun foo(): T` (anything else, including `List<X>` or a single entity) → **bug**.

**Why it's a bug.** Room executes the query synchronously on the calling thread when
the method is non-suspend, non-Flow, non-LiveData. If called from Main, throws
`IllegalStateException` ("Cannot access database on the main thread")  *unless*
`allowMainThreadQueries()` was set on the database — in which case it just blocks
silently and ANRs.

**Severity.** Critical (crash or ANR).

**Recommended fix.** Make the DAO method `suspend` or return `Flow`.

```kotlin
// Before
@Query("SELECT * FROM user") fun getAll(): List<User>
// After
@Query("SELECT * FROM user") suspend fun getAll(): List<User>
// Or
@Query("SELECT * FROM user") fun getAll(): Flow<List<User>>
```

---

### D2 — `Database.allowMainThreadQueries()` enabled

**Pattern.**

```bash
grep -rEn "allowMainThreadQueries" --include="*.kt" --include="*.java" .
```

**Why it's a bug.** Disables Room's main-thread guard, allowing silent blocking.

**Severity.** High. Often the root cause behind a fleet of D1 violations not throwing.

**Recommended fix.** Remove the call. Fix the queries it was masking.

---

### D3 — `SharedPreferences.commit()` (vs `apply()`)

**Pattern.**

```bash
grep -rEn "\.commit\(\)" --include="*.kt" --include="*.java" .
```

For each hit, check if it's `SharedPreferences.Editor.commit()`.

**Why it's a bug.** `commit()` is synchronous and disk-bound — writes to flash before
returning. On the main thread this is variable cost (10–500ms+ depending on device and
flash state). `apply()` returns immediately and writes asynchronously.

**Severity.** Medium on Main; the rare cases where commit's return value is needed are
legitimate but should be moved off Main.

**Recommended fix.** `apply()` for fire-and-forget. If you genuinely need to know the
write succeeded, do it inside `withContext(Dispatchers.IO)`.

---

### D4 — Network calls on the main thread

**Pattern A — Retrofit synchronous calls.**

```bash
grep -rEn "\.execute\(\)" --include="*.kt" --include="*.java" .
```

For each hit, check if it's a Retrofit `Call.execute()`. Synchronous, blocks calling
thread.

**Pattern B — `URL.openStream` / `HttpURLConnection.connect`.**

```bash
grep -rEn "URL\([^)]+\)\.openStream|HttpURLConnection|openConnection\(\)" \
  --include="*.kt" --include="*.java" .
```

For each, check the call site's threading.

**Pattern C — OkHttp synchronous.**

```bash
grep -rEn "client\.newCall\([^)]+\)\.execute\(\)" --include="*.kt" --include="*.java" .
```

**Why it's a bug.** Networking is variable-latency. On Main, every call is a potential ANR.
On a slow network, even small calls block frames.

**Severity.** Critical on Main.

**Recommended fix.** Use Retrofit suspend functions, OkHttp `enqueue` with a callback,
or `withContext(Dispatchers.IO) { call.execute() }`. For modern code, prefer suspend.

---

### D5 — File I/O on the main thread

**Pattern.**

```bash
grep -rEn "FileInputStream\(|FileOutputStream\(|FileReader\(|FileWriter\(|\
File\([^)]+\)\.readText|File\([^)]+\)\.readBytes|File\([^)]+\)\.writeText|\
File\([^)]+\)\.writeBytes|RandomAccessFile|Files\.read|Files\.write" \
  --include="*.kt" --include="*.java" .
```

For each hit, trace the call site to identify the dispatcher / thread.

**Why it's a bug.** Disk reads on Main on a busy device or a cold cache → ANR. Even
fast paths add measurable jank.

**Severity.** High to Critical depending on size and frequency.

**Recommended fix.** Wrap in `withContext(Dispatchers.IO) { … }`. For configuration files
read once at startup, consider DataStore (which is async by design).

---

### D6 — `BitmapFactory.decode*` on the main thread

**Pattern.**

```bash
grep -rEn "BitmapFactory\.(decodeFile|decodeStream|decodeResource|decodeByteArray)" \
  --include="*.kt" --include="*.java" .
```

**Why it's a bug.** Bitmap decoding is CPU-heavy and allocates large buffers; on Main it
janks the UI and risks OOM in addition.

**Severity.** High.

**Recommended fix.** Use Coil/Glide/Picasso for image loading (they handle threading
and caching). For ad-hoc decoding, do it on `Dispatchers.IO` (or `Default` if pure CPU).

---

### D7 — JSON parsing on the main thread

**Pattern.**

```bash
grep -rEn "JSONObject\([^)]+\)|JSONArray\([^)]+\)|Gson\(\)\.from|moshi\.adapter|\
\.fromJson\(|kotlinx.serialization.*decodeFromString" --include="*.kt" --include="*.java" .
```

For each, trace to the calling thread.

**Why it's a bug.** Large JSON parses on Main cause measurable jank. For payloads >100KB,
ANR risk.

**Severity.** Medium to High depending on payload size and frequency.

**Recommended fix.** Parse in `withContext(Dispatchers.Default)` for CPU-bound parses;
let Retrofit's converters parse off-thread automatically.

---

### D8 — Heavy work in `onCreate` / `onStart` / `onResume`

**Pattern.** Inside an Activity's or Fragment's `onCreate`, look for:
- `Database.databaseBuilder(…).build()` (Room build is heavy)
- Crypto initialization (`KeyStore.getInstance`, BouncyCastle setup)
- Reflection-heavy framework startup
- DI graph initialization that's not lazy

```bash
grep -rEnA20 "override fun onCreate" --include="*.kt" .
```

**Why it's a bug.** Adds to startup time and TTI (time-to-interactive). On low-end
devices, can cause cold-start ANR.

**Severity.** Medium to High.

**Recommended fix.** Move to App Startup library, lazy initialization, or background
init via WorkManager/coroutines launched from Application.

---

### D9 — `Thread.sleep` / `Object.wait` on Main

**Pattern.**

```bash
grep -rEn "Thread\.sleep|\.wait\(\d|wait\s*\(\s*\)" --include="*.kt" --include="*.java" .
```

For each, trace the thread.

**Why it's a bug.** Direct UI block. Rare in modern code but still appears in ports
from other platforms.

**Severity.** Critical on Main.

**Recommended fix.** `delay(ms)` in a coroutine.

---

### D10 — `SharedPreferences.getXxx` from disk on cold start

**Pattern.** First-touch reads of SharedPreferences in `Application.onCreate` or an
Activity's `onCreate`. The first read forces a full prefs file load.

```bash
grep -rEnA5 "getSharedPreferences\s*\(" --include="*.kt" --include="*.java" .
```

**Why it's a bug.** First read is synchronous disk I/O. On Main during cold start, adds
to TTI.

**Severity.** Medium.

**Recommended fix.** Migrate to DataStore. If staying on SharedPreferences, "warm" the
prefs in a background coroutine at App startup, or read on IO dispatcher.

---

### D11 — `ContentResolver.query` on Main

**Pattern.**

```bash
grep -rEn "\.contentResolver\.query\(|getContentResolver\(\)\.query\(" \
  --include="*.kt" --include="*.java" .
```

**Why it's a bug.** Content resolvers can hit other apps' processes (system, providers).
Variable latency, can ANR.

**Severity.** High.

**Recommended fix.** Wrap in `withContext(Dispatchers.IO)`.

---

### D12 — `WebView.loadUrl` with synchronous JS evaluation

**Pattern.**

```bash
grep -rEn "evaluateJavascript|\.loadUrl\(\"javascript:" --include="*.kt" --include="*.java" .
```

For each, check whether the callback handler does heavy work synchronously, and whether
the call is on Main (it usually is — WebView is Main-thread-bound).

**Severity.** Medium. WebView Main-thread requirement is a constraint, not a bug, but
heavy JS work in callbacks can stall.

---

### D13 — `Intent` / package-manager queries on Main

**Pattern.**

```bash
grep -rEn "packageManager\.\w+|getPackageManager\(\)\.\w+" --include="*.kt" --include="*.java" .
```

For each, verify the call: `queryIntentActivities`, `getInstalledPackages`, `getApplicationInfo`
in particular hit IPC and can be slow on devices with many apps.

**Severity.** Medium.

**Recommended fix.** Wrap in `withContext(Dispatchers.IO)`.

---

### D14 — Synchronous WorkManager / JobScheduler scheduling on Main during startup

**Pattern.** `WorkManager.getInstance(context).enqueue(...)` in `onCreate`.

Usually fine, but heavy enqueueing patterns in startup paths add measurable cost.

**Severity.** Low.

---

## Step 3 — Write the report

Write findings to `<workspace>/findings-main-thread-violations.md` in shared Bug Report
Format. Group by detector ID; the dispatcher will renumber and sort.

---

## Notes

- StrictMode catches many of these at runtime in debug builds. If the project has
  StrictMode enabled in Application.onCreate, mention it in the report — it's a
  complementary tool.
- `withContext(Dispatchers.IO)` is the most common fix; verify it's the right dispatcher
  (`IO` for blocking I/O, `Default` for CPU-bound) when recommending.
- Distinguish between "always on Main" (e.g. inside `onClick` of a View) and "sometimes
  on Main" (e.g. inside a callback whose threading depends on the SDK). For ambiguous
  cases, mark Confidence Medium and flag the call site for verification.
