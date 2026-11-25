# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Speede is an arcade-style reaction game built with Arduino, inspired by the Finnish TV game show "Speden Spelit." Players press illuminated buttons in the correct order as the game speeds up. The project targets **Arduino UNO** (current pin config) with a shift-register-driven 4-digit seven segment display; it also supports Arduino Mega 2560 (commented-out pin mappings).

## Build & Upload

This is an Arduino project. Open `speede.ino` in Arduino IDE (or use arduino-cli):

```bash
# Compile
arduino-cli compile --fqbn arduino:avr:uno speede.ino

# Upload
arduino-cli upload -p <PORT> --fqbn arduino:avr:uno speede.ino
```

The project depends on the **SevSegShift** library (shift-register variant of SevSeg) for the seven segment display: https://github.com/bridystone/SevSegShift

## Architecture

The codebase follows a module-per-concern pattern. Each module has a `.h`/`.cpp` pair:

- **speede.ino** — Entry point. `setup()` initializes all modules; `loop()` runs the game state machine.
- **game_state** — Game state machine with states: `GAME_LOBBY`, `GAME_SPEED`, `GAME_OVER`, `GAME_DEMO`, `GAME_HIGH_SCORE`. Controls transitions between states and handles lobby/demo/high-score display modes.
- **game_speed** — Core speed game logic. Manages the button press stack (FIFO queue of expected colors), reaction time curve, scoring, EEPROM high score persistence, and game-over conditions.
- **button** — Button input handling with press and long-press detection. Four buttons: red, yellow, green, blue (`ButtonColor` enum).
- **button_leds** — LED control for the button lights. Functions for highlight-one, all-on, all-off, and bitmask-based control.
- **display** — 4-digit seven segment display via SevSegShift. Handles number display and scrolling text. `refreshDisplay()` must be called every loop iteration (no `delay()` allowed).
- **note_player** — Piezo buzzer music system. Supports single notes and multi-note pieces (chimes for game over, new high score, easter egg). Uses non-blocking timing.
- **speede.h** — Global constants: `MAX_STACK`, pin definitions, timing values.
- **pitches.h** — Note frequency definitions for the buzzer.

## Key Design Constraints

- **No `delay()` calls** — The seven segment display requires continuous `refreshDisplay()` calls in the main loop. All timing uses `millis()` comparisons.
- **EEPROM high scores** — Stored at address 0. EEPROM has 100,000 write cycle limit.
- **Button press stack** — A FIFO array (`MAX_STACK` = 50) queues expected button colors. Game ends when stack overflows or player presses wrong button.
- **Reaction time curve** — Defined in `getUpdatedReactionTime()`: gradually decreases from 570ms with diminishing multipliers, hard floor at 100ms.
- **Pin configuration** — Currently set for Arduino UNO with shift register. Mega 2560 pin mappings exist as comments. Key pins: buzzer on pin 3, random seed from analog pin A5 (must be unconnected).
