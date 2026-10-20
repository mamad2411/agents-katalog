# AGENTS.md - Guide for AI Coding Agents

**Nimphea** v1.1.0 - Nim wrapper for libDaisy embedded audio platform (ARM Cortex-M7 / STM32H750).

## Build & Test Commands

```bash
# One-time setup (clone submodules, build libDaisy)
nimble init_libdaisy

# Development install — symlinks package into ~/.nimble/pkgs2/ so
# `import nimphea` resolves without hardcoded paths
nimble develop

# Build for ARM (outputs: build/*.elf, build/*.bin)
nimble make blink              # Build single example
nimble make examples/audio_demo  # Can use full path

# Flash to hardware
nimble flash blink              # Via DFU bootloader (USB)
nimble stlink blink             # Via ST-Link/OpenOCD (faster)

# Testing
nimble test                     # Syntax check all 43 examples (host, no ARM)
nim check examples/blink.nim    # Fast syntax check for single file
nimble make blink               # Full compile test with linking
nimble test_unit                # Unit tests for pure-Nim modules (host)

# Other
nimble clear                    # Remove build/ directory and artifacts
nimble docs                     # Generate API docs → docs/api/*.html
```

**Requirements**: Nim ≥2.0.0, arm-none-eabi-gcc, libDaisy (submodule)

## Code Style

### Naming Conventions

```nim
type DaisySeed* = object          # Types: PascalCase*
proc setLed*(x: var T)            # Procs: camelCase*
const SAMPLE_RATE* = 48000        # Constants: UPPER_SNAKE_CASE
type Mode* = enum INPUT, OUTPUT   # Enums: PascalCase type, values match C++
var ledState = false              # Vars: camelCase (not exported)
```

### Module Structure

```nim
## Module Title - Short description
## 
## Detailed description with usage examples.

import std/math                       # Standard imports first
import nimphea                        # For examples
import nimphea/nimphea_macros         # For wrapper modules
import nimphea/per/adc                # Category-based organization

useNimpheaNamespace()           # For examples (REQUIRED)
useNimpheaModules(adc)          # For wrappers (after imports!)

type MyType* = object
  field*: cint

proc myProc*() = discard
```

### C++ Interop Patterns

```nim
# Import C++ type
type
  DaisySeed* {.importcpp: "daisy::DaisySeed", header: "daisy_seed.h".} = object

# C++ methods (# = this pointer, @ = subsequent args)
proc init*(this: var DaisySeed) {.importcpp: "#.Init()".}
proc setLed*(this: var DaisySeed, state: bool) {.importcpp: "#.SetLed(#)".}
proc delay*(this: var DaisySeed, ms: csize_t) {.importcpp: "#.DelayMs(@)".}

# C++ constructor
proc newPin*(port: GPIOPort, pin: uint8): Pin 
  {.importcpp: "daisy::Pin(@)", constructor, header: "daisy_seed.h".}

# C function (no this-pointer)
proc arm_fir_f32*(S: ptr FirInstanceF32, ...) {.importc, header: "arm_math.h".}

# Type mappings: int→cint, float→cfloat, uint16→uint16, size_t→csize_t
# T*→ptr T, T&→var T, const T&→T
```

### Documentation Style

```nim
proc process*(input, output: AudioBuffer, size: int) =
  ## Process audio in real-time callback
  ## 
  ## **Parameters:**
  ## - `input` - Input [channel][sample]
  ## - `output` - Output [channel][sample]
  ## 
  ## **Example:**
  ## ```nim
  ## for i in 0..<size:
  ##   output[0][i] = input[0][i] * 0.5
  ## ```
```

## Directory Structure

```
src/
└── nimphea.nim               # Public API entry point (re-exports, DaisySeed, audio types)
src/nimphea/
├── nimphea_macros.nim        # Compile-time C++ interop macro system
├── panicoverride.nim         # Bare-metal panic handler
├── boards/                   # Per-board wrappers (7 boards: pod, patch, patch_sm,
│                             #   field, petal, versio, legio)
├── per/                      # Peripheral wrappers (11 modules: adc, dac, i2c, spi,
│                             #   spi_multislave, uart, pwm, qspi, rng, sdmmc, tim)
├── hid/                      # Human interface (switch, switch3, encoder/ctrl, led,
│                             #   rgb_led, midi, usb, logger, parameter, gatein)
│   └── disp/                 # Display abstractions (oled_display, graphics_common)
├── dev/                      # Device drivers (20 drivers: codecs, OLED, IMU,
│                             #   LED drivers, sensors, shift registers, etc.)
├── sys/                      # System modules (dma, sdram, fatfs, system)
├── cmsis/                    # CMSIS-DSP wrappers (13 modules: dsp_filtering,
│                             #   dsp_transforms, dsp_matrix, dsp_statistics,
│                             #   dsp_basic, dsp_fastmath, dsp_complex, etc.)
├── ui/                       # UI framework (display, events, menu_builder)
├── util/                     # Utilities (oled_fonts)
└── nimphea_*.nim             # Flat modules: fifo, stack, ringbuffer, fixedstr,
                              #   color, wavplayer, wavwriter, menu, sai, etc.
libDaisy/                     # C++ library (submodule — never modify)
tests/                        # Host-side unit tests (pure-Nim modules only)
```

**Published companion repos:**
- [nimphea-examples](https://github.com/Brokezawa/nimphea-examples) — 43 example programs
- [nimphea-template-basic](https://github.com/Brokezawa/nimphea-template-basic) — GitHub template for basic projects
- [nimphea-template-audio](https://github.com/Brokezawa/nimphea-template-audio) — GitHub template for audio projects

## Macro System (CRITICAL)

**Always use macros for C++ headers. NO raw emit!**

```nim
# For examples — includes all typedefs + `using namespace daisy`
import nimphea
useNimpheaNamespace()

# For wrapper modules under src/nimphea/ — selective includes
import nimphea/nimphea_macros
useNimpheaModules(spi, i2c)

# For CMSIS-DSP modules
useCmsisModules(dsp_filtering)

# WRONG — never do this
{.emit: """#include "per/spi.h"
using namespace daisy;""".}
```

**Raw emit allowed ONLY for:**
1. C++ operators (can't define in Nim)
2. `std::initializer_list` workarounds
3. Custom C++ helpers (rare, document why)

### Adding New Module

1. Find C++ header in `libDaisy/src/`
2. Edit `src/nimphea/nimphea_macros.nim`:
   ```nim
   const myTypedefs* = ["MyClass::Result MyResult"]
   # Add to getModuleHeaders() and useNimpheaModules()
   ```
3. Create wrapper in `src/nimphea/per/mymodule.nim`
4. Run `nim check src/nimphea/per/mymodule.nim` then `nimble test`

## Common Pitfalls

```nim
# WRONG: Missing # for this pointer
proc init*(x: var T) {.importcpp: "Init()".}
# CORRECT:
proc init*(x: var T) {.importcpp: "#.Init()".}

# WRONG: Not exported, wrong type
proc getValue(): int
# CORRECT:
proc getValue*(): cint

# WRONG: Macro before imports
useNimpheaModules(adc)
import nimphea/per/adc
# CORRECT:
import nimphea/per/adc
useNimpheaModules(adc)
```

## Embedded Constraints

- **CPU**: ARM Cortex-M7 @ 400-480MHz
- **RAM**: 512KB SRAM (+ optional 64MB SDRAM)
- **Bare metal**: No OS, no dynamic allocation by default
- **Real-time audio**: ~1ms callbacks (48 samples @ 48kHz)
- **Stack over heap**: Prefer `array` over `seq` in audio callbacks
- **All RT callbacks must have `{.cdecl, raises: [].}`** — prevents Nim exception machinery from crossing C call boundaries on bare metal
- **Use `assert` for invariants** — no exceptions in embedded paths

### Memory Management

```nim
# GOOD — static allocation
var buffer: array[1024, float32]

# AVOID in callbacks — dynamic allocation
var buffer = newSeq[float32](1024)

# GOOD — pre-allocate outside callback, use inside
var phase = 0.0
proc audioCallback(input, output: AudioBuffer, size: int) {.cdecl, raises: [].} =
  phase += phaseIncrement
```

### CMSIS-DSP Self-Referential Pointer Pattern

`Matrix[R,C]`, `FirFilter[NT,MB]`, and `BiquadFilter` embed a CMSIS instance struct with a `ptr` pointing into the object's own `array` buffer. **Always implement `=copy` and `=sink`** to rebind the pointer to the destination's buffer — default bitwise copy creates dangling pointers.

```nim
proc `=copy`*[NT, MB: static int](dest: var FirFilter[NT, MB], src: FirFilter[NT, MB]) =
  dest.state = src.state
  dest.instance = src.instance
  dest.instance.pState = addr dest.state[0]  # rebind to dest's buffer
```

## Testing Strategy

| Layer | Command | What it covers |
|---|---|---|
| Single file | `nim check examples/blink.nim` | Syntax + import resolution |
| All examples | `nimble test` | 43 examples syntax-checked |
| Pure-Nim units | `nimble test_unit` | FIFO, Stack, RingBuffer, FixedStr, MappedValue |

C++-dependent modules cannot be unit-tested on the host — validate via `nimble make <example>` and hardware flashing.

## Formatting

- **Indentation**: 2 spaces (NO tabs)
- **Line length**: 80-100 chars max
- **Blank lines**: 1 between procs
- **No automated formatter**: Manual (maintain consistency)

## References

- **nimphea.nimble** - Build system and task definitions
- **docs/API_REFERENCE.md** - Complete API reference (85 modules)
- **nimphea-examples/** - 43 example programs
- **libDaisy docs** - https://electro-smith.github.io/libDaisy
