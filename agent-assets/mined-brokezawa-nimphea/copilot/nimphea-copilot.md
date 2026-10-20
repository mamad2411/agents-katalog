# Nimphea — Copilot Instructions

Nim wrapper for the [libDaisy](https://github.com/electro-smith/libDaisy) C++ HAL targeting ARM Cortex-M7 (STM32H750) Daisy hardware. Compiles Nim → C++ → ARM ELF via `arm-none-eabi-gcc`. Requires Nim ≥ 2.0.0.

**Example projects:** See [nimphea-examples](https://github.com/Brokezawa/nimphea-examples) (43 programs). 
**Project templates:** [Basic](https://github.com/Brokezawa/nimphea-template-basic) and [Audio](https://github.com/Brokezawa/nimphea-template-audio) (GitHub templates).

## Build & Test

```bash
# One-time setup
nimble init_libdaisy          # Clone submodules + build libDaisy
nimble develop                # Symlink package into ~/.nimble/pkgs2/ so
                              # `import nimphea` works without hardcoded paths

# Build a single example (ARM cross-compile)
nimble make blink             # → build/blink.elf + build/blink.bin

# Flash to hardware
nimble flash blink            # DFU (USB)
nimble stlink blink           # ST-Link/OpenOCD

# Testing (no hardware needed)
nim check examples/blink.nim  # Fast single-file syntax check
nimble test                   # Syntax check all 43 examples (host)
nimble test_unit              # Unit tests for pure-Nim modules (host)

# Other
nimble clear                  # Remove build/
nimble docs                   # Generate HTML docs → docs/api/
```

CI (`nim check` + `nimble test`) runs on every push/PR via GitHub Actions (`.github/workflows/ci.yml`). `libDaisy` submodule is **not** checked out in CI — tests must not depend on it.

## Architecture

### Layers

```
examples/           # User programs — import nimphea, call useNimpheaNamespace()
src/nimphea.nim     # Public API re-export, DaisySeed type, audio callback types
src/nimphea/
  nimphea_macros.nim    # Compile-time macro system (THE glue between Nim and C++)
  boards/               # Per-board wrappers (DaisyPod, DaisyField, DaisyPetal…)
  per/                  # Peripheral wrappers (ADC, DAC, SPI, I2C, UART, PWM…)
  hid/                  # Human interface (Switch, Encoder, LED, MIDI, USB)
  dev/                  # Device drivers (sensors, codecs, OLED, LCD…)
  sys/                  # System modules (DMA, SDRAM, FatFS)
  cmsis/                # CMSIS-DSP math wrappers (FFT, FIR, matrix, stats…)
  ui/                   # UI framework (menus, events)
libDaisy/           # C++ submodule — never modify
tests/              # Host-side unit tests (pure Nim modules only)
```

### The Macro System — CRITICAL

All C++ header includes and `using namespace daisy` are generated at **compile time** by two macros. Never add raw `{.emit: """#include ...""".}` for headers.

```nim
# In examples and the root nimphea.nim:
import nimphea
useNimpheaNamespace()         # Emits ALL typedefs + using namespace daisy

# In wrapper modules under src/nimphea/:
import nimphea/nimphea_macros
useNimpheaModules(spi, i2c)   # Emits only selected module typedefs

# In CMSIS-DSP modules:
useCmsisModules(dsp_filtering) # Emits arm_math.h includes
```

`useNimpheaModules` **must come after imports**, not before. The macro generates `{.emit.}` blocks with the right headers and C++ typedef aliases (e.g., `using DacResult = DacHandle::Result`).

Raw `{.emit.}` is allowed only for: C++ operators, `std::initializer_list` workarounds, or documented C++ helpers.

### CMSIS-DSP Self-Referential Pointer Pattern

`Matrix[R,C]`, `FirFilter[NT,MB]`, and `BiquadFilter[NS,NB]` embed their CMSIS state struct which holds a `ptr T` pointing into the object's own `array` buffer. **Always implement custom `=copy` and `=sink`** that rebind the pointer to the destination's buffer after copy/move — default bitwise copy creates dangling pointers.

```nim
proc `=copy`*[NT, MB: static int](dest: var FirFilter[NT, MB], src: FirFilter[NT, MB]) =
  dest.state = src.state
  dest.instance = src.instance
  dest.instance.pState = addr dest.state[0]  # rebind!
```

## Naming & Module Conventions

| Entity | Convention | Example |
|---|---|---|
| Types | `PascalCase*` | `DaisySeed*`, `GPIOMode*` |
| Procs | `camelCase*` | `setLed*`, `startAudio*` |
| Constants | `UPPER_SNAKE_CASE*` | `SAMPLE_RATE*` |
| Enum values | Match C++ name | `INPUT`, `OUTPUT` |
| Module files | `nimphea_<name>.nim` | `nimphea_fifo.nim` |

## C++ Interop Rules

```nim
# Instance method — # is this-pointer, @ expands remaining args
proc init*(this: var DaisySeed) {.importcpp: "#.Init()".}
proc delay*(this: var DaisySeed, ms: csize_t) {.importcpp: "#.DelayMs(@)".}

# Constructor
proc newPin*(port: GPIOPort, pin: uint8): Pin
  {.importcpp: "daisy::Pin(@)", constructor, header: "daisy_seed.h".}

# C function (no this-pointer)
proc arm_fir_f32*(S: ptr FirInstanceF32, ...) {.importc, header: "arm_math.h".}
```

Type mappings: `int → cint`, `float → cfloat`, `size_t → csize_t`, `T* → ptr T`, `T& → var T`, `const T& → T`.

## Embedded / Real-Time Constraints

- **No dynamic allocation** (`newSeq`, `new`, etc.) inside audio callbacks or interrupt handlers — use `array` and pre-allocated globals.
- **All real-time callbacks must have `{.cdecl, raises: [].}`** — prevents Nim from inserting exception propagation across C call boundaries on bare metal.
- Audio callback signature: `proc cb(input, output: AudioBuffer, size: int) {.cdecl, raises: [].}`
- The linker script guarantees 4-byte alignment for SDRAM symbols; `cast[uint]` pointer arithmetic in `sys/sdram.nim` is intentional.
- Use `assert` for invariant checks; no exceptions in embedded paths.

## Testing Strategy

| Layer | Command | What it covers |
|---|---|---|
| Single file | `nim check examples/blink.nim` | Syntax + import resolution |
| All examples | `nimble test` | 43 examples syntax-checked |
| Pure-Nim units | `nimble test_unit` | FIFO, Stack, RingBuffer, FixedStr, MappedValue |

C++-dependent modules (anything using `importcpp`) cannot be unit-tested on the host — they are validated via `nimble make <example>` and hardware flashing.

## Adding a New Peripheral Wrapper

1. Find the C++ header in `libDaisy/src/`.
2. Add typedef entries to `nimphea_macros.nim` (`const myTypedefs* = [...]`) and register them in `getModuleHeaders()` and `useNimpheaModules()`.
3. Create `src/nimphea/per/mymodule.nim` — start with `useNimpheaModules(mymodule)`.
4. Run `nim check src/nimphea/per/mymodule.nim` then `nimble test`.
