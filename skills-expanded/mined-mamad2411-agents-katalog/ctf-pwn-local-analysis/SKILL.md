---
name: ctf-pwn-local-analysis
description: Use when pi needs to analyze a local Linux pwn binary, libc, loader, or exploit workflow. Covers ELF fingerprinting, protection checks, symbol and section inspection, gadget hunting, pwntools-based exploit scaffolding, and deciding when to switch from static analysis to runtime debugging. Trigger on mentions of pwn, ELF, libc, ld.so, ROP, ret2libc, GOT/PLT, canary, PIE, checksec, gadgets, cyclic offsets, pwntools, or local binary analysis.
---

# CTF Pwn Local Analysis

Use this skill for local analysis of Linux pwn artifacts on this (Linux) host.

Default behavior:

- Use the native Linux toolchain first (`file`, `readelf`, `objdump`, `strings`, `gdb`, `ROPgadget`, `checksec`, `pwntools`).
- Pull the target binary, matching `libc.so.6`, and relevant helper files into the challenge workspace before deeper analysis.
- Use runtime debugging (`gdb`, `/proc`, real loader) when the task needs actual execution behavior.

## Environment Notes

- `pwntools` is **not** installed. Per AGENTS.md 安装约定，装进 `sage10.9` env（`conda run -n sage10.9 pip install pwntools`）或 `tools/pylibs`，不要全局 `pip install`。
- `gdb`, `ROPgadget`, `checksec` may be missing too; check with `command -v` first. Per AGENTS.md 安装约定，装进 `tools/bin`（gdb 等二进制）或 `sage10.9` env（ROPgadget/pwntools 等 Python 包），不要全局安装。
- Native `readelf`, `objdump`, `strings`, `file` come from `binutils`/`file` packages and are usually present.

## Local Toolchain

- `file`: `file`
- `checksec`: `pwn checksec`（pwntools 装好后）或 `checksec`（装进 `tools/pylibs`/`sage10.9` env）
- `python`: `python3`
- `ROPgadget`: `ROPgadget` (pip) — `ropper` is an alternative if installed
- `readelf`, `objdump`, `strings`, `gdb`: from PATH (`binutils`, `gdb`)

Notes:

- Prefer plain command names from PATH; use absolute paths only if PATH resolution is inconsistent.
- `gdb` is a real Linux debugger here — use it directly for runtime analysis.

## Workflow

1. Stage the artifacts locally (copy into the challenge folder).
2. Fingerprint the binary and protections.
3. Inspect sections, symbols, relocations, and imports.
4. Hunt gadgets and compute offsets.
5. Build or refine the exploit with `pwntools`.
6. Drop into `gdb` when static analysis is no longer enough.

## Quick Start

Use this initial pass on a new binary:

```bash
file ./chall
checksec --file=./chall          # or: pwn checksec ./chall
readelf -h ./chall
readelf -Ws ./chall
readelf -d ./chall
strings -a ./chall | grep -E 'main|puts|system|/bin/sh|flag|menu'
```

Use this pass to answer:

- architecture and bitness
- dynamic vs static
- RELRO, Canary, NX, PIE
- stripped vs symbol-rich
- obvious imported functions, menus, and useful strings

## Static Analysis

Use `readelf` when you need structured metadata:

```bash
readelf -l ./chall
readelf -S ./chall
readelf -Ws ./chall
readelf -r ./chall
readelf -d ./chall
```

Use `objdump` when you need disassembly or relocation context:

```bash
objdump -d -M intel ./chall
objdump -R ./chall
objdump -T ./libc.so.6
```

Practical targets:

- find PLT/GOT entries for leak targets
- confirm whether the bug is before or after stack canary checks
- spot unsafe calls such as `gets`, `scanf`, `strcpy`, `memcpy`, `system`
- recover menu logic and argument flow when the binary is small

## Gadgets And Offsets

Use `ROPgadget` for gadget hunting:

```bash
ROPgadget --binary ./chall --only "ret|pop|leave"
ROPgadget --binary ./libc.so.6 --only "ret|pop|leave"
```

Use `pwntools` for cyclic patterns and address helpers:

```bash
python3 -c "from pwn import *; print(cyclic(200))"
python3 -c "from pwn import *; print(cyclic_find(0x6161616c))"
python3 -c "from pwn import *; elf = ELF('./chall'); print(hex(elf.plt.get('puts', 0))); print(hex(elf.got.get('puts', 0)))"
```

Checklist:

- verify the RIP overwrite offset from disassembly or a cyclic pattern
- identify whether a stack-alignment `ret` gadget is needed on amd64
- if using ret2libc, compute `libc_base`, `system`, `setuid`, `dup2`, `execve`, and `"/bin/sh"` from the exact libc when possible

## Exploit Scaffolding

Prefer a small `pwntools` scaffold before writing the final exploit:

```python
from pwn import *

context.binary = elf = ELF("./chall")
libc = ELF("./libc.so.6", checksec=False)

io = process([elf.path])

# leak parsing here
# libc.address = leaked_puts - libc.sym.puts
# payload construction here
```

Keep these pieces separate:

- leak collection
- base-address calculation
- gadget and symbol lookup
- final payload assembly
- local or remote tube selection

## Runtime Debugging

Drop into `gdb` directly when needed:

- the binary must actually execute under Linux
- you need `gdb`, `gdbserver`, `strace`, `/proc/<pid>/maps`, or loader behavior
- the target uses Linux-only syscalls, SUID behavior, namespaces, or seccomp details that static inspection cannot validate

```bash
gdb -q ./chall
# inside gdb: run, break *main, info proc mappings, x/20gx $rsp, etc.
```

If the skill is running in a restricted sandbox and local tool access or network access fails for environmental reasons, ask the user for global permissions and retry instead of treating the failure as a property of the binary.

## Notes

- Pull the matching `libc.so.6` whenever a leak-based exploit depends on symbol offsets.
- Save large disassembly outputs to files instead of flooding the conversation.
- For quick triage of a suspicious SUID binary, prioritize `file`, `checksec`, `strings`, `readelf -Ws`, and `objdump -d -M intel` before writing an exploit.
