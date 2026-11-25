---
name: zero-day-hunting
description: Zero-day vulnerability hunting — complete methodology from attack surface
  mapping through fuzzing, crash triage, root cause analysis, and PoC development
  to CVE submission. Covers AFL++, libFuzzer, syzkaller, AddressSanitizer, and WinDbg/GDB
  crash analysis.
version: 1.0.0
category: red-teaming
license: MIT
metadata:
  hermes_origin: import
tags:
- zero-day
- vulnerability-research
- fuzzing
- crash-analysis
- exploit-dev
- CVE
- AFL
- syzkaller
- ASAN
related_skills:
- security-orchestrator
- pentest-workflow
- reverse-engineering
- exploit-development
- binary-exploitation
- ctf-playbook
- hardware-iot-hacking
---

# Zero-Day Vulnerability Hunting — Complete Methodology

Zero-day hunting is the discipline of discovering previously unknown vulnerabilities in software, hardware, or firmware. It spans attack surface mapping, intelligent fuzzing, crash triage, root cause analysis (RCA), exploitability assessment, and responsible disclosure.

## Methodology Overview

```
1. TARGET SELECTION → 2. SURFACE MAPPING → 3. FUZZING → 4. CRASH TRIAGE → 5. ROOT CAUSE → 6. EXPLOITABILITY → 7. PoC → 8. DISCLOSURE
```

## 1. Target Selection

### Criteria for selecting targets

| Factor | High Value | Low Value |
|:-------|:-----------|:----------|
| Deployment scale | Global (Chrome, nginx, Linux kernel) | Niche internal tool |
| Privilege level | Kernel, SYSTEM, root | User-level sandboxed |
| Attack surface | Network-facing, parses untrusted input | Local-only, CLI tool |
| Existing audit | Never fuzzed, new code | Heavily audited, bounty-saturated |
| Patch gap | Vendor slow to patch | Rapid patch cycle |

### Target categories

```python
TARGET_CATEGORIES = {
    'browsers': 'Chrome, Firefox, Safari — renderer, JS engine, sandbox IPC',
    'kernels': 'Linux, Windows NT, XNU — syscalls, drivers, ioctl, netfilter',
    'parsers': 'Image (libpng/jpeg), archive (7z/zip), document (PDF/Office), media (ffmpeg)',
    'protocols': 'HTTP servers (nginx/Apache), DNS, DHCP, SMB, RDP, BLE, WiFi',
    'crypto': 'TLS implementations (OpenSSL), crypto libraries, JWT parsers',
    'containers': 'Docker, containerd, runc, Kubernetes API',
    'firmware': 'Router, IoT, UEFI, BMC, baseband — often unaudited',
    'cloud': 'AWS Lambda, Azure Functions, GCP Cloud Run — hypervisor breakout',
}
```

## 2. Attack Surface Mapping

### Identify every input vector

```python
def map_surface(binary_path: str) -> dict:
    """Map attack surface: every place the binary reads external input."""
    surface = {
        'network': [],      # ports, protocols
        'file_parsers': [], # file formats handled
        'syscalls': [],     # kernel: ioctl, syscall handlers
        'ipc': [],          # pipes, shared memory, D-Bus, COM
        'usb': [],          # USB descriptors, HID reports
        'cli_args': [],     # command-line argument parsing
        'env_vars': [],     # environment variable reads
        'config': [],       # config file parsing
        'api': [],          # REST/GraphQL/SOAP endpoints
    }
    # Tools: strings, objdump, Ghidra cross-references, strace/dtrace
    return surface
```

### Surface mapping tools

```bash
# Static: find all imported dangerous functions
objdump -T binary | grep -E 'recv|read|fread|scanf|gets|strcpy|sprintf|memcpy|mmap|ioctl'

# Dynamic: trace all syscalls with input
strace -f -e trace=read,write,recvfrom,recvmsg,ioctl ./binary input.txt 2>&1

# Kernel: find all exposed ioctls
grep -r 'unlocked_ioctl\|compat_ioctl' drivers/

# Network: D-Bus introspection
busctl introspect org.service.name /object/path

# Source code: grep for parser entry points
grep -rn 'open\|read\|parse\|deserialize\|decode\|unmarshal\|load' src/
```

## 3. Fuzzing — The Engine of Discovery

### Fuzzer Selection Guide

| Fuzzer | Best For | Type | Key Feature |
|:-------|:---------|:-----|:------------|
| **AFL++** | C/C++ programs, parsers | Mutation greybox | Custom mutators, cmplog, persistent mode |
| **libFuzzer** | Library APIs | Coverage-guided | In-process, fast, sanitizer integration |
| **syzkaller** | OS kernels | Coverage-guided syscall | Linux/Android/Darwin/Windows kernel fuzzing |
| **Honggfuzz** | C/C++, binaries | Mutation | HW-assisted coverage (Intel PT/BTS) |
| **oss-fuzz** | Open source projects | Continuous | Google infrastructure, 1000+ projects |
| **Fuzzilli** | JavaScript engines | Grammar-based | JS engine-specific intermediate language |
| **Domato** | Browser DOM | Grammar-based | HTML/CSS/JS DOM fuzzing |
| **FirmWire** | Baseband firmware | Emulation-based | Cellular baseband fuzzing |
| **Boofuzz** | Network protocols | Block-based | Protocol-aware, session tracking |

### AFL++ Setup & Usage

```bash
# Build target with AFL++ instrumentation
export CC=afl-clang-fast
export CXX=afl-clang-fast++
./configure --disable-shared
make -j$(nproc)

# Start fuzzing
afl-fuzz -i corpus/ -o output/ -m 1024 -- ./target @@

# Persistent mode (100x faster — instrument single function)
# Hook into the function that processes input:
__AFL_FUZZ_INIT();
unsigned char *buf = __AFL_FUZZ_TESTCASE_BUF;
while (__AFL_LOOP(10000)) {
    target_parse_function(buf, len);
}

# Parallel fuzzing
afl-fuzz -i corpus -o output -M master -- ./target @@
afl-fuzz -i corpus -o output -S slave1 -- ./target @@
afl-fuzz -i corpus -o output -S slave2 -p exploit -- ./target @@  # power schedule

# Minimize corpus + crashes
afl-cmin -i corpus -o corpus_min -- ./target @@
afl-tmin -i crash_file -o crash_min -- ./target @@

# CmpLog instrumentation (finds magic bytes/checksums)
export AFL_LLVM_CMPLOG=1
afl-clang-fast -o target target.c
```

### libFuzzer Usage

```cpp
// Fuzz target: fuzz_parser.cpp
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Call your target parser here
    parse_image(data, size);
    return 0;  // non-zero reserved for future use
}

// Compile
clang++ -g -fsanitize=fuzzer,address fuzz_parser.cpp -o fuzzer

// Run with corpus
./fuzzer corpus/ -jobs=8 -workers=8 -max_len=65536 -rss_limit_mb=4096
```

### syzkaller — Linux Kernel Fuzzing

```bash
# Setup syzkaller
git clone https://github.com/google/syzkaller
cd syzkaller; make

# Create VM image
# Debian/Ubuntu with custom kernel (KASAN + KCOV enabled)

# Kernel config requirements:
# CONFIG_KCOV=y, CONFIG_KASAN=y, CONFIG_KASAN_INLINE=y,
# CONFIG_DEBUG_INFO=y, CONFIG_CMDLINE_BOOL=y,
# CONFIG_CMDLINE="net.ifnames=0"

# Create syz-manager config
# Run: ./bin/syz-manager -config=my.cfg
```

### Writing Custom Syzkaller Descriptions

```
# Custom syscall description example
# File: my_driver.txt

openat$mydev(fd const[AT_FDCWD], file ptr[in, string["/dev/mydev"]], flags flags[open_flags], mode const[0]) fd_mydev

ioctl$MYDEV_CMD(fd fd_mydev, cmd const[MYDEV_IOCTL_MAGIC], arg ptr[in, MYDEV_ARGS])
ioctl$MYDEV_CMD_V2(fd fd_mydev, cmd const[MYDEV_IOCTL_MAGIC_V2], arg ptr[in, array[MYDEV_ARGS_V2, 0:16]])

MYDEV_ARGS {
    field1 int32[0:0xFFFF]
    field2 int32
    data ptr[in, array[int8, 1:1024]]
}

type fd_mydev fd[mydev]

resource fd_mydev[int32]: -1
```

## 4. Crash Triage

### Classification

```python
CRASH_TYPES = {
    'SEGV_ACCERR': 'Segfault on access — invalid pointer dereference → exploitable',
    'SEGV_MAPERR': 'Segfault on mapping — null/munmap\'d page → potentially exploitable',
    'SIGABRT': 'abort() → assertion/malloc corruption → symptom of memory corruption',
    'SIGBUS': 'Bus error — unaligned access → sometimes exploitable',
    'SIGILL': 'Illegal instruction → code corruption → possible RCE',
    'SIGFPE': 'Division by zero — rarely exploitable',
    'asan_heap_bof': 'ASAN heap buffer overflow → exploitable',
    'asan_heap_uaf': 'ASAN use-after-free → highly exploitable',
    'asan_stack_bof': 'ASAN stack buffer overflow → exploitable',
    'asan_global_bof': 'ASAN global buffer overflow → rarely exploitable',
    'ubsan_shift': 'UndefinedBehavior: shift out of bounds → logic bug',
    'ubsan_int_overflow': 'Signed integer overflow → logic bug, sometimes exploitable',
}
```

### !exploitable (Crash Analyzer)

```bash
# GDB crash analysis
gdb -batch -ex "run" -ex "bt" -ex "info registers" -ex "x/10i \$pc" \
    --args ./target crash_input

# !exploitable classification
# EXPLOITABLE: control of instruction pointer, write to arbitrary memory
# PROBABLY_EXPLOITABLE: corruption near sensitive data
# UNKNOWN: needs deeper analysis
# PROBABLY_NOT_EXPLOITABLE: null deref, assertion
```

### ASAN Crash Analysis

```bash
# ASAN output — key information:
# =================================================================
# ==12345==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x...
# READ of size 4 at 0x... thread T0
#     #0 0x... in vulnerable_func src/parser.c:42
#     #1 0x... in process_input src/main.c:128
# 0x... is located 0 bytes to the right of 64-byte region [...]
# allocated by thread T0 here:
#     #0 0x... in malloc
#     #1 0x... in allocate_buffer src/memory.c:24

# Summary: heap-buffer-overflow → 0 bytes past allocated buffer
# → off-by-one error in parser.c:42
# → allocated in memory.c:24 (64 bytes), overflowed by 1 byte
# → EXPLOITABLE: heap metadata corruption possible
```

## 5. Root Cause Analysis (RCA)

### Systematic RCA Workflow

```python
def rca_workflow(crash_input, binary):
    """Systematic root cause analysis."""
    steps = [
        "1. Minimize crash input (afl-tmin / delta debugging)",
        "2. Reproduce crash in debugger (GDB/WinDbg)",
        "3. Identify crashing instruction (PC/EIP/RIP)",
        "4. Trace data flow backward from crash point",
        "5. Find where attacker-controlled data enters",
        "6. Find where bounds checking should have occurred (missing check)",
        "7. Map the vulnerability class (UAF, heap/stack overflow, integer overflow)",
        "8. Identify constraints on attacker data (null bytes, charset limits)",
        "9. Document in advisory format",
    ]
    return steps
```

### RCA with GDB

```bash
# Reproduce crash under GDB
gdb --args ./target crash_input
(gdb) run
# Program received signal SIGSEGV, Segmentation fault.
(gdb) bt full          # full backtrace with locals
(gdb) info registers   # register state
(gdb) x/10i $rip-5     # disassemble around crash
(gdb) x/32gx $rsp-64   # examine stack
(gdb) frame 1          # go to caller
(gdb) info locals      # check variables
(gdb) p/x *ptr         # examine pointer

# Use rr (record and replay) for deterministic debugging
rr record ./target input
rr replay  # can step backward!

# Reverse execution in rr:
(gdb) reverse-step
(gdb) reverse-continue
(gdb) reverse-next 5
```

### RCA with WinDbg (Windows)

```
# Open crash dump
0:000> .ecxr  # switch to exception context
0:000> k      # stack trace
0:000> r      # registers
0:000> u .-10 L20  # disassemble around crash
0:000> dv     # local variables
0:000> dd @esp L40  # dump stack

# Application Verifier (enable heap checking)
appverif -enable Heaps Locks Handles Memory -for target.exe

# GFlags (page heap for UAF/heap overflow detection)
gflags /p /enable target.exe /full
```

### Linux Kernel RCA

```bash
# Kernel crash analysis
# 1. Enable KASAN + KCOV in kernel config
# 2. Reproduce with syzkaller reproducer
# 3. Analyze KASAN report:
#    - Which allocation? (slab/slub cache)
#    - Address relation to allocated object
#    - Call trace (who allocated it, who freed it, who used it after free)
# 4. Source code audit guided by traces
```

## 6. Exploitability Assessment

### Decision Framework

```python
EXPLOITABILITY_MATRIX = """
┌─────────────────────┬──────────┬─────────────┬────────────────┐
│ Vulnerability Type  │ Severity │ Exploit Diff│ Typical Result  │
├─────────────────────┼──────────┼─────────────┼────────────────┤
│ Use-After-Free      │ CRITICAL │ Hard        │ RCE / PrivEsc   │
│ Heap Overflow       │ CRITICAL │ Medium-Hard │ RCE / InfoLeak  │
│ Stack Buffer OF     │ CRITICAL │ Medium      │ RCE (ROP)       │
│ Format String       │ HIGH     │ Medium      │ RCE / InfoLeak  │
│ Integer Overflow    │ HIGH     │ Medium      │ Heap/Stack OF   │
│ Off-by-One          │ HIGH     │ Hard        │ Heap Corruption │
│ Null-Ptr Deref (w)  │ MEDIUM   │ Hard        │ PrivEsc (Linux) │
│ Info Leak           │ MEDIUM   │ Easy        │ Bypass ASLR/KASLR│
│ Uninit Memory       │ MEDIUM   │ Medium      │ InfoLeak/RCE    │
│ Race Condition      │ HIGH     │ Very Hard   │ PrivEsc/Logic   │
│ Type Confusion      │ HIGH     │ Medium      │ RCE/UAF         │
│ OOB Read            │ MEDIUM   │ Easy        │ InfoLeak        │
└─────────────────────┴──────────┴─────────────┴────────────────┘
"""
```

## 7. PoC Development

### PoC Template (Python/C)

```python
#!/usr/bin/env python3
"""
PoC for CVE-XXXX-YYYYY: Heap overflow in ExampleParser v1.2.3
Author: researcher
Date: 2026-07-15
Target: ExampleParser <= 1.2.3 (fixed in 1.2.4)
"""

import struct
import sys

def craft_exploit():
    """Craft input that triggers heap overflow."""
    # Header (8 bytes)
    header = b"EXPL" + struct.pack("<I", 0x100)  # magic + size

    # Body: 256 bytes + overflow (4 extra bytes for next chunk's size field)
    body = b"A" * 256  # fills allocated buffer (256 bytes)
    body += struct.pack("<I", 0xFFFFFFFF)  # overwrite next chunk size → crash

    return header + body

if __name__ == "__main__":
    payload = craft_exploit()
    print(f"[*] Payload size: {len(payload)} bytes")
    print(f"[*] Expected: heap corruption → crash in free()")

    # Write to file for reproduction
    with open("crash_input.bin", "wb") as f:
        f.write(payload)
    print("[+] Written to crash_input.bin")
    print("[+] Reproduce: ./ExampleParser crash_input.bin")
```

### CVE Report Template

```markdown
# CVE-XXXX-YYYYY Vulnerability Report

## Summary
- **Product**: ExampleParser v1.2.3
- **Vendor**: ExampleCorp
- **Vulnerability**: Heap buffer overflow in PNG chunk parsing
- **Severity**: CRITICAL (CVSS 9.8)
- **CWE**: CWE-122 — Heap-based Buffer Overflow
- **Discovered**: 2026-07-10

## Affected Versions
- ExampleParser 1.2.3 and earlier
- Fixed in 1.2.4

## Technical Details
The vulnerability exists in `png_parse_chunk()` in `src/png_parser.c:420`.
When parsing chunk length field, the function reads a 32-bit unsigned integer
from attacker-controlled input without validating it against the available
buffer size. This can cause a heap buffer overflow of up to 4 GB.

## Proof of Concept
Attached: poc.py / crash_input.bin

## Impact
Remote code execution when processing a malicious PNG file.
No user interaction required beyond opening the file.

## Remediation
Add bounds checking: if (chunk_len > remaining_buf_size) return ERROR;

## Timeline
- 2026-07-10: Discovered
- 2026-07-12: Vendor notified (security@examplecorp.com)
- 2026-07-14: Vendor confirmed, patch prepared
- 2026-07-15: Coordinated disclosure
```

## 8. Responsible Disclosure

### Disclosure Timeline

```
Day 0: Discover vulnerability → verify exploitability → prepare report
Day 1-3: Contact vendor security contact (security@, PSIRT, bug bounty)
Day 3-14: Vendor acknowledgment expected
Day 14-30: Vendor prepares patch
Day 30-90: Coordinated disclosure (CVE assigned, advisory published)
Day 90: If vendor unresponsive → CERT/CC coordination → public disclosure
```

### Disclosure Venues

| Venue | Type | When |
|:------|:-----|:-----|
| Vendor Security Contact | Private | First contact (Day 1-3) |
| CERT/CC (cert.org) | Assisted | If vendor unresponsive after 14-30 days |
| CVE Program (cve.org) | CVE assignment | Near disclosure date |
| Full Disclosure Mailing List | Public | After patch or deadlock |
| oss-security | Public | Open source vulns |
| Conference (BlackHat, DEF CON) | Presentation | After disclosure + patch |

### Bug Bounty Programs

```
Top bounty platforms:
- HackerOne (hackerone.com): Internet Bug Bounty (Chrome: $250k+ full chain)
- Bugcrowd (bugcrowd.com): Enterprise programs
- ZDI (zerodayinitiative.com): TippingPoint — buys vulns for defensive use
- Google VRP (bughunters.google.com): Android, Chrome, Google services
- Apple Security Bounty: max $2M for zero-click iOS kernel
- Microsoft MSRC: Azure, Windows, Office
```

## Tools Ecosystem

### Essential Zero-Day Hunting Toolkit

```bash
# Static Analysis
- Ghidra (NSA)          # decompilation, scripting, headless
- IDA Pro/Free          # deep interactive analysis
- Binary Ninja          # modern RE, excellent Python API
- radare2/rizin         # quick CLI triage, CTF
- CodeQL (GitHub)       # semantic code analysis, variant analysis

# Dynamic Analysis
- GDB + pwndbg/peda/gef # Linux debugging
- WinDbg + Preview      # Windows debugging
- x64dbg                # Windows user-mode debugger
- rr                    # deterministic record-and-replay
- strace / ltrace       # syscall / library call tracing
- ProcMon / Process Explorer  # Windows monitoring

# Fuzzing
- AFL++                 # mutation-based greybox (C/C++)
- libFuzzer             # in-process coverage-guided
- syzkaller             # kernel fuzzing (major OS kernels)
- Honggfuzz             # HW-assisted coverage
- Fuzzilli              # JS engine fuzzing
- Domato                # DOM fuzzer (browser)
- Boofuzz               # network protocol fuzzing
- Peach Fuzzer          # commercial, protocol-aware

# Sanitizers (compile with target)
- AddressSanitizer (ASAN)     # memory errors: OOB, UAF, double-free
- MemorySanitizer (MSAN)      # uninitialized memory
- UndefinedBehaviorSanitizer (UBSAN)  # integer overflow, shift, null
- ThreadSanitizer (TSAN)      # data races
- LeakSanitizer (LSAN)        # memory leaks

# Crash Analysis
- !exploitable / crash_analyzer  # GDB plugin
- CASR (crasher)                 # Apple crash analysis
- ClusterFuzz                     # Google crash clustering

# Symbolic Execution
- angr              # Python symbolic execution engine
- Triton            # dynamic binary analysis + symbolic execution
- Manticore         # symbolic execution with EVM support
- KLEE              # LLVM-based symbolic execution

# Exploit Development
- pwntools          # Python exploit dev framework
- ROPgadget         # ROP gadget finder
- one_gadget        # libc execve gadget finder
- libc-database     # libc version identification
```

## Training & Learning Resources

### Courses

| Course | Provider | Focus | Cost |
|:-------|:---------|:------|:-----|
| TGVRED (The Gate of VR & Exploit Dev) | ZeroDay Academy | Full VR lifecycle | Paid |
| OSED (Windows Exploit Dev) | OffSec | Windows userland | $1,500+ |
| OSCE³ (Advanced Exploit Dev) | OffSec | Windows + macOS exploitation | $1,500+ |
| AWE (Advanced Windows Exploitation) | OffSec | Windows kernel | $ — currently paused |
| Linux Kernel Exploitation | various | Linux kernel | varies |

### Key GitHub Repositories

```
- https://github.com/googleprojectzero (Project Zero research)
- https://github.com/google/oss-fuzz (continuous fuzzing)
- https://github.com/0vercl0k/rp (ROP gadget finder)
- https://github.com/jonathansalwan/Triton (dynamic binary analysis)
- https://github.com/angr/angr (symbolic execution)
- https://github.com/Gallopsled/pwntools (exploit dev)
- https://github.com/AFLplusplus/AFLplusplus (AFL++ fuzzer)
- https://github.com/google/syzkaller (kernel fuzzer)
- https://github.com/nickelpro/fuzzilli (JS fuzzer)
- https://github.com/googleprojectzero/fuzzilli (ProjectZero fork)
```

### Blogs & Researchers

```
- Project Zero blog (googleprojectzero.blogspot.com)
- Connor McGarr (connormcgarr.github.io) — Windows browser exploitation
- LiveOverflow (liveoverflow.com) — CTF + exploit methodology
- Zero Day Engineering (zerodayengineering.com)
- S3cur3Th1sSh1t (s3cur3th1ssh1t.github.io) — EDR/AV bypass
- Bishop Fox (bishopfox.com/blog) — Red team tools
- SpecterOps (posts.specterops.io) — AD security
```

## Deep Knowledge References

- **references/zero-day-research-methodology.md** — Complete zero-day research methodology (1881 lines) covering AFL++/libFuzzer/syzkaller fuzzing, crash triage with AddressSanitizer/WinDbg, root cause analysis via BinDiff/Ghidra/angr, exploit development with pwntools/ROPgadget/one_gadget, and kernel exploit techniques (modprobe_path, cred overwrite, eBPF).

## Pitfalls

- **Fuzzing without sanitizers**: You'll miss many bugs. Always compile with ASAN/UBSAN.
- **Crash ≠ exploitable**: Many crashes are null-derefs or safely handled OOB reads. Triage carefully.
- **Under-powering fuzzers**: Allocate enough cores and RAM. Fuzzing is compute-intensive.
- **Shallow corpus**: Without a good seed corpus, fuzzers never reach deep code paths.
- **Ignoring fuzzer feedback**: If coverage plateaus, write custom mutators or grammar fuzzers.
- **Kernel fuzzing needs VM snapshots**: Fuzzing corrupts state; use VM snapshots for reset.
- **Legal authorization**: Never fuzz software you don't own or have permission to test.
- **Vendor responsiveness varies**: Google: days, Microsoft: weeks, some IoT vendors: never.
- **Disclose responsibly**: Give vendors 90 days minimum; CERT/CC can help for unresponsive vendors.
- **Patching rate**: Some vendors ship incomplete fixes — verify the patch actually fixes the bug.
- **Variant analysis**: After finding one bug, look for the same pattern in related code (CodeQL).