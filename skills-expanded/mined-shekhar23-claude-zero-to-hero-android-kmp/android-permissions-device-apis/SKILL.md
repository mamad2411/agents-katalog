---
name: android-permissions-device-apis
description: |
  Runtime permissions and device API patterns for Android - permission requests, rationale flows, activity results, camera, location, notifications, and capability-based feature access. Use this skill whenever adding access to device capabilities or platform services that require runtime permission or launcher-based contracts. Trigger on phrases like "permission", "camera", "location", "notifications", "activity result", "pick image", "request permission", or "device capability".
---

# Android Permissions and Device APIs

## Core Principles

- Request a permission only when the user is about to use the related feature.
- Explain value before requesting when the need is not obvious.
- Model capability state in the `ViewModel`; keep platform request launching in the UI layer.
- Handle denial, permanent denial, and unavailable capability as first-class states.
- Prefer high-level platform contracts over manual intent/result plumbing.

---

## Permission Request Philosophy

Do not ask for permissions on app launch unless the entire app is unusable without them.

Good timing:
- camera permission when tapping scan or capture
- location permission when starting nearby search or map centering
- notification permission when enabling alerts

Bad timing:
- first frame of app startup
- before the user understands the feature value
- requesting unrelated permissions in bulk

---

## Capability-Based UI State

Represent device access as UI state, not scattered boolean checks:

```kotlin
data class CameraAccessState(
    val isGranted: Boolean = false,
    val shouldShowRationale: Boolean = false,
    val isPermanentlyDenied: Boolean = false
)
```

The screen renders from state and emits actions like `OnGrantCameraClick` or `OnOpenSettingsClick`.

---

## Compose Boundary

In Compose, launch permission or activity result contracts at the Root level and forward results as actions:

```kotlin
@Composable
fun CameraRoot(
    viewModel: CameraViewModel = koinViewModel()
) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { granted ->
        viewModel.onAction(CameraAction.OnCameraPermissionResult(granted))
    }

    CameraScreen(
        state = state,
        onAction = { action ->
            when (action) {
                CameraAction.OnGrantCameraClick -> {
                    permissionLauncher.launch(Manifest.permission.CAMERA)
                }
                else -> viewModel.onAction(action)
            }
        }
    )
}
```

Keep launcher ownership in the composable layer; keep state and decisions in the `ViewModel`.

---

## Common Cases

### Camera

- Request `CAMERA` only before capture/scan.
- If the app just picks an image, prefer a picker contract and avoid camera permission entirely.

### Photos / Media

- Prefer modern picker APIs when possible.
- Use storage/media permissions only when direct file/media access is actually needed.

### Location

- Request coarse/fine location based on the true requirement.
- Avoid background location unless the product genuinely needs it.
- Degrade gracefully when only coarse location is available.

### Notifications

- Ask only when the user enables a feature that produces notifications.
- Tie the prompt to clear value like reminders or order updates.

---

## Activity Result Contracts

Prefer built-in contracts instead of custom intent handling:

```kotlin
val pickImageLauncher = rememberLauncherForActivityResult(
    contract = ActivityResultContracts.PickVisualMedia()
) { uri ->
    viewModel.onAction(ProfileAction.OnImagePicked(uri))
}
```

Common good uses:
- pick media
- capture photo/video
- request permission
- open document
- create document

---

## Permanent Denial

When the user denies with "don't ask again", do not keep spamming the system dialog.

Instead:
- update UI state to reflect permanent denial
- explain why settings are needed
- offer a button to open app settings

```kotlin
val intent = Intent(
    Settings.ACTION_APPLICATION_DETAILS_SETTINGS,
    Uri.fromParts("package", context.packageName, null)
)
```

---

## ViewModel Responsibilities

The `ViewModel` should:
- decide what state the UI should show
- handle result callbacks as actions
- emit events for education dialogs/snackbars if needed

The `ViewModel` should not:
- hold `Activity` or `Context` references unnecessarily
- directly launch permission dialogs
- directly invoke activity result contracts

---

## Device API Wrappers

For non-trivial device integrations, wrap platform APIs behind interfaces:

```kotlin
interface LocationGateway {
    suspend fun getCurrentLocation(): Result<LocationData, DeviceError>
}
```

Benefits:
- cleaner testing
- less framework leakage into presentation
- better fallback handling

---

## Failure States to Design For

Always account for:
- permission denied
- permission permanently denied
- service disabled (GPS off, notifications disabled, camera unavailable)
- device/API unsupported
- user cancellation from picker/contract

These are normal product states, not edge-case afterthoughts.

---

## Testing Guidance

Test:
- state transitions after granted/denied results
- settings redirection flows
- behavior when capability is unavailable
- `ViewModel` logic around rationale and fallback UI

Keep the platform launcher layer thin and test the decision logic in the `ViewModel`.

---

## Checklist: Adding a Permissioned Feature

- [ ] Ask only at the moment of need
- [ ] Model permission/capability state explicitly
- [ ] Launch contracts from Root composables
- [ ] Send results back as actions to the `ViewModel`
- [ ] Handle permanent denial and settings redirection
- [ ] Design graceful fallback for unsupported or denied access