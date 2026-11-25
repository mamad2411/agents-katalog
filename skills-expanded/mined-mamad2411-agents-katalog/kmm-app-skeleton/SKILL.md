---
name: kmm-app-skeleton
description: Authoritative blueprint for scaffolding a brand-new Kotlin Multiplatform Mobile project with this project's conventions. Used by /init-kmm-app. Contains every file template, placeholder list, feature-flag block, and the procedure to emit runnable splash screens on Android (Compose) and iOS (SwiftUI).
---

# KMM app skeleton

Template registry consumed by `/init-kmm-app`. Substitute placeholders; do not improvise.

## Placeholders

| Placeholder | Meaning | Example |
|---|---|---|
| `{{APP_NAME}}` | Gradle + iOS target name | `MyApp` |
| `{{PACKAGE_ID}}` | Root package / applicationId | `com.example.myapp` |
| `{{PACKAGE_PATH}}` | Slash form of package id | `com/example/myapp` |
| `{{APP_DISPLAY_NAME}}` | Human-facing name | `My App` |
| `{{IOS_MIN}}` | iOS deployment target | `18.0` |

## Feature flags

| Flag | Adds |
|---|---|
| `INCLUDE_SQLDELIGHT` | `:shared` SQLDelight config, `.sq` file, drivers per platform, repository wrapper |
| `INCLUDE_FIREBASE` | Per-platform Crashlytics/Analytics behind a common interface |
| `IOS_DIST_DIRECT` | `embedAndSignAppleFrameworkForXcode` wiring |
| `IOS_DIST_COCOAPODS` | `kotlin.native.cocoapods` block + `Podfile` |
| `IOS_DIST_SPM` | XCFramework packaging task |

## Execution order

1. Create `{{APP_NAME}}/`.
2. Write root Gradle files.
3. Write `:shared` module.
4. Write `:androidApp` module.
5. Write `iosApp/` directory (SwiftUI + Xcode).
6. Write tests.
7. Build + test.
8. Emit manual setup notes.

---

## Root files

### `settings.gradle.kts`

```kts
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "{{APP_NAME}}"

include(":shared")
include(":androidApp")
```

### `build.gradle.kts` (root)

```kts
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.android.library) apply false
    alias(libs.plugins.kotlin.multiplatform) apply false
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.kotlin.serialization) apply false
    // INCLUDE_SQLDELIGHT: alias(libs.plugins.sqldelight) apply false
    // IOS_DIST_COCOAPODS: alias(libs.plugins.kotlin.cocoapods) apply false
}
```

### `gradle.properties`

```properties
org.gradle.jvmargs=-Xmx4g -Dfile.encoding=UTF-8
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.configuration-cache=true
kotlin.code.style=official
android.useAndroidX=true
android.nonTransitiveRClass=true
kotlin.mpp.stability.nowarn=true
```

### `gradle/libs.versions.toml`

**Do not copy the version strings below verbatim.** The `[versions]` block below shows the *shape* — which version refs the scaffold uses. When generating the file for a new project, resolve each version to the latest stable that satisfies the floor-constraint table after the TOML, then write those into the file.

If a resolved version falls below its listed floor, stop and surface the blocker rather than silently downgrading the template.

```toml
[versions]
agp = "<latest-stable>"
kotlin = "<latest-stable>"
coroutines = "<latest-stable>"
serialization = "<latest-stable>"
ktor = "<latest-stable>"
koin = "<latest-stable>"
sqldelight = "<latest-stable>"
multiplatform-settings = "<latest-stable>"
compose-bom = "<latest-stable>"
activity-compose = "<latest-stable>"
lifecycle = "<latest-stable>"
junit = "<latest-stable>"

[libraries]
kotlinx-coroutines-core = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-core", version.ref = "coroutines" }
kotlinx-coroutines-android = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-android", version.ref = "coroutines" }
kotlinx-coroutines-test = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-test", version.ref = "coroutines" }
kotlinx-serialization-json = { module = "org.jetbrains.kotlinx:kotlinx-serialization-json", version.ref = "serialization" }

ktor-client-core = { module = "io.ktor:ktor-client-core", version.ref = "ktor" }
ktor-client-content-negotiation = { module = "io.ktor:ktor-client-content-negotiation", version.ref = "ktor" }
ktor-client-logging = { module = "io.ktor:ktor-client-logging", version.ref = "ktor" }
ktor-serialization-kotlinx-json = { module = "io.ktor:ktor-serialization-kotlinx-json", version.ref = "ktor" }
ktor-client-okhttp = { module = "io.ktor:ktor-client-okhttp", version.ref = "ktor" }
ktor-client-darwin = { module = "io.ktor:ktor-client-darwin", version.ref = "ktor" }
ktor-client-mock = { module = "io.ktor:ktor-client-mock", version.ref = "ktor" }

koin-core = { module = "io.insert-koin:koin-core", version.ref = "koin" }
koin-android = { module = "io.insert-koin:koin-android", version.ref = "koin" }
koin-compose = { module = "io.insert-koin:koin-androidx-compose", version.ref = "koin" }

# INCLUDE_SQLDELIGHT
sqldelight-runtime = { module = "app.cash.sqldelight:runtime", version.ref = "sqldelight" }
sqldelight-coroutines = { module = "app.cash.sqldelight:coroutines-extensions", version.ref = "sqldelight" }
sqldelight-android = { module = "app.cash.sqldelight:android-driver", version.ref = "sqldelight" }
sqldelight-native = { module = "app.cash.sqldelight:native-driver", version.ref = "sqldelight" }

multiplatform-settings = { module = "com.russhwolf:multiplatform-settings", version.ref = "multiplatform-settings" }
multiplatform-settings-no-arg = { module = "com.russhwolf:multiplatform-settings-no-arg", version.ref = "multiplatform-settings" }

androidx-activity-compose = { module = "androidx.activity:activity-compose", version.ref = "activity-compose" }
androidx-lifecycle-runtime-ktx = { module = "androidx.lifecycle:lifecycle-runtime-ktx", version.ref = "lifecycle" }
compose-bom = { module = "androidx.compose:compose-bom", version.ref = "compose-bom" }
compose-ui = { module = "androidx.compose.ui:ui" }
compose-material3 = { module = "androidx.compose.material3:material3" }
compose-tooling-preview = { module = "androidx.compose.ui:ui-tooling-preview" }
compose-tooling = { module = "androidx.compose.ui:ui-tooling" }

junit = { module = "junit:junit", version.ref = "junit" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
android-library = { id = "com.android.library", version.ref = "agp" }
kotlin-multiplatform = { id = "org.jetbrains.kotlin.multiplatform", version.ref = "kotlin" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
kotlin-cocoapods = { id = "org.jetbrains.kotlin.native.cocoapods", version.ref = "kotlin" }
sqldelight = { id = "app.cash.sqldelight", version.ref = "sqldelight" }
```

**Floor constraints (enforce before writing the file):**

| Ref | Floor | Reason |
|---|---|---|
| `agp` | `>= 8.5.0` | KMP targets + K2 assume AGP 8.5+. |
| `kotlin` | `>= 2.0.0` | K2 compiler, default-hierarchy source sets the skill uses, and Koin 4.x ABI. |
| `ktor` | `>= 3.0.0` | v3 ContentNegotiation / MockEngine API that every networking example in the skill uses; v2 has a different DSL. |
| `koin` | `>= 4.0.0` | `expect val platformModule` / `KoinAppDeclaration` patterns the skill and scaffold both rely on. Koin 3.x → 4.x is a breaking bump (`/upgrade-deps` already flags it). |
| `sqldelight` | `>= 2.0.0` | Gradle plugin DSL (`databases { create(...) {} }`) used in `:shared/build.gradle.kts` only exists in 2.x. |
| `coroutines` | `>= 1.8.0` | Structured cancellation guarantees + `kotlinx-coroutines-test` `runTest { }` semantics. |
| `multiplatform-settings` | `>= 1.2.0` | `no-arg` artifact the KMM skill pairs with Koin. |

---

## `:shared` module

### `shared/build.gradle.kts`

```kts
plugins {
    alias(libs.plugins.kotlin.multiplatform)
    alias(libs.plugins.android.library)
    alias(libs.plugins.kotlin.serialization)
    // INCLUDE_SQLDELIGHT: alias(libs.plugins.sqldelight)
    // IOS_DIST_COCOAPODS: alias(libs.plugins.kotlin.cocoapods)
}

kotlin {
    androidTarget {
        compilations.all {
            kotlinOptions { jvmTarget = "17" }
        }
    }

    // Apple targets
    iosX64()
    iosArm64()
    iosSimulatorArm64()

    // IOS_DIST_DIRECT: produces a framework bound by `embedAndSignAppleFrameworkForXcode` below.
    listOf(iosX64(), iosArm64(), iosSimulatorArm64()).forEach { target ->
        target.binaries.framework {
            baseName = "Shared"
            isStatic = true
        }
    }

    // IOS_DIST_COCOAPODS
    // cocoapods {
    //     summary = "Shared framework for {{APP_NAME}}"
    //     homepage = "https://example.invalid/"
    //     ios.deploymentTarget = "{{IOS_MIN}}"
    //     framework {
    //         baseName = "Shared"
    //         isStatic = true
    //     }
    // }

    sourceSets {
        commonMain.dependencies {
            implementation(libs.kotlinx.coroutines.core)
            implementation(libs.kotlinx.serialization.json)
            implementation(libs.ktor.client.core)
            implementation(libs.ktor.client.content.negotiation)
            implementation(libs.ktor.client.logging)
            implementation(libs.ktor.serialization.kotlinx.json)
            implementation(libs.koin.core)
            implementation(libs.multiplatform.settings)
            // INCLUDE_SQLDELIGHT:
            implementation(libs.sqldelight.runtime)
            implementation(libs.sqldelight.coroutines)
        }
        commonTest.dependencies {
            implementation(kotlin("test"))
            implementation(libs.kotlinx.coroutines.test)
            implementation(libs.ktor.client.mock)
        }
        androidMain.dependencies {
            implementation(libs.kotlinx.coroutines.android)
            implementation(libs.ktor.client.okhttp)
            implementation(libs.koin.android)
            // INCLUDE_SQLDELIGHT: implementation(libs.sqldelight.android)
        }
        iosMain.dependencies {
            implementation(libs.ktor.client.darwin)
            // INCLUDE_SQLDELIGHT: implementation(libs.sqldelight.native)
        }
    }
}

android {
    namespace = "{{PACKAGE_ID}}.shared"
    compileSdk = 35
    defaultConfig { minSdk = 26 }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

// INCLUDE_SQLDELIGHT:
// sqldelight {
//     databases {
//         create("AppDatabase") {
//             packageName.set("{{PACKAGE_ID}}.shared.db")
//             schemaOutputDirectory.set(file("src/commonMain/sqldelight/schemas"))
//             verifyMigrations.set(true)
//         }
//     }
// }
```

### `shared/src/commonMain/kotlin/{{PACKAGE_PATH}}/shared/domain/Outcome.kt`

```kotlin
package {{PACKAGE_ID}}.shared.domain

sealed interface Outcome<out T> {
    data class Success<T>(val value: T) : Outcome<T>
    data class Failure(val error: DomainError) : Outcome<Nothing>
}

inline fun <T, R> Outcome<T>.map(block: (T) -> R): Outcome<R> = when (this) {
    is Outcome.Success -> Outcome.Success(block(value))
    is Outcome.Failure -> this
}
```

### `shared/src/commonMain/kotlin/{{PACKAGE_PATH}}/shared/domain/DomainError.kt`

```kotlin
package {{PACKAGE_ID}}.shared.domain

sealed class DomainError {
    data object Network : DomainError()
    data object Unauthorized : DomainError()
    data object NotFound : DomainError()
    data class Server(val code: Int) : DomainError()
    data class Unknown(val message: String? = null) : DomainError()
}
```

### `shared/src/commonMain/kotlin/{{PACKAGE_PATH}}/shared/network/KtorClientFactory.kt`

```kotlin
package {{PACKAGE_ID}}.shared.network

import io.ktor.client.HttpClient
import io.ktor.client.engine.HttpClientEngine
import io.ktor.client.plugins.HttpTimeout
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.plugins.logging.Logging
import io.ktor.serialization.kotlinx.json.json
import kotlinx.serialization.json.Json

fun createHttpClient(engine: HttpClientEngine): HttpClient = HttpClient(engine) {
    install(ContentNegotiation) {
        json(Json { ignoreUnknownKeys = true; explicitNulls = false })
    }
    install(HttpTimeout) {
        requestTimeoutMillis = 30_000
        connectTimeoutMillis = 15_000
    }
    install(Logging)
}
```

### `shared/src/commonMain/kotlin/{{PACKAGE_PATH}}/shared/sample/SampleApi.kt`

```kotlin
package {{PACKAGE_ID}}.shared.sample

import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.request.get
import kotlinx.serialization.Serializable

@Serializable
data class SampleDto(val id: String, val label: String)

class SampleApi(private val client: HttpClient, private val baseUrl: String) {
    suspend fun list(): List<SampleDto> = client.get("$baseUrl/samples").body()
}
```

### `shared/src/commonMain/kotlin/{{PACKAGE_PATH}}/shared/sample/SampleRepository.kt`

```kotlin
package {{PACKAGE_ID}}.shared.sample

import {{PACKAGE_ID}}.shared.domain.DomainError
import {{PACKAGE_ID}}.shared.domain.Outcome

class SampleRepository(private val api: SampleApi) {
    suspend fun load(): Outcome<List<SampleDto>> = try {
        Outcome.Success(api.list())
    } catch (t: Throwable) {
        Outcome.Failure(DomainError.Unknown(t.message))
    }
}
```

### `shared/src/commonMain/kotlin/{{PACKAGE_PATH}}/shared/splash/SplashViewModel.kt`

```kotlin
package {{PACKAGE_ID}}.shared.splash

import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.receiveAsFlow

data class SplashUiState(val message: String = "{{APP_DISPLAY_NAME}}")
sealed interface SplashUiEvent { data object Continue : SplashUiEvent }

class SplashViewModel {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)
    private val _state = MutableStateFlow(SplashUiState())
    val state: StateFlow<SplashUiState> = _state.asStateFlow()

    private val _events = Channel<SplashUiEvent>(Channel.BUFFERED)
    val events = _events.receiveAsFlow()

    fun onClose() { scope.close() }
}

private fun CoroutineScope.close() { kotlinx.coroutines.cancel() }
```

### `shared/src/commonMain/kotlin/{{PACKAGE_PATH}}/shared/di/Koin.kt`

```kotlin
package {{PACKAGE_ID}}.shared.di

import io.ktor.client.engine.HttpClientEngine
import org.koin.core.context.startKoin
import org.koin.dsl.KoinAppDeclaration
import org.koin.dsl.module
import {{PACKAGE_ID}}.shared.network.createHttpClient
import {{PACKAGE_ID}}.shared.sample.SampleApi
import {{PACKAGE_ID}}.shared.sample.SampleRepository
import {{PACKAGE_ID}}.shared.splash.SplashViewModel

fun initKoin(extra: KoinAppDeclaration = {}) = startKoin {
    extra()
    modules(sharedModule, platformModule)
}

private val sharedModule = module {
    single { createHttpClient(get()) }
    factory { (baseUrl: String) -> SampleApi(get(), baseUrl) }
    factory { SampleRepository(get { org.koin.core.parameter.parametersOf("https://example.invalid") }) }
    factory { SplashViewModel() }
}

expect val platformModule: org.koin.core.module.Module
```

### `shared/src/androidMain/kotlin/{{PACKAGE_PATH}}/shared/di/PlatformModule.kt`

```kotlin
package {{PACKAGE_ID}}.shared.di

import io.ktor.client.engine.okhttp.OkHttp
import org.koin.dsl.module

actual val platformModule = module {
    single<io.ktor.client.engine.HttpClientEngine> { OkHttp.create() }
}
```

### `shared/src/iosMain/kotlin/{{PACKAGE_PATH}}/shared/di/PlatformModule.kt`

```kotlin
package {{PACKAGE_ID}}.shared.di

import io.ktor.client.engine.darwin.Darwin
import org.koin.dsl.module

actual val platformModule = module {
    single<io.ktor.client.engine.HttpClientEngine> { Darwin.create() }
}
```

### `shared/src/commonTest/kotlin/{{PACKAGE_PATH}}/shared/sample/SampleRepositoryTest.kt`

```kotlin
package {{PACKAGE_ID}}.shared.sample

import io.ktor.client.HttpClient
import io.ktor.client.engine.mock.MockEngine
import io.ktor.client.engine.mock.respond
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.http.ContentType
import io.ktor.http.HttpStatusCode
import io.ktor.http.headersOf
import io.ktor.serialization.kotlinx.json.json
import io.ktor.utils.io.ByteReadChannel
import kotlinx.coroutines.test.runTest
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue
import {{PACKAGE_ID}}.shared.domain.Outcome

class SampleRepositoryTest {
    @Test
    fun `load returns parsed list`() = runTest {
        val engine = MockEngine { _ ->
            respond(
                content = ByteReadChannel("""[{"id":"a","label":"A"}]"""),
                status = HttpStatusCode.OK,
                headers = headersOf("Content-Type", "application/json"),
            )
        }
        val client = HttpClient(engine) {
            install(ContentNegotiation) { json() }
        }
        val api = SampleApi(client, "https://example.invalid")
        val repo = SampleRepository(api)
        val result = repo.load()
        assertTrue(result is Outcome.Success)
        assertEquals(1, result.value.size)
        assertEquals("A", result.value.first().label)
    }
}
```

---

## `:androidApp` module

### `androidApp/build.gradle.kts`

```kts
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
}

android {
    namespace = "{{PACKAGE_ID}}.android"
    compileSdk = 35
    defaultConfig {
        applicationId = "{{PACKAGE_ID}}"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "0.1.0"
    }
    buildFeatures { compose = true }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
}

dependencies {
    implementation(project(":shared"))
    implementation(libs.androidx.activity.compose)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(platform(libs.compose.bom))
    implementation(libs.compose.ui)
    implementation(libs.compose.material3)
    implementation(libs.compose.tooling.preview)
    debugImplementation(libs.compose.tooling)
    implementation(libs.koin.android)
    implementation(libs.koin.compose)
}
```

### `androidApp/src/main/AndroidManifest.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <application
        android:name=".MainApplication"
        android:allowBackup="false"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.App">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.App">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

### `androidApp/src/main/java/{{PACKAGE_PATH}}/android/MainApplication.kt`

```kotlin
package {{PACKAGE_ID}}.android

import android.app.Application
import org.koin.android.ext.koin.androidContext
import {{PACKAGE_ID}}.shared.di.initKoin
import {{PACKAGE_ID}}.shared.di.platformModule

class MainApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        initKoin {
            androidContext(this@MainApplication)
            modules(platformModule)
        }
    }
}
```

### `androidApp/src/main/java/{{PACKAGE_PATH}}/android/MainActivity.kt`

```kotlin
package {{PACKAGE_ID}}.android

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import org.koin.compose.koinInject
import {{PACKAGE_ID}}.shared.splash.SplashViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                val vm: SplashViewModel = koinInject()
                val state by vm.state.collectAsState()
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text(state.message)
                }
            }
        }
    }
}
```

### `androidApp/src/main/res/values/strings.xml`

```xml
<resources>
    <string name="app_name">{{APP_DISPLAY_NAME}}</string>
</resources>
```

### `androidApp/src/main/res/values/themes.xml`

```xml
<resources>
    <style name="Theme.App" parent="android:Theme.Material.Light.NoActionBar" />
</resources>
```

---

## `iosApp/`

SwiftUI app that consumes the `Shared` framework.

### `iosApp/{{APP_NAME}}/{{APP_NAME}}App.swift`

```swift
import SwiftUI
import Shared

@main
struct {{APP_NAME}}App: App {
    init() {
        KoinIOS.start()
    }

    var body: some Scene {
        WindowGroup {
            SplashView(viewModel: KoinIOS.splashViewModel())
        }
    }
}
```

### `iosApp/{{APP_NAME}}/KoinIOS.swift`

```swift
import Foundation
import Shared

enum KoinIOS {
    static func start() {
        let decl: (KoinAppDeclarationFunction)? = nil
        KoinKt.doInitKoin(extra: decl ?? { _ in })
    }

    static func splashViewModel() -> SplashViewModel {
        return SplashViewModel()
    }
}

typealias KoinAppDeclarationFunction = (KoinApplication) -> Void
```

### `iosApp/{{APP_NAME}}/SplashView.swift`

```swift
import SwiftUI
import Shared
import Combine

@MainActor
final class SplashObservable: ObservableObject {
    @Published var message: String = ""
    private let vm: SplashViewModel
    private var cancellable: AnyCancellable?

    init(_ vm: SplashViewModel) {
        self.vm = vm
        let flow = FlowWrapper<SplashUiState>(flow: vm.state)
        cancellable = flow.publisher.sink { [weak self] state in
            self?.message = state.message
        }
    }
}

struct SplashView: View {
    @StateObject private var state: SplashObservable

    init(viewModel: SplashViewModel) {
        _state = StateObject(wrappedValue: SplashObservable(viewModel))
    }

    var body: some View {
        Text(state.message)
            .font(.largeTitle)
            .bold()
    }
}
```

### `iosApp/{{APP_NAME}}/FlowWrapper.swift`

```swift
import Foundation
import Combine
import Shared

final class FlowWrapper<T: AnyObject> {
    let publisher = PassthroughSubject<T, Never>()
    private let flow: any Kotlinx_coroutines_coreStateFlow

    init(flow: any Kotlinx_coroutines_coreStateFlow) {
        self.flow = flow
        FlowKt.collect(flow: flow) { [weak self] value in
            if let typed = value as? T { self?.publisher.send(typed) }
        }
    }
}
```

*Note*: The exact `FlowWrapper` implementation depends on a small Kotlin bridge exported in `:shared` (`FlowKt.collect`). If you use `SKIE` or `KMP-NativeCoroutines`, replace this helper with the one that plugin emits. This skeleton keeps the bridge explicit.

### IOS_DIST_DIRECT — Xcode build phase

Add a Run Script phase before Compile Sources in the iosApp target:

```sh
cd "$SRCROOT/.."
./gradlew :shared:embedAndSignAppleFrameworkForXcode
```

And set in Build Settings:
- Framework Search Paths: `$(SRCROOT)/../shared/build/xcode-frameworks`
- Other Linker Flags: `-framework Shared`

### IOS_DIST_COCOAPODS — `Podfile`

```ruby
platform :ios, '{{IOS_MIN}}'
use_frameworks!

target '{{APP_NAME}}' do
  pod 'Shared', :path => '../shared'
end
```

### IOS_DIST_SPM — XCFramework task

```kts
tasks.register("packageXCFramework", org.jetbrains.kotlin.gradle.tasks.FatFrameworkTask::class.java) {
    baseName = "Shared"
    group = "build"
}
```

Recommend: use `XCFrameworkTask` for a real release artifact; wire it to a `releaseFramework` Gradle task.

---

## INCLUDE_SQLDELIGHT additions

### `shared/src/commonMain/sqldelight/{{PACKAGE_PATH}}/shared/db/Sample.sq`

```sql
CREATE TABLE Sample (
    id TEXT NOT NULL PRIMARY KEY,
    label TEXT NOT NULL
);

selectAll:
SELECT * FROM Sample;

upsert:
INSERT OR REPLACE INTO Sample (id, label) VALUES (?, ?);
```

### `shared/src/androidMain/kotlin/{{PACKAGE_PATH}}/shared/db/DriverFactory.kt`

```kotlin
package {{PACKAGE_ID}}.shared.db

import android.content.Context
import app.cash.sqldelight.db.SqlDriver
import app.cash.sqldelight.driver.android.AndroidSqliteDriver

actual class DriverFactory(private val context: Context) {
    actual fun create(): SqlDriver = AndroidSqliteDriver(AppDatabase.Schema, context, "app.db")
}
```

### `shared/src/iosMain/kotlin/{{PACKAGE_PATH}}/shared/db/DriverFactory.kt`

```kotlin
package {{PACKAGE_ID}}.shared.db

import app.cash.sqldelight.db.SqlDriver
import app.cash.sqldelight.driver.native.NativeSqliteDriver

actual class DriverFactory {
    actual fun create(): SqlDriver = NativeSqliteDriver(AppDatabase.Schema, "app.db")
}
```

### `shared/src/commonMain/kotlin/{{PACKAGE_PATH}}/shared/db/DriverFactory.kt`

```kotlin
package {{PACKAGE_ID}}.shared.db

import app.cash.sqldelight.db.SqlDriver

expect class DriverFactory {
    fun create(): SqlDriver
}
```

---

## Hard rules

- **SQLDelight** is the blessed persistence story. Do not add Room-KMP alongside it.
- **No platform imports in `commonMain`.** If you need one, use `expect/actual`.
- **`StateFlow` + `Channel`** is the shared view-model shape. UI-specific view models on each platform wrap the shared one.
- **Koin** for DI on both platforms. Android uses `initKoin { androidContext(this) }`, iOS uses `KoinIOS.start()`.
- **Ktor** everywhere. No Retrofit in `:shared` (Retrofit is JVM-only).
- **Version catalog** owns all versions.
- **`verifyMigrations = true`** once SQLDelight is enabled.
- **Forward-only migrations**. Never mutate shipped `.sq` or `.sqm` files.

## Post-scaffold manual steps

```
Scaffold complete. Next steps:

☐ [iOS] Open iosApp/{{APP_NAME}}.xcodeproj, set Team and Bundle ID.
☐ [iOS, direct mode] Confirm the Run Script phase runs `./gradlew :shared:embedAndSignAppleFrameworkForXcode` before Compile Sources.
☐ [iOS, CocoaPods] cd iosApp && pod install (requires `./gradlew :shared:podspec` first).
☐ [iOS, SPM] run `./gradlew :shared:packageXCFramework` and add the resulting XCFramework to the Xcode project.
☐ [SQLDelight] run `./gradlew :shared:generateSqlDelightInterface` and commit the initial schema snapshot.
☐ Replace Splash on both platforms with your first real feature.

Build it:
  ./gradlew :androidApp:assembleDebug
  ./gradlew :shared:allTests
  (Xcode) ⌘R on iosApp
```
