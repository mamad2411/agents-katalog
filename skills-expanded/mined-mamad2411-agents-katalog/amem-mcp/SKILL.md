---
name: amem-mcp
description: Use this skill when Codex needs to operate AMem through its MCP server or reason about AMem MCP tools, including checking GUI/IPC status, selecting Android processes, reading or writing memory, scanning values, managing hardware breakpoints, running Lua, resolving modules, or querying symbols. It provides safety rules, required workflow order, parameter constraints, and verification expectations for the live AMem memory-debugging MCP bridge.
---

# AMem MCP Usage Rules

## Core Contract

AMem MCP is a live memory-debugging bridge:

`Codex -> MCP stdio -> amem_mcp Python server -> AMem GUI IPC HTTP -> Android target`

Treat every operation as acting on the currently attached AMem GUI session. Do not invent process IDs, module names, addresses, handles, scan results, breakpoint hits, or Lua output. Read state first, then act from observed data.

## Required Workflow

1. Start with `get_status()`.
2. If the GUI or IPC is not reachable, explain that AMem GUI must be running and do not call mutating tools.
3. If no target process is open, use `list_processes()` and then `open_process(pid)` only when the user identified the target or the process choice is unambiguous.
4. For module-relative work, call `list_modules()` or `get_module_base(module_name)` before computing addresses.
5. Prefer read-only tools until the target, address, type, and expected effect are clear.
6. After any write, breakpoint change, or Lua action, verify with a read-back/status/list call when possible.

## Safety Boundaries

- Do not perform writes, breakpoint changes, driver initialization, or Lua execution unless the user explicitly requested that class of action or has approved the specific plan.
- Before a mutating call, know the process, address/module, data type, value/bytes, and expected size.
- Keep reads small and targeted. Use `read_value()` for typed reads and `read_memory()` only for byte ranges.
- Use `execute_lua(code)` only when MCP tools are insufficient or the user specifically asks for Lua automation. Keep Lua scripts short, deterministic, and scoped to the selected process.
- Avoid broad `scan_set_range("all")` scans unless the user requested a full scan or no narrower range is available.
- Clean up temporary breakpoints with `remove_breakpoint()` or restore them with `resume_breakpoint()` when the task is done.

## Parameter Rules

Use the MCP layer's validation rules deliberately:

- Addresses, module bases, and offsets must be non-negative integers; decimal and `0x` hex strings are valid.
- `size` and `count` must be positive. `read_memory` is capped at 65536 bytes. Paginated list calls are capped at 1000 items.
- Hex byte strings may contain whitespace, but after whitespace removal they must be non-empty, valid hex, and even length.
- Valid `data_type`: `byte`, `word`, `dword`, `qword`, `float`, `double`, `xor`.
- Valid `scan_type`: `exact`, `unknown`, `greater`, `less`, `between`, `increased`, `increased_by`, `decreased`, `decreased_by`, `changed`, `unchanged`.
- Valid `memory_type`: `all`, `anonymous`, `c_alloc`, `c_heap`, `c_data`, `c_bss`, `java_heap`, `java`, `stack`, `code_app`, `code_system`, `video`, `ashmem`, `bad`.
- Valid breakpoint types: `1/read`, `2/write`, `3/readwrite/access`, `4/execute`. Valid breakpoint sizes: `1`, `2`, `4`, `8`; execute breakpoints use size `4`.

## Operation Guidance

### Process and Modules

- Use `list_processes()` before `open_process(pid)` unless the PID is already known from the current AMem status or user request.
- Use `list_modules(filter, offset, count)` for discovery and pagination.
- Use `resolve_offset_chain(module, base_offset, offsets, deref_final)` for pointer chains instead of manually mixing module bases and reads.

### Memory Reads and Writes

- Use `read_value(address, data_type)` for scalar inspection.
- Use `read_memory(address, size)` for context bytes or hex dump inspection.
- Use `write_value(address, value, data_type)` for typed writes and `write_bytes(address, hex_string)` for raw patches.
- After writing, read the same address and type/range back to verify the result.

### Scanning

- Set a memory range first when the region is known.
- Use `scan_value()` for the first exact/relational scan, then `scan_next()` to refine.
- Use `scan_fuzzy()` only for unknown initial values or change tracking.
- Use `get_scan_count()` before pulling large pages of results.
- Use `get_scan_results(offset, count)` in pages; do not assume the first page contains the desired address.

### Breakpoints

- Prefer `write` breakpoints for finding writers, `read` for readers, `readwrite/access` for access tracking, and `execute` for code flow.
- Read hits with `read_breakpoint_info(address)` and summarize PC/SP/registers rather than dumping everything blindly.
- Suspend or remove breakpoints when they are no longer needed.

### Lua and Driver Initialization

- `init_driver(card_name)` requires a non-empty card/auth string and may change driver state.
- `execute_lua(code)` can perform complex actions inside AMem. Show or summarize the intended code path before execution unless the user supplied the exact code.
- If Lua fails, include both the error and captured output when reporting back.

### Symbols

- Call `symbol_init(module_base)` before `symbol_list()` or use `symbol_list(..., module_base=...)` to initialize and list in one step.
- Use `symbol_find(module_base, symbol_name)` only after the module base is known.

## Error Handling

- MCP errors may originate from the Python validation layer, the GUI IPC HTTP layer, or the Android socket backend.
- Validation errors mean the request should be corrected before retrying.
- Connection errors usually mean AMem GUI is not running or IPC port `28100` is unavailable.
- GUI IPC JSON errors should be reported as-is because they often contain the most precise failure reason.
- Do not repeatedly retry mutating operations after ambiguous failures; re-check status and read current state first.

## Reference Files

When editing or auditing this MCP implementation, read:

- `mcp/README.md` for installation, tool list, validation rules, and self-check commands.
- `mcp/reference/README.md` before using `reference/amem_client.py`; it is a binary protocol reference, not the MCP server path.
