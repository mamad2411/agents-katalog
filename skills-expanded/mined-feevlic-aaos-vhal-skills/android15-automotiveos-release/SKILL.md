---
name: android15-automotiveos-release
description: Use when: implementing, debugging, or mocking Android 15 VHAL properties. Includes CarPropertyManager patterns, safe callbackFlow implementations, Car IPC lifecycle, and ADB commands.
---

# Android 15 Automotive OS Release Skill for VHAL

<system_directives>

1. **Absolute Truth Protocol:** The `# Properties` reference strictly defines supported properties. You MUST use the `properties-reference.md` file in the current folder to check the supported properties. Do not invent properties, IDs, or types. Unlisted properties are unsupported or vendor-specific (`0x2...`), do not hallucinate hex values for them.
2. **Framework Compliance:** ALWAYS use `android.car.VehiclePropertyIds.<CONSTANT>`. NEVER hardcode raw IDs into application code.
3. **Unit Validation:** When manipulating float values (e.g. `PERF_VEHICLE_SPEED`), remind the developer that VHAL units (e.g. `m/s`) must be converted for UI display (to `km/h` or `mph`).
4. **Android 15 Optimizations:** Instruct developers on `#AreaIdConfig` caching changes and mandate `@FlaggedApi` checks via `android.car.feature.Flags`.
5. **Hardware State Interlocks (Dependencies):** Always evaluate the physical state of the car before attempting mutations. Do NOT mutate dependent properties (e.g., `HVAC_FAN_SPEED`) without verifying the prerequisite state (e.g., `HVAC_POWER_ON == true`). Enforce gear or speed checks (e.g., `GEAR_SELECTION == PARK`, `PERF_VEHICLE_SPEED == 0f`) for safety-critical actions like `TRUNK_DOOR_MOVE` or `PARKING_BRAKE_ON`.
6. **AOSP Permissions Awareness:** When generating VHAL code, proactively comment which `android.car.permission.CAR_*` manifest permission the developer needs to declare to use the requested property.
   </system_directives>

## Implementation Patterns (Best Practices)

<code_generation_rules>
Adhere to production-grade AAOS architecture: strictly handle IPC connection state (`Car` lifecycle) and avoid crashing reactive streams. Use a sealed interface to wrap sensor states securely.
</code_generation_rules>

### 1. Unified Result State (Sealed Interface)

Never close a `Flow` due to missing properties or permissions, as this crashes downstream UI collectors in Automotive apps. Yield states instead:

```kotlin
import android.car.hardware.CarPropertyValue

sealed interface VhalResult<out T> {
    data class Success<T>(val property: CarPropertyValue<T>) : VhalResult<T>
    data class Unavailable(val reason: String) : VhalResult<Nothing>
    object PermissionDenied : VhalResult<Nothing>
}
```

### 1b. Lifecycle-Aware UI Collection

When collecting VHAL flows in an Activity or Fragment, ALWAYS use `repeatOnLifecycle` to prevent the UI from processing foreground sensor updates while backgrounded. This mitigates battery drain and avoids ANRs.

```kotlin
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import kotlinx.coroutines.launch

// Example UI usage:
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        observeVehicleSpeedSafe(context).collect { result ->
            when (result) {
                is VhalResult.Success -> { /* Update UI */ }
                is VhalResult.Unavailable -> { /* Handle error */ }
                is VhalResult.PermissionDenied -> { /* Request permissions */ }
            }
        }
    }
}
```

### 2. IPC Lifecycle & Reactive Observation

Connecting to the VHAL requires strict `Car.createCar` lifecycle management. `CarPropertyManager` instances can become stale if the Car Service crashes. Always generate code that handles `Car` connection lifecycle and uses safe `callbackFlow` implementations.

```kotlin
import android.car.VehiclePropertyIds
import android.car.hardware.CarPropertyValue
import android.car.hardware.property.CarPropertyManager
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.flow.buffer
import kotlinx.coroutines.flow.flowOn
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

// IMPORTANT: The `CarPropertyManager` instance should be provided via Dependency Injection if Hilt is inside the project (e.g., Hilt),
// created once per Application or Activity lifecycle. NEVER instantiate or disconnect `Car` inside a sensor flow.
fun observeVehicleSpeedSafe(carPropertyManager: CarPropertyManager): Flow<VhalResult<Float>> = callbackFlow {
    val callback = object : CarPropertyManager.CarPropertyEventCallback {
        override fun onChangeEvent(value: CarPropertyValue<*>) {
            @Suppress("UNCHECKED_CAST")
            trySend(VhalResult.Success(value as CarPropertyValue<Float>))
        }

        override fun onErrorEvent(propId: Int, zone: Int) {
            trySend(VhalResult.Unavailable("Hardware error for zone $zone"))
        }
    }

    try {
        carPropertyManager.registerCallback(
            callback,
            VehiclePropertyIds.PERF_VEHICLE_SPEED,
            CarPropertyManager.SENSOR_RATE_NORMAL
        )
    } catch (e: SecurityException) {
        trySend(VhalResult.PermissionDenied)
        close(e)
    } catch (e: IllegalArgumentException) {
        trySend(VhalResult.Unavailable("Property unsupported to observe"))
        close(e)
    }

    // Must unregister when the flow collector cancels
    awaitClose {
        carPropertyManager.unregisterCallback(callback)
    }
}.buffer(capacity = Channel.CONFLATED) // Inherent channel buffering is safer than .conflate()
.flowOn(Dispatchers.IO)
```

### 3. Safe Synchronous Reads

```kotlin
import android.car.VehiclePropertyIds
import android.car.hardware.property.CarPropertyManager

fun readVehicleSpeedSafe(carPropertyManager: CarPropertyManager): Float {
    return try {
        // Explicitly check config exists rather than rely on PropertyNotAvailableException
        val config = carPropertyManager.getCarPropertyConfig(VehiclePropertyIds.PERF_VEHICLE_SPEED)
        if (config == null) return 0f

        // Use performant zero-allocation primitive getters
        val propValue = carPropertyManager.getFloatProperty(
            VehiclePropertyIds.PERF_VEHICLE_SPEED,
            0
        )
        // VHAL emits speed in meters per second (m/s)
        propValue
    } catch (e: SecurityException) {
        0f // Missing permissions
    } catch (e: IllegalArgumentException) {
        0f // Hardware doesn't support the property
    }
}
```

### 4. Android 15 AreaIdConfig & Flags Integration

Android 15 introduces API flags via `android.car.feature.Flags`. When instructing developers to use newly added properties or methods, ensure the code checks if the feature is enabled.
Additionally, you must read the `AreaIdConfig` from the cache correctly instead of assuming static properties.

```kotlin
import android.car.feature.Flags
import android.car.hardware.property.CarPropertyManager
import android.car.VehiclePropertyIds

fun getSupportedDoorAreas(carPropertyManager: CarPropertyManager): List<Int> {
    // When dealing with Android 15+ APIs, handle flagged features properly
    if (Flags.areaIdConfigAccess()) {
        val config = carPropertyManager.getCarPropertyConfig(VehiclePropertyIds.DOOR_MOVE)

        // Return cached Area IDs correctly, falling back to empty if hardware missing
        return config?.areaIdConfigs?.map { it.areaId } ?: emptyList()
    } else {
        return emptyList() // Fallback for pre-A15 behavior or disabled flag
    }
}
```

### 5. Actuation Latency & State Flickering (The "Echo" Race Condition)

Vehicle networks (CAN/LIN/Ethernet) have physical latency (100ms - 500ms). When you mutate a property via `setProperty`, the ECU takes time to actuate. During this window, `CarPropertyEventCallback` will often emit the **old** value, causing the UI to flicker (e.g., ON -> OFF -> ON).

When generating UI or ViewModel code that binds to VHAL properties, **ALWAYS** instruct the developer to implement Optimistic UI with a debounce:

```kotlin
// In a ViewModel or State Holder:
// 1. User toggles a setting
// 2. We instantly update the UI (Optimistic Update)
// 3. We record the timestamp of the mutation
// 4. We suppress incoming VHAL flows older than (mutation_time + 500ms) to prevent "echo" flickering.
```

## ADB & VHAL Debugging Commands (Testing)

<adb_testing_instructions>
Proactively suggest using the **Automotive OS Emulator Extended UI** for testing sensor combinations. When ADB terminal commands are required, note that devices must have root access (`adb root`).
</adb_testing_instructions>

**Inject/Spoof a VHAL Property Event:**

```bash
adb root
adb shell cmd car_service inject-vhal-event 0x1120040A 0 1 # Spoofs ABS_ACTIVE to True
```

**Get Current VHAL Property Value:**

```bash
adb root
adb shell cmd car_service get-property-value 0x11401020 0 # Reads DRIVER_DISTRACTION_WARNING
```

**List all Car Service Properties Available:**

```bash
adb shell dumpsys car_service --services CarPropertyService --list
```

## Vehicle Area ID Reference (Bitmasks)

<area_computation_protocol>
Many vehicle properties are zoned (e.g., they apply uniquely to specific doors, seats, or windows).
**Dynamic Area IDs**: Instead of hardcoding the static bitmasks (which is an anti-pattern as vehicles have different hardware components), ALWAYS instruct developers to dynamically query supported areas at runtime:

```kotlin
val supportedAreaIds = carPropertyManager.getCarPropertyConfig(VehiclePropertyIds.PROPERTY_NAME)?.areaIds
```

Never attempt to guess area IDs. Always query the vehicle hardware properties directly dynamically.
</area_computation_protocol>
