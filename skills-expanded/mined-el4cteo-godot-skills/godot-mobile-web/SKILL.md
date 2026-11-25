---
name: godot-mobile-web
description: Mobile (Android, iOS) and Web games in Godot 4.7 - renderer choice, safe areas and notches, orientation, touch and virtual keyboard, app lifecycle and back button, battery limits, haptics, permissions, Android/iOS plugins, in-app purchases, Web threads vs no-threads, COOP/COEP hosting, sample audio, JavaScriptBridge, with a local web server and export checker. Use for phone or browser builds.
license: MIT
compatibility: Godot 4.7+ (Web: GDScript only). Python 3.9+ for scripts/serve_web.py.
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Mobile and Web (4.7)

Exporting, signing and store builds are in `godot-export-ci`; touch controls and `VirtualJoystick` in `godot-input`; UI layout in `godot-ui`. This skill covers making the game *behave* on phones and browsers.

**Test a web build:** `python scripts/serve_web.py build/web --check` (threads, sizes, hosting warnings), then `python scripts/serve_web.py build/web` serves it with COOP/COEP headers and prints the URL. Run it in the background; a browser must open it (headless Godot can't render).

## Pick the renderer
| Target | Renderer |
|---|---|
| Web (any) | **Compatibility** (forced: `rendering_method.web = gl_compatibility`) |
| Low-end and old Android, widest reach | Compatibility |
| Modern phones/tablets with Vulkan/Metal, 3D | Mobile (`rendering_method.mobile` override; desktop can stay Forward+) |
Check what you use against the renderer: no SDFGI, volumetric fog or SSR on Mobile/Compatibility (`godot-3d-rendering`). Import textures with ETC2/ASTC (`rendering/textures/vram_compression/import_etc2_astc = true`) for mobile.

## Screen
- Stretch `canvas_items` + aspect `expand` (the 4.7 default for new projects). Design for 16:9 and test 19.5:9 phones and 4:3 tablets. Anchor HUD to corners.
- Orientation: `display/window/handheld/orientation` (landscape, portrait, sensor variants) or `DisplayServer.screen_set_orientation()` at runtime.
- **Safe area**: `DisplayServer.get_display_safe_area()` (screen pixels; Android/iOS only) and `get_display_cutouts()`. Convert to viewport units and pad a `MarginContainer` that wraps the HUD. Backgrounds go edge to edge; buttons stay inside (reference has the script).
- Big fingers: touch targets ≥ 48 dp (about 7–9 mm). Scale the UI with `DisplayServer.screen_get_scale()` or the theme, not tiny fonts.
- `display/window/energy_saving/keep_screen_on` is true by default. Turn it off for menu-only apps.

## Touch and keyboard
- `input_devices/pointing/emulate_mouse_from_touch` (default true) makes Controls and `InputEventMouseButton` code work with taps. For gameplay use `InputEventScreenTouch`/`InputEventScreenDrag` with `index` (multi-touch). Pinch/pan: track two touches yourself (`InputEventMagnifyGesture`/`PanGesture` aren't sent on every platform).
- Test touch on desktop: `emulate_touch_from_mouse = true`.
- Virtual keyboard: `LineEdit.virtual_keyboard_type` (number, email, …) shows it automatically. Shift the UI by `DisplayServer.virtual_keyboard_get_height()` so it doesn't cover the field.

## Lifecycle (where mobile games lose data)
| Event | Do |
|---|---|
| `NOTIFICATION_APPLICATION_PAUSED` | **save now** (iOS kills the app after ~5 s), pause audio and the game |
| `NOTIFICATION_APPLICATION_RESUMED` | show a pause menu; don't resume gameplay by itself |
| `NOTIFICATION_APPLICATION_FOCUS_OUT`/`_IN` | pause on desktop/web tab switch too |
| `NOTIFICATION_WM_GO_BACK_REQUEST` (Android back) | set `get_tree().quit_on_go_back = false` and close menus; quit only from the main menu |
Saves go to `user://` (app-private storage on mobile, IndexedDB on Web). Write to a temp file, then rename (`godot-architecture` save patterns).

## Performance and battery
- Cap the frame rate: `Engine.max_fps = 60` (or 30 for casual games, with a settings toggle). Menus and puzzle games: `application/run/low_processor_mode = true` redraws only on change.
- 3D: `rendering/scaling_3d/scale` 0.6–0.8 on phones, baked lighting (LightmapGI) over real-time GI, few dynamic shadows, MultiMesh for crowds and grass.
- Phones throttle after minutes of load. Test 15–20 minute sessions on a real mid-range device, not just the first minute. Remote debug: the editor's one-click deploy (Android device icon), logs with `adb logcat -s godot`.

## Device features
- Haptics: `Input.vibrate_handheld(duration_ms, amplitude)`, which needs the Android `permissions/vibrate` export option. Gamepads: `start_joy_vibration`.
- Permissions: tick them in the Android export preset, then ask at the moment of use: `OS.request_permission("android.permission.RECORD_AUDIO")`. The result arrives on `get_tree().on_request_permissions_result`. iOS usage strings go in the export preset.
- Open URLs/stores: `OS.shell_open(url)`. Sensors: `Input.get_accelerometer()`, `get_gyroscope()`, `get_gravity()`.

## Plugins, purchases, ads
- Android plugins (v2) are AARs or GDExtensions registered by an `EditorExportPlugin`. They need a **Gradle build** (`gradle_build/use_gradle_build`). Access them with `Engine.has_singleton("Name")` → `Engine.get_singleton("Name")`. Always guard with `has_singleton`, so desktop builds don't crash.
- In-app purchases, Android: the official **GodotGooglePlayBilling** (3.x for 4.2+) or **AndroidIAPP** (Billing Library 8, 4.6+). iOS: StoreKit plugins (e.g. "Godot iOS plugin for In-App purchase" 0.4 for 4.7). Wrap them in one `Store` autoload with the same signals on every platform, and validate purchases on a server for anything valuable.
- Ads/analytics SDKs: use maintained community plugins with a 4.7 build (`godot-addons`), and gate them behind consent (GDPR/ATT).

## Web specifics
- **No C#** for Web in 4.7 (GDScript only). GDExtension needs `variant/extensions_support`.
- **Threads**: `variant/thread_support = false` (the default) works on any host, including itch.io and GitHub Pages, and on iOS Safari. `true` gives smoother audio and `WorkerThreadPool` but needs `Cross-Origin-Opener-Policy: same-origin` + `Cross-Origin-Embedder-Policy: require-corp` from the server (itch.io: tick "SharedArrayBuffer support"; GitHub Pages: enable the PWA and `progressive_web_app/ensure_cross_origin_isolation_headers`).
- **Audio**: browsers start audio only after a user gesture, so put a "click to start" screen first. On Web, players default to **Sample** playback (`audio/general/default_playback_type.web`), which skips bus effects. Set `playback_type = AudioServer.PLAYBACK_TYPE_STREAM` on players that need effects.
- **Size**: the engine `.wasm` is ~37 MB raw, ~8–10 MB with brotli/gzip (the host must compress). Keep the `.pck` small: compressed textures, Ogg audio, and lazy-load levels. A custom template with a build profile strips unused classes (`godot-export-ci`).
- Feature tags: `OS.has_feature("web")`, plus `web_android`/`web_ios` for mobile browsers (show touch controls).
- JavaScript: `JavaScriptBridge.eval()`, `get_interface("localStorage")`, `create_callback()` (keep a reference to the returned object), `download_buffer()` to give a save file to the user.
- Fullscreen, pointer lock and clipboard need a user gesture: call them from an input event handler.

Safe-area container, lifecycle/back button handler, touch pinch-zoom, store wrapper, web bridge and audio unlock (compiled by the tests): [references/patterns.md](references/patterns.md)
