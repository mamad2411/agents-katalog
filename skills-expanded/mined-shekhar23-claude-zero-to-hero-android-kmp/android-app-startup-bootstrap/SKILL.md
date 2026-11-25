---
name: android-app-startup-bootstrap
description: |
  App startup and bootstrap patterns for Android - App Startup library Initializer<T> with dependency ordering, lazy vs eager initialization strategy, Baseline Profiles with Macrobenchmark and profileinstaller, SplashScreen API with animated icons, Application class best practices, and a cold-start checklist to eliminate strict-mode violations and synchronous I/O from the main thread. Use this skill whenever optimizing app startup time, setting up the splash screen, configuring the App Startup library, generating Baseline Profiles, or deciding what belongs in Application.onCreate(). Trigger on phrases like "app startup", "cold start", "splash screen", "SplashScreen API", "Baseline Profile", "App Startup library", "Initializer", or "startup time".
---

# Android App Startup and Bootstrap

## Core Principles

- Every millisecond of cold start is user-visible. Treat the main thread on startup as sacred.
- Do not initialize anything in `Application.onCreate()` that is not needed to render the first frame.
- Use the App Startup library to declare explicit initialization order and enable lazy loading.
- Baseline Profiles move critical code out of JIT and into AOT-compiled paths — generate them before every release.
- The SplashScreen API is the only supported way to show a launch screen on Android 12+.

---

## Application Class Best Practices

`Application.onCreate()` runs on the main thread before any UI. Keep it minimal.

Belongs in `Application.onCreate()`:
- registering the App Startup `AppInitializer` (if not using manifest-based discovery)
- crash reporting SDK init (but defer heavy config)
- creating the notification channels (see **android-notifications-push**)
- strict-mode setup in debug builds

Does not belong there:
- network calls
- database opens or migrations
- heavy SDK initialization that can be lazy
- anything that reads from disk synchronously

```kotlin
class App : Application() {

    override fun onCreate() {
        super.onCreate()

        if (BuildConfig.DEBUG) {
            StrictMode.setThreadPolicy(
                StrictMode.ThreadPolicy.Builder()
                    .detectAll()
                    .penaltyLog()
                    .build()
            )
            StrictMode.setVmPolicy(
                StrictMode.VmPolicy.Builder()
                    .detectLeakedSqlLiteObjects()
                    .detectLeakedClosableObjects()
                    .penaltyLog()
                    .build()
            )
        }

        createNotificationChannels(this)

        // App Startup initializers declared in manifest run automatically.
        // Call AppInitializer.getInstance(this).initializeComponent() only for
        // lazy initializers that are not auto-started.
    }
}
```

Anti-pattern: calling `FirebaseApp.initializeApp(this)` manually when `google-services.json` is present — the plugin already generates an automatic `ContentProvider` that runs before `Application.onCreate()`.

---

## App Startup Library

### Dependency

```kotlin
// libs.versions.toml
[libraries]
startup-runtime = { module = "androidx.startup:startup-runtime", version = "1.1.1" }
```

### Initializer<T>

Each `Initializer<T>` does one thing and declares its dependencies:

```kotlin
// Timber must initialize before anything that logs
class TimberInitializer : Initializer<Unit> {
    override fun create(context: Context) {
        if (BuildConfig.DEBUG) {
            Timber.plant(Timber.DebugTree())
        } else {
            Timber.plant(CrashReportingTree())
        }
    }
    override fun dependencies(): List<Class<out Initializer<*>>> = emptyList()
}

// Koin depends on nothing else
class KoinInitializer : Initializer<Unit> {
    override fun create(context: Context) {
        startKoin {
            androidContext(context)
            modules(appModule)
        }
    }
    override fun dependencies(): List<Class<out Initializer<*>>> = emptyList()
}

// Analytics depends on Timber so it can log initialization events
class AnalyticsInitializer : Initializer<Unit> {
    override fun create(context: Context) {
        // Initialize analytics SDK
        Timber.d("Analytics initialized")
    }
    override fun dependencies(): List<Class<out Initializer<*>>> =
        listOf(TimberInitializer::class.java)
}
```

### Manifest registration (eager — runs on app start)

```xml
<provider
    android:name="androidx.startup.InitializationProvider"
    android:authorities="${applicationId}.androidx-startup"
    android:exported="false"
    tools:node="merge">

    <meta-data
        android:name="com.example.app.TimberInitializer"
        android:value="androidx.startup" />
    <meta-data
        android:name="com.example.app.KoinInitializer"
        android:value="androidx.startup" />
    <meta-data
        android:name="com.example.app.AnalyticsInitializer"
        android:value="androidx.startup" />
</provider>
```

### Lazy initialization

Omit a component from the manifest and initialize it on first use:

```kotlin
// In manifest: no <meta-data> entry for HeavySdkInitializer

// Wherever the SDK is first needed
AppInitializer.getInstance(context)
    .initializeComponent(HeavySdkInitializer::class.java)
```

This is ideal for SDKs needed only in specific features (e.g., a map SDK used only on the map screen).

### Disabling an auto-start initializer from a library

If a third-party library ships its own `Initializer` and you want to control timing:

```xml
<provider
    android:name="androidx.startup.InitializationProvider"
    android:authorities="${applicationId}.androidx-startup"
    android:exported="false"
    tools:node="merge">
    <meta-data
        android:name="com.thirdparty.HeavySdkInitializer"
        tools:node="remove" />
</provider>
```

---

## SplashScreen API (Android 12+)

The `SplashScreen` API is mandatory on Android 12+. The old `windowBackground` theme trick still works as a fallback for older versions.

### Dependency

```kotlin
implementation("androidx.core:core-splashscreen:1.0.1")
```

### Theme setup

```xml
<!-- res/values/themes.xml -->
<style name="Theme.App.Starting" parent="Theme.SplashScreen">
    <item name="windowSplashScreenBackground">@color/splash_background</item>
    <item name="windowSplashScreenAnimatedIcon">@drawable/ic_splash_animated</item>
    <item name="windowSplashScreenAnimationDuration">500</item>
    <item name="postSplashScreenTheme">@style/Theme.App</item>
</style>
```

```xml
<!-- AndroidManifest.xml -->
<activity
    android:name=".MainActivity"
    android:theme="@style/Theme.App.Starting" />
```

### MainActivity — install the splash screen

Call `installSplashScreen()` **before** `setContent`, and before `super.onCreate()` is not required but must precede any content inflation:

```kotlin
class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        val splashScreen = installSplashScreen()
        super.onCreate(savedInstanceState)

        // Keep splash visible while async startup data is loading
        var keepSplash = true
        splashScreen.setKeepOnScreenCondition { keepSplash }

        lifecycleScope.launch {
            // Load session, remote config, etc.
            delay(0) // yield to ensure first frame draws before this runs
            authViewModel.sessionState.first { it != SessionState.Loading }
            keepSplash = false
        }

        setContent {
            AppTheme {
                AppNavHost()
            }
        }
    }
}
```

Anti-pattern: blocking `onCreate()` with `runBlocking` while waiting for data. Use `setKeepOnScreenCondition` instead — it keeps the splash on screen without blocking the main thread.

### Animated splash icon

The animated icon must be an `AnimatedVectorDrawable` and comply with the system-imposed constraints:
- icon size: 108dp × 108dp (with 72dp visible area)
- animation will be cut off after 1000ms on Android 12

```xml
<!-- res/drawable/ic_splash_animated.xml -->
<animated-vector xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:aapt="http://schemas.android.com/aapt">
    <aapt:attr name="android:drawable">
        <vector android:width="108dp" android:height="108dp" android:viewportWidth="108"
            android:viewportHeight="108">
            <path android:name="logo" android:pathData="..." android:fillColor="#FFFFFF"/>
        </vector>
    </aapt:attr>
    <target android:name="logo">
        <aapt:attr name="android:animation">
            <objectAnimator android:propertyName="fillAlpha"
                android:duration="500" android:valueFrom="0" android:valueTo="1" />
        </aapt:attr>
    </target>
</animated-vector>
```

---

## Baseline Profiles

Baseline Profiles tell the Android runtime which classes and methods to AOT-compile at install time, reducing interpreted/JIT overhead during cold start and critical user journeys.

### Modules

```kotlin
// settings.gradle.kts
include(":app")
include(":baselineprofile")   // new module
```

```kotlin
// baselineprofile/build.gradle.kts
plugins {
    id("androidx.baselineprofile")
}

android {
    targetProjectPath = ":app"
    testOptions.managedDevices.devices {
        create<ManagedVirtualDevice>("pixel6Api34") {
            device = "Pixel 6"
            apiLevel = 34
            systemImageSource = "aosp"
        }
    }
}

dependencies {
    implementation(libs.androidx.test.ext.junit)
    implementation(libs.androidx.test.espresso.core)
    implementation(libs.androidx.benchmark.macro.junit4)
}
```

### Writing a Baseline Profile generator

```kotlin
// baselineprofile/src/androidTest/.../BaselineProfileGenerator.kt
@RunWith(AndroidJUnit4::class)
class BaselineProfileGenerator {

    @get:Rule
    val baselineProfileRule = BaselineProfileRule()

    @Test
    fun startup() = baselineProfileRule.collect(
        packageName = "com.example.app"
    ) {
        pressHome()
        startActivityAndWait()
    }

    @Test
    fun criticalUserJourney_openNotesList() = baselineProfileRule.collect(
        packageName = "com.example.app"
    ) {
        pressHome()
        startActivityAndWait()
        device.findObject(By.res("notes_list")).wait(Until.hasObject(By.res("note_item")), 5_000)
    }
}
```

### Generating and committing the profile

```bash
./gradlew :baselineprofile:generateBaselineProfile
# Outputs: app/src/main/baseline-prof.txt
```

Commit `baseline-prof.txt` to source control. It is applied at install time via `profileinstaller`.

### profileinstaller dependency

```kotlin
// app/build.gradle.kts
dependencies {
    implementation("androidx.profileinstaller:profileinstaller:1.3.1")
}
```

No code needed — profileinstaller automatically applies the profile from `baseline-prof.txt` on install.

### When to regenerate

- Before every release
- After adding new features to critical user journeys
- After significant navigation or startup logic changes

---

## Cold Start Checklist

### Setup

- [ ] StrictMode enabled in debug builds — fix all violations before release
- [ ] App Startup library adopted; `Application.onCreate()` has no direct SDK inits

### Main thread hygiene

- [ ] No disk reads/writes on main thread during startup
- [ ] No network calls on main thread during startup
- [ ] No `runBlocking` or `Thread.sleep` on main thread
- [ ] No synchronous `SharedPreferences` reads in `Application.onCreate()` — migrate to DataStore (see **android-datastore-preferences**)

### Deferred work

- [ ] Third-party SDKs not needed for first frame are lazy-loaded via App Startup
- [ ] Heavy database initialization happens off main thread (Room uses a background thread by default)
- [ ] Analytics/crash SDK init is fast; heavy remote config fetch is deferred

### SplashScreen

- [ ] `installSplashScreen()` called before `setContent()`
- [ ] `setKeepOnScreenCondition` used for async data, not `runBlocking`
- [ ] Animated icon is an `AnimatedVectorDrawable` within size constraints
- [ ] `postSplashScreenTheme` correctly set to the real app theme

### Baseline Profiles

- [ ] `BaselineProfileGenerator` covers cold start and top user journeys
- [ ] `baseline-prof.txt` committed to source control
- [ ] `profileinstaller` dependency added to `:app`
- [ ] Profile regenerated before each release

---

## Measuring Startup Time

Use Macrobenchmark to get objective startup numbers:

```kotlin
@RunWith(AndroidJUnit4::class)
class StartupBenchmark {

    @get:Rule
    val benchmarkRule = MacrobenchmarkRule()

    @Test
    fun coldStartup() = benchmarkRule.measureRepeated(
        packageName = "com.example.app",
        metrics = listOf(StartupTimingMetric()),
        iterations = 5,
        startupMode = StartupMode.COLD
    ) {
        pressHome()
        startActivityAndWait()
    }
}
```

Target: `timeToInitialDisplay` < 500ms on a mid-range device. Investigate any regression above that threshold before merging.

Also check **android-performance-profiling** for systrace and frame timing analysis.
