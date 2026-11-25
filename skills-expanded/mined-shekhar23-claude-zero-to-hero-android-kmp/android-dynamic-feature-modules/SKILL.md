---
name: android-dynamic-feature-modules
description: |
  Dynamic feature modules for Android - on-demand vs install-time vs fast-follow delivery, build.gradle setup with com.android.dynamic-feature plugin, SplitInstallManager request and state monitoring, navigation to dynamic feature destinations, install failure handling, local testing with bundletool, and SplitInstallManager fakes for tests. Use this skill whenever splitting app features into on-demand modules, reducing base APK size, using Play Feature Delivery, or navigating to dynamically installed code. Trigger on phrases like "dynamic feature", "on-demand module", "Play Feature Delivery", "SplitInstallManager", "dynamic delivery", "install on demand", "modular APK", "feature split".
---

# Android Dynamic Feature Modules

## Overview

Dynamic Feature Modules (DFMs) let you ship features as separate APK splits installed on demand via Play Feature Delivery. This reduces base APK size and defers download of rarely used features.

**DFMs are not the same as multi-module architecture.** Multi-module is a build-time concern (faster builds, clear boundaries). DFMs are a delivery concern (smaller installs, on-demand code). A feature can be in its own Gradle module AND be a dynamic feature — these are orthogonal.

Related skills: `android-module-structure`, `android-navigation`, `android-di-koin`.

---

## When to Use Dynamic Features

Use DFMs when:
- A feature is used by < 20% of users (e.g. AR mode, admin panel, onboarding wizard)
- A feature adds > 2 MB to the download size
- You want to offer optional capabilities (e.g. language packs, game levels)

Do NOT use DFMs for:
- Core navigation paths (login, main feed)
- Features needed on first launch
- Reducing build complexity (use regular modules for that)

---

## Delivery Types

| Type | When installed | Use case |
|---|---|---|
| `on-demand` | App requests it at runtime | Rarely used features |
| `install-time` | With the base APK (but still a separate split) | Locale splits, density splits |
| `fast-follow` | Shortly after base install, in background | Features needed in first session |

---

## Gradle Setup

### App module (`build.gradle.kts :app`)

```kotlin
android {
    dynamicFeatures += setOf(":feature-camera", ":feature-admin")
}
```

### Dynamic feature module (`build.gradle.kts :feature-camera`)

```kotlin
plugins {
    id("com.android.dynamic-feature")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.feature.camera"
    compileSdk = 35

    defaultConfig {
        minSdk = 26
    }
}

dependencies {
    // depend on :app, not the other way around
    implementation(project(":app"))
    // your feature dependencies
}
```

### AndroidManifest.xml (dynamic feature)

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:dist="http://schemas.android.com/apk/distribution">

    <dist:module
        dist:instant="false"
        dist:title="@string/title_feature_camera">
        <dist:delivery>
            <dist:on-demand />
        </dist:delivery>
        <dist:fusing dist:include="true" />
    </dist:module>

</manifest>
```

---

## SplitInstallManager: Requesting a Module

```kotlin
class DynamicFeatureLoader(private val activity: Activity) {

    private val splitInstallManager = SplitInstallManagerFactory.create(activity)

    fun installCameraFeature(
        onInstalled: () -> Unit,
        onProgress: (Int) -> Unit,
        onFailure: (Int) -> Unit,
    ) {
        // Already installed — proceed immediately
        if (splitInstallManager.installedModules.contains("feature-camera")) {
            onInstalled()
            return
        }

        val request = SplitInstallRequest.newBuilder()
            .addModule("feature-camera")
            .build()

        splitInstallManager.registerListener { state ->
            when (state.status()) {
                SplitInstallSessionStatus.DOWNLOADING -> {
                    val progress = (state.bytesDownloaded() * 100 / state.totalBytesToDownload()).toInt()
                    onProgress(progress)
                }
                SplitInstallSessionStatus.INSTALLED -> onInstalled()
                SplitInstallSessionStatus.FAILED -> onFailure(state.errorCode())
                SplitInstallSessionStatus.REQUIRES_USER_CONFIRMATION -> {
                    // Large modules require user confirmation
                    splitInstallManager.startConfirmationDialogForResult(state, activity, REQUEST_CODE)
                }
                else -> Unit
            }
        }

        splitInstallManager.startInstall(request)
            .addOnFailureListener { exception ->
                val errorCode = (exception as? SplitInstallException)?.errorCode
                    ?: SplitInstallErrorCode.INTERNAL_ERROR
                onFailure(errorCode)
            }
    }
}
```

---

## Error Codes

Handle the most common failure states:

```kotlin
fun handleInstallError(errorCode: Int): UiText = when (errorCode) {
    SplitInstallErrorCode.NETWORK_ERROR ->
        UiText.StringResource(R.string.error_no_network)
    SplitInstallErrorCode.INSUFFICIENT_STORAGE ->
        UiText.StringResource(R.string.error_no_storage)
    SplitInstallErrorCode.MODULE_UNAVAILABLE ->
        UiText.StringResource(R.string.error_feature_unavailable)
    SplitInstallErrorCode.ACCESS_DENIED ->
        UiText.StringResource(R.string.error_access_denied)
    else ->
        UiText.StringResource(R.string.error_generic)
}
```

---

## Navigation to Dynamic Feature Destinations

Option A — manual class loading after install:

```kotlin
// After install confirmed:
val intent = Intent().setClassName(
    packageName,
    "com.example.feature.camera.CameraActivity"
)
startActivity(intent)
```

Option B — `DynamicNavHostFragment` (if using Jetpack Navigation with XML graphs):

```xml
<!-- nav graph in :app -->
<include-dynamic
    android:id="@+id/camera_graph"
    app:moduleName="feature-camera"
    app:graphResName="camera_nav_graph"
    app:progressDestination="@id/installProgressFragment" />
```

Option C — Compose with manual install gate (recommended for Compose projects):

```kotlin
@Composable
fun CameraEntryPoint(loader: DynamicFeatureLoader) {
    var installState by remember { mutableStateOf<InstallState>(InstallState.Idle) }

    when (installState) {
        is InstallState.Idle -> {
            Button(onClick = {
                installState = InstallState.Installing(0)
                loader.installCameraFeature(
                    onInstalled = { installState = InstallState.Installed },
                    onProgress = { installState = InstallState.Installing(it) },
                    onFailure = { installState = InstallState.Failed(it) },
                )
            }) { Text("Open Camera") }
        }
        is InstallState.Installing -> LinearProgressIndicator(
            progress = { (installState as InstallState.Installing).progress / 100f }
        )
        is InstallState.Installed -> CameraScreen() // loaded via reflection or class reference
        is InstallState.Failed -> ErrorView(
            message = handleInstallError((installState as InstallState.Failed).errorCode)
        )
    }
}

sealed interface InstallState {
    data object Idle : InstallState
    data class Installing(val progress: Int) : InstallState
    data object Installed : InstallState
    data class Failed(val errorCode: Int) : InstallState
}
```

---

## Local Testing with bundletool

Build and test locally without uploading to Play:

```bash
# Build app bundle
./gradlew :app:bundleDebug

# Install with bundletool (simulates Play delivery)
bundletool build-apks \
    --bundle=app/build/outputs/bundle/debug/app-debug.aab \
    --output=app.apks \
    --local-testing

bundletool install-apks --apks=app.apks
```

The `--local-testing` flag makes `SplitInstallManager` serve modules from the device's local storage instead of Play servers.

---

## Fake for Tests

```kotlin
class FakeSplitInstallManager : SplitInstallManager {
    private val _installedModules = mutableSetOf<String>()
    override fun getInstalledModules(): Set<String> = _installedModules

    fun simulateInstall(moduleName: String) {
        _installedModules.add(moduleName)
    }
    // implement other interface methods as no-ops
}
```

---

## Checklist

- [ ] Dynamic feature manifest declares `dist:on-demand` (or correct delivery type)
- [ ] Feature module depends on `:app`, not vice versa
- [ ] Install failure states handled (network, storage, unavailable)
- [ ] Large installs (> 10 MB) handle `REQUIRES_USER_CONFIRMATION`
- [ ] Tested locally with `bundletool --local-testing`
- [ ] Loading/progress UI shown during download
- [ ] Module name in `SplitInstallRequest` matches the Gradle module name exactly

---

## Anti-Patterns

| Anti-pattern | Why it's wrong | Instead |
|---|---|---|
| Using DFMs to reduce build complexity | DFMs add release complexity (bundletool, Play delivery) | Use regular Gradle modules for build boundaries |
| Putting core auth or main nav in a DFM | User can't launch the app if install fails | Only use DFMs for non-critical features |
| Ignoring `REQUIRES_USER_CONFIRMATION` | Install silently fails for large modules | Show the system confirmation dialog |
| Not testing with bundletool | Install works in debug APK but fails in AAB | Always test the AAB path locally |
| Accessing DFM classes before install confirmed | `ClassNotFoundException` at runtime | Gate all class access behind install state check |
