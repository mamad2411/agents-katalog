---
name: logic-analyzer-agent
description: Top-level agent for USB logic analyzer work using the verified dslogic-cli/libsigrok4DSL native backend. Use for DSLogic/DSView environment setup, device connection, capture (stream+buffer), protocol decode (UART/SPI/I2C), and data interpretation. Use the dsview-logic MCP for hardware operations.
---

# Logic Analyzer Agent

## Architecture
- This skill is the single domain entry for local logic analyzer work.
- Hardware operations go through the `dsview-logic` MCP (10 tools, all native
  dslogic-cli → libsigrok4DSL, zero sigrok-cli).
- Keep judgment here: channel mapping, sample rate adequacy, signal
  interpretation, capture sufficiency, next-measurement decisions.

## MCP Tool Reference

| Tool | Purpose |
|------|---------|
| `logic_analyzer_status` | Check dslogic-cli + libsigrok4DSL readiness (`native_ok` gate) |
| `logic_analyzer_scan` | DISABLED — returns error. Use `capture` directly. |
| `logic_analyzer_list_decoders` | Built-in decoders: uart, spi, i2c |
| `logic_analyzer_capture` | Native capture to raw `.bin` (stream + buffer modes) |
| `logic_analyzer_decode_file` | Decode raw `.bin` with built-in SPI/UART/I2C |
| `logic_analyzer_uart_decode_file` | UART-specific decode helper |
| `logic_analyzer_dsview_info` | DSView GUI version info (GUI-first, not for capture) |

## Pre-capture checklist

1. `logic_analyzer_status` → confirm `native_ok` is true.
2. Stop DSView GUI and any stale `dslogic-cli` process before capture.
3. Run `logic_analyzer_capture` directly — `open` does device init.
4. No scan step. Never run `dslogic-cli scan`.

## Capture modes

| Mode | Stream | Shape | Samples | Duration | Payload |
|------|--------|-------|---------|----------|---------|
| Stream 3 | stream | 100MHz ×3ch | 89.5M | 0.90s | `{"stream":1,"channel_mode":3,"samplerate":100000000,"channels":3}` |
| Buffer 20 | buffer | 100MHz ×16ch | 16.8M | 0.17s | `{"stream":0,"channel_mode":20,"samplerate":100000000,"channels":3}` |
| Buffer 22 | buffer | 400MHz ×4ch | 67.1M | 0.17s | `{"stream":0,"channel_mode":22,"samplerate":400000000,"channels":[0,1,2,3]}` |
| Stream 0 | stream | 20MHz ×16ch | 16.8M | 0.84s | `{"stream":1,"channel_mode":0,"samplerate":20000000}` |
| Stream 1 | stream | 25MHz ×12ch | 16.8M | 0.67s | `{"stream":1,"channel_mode":1,"samplerate":25000000}` |
| Stream 2 | stream | 50MHz ×6ch | 16.8M | 0.34s | `{"stream":1,"channel_mode":2,"samplerate":50000000}` |
| Buffer 21 | buffer | 200MHz ×8ch | 16.8M | 0.08s | `{"stream":0,"channel_mode":21,"samplerate":200000000}` |

All output: raw `.bin` under `deliverables/logic-analyzer/`.

## Backend rules
- Use native `dslogic-cli` → `libsigrok4DSL` for all operations.
- `native_ok` is the readiness gate.
- **Never mix sigrok-cli and dslogic-cli** on the same device.
- **Never run `dslogic-cli scan`** — it bricks the device via firmware upload.
- **Arm FPGA failed → re-run capture**, don't touch USB subsystem.
- **Physical replug is absolute last resort only.**

## Red lines (DO NOT)
- Run `dslogic-cli scan` as a standalone CLI command.
- Create symlinks from FPGA `.bin` to Cypress `.fw`.
- Mix sigrok-cli and dslogic-cli on the same device.
- Unbind/rebind USB as a routine recovery step.

## Capture pitfalls
- **Enable channels BEFORE capture.** Without `enable <ch> 1`, all channels
  default to disabled, producing all-zero output even with signals connected.
- Set `channel_mode` after `stream`; default stream mode is 0 (20MHz x16ch).
- Use numeric channel indices: `enable 0 1`, not `enable D0 1`.
- For 3.3V logic, use `vth 1.8`; `vth 3.3` sets threshold at signal rail.
- The 3ch packing (mode 3) produces `samples / 8 × 3` bytes.
- Stop DSView GUI before CLI capture; only one process owns the USB device.
- If target MCU is halted by a debugger, resume it before capturing.

## Raw 3ch packed binary format
8 samples packed across 3 bytes: Byte0=D0[0..7], Byte1=D1[0..7], Byte2=D2[0..7].
Total bytes = samples × 3 / 8. Native decoder treats 1 byte = 1 sample, so
decoded indices are offset. Unpack before precise protocol decode.

## Interpretation rules
- Adjacent edge spacing is half the full period for 50% square waves.
- Treat captures as snapshots of current wiring only.
- Prefer a known-good channel as roaming probe when pin labels are ambiguous.
- For protocol validation: report baud/channel/options, file path, decode results.
- Report sample rate, mode, byte count, output path for every capture.

## Building and installing (one-time setup)

### libsigrok4DSL.so
```bash
cd /path/to/DSView
SRC="libsigrok4DSL/version.c libsigrok4DSL/strutil.c ..."
COMMON_SRC="common/minizip/zip.c common/minizip/unzip.c common/minizip/ioapi.c common/log/xlog.c"
gcc -shared -fPIC -O2 -std=c99 -I. -Ilibsigrok4DSL -Icommon \
    -DHAVE_CONFIG_H -D_DEFAULT_SOURCE \
    $(pkg-config --cflags glib-2.0) $(pkg-config --cflags libusb-1.0) -I/usr/include/python3.13 \
    -o libsigrok4DSL.so $SRC $COMMON_SRC \
    $(pkg-config --libs glib-2.0) $(pkg-config --libs libusb-1.0) -lz -lpthread -lpython3.13
sudo cp libsigrok4DSL.so /usr/local/lib/ && sudo ldconfig
```

### dslogic-cli + firmware
```bash
# Build dslogic-cli from source package
# Install to /usr/local/bin/dslogic-cli

# Copy firmware resources
sudo mkdir -p /opt/dslogic/res
sudo cp /path/to/DSView/DSView/res/* /opt/dslogic/res/
```

## Typical workflows

### GPIO validation
1. `logic_analyzer_status` → check `native_ok`
2. `logic_analyzer_capture` at conservative rate (e.g. 1MHz, 1k samples)
3. `scripts/capture_verify.py` on output

### Protocol decode
1. Capture to raw `.bin`
2. `logic_analyzer_decode_file` with correct decoder + channel mapping
3. For SPI: verify CLK/MOSI/CS channel assignments
4. Report decoder, file path, word count, sample decoded words

### Wiring reference
| DSLogic | Target | Signal |
|---------|--------|--------|
| GND | GND | common ground |
| D0 | target output | channel 0 |
| D1 | target output | channel 1 |
| D2 | target output | channel 2 |
| D3 | target output | channel 3 |

## References
- `references/channel-modes.md` — DSLogic Plus mode table, USB bandwidth math
- `references/dsl-driver-internals.md` — libsigrok4DSL stream stop, buffer sizing
- `references/stream-overflow-analysis.md` — buffer overflow root cause
- `references/dsl-format.md` — DSView `.dsl` archive vs CLI raw binary
- `references/pure-c-decoders.md` — native UART/SPI/I2C decoder behavior
- `scripts/capture_verify.py` — raw `.bin` sanity checker
