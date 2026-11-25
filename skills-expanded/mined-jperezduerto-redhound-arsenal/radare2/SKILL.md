---
name: radare2
description: >
  Operate radare2 (r2) — an open source reverse engineering framework and binary analysis
  toolkit. Use when disassembling, debugging, or patching binaries, when the user asks about
  static analysis, dynamic analysis, ROP gadget hunting, shellcode analysis, binary diffing,
  CTF reversing challenges, or malware analysis. Covers r2 CLI, analysis commands, visual/graph
  mode, scripting with r2pipe, Cutter GUI, r2pm plugin manager, and integration workflows
  with Ghidra and GDB.
license: LGPL-3.0
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/radareorg/radare2
---

# radare2 Agent Skill

## When to Use This Skill

Use this skill when:
- Performing static analysis or dynamic debugging of binaries (ELF, PE, Mach-O, raw shellcode)
- CTF reversing challenges requiring disassembly, patching, or flag extraction
- Hunting ROP gadgets for exploit development
- Analyzing malware samples offline
- Diffing two binaries to identify patched functions
- Scripting binary analysis workflows with Python via r2pipe

## What radare2 Does

radare2 is a portable, scriptable reverse engineering framework built around a hex editor
core. It provides disassembly (supporting 70+ architectures), a built-in debugger, code
analysis, binary patching, and a UNIX-philosophy command language where every operation is
composable. It is free, runs on all major platforms, and is the primary open-source
alternative to IDA Pro and Binary Ninja for professional reverse engineering work.

## Installation

```bash
# Kali / Debian
sudo apt install radare2

# Build from source (latest features)
git clone https://github.com/radareorg/radare2
cd radare2 && sys/install.sh

# macOS
brew install radare2

# Windows (via scoop)
scoop install radare2

# Verify install
r2 -v

# Cutter GUI (official Qt-based frontend)
# Download AppImage from https://github.com/rizinorg/cutter/releases
chmod +x Cutter-*.AppImage && ./Cutter-*.AppImage
```

### r2pm — Plugin Manager

```bash
r2pm update          # update package index
r2pm install r2dec   # decompiler plugin
r2pm install r2ghidra  # Ghidra decompiler backend (pdg command)
r2pm install iaito   # alternative GUI
r2pm list            # list installed plugins
```

## Core Concepts

### Opening Binaries

```bash
r2 binary              # open for analysis (no exec)
r2 -d binary           # open in debugger (spawn process)
r2 -d -p pid           # attach to running PID
r2 -w binary           # open in write mode (for patching)
r2 -A binary           # open and auto-analyze (runs aaa)
r2 -q -c 'cmd' binary  # run command non-interactively, quit
r2 -n binary           # do NOT load symbols/sections (raw mode)
r2 malloc://512        # open empty 512-byte buffer in memory
```

### Command Grammar

Radare2's command language follows a consistent grammar:
- Command + subcommand character: `aa` (analyze all), `afl` (analyze functions list)
- `?` suffix = help: `a?`, `p?`, `s?`
- `~` = internal grep: `afl~main`, `pd 20~call`
- `@@` = iterate over: `pd 5 @@ fcn.*` (disassemble at each function)
- `>` / `>>` = redirect to file: `afl > functions.txt`
- `;` = command chaining: `s main; pdf`
- `|` = pipe to shell: `afl | wc -l`

## CLI Reference

### Navigation (Seeking)

```bash
s 0x401000      # seek to address
s main          # seek to symbol
s+10            # seek forward 10 bytes
s-10            # seek backward 10 bytes
s?              # list seek history
sr rip          # seek to register value (debug mode)
```

### Printing / Disassembly

```bash
pd 20           # disassemble 20 instructions at current offset
pdf             # disassemble entire current function (print disasm function)
pdc             # pseudo-C decompilation (r2dec plugin)
pdg             # Ghidra decompiler output (r2ghidra plugin)
px 64           # hex dump 64 bytes
pxw 32          # hex dump as 32-bit words
ps @ 0x402010   # print string at address
pf i            # print format: integer at cursor
p8 16           # print 16 bytes as raw hex string
```

### Analysis Commands

```bash
aa              # analyze all (basic: functions, calls, strings)
aaa             # deeper analysis (includes xrefs, types, vtables)
aaaa            # even deeper (slow on large binaries)
afl             # list all functions
afl~sym         # grep function list for 'sym'
afn newname     # rename current function
afv             # list function variables
afx             # list function cross-references
axt 0x401000    # show references TO address (xref to)
axf 0x401000    # show references FROM address (xref from)
iz              # list strings in data sections
izz             # list ALL strings in binary
iI              # binary info (arch, bits, endian, compiler)
il              # list libraries
ii              # list imports
ie              # list exports
is              # list symbols
iS              # list sections
```

### Visual Mode

```bash
V               # enter visual mode (hex view)
p               # cycle through view modes (hex, disasm, esil, etc.)
V!              # block-based ASCII graph (jump to VV)
VV              # control flow graph of current function
```

**Visual mode keys:**
```
arrows / hjkl   navigate
Enter           follow call/jump
u               undo navigation
:               enter command
/               search
q               quit visual mode
F               set/unset function at cursor
c               cursor mode (select bytes)
d               define flag/data
n               rename symbol at cursor
```

### Graph Mode (VV)

```bash
VV              # CFG of current function
# Inside graph:
hjkl / arrows   pan
+/-             zoom in/out
g               go to (enter address)
q               quit
.               center on current offset
t/f             follow true/false branch
```

```bash
# Non-interactive graph export
r2 -q -c 'aaa; agf @ main' binary          # ASCII graph to stdout
r2 -q -c 'aaa; agfd @ main' binary         # dot format for Graphviz
r2 -q -c 'aaa; agfd @ main' binary | dot -Tpng -o graph.png
```

### Debugging (-d mode)

```bash
r2 -d ./vuln_binary arg1     # spawn in debugger

# Inside r2 debug session:
db 0x401234      # set breakpoint at address
db sym.main      # breakpoint at symbol
dbl              # list breakpoints
dbc 0x401234 'dc'  # conditional: run 'dc' when hit
dc               # continue execution
ds               # step into (single step)
dso              # step over
dsu 0x401500     # step until address
dr               # show all registers
dr rip           # show single register
dr rax=0x41      # set register
dm               # memory maps
dmp 0x1000 rwx   # change memory permissions
dbt              # backtrace
dk 9             # send signal 9 (SIGKILL)
```

### Patching (open with -w)

```bash
r2 -w binary
# Seek to target address, then:
wa nop           # write NOP instruction
wa jmp 0x401200  # write jump
wx 9090          # write raw bytes (NOPs)
wv4 0xdeadbeef   # write 4-byte value
wf patch.bin @ 0x401000   # write file contents at address

# Save changes
r2 -w -c 'wa nop @ 0x401234; wa nop @ 0x401235' binary
```

### Flags (Labels)

```bash
f                # list all flags
f myvar @ 0x601020    # create flag at address
f- myvar              # remove flag
fr myvar newvar       # rename flag
fs imports       # switch to flag space 'imports'
fs *             # list flag spaces
```

### Searching

```bash
/ password       # search for string
/x deadbeef      # search for hex bytes
/a jmp rax       # search for assembly instruction
/R pop rdi       # find ROP gadgets containing 'pop rdi'
/R/q pop rdi     # quiet ROP search (addresses only)
```

## ROP Gadget Hunting

```bash
# Built-in ROP search
r2 binary
[0x00400000]> /R pop rdi
# Shows gadget addresses and instruction sequences

# More powerful: use ROPgadget alongside r2
ROPgadget --binary binary --rop --thumb > gadgets.txt

# r2 approach for full gadget list
r2 -q -c '/R/ ret' binary | head -50    # all gadgets ending in ret

# Find syscall gadgets
/R syscall
/R int 0x80
```

## Shellcode Analysis

```bash
# Analyze raw shellcode blob
r2 -b 32 -m 0x1000 shellcode.bin    # 32-bit, load at 0x1000
r2 -b 64 -m 0x1000 shellcode.bin    # 64-bit

# Alternatively from hex string
rasm2 -d 'e8000000005b81eb07104000...'  # disassemble hex

# Inside r2 for shellcode:
pd 50           # disassemble first 50 instructions
pdc             # decompile to pseudo-C
V               # visual/graph mode
```

## Binary Diffing

```bash
# radiff2 — binary diff tool (included with r2)
radiff2 binary_v1 binary_v2       # byte-level diff
radiff2 -s binary_v1 binary_v2   # similarity analysis
radiff2 -g main binary_v1 binary_v2  # graph diff of function 'main'
radiff2 -C binary_v1 binary_v2   # diff code (disassembly level)

# Function-level diff in r2:
r2 -AA binary_v1
[0x...]> r2 binary_v2   # open second binary in r2 session
[0x...]> afd            # diff functions
```

## Scripting with r2pipe (Python)

```bash
pip install r2pipe
```

```python
import r2pipe

# Open binary (non-interactive)
r2 = r2pipe.open('./binary')
r2.cmd('aaa')                     # analyze

# Get function list as JSON
funcs = r2.cmdj('aflj')           # 'j' suffix = JSON output
for f in funcs:
    print(f['name'], hex(f['offset']))

# Disassemble main
r2.cmd('s main')
disasm = r2.cmdj('pdfj')          # disassemble function as JSON
for op in disasm['ops']:
    print(hex(op['offset']), op.get('disasm',''))

# Find all strings
strings = r2.cmdj('izzj')
for s in strings:
    print(s['vaddr'], s['string'])

# Patch and save
r2 = r2pipe.open('./binary', flags=['-w'])
r2.cmd('s 0x401234')
r2.cmd('wa nop')

r2.quit()
```

### Batch analysis script

```python
import r2pipe, json, sys

def analyze_binary(path):
    r2 = r2pipe.open(path, flags=['-2'])  # suppress stderr
    r2.cmd('aaa')
    info = r2.cmdj('iIj')
    functions = r2.cmdj('aflj') or []
    imports = r2.cmdj('iij') or []
    strings = r2.cmdj('izzj') or []
    r2.quit()
    return {
        'info': info,
        'function_count': len(functions),
        'imports': [i['name'] for i in imports],
        'strings': [s['string'] for s in strings if len(s['string']) > 5]
    }

print(json.dumps(analyze_binary(sys.argv[1]), indent=2))
```

## Common Workflows

### CTF RE Challenge Workflow

```bash
# 1. Identify binary
file challenge
checksec --file=challenge   # NX, PIE, RELRO, stack canary
r2 -A challenge             # auto-analyze

# 2. Find interesting functions
[0x...]> afl~sym.           # list non-imported functions
[0x...]> iz~flag            # search strings for 'flag'

# 3. Examine main logic
[0x...]> s main; pdf        # disassemble main
[0x...]> VV                 # graph mode

# 4. Trace execution path
[0x...]> r2 -d challenge
[0x...]> db sym.check_password
[0x...]> dc
```

### Malware Static Analysis

```bash
r2 -A malware.exe
# Check imports for suspicious APIs
ii~Virtual         # VirtualAlloc, VirtualProtect
ii~Crypt           # crypto APIs
ii~WSA             # winsock
iz~http            # hardcoded URLs
iz~cmd             # shell commands
# Examine suspicious functions
afl~sub_ | head    # unnamed functions = likely unpacked code
```

### Exploit Development — Buffer Overflow

```bash
# Find vulnerable function
r2 -d vuln
[0x...]> aaa; afl~vuln
[0x...]> s sym.vuln_func; pdf

# Find ROP gadgets
[0x...]> /R pop rdi; ret
[0x...]> /R pop rsi; ret
[0x...]> /R pop rdx; ret

# Check ASLR / PIE
[0x...]> iI~pic      # Position Independent Code?
[0x...]> dm          # memory map — check base addresses
```

## Integration with Other Tools

### Ghidra comparison workflow

```bash
# Use r2ghidra for Ghidra decompiler inside r2
r2pm install r2ghidra
r2 -A binary
[0x...]> s main; pdg     # Ghidra decompile in r2 terminal

# Export r2 analysis to Ghidra project
r2 -q -c 'aaa; aflj' binary > r2_functions.json
# Import into Ghidra with r2ghidra bridge plugin
```

### GDB integration

```bash
# Start binary under r2 debugger, attach GDB for extensions
r2 -d ./binary
[0x...]> =!gdb    # launch GDB attached to same process (experimental)

# Or use r2 alongside GDB with pwndbg/gef
gdb ./binary
(gdb) target remote :1234    # if r2 started with r2 -d -w binary
```

### pwntools + r2pipe

```python
from pwn import *
import r2pipe

r2 = r2pipe.open('./pwn_chall')
r2.cmd('aaa')

# Get binary base for offset calculations
elf = ELF('./pwn_chall')
main_offset = r2.cmdj('aflj')[0]['offset']

# Build ROP chain using r2 gadgets + pwntools
gadgets = r2.cmd('/R pop rdi; ret').strip().split('\n')
pop_rdi = int(gadgets[0].split()[0], 16)
```

## Troubleshooting

**`aaa` hangs on large binary**
```bash
# Use lighter analysis first
r2 binary
[0x...]> aa      # basic analysis only
[0x...]> af @ main   # analyze specific function
# Or limit with: r2 -e anal.timeout=30 binary
```

**`pdf` shows `[invalid]` instructions**
```bash
# Wrong architecture or bitness
[0x...]> e asm.arch=x86
[0x...]> e asm.bits=32
r2 -b 32 binary    # set bitness at open
```

**Symbols stripped, no function names**
```bash
# r2 can still auto-detect functions
[0x...]> aab    # analyze basic blocks
[0x...]> afl    # lists functions as fcn.XXXXXXXX
# Use FLIRT signatures for library function detection
r2pm install sigdb
[0x...]> zfs /path/to/sig.sig   # apply FLIRT sigs
```

**Visual mode rendering issues (tmux)**
```bash
# Set terminal size explicitly
export COLUMNS=220 LINES=50
r2 binary
# Or use Cutter GUI to avoid terminal rendering issues
```

**r2pipe connection refused**
```python
# Ensure r2 binary is in PATH
import subprocess, r2pipe
subprocess.run(['which', 'r2'])   # verify installation
r2 = r2pipe.open('/absolute/path/to/binary')
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
