---
name: android-media-playback-camera
description: |
  Media playback and camera patterns for Android - Media3/ExoPlayer player lifecycle, PlayerView in Compose via AndroidView, CameraX Preview/ImageCapture/VideoCapture use cases, ProcessCameraProvider lifecycle binding, saving captured media to MediaStore with scoped storage, and background audio with MediaSessionService. Use this skill whenever implementing video or audio playback, integrating a camera preview, capturing photos or video, or playing audio in the background. Trigger on phrases like "video player", "ExoPlayer", "Media3", "camera", "CameraX", "capture photo", "record video", "media playback", or "background audio".
---

# Android Media Playback and Camera (Media3 + CameraX)

## Core Principles

- Create the ExoPlayer in `onStart`, release it in `onStop` — never leak a player across configuration changes.
- CameraX use cases are bound to a `LifecycleOwner`; let the library manage start/stop automatically.
- Always request CAMERA and RECORD_AUDIO permissions before binding CameraX use cases. See **android-permissions-device-apis**.
- Save captured media through MediaStore, not raw file paths — scoped storage makes direct paths unreliable on Android 10+.
- Background audio requires a `MediaSessionService` and a foreground notification; plain coroutines in the background are killed.

---

## Gradle Dependencies

```kotlin
// libs.versions.toml
[versions]
media3 = "1.3.1"
camerax = "1.3.3"

[libraries]
media3-exoplayer      = { module = "androidx.media3:media3-exoplayer",       version.ref = "media3" }
media3-ui             = { module = "androidx.media3:media3-ui",              version.ref = "media3" }
media3-session        = { module = "androidx.media3:media3-session",         version.ref = "media3" }
camerax-core          = { module = "androidx.camera:camera-core",            version.ref = "camerax" }
camerax-camera2       = { module = "androidx.camera:camera-camera2",        version.ref = "camerax" }
camerax-lifecycle     = { module = "androidx.camera:camera-lifecycle",       version.ref = "camerax" }
camerax-view          = { module = "androidx.camera:camera-view",            version.ref = "camerax" }
camerax-video         = { module = "androidx.camera:camera-video",           version.ref = "camerax" }
```

```kotlin
// app/build.gradle.kts
dependencies {
    implementation(libs.media3.exoplayer)
    implementation(libs.media3.ui)
    implementation(libs.media3.session)
    implementation(libs.camerax.core)
    implementation(libs.camerax.camera2)
    implementation(libs.camerax.lifecycle)
    implementation(libs.camerax.view)
    implementation(libs.camerax.video)
}
```

---

## Media3 / ExoPlayer — Player Lifecycle

The player is expensive. Create it in `onStart` (or later), release it in `onStop` so it does not hold codec resources while the app is not visible.

```kotlin
class VideoViewModel : ViewModel() {

    var player: ExoPlayer? = null
        private set

    fun initPlayer(context: Context) {
        if (player != null) return
        player = ExoPlayer.Builder(context.applicationContext).build()
    }

    fun setMediaItem(url: String) {
        player?.run {
            setMediaItem(MediaItem.fromUri(url))
            prepare()
            playWhenReady = true
        }
    }

    fun pausePlayer() {
        player?.pause()
    }

    fun releasePlayer() {
        player?.release()
        player = null
    }

    override fun onCleared() {
        super.onCleared()
        releasePlayer()
    }
}
```

Anti-pattern: creating `ExoPlayer` inside a `@Composable` — it will be recreated on every recomposition. Own the player in the `ViewModel` or a `DisposableEffect`.

---

## PlayerView in Compose via AndroidView

`PlayerView` is a traditional `View`; wrap it with `AndroidView`:

```kotlin
@Composable
fun VideoPlayer(
    player: ExoPlayer,
    modifier: Modifier = Modifier
) {
    AndroidView(
        factory = { context ->
            PlayerView(context).apply {
                this.player = player
                useController = true
                resizeMode = AspectRatioFrameLayout.RESIZE_MODE_FIT
            }
        },
        update = { view ->
            // Re-attach if the player instance changed
            view.player = player
        },
        modifier = modifier.fillMaxWidth().aspectRatio(16f / 9f)
    )
}
```

Lifecycle management from a screen:

```kotlin
@Composable
fun VideoScreen(viewModel: VideoViewModel = koinViewModel()) {
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current

    DisposableEffect(lifecycleOwner) {
        val observer = LifecycleEventObserver { _, event ->
            when (event) {
                Lifecycle.Event.ON_START -> viewModel.initPlayer(context)
                Lifecycle.Event.ON_STOP  -> viewModel.releasePlayer()
                else -> Unit
            }
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose { lifecycleOwner.lifecycle.removeObserver(observer) }
    }

    val player = viewModel.player ?: return
    VideoPlayer(player = player)
}
```

---

## CameraX — Permission Check

Always verify permissions before any camera operation. See **android-permissions-device-apis** for the full request flow.

```kotlin
fun hasCameraPermission(context: Context): Boolean =
    ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA) ==
        PackageManager.PERMISSION_GRANTED

fun hasAudioPermission(context: Context): Boolean =
    ContextCompat.checkSelfPermission(context, Manifest.permission.RECORD_AUDIO) ==
        PackageManager.PERMISSION_GRANTED
```

Declare in `AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-feature android:name="android.hardware.camera.any" android:required="false" />
```

---

## CameraX — ProcessCameraProvider and Lifecycle Binding

```kotlin
class CameraViewModel : ViewModel() {

    private val _capturedImageUri = MutableStateFlow<Uri?>(null)
    val capturedImageUri: StateFlow<Uri?> = _capturedImageUri.asStateFlow()

    // Owned here so composable can access
    var imageCapture: ImageCapture? = null
        private set

    fun bindCamera(
        lifecycleOwner: LifecycleOwner,
        context: Context,
        previewView: PreviewView
    ) {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(context)
        cameraProviderFuture.addListener({
            val cameraProvider = cameraProviderFuture.get()

            val preview = Preview.Builder().build().also {
                it.setSurfaceProvider(previewView.surfaceProvider)
            }

            imageCapture = ImageCapture.Builder()
                .setCaptureMode(ImageCapture.CAPTURE_MODE_MINIMIZE_LATENCY)
                .build()

            try {
                cameraProvider.unbindAll()
                cameraProvider.bindToLifecycle(
                    lifecycleOwner,
                    CameraSelector.DEFAULT_BACK_CAMERA,
                    preview,
                    imageCapture!!
                )
            } catch (e: Exception) {
                // Camera bind failed — handle gracefully in UI state
            }
        }, ContextCompat.getMainExecutor(context))
    }
}
```

`bindToLifecycle` handles start/stop automatically: camera opens on `ON_START`, closes on `ON_STOP`. Never call `camera.close()` manually when using lifecycle binding.

---

## CameraX — ImageCapture (Photo)

```kotlin
fun capturePhoto(
    context: Context,
    imageCapture: ImageCapture,
    onResult: (Uri?) -> Unit
) {
    val contentValues = ContentValues().apply {
        put(MediaStore.Images.Media.DISPLAY_NAME, "photo_${System.currentTimeMillis()}.jpg")
        put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg")
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            put(MediaStore.Images.Media.RELATIVE_PATH, Environment.DIRECTORY_PICTURES + "/MyApp")
        }
    }

    val outputOptions = ImageCapture.OutputFileOptions.Builder(
        context.contentResolver,
        MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
        contentValues
    ).build()

    imageCapture.takePicture(
        outputOptions,
        ContextCompat.getMainExecutor(context),
        object : ImageCapture.OnImageSavedCallback {
            override fun onImageSaved(output: ImageCapture.OutputFileResults) {
                onResult(output.savedUri)
            }
            override fun onError(exception: ImageCaptureException) {
                onResult(null)
            }
        }
    )
}
```

---

## CameraX — VideoCapture (Recording)

```kotlin
// Add VideoCapture use case alongside Preview in bindCamera
private var videoCapture: VideoCapture<Recorder>? = null
private var activeRecording: Recording? = null

fun bindCameraWithVideo(
    lifecycleOwner: LifecycleOwner,
    context: Context,
    previewView: PreviewView
) {
    val cameraProviderFuture = ProcessCameraProvider.getInstance(context)
    cameraProviderFuture.addListener({
        val cameraProvider = cameraProviderFuture.get()
        val preview = Preview.Builder().build().also {
            it.setSurfaceProvider(previewView.surfaceProvider)
        }
        val recorder = Recorder.Builder()
            .setQualitySelector(QualitySelector.from(Quality.HD))
            .build()
        videoCapture = VideoCapture.withOutput(recorder)

        cameraProvider.unbindAll()
        cameraProvider.bindToLifecycle(
            lifecycleOwner,
            CameraSelector.DEFAULT_BACK_CAMERA,
            preview,
            videoCapture!!
        )
    }, ContextCompat.getMainExecutor(context))
}

fun startRecording(context: Context, onVideoSaved: (Uri?) -> Unit) {
    val contentValues = ContentValues().apply {
        put(MediaStore.Video.Media.DISPLAY_NAME, "video_${System.currentTimeMillis()}.mp4")
        put(MediaStore.Video.Media.MIME_TYPE, "video/mp4")
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            put(MediaStore.Video.Media.RELATIVE_PATH, Environment.DIRECTORY_MOVIES + "/MyApp")
        }
    }

    activeRecording = videoCapture?.output
        ?.prepareRecording(context, MediaStoreOutputOptions.Builder(
            context.contentResolver,
            MediaStore.Video.Media.EXTERNAL_CONTENT_URI
        ).setContentValues(contentValues).build())
        ?.withAudioEnabled()
        ?.start(ContextCompat.getMainExecutor(context)) { event ->
            if (event is VideoRecordEvent.Finalize) {
                onVideoSaved(if (!event.hasError()) event.outputResults.outputUri else null)
            }
        }
}

fun stopRecording() {
    activeRecording?.stop()
    activeRecording = null
}
```

---

## Saving to MediaStore (Scoped Storage)

On Android 10+ (API 29+) you must write media through `MediaStore` or the Storage Access Framework. Direct paths to shared storage are no longer permitted.

```kotlin
fun saveImageToMediaStore(context: Context, bitmap: Bitmap): Uri? {
    val contentValues = ContentValues().apply {
        put(MediaStore.Images.Media.DISPLAY_NAME, "image_${System.currentTimeMillis()}.jpg")
        put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg")
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            put(MediaStore.Images.Media.RELATIVE_PATH, Environment.DIRECTORY_PICTURES)
            put(MediaStore.Images.Media.IS_PENDING, 1)
        }
    }

    val resolver = context.contentResolver
    val uri = resolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, contentValues)
        ?: return null

    resolver.openOutputStream(uri)?.use { stream ->
        bitmap.compress(Bitmap.CompressFormat.JPEG, 95, stream)
    }

    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        contentValues.clear()
        contentValues.put(MediaStore.Images.Media.IS_PENDING, 0)
        resolver.update(uri, contentValues, null, null)
    }

    return uri
}
```

Set `IS_PENDING = 1` while writing, then `IS_PENDING = 0` after — this prevents other apps from seeing a partially written file.

Anti-pattern: writing to `Environment.getExternalStorageDirectory()` directly — crashes with `FileNotFoundException` on Android 10+ without legacy storage permission.

---

## CameraX Preview in Compose

```kotlin
@Composable
fun CameraPreview(
    onPreviewCreated: (PreviewView) -> Unit,
    modifier: Modifier = Modifier
) {
    AndroidView(
        factory = { context ->
            PreviewView(context).apply {
                implementationMode = PreviewView.ImplementationMode.COMPATIBLE
                scaleType = PreviewView.ScaleType.FILL_CENTER
                onPreviewCreated(this)
            }
        },
        modifier = modifier
    )
}

@Composable
fun CameraScreen(viewModel: CameraViewModel = koinViewModel()) {
    val lifecycleOwner = LocalLifecycleOwner.current
    val context = LocalContext.current

    CameraPreview(
        onPreviewCreated = { previewView ->
            viewModel.bindCamera(lifecycleOwner, context, previewView)
        },
        modifier = Modifier.fillMaxSize()
    )
}
```

---

## Background Audio with MediaSessionService

For audio that should continue when the user leaves the app, use `MediaSessionService`:

```kotlin
class AudioPlaybackService : MediaSessionService() {

    private lateinit var player: ExoPlayer
    private lateinit var mediaSession: MediaSession

    override fun onCreate() {
        super.onCreate()
        player = ExoPlayer.Builder(this).build()
        mediaSession = MediaSession.Builder(this, player).build()
    }

    override fun onGetSession(controllerInfo: MediaSession.ControllerInfo): MediaSession =
        mediaSession

    override fun onDestroy() {
        mediaSession.release()
        player.release()
        super.onDestroy()
    }
}
```

Register in `AndroidManifest.xml`:

```xml
<service
    android:name=".AudioPlaybackService"
    android:foregroundServiceType="mediaPlayback"
    android:exported="true">
    <intent-filter>
        <action android:name="androidx.media3.session.MediaSessionService" />
    </intent-filter>
</service>
```

Connect from the UI with `MediaController`:

```kotlin
class AudioViewModel : ViewModel() {

    private var mediaController: MediaController? = null

    fun connectController(context: Context) {
        val sessionToken = SessionToken(
            context,
            ComponentName(context, AudioPlaybackService::class.java)
        )
        MediaController.Builder(context, sessionToken)
            .buildAsync()
            .also { future ->
                future.addListener(
                    { mediaController = future.get() },
                    ContextCompat.getMainExecutor(context)
                )
            }
    }

    fun play(uri: Uri) {
        mediaController?.run {
            setMediaItem(MediaItem.fromUri(uri))
            prepare()
            play()
        }
    }

    fun pause()  { mediaController?.pause() }
    fun resume() { mediaController?.play()  }

    override fun onCleared() {
        mediaController?.release()
        super.onCleared()
    }
}
```

---

## App-Specific Storage vs MediaStore

| Use case                          | Recommended location              |
|-----------------------------------|-----------------------------------|
| App's own cache (temp files)      | `context.cacheDir`                |
| App's own persistent files        | `context.filesDir` / `getExternalFilesDir` |
| Photos/videos visible in Gallery  | `MediaStore`                      |
| User-picked file locations        | Storage Access Framework          |

App-specific directories do not require any storage permissions.

---

## Checklist: Media Playback

- [ ] ExoPlayer created in `onStart`, released in `onStop`
- [ ] Player owned in `ViewModel` or a `DisposableEffect`, never recreated per recomposition
- [ ] `PlayerView` wrapped in `AndroidView` with `update` lambda for player re-attachment
- [ ] Background audio uses `MediaSessionService` with `foregroundServiceType="mediaPlayback"`

## Checklist: Camera

- [ ] CAMERA (and RECORD_AUDIO for video) permissions requested before use
- [ ] Use cases bound with `bindToLifecycle` — never manage camera lifecycle manually
- [ ] Captured images/videos written to MediaStore with `IS_PENDING` guard
- [ ] Video recording stops explicitly before the lifecycle ends
- [ ] CameraX `PreviewView` wrapped in `AndroidView` in Compose
