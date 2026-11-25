---
name: android-maps-location-ui
description: |
  Android maps and location UI patterns - map screens, markers, camera state, location permission integration, geospatial UI state, and user-friendly place interactions. Use this skill whenever building map-based screens, showing nearby results, controlling map camera state, or combining location permissions with spatial UI. Trigger on phrases like "map", "marker", "camera position", "nearby places", "location UI", "geospatial", or "map screen".
---

# Android Maps and Location UI

## Core Principles

- Map UI should support a clear user task, not exist as decoration.
- The `ViewModel` owns location-driven screen state; the map renders it.
- Permission, location availability, and empty results are first-class UI states.
- Camera movement and marker interactions should feel intentional.
- Spatial screens should degrade gracefully when location is unavailable.

---

## Typical Use Cases

Good map use cases:
- nearby search
- delivery/trip progress
- pick a place on a map
- view clustered locations
- inspect one location in context

Bad map use cases:
- showing a map when a simple list would do
- loading too many points without clustering or filtering
- making location permission mandatory before any value is shown

---

## Screen State

Represent map state explicitly:

```kotlin
data class NearbyMapState(
    val markers: List<PlaceUi> = emptyList(),
    val selectedPlaceId: String? = null,
    val isLocationGranted: Boolean = false,
    val isLocationEnabled: Boolean = false,
    val isLoading: Boolean = false,
    val error: UiText? = null
)
```

The screen should render from one state object rather than scattered booleans.

---

## Camera Ownership

Decide which camera changes are app-driven vs user-driven.

Common good patterns:
- initial camera from last known or default region
- animate to selected marker
- animate to user location only after explicit user intent or first meaningful entry

Bad patterns:
- constantly fighting the user's manual pan/zoom
- recentering on every location update

---

## Marker Strategy

For markers:
- keep labels concise
- show selection state clearly
- cluster dense data when necessary
- avoid loading huge marker sets without strategy

If the map shows many results, combine filtering, clustering, or list+map patterns instead of plotting everything at once.

---

## Permission and Device State

Maps often depend on both permission and device services.

Handle separately:
- location permission denied
- location permanently denied
- GPS/location services disabled
- no current fix available

A map screen can often still provide value without current location by showing a default region, search, or manually chosen area.

See the **android-permissions-device-apis** skill.

---

## Map + List Coordination

Many map screens work best with a companion list or bottom sheet.

Patterns that work well:
- selecting a list item highlights and centers the marker
- tapping a marker selects an item card or bottom sheet
- the map provides spatial context while the list provides detail and scannability

Keep selection state centralized in the `ViewModel`.

---

## Deep Links and External Entry

If the app opens directly to a place or coordinates:
- validate inbound data
- map to a typed destination
- initialize the screen with a safe default if coordinates are invalid

See the **android-deep-links** skill.

---

## Performance Guidance

Map screens can get expensive quickly.

Guidelines:
- avoid excessive recomposition around map state
- throttle expensive nearby searches tied to camera movement when needed
- cluster or page large result sets
- precompute UI-ready marker data where helpful

For broader optimization guidance, see the **android-performance-profiling** skill.

---

## Testing Guidance

Test:
- state changes for permission/device availability
- marker selection and selection clearing
- camera-triggering actions from the `ViewModel`
- fallback UI when no location or no results are available
- list/map coordination behavior

Keep map SDK specifics thin enough that most logic is testable without instrumented map rendering.

---

## Checklist: Adding a Map Screen

- [ ] Confirm the map supports a clear user task
- [ ] Model marker, selection, and location state explicitly
- [ ] Handle permission and disabled-service states separately
- [ ] Avoid camera behavior that fights user gestures
- [ ] Add clustering/filtering strategy for large result sets
- [ ] Keep list/map selection coordinated through the `ViewModel`