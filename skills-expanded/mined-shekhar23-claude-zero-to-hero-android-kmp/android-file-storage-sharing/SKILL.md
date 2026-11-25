---
name: android-file-storage-sharing
description: |
  File storage and sharing patterns for Android - scoped storage rules, app-specific storage with getExternalFilesDir and cacheDir, MediaStore API for images/video/audio/downloads, Storage Access Framework with ActivityResultContracts.OpenDocument and CreateDocument, FileProvider setup with provider_paths.xml for sharing content:// URIs via Intent.ACTION_SEND, DownloadManager for large background downloads, and safe handling of content:// vs file:// URIs. Use this skill whenever saving, reading, or sharing files, integrating with system file pickers, downloading large files, or configuring FileProvider for URI sharing. Trigger on phrases like "save file", "read file", "share file", "FileProvider", "MediaStore", "scoped storage", "download", "SAF", "content URI", "pick file", or "open document".
---

# Android File Storage and Sharing

## Core Principles

- On Android 10+ (API 29+), apps cannot freely write to shared storage. Use MediaStore or the Storage Access Framework.
- Never expose `file://` URIs to other apps — they will throw `FileUriExposedException` on API 24+. Use `FileProvider` instead.
- App-specific storage (`filesDir`, `cacheDir`, `getExternalFilesDir`) requires no permissions at any API level.
- Prefer MediaStore for media that should appear in system Gallery/Files apps; prefer SAF for user-chosen document locations.
- Always close streams in `finally` blocks or use `use {}` — leaking file descriptors causes silent data corruption.

---

## Storage Location Decision Tree

```
Does the file need to be visible to other apps or survive uninstall?
├── No  → App-specific storage (filesDir / cacheDir / getExternalFilesDir)
└── Yes → Is it a photo, video, audio, or generic download?
          ├── Yes → MediaStore
          └── No  → Storage Access Framework (user picks the location)
```

---

## App-Specific Storage

No permissions required. Files are deleted when the app is uninstalled.

### Internal storage (always private)

```kotlin
// Write
fun writeInternalFile(context: Context, filename: String, content: String) {
    context.openFileOutput(filename, Context.MODE_PRIVATE).use { stream ->
        stream.write(content.toByteArray())
    }
}

// Read
fun readInternalFile(context: Context, filename: String): String {
    return context.openFileInput(filename).bufferedReader().use { it.readText() }
}

// Path: context.filesDir / filename
// Cache (may be cleared by system): context.cacheDir / filename
```

### External app-specific storage (no permission needed)

```kotlin
fun writeExternalAppFile(context: Context, filename: String, data: ByteArray): File {
    val dir = context.getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS)
        ?: context.filesDir   // fallback if external not available
    return File(dir, filename).also { it.writeBytes(data) }
}
```

Use `getExternalFilesDir(null)` for a generic directory, or pass a `Environment.DIRECTORY_*` constant.

Anti-pattern: writing to `Environment.getExternalStorageDirectory()` directly — this requires `WRITE_EXTERNAL_STORAGE` (removed for new apps targeting API 29+) and is scoped-storage-incompatible.

---

## MediaStore API

Use MediaStore to insert media that should appear in the system Gallery, Music, or Files apps.

### Inserting an image

```kotlin
fun saveImageToMediaStore(
    context: Context,
    bitmap: Bitmap,
    displayName: String = "photo_${System.currentTimeMillis()}.jpg",
    relativePath: String = Environment.DIRECTORY_PICTURES + "/MyApp"
): Uri? {
    val resolver = context.contentResolver

    val contentValues = ContentValues().apply {
        put(MediaStore.Images.Media.DISPLAY_NAME, displayName)
        put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg")
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            put(MediaStore.Images.Media.RELATIVE_PATH, relativePath)
            put(MediaStore.Images.Media.IS_PENDING, 1)
        }
    }

    val uri = resolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, contentValues)
        ?: return null

    try {
        resolver.openOutputStream(uri)?.use { stream ->
            bitmap.compress(Bitmap.CompressFormat.JPEG, 95, stream)
        }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            contentValues.clear()
            contentValues.put(MediaStore.Images.Media.IS_PENDING, 0)
            resolver.update(uri, contentValues, null, null)
        }
    } catch (e: Exception) {
        resolver.delete(uri, null, null)   // clean up partial write
        return null
    }

    return uri
}
```

Always set `IS_PENDING = 1` before writing and `IS_PENDING = 0` after — this hides the file from other apps while it is being written.

### Inserting a video

```kotlin
fun insertVideoEntry(context: Context, displayName: String): Uri? {
    val contentValues = ContentValues().apply {
        put(MediaStore.Video.Media.DISPLAY_NAME, displayName)
        put(MediaStore.Video.Media.MIME_TYPE, "video/mp4")
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            put(MediaStore.Video.Media.RELATIVE_PATH, Environment.DIRECTORY_MOVIES + "/MyApp")
            put(MediaStore.Video.Media.IS_PENDING, 1)
        }
    }
    return context.contentResolver.insert(
        MediaStore.Video.Media.EXTERNAL_CONTENT_URI,
        contentValues
    )
}
```

### Inserting a download

```kotlin
fun saveFileToDownloads(context: Context, filename: String, mimeType: String): Uri? {
    if (Build.VERSION.SDK_INT < Build.VERSION_CODES.Q) return null // use DownloadManager for older
    val contentValues = ContentValues().apply {
        put(MediaStore.Downloads.DISPLAY_NAME, filename)
        put(MediaStore.Downloads.MIME_TYPE, mimeType)
        put(MediaStore.Downloads.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS)
        put(MediaStore.Downloads.IS_PENDING, 1)
    }
    return context.contentResolver.insert(
        MediaStore.Downloads.EXTERNAL_CONTENT_URI,
        contentValues
    )
}
```

### Querying media

```kotlin
fun queryImages(context: Context): List<Uri> {
    val uris = mutableListOf<Uri>()
    val projection = arrayOf(MediaStore.Images.Media._ID, MediaStore.Images.Media.DISPLAY_NAME)
    context.contentResolver.query(
        MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
        projection,
        "${MediaStore.Images.Media.RELATIVE_PATH} LIKE ?",
        arrayOf("%MyApp%"),
        "${MediaStore.Images.Media.DATE_MODIFIED} DESC"
    )?.use { cursor ->
        val idColumn = cursor.getColumnIndexOrThrow(MediaStore.Images.Media._ID)
        while (cursor.moveToNext()) {
            uris.add(
                ContentUris.withAppendedId(
                    MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
                    cursor.getLong(idColumn)
                )
            )
        }
    }
    return uris
}
```

---

## Storage Access Framework (SAF)

Use SAF when the user needs to choose the location — documents, export destinations, import sources.

### Opening a document (read)

```kotlin
// In a Root composable
val openDocumentLauncher = rememberLauncherForActivityResult(
    ActivityResultContracts.OpenDocument()
) { uri: Uri? ->
    uri?.let { viewModel.onAction(EditorAction.OnDocumentOpened(it)) }
}

// Trigger it
openDocumentLauncher.launch(arrayOf("application/pdf", "text/plain"))
```

### Creating a document (write/export)

```kotlin
val createDocumentLauncher = rememberLauncherForActivityResult(
    ActivityResultContracts.CreateDocument("application/pdf")
) { uri: Uri? ->
    uri?.let { viewModel.onAction(ExportAction.OnSaveLocationChosen(it)) }
}

// Trigger it — suggest a filename
createDocumentLauncher.launch("report_${LocalDate.now()}.pdf")
```

### Writing to a SAF URI

```kotlin
fun writeToSafUri(context: Context, uri: Uri, content: ByteArray) {
    context.contentResolver.openOutputStream(uri, "wt")?.use { stream ->
        stream.write(content)
    }
}
```

Use `"wt"` mode (write + truncate) to overwrite existing content. Use `"wa"` to append.

### Persisting SAF permissions across reboots

```kotlin
fun persistPermission(context: Context, uri: Uri) {
    context.contentResolver.takePersistableUriPermission(
        uri,
        Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION
    )
}
```

Call this immediately after the user picks a URI. The permission survives reboots until explicitly released.

---

## FileProvider Setup

FileProvider translates `File` paths to `content://` URIs that can be safely shared with other apps.

### 1. Declare in AndroidManifest.xml

```xml
<provider
    android:name="androidx.core.content.FileProvider"
    android:authorities="${applicationId}.fileprovider"
    android:exported="false"
    android:grantUriPermissions="true">
    <meta-data
        android:name="android.support.FILE_PROVIDER_PATHS"
        android:resource="@xml/provider_paths" />
</provider>
```

### 2. Define provider_paths.xml

```xml
<!-- res/xml/provider_paths.xml -->
<paths>
    <!-- Internal files dir: context.filesDir -->
    <files-path name="internal_files" path="." />

    <!-- Cache dir: context.cacheDir -->
    <cache-path name="cache" path="." />

    <!-- External files dir: getExternalFilesDir(null) -->
    <external-files-path name="external_files" path="." />

    <!-- External cache: getExternalCacheDir() -->
    <external-cache-path name="external_cache" path="." />
</paths>
```

### 3. Get a shareable URI

```kotlin
fun getShareableUri(context: Context, file: File): Uri {
    return FileProvider.getUriForFile(
        context,
        "${context.packageName}.fileprovider",
        file
    )
}
```

Anti-pattern: using `Uri.fromFile(file)` — this produces a `file://` URI that throws `FileUriExposedException` on API 24+ when passed to another app.

---

## Sharing a File via Intent

```kotlin
fun shareFile(context: Context, file: File, mimeType: String, chooserTitle: String) {
    val uri = getShareableUri(context, file)

    val shareIntent = Intent(Intent.ACTION_SEND).apply {
        type = mimeType
        putExtra(Intent.EXTRA_STREAM, uri)
        addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
    }

    context.startActivity(
        Intent.createChooser(shareIntent, chooserTitle)
            .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    )
}
```

Always include `FLAG_GRANT_READ_URI_PERMISSION` — without it the receiving app cannot open the URI.

### Sharing multiple files

```kotlin
fun shareMultipleFiles(context: Context, files: List<File>, mimeType: String) {
    val uris = files.map { getShareableUri(context, it) }

    val intent = Intent(Intent.ACTION_SEND_MULTIPLE).apply {
        type = mimeType
        putParcelableArrayListExtra(Intent.EXTRA_STREAM, ArrayList(uris))
        addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
    }
    context.startActivity(Intent.createChooser(intent, null).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
}
```

---

## Download Manager

Use `DownloadManager` for large file downloads that should survive app backgrounding and integrate with the system Downloads UI.

```kotlin
fun downloadFile(
    context: Context,
    url: String,
    fileName: String,
    mimeType: String = "application/octet-stream"
): Long {
    val request = DownloadManager.Request(Uri.parse(url)).apply {
        setTitle(fileName)
        setMimeType(mimeType)
        setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
        setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, fileName)
        setAllowedOverMetered(true)
        setAllowedOverRoaming(false)
    }
    val dm = context.getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager
    return dm.enqueue(request) // returns a download ID
}
```

### Observing download completion via BroadcastReceiver

```kotlin
class DownloadCompleteReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val downloadId = intent.getLongExtra(DownloadManager.EXTRA_DOWNLOAD_ID, -1L)
        if (downloadId == -1L) return
        // Notify ViewModel or repository with the completed download ID
    }
}
```

Register dynamically to avoid always-on battery drain:

```kotlin
// In Activity/Fragment onStart
val filter = IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE)
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
    registerReceiver(downloadReceiver, filter, Context.RECEIVER_NOT_EXPORTED)
} else {
    registerReceiver(downloadReceiver, filter)
}

// In onStop
unregisterReceiver(downloadReceiver)
```

### Querying download status

```kotlin
fun queryDownloadStatus(context: Context, downloadId: Long): Int {
    val dm = context.getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager
    val query = DownloadManager.Query().setFilterById(downloadId)
    return dm.query(query)?.use { cursor ->
        if (cursor.moveToFirst()) {
            cursor.getInt(cursor.getColumnIndexOrThrow(DownloadManager.COLUMN_STATUS))
        } else {
            DownloadManager.STATUS_FAILED
        }
    } ?: DownloadManager.STATUS_FAILED
}
```

---

## Handling content:// vs file:// URIs Safely

Never assume a URI is a `file://` URI from a third-party source. Always use `ContentResolver`:

```kotlin
fun readUriAsBytes(context: Context, uri: Uri): ByteArray? {
    return try {
        context.contentResolver.openInputStream(uri)?.use { it.readBytes() }
    } catch (e: Exception) {
        null
    }
}

fun copyUriToAppStorage(context: Context, sourceUri: Uri, destFileName: String): File? {
    val destFile = File(context.cacheDir, destFileName)
    return try {
        context.contentResolver.openInputStream(sourceUri)?.use { input ->
            destFile.outputStream().use { output ->
                input.copyTo(output)
            }
        }
        destFile
    } catch (e: Exception) {
        null
    }
}
```

Getting a display name from a content URI:

```kotlin
fun getFileNameFromUri(context: Context, uri: Uri): String? {
    if (uri.scheme == ContentResolver.SCHEME_CONTENT) {
        context.contentResolver.query(uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null)
            ?.use { cursor ->
                if (cursor.moveToFirst()) {
                    return cursor.getString(cursor.getColumnIndexOrThrow(OpenableColumns.DISPLAY_NAME))
                }
            }
    }
    return uri.lastPathSegment
}
```

Getting a file size from a content URI:

```kotlin
fun getFileSizeFromUri(context: Context, uri: Uri): Long? {
    if (uri.scheme == ContentResolver.SCHEME_CONTENT) {
        context.contentResolver.query(uri, arrayOf(OpenableColumns.SIZE), null, null, null)
            ?.use { cursor ->
                if (cursor.moveToFirst()) {
                    val sizeIndex = cursor.getColumnIndex(OpenableColumns.SIZE)
                    if (!cursor.isNull(sizeIndex)) return cursor.getLong(sizeIndex)
                }
            }
    }
    return null
}
```

Anti-pattern: calling `uri.path` on a `content://` URI and trying to open it as a `File` — this only works for `file://` URIs and will return null or a non-existent path for content URIs.

---

## Checklist: File Storage and Sharing

- [ ] App-specific storage used for files that do not need to be visible to other apps
- [ ] MediaStore used for photos/videos/audio/downloads that should appear in system apps
- [ ] SAF used when the user must choose where to save or load a file
- [ ] `IS_PENDING` guard applied for all MediaStore writes
- [ ] `file://` URIs never exposed to other apps — FileProvider used instead
- [ ] `FLAG_GRANT_READ_URI_PERMISSION` included in all sharing intents
- [ ] `provider_paths.xml` only exposes directories the app actually needs to share
- [ ] Large downloads use `DownloadManager`, not background coroutines writing directly
- [ ] All `InputStream`/`OutputStream` access wrapped in `use {}` or explicit `finally` close
- [ ] Content URI metadata (name, size) read via `ContentResolver.query` with `OpenableColumns`
