# .clinerules - Technical Rules for libtnc

TNC-related utilities library for AX.25 packet radio. Contains utilities both intended for use **in** a TNC program as well as others **interfacing** with a TNC.

## Code Style

- **Minimal comments**—self-explanatory code preferred
- **Function prefixes** group related functionality: `ax25_`, `hldc_`, `kiss_`, `tnc2_`, `crc_`, `line_`, `buf_`
- **Struct-based organization** with `init()`, `process()`, `free()` pattern
- **Buffer safety**: Always pass buffer size, verify available capacity before writes
- **Error codes**: 0 = success, negative = error
- **Goto for cleanup** only in main functions

## Module Breakdown

### Protocols

- `ax25_addr_*` / `ax25_packet_*`: AX.25 (7-byte addresses: 6-char callsign, SSID, repeat flag)
- `hldc_framer_*` / `hldc_deframer_*`: HDLC framing (NRZI, bit stuffing, CRC-CCITT 0xFFFF, 0x7E flags)
- `tnc2_*`: TNC2 text format parsing (human-readable: STATION>DEST,PATH:DATA)
- `kiss_*`: KISS binary protocol with escape sequences (PORT + COMMAND + data, 0xC0 delimiters)
- `crc_ccitt_*`: CRC-CCITT checksums (16-bit CRC calculation)

### Core

- `buf_*`: Buffer capacity/size checks and safe write operations
- `line_*`: Buffered line reader with callback for parsing line-based input
- `common_*`: Logging macros and utilities

## Protocol Details

**AX.25**: 7-byte addresses (6-char space-padded callsign + 4-bit SSID + repeat flag)
**HDLC**: NRZI encode → bit-stuff (insert 0 after five 1s) → CRC-CCITT → 0x7E delimiters
**KISS**: PORT + COMMAND + data bytes, 0xC0 frame delimiters, 0xDB escape
**TNC2**: Human-readable (e.g., STATION>DEST,PATH:DATA)

## Logging

Macros in `common.h`, output to stderr, auto-includes function name:

- `LOG(str, ...)`: Always visible
- `LOGV(str, ...)`: With `--verbose`
- `LOGD(str, ...)`: With `--debug` only
- `EXIT(code, str, ...)`, `EXITIF(cond, code, ...)`: Fatal errors
- `nonnull(val, name)`, `nonzero(val, name)`: Input validation (exit -2/-3)

Messages: lowercase start, no period/newline (auto-added).

## Build

**Library**: `libtnc.a` (static)

**Makefile targets**: `build`, `release`, `test`, `install`, `clean`

## Unit Testing

- Test files: `test_*.h` (functions matching `void test_name(void)`)
- Added to `main_test.c`
- Run via `make test`
- Use assertion macros from `test.h`
- Test: normal operation, boundary conditions (empty/full/wrap), init/free, diverse inputs

## Using in real projects

Refer to snippets in `README.md` for usage examples.
