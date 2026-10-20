# GitHub Copilot Instructions for Pi Bot

## Project Overview

Pi Bot is an AI-driven companion robot for Raspberry Pi 5, built in Rust using an event-driven architecture. The bot features voice interaction (wake word detection, STT, TTS), visual expression (RGB LED patterns), environmental awareness (PIR motion, camera, temperature), and local LLM integration (Ollama).

**Design Philosophy**: Component independence, fault tolerance, personality-first design with proactive engagement, and separation of conversation behavior from visual presentation.

---

## Architecture Principles

### Event-Driven Communication Flow

```
[Sensors] → Events → [AI Controller] → Commands → [Actuators]
```

**Critical Rules**:
- Sensors **only emit events** (never control actuators directly)
- AI Controller **owns all behavioral logic** and decision-making
- Actuators **only consume commands** (no business logic)
- Components communicate via async channels (`mpsc`, `broadcast`)
- **No shared mutable state** between components
- Each component is an independent async task with its own error handling

### Component Independence

- Each component operates in its own async task/event loop
- Components can fail without crashing the system
- Non-critical components (camera, LCD, DHT11) fail gracefully
- Critical path: LLM + audio pipeline + RGB LED = minimum viable system

### State Management

The bot separates **conversation state** (what the bot does) from **lighting mode** (what you see):

**Conversation States**:
- `Ready`: Default monitoring, responds to wake phrase
- `Observing`: Evaluating context, deciding whether to initiate conversation
- `Active(SubState)`: In conversation (Listening → Thinking → Learning → Speaking)
- `Silent { manual: bool }`: Do Not Disturb mode (manual or auto via PIR timeout)

**Lighting Modes**:
- `StateBased`: LED reflects conversation state (orange=listening, blue=thinking, green=speaking)
- `Ambient { pattern }`: Decorative lighting independent of state
- `Minimal`: Dim or off for meetings/sleep

These are **orthogonal dimensions** allowing flexible combinations (e.g., ambient lighting while bot can still talk).

---

## Workspace Structure

Cargo workspace with 6 crates:

```
pi-bot/
├── actuators/          # Hardware outputs: RGB LED, speakers, status LEDs
├── ai_controller/      # LLM service, memory, decision-making logic
├── audio_pipeline/     # Vosk (wake word/STT), Piper (TTS)
├── bot_core/           # Shared types: Event, Command, State, Config
├── sensors/            # Hardware inputs: PIR motion, microphone
└── runner/             # Main orchestration binary (spawns all tasks)
```

**Key Files**:
- `bot_core/src/events.rs`: All sensor events
- `bot_core/src/commands.rs`: All actuator commands
- `bot_core/src/state.rs`: State models and color definitions
- `bot_core/src/config.rs`: YAML config loading
- `runner/src/main.rs`: Task orchestration and channel setup
- `config/config.yaml`: GPIO pins, audio settings, LLM config

---

## Coding Patterns & Conventions

### Event & Command Enums

**Events** represent "something happened" (sensors → controller):
```rust
pub enum Event {
    PresenceDetected,
    WakeWordDetected,
    SpeechCaptured(String),
    SpeechComplete,
    SystemReady,
    // ...
}
```

**Commands** represent "do this thing" (controller → actuators):
```rust
pub enum Command {
    SetColor(RgbColor),
    SetPattern { pattern: LedPattern, colors: Vec<RgbColor> },
    Speak { text: String },
    StartListening,
    // ...
}
```

### Async Task Pattern

Each component follows this structure:
```rust
pub async fn run_component_task(
    config: &Config,
    mut cmd_rx: mpsc::Receiver<Command>,
    event_tx: mpsc::Sender<Event>,
    mut shutdown_rx: broadcast::Receiver<()>,
) -> Result<()> {
    loop {
        tokio::select! {
            Some(cmd) = cmd_rx.recv() => {
                // Handle command
            }
            _ = shutdown_rx.recv() => {
                log::info!("Component shutting down...");
                break;
            }
        }
    }
    Ok(())
}
```

### Error Handling

- Use `anyhow::Result` for application code
- Use `thiserror` for custom error types in libraries
- Log errors with `log::error!` but allow graceful degradation
- Wrap hardware operations with recovery logic

### Documentation Style

Use **module-level doc comments** (`//!`) with clear sections:
```rust
//! Brief description of module
//!
//! Detailed explanation of purpose and behavior.
//!
//! ## Integration
//! How this component fits into the system
//!
//! ## Error Handling
//! How failures are handled
```

Use **item-level doc comments** (`///`) for public APIs:
```rust
/// Set RGB LED to a solid color
///
/// # Arguments
/// * `color` - The RGB color to display
SetColor(RgbColor),
```

### Hardware Test Binaries

Each hardware component has a standalone test binary in `src/bin/`:
- `rgb-led-test.rs`: Test RGB LED color changes
- `status-led-test.rs`: Test green/red status LEDs
- `pir-test.rs`: Test motion sensor
- `stt-test.rs`: Test speech-to-text
- `wake-word-test.rs`: Test wake word detection
- `tts-test.rs`: Test text-to-speech

**Purpose**: Verify hardware wiring and GPIO config before system integration

---

## Dependencies & Key Libraries

**Core Async & Hardware**:
- `tokio = { version = "1.40", features = ["full"] }` - Async runtime
- `rppal = "0.22"` - Raspberry Pi GPIO control

**Serialization & Config**:
- `serde = { version = "1.0", features = ["derive"] }` - Serialization framework
- `serde_json = "1.0"` - JSON support
- `serde_yaml = "0.9"` - YAML config loading

**HTTP & AI**:
- `reqwest = { version = "0.12", features = ["json"] }` - HTTP client for Ollama API

**Error Handling**:
- `anyhow = "1.0"` - Application error handling
- `thiserror = "1.0"` - Custom error types

**Logging & Time**:
- `log = "0.4"` + `env_logger = "0.11"` - Logging framework
- `chrono = "0.4"` - Date/time utilities

---

## Common Tasks & Patterns

### Adding a New Sensor

1. **Define event variant** in `bot_core/src/events.rs`:
   ```rust
   /// Description of what this sensor detects
   NewSensorReading { data: SensorData },
   ```

2. **Create sensor module** in `sensors/src/`:
   ```rust
   pub async fn run_sensor_task(
       config: &Config,
       event_tx: mpsc::Sender<Event>,
       shutdown_rx: broadcast::Receiver<()>,
   ) -> Result<()> { /* ... */ }
   ```

3. **Add test binary** in `sensors/src/bin/sensor_test.rs`

4. **Spawn task** in `runner/src/main.rs`

5. **Handle event** in AI controller logic

### Adding a New Actuator

1. **Define command variant** in `bot_core/src/commands.rs`:
   ```rust
   /// Description of what this actuator does
   ControlActuator { params: ActuatorParams },
   ```

2. **Create actuator module** in `actuators/src/`:
   ```rust
   pub async fn run_actuator_task(
       config: &Config,
       cmd_rx: mpsc::Receiver<Command>,
       shutdown_rx: broadcast::Receiver<()>,
   ) -> Result<()> { /* ... */ }
   ```

3. **Add test binary** in `actuators/src/bin/actuator_test.rs`

4. **Spawn task** in `runner/src/main.rs`

5. **Add routing** in `command_distributor.rs`

### Modifying State Behavior

1. **Update state definitions** in `bot_core/src/state.rs` if adding new states
2. **Update state transition logic** in AI controller
3. **Update LED patterns** in `rgb_led_actuator.rs` for new states
4. **Document behavior** in `docs/STATE_MODEL.md`

### Working with Configuration

- **Location**: `config/config.yaml`
- **Loading**: Via `bot_core::load_config()`
- **Structure**: GPIO pins, audio settings, LLM endpoints, timing parameters
- **Hot reload**: Not currently supported; requires restart

---

## Testing Strategy

### Unit Tests
- Test pure logic functions in isolation
- Mock hardware interfaces
- Use `#[cfg(test)]` modules

### Hardware Tests
- Standalone binaries in `src/bin/` for each component
- Minimal dependencies (just the hardware controller + logging)
- Run before system integration: `cargo run --bin <test_name> --release`

### Integration Tests
- Test component interactions via channels
- Mock event/command flow
- Verify state transitions

### System Tests
- Run full `runner` binary on actual hardware
- Monitor logs for errors
- Test real-world interaction scenarios

---

## Performance Considerations

### Raspberry Pi 5 Constraints
- **RAM**: 16GB available, but LLM (Qwen2.5 7B) uses ~8GB
- **CPU**: 4 cores (Arm Cortex-A76), optimize for minimal CPU in idle state
- **Audio**: 16kHz sample rate for Vosk to balance accuracy and CPU usage

### Optimization Strategies
- **Lazy loading**: Load Vosk/Piper models only when needed
- **Keyword mode**: Use Vosk keyword spotting (low CPU) vs full STT
- **LED updates**: Rate-limit pattern updates to avoid GPIO spam
- **Memory**: Store conversations in JSON, prune old sessions

---

## AI & ML Integration

### Ollama (Local LLM)
- **Model**: Qwen2.5 7B (fits in 16GB RAM)
- **API**: HTTP REST API via `reqwest`
- **Usage**: Conversation generation, memory extraction, observation decisions
- **Endpoint**: Configurable in `config.yaml`

### Vosk (Wake Word + STT)
- **Models**: Download via `scripts/download_models.sh`
- **Modes**:
  - Keyword spotting (low CPU) for wake word detection
  - Full STT for speech transcription after wake word
- **Configuration**: Model path, wake phrase, capture timeout in `config.yaml`

### Piper (TTS)
- **Voice**: `en_GB-alba-medium` (natural British English)
- **Models**: ONNX format in `models/piper/`
- **Usage**: Convert LLM responses to speech audio

---

## Common Pitfalls & Solutions

### Problem: GPIO Pin Already in Use
**Solution**: Check `/sys/class/gpio/` for exported pins, unexport them, or restart system

### Problem: Vosk Model Not Found
**Solution**: Run `./scripts/download_models.sh`, verify path in `config.yaml`

### Problem: Audio Device Not Found
**Solution**: Check `arecord -l` and `aplay -l` for device names, update `config.yaml`

### Problem: Task Hangs on Shutdown
**Solution**: Ensure all tasks have `tokio::select!` with `shutdown_rx` branch, use timeout for cleanup

### Problem: RGB LED Wrong Colors
**Solution**: Verify GPIO pin wiring matches `config.yaml`, check common cathode/anode

### Problem: LLM Out of Memory
**Solution**: Use smaller model (Qwen2.5 3B), reduce context window, or increase swap space

---

## Development Workflow

### Building
```bash
# Build all crates
cargo build --release

# Build specific crate
cargo build -p actuators --release

# Run main system
cargo run --bin runner --release
```

### Testing Hardware
```bash
# Test individual components
cargo run --bin rgb-led-test --release
cargo run --bin pir-test --release
cargo run --bin stt-test --release
```

### Debugging
```bash
# Enable debug logging
RUST_LOG=debug cargo run --bin runner

# Target specific module
RUST_LOG=audio_pipeline=debug cargo run --bin runner
```

### Adding Dependencies
1. Add to `[workspace.dependencies]` in root `Cargo.toml`
2. Reference in crate's `Cargo.toml`: `my_crate = { workspace = true }`

---

## Code Generation Preferences

When generating code for this project:

1. **Follow event-driven patterns**: Use Events and Commands enums, never bypass the controller
2. **Maintain independence**: Components communicate only via channels
3. **Include doc comments**: Module and item-level documentation
4. **Handle errors gracefully**: Use `anyhow::Result`, log errors, allow degradation
5. **Write test binaries**: Create standalone tests for hardware components
6. **Respect state model**: Don't mix conversation state with lighting mode
7. **Use configuration**: Read from `config.yaml` rather than hardcoding values
8. **Async patterns**: Use `tokio::select!` for shutdown handling
9. **Logging**: Use `log::info!`, `log::warn!`, `log::error!` appropriately
10. **Naming conventions**:
    - Events: Past tense or present perfect (WakeWordDetected, PresenceDetected)
    - Commands: Imperative (SetColor, Speak, StartListening)
    - Tasks: `run_<component>_task` pattern
    - Channels: `<purpose>_tx` / `<purpose>_rx`

---

## Future Development (Phase 2+)

Planned features currently marked as TODO:
- **Camera integration**: Human detection, desk occupancy, object change detection
- **LCD display**: 16x2 text output for status messages
- **DHT11 sensor**: Temperature and humidity monitoring
- **Gesture recognition**: Camera-based hand gesture commands
- **Voice modulation**: Emotion-based TTS tone adjustment
- **Memory system**: Long-term conversation memory and personality adaptation
- **Web dashboard**: Browser-based control and monitoring interface

When implementing these, follow the same event-driven patterns and maintain component independence.

---

## Resources & Documentation

- **Project Docs**:
  - `docs/ARCHITECTURE.md` - System architecture details
  - `docs/STATE_MODEL.md` - State behavior specification
  - `docs/FEATURES.md` - Feature descriptions and behaviors
  - `docs/REQUIREMENTS.md` - Hardware specs and software requirements
  - `docs/ROADMAP.md` - Development phases and timeline

- **Configuration**: `config/config.yaml` - GPIO pins, audio, LLM settings
- **Models**: `models/` - AI/ML models (not in git, download via script)

---

## Troubleshooting & Diagnostics

### Log Analysis
- System startup: Look for "Pi Bot Companion System v0.1.0" banner
- Task spawning: Check for "Spawning X task..." messages
- Ready state: Look for "SystemReady event" from audio sensor
- Errors: Search for "ERROR" level logs with component name

### Health Monitoring
- **Green LEDs**: System healthy and ready
- **Red LEDs breathing**: DND/idle mode
- **Red LEDs flashing**: System error
- **RGB LED colors**: See state-based patterns in `docs/FEATURES.md`

### Common Debug Commands
```bash
# Check GPIO pin state
cat /sys/class/gpio/gpio<PIN>/value

# List audio devices
arecord -l
aplay -l

# Test Ollama
curl http://localhost:11434/api/generate -d '{"model":"qwen2.5:7b","prompt":"Hello"}'

# Monitor system resources
htop
```

---

## Summary

Pi Bot is a Raspberry Pi AI companion with strict architectural boundaries:
- **Sensors → Events → AI Controller → Commands → Actuators** (unidirectional flow)
- **Component independence** (fail gracefully, test in isolation)
- **State separation** (conversation behavior vs lighting presentation)
- **Rust + Tokio async** (event-driven, channel-based communication)
- **Local AI** (Ollama LLM, Vosk STT, Piper TTS)

When assisting with this project, prioritize architectural consistency, fault tolerance, and testability. Always respect the event-driven pattern and avoid direct coupling between components.
