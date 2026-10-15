---
name: embedded-debugger
description: Embedded hardware debugging workflow for probe-rs targets using embedded-debugger-mcp. Use when Codex or Claude Code needs to inspect debug probes, validate embedded debugger setup, start the MCP server, guide a user through ARM Cortex-M/RISC-V flashing/debugging/RTT workflows, or operate without installing an MCP client by using the CLI plus prompts.
---

# Embedded Debugger

Use the local `embedded-debugger-mcp` binary as the source of truth. Prefer CLI
checks first, then MCP tools when an MCP client is available.

## Entry Decision

1. If the user has an MCP client configured, start or verify the server:
   `embedded-debugger-mcp serve`
2. If the user wants no MCP install, use CLI-first mode:
   `embedded-debugger-mcp doctor`, `embedded-debugger-mcp probes list`, and
   `embedded-debugger-mcp skill print-prompt`.
3. If hardware access is required, confirm the probe and target are connected
   before destructive actions such as flash erase or program.

## CLI Workflow

Run these in order and report the exact outcome:

```bash
embedded-debugger-mcp doctor
embedded-debugger-mcp probes list
embedded-debugger-mcp config show
```

Use JSON for automation:

```bash
embedded-debugger-mcp doctor --json
embedded-debugger-mcp probes list --json
```

## Backends

One tool set runs over two interchangeable engines, chosen at `connect`:

- `backend: "probe-rs"` (default) — native probe-rs; supports flash and RTT.
- `backend: "openocd"` (experimental) — talks to an already-running `openocd`
  over its GDB port via `openocd_address` (default `127.0.0.1:3333`). Use for
  chips probe-rs does not cover well (e.g. Xtensa ESP32 via openocd-esp32).
  Memory access and halt/run/step/reset are validated on real ESP32-S3; flash
  and RTT are not available on this backend. Register reads currently use ARM
  gdb register numbers, so PC/SP are wrong on Xtensa (known limitation).
  `diagnose_fault` and `unwind_exception` are Cortex-M specific and do not
  apply to Xtensa targets.
  - Start openocd with `gdb_memory_map disable`, otherwise it probes flash on
    the GDB connect, fails, and REJECTS the connection. Example:
    `openocd -f board/esp32s3-builtin.cfg -c "gdb_memory_map disable"`.

The AI uses the same tools regardless of backend; only `connect` differs.

## MCP Workflow

Use MCP tools for session-based operations:

1. `list_probes`
2. `connect` (add `backend: "openocd"` and `openocd_address` to use OpenOCD)
3. Read-only checks such as `probe_info`, `get_status`, and `read_memory`
4. On a crash or halt, call `diagnose_fault`: it reads the Cortex-M SCB fault
   registers (CFSR/HFSR/MMFAR/BFAR/SHCSR/CPUID) plus PC/SP/LR and returns a
   compact structured evidence bundle in one call. Halt the target first for
   meaningful values; reason over the set fault bits yourself. Then call
   `unwind_exception` with `elf_path` to map the crash to a source line
   (full DWARF backtrace on probe-rs; faulting PC/LR on OpenOCD).
5. Mutating operations only after the user confirms target, file path, and risk:
   `write_memory`, `flash_erase`, `flash_program`, `run_firmware` (probe-rs)
6. RTT operations after firmware is running: `rtt_attach`, `rtt_channels`,
   `rtt_read`, `rtt_write`, `rtt_detach` (probe-rs)
7. `disconnect`

## Fetch authoritative info yourself

You are a capable model: prefer fetching ground truth over relying on memorized
or hardcoded chip data. This skill points you to sources; it does not embed
register tables. In order of authority:

1. The target itself (runtime, most authoritative for this exact chip):
   registers are self-described by the GDB target description; memory is read
   with `read_memory`; core identity from CPUID / the connected target.
2. The firmware ELF (what is actually running): symbols and source lines come
   from DWARF — use `unwind_exception` (pass `elf_path`) to map addresses to
   `file:line`.
3. The chip datasheet / reference manual (external, per-chip): for a peripheral
   or fault register, find the peripheral's base in the memory-map chapter, add
   the register offset, then `read_memory`. Search the vendor document for the
   exact value; do not guess addresses from memory. CMSIS-SVD files are a
   machine-readable source for register maps.
4. ARM Cortex-M architecture registers (SCB fault regs, CPUID) are fixed by the
   ARM architecture and identical across vendors — `diagnose_fault` reads them.
   They do not exist on non-Cortex-M targets (e.g. Xtensa ESP32).

Do not hardcode or invent register/peripheral addresses. If a value is not
recoverable from the target, the ELF, or a cited datasheet, say so.

## Know your versions

Behavior and target support depend on tool versions — check them before
concluding something is unsupported or broken:

- probe-rs version determines which chips and architectures are supported
  (e.g. Xtensa support is comparatively new). Check `embedded-debugger-mcp doctor`.
- OpenOCD version and fork matter: the Espressif fork (openocd-esp32) is needed
  for Xtensa ESP32, and some targets need flags like `gdb_memory_map disable`.
  Check `openocd --version`.
- Probe firmware (ST-Link / J-Link) can affect connectivity; `probes list`
  reports the connected probe.

## Safety Rules

- Treat flash erase, flash program, memory write, reset, run, and RTT write as
  mutating hardware operations.
- Prefer read-only discovery before mutation.
- Respect project configuration limits for file paths, file sizes, memory
  ranges, and flash erase permissions.
- Do not claim hardware success from command text alone; cite the command or MCP
  tool result that produced the evidence.

## Prompt Reference

For a reusable CLI+Skill prompt, read
`references/default-prompt.md`.
