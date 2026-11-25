---
name: unity-xr
description: >
  Unity 6000.3 LTS XR patterns for AR/VR development. Covers AR Foundation,
  VR development, XR Interaction Toolkit, XR device management, passthrough,
  hand tracking, eye tracking, body tracking, and platform-specific considerations
  for Meta Quest, Vision Pro, HoloLens, PSVR2, and SteamVR.
  Trigger: When developing AR/VR applications, using XR frameworks,
  implementing XR interactions, or handling XR devices in Unity 6000.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Developing AR applications using AR Foundation (plane detection, image tracking, meshing)
- Building VR experiences with XR Interaction Toolkit (locomotion, hand interactions, UI)
- Implementing hand tracking, eye tracking, or body tracking
- Managing XR devices (Meta Quest, Apple Vision Pro, HoloLens, PSVR2, SteamVR)
- Working with XR Subsystems (session management, tracking, anchors)
- Configuring XR Plug-in Framework and provider plugins
- Setting up passthrough, mixed reality, or immersion levels
- Handling XR input from controllers, hands, or haptics

## Critical Rules

### XR Lifecycle — Always Follow the Sequence

```csharp
// CORRECT XR lifecycle order:
// 1. Check availability
// 2. Request permission
// 3. Start subsystem
// 4. Update every frame
// 5. Stop subsystem on cleanup

public class XRSessionManager : MonoBehaviour
{
    private XRSessionSubsystem _session;

    private void Start()
    {
        // 1. Check if XR is supported
        if (!XRGeneralSettings.Instance?.Manager?.isPlatformsInitialized ?? true)
        {
            Debug.LogError("XR not initialized");
            return;
        }

        // 2. Get the session subsystem
        _session = XRGeneralSettings.Instance.Manager.GetLoadedSubsystem<XRSessionSubsystem>();
        if (_session != null)
        {
            // 3. Start the session
            _session.Start();
        }
    }

    private void OnDestroy()
    {
        // 4. Stop on cleanup
        _session?.Stop();
    }
}
```

**Why:** Skipping steps causes runtime errors, devices fail to initialize, or features like passthrough/anchoring silently break.

### Never Access XR Hardware Directly — Use Subsystems

```csharp
// ❌ WRONG — Tries to access hardware directly
void Update()
{
    var pos = OVRPlugin.GetControllerPose(OVRController.Controller.RTouch);
}

// ✅ CORRECT — Use input subsystem abstraction
void Update()
{
    var inputDevice = InputDevices.GetDeviceAtXRNode(XRNode.RightHand);
    if (inputDevice.TryGetFeatureValue(CommonUsages.devicePosition, out Vector3 pos))
    {
        // Use position
    }
}
```

**Why:** Direct hardware access ties you to one platform. Subsystems abstract across Quest, Vision Pro, HoloLens, and more.

### FixedUpdate for XR Tracking, Update for Rendering

```csharp
public class XRTransformSync : MonoBehaviour
{
    private void Update()
    {
        // Get tracking data in Update (or use events)
        // Apply to visuals smoothly
    }

    private void FixedUpdate()
    {
        // Physics-based XR interactions in FixedUpdate
        // Consistent with physics simulation
    }
}
```

### Always Check Feature Support Before Using

```csharp
// Check before using eye tracking
if (XRDisplaySubsystem.GetEyeTrackingSupported())
{
    // Safe to query eye tracking
}

// Check before using hand tracking
if (InputDevices.DeviceSupportsFeature(XR_SPECIFIC_FEATURE_REMOVED_1))
{
    // Actually check hand tracking subsystem
    var handSubsystem = XRGeneralSettings.Instance.Manager
        .GetLoadedSubsystem<XRHandSubsystem>();
    if (handSubsystem != null && handSubsystem.running)
    {
        // Hand tracking is active
    }
}
```

**Why:** Features like eye tracking, hand tracking, and passthrough vary by device. Code that assumes support crashes or silently fails on unsupported hardware.

## AR Foundation

### AR Session Management

```csharp
// ARSession controls the AR experience lifecycle
public class ARSessionController : MonoBehaviour
{
    [SerializeField] private bool _requireCamera = true;
    [SerializeField] private ARSession _session;

    private void Start()
    {
        if (_session == null)
        {
            _session = FindObjectOfType<ARSession>();
            if (_session == null)
            {
                _session = new GameObject("AR Session").AddComponent<ARSession>();
            }
        }

        // NotRecommended: ARSessionState.CheckAvailability() requires internet for first check
        // Better: Try to start and handle failure
    }

    public void StartAR()
    {
        _session.enabled = true;
    }

    public void StopAR()
    {
        _session.enabled = false;
    }
}
```

### Plane Detection

```csharp
// ARPlaneManager detects horizontal and vertical surfaces
public class PlaneDetection : MonoBehaviour
{
    [SerializeField] private ARPlaneManager _planeManager;
    [SerializeField] private GameObject _planePrefab;

    private void OnEnable()
    {
        _planeManager.planesChanged += OnPlanesChanged;
    }

    private void OnDisable()
    {
        _planeManager.planesChanged -= OnPlanesChanged;
    }

    private void OnPlanesChanged(ARPlanesChangedEventArgs args)
    {
        // New planes detected
        foreach (var plane in args.added)
        {
            // plane.classification tells you floor, wall, ceiling, table, chair, etc.
            if (plane.classification == PlaneClassification.Table)
            {
                SpawnContentOnPlane(plane);
            }
        }

        // Updated planes (size changed)
        foreach (var plane in args.updated)
        {
            UpdatePlaneVisual(plane);
        }

        // Removed planes
        foreach (var plane in args.removed)
        {
            RemovePlaneVisual(plane);
        }
    }

    // Classification confidence levels
    // Use plane.classification for runtime decisions
    // Not all devices support classification
}
```

### AR Raycasting

```csharp
// ARRcastPlanner for efficient AR raycasting
public class ARRaycastController : MonoBehaviour
{
    [SerializeField] private ARRaycastManager _raycastManager;
    [SerializeField] private LayerMask _placeableLayers;
    private List<ARRaycastHit> _hits = new();

    public bool TryPlaceObject(Vector2 screenPosition)
    {
        _hits.Clear();

        // Raycast against planes and depth
        if (_raycastManager.Raycast(screenPosition, _hits,
            ARRaycastManager.TrackableType.Planes |
            ARRaycastManager.TrackableType.Depth |
            ARRaycastManager.TrackableType.InstantPlanes))
        {
            // Sort by distance
            _hits.Sort((a, b) => a.distance.CompareTo(b.distance));

            var hit = _hits[0];
            var obj = Instantiate(_prefab, hit.pose.position, hit.pose.rotation);

            // Align to surface normal
            obj.transform.up = hit.normal;

            return true;
        }

        return false;
    }

    // For instant placement without plane detection
    public void PlaceInstant(Vector3 position, Quaternion rotation)
    {
        vargo.transform.SetPositionAndRotation(position, rotation);
    }
}
```

### AR Anchors

```csharp
// ARAnchorManager for persistent world-locked content
public class ARAnchorManager : MonoBehaviour
{
    [SerializeField] private ARAnchorManager _anchorManager;
    private Dictionary<ARAnchor, GameObject> _anchorPrefabs = new();

    public ARAnchor CreateAnchor(ARAnchor anchor)
    {
        // Attach to existing trackable
        var anchorAttach = _anchorManager.AttachAnchor(anchor);
        return anchorAttach;
    }

    public ARAnchor CreateAnchorFromRaycast(ARRaycastHit hit)
    {
        // Create new anchor at raycast result
        var anchor = _anchorManager.AddAnchor(hit.pose);
        if (anchor != null)
        {
            // Anchor is world-locked
            _anchorPrefabs[anchor] = CreateAnchorVisual(anchor);
        }
        return anchor;
    }

    public void RemoveAnchor(ARAnchor anchor)
    {
        if (_anchorPrefabs.TryGetValue(anchor, out var visual))
        {
            Destroy(visual);
            _anchorPrefabs.Remove(anchor);
        }
        _anchorManager.RemoveAnchor(anchor);
    }
}
```

### AR Meshing (Reality Mesh)

```csharp
// ARMeshManager for scene understanding and occlusion
public class ARMeshController : MonoBehaviour
{
    [SerializeField] private ARMeshManager _meshManager;
    [SerializeField] private Material _occlusionMaterial;
    [SerializeField] private Material _visualizationMaterial;

    private void OnEnable()
    {
        _meshManager.meshesChanged += OnMeshesChanged;
    }

    private void OnDisable()
    {
        _meshManager.meshesChanged -= OnMeshesChanged;
    }

    private void OnMeshesChanged(ARMeshesChangedEventArgs args)
    {
        foreach (var meshFilter in args.added)
        {
            // Apply occlusion material for real occlusion
            var renderer = meshFilter.GetComponent<MeshRenderer>();
            renderer.material = _occlusionMaterial;
        }
    }

    // Enable blockwise meshing for better performance on large surfaces
    // ARMeshManager.meshPrefab can use optimized low-poly meshes
}
```

### AR Image Tracking

```csharp
// ARImageTrackingSubsystem for marker-based AR
public class ARImageTracking : MonoBehaviour
{
    [SerializeField] private ARImageTrackingSubsystem _subsystem;
    [SerializeField] private ARTrackedImageManager _trackedImageManager;
    [SerializeField] private int _maxTrackedImages = 10;

    public void SetupLibrary()
    {
        // Runtime-generated reference image library
        var library = _trackedImageManager.CreateRuntimeLibrary();

        // Add image at runtime
        Texture2D texture = LoadImage("marker");
        AddImageToLibrary(library, texture, "myMarker", 0.1f); // 10cm physical size
    }

    private void AddImageToLibrary(ScriptableRuntimeReferenceImageLibrary library,
        Texture2D texture, string name, float physicalSize)
    {
        // Must use Add with new RuntimeReferenceImage
        // library.Add(new RuntimeReferenceImage(...)); - API varies by Unity version
    }

    private void OnTrackedImagesChanged(ARTrackedImagesChangedEventArgs args)
    {
        foreach (var trackedImage in args.added)
        {
            // trackedImage.referenceImage.name tells you which marker
            // trackedImage.transform is world-locked
            trackedImage.gameObject.SetActive(true);
        }

        foreach (var trackedImage in args.updated)
        {
            // Update position/rotation based on tracking quality
            var quality = trackedImage.trackingState;
        }
    }
}
```

### AR Occlusion

```csharp
// AROcclusionManager for human segmentation and depth
public class AROcclusionController : MonoBehaviour
{
    [SerializeField] private AROcclusionManager _occlusionManager;

    public void EnableOcclusionTypes()
    {
        // Human segmentation — people occlude AR content
        _occlusionManager.requestedHumanSegmentationStencilMode =
            HumanSegmentationStencilMode.Enabled;
        _occlusionManager.requestedHumanSegmentationDepthMode =
            HumanSegmentationDepthMode.Enabled;

        // Environment depth — real world occludes virtual
        _occlusionManager.requestedDepthMode = AROcclusionManager.Depth requestedDepthMode;

        // Object occlusion (if supported)
        _occlusionManager.requestedOcclusionPreferenceMode =
            AROcclusionManager.OcclusionPreferenceMode.Any;
    }

    // Check supported modes
    private void CheckSupport()
    {
        var supportedDepth = _occlusionManager.IsDepthModeSupported(
            AROcclusionManager.DepthRequestedDepthMode);
    }
}
```

## VR Development

### XR Plug-in Framework

```csharp
// XRGeneralSettings controls subsystem initialization
public class XRPlatformManager : MonoBehaviour
{
    [SerializeField] private XRGeneralSettings _xrSettings;

    private void Start()
    {
        // Initialize subsystems manually (optional — can be automatic)
        _xrSettings.Manager.InitializeLoaderSync();

        // Start all subsystems
        _xrSettings.Manager.StartSubsystems();

        // Stop on cleanup
        _xrSettings.Manager.StopSubsystems();
        _xrSettings.Manager.Deinitialize();
    }

    // For VR, ensure correct initialization order:
    // 1. XRGeneralSettings.Instance.Manager.InitializeLoaderSync()
    // 2. StartSubsystems()
    // 3. For VR: Ensure VR is enabled in Build Settings
}
```

### VR Display Settings

```csharp
// XRDisplaySubsystem controls VR-specific display features
public class VRDisplaySettings : MonoBehaviour
{
    private XRDisplaySubsystem _displaySubsystem;

    private void GetDisplaySubsystem()
    {
        _displaySubsystem = XRGeneralSettings.Instance.Manager
            .GetLoadedSubsystem<XRDisplaySubsystem>();
    }

    public void EnablePassthrough()
    {
        // Quest passthrough via OpenXR or OVRPlugin
        _displaySubsystem?.EnablePassthrough();
    }

    public void DisablePassthrough()
    {
        _displaySubsystem?.DisablePassthrough();
    }

    public void SetRefreshRate(float hz)
    {
        // Quest supports 72Hz, 90Hz, 120Hz
        _displaySubsystem?.SetPreferredRefreshRate(hz);
    }

    // Query current state
    private void QueryDisplayState()
    {
        if (_displaySubsystem != null)
        {
            var renderPassCount = _displaySubsystem.GetRenderPassCount();
            for (uint i = 0; i < renderPassCount; i++)
            {
                _displaySubsystem.GetRenderPass(i, out var renderPass);
                // Use renderPass for custom rendering
            }
        }
    }
}
```

### VR Immersion Levels

```csharp
// VR immersion is platform-specific
public class VRImmersionManager : MonoBehaviour
{
    // immersion levels from least to most immersive:
    // Inline — No VR, just AR-like view (for testing)
    // MixedReality — Passthrough with virtual objects
    // Immersive — Full VR, no passthrough

    public void SetImmersionLevel(VRImmersionLevel level)
    {
        switch (level)
        {
            case VRImmersionLevel.Inline:
                // For editor testing or non-VR builds
                break;

            case VRImmersionLevel.MixedReality:
                // Enable passthrough (Quest, Vision Pro)
                EnableMixedReality();
                break;

            case VRImmersionLevel.Immersive:
                // Full VR immersion
                DisablePassthrough();
                break;
        }
    }

    // Always respect user preference for immersion level
    // Never force full immersion without consent
}
```

### VR Locomotion

```csharp
// Snap vs Smooth turning for comfort
public class VRLocomotion : MonoBehaviour
{
    [SerializeField] private float _moveSpeed = 3f;
    [SerializeField] private float _turnSpeed = 90f;
    [SerializeField] private bool _snapTurn = true;
    [SerializeField] private float _snapAngle = 30f;
    [SerializeField] private float _gravity = -9.81f;

    private CharacterController _characterController;
    private Vector2 _moveInput;
    private Vector2 _turnInput;
    private float _currentYaw;
    private bool _isGrounded;

    private void Start()
    {
        _characterController = GetComponent<CharacterController>();
    }

    private void Update()
    {
        ReadInput();
        HandleTurning();
    }

    private void FixedUpdate()
    {
        HandleMovement();
    }

    private void ReadInput()
    {
        // Get input from XR controllers
        var leftHand = InputDevices.GetDeviceAtXRNode(XRNode.LeftHand);
        var rightHand = InputDevices.GetDeviceAtXRNode(XRNode.RightHand);

        leftHand.TryGetFeatureValue(CommonUsages.trigger, out float trigger);
        rightHand.TryGetFeatureValue(CommonUsages.grip, out float grip);

        // Movement typically on left thumbstick
        leftHand.TryGetFeatureValue(CommonUsages.primary2DActor, out _moveInput);

        // Turn typically on right thumbstick
        rightHand.TryGetFeatureValue(CommonUsages.primary2DActor, out _turnInput);
    }

    private void HandleTurning()
    {
        if (_snapTurn)
        {
            if (Mathf.Abs(_turnInput.x) > 0.8f)
            {
                // Snap turn
                float direction = _turnInput.x > 0 ? 1f : -1f;
                _currentYaw += direction * _snapAngle;
                _turnInput = Vector2.zero; // Reset to prevent re-trigger
            }
        }
        else
        {
            // Smooth turning
            _currentYaw += _turnInput.x * _turnSpeed * Time.deltaTime;
        }

        transform.rotation = Quaternion.Euler(0, _currentYaw, 0);
    }

    private void HandleMovement()
    {
        _isGrounded = _characterController.isGrounded;

        Vector3 move = transform.forward * _moveInput.y + transform.right * _moveInput.x;
        move *= _moveSpeed;

        if (!_isGrounded)
        {
            move.y = _gravity;
        }

        _characterController.Move(move * Time.fixedDeltaTime);
    }
}
```

### VR Teleportation

```csharp
// Teleportation with fade transition
public class VRTeleport : MonoBehaviour
{
    [SerializeField] private TeleportationProvider _teleportProvider;
    [SerializeField] private LineRenderer _teleportLine;
    [SerializeField] private GameObject _teleportMarker;
    [SerializeField] private LayerMask _teleportableLayers;
    [SerializeField] private float _maxTeleportDistance = 10f;

    private TeleportRequest _currentRequest;
    private bool _isTeleportValid;

    public void ProcessTeleportInput(XRNode controllerNode)
    {
        var controller = InputDevices.GetDeviceAtXRNode(controllerNode);

        controller.TryGetFeatureValue(CommonUsages.trigger, out float triggerValue);
        bool isAiming = triggerValue > 0.5f;

        if (isAiming)
        {
            AimTeleport(controller);
        }
        else if (_isTeleportValid && triggerValue < 0.2f)
        {
            ExecuteTeleport();
        }

        _teleportLine.enabled = isAiming;
    }

    private void AimTeleport(InputDevice controller)
    {
        controller.TryGetFeatureValue(CommonUsages.devicePosition, out Vector3 controllerPos);
        controller.TryGetFeatureValue(CommonUsages.deviceRotation, out Quaternion controllerRot);

        // Raycast from controller
        Ray aimRay = new Ray(controllerPos, controllerRot * Vector3.forward);

        if (Physics.Raycast(aimRay, out RaycastHit hit, _maxTeleportDistance, _teleportableLayers))
        {
            _isTeleportValid = true;
            _currentRequest = new TeleportRequest
            {
                destinationPosition = hit.point,
                destinationRotation = Quaternion.LookRotation(hit.normal),
                requestType = TeleportRequestType.Destination
            };

            // Show marker
            _teleportMarker.SetActive(true);
            _teleportMarker.transform.position = hit.point;
            _teleportMarker.transform.rotation = Quaternion.LookRotation(hit.normal);
        }
        else
        {
            _isTeleportValid = false;
            _teleportMarker.SetActive(false);
        }
    }

    private void ExecuteTeleport()
    {
        if (_isTeleportValid)
        {
            _teleportProvider.QueueTeleportRequest(_currentRequest);
        }
    }
}
```

### VR Boundary and Play Space

```csharp
// XRPlaySpace for boundary and room-scale management
public class VRPlaySpaceManager : MonoBehaviour
{
    private void CheckPlaySpaceBounds()
    {
        // Get tracked anchors (room boundaries on Quest, guardian on Rift)
        var trackedAnchors = new List<XRTrackedAnchorsSubsystem>();

        // Check if bounds are configured
        var playArea = XRGeneralSettings.Instance?.Manager
            ?.GetLoadedSubsystem<XRTrackedAnchorsSubsystem>();

        if (playArea != null)
        {
            // Get room-scale bounds
            var bounds = playArea.GetBounds();
            if (bounds.HasValue)
            {
                Debug.Log($"Play space bounds: {bounds.Value}");
            }
        }
    }

    // Handle boundary violations
    public void OnBoundaryViolated()
    {
        // User or controller crossed boundary
        // Typically handled by XR system with warning UI
    }

    public void RequestBoundaryDebugVisualization()
    {
        // Some platforms support visualizing boundaries
        // XRGeneralSettings.Instance.Manager.
    }
}
```

## XR Interaction Toolkit

### XR Controller Setup

```csharp
// XRController for device input
public class XRControllerInput : MonoBehaviour
{
    [SerializeField] private XRController _leftController;
    [SerializeField] private XRController _rightController;
    [SerializeField] private InputHelpers.TimedButtonPress _grabButton;
    [SerializeField] private InputHelpers.TimedButtonPress _useButton;

    private void Update()
    {
        ReadControllerInput(_leftController, XRNode.LeftHand);
        ReadControllerInput(_rightController, XRNode.RightHand);
    }

    private void ReadControllerInput(XRController controller, XRNode node)
    {
        if (controller == null) return;

        // Using XRController's automatic input reading
        var inputDevice = controller.inputDevice;

        // Common controller features
        inputDevice.TryGetFeatureValue(CommonUsages.trigger, out float trigger);
        inputDevice.TryGetFeatureValue(CommonUsages.grip, out float grip);
        inputDevice.TryGetFeatureValue(CommonUsages.primaryButton, out bool primary);
        inputDevice.TryGetFeatureValue(CommonUsages.secondaryButton, out bool secondary);
        inputDevice.TryGetFeatureValue(CommonUsages.menu, out bool menu);
        inputDevice.TryGetFeatureValue(CommonUsages.primary2DActor, out Vector2 thumbstick);
    }
}
```

### XR Interactables

```csharp
// IXRInteractor for objects that interact
// IXRInteractable for objects that can be interacted with

// Simple interactable object
public class XRGrabbable : MonoBehaviour, IXRInteractable
{
    private Rigidbody _rb;
    private Collider[] _colliders;

    [SerializeField] private Transform _attachPoint;

    public MonoBehaviour Interactor { get; private set; }

    private void Awake()
    {
        _rb = GetComponent<Rigidbody>();
        _colliders = GetComponentsInChildren<Collider>();
    }

    public void ProcessInteractable(XRInteractionUpdateOrder.UpdatePhase updatePhase)
    {
        if (updatePhase == XRInteractionUpdateOrder.UpdatePhase.Dynamic)
        {
            // Update physics or visual here
        }
    }

    public void OnHoverEntered(XRBaseInteractor interactor)
    {
        // Highlight on hover
    }

    public void OnHoverExited(XRBaseInteractor interactor)
    {
        // Remove highlight
    }

    public void OnSelectEntered(XRBaseInteractor interactor)
    {
        Interactor = interactor;
        // Attach to interactor's hand
        transform.SetParent(interactor.transform);
    }

    public void OnSelectExited(XRBaseInteractor interactor)
    {
        Interactor = null;
        transform.SetParent(null);
        // If was grabbed with physics, may need to match velocity
    }

    // Required interface members
    public bool IsHoverable() => true;
    public bool IsSelectable() => true;
}
```

### XR Interaction Events

```csharp
// XRBaseInteractable events for interaction callbacks
public class XRInteractableEvents : MonoBehaviour, IXRInteractable
{
    public UnityEngine.Events.UnityEvent<XRBaseInteractor, XRBaseInteractable> onHoverEnter;
    public UnityEngine.Events.UnityEvent<XRBaseInteractor, XRBaseInteractable> onHoverExit;
    public UnityEngine.Events.UnityEvent<XRBaseInteractor, XRBaseInteractable> onSelectEnter;
    public UnityEngine.Events.UnityEvent<XRBaseInteractor, XRBaseInteractable> onSelectExit;

    private XRBaseInteractor _currentInteractor;

    public void OnHoverEntered(XRBaseInteractor interactor)
    {
        _currentInteractor = interactor;
        onHoverEnter?.Invoke(interactor, this);
    }

    public void OnHoverExited(XRBaseInteractor interactor)
    {
        onHoverExit?.Invoke(interactor, this);
        if (_currentInteractor == interactor)
            _currentInteractor = null;
    }

    public void OnSelectEntered(XRBaseInteractor interactor)
    {
        onSelectEnter?.Invoke(interactor, this);
    }

    public void OnSelectExited(XRBaseInteractor interactor)
    {
        onSelectExit?.Invoke(interactor, this);
    }

    // IXRInteractable required members
    public Transform transform => base.transform;
    public bool IsHoverable() => true;
    public bool IsSelectable() => true;
    public void ProcessInteractable(XRInteractionUpdateOrder.UpdatePhase phase) { }
}
```

### XR Ray Interactors

```csharp
// Custom ray interactor for teleportation or UI
public class XRCustomRayInteractor : XRBaseInteractor
{
    [SerializeField] private LineRenderer _lineRenderer;
    [SerializeField] private float _rayLength = 10f;
    [SerializeField] private LayerMask _validLayers;
    [SerializeField] private QueryTriggerInteraction _triggerInteraction = QueryTriggerInteraction.Ignore;

    public IXRInteractable CurrentTarget { get; private set; }

    protected override void OnEnable()
    {
        base.OnEnable();
        _lineRenderer.enabled = true;
    }

    protected override void OnDisable()
    {
        base.OnDisable();
        _lineRenderer.enabled = false;
    }

    public override void ProcessInteractable(XRInteractionUpdateOrder.UpdatePhase updatePhase)
    {
        base.ProcessInteractable(updatePhase);

        if (updatePhase == XRInteractionUpdateOrder.UpdatePhase.Dynamic)
        {
            UpdateRaycast();
        }
    }

    private void UpdateRaycast()
    {
        Ray ray = new Ray(transform.position, transform.forward);

        if (Physics.Raycast(ray, out RaycastHit hit, _rayLength, _validLayers, _triggerInteraction))
        {
            _lineRenderer.SetPosition(0, transform.position);
            _lineRenderer.SetPosition(1, hit.point);

            // Check if hit object is interactable
            if (hit.collider.TryGetComponent<IXRInteractable>(out var interactable))
            {
                CurrentTarget = interactable;
            }
        }
        else
        {
            _lineRenderer.SetPosition(0, transform.position);
            _lineRenderer.SetPosition(1, transform.position + transform.forward * _rayLength);
            CurrentTarget = null;
        }
    }

    public override void GetValidTargets(List<IXRInteractable> targets)
    {
        targets.Clear();
        if (CurrentTarget != null)
            targets.Add(CurrentTarget);
    }

    protected override void OnHoverEntered(XRBaseInteractable interactable)
    {
        base.OnHoverEntered(interactable);
    }

    protected override void OnHoverExited(XRBaseInteractable interactable)
    {
        base.OnHoverExited(interactable);
    }
}
```

### XR UI Interaction

```csharp
// XR UI with XR Interaction Toolkit
public class XRUIInteraction : MonoBehaviour
{
    [SerializeField] private XRRayInteractor _leftRayInteractor;
    [SerializeField] private XRRayInteractor _rightRayInteractor;
    [SerializeField] private Canvas _worldSpaceCanvas;

    private void SetupUIRaycasters()
    {
        // Enable raycasters on controllers
        _leftRayInteractor.lineType = XRRayInteractor.LineType.ProjectileCurve;
        _leftRayInteractor.sampleGeometricType = XRRayInteractor.SampleGeometryType.Cylinder;

        _rightRayInteractor.lineType = XRRayInteractor.LineType.ProjectileCurve;

        // For world space canvas UI
        if (_worldSpaceCanvas != null)
        {
            var graphicRaycaster = _worldSpaceCanvas.GetComponent<GraphicRaycaster>();
            if (graphicRaycaster == null)
            {
                graphicRaycaster = _worldSpaceCanvas.AddComponent<GraphicRaycaster>();
            }
            graphicRaycaster.ignoreReversedGraphics = true;
            graphicRaycaster.blockingObjects = GraphicRaycaster.BlockingObjects.All;
        }
    }

    // UI interaction is automatic via XRRayInteractor when pointed at GraphicRaycaster
}
```

### Hand Tracking

```csharp
// XRHandSubsystem for hand tracking (Quest, Vision Pro)
public class XRHandTracking : MonoBehaviour
{
    private XRHandSubsystem _handSubsystem;
    private bool _isHandTrackingActive;

    [SerializeField] private GameObject _leftHandVisual;
    [SerializeField] private GameObject _rightHandVisual;

    private void Start()
    {
        TryGetHandSubsystem();
    }

    private void TryGetHandSubsystem()
    {
        var subsystems = new List<XRHandSubsystem>();
        SubsystemManager.GetInstances(subsystems);

        foreach (var subsystem in subsystems)
        {
            if (subsystem.running)
            {
                _handSubsystem = subsystem;
                _isHandTrackingActive = true;
                break;
            }
        }

        if (_handSubsystem == null)
        {
            Debug.Log("Hand tracking not available");
        }
    }

    private void Update()
    {
        if (!_isHandTrackingActive || _handSubsystem == null) return;

        UpdateHand(_handSubsystem.leftHand, _leftHandVisual);
        UpdateHand(_handSubsystem.rightHand, _rightHandVisual);
    }

    private void UpdateHand(Hand hand, GameObject visual)
    {
        if (!hand.isTracked)
        {
            visual?.SetActive(false);
            return;
        }

        visual?.SetActive(true);

        // Get root position and rotation
        if (hand.rootPose.TryGetPosition(out Vector3 position))
        {
            visual.transform.position = position;
        }

        if (hand.rootPose.TryGetRotation(out Quaternion rotation))
        {
            visual.transform.rotation = rotation;
        }

        // Iterate joints
        foreach (XRHandJoint joint in hand)
        {
            if (joint.TryGetPose(out Pose pose))
            {
                // Update joint transform
                UpdateJointVisual(joint.jointName, pose);
            }
        }
    }

    private void UpdateJointVisual(XRHandJoint jointName, Pose pose)
    {
        // Map joint name to visual transform
        // XRHandJoint.ThumbTip, XRHandJoint.IndexTip, etc.
    }

    // Pinch gesture detection
    private bool IsIndexThumbPinch(Hand hand)
    {
        if (!hand.isTracked) return false;

        // Get index and thumb tip positions
        var indexTip = hand.GetJoint(XRHandJointID.IndexTip);
        var thumbTip = hand.GetJoint(XRHandJointID.ThumbTip);

        if (indexTip.TryGetPosition(out Vector3 indexPos) &&
            thumbTip.TryGetPosition(out Vector3 thumbPos))
        {
            float distance = Vector3.Distance(indexPos, thumbPos);
            return distance < 0.02f; // 2cm pinch threshold
        }

        return false;
    }
}
```

### Eye Tracking

```csharp
// XREyeTrackingSubsystem for gaze and vergence (Vision Pro, Quest Pro)
public class XREyeTracking : MonoBehaviour
{
    private XREyeTrackingSubsystem _eyeTrackingSubsystem;

    [SerializeField] private GameObject _gazeIndicator;
    [SerializeField] private float _gazeTimeout = 0.5f;

    private float _currentGazeDuration;
    private bool _isLookingAtTarget;

    private void Start()
    {
        TryGetEyeTrackingSubsystem();
    }

    private void TryGetEyeTrackingSubsystem()
    {
        var subsystems = new List<XREyeTrackingSubsystem>();
        SubsystemManager.GetInstances(subsystems);

        if (subsystems.Count > 0)
        {
            _eyeTrackingSubsystem = subsystems[0];
        }
    }

    private void Update()
    {
        if (_eyeTrackingSubsystem == null || !_eyeTrackingSubsystem.running)
            return;

        // Get gaze ray
        if (_eyeTrackingSubsystem.TryGetGazeRay(out Ray gazeRay))
        {
            // Cast to scene
            if (Physics.Raycast(gazeRay, out RaycastHit hit))
            {
                HandleGazeHit(hit);
            }
        }

        // Get vergence (convergence depth for 3D)
        if (_eyeTrackingSubsystem.TryGet fixation out Vector3 fixationPoint))
        {
            // Use for depth-aware UI or foveated rendering hints
        }

        // Get了眼 tracking state
        var leftEye = _eyeTrackingSubsystem.leftEye;
        var rightEye = _eyeTrackingSubsystem.rightEye;
    }

    private void HandleGazeHit(RaycastHit hit)
    {
        // Gaze timeout for activation
        if (hit.collider.CompareTag("Gazeable"))
        {
            _isLookingAtTarget = true;
            _currentGazeDuration += Time.deltaTime;

            if (_currentGazeDuration >= _gazeTimeout)
            {
                ActivateGazeTarget(hit.collider.gameObject);
                _currentGazeDuration = 0f;
            }
        }
        else
        {
            _isLookingAtTarget = false;
            _currentGazeDuration = 0f;
        }
    }
}
```

### Body Tracking

```csharp
// XRBodySubsystem for full-body tracking (Quest, PSVR2)
public class XRBodyTracking : MonoBehaviour
{
    private XRBodySubsystem _bodySubsystem;

    [SerializeField] private Skeleton、骨骼[] _skeletonBones;
    [SerializeField] private GameObject _bodyRoot;

    private void Start()
    {
        TryGetBodySubsystem();
    }

    private void TryGetBodySubsystem()
    {
        var subsystems = new List<XRBodySubsystem>();
        SubsystemManager.GetInstances(subsystems);

        if (subsystems.Count > 0)
        {
            _bodySubsystem = subsystems[0];
            _bodySubsystem.Start();
        }
    }

    private void Update()
    {
        if (_bodySubsystem == null || !_bodySubsystem.running) return;

        // Get body pose
        if (_bodySubsystem.TryGetBodyPose(out XRBodyPose bodyPose))
        {
            UpdateBodyFromPose(bodyPose);
        }

        // Get skeleton
        if (_bodySubsystem.TryGetSkeleton(out SkeletonBone[] skeleton))
        {
            UpdateSkeletonFromBones(skeleton);
        }
    }

    private void UpdateBodyFromPose(XRBodyPose pose)
    {
        // Root position
        if (pose.TryGetRootBonePose(out Pose rootPose))
        {
            _bodyRoot.transform.position = rootPose.position;
            _bodyRoot.transform.rotation = rootPose.rotation;
        }

        // Individual joint rotations
        // pose.IsJointTracked(XRBodyJointID.Head)
        // pose.TryGetJointPose(XRBodyJointID.LeftHand, out Pose handPose)
    }

    private void UpdateSkeletonFromBones(SkeletonBone[] skeleton)
    {
        // Map skeleton bones to humanoid rig
        // Use Animator.SetBoneLocalRotation()
    }

    private void OnDestroy()
    {
        _bodySubsystem?.Stop();
    }
}
```

## Device Management

### Meta Quest (Quest 2, Quest 3, Quest Pro)

```csharp
// Meta Quest specific via OVRPlugin or OpenXR
public class MetaQuestManager : MonoBehaviour
{
    // OVRPlugin for Meta-specific features
    // Prefer OpenXR for cross-platform compatibility

    public void ConfigureQuestSettings()
    {
        // Recommended Quest settings:
        // - Stereo Rendering Mode: Single Pass Instanced
        // - Render Resolution: 1.0x (or 0.8x for performance)
        // - Enable PSS (Predictive Stereo Separation)
        // - Target Frame Rate: 72Hz (Quest 2), 90Hz (Quest 3)

        OVRManager.quickActionMenuEnable = true;
        OVRManager.virtual屏幕 = OVRManager.VirtualScreenSpecType.Default;
    }

    // Passthrough (Quest 3/Pro)
    public void EnableQuestPassthrough()
    {
        if (OVRManager.LoadOptEnablePassthrough())
        {
            OVRPluginPassthroughColorStyle colorStyle =
                OVRPluginPassthroughColorStyle.Grayscale;
            OVRPlugin.SetPassthroughColorStyle(colorStyle);
            OVRPlugin.StartPassthrough();
        }
    }

    // Scene API for spatial anchors (Quest)
    public void RequestSceneCapture()
    {
        OVRSpatialAnchor.RequestCaptureScene();
        // User will see scene capture UI
        // Results come back via OVRSpatialAnchor.QueryCompleted
    }

    // Hand tracking
    public void ConfigureHandTracking()
    {
        OVRHandTracking.SetHandNodeTrackingPriority(
            OVRHand.TrackingPriority.HandTracking);
    }

    // Eye tracking (Quest Pro)
    public void ConfigureEyeTracking()
    {
        if (OVRPlugin.eyeTrackingEnabled)
        {
            // Safe to query eye tracking
        }
    }

    // Performance headroom
    public float GetPerformanceHeadroom()
    {
        return OVRPlugin.GetPerfMetrics().AvailableScreenSpace / 100f;
    }

    // Adaptive Performance
    public void ConfigureAdaptivePerformance()
    {
        OVRManager.AdaptivePerformance.EnableAdaptiveMippapLevel = true;
        OVRManager.AdaptivePerformance.EnableAdaptiveFixedFoveatedRendering = true;
    }
}
```

### Apple Vision Pro

```csharp
// Vision Pro via PolySpatial or native APIs
public class VisionProManager : MonoBehaviour
{
    // Vision Pro uses different paradigms:
    // - Volume (not world-locked anchors)
    // - Hand tracking is primary input
    // - Passthrough is default (immersive only when requested)

    public void RequestImmersiveSpace()
    {
        // Use PolySpatial for cross-platform compatibility
        // Or native XROS APIs for Vision Pro specific features

        // Check for visionOS specific subsystem
        var xrSubsystems = new List<XRTrackedAnchorsSubsystem>();
        SubsystemManager.GetInstances(xrSubsystems);
    }

    // Volume configuration
    public void CreateVolume(string volumeName, Vector3 size)
    {
        // Vision Pro renders content in volumes
        // Size determines the render resolution
    }

    // Hand tracking is default input
    public void ConfigureHandTrackingInput()
    {
        // Vision Pro hand tracking is highly accurate
        // No controllers by default
    }

    // Passthrough handling
    public void ConfigurePassthrough()
    {
        // Vision Pro has native passthrough
        // Mixed reality content sits on top
    }
}
```

### HoloLens

```csharp
// HoloLens via Windows XR Plugin or OpenXR
public class HoloLensManager : MonoBehaviour
{
    // QR Code tracking
    public void ConfigureQRTracking()
    {
        var qrSubsystem = XRGeneralSettings.Instance.Manager
            .GetLoadedSubsystem<XRQRCodeSubsystem>();
        if (qrSubsystem != null)
        {
            qrSubsystem.Start();
        }
    }

    // Spatial mapping
    public void ConfigureSpatialMapping()
    {
        var meshSubsystem = XRGeneralSettings.Instance.Manager
            .GetLoadedSubsystem<XRMeshSubsystem>();
        if (meshSubsystem != null)
        {
            meshSubsystem.meshDensity = 0.5f;
            meshSubsystem.requestedMeshVertexAttributes = MeshVertexAttributes.Normals |
                MeshVertexAttributes.Tangents;
            meshSubsystem.Start();
        }
    }

    // Spatial anchors (Azure Spatial Anchors pattern)
    public void CreateSpatialAnchor(Vector3 position, Quaternion rotation)
    {
        var anchorSubsystem = XRGeneralSettings.Instance.Manager
            .GetLoadedSubsystem<XRAnchorSubsystem>();
        // Create and persist anchor
    }

    // Eye tracking (HoloLens 2)
    public void ConfigureEyeTracking()
    {
        var eyeSubsystem = XRGeneralSettings.Instance.Manager
            .GetLoadedSubsystem<XREyeTrackingSubsystem>();
        if (eyeSubsystem != null)
        {
            // Query gaze data
        }
    }

    // Hand tracking (HoloLens 2)
    public void ConfigureHandTracking()
    {
        var handSubsystem = XRGeneralSettings.Instance.Manager
            .GetLoadedSubsystem<XRHandSubsystem>();
        if (handSubsystem != null)
        {
            handSubsystem.Start();
        }
    }
}
```

### PlayStation VR2

```csharp
// PSVR2 via Sony's plugin or OpenXR
public class PSVR2Manager : MonoBehaviour
{
    // Eye tracking
    public void ConfigureEyeTracking()
    {
        // PSVR2 has built-in eye tracking
        // Use via OpenXR or Sony's plugin
    }

    // Haptic feedback
    public void SendHapticFeedback(XRNode controllerNode, float intensity, float duration)
    {
        var device = InputDevices.GetDeviceAtXRNode(controllerNode);
        if (device.TryGetHapticCapabilities(out HapticCapabilities capabilities))
        {
            if (capabilities.supportsImpulse)
            {
                device.SendHapticImpulse(0, intensity, duration); // channel 0
            }
        }
    }

    // Headset haptics
    public void SendHeadsetHaptic(float intensity, float duration)
    {
        var device = InputDevices.GetDeviceAtXRNode(XRNode.Head);
        device.SendHapticImpulse(0, intensity, duration);
    }

    // Controller adaptive triggers
    public void ConfigureTriggerEffect(XRNode controllerNode,
        float triggerResistance, float triggerForce)
    {
        var device = InputDevices.GetDeviceAtXRNode(controllerNode);

        // PSVR2 specific features via Sony plugin
        // or OpenXR haptic extensions
    }

    // Passthrough (PSVR2 doesn't have full passthrough)
    // Similar mixed reality approach not available
}
```

### SteamVR (Index, Vive, Windows Mixed Reality)

```csharp
// SteamVR via OpenXR or legacy SteamVR Plugin
public class SteamVRManager : MonoBehaviour
{
    // OpenXR is preferred
    // Legacy SteamVR plugin still supported

    public void ConfigureSteamVRSettings()
    {
        // Recommended settings:
        // - Render models: Load from SteamVR
        // - Auto-show VR dashboard
        // - Enable standing or seated mode
    }

    // Room-scale boundaries
    public void GetRoomBounds()
    {
        // SteamVR handles boundaries via chaperone system
        // Access via OpenXR or legacy API
    }

    // Index controllers (finger tracking)
    public void ConfigureIndexControllers()
    {
        var leftDevice = InputDevices.GetDeviceAtXRNode(XRNode.LeftHand);
        var rightDevice = InputDevices.GetDeviceAtXRNode(XRNode.RightHand);

        // SteamVR provides skeleton input
        // Use hand skeleton for finger tracking
    }

    // Lighthouse tracking (external trackers)
    public void ConfigureTrackedDevices()
    {
        // SteamVR supports multiple trackers
        // Map to XRNode for consistent input
    }
}
```

## Common Mistakes to Prevent

### Never Hardcode Device-Specific Features

```csharp
// ❌ WRONG — Quest-only code in main logic
void Update()
{
    if (OVRPlugin.productName == OVRProduct.Quest)
    {
        // Quest-specific
    }
}

// ✅ CORRECT — Check subsystem availability
void Update()
{
    var sessionSubsystem = XRGeneralSettings.Instance.Manager
        .GetLoadedSubsystem<XRSessionSubsystem>();
    if (sessionSubsystem?.running == true)
    {
        // Use subsystem APIs
    }
}
```

### Never Use Threading for XR Updates

```csharp
// ❌ WRONG — XR callbacks on background thread
void OnImageCaptured(ThreadedImageData data)
{
    // This runs on separate thread!
    transform.position = data.position; // Thread-safe? NO!
}

// ✅ CORRECT — Marshal to main thread
private Queue<Action> _mainThreadActions = new();

void OnImageCaptured(ThreadedImageData data)
{
    lock (_mainThreadActions)
    {
        _mainThreadActions.Enqueue(() => ProcessImage(data));
    }
}

void Update()
{
    lock (_mainThreadActions)
    {
        while (_mainThreadActions.Count > 0)
        {
            _mainThreadActions.Dequeue()?.Invoke();
        }
    }
}
```

### Never Assume Tracking Data is Valid

```csharp
// ❌ WRONG — Assumes tracking always valid
void Update()
{
    var device = InputDevices.GetDeviceAtXRNode(XRNode.RightHand);
    device.TryGetFeatureValue(CommonUsages.devicePosition, out Vector3 pos);
    transform.position = pos; // May be zero or stale!
}

// ✅ CORRECT — Check tracking state
void Update()
    var device = InputDevices.GetDeviceAtXRNode(XRNode.RightHand);
    
    if (device.TryGetFeatureValue(new InputFeatureUsage<bool>("IsTracked"), out bool isTracked)
        && isTracked)
    {
        if (device.TryGetFeatureValue(CommonUsages.devicePosition, out Vector3 pos))
        {
            transform.position = pos;
        }
    }
    else
    {
        // Show "tracking lost" state or hide object
        gameObject.SetActive(false);
    }
}
```

### Never Ignore Frame Rate Requirements

```csharp
// ❌ WRONG — Unconstrained rendering
void Update()
{
    // Draw everything at any frame rate
}

// ✅ CORRECT — Match XR requirements
void Update()
{
    // Use Application.targetFrameRate = 72 for Quest 2
    // Use Application.targetFrameRate = 90 for Quest 3
    // Use Application.targetFrameRate = 90 for PSVR2
    // Use Application.targetFrameRate = 90 for Index
    // Use dynamic resolution for adaptive performance

    // For Quest: Use OVRManager.display.displayFrequency
    // For others: XRDisplaySubsystem.RefreshRate
}
```

### Never Skip Subsystem Cleanup

```csharp
// ❌ WRONG — No cleanup
void OnDestroy()
{
    // Subsystems keep running!
}

// ✅ CORRECT — Proper lifecycle
void OnEnable()
{
    // Subscribe to subsystem events
}

void OnDisable()
{
    // Unsubscribe from events
}

void OnDestroy()
{
    // Stop and cleanup subsystems
    _session?.Stop();
    _session = null;
}
```

### Never Hardcode Controller Mappings

```csharp
// ❌ WRONG — Hardcoded button mappings
void Update()
{
    if (Input.GetKey(KeyCode.JoystickButton0)) // Quest A button
    {
        Select();
    }
}

// ✅ CORRECT — Use CommonUsages or XR Interaction Toolkit
void Update()
{
    var device = InputDevices.GetDeviceAtXRNode(XRNode.RightHand);
    
    // Works across platforms
    if (device.TryGetFeatureValue(CommonUsages.primaryButton, out bool pressed)
        && pressed)
    {
        Select();
    }

    // Or use XRController directly
}
```

## Response Format

### Code Organization

```csharp
// Structure XR code with clear separation:
// 1. Subsystem initialization and lifecycle
// 2. Input handling (read in Update)
// 3. Interaction logic (process in FixedUpdate for physics)
// 4. Visual updates (apply in Update)

// Good organization:
public class XRFeature : MonoBehaviour
{
    // Section 1: Serialized fields
    [SerializeField] private XRController _controller;
    [SerializeField] private float _speed = 3f;

    // Section 2: Private state
    private XRSubsystem _subsystem;
    private InputDevice _device;

    // Section 3: Lifecycle
    private void Start() => Initialize();
    private void OnEnable() => SubscribeToEvents();
    private void OnDisable() => UnsubscribeFromEvents();
    private void OnDestroy() => Cleanup();

    // Section 4: Input
    private void Update() => ReadInput();

    // Section 5: Logic
    private void FixedUpdate() => ProcessPhysics();

    // Section 6: Helpers
    private void Initialize() { }
    private void SubscribeToEvents() { }
}
```

### When to Use Events vs Polling

| Approach | Use when |
|---------|----------|
| **Events (TryGetXXXEvents)** | UI interactions, rare state changes, input buttons |
| **Polling (TryGetFeatureValue)** | Continuous data (tracking, haptics), every-frame values |

```csharp
// Events for discrete input
var device = InputDevices.GetDeviceAtXRNode(XRNode.RightHand);
device.TryGetFeatureValue(CommonUsages.primaryButton, out bool pressed);

// Polling for continuous tracking
void Update()
{
    device.TryGetFeatureValue(CommonUsages.devicePosition, out Vector3 pos);
    device.TryGetFeatureValue(CommonUsages.deviceRotation, out Quaternion rot);
}
```

### Performance Considerations

```csharp
// 1. Cache device references
private InputDevice _leftHand;
private InputDevice _rightHand;

private void Start()
{
    _leftHand = InputDevices.GetDeviceAtXRNode(XRNode.LeftHand);
    _rightHand = InputDevices.GetDeviceAtXRNode(XRNode.RightHand);
}

// 2. Use TryGetFeatureValue instead of GetFeatureValue
//    TryGet returns false if unavailable (no allocation)
device.TryGetFeatureValue(CommonUsages.devicePosition, out Vector3 pos);

// 3. Limit raycasts in XR
//    Use simple geometry or layers to reduce raycast cost

// 4. Consider single-pass instanced rendering
//    Project Settings > XR Plug-in Management > Windows MR >
//    Render Mode: Single Pass Instanced

// 5. Reduce haptics frequency
//    Don't send haptics every frame — use cooldowns
```

### Testing Checklist

```csharp
// □ Does it work without XR device? (Editor simulation)
// □ Does it work on Quest? (Android build)
// □ Does it work on Vision Pro? (visionOS if available)
// □ Does it work without camera permission? (AR Foundation)
// □ Does it handle tracking loss gracefully?
// □ Does it clean up subsystems on destroy?
// □ Does it respect platform-specific capabilities?
// □ Does input work with both hands?
// □ Does it maintain frame rate on target device?
```

### XR Debug Tips

```csharp
// 1. Check subsystem status
Debug.Log($"XR initialized: {XRGeneralSettings.Instance?.Manager != null}");
Debug.Log($"Session running: {_session?.running}");

// 2. List available devices
var devices = new List<InputDevice>();
InputDevices.GetDevices(devices);
foreach (var device in devices)
{
    Debug.Log($"Device: {device.name} {device.role}");
}

// 3. List loaded subsystems
var sessionSubsystems = new List<XRSessionSubsystem>();
SubsystemManager.GetInstances(sessionSubsystems);
foreach (var s in sessionSubsystems)
{
    Debug.Log($"Subsystem: {s.GetType().Name} running={s.running}");
}

// 4. Enable XR dev mode (Quest)
// OVRManager.SetDeveloperMode(true);

// 5. Use XR Dev Tools package for debugging
```
