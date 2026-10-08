# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Lumos is a Windows system tray application for real-time monitor gamma adjustment. It's a modern C++ reimplementation of Gamminator (Wolfgang Freiler, 2005) with multi-monitor support. Licensed under GPL v2.

**Key technologies:**
- Modern C++20
- CMake build system
- ImGui for UI (DirectX 11 backend)
- Win32 APIs for platform features (gamma control, system tray, global hotkeys)

## Build Commands

### Initial Setup
```bash
# Initialize submodules (ImGui)
git submodule update --init --recursive

# Configure with Visual Studio 2022
cmake -B build -G "Visual Studio 17 2022" -A x64

# Build
cmake --build build --config Release
cmake --build build --config Debug
```

### Running
```bash
# GUI mode
.\build\Release\lumos.exe

# CLI mode (set gamma and exit)
.\build\Release\lumos.exe 1.2

# Show help/version
.\build\Release\lumos.exe --help
.\build\Release\lumos.exe --version
```

### Rebuilding After Changes
```bash
# Rebuild specific configuration
cmake --build build --config Release

# Clean rebuild
cmake --build build --config Release --clean-first
```

## Architecture

### Platform Abstraction Pattern

**Core principle:** Platform-specific code (Win32 APIs) is isolated in `src/platform/win32/`. UI code (ImGui) is isolated in `src/ui/`. The `App` class coordinates between layers but contains no platform-specific code.

```
main.cpp (Win32 entry point, DirectX 11 setup, message loop)
    │
    ├─► app.cpp/h (Application orchestration, business logic)
    │       ├─► config.cpp/h (INI persistence)
    │       ├─► platform/win32/gamma.cpp/h (GetDeviceGammaRamp/SetDeviceGammaRamp)
    │       ├─► platform/win32/tray.cpp/h (Shell_NotifyIcon, popup menu)
    │       └─► platform/win32/hotkeys.cpp/h (RegisterHotKey)
    │
    └─► ui/main_window.cpp/h (ImGui rendering)
```

### Module Responsibilities

- **main.cpp**: Win32/DirectX11 boilerplate, window creation, message loop, ImGui initialization
- **app.cpp/h**: Application state machine, gamma value tracking, orchestrates platform modules
- **cli.cpp/h**: Command line parsing (`--help`, `--version`, gamma values)
- **config.cpp/h**: INI file read/write at `%APPDATA%\Lumos\lumos.ini`
- **platform/win32/gamma.cpp/h**: Multi-monitor enumeration, gamma ramp capture/apply
- **platform/win32/tray.cpp/h**: System tray icon, popup menu (Open/Reset/Exit)
- **platform/win32/hotkeys.cpp/h**: Global hotkey registration (Ctrl+Alt+Up/Down/R)
- **ui/main_window.cpp/h**: ImGui main window with gamma slider and tabs (Monitor, About, Help)
- **ui/theme.h**: VS Code-style color theme for ImGui

### Key Design Patterns

**Crash safety:**
- Original gamma ramps are captured on startup via `Gamma::initialize()`
- Restored in three ways: normal shutdown, `App::resetGamma()`, or unhandled exception filter
- Global `g_crash_gamma` pointer enables restoration from `CrashHandler()` in [main.cpp:41](main.cpp#L41)

**Multi-monitor support:**
- `Gamma` class enumerates all monitors via `EnumDisplayMonitors()`
- Stores original ramps per monitor in `std::vector<MonitorInfo>`
- `applyAll()` applies to all displays, `apply(index)` applies to specific monitor

**ImGui integration:**
- DirectX 11 is chosen (lightweight, ships with Windows, no external DLLs)
- UI rendering happens in [main.cpp:184](main.cpp#L184) via `main_window.render(app)`
- Custom VS Code-style theme applied at startup ([main.cpp:132](main.cpp#L132))

**Minimize to tray:**
- WM_CLOSE and WM_SYSCOMMAND(SC_MINIMIZE) hide window instead of closing ([main.cpp:294-309](main.cpp#L294-L309))
- Only exits when `App::requestExit()` is explicitly called

## Development Roadmap

The project follows a phased roadmap documented in `docs/plans/`:

- **v0.1 "It works"** ✅ - Core gamma adjustment, tray icon, single monitor
- **v0.2 "Usable daily"** ✅ - Multi-monitor, global hotkeys, CLI, About/Help dialogs
- **v0.3 "Polish"** (current) - Test patterns, gamma curve visualization
- **v1.0 "Parity"** - Full Gamminator feature parity (auto-calibration, hotkey customization UI)

When implementing new features, check `docs/plans/` for the current milestone's implementation plan.

## Configuration File

**Location:** `%APPDATA%\Lumos\lumos.ini`

**Current format (v0.2):**
```ini
[Gamma]
LastValue=1.0

[Hotkeys]
Increase=Ctrl+Alt+Up
Decrease=Ctrl+Alt+Down
Reset=Ctrl+Alt+R
```

Config is loaded in `App::initialize()` and saved in `App::shutdown()`.

## Common Patterns

### Adding a new platform feature

1. Create interface in `src/platform/win32/<feature>.h`
2. Implement using Win32 APIs in `src/platform/win32/<feature>.cpp`
3. Add module to `App` class as member variable
4. Initialize in `App::initialize()`, cleanup in `App::shutdown()`
5. Update [CMakeLists.txt:26-36](CMakeLists.txt#L26-L36) to include new source files

### Adding UI components

1. Use ImGui API in `ui/main_window.cpp` or create new file in `ui/`
2. Follow existing tab structure (see `main_window.cpp` for examples)
3. Use `theme.h` colors for consistency with VS Code style
4. UI code should call `App` methods, never directly call platform modules

### Modifying gamma behavior

- Gamma values are clamped to 0.1 - 9.0 range
- All changes go through `App::setGamma()` to ensure consistency
- Always validate that original ramps exist before applying (`Gamma::hasOriginal()`)
- Multi-monitor: `applyAll()` is the default, per-monitor control is available but not exposed in v0.2 UI

## Windows Resource Files

- Icon: [resources/lumos.ico](resources/lumos.ico) - Used for executable icon and tray icon
- Resource script: [resources/lumos.rc](resources/lumos.rc) - Defines icon resources
- Resource header: [resources/resource.h](resources/resource.h) - `IDI_LUMOS` constant

When changing icons, update both `.ico` file and `.rc` file.

## Attribution

This is a derivative work of Gamminator (GPL v2). When adding features:
- Maintain GPL v2 license headers in all source files
- Credit original authors in About dialog
- Keep attribution in README.md and source comments
