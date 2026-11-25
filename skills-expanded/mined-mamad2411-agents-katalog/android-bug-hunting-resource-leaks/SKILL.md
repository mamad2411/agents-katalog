---
name: android-bug-hunting-resource-leaks
description: >
  Hunt for resource leaks in Android/Kotlin code: Cursor, InputStream, OutputStream, Reader,
  Writer not closed; OkHttp Response bodies not closed; database transactions left open;
  ContentProviderClient not released; TypedArray.recycle() missing; Bitmap not recycled
  (legacy); ParcelFileDescriptor leaks; AssetFileDescriptor leaks; MediaPlayer/MediaRecorder
  not released; Camera/CameraX session not closed; SQLite SQLiteStatement / SQLiteOpenHelper
  not closed. Use this skill whenever the user asks to find resource leaks, file-descriptor
  leaks, "unclosed streams", "unclosed cursors", or wants an audit for resources not properly
  released. Trigger whenever a bug hunt covers code that opens files, streams, cursors,
  network responses, or other closeable resources.
---

# Resource Leak Hunter

## Purpose

Resource leaks are a separate category from memory leaks. Memory leaks retain heap
references; resource leaks fail to release file descriptors, native handles, database
connections, or system handles. They manifest as `Too many open files`, `EMFILE`, slow
crashes, and intermittent failures that escape unit tests.

The pattern is almost always: opened, used, *missed close on an early return / exception
path*. Kotlin's `use { }` extension makes the fix cheap; this skill finds the places
where it isn't applied.

**Output format.** Use the shared Bug Report Format. Read `.claude/skills/android-bug-hunting-dispatcher/references/report-format.md` before writing findings.

---

## Step 1 — Scope

```bash
grep -rEln "Cursor|InputStream|OutputStream|Reader|Writer|Response|TypedArray|\
ParcelFileDescriptor|AssetFileDescriptor|MediaPlayer|MediaRecorder|SQLiteStatement|\
SQLiteOpenHelper|SQLiteDatabase|ContentProviderClient|FileChannel|RandomAccessFile|\
ZipFile|JarFile|Socket|ServerSocket|DatagramSocket" \
  --include="*.kt" --include="*.java" .
```

---

## Step 2 — Run each detector

The general method:

1. Find every place a closeable is opened.
2. For each, verify it is wrapped in `use { … }` (Kotlin) or `try-with-resources`
   (Java), OR closed in a `finally` that handles every path including exceptions.
3. If neither, flag.

---

### D1 — Cursor not in `use { }` / `try-finally`

**Pattern.**

```bash
grep -rEn "\.query\(|rawQuery\(" --include="*.kt" --include="*.java" .
```

Plus `ContentResolver.query` and Room helpers that return a raw `Cursor`.

For each, trace the returned Cursor:
- Kotlin: `cursor.use { … }` → safe.
- Java: `try (Cursor c = …)` → safe.
- Anything else → likely leak.

**Why it's a bug.** Cursors hold native database handles. Leaks accumulate file
descriptors and lock the parent SQLite connection. On large apps, this causes "too
many open cursors" errors.

**Severity.** Critical on hot paths, High elsewhere.

**Recommended fix.**

```kotlin
// Kotlin
contentResolver.query(uri, null, null, null, null)?.use { cursor ->
    while (cursor.moveToNext()) { /* … */ }
}
```

---

### D2 — Stream / Reader / Writer not closed

**Pattern.**

```bash
grep -rEn "FileInputStream\(|FileOutputStream\(|BufferedReader\(|BufferedWriter\(|\
InputStreamReader\(|OutputStreamWriter\(|FileReader\(|FileWriter\(|\
DataInputStream\(|DataOutputStream\(|ObjectInputStream\(|ObjectOutputStream\(" \
  --include="*.kt" --include="*.java" .
```

For each, verify `use { }` or `try-with-resources`.

**Why it's a bug.** File descriptor leak. On Android the per-process FD limit is small
(commonly 1024). Hot leaks burn through this within minutes.

**Severity.** High to Critical depending on hotness.

**Recommended fix.** `stream.use { … }`. For chained streams, use the outermost wrapper:

```kotlin
File("data.bin").inputStream().buffered().use { input ->
    /* read */
}
```

---

### D3 — OkHttp `Response` body not closed

**Pattern.**

```bash
grep -rEn "client\.newCall\(.*\)\.execute\(\)|\.body\(\)" --include="*.kt" --include="*.java" .
```

For each `execute()` that's stored or used, check whether:
- The Response is in `use { }` (Kotlin) or `try-with-resources` (Java), or
- `response.close()` is called on every path, or
- `response.body()?.string()` / `bytes()` / `byteStream()` is consumed (these read
  fully and close in the consume case for `string()`/`bytes()`, but `byteStream()`
  must be closed explicitly).

**Why it's a bug.** Unclosed responses leak the HTTP connection back into the pool in
a bad state, eventually exhausting the connection pool and stalling future requests.

**Severity.** Critical on hot paths.

**Recommended fix.**

```kotlin
client.newCall(request).execute().use { response ->
    val body = response.body?.string()
    /* … */
}
```

---

### D4 — `TypedArray.recycle()` missing

**Pattern.**

```bash
grep -rEn "obtainStyledAttributes" --include="*.kt" --include="*.java" .
```

For each, check for a corresponding `.recycle()` call on every path.

**Why it's a bug.** `TypedArray` holds a pooled native handle; not recycling exhausts
the pool over time, causing custom view inflation to slow down or fail.

**Severity.** Medium.

**Recommended fix.**

```kotlin
val a = context.obtainStyledAttributes(attrs, R.styleable.MyView)
try {
    /* read attrs */
} finally {
    a.recycle()
}
```

---

### D5 — `ContentProviderClient` not released

**Pattern.**

```bash
grep -rEn "acquireContentProviderClient|acquireUnstableContentProviderClient" \
  --include="*.kt" --include="*.java" .
```

For each, check for a paired `.release()` (or `close()` on API 24+).

**Why it's a bug.** Each unreleased client holds a reference into the provider process
and a binder reference; long-running leaks can prevent the provider's process from
being killed.

**Severity.** Medium.

**Recommended fix.** `client.use { … }` if API ≥ 24, otherwise try/finally with `release()`.

---

### D6 — Bitmap not recycled (legacy code targeting < API 26)

**Pattern.**

```bash
grep -rEn "BitmapFactory\.decode|Bitmap\.createBitmap|Bitmap\.createScaledBitmap" \
  --include="*.kt" --include="*.java" .
```

For modern apps (minSdk ≥ 26), `Bitmap.recycle()` is mostly informational — the GC
handles it. For older minSdks, manually recycling matters.

**Severity.** Low for modern apps; Medium for minSdk < 26.

**Recommended fix.** Use Coil/Glide for non-trivial bitmap work. For ad-hoc decoding,
recycle when done if minSdk < 26.

---

### D7 — `MediaPlayer` / `MediaRecorder` / `MediaCodec` not released

**Pattern.**

```bash
grep -rEn "MediaPlayer\(\)|MediaPlayer\.create|MediaRecorder\(\)|MediaCodec\.create" \
  --include="*.kt" --include="*.java" .
```

For each, verify `.release()` is called in the appropriate teardown
(`onStop`/`onDestroy`/`onPause` depending on the use case).

**Why it's a bug.** These hold large native buffers and audio focus / camera handles.
Leaks corrupt the global media state — other apps may fail to acquire audio focus, etc.

**Severity.** Critical when reachable.

**Recommended fix.** Always call `.release()` in symmetric teardown. Set the field
to null after release to make double-release safer.

---

### D8 — `Camera` / `CameraX` `ImageProxy` / `ImageReader` not closed

**Pattern.**

```bash
grep -rEn "ImageProxy|ImageReader|ImageAnalysis|androidx\.camera" \
  --include="*.kt" --include="*.java" .
```

For analyzers receiving `ImageProxy`, verify `.close()` is called even on early returns.

**Why it's a bug.** CameraX has a finite buffer queue; not closing a proxy stalls the
analysis pipeline within a few frames.

**Severity.** Critical for image analysis.

**Recommended fix.**

```kotlin
override fun analyze(image: ImageProxy) {
    try {
        /* … */
    } finally {
        image.close()
    }
}
```

---

### D9 — `SQLiteDatabase` / `SQLiteStatement` not closed

**Pattern.**

```bash
grep -rEn "SQLiteDatabase\.openOrCreateDatabase|compileStatement\(|\
SQLiteOpenHelper.*getReadableDatabase|getWritableDatabase" \
  --include="*.kt" --include="*.java" .
```

For each, check for symmetric close.

**Caveat.** Generally Room manages this. Flag only when raw SQLite APIs are used (which
already merits a Medium-priority modernization comment).

**Severity.** High in raw SQLite code.

---

### D10 — `ParcelFileDescriptor` / `AssetFileDescriptor` not closed

**Pattern.**

```bash
grep -rEn "ParcelFileDescriptor|AssetFileDescriptor|openFileDescriptor|openAssetFile" \
  --include="*.kt" --include="*.java" .
```

For each, verify `.close()` is called.

**Why it's a bug.** Direct file descriptor leak.

**Severity.** Critical.

**Recommended fix.** `descriptor.use { … }` (API 19+).

---

### D11 — `ZipFile` / `JarFile` not closed

**Pattern.**

```bash
grep -rEn "ZipFile\(|JarFile\(" --include="*.kt" --include="*.java" .
```

**Severity.** High when on hot paths (e.g. APK parsing).

**Recommended fix.** `ZipFile(file).use { … }`.

---

### D12 — `Socket` / `ServerSocket` / `DatagramSocket` not closed

**Pattern.**

```bash
grep -rEn "new Socket\(|new ServerSocket\(|new DatagramSocket\(|\
Socket\([^)]*\)\.|ServerSocket\(" --include="*.kt" --include="*.java" .
```

**Severity.** High.

**Recommended fix.** `socket.use { … }` (API 19+ for `Socket`).

---

### D13 — Database transaction begun without commit/rollback on every path

**Pattern.**

```bash
grep -rEn "beginTransaction|inTransaction" --include="*.kt" --include="*.java" .
```

For each `beginTransaction()`, the contract is to call `setTransactionSuccessful()`
and then `endTransaction()`. Look for missing `endTransaction()` in `finally`.

**Severity.** High. Leaked transactions hold write locks indefinitely.

**Recommended fix.** Use Room's `@Transaction` or `db.withTransaction { … }` from
`androidx.room.withTransaction`. For raw SQLite:

```kotlin
db.beginTransaction()
try {
    /* work */
    db.setTransactionSuccessful()
} finally {
    db.endTransaction()
}
```

---

### D14 — `BroadcastReceiver` registered with `Context.registerReceiver` not unregistered

This overlaps with `android-bug-hunting-lifecycle-leak-hunter` D5 — flag here when the receiver holds a
specific resource (file, socket, native handle), not just an Activity reference.

---

### D15 — Native `Bitmap.Config.HARDWARE` shared across processes / threads incorrectly

**Pattern.** `Bitmap.Config.HARDWARE` bitmaps cannot be read back, transformed on CPU,
or moved between processes.

```bash
grep -rEn "Bitmap\.Config\.HARDWARE" --include="*.kt" --include="*.java" .
```

**Severity.** Low to Medium — usually a correctness issue (crashes when read), not a
leak per se.

---

## Step 3 — Write the report

Write findings to `<workspace>/findings-resource-leaks.md` in shared Bug Report Format.
Group by detector ID; the dispatcher will renumber and sort.

---

## Notes

- `kotlin.io.use` is the most common fix and works for any `Closeable` (Java) or
  `AutoCloseable` (API 19+). Recommend it freely.
- Be careful with chained streams — close the outermost wrapper, not the inner one,
  to avoid "Stream Closed" exceptions on flush.
- For OkHttp, `response.body?.string()` and `.bytes()` close the body internally;
  `.byteStream()` and `.charStream()` and `.source()` do not. This nuance produces
  a steady stream of false positives — verify before flagging.
- `try-with-resources` in Java and `use` in Kotlin are not equivalent in suppression
  semantics; both are correct fixes.
