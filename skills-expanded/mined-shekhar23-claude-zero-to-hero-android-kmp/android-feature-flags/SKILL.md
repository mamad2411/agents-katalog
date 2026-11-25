---
name: android-feature-flags
description: |
  Feature flag patterns for Android - typed local flags with DataStore persistence, Firebase Remote Config fetch/activate lifecycle, wrapping remote config behind a FeatureFlagRepository interface, flag-gated navigation, environment-specific defaults, A/B testing user bucketing with exposure logging, and flag lifecycle naming conventions to prevent sprawl. Use this skill whenever adding feature toggles, kill switches, remote experiments, or A/B tests. Trigger on phrases like "feature flag", "remote config", "Firebase Remote Config", "A/B test", "feature toggle", "kill switch", "flag-gated", or "experiment".
---

# Android Feature Flags

## Core Principles

- Flags are temporary by default — every flag should have a defined retirement path.
- The domain layer knows about flag values but never about Remote Config, Firebase, or DataStore.
- Local flags are the floor; remote flags override them.
- Never gate safety-critical behavior behind a remote flag with no safe default.
- Exposure events must be logged at the moment the user is bucketed, not when they convert.

---

## Flag Types

| Type | Source | Typical use |
|---|---|---|
| Local static | Hardcoded constant | Dev builds, test seams |
| Local persisted | DataStore | Sideloaded overrides, offline defaults |
| Remote | Firebase Remote Config | Server-controlled rollouts, A/B tests |

All three should conform to the same `FeatureFlagRepository` interface.

---

## Typed Flag Model

Use a sealed interface or enum so flags are always exhaustive and refactor-safe:

```kotlin
sealed interface FeatureFlag {
    // Boolean flags
    data object NewCheckoutFlow : FeatureFlag
    data object OfflineMode : FeatureFlag

    // String/variant flags
    data object OnboardingVariant : FeatureFlag
    data object HomeFeedLayout : FeatureFlag
}

// Typed value wrappers
sealed interface FlagValue {
    data class Bool(val value: Boolean) : FlagValue
    data class Str(val value: String) : FlagValue
    data class Num(val value: Long) : FlagValue
}
```

Avoid stringly-typed flag name lookups outside the data layer — callers should reference `FeatureFlag.NewCheckoutFlow`, not the string `"new_checkout_flow"`.

---

## FeatureFlagRepository Interface

```kotlin
interface FeatureFlagRepository {
    suspend fun getBool(flag: FeatureFlag, default: Boolean = false): Boolean
    suspend fun getString(flag: FeatureFlag, default: String = ""): String
    suspend fun getLong(flag: FeatureFlag, default: Long = 0L): Long
    fun observe(flag: FeatureFlag): Flow<FlagValue>
}
```

The domain and presentation layers depend only on this interface. The data layer provides the implementation backed by Remote Config, DataStore, or both.

---

## Local Feature Flags with DataStore

Use DataStore for local flag overrides (useful for QA, debug menus, and offline defaults). See **android-datastore-preferences** for general DataStore patterns.

```kotlin
class LocalFeatureFlagDataSource(
    private val dataStore: DataStore<Preferences>
) {
    suspend fun setOverride(flag: FeatureFlag, value: FlagValue) {
        dataStore.edit { prefs ->
            prefs[flag.preferencesKey()] = value.serialize()
        }
    }

    fun observe(flag: FeatureFlag): Flow<FlagValue?> = dataStore.data.map { prefs ->
        prefs[flag.preferencesKey()]?.deserialize()
    }

    suspend fun clearOverride(flag: FeatureFlag) {
        dataStore.edit { prefs -> prefs.remove(flag.preferencesKey()) }
    }
}

// Extension to derive a DataStore key from the flag type
private fun FeatureFlag.preferencesKey(): Preferences.Key<String> =
    stringPreferencesKey("flag_override_${this::class.simpleName}")
```

Local overrides take precedence over remote values. Use them to unblock QA testing of features not yet fully rolled out remotely.

---

## Firebase Remote Config: Defaults XML

Always declare defaults in `res/xml/remote_config_defaults.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<defaultsMap>
    <entry>
        <key>new_checkout_flow</key>
        <value>false</value>
    </entry>
    <entry>
        <key>offline_mode</key>
        <value>false</value>
    </entry>
    <entry>
        <key>onboarding_variant</key>
        <value>control</value>
    </entry>
    <entry>
        <key>home_feed_layout</key>
        <value>grid</value>
    </entry>
</defaultsMap>
```

The defaults file ensures flags work correctly even before the first successful fetch. Never ship a flag without a default.

---

## Firebase Remote Config: Fetch and Activate

```kotlin
class RemoteConfigDataSource(
    private val remoteConfig: FirebaseRemoteConfig
) {
    suspend fun initialize() {
        remoteConfig.setDefaultsAsync(R.xml.remote_config_defaults).await()
        fetchAndActivate()
    }

    suspend fun fetchAndActivate(): Boolean {
        return try {
            remoteConfig.fetchAndActivate().await()
        } catch (e: Exception) {
            // Fetch failed — defaults or last cached values remain active
            false
        }
    }

    fun getBool(key: String, default: Boolean): Boolean =
        remoteConfig.getBoolean(key)

    fun getString(key: String, default: String): String =
        remoteConfig.getString(key).ifEmpty { default }

    fun getLong(key: String, default: Long): Long =
        remoteConfig.getLong(key)
}
```

### Minimum Fetch Interval

```kotlin
val configSettings = remoteConfigSettings {
    minimumFetchIntervalInSeconds = if (BuildConfig.DEBUG) 0 else 3600
}
remoteConfig.setConfigSettingsAsync(configSettings)
```

Set interval to `0` in debug builds so QA can test flag changes immediately. Production default is 12 hours but 1 hour is appropriate for active rollouts.

**Do not** call `fetchAndActivate` on every screen entry — it is rate-limited and adds startup latency.

---

## Composing Local + Remote Config

A production `FeatureFlagRepository` checks local overrides first, falls back to remote:

```kotlin
class FeatureFlagRepositoryImpl(
    private val remoteConfig: RemoteConfigDataSource,
    private val localOverrides: LocalFeatureFlagDataSource
) : FeatureFlagRepository {

    override suspend fun getBool(flag: FeatureFlag, default: Boolean): Boolean {
        val override = localOverrides.observe(flag).firstOrNull()
        if (override is FlagValue.Bool) return override.value
        return remoteConfig.getBool(flag.remoteKey(), default)
    }

    override suspend fun getString(flag: FeatureFlag, default: String): String {
        val override = localOverrides.observe(flag).firstOrNull()
        if (override is FlagValue.Str) return override.value
        return remoteConfig.getString(flag.remoteKey(), default)
    }

    override fun observe(flag: FeatureFlag): Flow<FlagValue> = localOverrides
        .observe(flag)
        .map { localValue ->
            localValue ?: FlagValue.Bool(remoteConfig.getBool(flag.remoteKey(), false))
        }
        .distinctUntilChanged()
}

private fun FeatureFlag.remoteKey(): String = when (this) {
    FeatureFlag.NewCheckoutFlow -> "new_checkout_flow"
    FeatureFlag.OfflineMode -> "offline_mode"
    FeatureFlag.OnboardingVariant -> "onboarding_variant"
    FeatureFlag.HomeFeedLayout -> "home_feed_layout"
}
```

---

## Environment-Specific Defaults

Define defaults per build type to avoid accidentally enabling in-progress features in production:

```kotlin
object FeatureFlagDefaults {
    val bool: Map<FeatureFlag, Boolean> = mapOf(
        FeatureFlag.NewCheckoutFlow to BuildConfig.DEBUG,  // on in debug, off in release
        FeatureFlag.OfflineMode to false,
        FeatureFlag.OnboardingVariant to false
    )
}
```

Use a `BuildConfig` constant or a Gradle-generated value — not a hardcoded `if (debug)` check scattered through feature code.

---

## Flag-Gated Navigation

Check flag values before navigating to a destination. Keep flag checks in the `ViewModel`, not inside composables:

```kotlin
class HomeViewModel(
    private val flags: FeatureFlagRepository
) : ViewModel() {

    fun onCheckoutClick() {
        viewModelScope.launch {
            val useNewFlow = flags.getBool(FeatureFlag.NewCheckoutFlow, default = false)
            val event = if (useNewFlow) {
                HomeEvent.NavigateTo(Destination.NewCheckout)
            } else {
                HomeEvent.NavigateTo(Destination.LegacyCheckout)
            }
            _events.send(event)
        }
    }
}
```

Do not gate routes directly inside `NavHost` blocks — keep navigation logic in the `ViewModel` and emit typed events. See **android-navigation** for typed destination patterns.

---

## A/B Testing: Bucketing and Exposure Events

A/B bucketing happens on the server (Remote Config or your own experiment service). The client's job is:
1. Read the assigned variant.
2. Log an exposure event immediately when the user is shown the variant.
3. Log conversion events separately.

```kotlin
class OnboardingViewModel(
    private val flags: FeatureFlagRepository,
    private val analytics: AnalyticsTracker
) : ViewModel() {

    private var exposureLogged = false

    fun loadVariant() {
        viewModelScope.launch {
            val variant = flags.getString(FeatureFlag.OnboardingVariant, default = "control")
            if (!exposureLogged) {
                analytics.track(
                    AnalyticsEvent(
                        name = "experiment_exposure",
                        properties = mapOf(
                            "experiment" to "onboarding_variant",
                            "variant" to variant
                        )
                    )
                )
                exposureLogged = true
            }
            _state.update { it.copy(variant = variant) }
        }
    }
}
```

Log the exposure exactly once per session per experiment — not on every recomposition. See **android-analytics-logging** for event design and tracker patterns.

---

## Debug Flag Override Screen

Expose a debug menu in non-production builds for QA to flip flags without code changes:

```kotlin
@Composable
fun DebugFlagScreen(
    viewModel: DebugFlagViewModel = koinViewModel()
) {
    val flags by viewModel.flags.collectAsStateWithLifecycle()
    LazyColumn {
        items(flags) { (flag, value) ->
            FlagToggleRow(
                label = flag::class.simpleName.orEmpty(),
                value = value,
                onToggle = { viewModel.toggleFlag(flag) }
            )
        }
    }
}
```

Gate the debug screen with `if (BuildConfig.DEBUG)` at the nav graph level.

---

## Flag Lifecycle and Naming Conventions

### Naming

Use the pattern `<area>_<feature>_<state>`:
- `checkout_new_flow_enabled`
- `home_feed_layout` (enum variant)
- `auth_biometric_prompt_enabled`

Avoid generic names like `feature_1`, `experiment_a`, `new_thing`.

### Lifecycle Stages

```
add → active → mature → retired
```

- **add**: flag created, default off, under development.
- **active**: flag enabled for some or all users via rollout.
- **mature**: flag fully rolled out; all users on new behavior.
- **retired**: old code path deleted, flag removed from code and Remote Config.

When a flag reaches **mature**, file a ticket to remove the old code path within one sprint. Flag sprawl makes code unreadable and tests expensive.

---

## Anti-Patterns

- Reading flags directly in composables with `LaunchedEffect` — keep flag reads in the `ViewModel`.
- Creating a `RemoteConfig` singleton not wrapped by `FeatureFlagRepository` — other layers take on Firebase coupling.
- Using Remote Config to store sensitive data (API keys, secrets) — Remote Config values are client-readable.
- Never retiring flags — code accumulates dead branches that are never exercised.
- Logging exposure events on conversion (purchase, signup) instead of on first view — skews experiment results by excluding non-converting users.
- Defaulting all flags to `true` in debug and `false` in release — some flags should default to `false` everywhere until specifically enabled.
- Calling `fetchAndActivate` inside a `ViewModel` on every creation — rate-limited and adds cold start latency; call it once during app startup.

---

## Testing Guidance

Use a `FakeFeatureFlagRepository` in all unit and integration tests:

```kotlin
class FakeFeatureFlagRepository : FeatureFlagRepository {
    private val boolOverrides = mutableMapOf<FeatureFlag, Boolean>()
    private val stringOverrides = mutableMapOf<FeatureFlag, String>()

    fun setFlag(flag: FeatureFlag, value: Boolean) { boolOverrides[flag] = value }
    fun setFlag(flag: FeatureFlag, value: String) { stringOverrides[flag] = value }

    override suspend fun getBool(flag: FeatureFlag, default: Boolean): Boolean =
        boolOverrides[flag] ?: default

    override suspend fun getString(flag: FeatureFlag, default: String): String =
        stringOverrides[flag] ?: default

    override suspend fun getLong(flag: FeatureFlag, default: Long): Long = default
    override fun observe(flag: FeatureFlag): Flow<FlagValue> =
        flowOf(FlagValue.Bool(boolOverrides[flag] ?: false))
}
```

Test both the flag-on and flag-off paths for every gated code path:

```kotlin
@Test
fun `new checkout shown when flag enabled`() = runTest {
    fakeFlags.setFlag(FeatureFlag.NewCheckoutFlow, true)
    viewModel.onCheckoutClick()
    assertThat(viewModel.events.first()).isEqualTo(HomeEvent.NavigateTo(Destination.NewCheckout))
}

@Test
fun `legacy checkout shown when flag disabled`() = runTest {
    fakeFlags.setFlag(FeatureFlag.NewCheckoutFlow, false)
    viewModel.onCheckoutClick()
    assertThat(viewModel.events.first()).isEqualTo(HomeEvent.NavigateTo(Destination.LegacyCheckout))
}
```

---

## Checklist: Adding a Feature Flag

- [ ] Add the flag to the `FeatureFlag` sealed interface
- [ ] Add a default to `remote_config_defaults.xml`
- [ ] Define environment-specific defaults in `FeatureFlagDefaults`
- [ ] Map the flag to its Remote Config key in `remoteKey()`
- [ ] Keep flag reads in the `ViewModel`, not in composables
- [ ] Log an exposure event once when the user is bucketed
- [ ] Write tests for both flag-on and flag-off states
- [ ] Add a retirement ticket when the flag reaches full rollout
