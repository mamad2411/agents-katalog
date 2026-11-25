---
name: validate-pluginval
description: Validate VST3 (.vst3) and AudioUnit (.component) plugins with pluginval at configurable strictness levels. Use when user says "run pluginval", "validate plugin", or wants comprehensive cross-format testing. Does NOT support .clap files. For multi-bus VST3 plugins that crash, use validate-vst3 instead.
compatibility: macOS, Windows, Linux. AudioUnit validation only on macOS.
metadata:
  author: Oli Larkin
  version: 0.0.1
---

# pluginval

Cross-platform validator for VST3 and AudioUnit plugins.

## Plugin Install Locations

`pluginval` accepts a direct path. These are the standard install locations by format.

**AudioUnit (.component)** — macOS only:

| Location | Scope |
|----------|-------|
| `~/Library/Audio/Plug-Ins/Components/` | Current user only |
| `/Library/Audio/Plug-Ins/Components/` | All users |

**VST3 (.vst3)**:

| Platform | User Location | System Location |
|----------|--------------|-----------------|
| macOS | `~/Library/Audio/Plug-Ins/VST3/` | `/Library/Audio/Plug-Ins/VST3/` |
| Windows | `%LOCALAPPDATA%\Programs\Common\VST3\` | `C:\Program Files\Common Files\VST3\` |
| Linux | `~/.vst3/` | `/usr/lib/vst3/` or `/usr/local/lib/vst3/` |

## Instructions

1. Install pluginval (see Installation below)
2. Locate the built plugin (`.vst3` or `.component`) in your build output directory or one of the standard locations above
3. Run at strictness level 5 (recommended minimum):
   - macOS: `/Applications/pluginval.app/Contents/MacOS/pluginval --strictness-level 5 /path/to/plugin`
   - Windows: `pluginval.exe --strictness-level 5 "C:\path\to\plugin.vst3"`
   - Linux: `pluginval --strictness-level 5 /path/to/plugin.vst3`
4. If it crashes on a multi-bus VST3, use `validate-vst3` instead
5. For CI, add `--skip-gui-tests` for headless environments

## Installation

Download from [GitHub Releases](https://github.com/Tracktion/pluginval/releases).

| Platform | Setup |
|----------|-------|
| macOS | Extract and move `pluginval.app` to `/Applications/` |
| Windows | Extract `pluginval.exe` and add to `PATH` or use full path |
| Linux | Extract `pluginval` binary, `chmod +x`, place in `/usr/local/bin/` |

**Verify installation:**
```bash
# macOS
/Applications/pluginval.app/Contents/MacOS/pluginval --help

# Windows
pluginval.exe --help

# Linux
pluginval --help
```

## Basic Usage

```bash
# macOS
/Applications/pluginval.app/Contents/MacOS/pluginval --strictness-level 5 /path/to/plugin

# Windows
pluginval.exe --strictness-level 5 "C:\path\to\plugin.vst3"

# Linux
pluginval --strictness-level 5 /path/to/plugin.vst3
```

## Strictness Levels

| Level | Description |
|-------|-------------|
| 1-4 | Basic tests |
| 5 | **Recommended minimum** for host compatibility |
| 6-9 | Increasingly thorough tests |
| 10 | Most comprehensive (may take a long time) |

At levels 5+, pluginval automatically runs `auval` for AudioUnits and VST3 `validator` for VST3.

## Command Line Options

```bash
# Set strictness level (1-10)
--strictness-level 5

# Skip GUI tests (useful for headless CI)
--skip-gui-tests

# Set timeout in milliseconds (use "-1" to disable)
--timeout-ms 30000

# Output logs to directory
--output-dir /path/to/logs

# Set log filename (within output-dir or current directory)
--output-filename results.log

# Repeat tests multiple times
--repeat 3

# Randomize test order
--randomise

# Use specific random seed (for reproducibility)
--seed 0x374115a

# Verbose output
--verbose

# Custom sample rates (comma-separated, default: 44100,48000,96000)
--sample-rates 44100,48000,96000,192000

# Custom block sizes (comma-separated, default: 64,128,256,512,1024)
--block-sizes 64,128,256,512,1024

# Provide a data file for test configuration
--data-file /path/to/config.txt

# Disable specific tests (file with one test name per line)
--disabled-tests /path/to/disabled.txt

# Specify path to VST3 validator (run as part of test process)
--vst3validator /path/to/validator
```

## Environment Variables

All command line options can be set as environment variables by removing the `--` prefix, converting dashes to underscores, and uppercasing. Command line options override environment variables.

```bash
# Examples
export STRICTNESS_LEVEL=5
export SKIP_GUI_TESTS=1
export TIMEOUT_MS=30000
export SAMPLE_RATES="44100,48000,96000"
export BLOCK_SIZES="64,128,256,512,1024"
```

## CI Integration

### macOS / Linux

```bash
pluginval --strictness-level 5 --skip-gui-tests --timeout-ms 60000 /path/to/plugin.vst3

if [ $? -ne 0 ]; then
  echo "Plugin validation failed!"
  exit 1
fi
```

### Windows (PowerShell)

```powershell
& pluginval.exe --strictness-level 5 --skip-gui-tests --timeout-ms 60000 "C:\path\to\plugin.vst3"

if ($LASTEXITCODE -ne 0) {
    Write-Error "Plugin validation failed!"
    exit 1
}
```

## Reproducing Failures

pluginval uses randomness for some tests. To reproduce a failure:

1. Note the random seed from the log (e.g., `Random seed: 0x374115a`)
2. Re-run with that seed:
```bash
/Applications/pluginval.app/Contents/MacOS/pluginval --seed 0x374115a -s 5 /path/to/plugin
```

## Known Limitations

### No CLAP Support
Use `clap-validator` for CLAP plugins.

### Multi-Bus VST3 Plugins May Crash
Plugins with multiple audio buses (multi-output instruments, sidechain effects) may crash pluginval during VST3 validation.

**Workaround:**
1. Use the official Steinberg VST3 validator instead
2. Test the AU version with pluginval (usually works)
3. Verify with `auval` for AU format
