# AGENTS.md

## Project Summary

This repository contains ESP32 firmware for the HLK-LD2450 radar sensor on the ESP32-2432S028R CYD display.

The code supports three compile-time node modes:

- `0`: headless radar node, no LCD, serves HTTP JSON
- `1`: LCD remote viewer, polls a remote radar node and renders its JSON data
- `2`: LCD local radar, reads the local LD2450 and renders directly

Default mode is `2`.

## What The AI Should Do

- Prefer small, testable changes.
- Keep the public repo clean and focused on the firmware, README, license, and AI instructions.
- Preserve local-only documentation if the user wants it kept off GitHub.
- Validate build and upload after code changes.
- When changing UI behavior, verify on-device behavior rather than relying on compile success.

## Public Interfaces

- HTTP JSON endpoint: `GET /api/radar`
- Web UI: `GET /`
- WiFi config page: `GET /wifi-config`
- SSID scan: `GET /scan`
- Save WiFi/config: `POST /wifi-save`

## Important Files

- [src/app.cpp](src/app.cpp): runtime orchestration and mode handling
- [src/project_config.h](src/project_config.h): build flags and defaults
- [src/wifi_server.cpp](src/wifi_server.cpp): AP/STA server and JSON API
- [src/remote_radar_client.cpp](src/remote_radar_client.cpp): remote viewer HTTP polling
- [src/lcd_view.cpp](src/lcd_view.cpp): LCD rendering and touch UI
- [src/settings_store.cpp](src/settings_store.cpp): flash-backed settings

## Validation

- Use PlatformIO build and upload.
- Use serial logs to confirm boot mode and WiFi/IP behavior.
- Use browser or `Invoke-WebRequest` against `/api/radar` for HTTP validation.

## Repository Hygiene

Keep these local-only unless the user explicitly wants them published:

- `.pio/`
- `.vscode/`
- internal planning/test docs if they are marked local-only by the user

## License Guidance

Recommend MIT for the public repo unless the user asks for stronger copyleft or a private-only repository.
