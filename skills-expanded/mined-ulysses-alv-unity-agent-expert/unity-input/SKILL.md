---
name: unity-input
description: >
  Unity 6000.3 LTS input patterns. Covers Input System package,
  InputAction, InputDevice, PlayerInput, InputBindings, actions maps,
  composite bindings, and legacy input migration.
  Trigger: When handling player input, using Input System,
  or migrating from legacy input in Unity 6000.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Handling player input for any platform (PC, Console, Mobile, Web)
- Working with keyboard, mouse, gamepad, touch, or joystick input
- Migrating projects from legacy `Input.GetAxis()` / `Input.GetButton()` to Input System
- Implementing rebindable controls or input settings UI
- Reading input from multiple devices simultaneously
- Using Input System's enhanced debugging and profiling tools
- Unity 6000.3 LTS projects (Input System package 1.8+)

## Critical Rules

### Unity 6000 Uses NEW Input System — NOT Legacy Input

```csharp
// ❌ LEGACY — Unity 6000 deprecates these
Input.GetAxis("Horizontal");
Input.GetAxis("Vertical");
Input.GetButton("Jump");
Input.GetKey(KeyCode.Space);

// ✅ NEW INPUT SYSTEM — Unity 6000 standard
_input.action.ReadValue<Vector2>();
_input.action.IsPressed();
```

**Why:** Unity 6000 LTS ships with Input System as the primary input backend. Legacy `Input.*` APIs are deprecated and may be removed in future releases. Input System provides device abstraction, better debugging, and cross-platform support.

### Input System Requires Package Installation

```
Window > Package Manager > Unity Registry > Input System > Install
```

**Required after install:**

1. **Double-click** `Assets/Settings/Input System Package.asset` (auto-created)
2. Or go to **Edit > Project Settings > Input System Module**
3. Set **Active Input Handling** to `Input System Package (New)` or `Both`
4. **Restart Unity** when prompted

### Always Use Callback-Based Input, NOT Polling in Update

```csharp
// ❌ POLLING — Checks state every frame, harder to manage
void Update()
{
    if (Input.GetButtonDown("Jump"))
    {
        Jump();
    }
}

// ✅ CALLBACK — Responds immediately when input occurs
_input.action.performed += OnJump;

void OnJump(InputAction.CallbackContext context)
{
    Jump();
}
```

**Why:** Callback-based input via `performed`/`started`/`canceled` callbacks ensures immediate response and proper Input System phase handling. Polling bypasses the action phase system and can miss input.

### InputAction.ReadValue<T>() vs .triggered / .WasPressedThisFrame

```csharp
// ✅ ReadValue — Get the actual input value (axis, vector, etc.)
Vector2 move = _moveAction.ReadValue<Vector2>();

// ✅ IsPressed — True while the input is held (gamepad, key held)
bool isHeld = _interactAction.IsPressed();

// ❌ Don't use .WasPressedThisFrame() or .triggered on InputAction
// These are for InputActionMap, not individual actions
```

**Why:** `ReadValue<T>()` returns the current value from the device. `IsPressed()` checks if a control is currently pressed. The legacy `GetButtonDown` equivalent is handled by the `started`/`performed` callbacks.

## InputAction

### Creating InputActions (C#)

```csharp
using UnityEngine;
using UnityEngine.InputSystem;

// Option 1: Asset Reference (recommended for complex projects)
[SerializeField] private InputActionAsset _inputAsset;

void Awake()
{
    // Get action from asset by name/path
    var moveAction = _inputAsset.FindAction("Gameplay/Move");
    moveAction.performed += OnMove;
    moveAction.started += OnMove;
    moveAction.canceled += OnMove;
}

void OnEnable()
{
    _inputAsset.Enable();
}

void OnDisable()
{
    _inputAsset.Disable();
}
```

```csharp
// Option 2: Programmatic Actions (simple prototypes)
private InputAction _jumpAction;

void SetupInput()
{
    _jumpAction = new InputAction(
        name: "Jump",
        binding: "<Keyboard>/space"
    );
    
    _jumpAction.performed += context => Jump();
    _jumpAction.Enable();
}
```

### InputAction Phase Flow

```
Disabled → Waiting → Started → Performed → Canceled → Waiting
                    ↓
               (input lost before completion)
                    ↓
                 Canceled
```

| Phase | When | Use for |
|-------|------|---------|
| `Started` | Input begins (button pressed) | Starting animations, charging |
| `Performed` | Input completes (value available) | Execute action |
| `Canceled` | Input ends (button released OR cancelled) | Reset states |

```csharp
private InputAction _shootAction;

void Setup()
{
    _shootAction.performed += OnShootPerformed;
    _shootAction.started += OnShootStarted;
    _shootAction.canceled += OnShootCanceled;
}

void OnShootStarted(InputAction.CallbackContext context)
{
    // Button just pressed — start charging
    _isCharging = true;
    _chargeStartTime = Time.time;
}

void OnShootPerformed(InputAction.CallbackContext context)
{
    // Button released after press — fire!
    float chargeTime = Time.time - _chargeStartTime;
    Fire(chargeTime);
    _isCharging = false;
}

void OnShootCanceled(InputAction.CallbackContext context)
{
    // Released without firing OR input interrupted
    _isCharging = false;
}
```

### Action Types

#### Value Action (continuous input)

```csharp
// Value — continuous input like movement axes, mouse delta
private InputAction _moveAction;

void Setup()
{
    _moveAction = new InputAction(
        name: "Move",
        type: InputActionType.Value,
        binding: "<Keyboard>/w"
    );
    
    // For composite bindings (WASD), add multiple bindings to same action
    _moveAction.AddCompositeBinding("2DVector")
        .With("Up", "<Keyboard>/w")
        .With("Down", "<Keyboard>/s")
        .With("Left", "<Keyboard>/a")
        .With("Right", "<Keyboard>/d");
    
    _moveAction.performed += OnMove;
    _moveAction.Enable();
}

void OnMove(InputAction.CallbackContext context)
{
    // ReadValue returns Vector2 for 2D vector composite
    Vector2 direction = context.ReadValue<Vector2>();
    Debug.Log($"Move: {direction}");
}
```

#### Button Action (discrete input)

```csharp
// Button — discrete press/release events
private InputAction _interactAction;

void Setup()
{
    _interactAction = new InputAction(
        name: "Interact",
        type: InputActionType.Button,
        binding: "<Keyboard>/e"
    );
    
    _interactAction.performed += OnInteract;
    _interactAction.Enable();
}

void OnInteract(InputAction.CallbackContext context)
{
    Debug.Log("Interact pressed!");
}
```

#### Pass Through (unprocessed input)

```csharp
// PassThrough — raw input without action processing
// Use for input that needs to map 1:1 with device
private InputAction _mouseAction;

void Setup()
{
    _mouseAction = new InputAction(
        name: "Mouse",
        type: InputActionType.PassThrough,
        binding: "<Mouse>/position"
    );
    
    _mouseAction.performed += OnMouseMove;
    _mouseAction.Enable();
}

void OnMouseMove(InputAction.CallbackContext context)
{
    Vector2 position = context.ReadValue<Vector2>();
    // Raw mouse position, no action processing
}
```

### Bindings

#### Simple Bindings

```csharp
// Keyboard
new InputAction(binding: "<Keyboard>/space");
new InputAction(binding: "<Keyboard>/enter");
new InputAction(binding: "<Keyboard>/a");

// Mouse
new InputAction(binding: "<Mouse>/leftButton");
new InputAction(binding: "<Mouse>/rightButton");
new InputAction(binding: "<Mouse>/delta"); // Movement delta
new InputAction(binding: "<Mouse>/scroll/y"); // Scroll wheel

// Gamepad
new InputAction(binding: "<Gamepad>/buttonSouth"); // A/X
new InputAction(binding: "<Gamepad>/buttonNorth"); // Y/Triangle
new InputAction(binding: "<Gamepad>/leftStick");
new InputAction(binding: "<Gamepad>/rightStick");
new InputAction(binding: "<Gamepad>/dpad");
new InputAction(binding: "<Gamepad>/leftTrigger");
new InputAction(binding: "<Gamepad>/rightTrigger");

// Touch
new InputAction(binding: "<Touchscreen>/touch0/position");
new InputAction(binding: "<Touchscreen>/touch0/phase"); // Began/Moved/Ended
```

#### Composite Bindings (WASD, etc.)

```csharp
// 2D Vector Composite — WASD movement
var moveAction = new InputAction(name: "Move");
moveAction.AddCompositeBinding("2DVector")
    .With("Up", "<Keyboard>/w")
    .With("Down", "<Keyboard>/s")
    .With("Left", "<Keyboard>/a")
    .With("Right", "<Keyboard>/d");

// 1D Axis Composite — mouse sensitivity
var scrollAction = new InputAction(name: "Scroll");
scrollAction.AddCompositeBinding("1DAxis")
    .With("Positive", "<Mouse>/scroll/y")
    .With("Negative", "<Keyboard>/pageDown");
```

#### Binding Masking

```csharp
// Filter which devices/bindings are active
_inputAsset.devices = new[] { Keyboard.current };

// Or per-action
moveAction.bindingMask = InputBinding.MaskByGroup("Keyboard");
```

### InputActionAsset (Input Actions Asset File)

Create via: **Assets > Create > Input Actions**

```csharp
// Load from Resources
[SerializeField] private InputActionAsset _inputAsset;

// Or load programmatically
var json = Resources.Load<TextAsset>("InputActions");
var asset = InputActionAsset.FromJson(json);
```

### PlayerInput Component

```csharp
using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerController : MonoBehaviour
{
    private PlayerInput _playerInput;
    
    private void Awake()
    {
        _playerInput = GetComponent<PlayerInput>();
    }
    
    // Called by PlayerInput based on action map name
    public void OnMove(InputAction.CallbackContext context)
    {
        Vector2 value = context.ReadValue<Vector2>();
        // Handle movement
    }
    
    public void OnJump(InputAction.CallbackContext context)
    {
        if (context.performed)
        {
            Jump();
        }
    }
    
    public void OnLook(InputAction.CallbackContext context)
    {
        Vector2 delta = context.ReadValue<Vector2>();
        // Handle camera rotation
    }
}
```

**Setup:**
1. Add `PlayerInput` component to GameObject
2. Assign `Default Input Actions` asset
3. Set `Default Map` to your action map name
4. Enable `Invoke Unity Events` or `Send Messages`

## InputDevice

### Accessing Devices

```csharp
// Current device (last device used)
Keyboard.current; // Keyboard.current.IsPressed(KeyCode.Space)
Mouse.current;     // Mouse.current.position.ReadValue()
Gamepad.current;   // Gamepad.current.leftStick.ReadValue()
Touchscreen.current;

// Check if device is connected
if (Keyboard.current != null)
{
    // Keyboard is connected
}

// Check device connection changes
InputDeviceChangeListener.OnDeviceChange += (device, change) =>
{
    if (change == InputDeviceChange.Added)
        Debug.Log($"Device added: {device.displayName}");
    if (change == InputDeviceChange.Removed)
        Debug.Log($"Device removed: {device.displayName}");
};
```

### Device Layouts

```csharp
// All devices are organized by "layout"
// Common layouts:
//   Keyboard, Mouse, Gamepad, Touchscreen, Joystick, Pen, Trackpad

// Find all devices of a type
foreach (var gamepad in Gamepad.all)
{
    Debug.Log($"Gamepad: {gamepad.displayName}");
}

// Device description
Gamepad gamepad = Gamepad.current;
Debug.Log($"Name: {gamepad.displayName}");
Debug.Log($"Layout: {gamepad.layout}");
Debug.Log($"Device ID: {gamepad.deviceId}");
```

### Gamepad (HID Standard)

```csharp
// Left stick
Vector2 leftStick = Gamepad.current.leftStick.ReadValue();

// Right stick
Vector2 rightStick = Gamepad.current.rightStick.ReadValue();

// D-Pad (as 2D vector)
Vector2 dpad = Gamepad.current.dpad.ReadValue();

// Buttons (as float 0-1 or bool)
float aButton = Gamepad.current.buttonSouth.ReadValue<float>(); // A/X
bool aPressed = Gamepad.current.buttonSouth.IsPressed();

// Triggers (0-1 range)
float leftTrigger = Gamepad.current.leftTrigger.ReadValue<float>();
float rightTrigger = Gamepad.current.rightTrigger.ReadValue<float>();

// Bumpers
float leftBumper = Gamepad.current.leftBumper.ReadValue<float>();
float rightBumper = Gamepad.current.rightBumper.ReadValue<float>();

// Analog sticks as buttons (threshold)
bool leftStickClick = Gamepad.current.leftStickButton.IsPressed();
bool rightStickClick = Gamepad.current.rightStickButton.IsPressed();
```

### Keyboard

```csharp
// Individual keys
bool spacePressed = Keyboard.current.spaceKey.IsPressed();
bool enterPressed = Keyboard.current.enterKey.IsPressed();

// Check with KeyCode-style enum
if (Keyboard.current[Key.Space].IsPressed())
{
    // Space is pressed
}

// Modifier keys
bool ctrl = Keyboard.current.leftCtrlKey.IsPressed();
bool shift = Keyboard.current.rightShiftKey.IsPressed();
bool alt = Keyboard.current.leftAltKey.IsPressed();

// Any key press
bool anyKey = Keyboard.current.anyKey.IsPressed;

// Text input (for chat, naming)
void OnTextInput(InputAction.CallbackContext context)
{
    string chars = context.GetInputEvent<char>().character;
}
```

### Mouse

```csharp
// Position (screen space)
Vector2 position = Mouse.current.position.ReadValue();

// Delta movement
Vector2 delta = Mouse.current.delta.ReadValue();

// Scroll wheel
Vector2 scroll = Mouse.current.scroll.ReadValue();

// Buttons
bool leftClick = Mouse.current.leftButton.IsPressed();
bool rightClick = Mouse.current.rightButton.IsPressed();
bool middleClick = Mouse.current.middleButton.IsPressed();

// Click count (double-click detection)
int clickCount = Mouse.current.clickCount.ReadValue<int>();
```

### Touch

```csharp
Touchscreen touchscreen = Touchscreen.current;

// Primary touch position
Vector2 position = touchscreen.primaryTouch.position.ReadValue();

// Touch phase
TouchPhase phase = touchscreen.primaryTouch.phase.ReadValue<TouchPhase>();

switch (phase)
{
    case TouchPhase.Began:
        // Touch started
        break;
    case TouchPhase.Moved:
        // Touch moved
        break;
    case TouchPhase.Stationary:
        // Touch held without moving
        break;
    case TouchPhase.Ended:
        // Touch ended
        break;
    case TouchPhase.Canceled:
        // Touch interrupted
        break;
}

// Multi-touch (up to 10 touches)
for (int i = 0; i < Touchscreen.current.touches.Length; i++)
{
    var touch = touchscreen.touches[i];
    if (touch.phase.ReadValue<TouchPhase>() != TouchPhase.None)
    {
        Vector2 pos = touch.position.ReadValue();
        // Process touch
    }
}
```

### InputEvent

```csharp
// Access the raw InputEvent for advanced scenarios
void OnAction(InputAction.CallbackContext context)
{
    InputEvent eventPtr = context.eventPtr;
    
    if (eventPtr.IsA<StateEvent>())
    {
        // Input state changed
    }
    else if (eventPtr.IsA<DeltaStateEvent>())
    {
        // Partial state update (mouse delta, etc.)
    }
}
```

## Legacy Migration

### Migration Overview

| Legacy API | Input System Equivalent |
|------------|--------------------------|
| `Input.GetButton("Jump")` | `action.IsPressed()` or callback |
| `Input.GetButtonDown("Jump")` | `action.performed` callback |
| `Input.GetAxis("Horizontal")` | `action.ReadValue<Vector2>()` |
| `Input.GetMouseButton(0)` | `Mouse.current.leftButton.IsPressed()` |
| `Input.mousePosition` | `Mouse.current.position.ReadValue<Vector2>()` |
| `Input.GetKey(KeyCode.Space)` | `Keyboard.current.spaceKey.IsPressed()` |

### Step-by-Step Migration

#### 1. Install Input System Package

```
Window > Package Manager > Unity Registry > Input System > Install
```

#### 2. Create Input Actions Asset

```
Assets > Create > Input Actions
Name it: "PlayerInputActions"
```

#### 3. Define Action Maps and Actions

```
PlayerInputActions (asset)
├── Gameplay (action map)
│   ├── Move (Value, Vector2)
│   ├── Jump (Button)
│   ├── Look (Value, Vector2)
│   └── Interact (Button)
└── UI (action map)
    ├── Navigate (Value, Vector2)
    ├── Submit (Button)
    └── Cancel (Button)
```

#### 4. Add Bindings

```
Move:
  - <Keyboard>/w
  - <Keyboard>/a
  - <Keyboard>/s
  - <Keyboard>/d
  - <Gamepad>/leftStick

Jump:
  - <Keyboard>/space
  - <Gamepad>/buttonSouth

Look:
  - <Mouse>/delta
  - <Gamepad>/rightStick

Interact:
  - <Keyboard>/e
  - <Gamepad>/buttonNorth
```

#### 5. Update C# Scripts

```csharp
// BEFORE (Legacy)
public class PlayerController : MonoBehaviour
{
    public float speed = 5f;
    
    void Update()
    {
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");
        Vector3 movement = new Vector3(h, 0, v);
        transform.Translate(movement * speed * Time.deltaTime);
        
        if (Input.GetButtonDown("Jump"))
        {
            Jump();
        }
    }
    
    void Jump() { /* ... */ }
}
```

```csharp
// AFTER (Input System)
using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerController : MonoBehaviour
{
    [SerializeField] private InputActionAsset _inputAsset;
    [SerializeField] private float _speed = 5f;
    
    private InputAction _moveAction;
    private InputAction _jumpAction;
    
    private void Awake()
    {
        // Get actions from asset
        _moveAction = _inputAsset.FindAction("Gameplay/Move");
        _jumpAction = _inputAsset.FindAction("Gameplay/Jump");
        
        // Subscribe to callbacks
        _moveAction.performed += OnMove;
        _moveAction.canceled += OnMove;
        _jumpAction.performed += OnJump;
    }
    
    private void OnEnable()
    {
        _inputAsset.Enable();
    }
    
    private void OnDisable()
    {
        _inputAsset.Disable();
    }
    
    private void OnMove(InputAction.CallbackContext context)
    {
        Vector2 direction = context.ReadValue<Vector2>();
        Vector3 movement = new Vector3(direction.x, 0, direction.y);
        transform.Translate(movement * _speed * Time.deltaTime);
    }
    
    private void OnJump(InputAction.CallbackContext context)
    {
        Jump();
    }
    
    void Jump() { /* ... */ }
}
```

### Dual Input Handling (During Migration)

```csharp
// Support both old and new input during transition
public class PlayerController : MonoBehaviour
{
    [SerializeField] private InputActionAsset _inputAsset;
    private InputAction _moveAction;
    private InputAction _jumpAction;
    
    private void Awake()
    {
        if (_inputAsset != null)
        {
            SetupInputSystem();
        }
    }
    
    void SetupInputSystem()
    {
        _moveAction = _inputAsset.FindAction("Gameplay/Move");
        _jumpAction = _inputAsset.FindAction("Gameplay/Jump");
        
        _moveAction.performed += ctx => _moveInput = ctx.ReadValue<Vector2>();
        _moveAction.canceled += ctx => _moveInput = Vector2.zero;
        _jumpAction.performed += ctx => _jumpPressed = true;
        
        _inputAsset.Enable();
    }
    
    Vector2 _moveInput;
    bool _jumpPressed;
    
    void Update()
    {
        Vector2 move;
        
        #if ENABLE_LEGACY_INPUT_MANAGER
        // Use legacy input if Input System not configured
        if (_moveAction == null)
        {
            move = new Vector2(Input.GetAxis("Horizontal"), Input.GetAxis("Vertical"));
            if (Input.GetButtonDown("Jump")) _jumpPressed = true;
        }
        else
        #endif
        {
            move = _moveInput;
        }
        
        // Common movement logic
        Vector3 movement = new Vector3(move.x, 0, move.y);
        transform.Translate(movement * 5f * Time.deltaTime);
    }
}
```

### Project Settings for Migration

```csharp
// Edit > Project Settings > Player > Other Settings
// Active Input Handling:
//   - "Input System Package (New)" — Input System only
//   - "Both" — Support both during migration
```

### Common Migration Issues

| Issue | Legacy | New Input System |
|-------|--------|------------------|
| "Jump only fires once" | `GetButtonDown` in Update | Use `performed` callback, not `IsPressed()` in Update |
| "Movement is sluggish" | `GetAxis` with sensitivity | Adjust action value sensitivity in asset |
| "Mouse look is too fast" | Fixed sensitivity | Divide `Mouse.current.delta.ReadValue()` by sensitivity |
| "Gamepad stick dead zone" | Manual in code | Built-in dead zone on binding |

## Common Mistakes to Prevent

### Mistake 1: Forgetting to Enable Input Actions

```csharp
// ❌ WRONG — Actions disabled, nothing works
void Start()
{
    _moveAction.performed += OnMove;
    // Forgot to call Enable!
}

// ✅ CORRECT — Enable after subscribing
void OnEnable()
{
    _inputAsset.Enable();
}
```

### Mistake 2: Not Unsubscribing from Callbacks

```csharp
// ❌ WRONG — Memory leak, duplicate callbacks
void OnEnable()
{
    _action.performed += OnAction; // Adding without removing
}

// ✅ CORRECT — Unsubscribe in OnDisable
void OnEnable()
{
    _action.performed += OnAction;
}

void OnDisable()
{
    _action.performed -= OnAction;
}
```

### Mistake 3: Reading Values in Update Instead of Callbacks

```csharp
// ❌ WRONG — Polling bypasses action system
void Update()
{
    if (_jumpAction.IsPressed()) // Works but not idiomatic
    {
        Jump();
    }
}

// ✅ CORRECT — Use callbacks for discrete actions
void Setup()
{
    _jumpAction.performed += OnJump;
}

void OnJump(InputAction.CallbackContext context)
{
    Jump();
}
```

### Mistake 4: Wrong ReadValue Type

```csharp
// ❌ WRONG — Type mismatch causes exception
Vector2 move = _moveAction.ReadValue<Vector3>(); // Wrong type!

// ✅ CORRECT — Match the action's value type
// For Value action returning Vector2:
Vector2 move = _moveAction.ReadValue<Vector2>();

// For Button action returning float:
float pressed = _interactAction.ReadValue<float>();
```

### Mistake 5: Not Handling Null Device

```csharp
// ❌ WRONG — Crash if no keyboard connected
bool space = Keyboard.current.spaceKey.IsPressed();

// ✅ CORRECT — Check for null
if (Keyboard.current != null)
{
    bool space = Keyboard.current.spaceKey.IsPressed();
}

// Or use ?. for nullable access
bool space = Keyboard.current?.spaceKey.IsPressed() ?? false;
```

### Mistake 6: Action Maps Not Matching Send Message Method Names

```csharp
// If using PlayerInput with Send Messages:
// The action name must EXACTLY match the method name

// Asset: action named "Jump"
// ✅ Correct method name:
public void OnJump(InputAction.CallbackContext context) { }

// ❌ Wrong — method not called:
public void OnPlayerJump(InputAction.CallbackContext context) { }
```

### Mistake 7: Ignoring Input Devices Configuration

```csharp
// ❌ WRONG — Only Gamepad works but Keyboard bindings exist
_inputAsset.devices = new[] { Gamepad.current };

// ✅ CORRECT — Let Input System auto-detect or specify all needed devices
_inputAsset.devices = new InputDevice[]
{
    Keyboard.current,
    Mouse.current,
    Gamepad.current
};

// Or use default (all devices):
_inputAsset.devices = null; // Default: all devices
```

## Input System Debugging

### Input Debugger Window

`Window > Analysis > Input Debugger`

- View all connected devices
- See device input in real-time
- Inspect action bindings
- Test input without running play mode

### Debug Log Input

```csharp
// Log all input events
void OnEnable()
{
    InputSystem.onEvent += OnInputEvent;
}

void OnInputEvent(InputEventPtr eventPtr, InputDevice device)
{
    Debug.Log($"Event from {device.displayName}: {eventPtr}");
}

void OnDisable()
{
    InputSystem.onEvent -= OnInputEvent;
}
```

### Visualize Input in Play Mode

```csharp
// Add to any GameObject to see input visually
using UnityEngine.InputSystem;

public class InputDebugger : MonoBehaviour
{
    void Update()
    {
        if (Gamepad.current != null)
        {
            Vector2 ls = Gamepad.current.leftStick.ReadValue();
            Vector2 rs = Gamepad.current.rightStick.ReadValue();
            float lt = Gamepad.current.leftTrigger.ReadValue<float>();
            float rt = Gamepad.current.rightTrigger.ReadValue<float>();
            
            Debug.DrawLine(transform.position, transform.position + Vector3.right * ls.x, Color.red);
            Debug.DrawLine(transform.position, transform.position + Vector3.forward * ls.y, Color.blue);
        }
    }
}
```

### Test Input Without GameObject

```csharp
// Use InputTestFixture for tests
using UnityEngine.InputSystem;
using UnityEngine.TestTools;
using NUnit.Framework;

[TestFixture]
public class PlayerInputTests
{
    private InputTestFixture _fixture;
    
    [SetUp]
    public void Setup()
    {
        _fixture = new InputTestFixture();
        _fixture.SetUp();
    }
    
    [TearDown]
    public void TearDown()
    {
        _fixture.TearDown();
    }
    
    [Test]
    public void Jump_Performed_WhenSpacePressed()
    {
        var keyboard = InputSystem.AddDevice<Keyboard>();
        
        var jumpAction = new InputAction("Jump", binding: "<Keyboard>/space");
        bool jumped = false;
        jumpAction.performed += ctx => jumped = true;
        jumpAction.Enable();
        
        // Press space
        Press(kboard.spaceKey);
        Assert.IsTrue(jumped);
    }
}
```

## Rebindable Input

### Runtime Rebinding

```csharp
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.UI;

public class InputRebinder : MonoBehaviour
{
    [SerializeField] private InputActionAsset _inputAsset;
    [SerializeField] private Text _bindingText;
    
    private InputAction _targetAction;
    private int _bindingIndex;
    
    public void StartRebinding(InputAction action, int bindingIndex)
    {
        _targetAction = action;
        _bindingIndex = bindingIndex;
        
        // Remove current binding
        _targetAction.Disable();
        
        // Perform interactive rebind
        _targetAction.PerformInteractiveRebinding(_bindingIndex)
            .WithTargetBinding(_bindingIndex)
            .OnComplete(callback => {
                callback.Dispose();
                _targetAction.Enable();
                UpdateBindingText();
            })
            .Start();
    }
    
    public void ResetToDefault()
    {
        _targetAction.RemoveBindingOverride(_bindingIndex);
        UpdateBindingText();
    }
    
    void UpdateBindingText()
    {
        var binding = _targetAction.bindings[_bindingIndex];
        _bindingText.text = binding.ToDisplayString();
    }
}
```

### Save/Load Rebinds

```csharp
// Save
public void SaveRebinds()
{
    string rebinds = _inputAsset.SaveBindingOverridesAsJson();
    PlayerPrefs.SetString("InputRebinds", rebinds);
}

// Load
public void LoadRebinds()
{
    string rebinds = PlayerPrefs.GetString("InputRebinds", "");
    if (!string.IsNullOrEmpty(rebinds))
    {
        _inputAsset.LoadBindingOverridesFromJson(rebinds);
    }
}
```

## Response Format

When responding to Unity input questions:

1. **Lead with the Input System approach** — Unity 6000 standard
2. **Show working code** — Complete, compilable examples
3. **Include binding syntax** — `<Keyboard>/space`, `<Gamepad>/buttonSouth`
4. **Explain the callback flow** — `performed`/`started`/`canceled`
5. **Mention device access** — `Keyboard.current`, `Gamepad.current`
6. **Note migration path** — Legacy vs new Input System
7. **Include common mistakes** — Null checks, enabling, unsubscribing

### Template for Input Questions

```csharp
using UnityEngine;
using UnityEngine.InputSystem;

public class InputHandler : MonoBehaviour
{
    [SerializeField] private InputActionAsset _inputAsset;
    
    private InputAction _action;
    
    private void Awake()
    {
        _action = _inputAsset.FindAction("ActionMap/ActionName");
        _action.performed += OnAction;
        _action.started += OnActionStarted;
        _action.canceled += OnActionCanceled;
    }
    
    private void OnEnable()
    {
        _inputAsset.Enable();
    }
    
    private void OnDisable()
    {
        _action.performed -= OnAction;
        _action.started -= OnActionStarted;
        _action.canceled -= OnActionCanceled;
        _inputAsset.Disable();
    }
    
    private void OnAction(InputAction.CallbackContext context)
    {
        // Read value based on action type
        var value = context.ReadValue<ValueType>();
    }
    
    private void OnActionStarted(InputAction.CallbackContext context)
    {
        // Input began
    }
    
    private void OnActionCanceled(InputAction.CallbackContext context)
    {
        // Input ended
    }
}
```

## Unity 6000 Input System Package Versions

| Package Version | Unity 6000 Compatibility | Features |
|-----------------|-------------------------|----------|
| 1.7.x | 6000.0+ | Basic Input System |
| 1.8.x | 6000.1+ | Enhanced debug tools |
| 1.9.x | 6000.2+ | Performance improvements |
| 1.10.x | 6000.3 LTS | Current LTS stable |

### Check Installed Version

```csharp
// Via code
var packageInfo = UnityEditor.PackageManager.PackageInfo.FindForAssembly(typeof(UnityEngine.InputSystem.InputSystem).Assembly);
Debug.Log($"Input System Version: {packageInfo.version}");
```

### Update Input System

```
Window > Package Manager > Unity Registry
Find "Input System" > Select version > Update
```

## Best Practices Summary

1. **Use InputActionAsset** — Define actions in editor for complex projects
2. **Prefer Callbacks** — Subscribe to `performed`/`started`/`canceled` events
3. **Enable/Disable Pairs** — Always unsubscribe and disable input
4. **Check for Null Device** — `Keyboard.current != null` before access
5. **Use Correct ReadValue Type** — Match action's value type
6. **Debug with Input Debugger** — `Window > Analysis > Input Debugger`
7. **Test All Devices** — Keyboard, mouse, gamepad, touch
8. **Save Binding Overrides** — PlayerPrefs or PlayerData for rebinds
9. **Use Composite Bindings** — WASD, 2D vectors for natural input
10. **Migrate Incrementally** — Use "Both" active input handling during transition

(End of file - 1007 lines)
