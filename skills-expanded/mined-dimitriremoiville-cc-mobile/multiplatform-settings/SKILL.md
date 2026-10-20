---
name: multiplatform-settings
description: `multiplatform-settings` patterns for this KMP project — observable / suspending settings, typed wrappers, platform constructors, migrations, security considerations (secrets do not belong here). Load whenever adding a shared key-value preference.
---

# multiplatform-settings

## What it is

Thin KMP key-value wrapper over platform-native storage:
- Android: `SharedPreferences` (or `DataStore` via no-arg coroutines module).
- iOS: `NSUserDefaults`.
- JVM: `java.util.prefs.Preferences`.
- JS: `Storage`.

It's the right tool for UI preferences. **Not** for tokens, credentials, or anything sensitive.

## Dependencies

In `libs.versions.toml` (resolve `<latest-stable>` to the newest non-alpha release at scaffold time):

```toml
[versions]
multiplatform-settings = "<latest-stable>"

[libraries]
multiplatform-settings = { module = "com.russhwolf:multiplatform-settings", version.ref = "multiplatform-settings" }
multiplatform-settings-coroutines = { module = "com.russhwolf:multiplatform-settings-coroutines", version.ref = "multiplatform-settings" }
```

```kotlin
kotlin {
    sourceSets {
        commonMain.dependencies {
            api(libs.multiplatform.settings)
            implementation(libs.multiplatform.settings.coroutines)
        }
    }
}
```

## Factory per platform

`expect class` in `commonMain`:

```kotlin
expect class SettingsFactory {
    fun create(name: String): Settings
}
```

`actual` in `androidMain`:

```kotlin
actual class SettingsFactory(private val context: Context) {
    actual fun create(name: String): Settings = SharedPreferencesSettings(
        context.getSharedPreferences(name, Context.MODE_PRIVATE)
    )
}
```

`actual` in `iosMain`:

```kotlin
actual class SettingsFactory {
    actual fun create(name: String): Settings = NSUserDefaultsSettings(
        NSUserDefaults(suiteName = name) ?: NSUserDefaults.standardUserDefaults
    )
}
```

Register in Koin:

```kotlin
val settingsModule = module {
    single { get<SettingsFactory>().create("app-prefs") }
    single<UserPreferences> { UserPreferencesImpl(get()) }
}
```

## Typed wrapper

Don't let callers pass raw keys around. One typed interface per concern:

```kotlin
interface UserPreferences {
    var theme: AppTheme
    fun themeFlow(): Flow<AppTheme>
    var hasCompletedOnboarding: Boolean
    fun clear()
}

class UserPreferencesImpl(private val settings: ObservableSettings) : UserPreferences {
    private object Keys {
        const val THEME = "theme"
        const val ONBOARDED = "has_completed_onboarding"
    }

    override var theme: AppTheme
        get() = settings.getStringOrNull(Keys.THEME)?.let(AppTheme::valueOf) ?: AppTheme.SYSTEM
        set(value) { settings[Keys.THEME] = value.name }

    override fun themeFlow(): Flow<AppTheme> =
        settings.getStringFlow(Keys.THEME, AppTheme.SYSTEM.name).map(AppTheme::valueOf)

    override var hasCompletedOnboarding: Boolean
        get() = settings.getBoolean(Keys.ONBOARDED, false)
        set(value) { settings[Keys.ONBOARDED] = value }

    override fun clear() = settings.clear()
}
```

Prefer `ObservableSettings` over `Settings` when you want Flow-backed observation (requires the `observable` artifact or the coroutines extensions).

## Serializable values

For enums, pack to string. For structured values, use `kotlinx.serialization`:

```kotlin
var draftOrder: DraftOrder?
    get() = settings.getStringOrNull(Keys.DRAFT)?.let { json.decodeFromString<DraftOrder>(it) }
    set(value) {
        if (value == null) settings.remove(Keys.DRAFT)
        else settings[Keys.DRAFT] = json.encodeToString(value)
    }
```

Keep the JSON stable — a schema change without a migration silently drops data.

## Observation

`ObservableSettings.getStringFlow(key, default)` emits the current value and every subsequent write. Works via `SharedPreferences.OnSharedPreferenceChangeListener` on Android and KVO on iOS.

For Settings factories without observation support, wrap with `ObservableSettings.Factory.create(settings)` or poll with `flow { while (true) { emit(...); delay(...) } }` — last resort.

## Migrations

Preferences don't self-migrate. Version them manually:

```kotlin
class PreferencesMigration(private val settings: Settings) {
    fun run() {
        val v = settings.getInt("prefs_version", 0)
        if (v < 1) migrateV0ToV1()
        settings["prefs_version"] = 1
    }

    private fun migrateV0ToV1() {
        settings.getStringOrNull("colour")?.let { settings["theme"] = it; settings.remove("colour") }
    }
}
```

Run at app startup before anyone reads. Ship the migration for one release, remove it the next.

## Secrets go elsewhere

- On Android: Keystore + `EncryptedSharedPreferences` or Tink.
- On iOS: Keychain.

`multiplatform-settings` writes plaintext; never use it for auth tokens or PII. A dedicated `expect interface SecureStore` lives alongside your settings wrapper for that.

## Testing

`MapSettings()` is an in-memory implementation that matches the `Settings` contract:

```kotlin
@Test fun themeRoundTrip() {
    val sut = UserPreferencesImpl(MapSettings().toObservableSettings())
    sut.theme = AppTheme.DARK
    assertEquals(AppTheme.DARK, sut.theme)
}
```

## Hard nos

- No storing tokens, passwords, or PII.
- No `Settings` instance reach-ins from the UI layer.
- No unversioned schema changes on structured values.
- No sharing a single `name` for unrelated concerns (use `app-prefs`, `feature-cart`, `onboarding` as separate factories).
- No direct `NSUserDefaults.standardUserDefaults` or `context.getSharedPreferences(...)` outside the `SettingsFactory`.
