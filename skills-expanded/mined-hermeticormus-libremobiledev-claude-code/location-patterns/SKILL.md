---
name: location-patterns
description: "Location code for CoreLocation, FusedLocationProvider, geofencing and geocoding on both platforms, Flutter geolocator with flutter_map, and a battery impact comparison. Use when adding location tracking, geofences, or maps."
---

# Location Patterns

## iOS: CoreLocation Setup

```swift
import CoreLocation

class LocationService: NSObject, CLLocationManagerDelegate {
    static let shared = LocationService()
    private let manager = CLLocationManager()

    var onLocationUpdate: ((CLLocation) -> Void)?
    var onAuthorizationChange: ((CLAuthorizationStatus) -> Void)?

    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyHundredMeters
        manager.distanceFilter = 50 // Only update every 50 meters
    }

    func requestPermission() {
        manager.requestWhenInUseAuthorization()
    }

    func startTracking() {
        guard CLLocationManager.locationServicesEnabled() else { return }
        manager.startUpdatingLocation()
    }

    func stopTracking() {
        manager.stopUpdatingLocation()
    }

    // For background monitoring (requires .authorizedAlways)
    func startSignificantLocationChange() {
        manager.startMonitoringSignificantLocationChanges()
    }

    // CLLocationManagerDelegate
    func locationManager(_ manager: CLLocationManager,
                         didUpdateLocations locations: [CLLocation]) {
        guard let location = locations.last else { return }
        // Filter out old/inaccurate fixes
        guard location.timestamp.timeIntervalSinceNow > -10,
              location.horizontalAccuracy < 100 else { return }
        onLocationUpdate?(location)
    }

    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        onAuthorizationChange?(manager.authorizationStatus)
    }
}
```

### iOS Geofencing
```swift
func addGeofence(identifier: String, coordinate: CLLocationCoordinate2D, radius: Double) {
    let region = CLCircularRegion(
        center: coordinate,
        radius: min(radius, manager.maximumRegionMonitoringDistance), // Respect system max
        identifier: identifier
    )
    region.notifyOnEntry = true
    region.notifyOnExit = true

    manager.startMonitoring(for: region)
}

func locationManager(_ manager: CLLocationManager,
                     didEnterRegion region: CLRegion) {
    guard let circularRegion = region as? CLCircularRegion else { return }
    print("Entered region: \(circularRegion.identifier)")
    // Trigger local notification or background task
}
```

### iOS Geocoding
```swift
let geocoder = CLGeocoder()

func reverseGeocode(_ location: CLLocation, completion: @escaping (String?) -> Void) {
    geocoder.reverseGeocodeLocation(location) { placemarks, error in
        guard let placemark = placemarks?.first, error == nil else {
            completion(nil)
            return
        }
        let address = [
            placemark.thoroughfare,
            placemark.locality,
            placemark.administrativeArea
        ].compactMap { $0 }.joined(separator: ", ")
        completion(address)
    }
}
```

---

## Android: FusedLocationProvider

```kotlin
import com.google.android.gms.location.*

class LocationService(private val context: Context) {
    private val fusedClient = LocationServices.getFusedLocationProviderClient(context)

    private val locationRequest = LocationRequest.Builder(
        Priority.PRIORITY_BALANCED_POWER_ACCURACY,
        10_000L // 10 second interval
    ).apply {
        setMinUpdateIntervalMillis(5_000L) // Fastest: 5 seconds
        setMinUpdateDistanceMeters(20f)     // Only update if moved 20m
    }.build()

    private val locationCallback = object : LocationCallback() {
        override fun onLocationResult(result: LocationResult) {
            result.lastLocation?.let { location ->
                onLocationUpdate(location)
            }
        }
    }

    @SuppressLint("MissingPermission") // Permission checked by caller
    fun startTracking(onUpdate: (Location) -> Unit) {
        onLocationUpdate = onUpdate
        fusedClient.requestLocationUpdates(
            locationRequest,
            locationCallback,
            Looper.getMainLooper()
        )
    }

    fun stopTracking() {
        fusedClient.removeLocationUpdates(locationCallback)
    }

    @SuppressLint("MissingPermission")
    suspend fun getLastKnownLocation(): Location? =
        fusedClient.lastLocation.await()

    private var onLocationUpdate: ((Location) -> Void) = {}
}
```

### Android Geofencing
```kotlin
val geofencingClient = LocationServices.getGeofencingClient(context)

fun addGeofence(id: String, lat: Double, lng: Double, radiusMeters: Float) {
    val geofence = Geofence.Builder()
        .setRequestId(id)
        .setCircularRegion(lat, lng, radiusMeters)
        .setExpirationDuration(Geofence.NEVER_EXPIRE)
        .setTransitionTypes(Geofence.GEOFENCE_TRANSITION_ENTER or Geofence.GEOFENCE_TRANSITION_EXIT)
        .setLoiteringDelay(30_000) // 30s dwell before DWELL event
        .build()

    val request = GeofencingRequest.Builder()
        .setInitialTrigger(GeofencingRequest.INITIAL_TRIGGER_ENTER)
        .addGeofence(geofence)
        .build()

    geofencingClient.addGeofences(request, geofencePendingIntent)
        .addOnSuccessListener { Log.d("Geofence", "Added $id") }
        .addOnFailureListener { Log.e("Geofence", "Failed: ${it.message}") }
}

// BroadcastReceiver for geofence events
class GeofenceBroadcastReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val geofencingEvent = GeofencingEvent.fromIntent(intent) ?: return
        if (geofencingEvent.hasError()) return

        val transition = geofencingEvent.geofenceTransition
        val triggeringGeofences = geofencingEvent.triggeringGeofences ?: return

        when (transition) {
            Geofence.GEOFENCE_TRANSITION_ENTER -> handleEnter(triggeringGeofences)
            Geofence.GEOFENCE_TRANSITION_EXIT -> handleExit(triggeringGeofences)
        }
    }
}
```

---

## Flutter: geolocator + flutter_map

```dart
import 'package:geolocator/geolocator.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

class LocationRepository {
  Stream<Position> getPositionStream() {
    const settings = LocationSettings(
      accuracy: LocationAccuracy.high,
      distanceFilter: 10, // meters
    );
    return Geolocator.getPositionStream(locationSettings: settings);
  }

  Future<Position?> getCurrentPosition() async {
    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) return null;
    }
    return Geolocator.getCurrentPosition(desiredAccuracy: LocationAccuracy.high);
  }
}

// flutter_map with user location
class MapScreen extends StatefulWidget {
  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  LatLng? _userLocation;

  @override
  Widget build(BuildContext context) {
    return FlutterMap(
      options: MapOptions(
        initialCenter: _userLocation ?? const LatLng(9.0, -79.5),
        initialZoom: 13.0,
      ),
      children: [
        TileLayer(
          urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
          userAgentPackageName: 'com.myapp',
        ),
        if (_userLocation != null)
          MarkerLayer(
            markers: [
              Marker(
                point: _userLocation!,
                child: const Icon(Icons.my_location, color: Colors.blue),
              ),
            ],
          ),
      ],
    );
  }
}
```

---

## Battery Impact Comparison

| Strategy | iOS | Android | Accuracy | Battery |
|----------|-----|---------|----------|---------|
| Significant change | `startMonitoringSignificantLocationChanges` | `PRIORITY_LOW_POWER` | ~500m | Very low |
| Balanced | `kCLLocationAccuracyHundredMeters` | `PRIORITY_BALANCED_POWER_ACCURACY` | ~100m | Low |
| High accuracy | `kCLLocationAccuracyBest` | `PRIORITY_HIGH_ACCURACY` | ~5m | High |
| Navigation | `kCLLocationAccuracyBestForNavigation` | `PRIORITY_HIGH_ACCURACY` + heading | ~3m | Very high |
