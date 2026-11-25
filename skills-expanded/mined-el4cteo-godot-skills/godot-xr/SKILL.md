---
name: godot-xr
description: VR/AR/MR with Godot 4.7 and OpenXR - project setup (Mobile renderer, OpenXR enable, action map), XROrigin3D/XRCamera3D/XRController3D rig, input via actions, hand tracking, passthrough with environment blend modes, refresh rate and foveation, Android XR / Quest / Steam Frame / PCVR export via the vendors plugin, comfort and performance rules. Use for any VR, AR, mixed-reality or OpenXR task.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#). OpenXR runtime or headset for testing.
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# XR with OpenXR (4.7)

Headless runs can't start XR. Code paths still run (the interface reports not initialized), so headsets are needed for real tests.

## Setup
1. Renderer: **Mobile** (recommended for XR in 4.7, desktop and standalone). Compatibility works for low-end standalone. Forward+ works on PCVR but isn't optimized for it.
2. Project Settings: `xr/openxr/enabled = true` and `xr/shaders/enabled = true`. The default action map (`xr/openxr/default_action_map`) has 4 profiles in 4.7: generic controller, touch controller, Pico 4 and hand interaction. Add profiles for other devices in the action map editor.
3. Standalone Android headsets (Quest, Pico, **Android XR**, which is day-one in 4.7) need the **Godot OpenXR Vendors plugin** (Asset Store) and an Android export preset with XR mode = OpenXR plus the vendor's loader enabled. Steam Frame and PCVR go through SteamVR's OpenXR runtime.
4. Scene rig: `XROrigin3D` → `XRCamera3D` + `XRController3D` (`tracker = &"left_hand"` / `&"right_hand"`). One origin per scene. Move the player by moving the origin, never the camera.

## Startup (see the reference)
`var xr := XRServer.find_interface("OpenXR")` → `xr.is_initialized()` (auto-initialized when OpenXR is enabled) → `get_viewport().use_xr = true`. Turn VSync off (`DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)`), because the headset paces frames. Match `Engine.physics_ticks_per_second` to the headset refresh rate (`display_refresh_rate`), so held objects don't jitter. Listen for the OpenXR session signals: `session_begun`, `session_visible`, `session_focussed` (resume), `session_stopping`, `pose_recentered`.

## Input
- Use actions from the action map: `controller.is_button_pressed(&"trigger_click")`, `get_float(&"trigger")`, `get_vector2(&"primary")` (thumbstick), plus the `button_pressed`/`button_released` signals. Action names come from the action map, not hardware buttons.
- Haptics: `controller.trigger_haptic_pulse(&"haptic", frequency, amplitude, duration_sec, delay_sec)`.
- Hand tracking: `XRHandModifier3D` on a hand skeleton (OpenXR hand tracking extension). The hand interaction profile gives pinch and grasp as actions. Body tracking uses `XRBodyModifier3D`.
- Desktop and UI interaction: render 2D UI in a `SubViewport` on a quad and raycast with the controller, or use Godot XR Tools' pointer and viewport-2D-in-3D (addon).

## Passthrough and AR
Check `xr.get_supported_environment_blend_modes()` for `XRInterface.XR_ENV_BLEND_MODE_ALPHA_BLEND`. Set `xr.environment_blend_mode = XR_ENV_BLEND_MODE_ALPHA_BLEND` and `get_viewport().transparent_bg = true`, with an Environment background clear color alpha of 0. `start_passthrough()`/`is_passthrough_enabled()` are **deprecated**. Spatial anchors, planes and markers come from OpenXR spatial entities (4.6+, experimental classes `OpenXR*Tracker`, `OpenXRSpatial*`).

## Performance and comfort (non-negotiable)
- Hold the refresh rate (72/90/120 Hz). A missed frame causes nausea. Budget ~11 ms at 90 Hz, both eyes.
- Mobile renderer, few dynamic lights, baked lighting, no SSR/SSAO/volumetrics, MSAA 2x/4x instead of post AA, and `OpenXRInterface.foveation_level` (0–3) + `foveation_dynamic` on standalone. 4.7's Vulkan subsampled images improve foveated rendering on Mobile.
- Never move the camera without player input. Offer snap turn + teleport, a vignette during smooth locomotion, and seated/standing height calibration (`XRServer.center_on_hmd`).
- Keep UI at 1–3 m and world-locked. Readable text needs a large MSDF font.
- Godot XR Tools (addon) provides locomotion, grabbing, pointers and hands. Use it instead of reinventing them.

XR startup with session handling, controller input and haptics, passthrough toggle (compiled by the tests): [references/patterns.md](references/patterns.md)
