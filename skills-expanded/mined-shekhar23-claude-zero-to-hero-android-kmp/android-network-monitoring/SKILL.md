---
name: android-network-monitoring
description: |
  Network connectivity monitoring for Android - ConnectivityManager with NetworkCallback, wrapping network state in a Flow, offline banner UI, network-aware retry, WiFi vs cellular detection, and fake NetworkMonitor for tests. Use this skill whenever detecting connectivity loss, showing an offline indicator, triggering re-fetch when connectivity returns, or gating downloads to WiFi. Trigger on phrases like "network monitor", "offline detection", "ConnectivityManager", "NetworkCallback", "connectivity", "offline banner", "no internet", "network state", "detect wifi", "connectivity change".
---

# Android Network Monitoring

## Overview

Real-time connectivity monitoring via `ConnectivityManager` and `NetworkCallback`. The key rule: **never poll** — use callbacks only. Wrap the result in a `Flow<Boolean>` behind a domain interface so ViewModels and Workers stay framework-free.

Related skills: `android-coroutines-flow`, `android-data-layer`, `android-workmanager`.

---

## Domain Interface

```kotlin
// domain layer — no Android imports
interface NetworkMonitor {
    val isOnline: Flow<Boolean>
}
```

---

## Implementation

```kotlin
// data layer
class AndroidNetworkMonitor(
    private val context: Context,
) : NetworkMonitor {

    override val isOnline: Flow<Boolean> = callbackFlow {
        val connectivityManager =
            context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager

        val callback = object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(network: Network) {
                trySend(true)
            }
            override fun onLost(network: Network) {
                trySend(false)
            }
            override fun onUnavailable() {
                trySend(false)
            }
        }

        val request = NetworkRequest.Builder()
            .addCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
            .addCapability(NetworkCapabilities.NET_CAPABILITY_VALIDATED)
            .build()

        connectivityManager.registerNetworkCallback(request, callback)

        // Emit the current state immediately on collection
        val currentlyConnected = connectivityManager.activeNetwork
            ?.let { connectivityManager.getNetworkCapabilities(it) }
            ?.hasCapability(NetworkCapabilities.NET_CAPABILITY_VALIDATED)
            ?: false
        trySend(currentlyConnected)

        awaitClose {
            connectivityManager.unregisterNetworkCallback(callback)
        }
    }.distinctUntilChanged()
}
```

Koin binding:
```kotlin
single<NetworkMonitor> { AndroidNetworkMonitor(androidContext()) }
```

---

## Sharing the Flow

Share the flow at the app level so all collectors get the same callback — don't create a new `callbackFlow` per subscriber.

```kotlin
// In Koin application-scoped module
single<NetworkMonitor> {
    object : NetworkMonitor {
        private val monitor = AndroidNetworkMonitor(androidContext())
        override val isOnline: Flow<Boolean> =
            monitor.isOnline.shareIn(
                scope = GlobalScope, // application-scoped — acceptable here
                started = SharingStarted.WhileSubscribed(5_000),
                replay = 1,
            )
    }
}
```

---

## Offline Banner in a ViewModel

```kotlin
data class MyScreenState(
    val items: List<Item> = emptyList(),
    val isOffline: Boolean = false,
    val isLoading: Boolean = false,
)

class MyViewModel(
    private val repository: ItemRepository,
    private val networkMonitor: NetworkMonitor,
) : ViewModel() {

    private val _state = MutableStateFlow(MyScreenState())
    val state: StateFlow<MyScreenState> = _state.asStateFlow()

    init {
        observeConnectivity()
        loadItems()
    }

    private fun observeConnectivity() {
        viewModelScope.launch {
            networkMonitor.isOnline.collect { online ->
                _state.update { it.copy(isOffline = !online) }
                if (online) loadItems() // re-fetch when connectivity returns
            }
        }
    }
}
```

---

## Offline Banner Composable

```kotlin
@Composable
fun OfflineBanner(isOffline: Boolean, modifier: Modifier = Modifier) {
    AnimatedVisibility(
        visible = isOffline,
        enter = slideInVertically() + fadeIn(),
        exit = slideOutVertically() + fadeOut(),
        modifier = modifier,
    ) {
        Surface(
            color = MaterialTheme.colorScheme.errorContainer,
            modifier = Modifier.fillMaxWidth(),
        ) {
            Text(
                text = stringResource(R.string.offline_banner),
                style = MaterialTheme.typography.labelMedium,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
            )
        }
    }
}
```

---

## Detecting WiFi vs Cellular

Gate large downloads or sync operations to WiFi only.

```kotlin
fun isOnWifi(context: Context): Boolean {
    val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
    val caps = cm.activeNetwork?.let { cm.getNetworkCapabilities(it) } ?: return false
    return caps.hasTransport(NetworkCapabilities.TRANSPORT_WIFI)
}
```

Or model it in the flow:

```kotlin
enum class ConnectionType { NONE, CELLULAR, WIFI, OTHER }

val connectionType: Flow<ConnectionType> = callbackFlow {
    // similar NetworkCallback implementation
    // check TRANSPORT_WIFI vs TRANSPORT_CELLULAR in onCapabilitiesChanged
}
```

---

## WorkManager Constraint

For background sync that requires network (see `android-workmanager`):

```kotlin
val constraints = Constraints.Builder()
    .setRequiredNetworkType(NetworkType.CONNECTED) // or UNMETERED for WiFi-only
    .build()
```

---

## Fake for Tests

```kotlin
class FakeNetworkMonitor(initiallyOnline: Boolean = true) : NetworkMonitor {
    private val _isOnline = MutableStateFlow(initiallyOnline)
    override val isOnline: Flow<Boolean> = _isOnline.asStateFlow()

    fun setOnline(value: Boolean) { _isOnline.value = value }
}

// In a test:
val monitor = FakeNetworkMonitor(initiallyOnline = false)
val viewModel = MyViewModel(fakeRepository, monitor)
monitor.setOnline(true)
// assert re-fetch triggered
```

---

## Anti-Patterns

| Anti-pattern | Why it's wrong | Instead |
|---|---|---|
| Polling with `delay` in a loop | Wastes battery, misses instant changes | Use `NetworkCallback` |
| Calling `activeNetworkInfo.isConnected` (deprecated) | Removed in API 29 | Use `NetworkCapabilities.NET_CAPABILITY_VALIDATED` |
| Checking connectivity before each network call | Race condition — state can change mid-request | Handle `IOException` / retry logic instead |
| Registering `NetworkCallback` in a ViewModel | Leaks if ViewModel outlives Activity context | Register in an application-scoped component |
| Not unregistering the callback | Leaks the callback registration | Always unregister in `awaitClose` or `onStop` |
