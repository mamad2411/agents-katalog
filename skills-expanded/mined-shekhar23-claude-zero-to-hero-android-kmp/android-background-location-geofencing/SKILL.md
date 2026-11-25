---
name: android-background-location-geofencing
description: |
  Background location and geofencing patterns for Android - FusedLocationProviderClient setup, foreground vs background location permission flows, foreground service for continuous tracking, GeofencingClient with broadcast receivers, battery-aware accuracy strategies, and graceful permission denial handling. Use this skill whenever implementing continuous location tracking, geofence entry/exit events, or any feature requiring ACCESS_BACKGROUND_LOCATION. Trigger on phrases like "background location", "geofence", "location tracking", "FusedLocationProvider", "ACCESS_BACKGROUND_LOCATION", "location foreground service", or "track location".
---

# Android Background Location and Geofencing

## Core Principles

- Foreground location and background location are separate permission tiers — request them independently and in sequence.
- Continuous tracking requires a Foreground Service with `foregroundServiceType="location"`.
- Geofences are battery-efficient; prefer them over polling when the requirement is proximity-based.
- Battery accuracy must match the actual product need — do not default to `PRIORITY_HIGH_ACCURACY`.
- Location code in the data layer; permission state and UI decisions in the presentation layer.

---

## Permission Tiers

Android enforces a two-step permission model for background location:

1. `ACCESS_FINE_LOCATION` or `ACCESS_COARSE_LOCATION` — required first.
2. `ACCESS_BACKGROUND_LOCATION` — can only be requested *after* the foreground permission is granted.

Declare in `AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_BACKGROUND_LOCATION" />

<!-- Required for Android 14+ foreground location service -->
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_LOCATION" />
```

**Do not** request `ACCESS_BACKGROUND_LOCATION` in the same launcher call as the foreground permission. The system ignores or rejects bundled requests on Android 11+.

---

## Permission Flow in Compose

Model all states explicitly:

```kotlin
data class LocationPermissionState(
    val isForegroundGranted: Boolean = false,
    val isBackgroundGranted: Boolean = false,
    val shouldShowForegroundRationale: Boolean = false,
    val shouldShowBackgroundRationale: Boolean = false,
    val isForegroundPermanentlyDenied: Boolean = false,
    val isBackgroundPermanentlyDenied: Boolean = false
)
```

Launch foreground first, background only after foreground is granted:

```kotlin
@Composable
fun LocationTrackingRoot(viewModel: LocationViewModel = koinViewModel()) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    val foregroundLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { results ->
        viewModel.onAction(LocationAction.OnForegroundPermissionResult(results))
    }

    val backgroundLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        viewModel.onAction(LocationAction.OnBackgroundPermissionResult(granted))
    }

    LocationTrackingScreen(
        state = state,
        onAction = { action ->
            when (action) {
                LocationAction.OnRequestForegroundClick -> foregroundLauncher.launch(
                    arrayOf(
                        Manifest.permission.ACCESS_FINE_LOCATION,
                        Manifest.permission.ACCESS_COARSE_LOCATION
                    )
                )
                LocationAction.OnRequestBackgroundClick -> backgroundLauncher.launch(
                    Manifest.permission.ACCESS_BACKGROUND_LOCATION
                )
                else -> viewModel.onAction(action)
            }
        }
    )
}
```

On Android 11+, requesting `ACCESS_BACKGROUND_LOCATION` opens the system settings screen, not a dialog. Explain this to the user before launching.

---

## Foreground Service for Continuous Tracking

Declare the service in the manifest with `foregroundServiceType`:

```xml
<service
    android:name=".location.LocationForegroundService"
    android:foregroundServiceType="location"
    android:exported="false" />
```

The service class:

```kotlin
class LocationForegroundService : Service() {

    private val fusedClient by lazy {
        LocationServices.getFusedLocationProviderClient(this)
    }
    private var locationCallback: LocationCallback? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent?.action == ACTION_STOP) {
            stopTracking()
            return START_NOT_STICKY
        }
        startForeground(NOTIFICATION_ID, buildNotification())
        startTracking()
        return START_STICKY
    }

    private fun startTracking() {
        val request = buildLocationRequest()
        locationCallback = object : LocationCallback() {
            override fun onLocationResult(result: LocationResult) {
                result.lastLocation?.let { location ->
                    // Emit to a shared Flow, repository, or broadcast
                    LocationEventBus.emit(location)
                }
            }
        }
        fusedClient.requestLocationUpdates(request, locationCallback!!, Looper.getMainLooper())
    }

    private fun stopTracking() {
        locationCallback?.let { fusedClient.removeLocationUpdates(it) }
        stopForeground(STOP_FOREGROUND_REMOVE)
        stopSelf()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    companion object {
        const val ACTION_STOP = "action.stop_location"
        private const val NOTIFICATION_ID = 1001
    }
}
```

**Do not** run location updates in a `CoroutineWorker` without a foreground service — WorkManager workers are not guaranteed to stay alive for continuous streaming.

---

## LocationRequest: Accuracy and Battery Trade-offs

```kotlin
fun buildLocationRequest(): LocationRequest =
    LocationRequest.Builder(
        Priority.PRIORITY_BALANCED_POWER_ACCURACY,
        intervalMillis = 30_000L          // preferred update interval
    )
        .setMinUpdateIntervalMillis(15_000L)     // fastest interval if updates come faster
        .setMinUpdateDistanceMeters(50f)         // skip update if moved less than 50 m
        .setWaitForAccurateLocation(false)
        .build()
```

| Priority | Battery use | Accuracy | When to use |
|---|---|---|---|
| `PRIORITY_HIGH_ACCURACY` | High | GPS-level | Turn-by-turn navigation |
| `PRIORITY_BALANCED_POWER_ACCURACY` | Medium | ~100 m | Delivery tracking, fitness |
| `PRIORITY_LOW_POWER` | Low | City-level | Background city-aware features |
| `PRIORITY_PASSIVE` | Minimal | Opportunistic | Logging only, no urgency |

`setMinUpdateDistanceMeters` is the most impactful battery saving for stationary or slow-moving users. Always set it unless sub-meter precision is required at rest.

---

## FusedLocationProviderClient Setup

Wrap the client behind a data-layer interface:

```kotlin
interface LocationDataSource {
    fun locationUpdates(): Flow<Location>
    suspend fun lastKnownLocation(): Location?
}

class FusedLocationDataSource(
    private val context: Context
) : LocationDataSource {

    private val client = LocationServices.getFusedLocationProviderClient(context)

    @SuppressLint("MissingPermission")
    override fun locationUpdates(): Flow<Location> = callbackFlow {
        val request = buildLocationRequest()
        val callback = object : LocationCallback() {
            override fun onLocationResult(result: LocationResult) {
                result.lastLocation?.let { trySend(it) }
            }
        }
        client.requestLocationUpdates(request, callback, Looper.getMainLooper())
        awaitClose { client.removeLocationUpdates(callback) }
    }

    @SuppressLint("MissingPermission")
    override suspend fun lastKnownLocation(): Location? =
        client.lastLocation.await()
}
```

The `@SuppressLint("MissingPermission")` annotation is acceptable here because permission checks happen in the presentation layer before starting the service. Never call these APIs without a prior permission check.

---

## Geofencing API

### Setup

```kotlin
class GeofenceManager(private val context: Context) {

    private val client: GeofencingClient =
        LocationServices.getGeofencingClient(context)

    private val geofencePendingIntent: PendingIntent by lazy {
        val intent = Intent(context, GeofenceBroadcastReceiver::class.java)
        PendingIntent.getBroadcast(
            context,
            0,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_MUTABLE
        )
    }

    @SuppressLint("MissingPermission")
    fun addGeofences(fences: List<GeofenceSpec>) {
        val geofences = fences.map { spec ->
            Geofence.Builder()
                .setRequestId(spec.id)
                .setCircularRegion(spec.lat, spec.lng, spec.radiusMeters)
                .setTransitionTypes(
                    Geofence.GEOFENCE_TRANSITION_ENTER or Geofence.GEOFENCE_TRANSITION_EXIT
                )
                .setExpirationDuration(Geofence.NEVER_EXPIRE)
                .build()
        }

        val request = GeofencingRequest.Builder()
            .setInitialTrigger(GeofencingRequest.INITIAL_TRIGGER_ENTER)
            .addGeofences(geofences)
            .build()

        client.addGeofences(request, geofencePendingIntent)
            .addOnFailureListener { e ->
                // Log failure; re-register on next app start if needed
            }
    }

    fun removeGeofences(ids: List<String>) {
        client.removeGeofences(ids)
    }
}

data class GeofenceSpec(
    val id: String,
    val lat: Double,
    val lng: Double,
    val radiusMeters: Float
)
```

### BroadcastReceiver

```kotlin
class GeofenceBroadcastReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        val event = GeofencingEvent.fromIntent(intent) ?: return
        if (event.hasError()) {
            // Log GeofenceStatusCodes.getStatusCodeString(event.errorCode)
            return
        }

        val transition = event.geofenceTransition
        val triggeringIds = event.triggeringGeofences?.map { it.requestId } ?: return

        when (transition) {
            Geofence.GEOFENCE_TRANSITION_ENTER -> handleEnter(context, triggeringIds)
            Geofence.GEOFENCE_TRANSITION_EXIT -> handleExit(context, triggeringIds)
        }
    }

    private fun handleEnter(context: Context, ids: List<String>) {
        // Start a coroutine via a dedicated scope or inject via a service/work
        GeofenceEventBus.emit(GeofenceEvent.Enter(ids))
    }

    private fun handleExit(context: Context, ids: List<String>) {
        GeofenceEventBus.emit(GeofenceEvent.Exit(ids))
    }
}
```

Register the receiver in the manifest:

```xml
<receiver
    android:name=".location.GeofenceBroadcastReceiver"
    android:exported="false" />
```

**Do not** do heavy processing directly in `onReceive` — it runs on the main thread with a short time budget. Delegate to a coroutine scope, a service, or WorkManager.

---

## Re-registering Geofences After Reboot

Geofences are cleared when the device reboots or the app is updated. Re-register on:
- `BOOT_COMPLETED` broadcast
- App process restart if the data layer detects missing fences

```kotlin
class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
            // Re-enqueue geofence registration work via WorkManager
            GeofenceRestoreWorker.enqueue(WorkManager.getInstance(context))
        }
    }
}
```

---

## Anti-Patterns

- Requesting `ACCESS_BACKGROUND_LOCATION` without a clearly user-visible reason — triggers Play Store review scrutiny.
- Using `PRIORITY_HIGH_ACCURACY` for passive or periodic use cases — drains the battery unnecessarily.
- Not calling `removeLocationUpdates` when the service stops — keeps GPS hardware active.
- Storing raw `Location` objects in the domain layer — map to typed domain models with lat/lng/accuracy/timestamp.
- Ignoring geofence `GEOFENCE_STATUS_OPERATION_NOT_AVAILABLE` — the device may not support geofencing; degrade gracefully.
- Re-registering geofences on every app launch without checking if they are already active — wastes resources and can hit the 100-geofence limit.

---

## Testing Guidance

- Test `ViewModel` state transitions for each permission state (denied, rationale, permanently denied, granted foreground, granted background).
- Mock `FusedLocationDataSource` behind an interface for unit tests.
- Use `FakeLocation` helpers or `LocationManager.setTestProviderLocation` in instrumented tests.
- Test geofence event handling in `GeofenceBroadcastReceiver` by constructing a mock `Intent`.

See **android-permissions-device-apis** for the general permission request and rationale pattern.
See **android-maps-location-ui** for displaying location on a map screen.

---

## Checklist: Adding Background Location or Geofencing

- [ ] Request foreground location permission before background
- [ ] Show a clear rationale before requesting `ACCESS_BACKGROUND_LOCATION`
- [ ] Use a foreground service with `foregroundServiceType="location"` for continuous tracking
- [ ] Set `interval`, `minUpdateInterval`, and `minUpdateDistanceMeters` to match battery needs
- [ ] Choose accuracy priority based on actual requirement, not convenience
- [ ] Register a `GeofenceBroadcastReceiver` and re-register fences after reboot
- [ ] Delegate from `onReceive` — do not do heavy work on the main thread
- [ ] Handle permanent denial with a settings redirect
- [ ] Wrap platform APIs behind a testable interface
