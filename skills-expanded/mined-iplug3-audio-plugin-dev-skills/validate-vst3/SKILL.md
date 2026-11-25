---
name: validate-vst3
description: Validate VST3 plugins (.vst3 bundles) using Steinberg's official validator tool. Use when user says "run VST3 validator", "validate VST3", "test the .vst3", or needs Steinberg-specific test suites. Prefer this over pluginval for multi-bus VST3 plugins.
compatibility: macOS, Windows, Linux. Built from VST3 SDK source.
metadata:
  author: Oli Larkin
  version: 0.0.1
---

# VST3 Validator

## Plugin Install Locations

The `validator` accepts a direct path, but `validator -list` only scans standard locations.

| Platform | User Location | System Location |
|----------|--------------|-----------------|
| macOS | `~/Library/Audio/Plug-Ins/VST3/` | `/Library/Audio/Plug-Ins/VST3/` |
| Windows | `%LOCALAPPDATA%\Programs\Common\VST3\` | `C:\Program Files\Common Files\VST3\` |
| Linux | `~/.vst3/` | `/usr/lib/vst3/` or `/usr/local/lib/vst3/` |

## Instructions

1. Locate the built `.vst3` bundle (in your build output directory or one of the standard locations above)
2. Locate the `validator` binary (see Common Binary Locations below)
3. Run: `validator /path/to/plugin.vst3`
4. For thorough testing add `-e`: `validator -e /path/to/plugin.vst3`
5. Check output for FAILED lines — see Common Issues below for fixes

## Basic Usage

```bash
# Validate a VST3 plugin (validator location depends on your VST3 SDK build)
validator /path/to/plugin.vst3
```

### Common Binary Locations

| Platform | Path |
|----------|------|
| macOS | `<vst3sdk>/build/bin/Release/validator` or `/usr/local/bin/validator` |
| Windows | `<vst3sdk>\build\bin\Release\validator.exe` |
| Linux | `<vst3sdk>/build/bin/Release/validator` |

## Options

```bash
# Run extensive tests (takes longer but more thorough)
validator -e /path/to/plugin.vst3

# Quiet mode - only print errors
validator -q /path/to/plugin.vst3

# Run only a specific test suite
validator -suite "General Tests" /path/to/plugin.vst3

# Test only a specific processor class ID
validator -cid "ABCD1234..." /path/to/plugin.vst3

# Use local instance per test (isolates tests)
validator -l /path/to/plugin.vst3
```

## Listing Plugins

```bash
# List all installed VST3 plugins
validator -list

# List snapshots from all installed plugins
validator -snapshots
```

## Test Suites

| Suite | Description |
|-------|-------------|
| General Tests | Basic plugin loading and info |
| Single Precision | 32-bit audio processing |
| Double Precision | 64-bit audio processing |
| Bus Activation | Bus enable/disable handling |
| Bus Arrangement | Channel configuration |
| Parameters | Parameter handling and automation |
| State | Preset save/restore |
| Editor | UI creation/destruction |
| Process Context | Transport and tempo handling |

## Building the Validator

Clone the [VST3 SDK](https://github.com/steinbergmedia/vst3sdk) if you don't have it, then build:

```bash
cd <vst3sdk>
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --target validator
```

## Common Issues

### Plugin Not Loading
- Check the binary architecture matches (arm64 vs x86_64 on macOS, x64 vs x86 on Windows)
- Verify all dependencies are bundled or available
- Check logs: Console.app (macOS), Event Viewer (Windows), or stderr (Linux)

### Test Failures
- **State tests**: Ensure `getState`/`setState` are implemented correctly
- **Parameter tests**: Check parameter IDs are stable and unique
- **Bus tests**: Verify channel configurations are valid

### Extensive Test Failures
The `-e` flag runs stress tests that may reveal:
- Memory leaks
- Thread safety issues
- Edge cases in parameter handling
