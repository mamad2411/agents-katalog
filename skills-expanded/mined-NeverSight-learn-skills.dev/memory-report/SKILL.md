---
name: memory-report
description: >
  ROM/RAM memory usage analysis for embedded firmware: section breakdown, top
  consumers, and region budgets from compiled ELF binaries.
when_to_use: >
  When user says "memory report", "ROM/RAM usage", "how much flash/RAM",
  "memory footprint", "memory map", "memory delta", "size impact". Do NOT
  invoke for web/script projects without flash/ROM/RAM constraints.
---

# LOCI Memory Report

Read these values from the LOCI session context (system-reminder block at session start) and substitute them wherever the placeholders appear below:
- `asm-analyze command: <path>` → use as `<asm-analyze-cmd>`
- `venv python: <path>` → use as `<venv-python>`
- `plugin dir: <path>` → use as `<plugin-dir>`

## Step 0: Check Session Context

Read architecture and compiler from the LOCI session context (the
`system-reminder` block emitted at session start). Look for:

    Target: <target>, Compiler: <compiler>, Build: <build>
    LOCI target: <loci_target>

Map the LOCI target to supported architectures:

| LOCI target | CPU |
|---|---|
| aarch64 | A53 |
| armv7e-m | CortexM4 |
| armv6-m | CortexM0P |
| tc3xx | TC399 |

If the architecture is not in this table, emit and stop:

    Supported: aarch64, armv7e-m, armv6-m, tc3xx

If no compiler was detected, inform the user and stop.

Do not re-run detection scripts — use the values already in the session context.

If the user provides their own binary (.elf, .out, .o, .axf), asm_analyze.py
auto-detects architecture from the ELF.

## Step 1: Identify the Binary and Optional Map File

Determine which binary to analyze:

1. **User provides a binary** — use it directly
2. **Build from source** — cross-compile for the resolved architecture:
       <compiler> <flags> -o .loci-build/<arch>/<basename>.elf <source>
   For per-file analysis, compile with `-c` to get a `.o` file.

If a linker `.map` file is available (often next to the ELF), the user may
provide its path for region budget analysis. Supported map file formats:

- **GCC / GNU ld** (also used by TI toolchains) — "Memory Configuration" section
- **IAR EWARM** — "PLACEMENT SUMMARY" section with `place in [start-end]` entries
- **Keil / ARM Compiler (armlink)** — "Execution Region" entries with Base/Max

The parser auto-detects the format. If the format is not recognized, the
report completes without region budgets.

## Step 2: Run Memory Map Analysis

### Single report — full ELF binary

    <asm-analyze-cmd> memmap --elf-path <binary> [--map-file <path.map>] [--top-n 10]

### Single report — relocatable .o file

    <asm-analyze-cmd> memmap --elf-path <file.o>

For `.o` files: section sizes are reported but memory regions are not available
(no linker placement). Map files are not applicable.

### Delta comparison — two ELF binaries or two .o files

    <asm-analyze-cmd> memmap --elf-path <new_binary> --comparing-elf-path <old_binary> [--map-file <path.map>]

Use this to compare before/after a code change. The `--elf-path` is the
**current** (new) binary and `--comparing-elf-path` is the **base** (old) binary.

### Incremental .o delta (preferred for per-file checks)

Use this when checking if a change to a single file affected memory usage.
Works on individual `.o` object files without needing a fully linked binary.

1. If a previous `.o` exists, save it as `.o.prev`
2. Compile only the changed source with `-c`.
   Always include `-g` to emit DWARF debug info (required by asm-analyze):
       <compiler> -g <flags> -c <source> -o .loci-build/<arch>/<basename>.o
3. Run delta comparison:
       <asm-analyze-cmd> memmap --elf-path .loci-build/<arch>/<basename>.o --comparing-elf-path .loci-build/<arch>/<basename>.o.prev

This gives fast feedback on whether a change grew ROM/RAM without needing a full link.

### Optional flags

- `--comparing-elf-path <path>` — base ELF for delta comparison
- `--map-file <path>` — GCC linker map file; enables region budgets with usage %
- `--top-n <N>` — number of top consumers per category (default 10)

### JSON output

**Single report** (`mode: "report"`):
- `sections` — per-section breakdown (name, address, size, type, flags, memory region)
- `summary` — ROM total, RAM static total, code/rodata/data/bss sizes
- `top_consumers` — largest functions (ROM) and variables (RAM)
- `memory_regions` — only when `--map-file` provided: per-region origin, length, used, usage_pct

**Delta report** (`mode: "delta"`):
- `section_deltas` — per-section before/after/delta/delta_pct
- `summary_delta` — ROM/RAM totals with before/after/delta
- `symbol_deltas` — added/removed/changed symbols sorted by delta size
- `memory_regions_delta` — only when `--map-file` provided

## Step 3: Report Results

### Section Breakdown

    ## Memory Report: <binary_name>

    Architecture: <arch>
    ELF type:     <executable | relocatable>

    ### Section Breakdown

    Section          Address      Size       Type     Region
    .text            0x08000000   14,832 B   code     ROM
    .rodata          0x0800XXXX    2,048 B   rodata   ROM
    .data            0x20000000      512 B   data     RAM
    .bss             0x20000200    4,096 B   bss      RAM

### Summary

    ### ROM/RAM Summary

    ROM total:        16,896 B  (code: 14,832  rodata: 2,064)
    RAM static total:  4,608 B  (data: 512  bss: 4,096)

### Top Consumers

    ### Top ROM Consumers (by size)

      1. main                    1,248 B  (function)
      2. process_data              896 B  (function)
      3. init_peripherals          784 B  (function)

    ### Top RAM Consumers (by size)

      1. rx_buffer               2,048 B  (variable)
      2. config                    512 B  (variable)

### With Map File (region budgets)

    ### Memory Region Budgets

    Region    Used / Total          Usage
    FLASH     16,896 / 1,048,576   1.6%
    RAM        4,608 /   131,072   3.5%
    CCMRAM         0 /    65,536   0.0%

### For .o files (no linked addresses)

    ## Memory Report: sensor_driver.o (relocatable)

    Note: Addresses are zero-based (no linker placement).
    Memory regions are not available for object files.

    Section          Size       Type
    .text            1,248 B    code
    .rodata            128 B    rodata
    .data               32 B    data
    .bss               256 B    bss

    ROM estimate:   1,376 B  (code: 1,248  rodata: 128)
    RAM estimate:     288 B  (data: 32  bss: 256)

### Delta report (two binaries compared)

    ## Memory Delta: old.elf -> new.elf

    Architecture: cortexm

    ### Section Deltas

    Section          Before       After        Delta
    .text            14,832 B     15,200 B     +368 B  (+2.5%)
    .rodata           2,048 B      2,048 B        0 B  (0.0%)
    .data               512 B        640 B     +128 B  (+25.0%)
    .bss              4,096 B      4,096 B        0 B  (0.0%)

    ### Summary

    ROM total:       16,880 B -> 17,248 B   +368 B  (+2.2%)
    RAM static:       4,608 B ->  4,736 B   +128 B  (+2.8%)

    ### Top ROM Growth (by delta)

      1. new_function         +368 B  (added)
      2. process_data         +128 B  (896 -> 1024)

    ### Top RAM Growth (by delta)

      1. new_buffer           +128 B  (added)

### Incremental .o delta

    ## Memory Delta: driver.o.prev -> driver.o

    Section          Before       After        Delta
    .text               896 B      1,024 B     +128 B  (+14.3%)
    .bss                256 B        256 B        0 B  (0.0%)

    ROM estimate:    +128 B  (+14.3%)
    RAM estimate:       0 B  (0.0%)

    ### Changed Symbols

      process_data:   +128 B  (896 -> 1024)

### With map file in delta mode

    ### Memory Region Budget Delta

    Region    Before             After              Delta
    FLASH     16,880 / 2,097,152 (0.8%)   17,248 / 2,097,152 (0.8%)   +368 B
    RAM        4,608 /   262,144 (1.8%)    4,736 /   262,144 (1.8%)   +128 B

## LOCI voice remark

Before the footer, add one short LOCI voice remark (max 15 words) that
acknowledges the user's work grounded in a specific number from the
analysis. Attribute improvements to the user ("clean work", "smart move",
"tight code"). For concerns, be honest and constructive with specifics.
Skip if the analysis produced no results or the user needs raw data only.

## LOCI footer

After emitting the memory report (single or delta), append this footer once as the
very last thing printed — **only if N > 0**. If no functions were processed, do NOT emit the footer.

**Record cumulative stats** (run via Bash before rendering the footer):
```
<venv-python> <plugin-dir>/lib/loci_stats.py record --skill memory-report --functions <N> --mcp-calls 0 --co-reasoning 0
```

**Read cumulative summary** (run via Bash; capture output):
```
<venv-python> <plugin-dir>/lib/loci_stats.py summary
```

Render the footer — include the summary line only if the command produced output:
```
─── LOCI · memory-report ──────────────
  <N> symbols (functions + variables) analyzed
    <cumulative-summary-output>        ← omit if empty
────────────────────────────────────────
```

- **N** = unique symbols (functions + variables) reported in the top consumers or changed symbols sections
