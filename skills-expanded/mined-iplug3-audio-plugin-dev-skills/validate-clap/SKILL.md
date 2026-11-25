---
name: validate-clap
description: Validate CLAP plugins (.clap files) using clap-validator. Use when user says "validate CLAP", "run clap-validator", "test the .clap", or "test CLAP plugin". Does NOT validate .vst3 or .component — use the appropriate validators.
compatibility: macOS, Windows, Linux. Requires clap-validator binary (pre-built or via Rust/cargo).
metadata:
  author: Oli Larkin
  version: 0.0.1
---

# CLAP Validator

## Plugin Install Locations

`clap-validator` accepts a direct path, but these are the standard install locations where hosts scan for CLAP plugins.

| Platform | User Location | System Location |
|----------|--------------|-----------------|
| macOS | `~/Library/Audio/Plug-Ins/CLAP/` | `/Library/Audio/Plug-Ins/CLAP/` |
| Windows | `%LOCALAPPDATA%\Programs\Common\CLAP\` | `C:\Program Files\Common Files\CLAP\` |
| Linux | `~/.clap/` | `/usr/lib/clap/` or `/usr/local/lib/clap/` |

## Instructions

1. Install `clap-validator` (see Installation below)
2. Locate the built `.clap` plugin bundle (in your build output directory or one of the standard locations above)
3. Run: `clap-validator validate /path/to/plugin.clap`
4. To see only failures: `clap-validator validate --only-failed /path/to/plugin.clap`
5. For debugging, run a specific test in-process: `clap-validator validate --in-process --test-filter <test> /path/to/plugin.clap`

## Installation

### Option 1: Download Pre-built Binary

1. Download from [GitHub Releases](https://github.com/free-audio/clap-validator/releases)
2. Extract and place in your PATH:
   - **macOS / Linux**: `/usr/local/bin/`
   - **Windows**: Add to `PATH` or place in project directory

**macOS only:** Builds are unsigned. Remove the quarantine attribute:
```bash
xattr -dr com.apple.quarantine /path/to/clap-validator
```

### Option 2: Build from Source

```bash
# Requires Rust (all platforms)
cargo install clap-validator

# Or build from source
git clone https://github.com/free-audio/clap-validator
cd clap-validator
cargo build --release
# Binary at target/release/clap-validator (macOS/Linux)
# Binary at target\release\clap-validator.exe (Windows)
```

## Basic Usage

```bash
# Validate a CLAP plugin
clap-validator validate /path/to/plugin.clap

# Show only failed tests
clap-validator validate --only-failed /path/to/plugin.clap

# Validate multiple plugins
clap-validator validate /path/to/plugin1.clap /path/to/plugin2.clap
```

## Commands

```bash
# List available tests
clap-validator list tests

# List tests with descriptions (JSON format)
clap-validator list tests --json

# List all installed CLAP plugins
clap-validator list plugins

# List installed plugins (JSON format)
clap-validator list plugins --json

# List presets for specific plugins
clap-validator list presets /path/to/plugin.clap

# List presets for all installed plugins
clap-validator list presets

# List presets (JSON format)
clap-validator list presets --json
```

## Validation Options

```bash
# Show only failed and warning tests
clap-validator validate --only-failed /path/to/plugin.clap

# Run tests in current process (for debugging, allows debugger attachment)
clap-validator validate --in-process /path/to/plugin.clap

# Filter to specific test (case-insensitive regex)
clap-validator validate --test-filter <REGEX> /path/to/plugin.clap

# Invert filter — skip matching tests instead
clap-validator validate --test-filter <REGEX> --invert-filter /path/to/plugin.clap

# Only validate a specific plugin ID from a multi-plugin library
clap-validator validate --plugin-id <PLUGIN_ID> /path/to/plugin.clap

# Disable parallel test execution (sequential, keeps output in order)
clap-validator validate --no-parallel /path/to/plugin.clap

# Hide plugin's own output (useful for noisy plugins)
clap-validator validate --hide-output /path/to/plugin.clap

# Output results as JSON
clap-validator validate --json /path/to/plugin.clap

# JSON output showing only failures
clap-validator validate --json --only-failed /path/to/plugin.clap
```

## Verbosity

The top-level `-v`/`--verbosity` flag controls the validator's own logging (not the plugin's output):

```bash
# Suppress all non-essential output
clap-validator -v quiet validate /path/to/plugin.clap

# Default level
clap-validator -v debug validate /path/to/plugin.clap

# Available levels: quiet, error, warn, info, debug, trace
```

## Debugging Failed Tests

```bash
# List available tests
clap-validator list tests

# Run specific test in-process (allows debugger attachment)
clap-validator validate --in-process --test-filter <test-name> /path/to/plugin.clap

# With lldb (macOS/Linux)
lldb -- clap-validator validate --in-process --test-filter <test> /path/to/plugin.clap

# With Visual Studio debugger (Windows) - attach to process or use:
devenv /debugexe clap-validator.exe validate --in-process --test-filter <test> C:\path\to\plugin.clap
```

## Test Categories

| Category | Description |
|----------|-------------|
| Plugin loading | Library symbols, entry point, factory |
| Descriptors | Plugin ID, name, features, categories |
| Parameters | Info, ranges, text conversion, automation flags |
| State | Save/load, empty state handling |
| Audio processing | Activation, processing, thread safety |
| Fuzzing | Random parameter values, random audio/MIDI |
| Presets | Discovery, loading (if supported) |

## Common Issues

### Parameter Test Failures
- Ensure `CLAP_PARAM_IS_READONLY` is not combined with `CLAP_PARAM_IS_AUTOMATABLE`
- Check parameter ranges and default values are valid
- Verify text-to-value and value-to-text conversions

### State Test Failures
- Ensure `clap_plugin_state::load()` returns `false` for empty/invalid state
- Check thread safety in state save/load
