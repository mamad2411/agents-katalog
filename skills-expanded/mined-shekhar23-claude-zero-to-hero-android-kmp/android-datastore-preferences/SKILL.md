---
name: android-datastore-preferences
description: |
  DataStore and preferences patterns for Android/KMP - user settings, typed preference models, serialization, migrations from SharedPreferences, corruption handling, and repository boundaries. Use this skill whenever storing app settings, feature flags, lightweight local state, or replacing SharedPreferences. Trigger on phrases like "DataStore", "preferences", "Proto DataStore", "settings", "user preferences", "SharedPreferences migration", or "local settings persistence".
---

# Android DataStore and Preferences

## Core Principles

- Use DataStore for small local settings and preference-like state.
- Do not use DataStore as a database or cache for large relational data.
- Persist only data that should survive process death and app restarts.
- Expose typed models to the rest of the app, not raw preference keys.
- Keep storage details inside the data layer.

---

## When to Use DataStore

Good fits:
- theme mode
- onboarding completed flag
- sort/filter preferences
- selected app language
- lightweight session-adjacent non-sensitive flags

Bad fits:
- large lists of entities
- search indexes
- offline sync source of truth
- highly relational or query-heavy data

Use Room for structured app data. See the **android-room-database** skill.

---

## Preferences vs Proto DataStore

| Need | Preferred option |
|---|---|
| Simple key/value settings | Preferences DataStore |
| Strong schema and typed persistence | Proto DataStore |
| Cross-team/shared contract that should evolve safely | Proto DataStore |

Default to Preferences DataStore unless the settings model is large enough or important enough to benefit from a defined schema.

---

## Module Ownership

Common placements:

```text
:core:data                  -> shared DataStore factory and generic helpers
:core:auth                  -> secure/session-adjacent non-token local state if needed
:feature:<name>:data        -> feature-specific preference repositories
```

If settings are shared app-wide, keep them in a shared core module. If they are feature-specific, keep them in that feature's `data` module.

---

## Preferences DataStore Example

```kotlin
class UserSettingsDataSource(
    private val dataStore: DataStore<Preferences>
) {
    suspend fun setDarkMode(enabled: Boolean) {
        dataStore.edit { prefs ->
            prefs[Keys.darkMode] = enabled
        }
    }

    fun observeSettings(): Flow<UserSettings> {
        return dataStore.data.map { prefs ->
            UserSettings(
                darkMode = prefs[Keys.darkMode] ?: false,
                dynamicColor = prefs[Keys.dynamicColor] ?: true
            )
        }
    }

    private object Keys {
        val darkMode = booleanPreferencesKey("dark_mode")
        val dynamicColor = booleanPreferencesKey("dynamic_color")
    }
}
```

Keep keys private to the data source.

---

## Typed Preference Model

Expose a typed domain or data model instead of multiple primitive flows:

```kotlin
data class UserSettings(
    val darkMode: Boolean = false,
    val dynamicColor: Boolean = true,
    val use24HourClock: Boolean = false
)
```

The `ViewModel` should observe one settings model and map it into screen state when needed.

---

## Proto DataStore Example

Use Proto DataStore when schema, defaults, and evolution matter:

```kotlin
class UserSettingsSerializer : Serializer<UserSettingsProto> {
    override val defaultValue: UserSettingsProto = UserSettingsProto.getDefaultInstance()

    override suspend fun readFrom(input: InputStream): UserSettingsProto {
        return try {
            UserSettingsProto.parseFrom(input)
        } catch (exception: InvalidProtocolBufferException) {
            throw CorruptionException("Cannot read proto.", exception)
        }
    }

    override suspend fun writeTo(t: UserSettingsProto, output: OutputStream) {
        t.writeTo(output)
    }
}
```

Prefer Proto when:
- multiple fields should evolve together
- defaults must be explicit and stable
- type safety matters more than setup simplicity

---

## Error and Corruption Handling

Handle corruption explicitly:

```kotlin
val Context.userSettingsDataStore by dataStore(
    fileName = "user_settings.pb",
    serializer = UserSettingsSerializer(),
    corruptionHandler = ReplaceFileCorruptionHandler {
        UserSettingsProto.getDefaultInstance()
    }
)
```

Rules:
- recover to safe defaults when corruption is acceptable
- avoid crashing the whole app for recoverable local settings corruption
- log corruption in a redaction-safe way

---

## SharedPreferences Migration

Migrate legacy preferences once:

```kotlin
val Context.settingsDataStore by preferencesDataStore(
    name = "settings",
    produceMigrations = { context ->
        listOf(SharedPreferencesMigration(context, "legacy_settings"))
    }
)
```

After migration:
- stop writing to SharedPreferences
- keep one source of truth only
- remove legacy access paths when safe

---

## Repository Pattern

Wrap DataStore behind a repository interface when presentation or domain consumes it:

```kotlin
interface SettingsRepository {
    fun observeSettings(): Flow<UserSettings>
    suspend fun setDarkMode(enabled: Boolean)
}
```

Implementation details stay in the data layer.

---

## Compose Usage

Collect settings in a `ViewModel`, not directly in screen composables:

```kotlin
val state by viewModel.state.collectAsStateWithLifecycle()
```

The `ViewModel` observes DataStore-backed flows and maps them into UI state. See the **android-presentation-mvi** and **android-coroutines-flow** skills.

---

## Security Boundary

DataStore is not a secure secret vault.

Do not store:
- passwords
- refresh tokens
- private keys
- highly sensitive credentials

For auth/session secret guidance, see the **android-auth-security** skill.

---

## Checklist: Adding DataStore

- [ ] Confirm the data is preference-like, not relational
- [ ] Choose Preferences or Proto DataStore intentionally
- [ ] Keep keys and serialization details in the data layer
- [ ] Expose a typed settings model
- [ ] Add corruption handling and migration if needed
- [ ] Avoid storing secrets in DataStore