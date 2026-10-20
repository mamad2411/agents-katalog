# Repository Guidelines

## Project Structure & Module Organization

This is a PlatformIO Arduino firmware project for an ESP32 CYD dashboard.

- `src/main.cpp` initializes queues, events, and FreeRTOS tasks.
- `src/tasks/` contains task ownership boundaries: `NetworkTask` owns WiFi, MQTT, WiFiManager, and reset logic; `UiTask` owns LVGL, TFT, and touch.
- `src/ui/` contains LVGL porting, touch input, dashboard, settings, and reset confirmation screens.
- `src/display/` contains TFT/display bring-up helpers.
- `src/app/` contains app state and MQTT settings persistence.
- `include/` mirrors public headers and configuration, including `include/AppConfig.h`, `include/display/DisplayConfig.h`, and `include/display/TouchConfig.h`.
- `test/` currently contains PlatformIO placeholder documentation, not an active test suite.

## Build, Test, and Development Commands

Use the project-local PlatformIO environment:

```bash
/home/giuseppe/.platformio/penv/bin/platformio run
```

Builds the firmware for `esp32dev`.

```bash
/home/giuseppe/.platformio/penv/bin/platformio run --target upload
```

Builds and uploads to the connected ESP32.

```bash
/home/giuseppe/.platformio/penv/bin/platformio device monitor
```

Opens the serial monitor at `115200` baud.

## Coding Style & Naming Conventions

Use C++ with Arduino conventions and existing repository style. Prefer two-space indentation, `constexpr` constants, namespaces for configuration, and descriptive names such as `TelemetryStaleAfterMs` or `createSettingsPage()`. Keep LVGL object creation out of frequent update loops. Do not introduce unrelated refactors while changing firmware behavior.

## Testing Guidelines

There is no automated test framework yet. At minimum, run `platformio run` before committing firmware changes. For UI/touch changes, verify on the CYD hardware: no clipping, correct touch alignment, and no continuous log spam. For network changes, confirm MQTT subscriptions and WiFiManager behavior remain unchanged unless intentionally modified.

## Commit & Pull Request Guidelines

Commit history uses short imperative messages, for example `Fix CYD touch coordinate mapping` and `Add settings page with credential reset`. Keep commits scoped to one behavior or documentation change.

Pull requests should include:

- concise summary of the change;
- affected modules or screens;
- build result;
- hardware verification notes when display, touch, WiFi, or MQTT behavior changes;
- screenshots or device photos for visible UI changes when useful.

## Architecture & Safety Notes

Preserve task ownership. Only `UiTask` may call LVGL. `NetworkTask` owns WiFiManager, MQTT, Preferences, and restart/reset execution. The MQTT callback must not call LVGL. Do not commit real WiFi passwords, MQTT passwords, tokens, or private credentials.
