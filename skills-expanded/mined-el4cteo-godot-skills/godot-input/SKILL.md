---
name: godot-input
description: Input in Godot 4.7 for keyboard/mouse, gamepads and touch - InputMap actions, _input vs _unhandled_input, analog movement with deadzones, runtime rebinding with save/load, button prompts per device, gamepad vibration, gyro/accelerometer aiming (4.7), touch gestures and VirtualJoystick (4.7), mouse capture. Use for controls, key bindings, controller support or mobile touch input.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#).
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Input (4.7)

See the project's actions with `python ../godot-core/scripts/project_inspect.py` → `input`. Reuse those action names.

## Actions, not keys
- Define actions in Project Settings → Input Map (stored in `project.godot [input]`). Bind every action to keyboard **and** gamepad from day one. Use physical keycodes (`physical_keycode`) so WASD works on AZERTY.
- Polling in `_physics_process`/`_process`: `Input.is_action_pressed`, `is_action_just_pressed` and `is_action_just_released`.
  Analog values: `Input.get_vector(&"move_left", &"move_right", &"move_up", &"move_down")` returns a circular deadzone and a normalized length. `get_axis(neg, pos)` and `get_action_strength` cover the rest.
- Events: `_unhandled_input(event)` handles gameplay (UI gets first chance in `_gui_input`). `_input` sees everything first, so use it only for global hotkeys and mark them handled with `get_viewport().set_input_as_handled()`. `_shortcut_input` is for menus' shortcuts.
- `event.is_action_pressed(&"jump")` inside event callbacks. Add `allow_echo` for key repeat, and `exact_match` to require exactly those modifiers.
- 4.7: keyboard and mouse events report `event.device == InputEvent.DEVICE_ID_KEYBOARD` / `DEVICE_ID_MOUSE`, no longer 0. Gamepads keep 0..N. Don't compare `device == 0` to mean "keyboard".
- In C#, cache action names: `static readonly StringName Jump = "jump";`.

## Gamepads
- Hot-plug: `Input.joy_connection_changed(device, connected)`, `Input.get_connected_joypads()`, `Input.get_joy_name(device)`, `Input.get_joy_info(device)` (vendor and product IDs). SDL3 drives gamepads since 4.5.
- Rumble: `Input.start_joy_vibration(device, weak, strong, duration)` and `stop_joy_vibration`. On phones, `Input.vibrate_handheld(ms)`.
- **Motion sensors (4.7):** `has_joy_motion_sensors(d)`, `set_joy_motion_sensors_enabled(d, true)`, then `get_joy_gyroscope(d)` (rad/s), `get_joy_accelerometer(d)` and `get_joy_gravity(d)`. Calibrate with `start_joy_motion_sensors_calibration`/`stop_...`. Supported on Windows, Linux, macOS and iOS. Gyro aiming is in the reference.
- Lights (DualShock/DualSense): `has_joy_light`, `set_joy_light(device, color)`.
- 4.7 setting `input_devices/joypads/ignore_joypad_on_unfocused_application` (default off) stops background controller input.
- Several local players: give each player a device ID and read events filtered by `event.device`. The `Input.*` polling functions merge all devices, so poll per device with `Input.get_joy_axis(device, axis)` or route events yourself.

## Rebinding
Change bindings at runtime with `InputMap.action_erase_events`/`action_add_event`, and save them yourself (ConfigFile with serialized events, see the reference). Load them at startup. `InputMap.load_from_project_settings()` resets to defaults. For button prompts, show `event.as_text()` for keys, or map `JoyButton` to your own icon set per controller family (detect it from `get_joy_name`).

## Mouse
- FPS look: `Input.mouse_mode = Input.MOUSE_MODE_CAPTURED` and `InputEventMouseMotion.relative` in `_unhandled_input`. Never use `_process` mouse deltas. Release the mouse on pause or Escape.
- `Input.use_accumulated_input = false` (C#: `UseAccumulatedInput`) gives raw per-event motion for drawing apps. The default accumulation is fine for games.

## Touch and mobile
- `InputEventScreenTouch` (index, pressed, double_tap) and `InputEventScreenDrag` (relative, velocity). Gestures: `InputEventMagnifyGesture` and `InputEventPanGesture`.
- `input_devices/pointing/emulate_mouse_from_touch` is on by default, so buttons work with touch. Turn `emulate_touch_from_mouse` on to test touch on desktop.
- **`VirtualJoystick` (4.7):** set `joystick_mode` (FIXED, DYNAMIC or FOLLOWING), `action_left/right/up/down` (it feeds those actions, so `get_vector` just works), `deadzone_ratio` and `visibility_mode = VISIBILITY_WHEN_TOUCHED`. Signals: `pressed`, `released`, `tapped`, `flicked`.
- `TouchScreenButton` (CanvasItem) triggers an `action` and supports multitouch. Regular `Button` is fine for menus.
- Show touch controls only when touch is present: `DisplayServer.is_touchscreen_available()`.

## Testing input headless
Inject events in tests: `Input.parse_input_event(ev)`, or `Input.action_press(&"jump")` / `action_release`. See `godot-testing-debug`.

Rebinding with persistence, device-aware prompts, gyro aim, touch camera (compiled by the tests): [references/patterns.md](references/patterns.md)
