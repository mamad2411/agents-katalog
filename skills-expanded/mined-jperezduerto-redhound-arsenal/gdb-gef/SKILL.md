---
name: gdb-gef
description: >
  Build, extend, and operate GDB with GEF (GDB Enhanced Features) for binary exploit development,
  reverse engineering, and vulnerability research. Use when debugging ELF/PE/Mach-O binaries,
  developing heap or stack exploits, analyzing memory layout, building ROP chains, or integrating
  GDB with pwntools. Use when the user asks about GEF commands (vmmap, heap, checksec, pattern,
  xinfo, rop, canary), heap exploitation helpers, breakpoints, memory examination, or comparing
  GEF with PEDA and pwndbg.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/hugsy/gef
  stars: '7.1k'
---

# gdb-gef Agent Skill

## When to Use This Skill

Use this skill when:
- Developing exploits for CTF challenges or authorized vulnerability research
- Analyzing heap exploitation (tcache, fastbin, unsorted bin, largebin attacks)
- Examining stack layout for buffer overflow / ROP chain development
- Investigating memory corruption bugs (use-after-free, heap overflow, format string)
- Integrating GDB into a pwntools exploit development workflow
- Checking binary mitigations (ASLR, NX, PIE, stack canary, RELRO)
- Building and validating ROP gadget chains
- Comparing GEF functionality against PEDA and pwndbg

## What GDB + GEF Does

GDB (GNU Debugger) is the standard debugger for compiled binaries on Linux/macOS. GEF (GDB Enhanced Features) is a Python plugin that extends GDB with exploit-development-specific commands: colorized context output (registers, stack, code, threads), heap introspection, binary mitigation detection, pattern generation, format string analysis, ROP gadget search, and memory mapping utilities. GEF is the most actively maintained GDB plugin for exploit development, alongside pwndbg and the older PEDA.

## Installation

```bash
# One-liner GEF install (fetches and adds to ~/.gdbinit)
bash -c "$(curl -fsSL https://gef.blah.cat/sh)"

# Manual install
wget https://github.com/hugsy/gef/raw/main/gef.py -O ~/.gdbinit-gef.py
echo source ~/.gdbinit-gef.py >> ~/.gdbinit

# Verify
gdb -q
# Should show: GEF for linux ready, X commands loaded

# Optional dependencies (unlocks additional features)
pip install keystone-engine        # Assembly in gef assemble
pip install capstone               # Disassembly engine
pip install unicorn                # Emulation
pip install ropper                 # ROP chain builder
pip install ROPgadget              # Alternative ROP gadget finder

# GDB install (if needed)
sudo apt-get install gdb gdb-multiarch

# For multi-arch (ARM, MIPS, RISC-V analysis)
sudo apt-get install gdb-multiarch qemu-user-static
gdb-multiarch ./arm-binary
```

### ~/.gdbinit Best Practices

```
source ~/.gdbinit-gef.py
set disassembly-flavor intel           # Intel syntax (not AT&T)
set follow-fork-mode child             # Follow child process on fork
set detach-on-fork off                 # Keep parent alive too
set print pretty on
set history save on
set history filename ~/.gdb_history
set history size 10000
```

## Starting GDB

```bash
# Debug a binary
gdb ./vuln

# Attach to running process
gdb -p 1234

# With arguments
gdb --args ./vuln arg1 arg2

# Run via pwntools (see pwntools section)
# Core dump analysis
gdb ./vuln core

# Remote target (gdbserver)
gdb ./vuln
(gdb) target remote 192.168.1.1:4444
```

## GEF Context Display

When execution stops (breakpoint, SIGSEGV, etc.), GEF shows an automatic context panel:

```
──────────────────────── registers ──────────────────────────
$rax   : 0x0
$rbx   : 0x00007ffff7ffe2d0
$rcx   : 0x00000000004011f0
$rip   : 0x0000000000401162
...
──────────────────────── stack ──────────────────────────────
0x00007fffffffe350│+0x0000: 0x00007fffffffe450
0x00007fffffffe358│+0x0008: 0x0000000000401196
...
──────────────────────── code ───────────────────────────────
   0x401155 <main+0>:   push   rbp
   0x401156 <main+1>:   mov    rbp,rsp
→  0x401162 <main+13>:  call   0x401030 <gets@plt>
...
──────────────────────── threads ────────────────────────────
[#0] Id 1, Name: "vuln", stopped at 0x401162, reason: BREAKPOINT
──────────────────────── trace ──────────────────────────────
[#0] 0x401162 → main()
```

Control context sections:

```
gef➤ gef config context.layout "regs stack code args source threads trace"
gef➤ gef config context.nb_lines_stack 10
gef➤ gef config context.nb_lines_code 8
```

## Key GEF Commands

### Binary Information

```
# Check security mitigations
gef➤ checksec
[*] /home/user/vuln
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)

# ASLR status
gef➤ aslr
ASLR is ON

# Toggle ASLR for testing
gef➤ aslr off

# Virtual memory map
gef➤ vmmap
[ Legend:  Code | Heap | Stack ]
Start              End                Offset             Perm Path
0x0000000000400000 0x0000000000401000 0x0000000000000000 r-- /home/user/vuln
0x0000000000401000 0x0000000000402000 0x0000000000001000 r-x /home/user/vuln
0x00007ffff7d00000 0x00007ffff7f2c000 0x0000000000000000 r-x /lib/x86_64-linux-gnu/libc.so.6

# Show specific mapping
gef➤ vmmap stack
gef➤ vmmap heap
gef➤ vmmap libc
```

### Memory Examination (x command)

```
# Examine N units of format fmt at address
# Format: x/[N][fmt][unit]  where unit = b(byte) h(half) w(word=4B) g(giant=8B)
# fmt: x(hex) d(decimal) s(string) i(instruction) c(char)

# 10 hex words at rsp
gef➤ x/10xg $rsp

# String at address
gef➤ x/s 0x402010

# Disassemble 20 instructions at rip
gef➤ x/20i $rip

# Hex dump of 64 bytes
gef➤ x/64xb $rsp

# Follow pointer chain
gef➤ x/xg $rbp
gef➤ x/xg <value from above>

# Hex/ASCII dump
gef➤ hexdump byte $rsp 64
gef➤ hexdump dword $rsp 32
```

### xinfo — Detailed Address Information

```
# Show what address/symbol belongs to which mapping
gef➤ xinfo 0x00007ffff7a8d3a0
──────────────────────── xinfo: 0x7ffff7a8d3a0 ──────────────────────
Contained in : /lib/x86_64-linux-gnu/libc-2.31.so [r-x]
Offset (from base): 0x6d3a0
Symbol: __GI__IO_puts
```

### Pattern Generation (De Bruijn)

```
# Generate 200-byte De Bruijn pattern
gef➤ pattern create 200
[+] Generating a pattern of 200 bytes (n=8)
aaaabaaacaaadaaaeaaafaaagaaah...
# (automatically copied to clipboard and stored)

# Run the binary and let it crash
gef➤ run < <(python3 -c "import sys; sys.stdout.buffer.write(b'aaaabaaacaaadaaaeaaafaaagaaah...')")

# After crash — find offset of EIP/RIP
gef➤ pattern search $rsp
[+] Searching '$rsp'
[+] Found at offset 72 (little-endian search)

# Search for specific sequence in pattern
gef➤ pattern search 0x6161616e
[+] Searching '0x6161616e'
[+] Found at offset 40
```

### Registers

```
# Show all registers
gef➤ info registers
gef➤ info registers rax rbx rcx

# GEF-enhanced register view (colored, with derefs)
# Shown automatically in context

# Set register value
gef➤ set $rax = 0x1337

# Show register as different types
gef➤ p/x $rsp
gef➤ p/d $rax
```

### Breakpoints and Watchpoints

```
# Software breakpoint at address or symbol
gef➤ break main
gef➤ break *0x401162
gef➤ b *0x401162       # shorthand

# Hardware breakpoint (survives self-modifying code)
gef➤ hbreak *0x401162

# Conditional breakpoint
gef➤ break *0x401162 if $rax == 0

# Watchpoint (break on memory access)
gef➤ watch *0x602060        # write watchpoint
gef➤ rwatch *0x602060       # read watchpoint
gef➤ awatch *0x602060       # read/write

# List breakpoints
gef➤ info breakpoints
gef➤ info break

# Delete breakpoint by number
gef➤ delete 1

# Disable/enable
gef➤ disable 2
gef➤ enable 2

# Temporary breakpoint (auto-deletes after hit)
gef➤ tbreak *0x401162
```

### Stepping

```
# Continue execution
gef➤ continue  (or c)

# Step one source line (into calls)
gef➤ step       (or s)

# Step one source line (over calls)
gef➤ next       (or n)

# Step one machine instruction (into calls)
gef➤ si

# Step one machine instruction (over calls)
gef➤ ni

# Run until current function returns
gef➤ finish

# Advance to specific address
gef➤ advance *0x401200

# Jump to address (skip instructions)
gef➤ jump *0x401250
```

### GOT and PLT Analysis

```
# Show Global Offset Table entries
gef➤ got
[0x601018] puts@GLIBC_2.2.5  →  0x7ffff7a64aa0 → libc!puts
[0x601020] printf@GLIBC_2.2.5 →  0x7ffff7a3d3e0 → libc!printf
[0x601028] gets@GLIBC_2.2.5  →  0x7ffff7a62970 → libc!gets

# Overwrite GOT entry (for testing)
gef➤ set *0x601028 = 0x00007ffff7a64aa0  # redirect gets → puts
```

### Stack Canary

```
# Check if canary exists and show its value
gef➤ canary
[+] The canary of process 12345 is at 0x00007ffff7ff7040, value is 0x7c49b0e3b9cc5b00

# In context display — canary is highlighted in stack
```

## Heap Exploitation Helpers

GEF provides comprehensive glibc heap introspection:

```
# Show all heap chunks
gef➤ heap chunks
gef➤ heap chunks 0x603000   # specific arena base

# Show free lists (bins)
gef➤ heap bins
gef➤ heap bins tcache       # tcache bins only
gef➤ heap bins fast         # fastbins only
gef➤ heap bins unsorted     # unsorted bin
gef➤ heap bins small        # small bins
gef➤ heap bins large        # large bins

# Specific chunk info
gef➤ heap chunk 0x603010

# Show all arenas (multi-threaded)
gef➤ heap arenas

# Find heap corruption (basic)
gef➤ heap chunks  # look for chunks where prev_inuse bit inconsistencies
```

### Common Heap Attack Verification

```
# Tcache poisoning: after double-free, verify fd pointer
gef➤ heap bins tcache
# Should show corrupted fd → arbitrary address in tcache list

# Fastbin attack: verify fake chunk in fastbin
gef➤ heap bins fast

# Unsorted bin leak: after freeing large chunk, fd/bk point to libc arena
gef➤ heap bins unsorted
# fd == bk == main_arena+88 → libc leak
```

## ROP and Gadget Tools

```
# Built-in ROPgadget search
gef➤ rop  --grep "pop rdi"

# Using ropper (if installed)
gef➤ ropper --search "pop rdi; ret"

# Find ret2libc gadgets
gef➤ rop --grep "pop rdi; ret" --binary /lib/x86_64-linux-gnu/libc.so.6

# External ROPgadget
ROPgadget --binary ./vuln --rop --badbytes "0a"
ROPgadget --binary ./vuln --string "/bin/sh"

# Search for string in binary
gef➤ search-pattern "/bin/sh"
[+] Searching '/bin/sh' in memory
[0x7ffff7b97d88-0x7ffff7b97d8f]  "/bin/sh\x00" in /lib/x86_64-linux-gnu/libc-2.31.so
```

## Format String Helper

```
# Analyze a format string vulnerability
gef➤ format-string-helper
[+] Generating payload for ASAN/format-string...
# Provides offsets and payload suggestions for format string exploitation
```

## Integration with pwntools

```python
from pwn import *

# Attach GDB + GEF to a running pwntools process
context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']  # or ['x-terminal-emulator', '-e']

# Local process
p = process('./vuln')
gdb.attach(p, gdbscript='''
set follow-fork-mode child
break *0x401162
continue
''')

# With GEF commands in gdbscript
gdb.attach(p, gdbscript='''
gef config context.layout "regs stack code"
break main
continue
vmmap
heap bins
''')

# Remote with gdbserver
# On target: gdbserver 0.0.0.0:4444 ./vuln
p = remote('target', 1337)
gdb.attach(('target', 4444), gdbscript='continue')
```

### pwntools + GEF Exploit Template

```python
from pwn import *

elf = ELF('./vuln')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
rop = ROP(elf)

context.binary = elf
context.arch = 'amd64'

p = process('./vuln')

if args.GDB:
    gdb.attach(p, gdbscript='''
        break *{}
        continue
    '''.format(hex(elf.sym['vulnerable_func'])))

# Build ROP chain
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]

payload = flat({
    0: b'A' * 72,          # padding to RIP
    72: pop_rdi,
    80: next(elf.search(b'/bin/sh')),
    88: elf.sym['system'],
})

p.sendlineafter(b'Input: ', payload)
p.interactive()
```

## Exploit Development Workflow

### Phase 1 — Reconnaissance

```
gef➤ checksec               # identify mitigations
gef➤ info functions         # function list
gef➤ info variables         # global variables
gef➤ vmmap                  # memory layout
gef➤ x/s <address>         # find interesting strings
gef➤ search-pattern "/bin/sh"
```

### Phase 2 — Crash and Offset

```
gef➤ pattern create 300
gef➤ run < pattern.txt
# SIGSEGV
gef➤ pattern search $rsp    # or $rip for 32-bit
# offset: 72
```

### Phase 3 — Control Flow

```
gef➤ break *0x401162
gef➤ run < payload.py
gef➤ x/20xg $rsp           # verify stack layout
gef➤ ni                     # step through return
```

### Phase 4 — ROP and Leak

```
# ret2plt leak (if PIE off)
gef➤ got                    # find PLT addresses
gef➤ rop --grep "pop rdi"  # find gadget

# After leak — calculate libc base
# gef➤ vmmap libc (shows actual base after leak applied)
```

### Phase 5 — Heap Exploitation

```
gef➤ heap chunks            # find target chunk
gef➤ heap bins tcache       # verify free list state
# Trigger allocation
gef➤ heap chunks            # verify chunk header manipulation
```

## Comparison: GEF vs PEDA vs pwndbg

| Feature | GEF | PEDA | pwndbg |
|---------|-----|------|--------|
| Maintenance | Active (2024) | Abandoned | Active (2024) |
| Heap analysis | Excellent | Basic | Excellent |
| Color/UI | Excellent | Good | Excellent |
| pwntools integration | Good | Basic | Excellent (native) |
| Pattern tool | Built-in | Built-in | Built-in |
| ROPgadget | Built-in | Via `searchmem` | Via `ropper`/`rp++` |
| Format string | `format-string-helper` | None | None |
| Arm/MIPS support | Good | Poor | Good |
| Emulation (Unicorn) | Yes | No | Partial |
| Install complexity | Low (one-liner) | Low | Low |
| Best for | CTF/exploit dev | Legacy support | pwntools workflows |

**Recommendation:** Use GEF for standalone GDB sessions; pwndbg if using pwntools heavily (tighter integration); avoid PEDA (unmaintained).

## Troubleshooting

| Issue | Fix |
|-------|-----|
| GEF not loading | Check `~/.gdbinit` has `source ~/.gdbinit-gef.py`; run `gdb -q` |
| `ImportError` for heap | Run `pip install capstone`; verify Python 3 used by GDB |
| Pattern search fails | Use `pattern search $rip` for 32-bit; `$rsp` for 64-bit stack overflow |
| Heap bins empty | Heap not initialized yet — run until at least one `malloc` call |
| `checksec` shows wrong info | Binary may be stripped; run against unpacked version |
| ASLR enabled despite `aslr off` | Must be set inside GDB session, not globally; or use `echo 0 > /proc/sys/kernel/randomize_va_space` |
| pwntools `gdb.attach` not opening | Set `context.terminal`; verify tmux/terminal emulator is installed |
| Remote target connection fails | Ensure `gdbserver` is running: `gdbserver 0.0.0.0:4444 ./vuln` |
| Unicorn emulation errors | `pip install unicorn==1.0.3` — v2.x has breaking API changes |
| GEF slow on large heaps | Heap with many chunks is slow; use `heap chunks --all false` or filter by address |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
