# Copilot Instructions for Arduino Project

## Workflow Preferences

- **Testing**: User tests code locally on hardware. Skip compilation verification (`pio run`, etc.)
- **Communication**: Keep responses brief and implementation-focused. Avoid verbose explanations.
- **Token Efficiency**: Minimize unnecessary tool calls and context usage.

## Code Conventions

### File Naming
- Use **underscores** for C++ filenames and folders (e.g., `setup_led.cpp`, `sound_meter/`)
- Avoid hyphens in new code

### Project Structure
- `src/` — Setup implementations in separate folders (e.g., `simple_led/`, `sound_meter/`)
- `lib/` — Reusable components and libraries
- `include/` — Configuration headers (e.g., `config.h` with pin definitions)
- `docs/` — Circuit diagrams, setup guides, refactoring plans

### Setup Pattern
Each circuit gets:
1. **`setup_*.h`** — Public function declarations
   - `void setup_*_init()`
   - `void setup_*_loop()`

2. **`setup_*.cpp`** — Implementation with static helpers
3. **`circuit.md`** — Hardware documentation

### Main Entry Point
`src/main.cpp` dispatches to active setup via `#define ACTIVE_SETUP_*`

## Library Reuse

Before duplicating code, check:
- `lib/led/` — LED classes and functions
- `lib/display/` — 7-segment display (`seven_segment.h`)
- `lib/Light/` — Light-related components
- `lib/basics/` — Basic utilities

## Serial Monitoring

Include debug output with Serial.print() for:
- Initialization messages
- Event triggers (detection, state changes)
- Counter/status values

Use consistent format: `"[COMPONENT] info | Value: X"`
