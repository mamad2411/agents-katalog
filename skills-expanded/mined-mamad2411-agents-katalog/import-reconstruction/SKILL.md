---
name: import-reconstruction
description: >
  IAT (Import Address Table) reconstruction for packed, obfuscated, or manually-mapped PE files
  that have destroyed or hidden their imports. Covers API hashing identification, dynamic
  import logging, pe-sieve IAT dump, and Scylla fix-imports workflow.
targets: [deobfuscator, static_analyst]
---

# Import Reconstruction Skill

## Why Imports Are Destroyed

Packers and loaders destroy the IAT to:
1. Prevent static analysis from seeing which APIs are used
2. Replace `GetProcAddress` with an internal resolver
3. Map PE manually (VirtualAlloc + custom loader) bypassing OS loader

After unpacking, the dumped PE will show:
- IAT full of zeros or junk (original table overwritten)
- A small import stub table with just `LoadLibraryA` + `GetProcAddress`
- Fabricated thunk functions that call a resolver

---

## Step 1 — Identify API Hashing Routine

Most packers use a hash of the API name to look it up in `ntdll.dll` exports.

### Common Hash Algorithms

| Name | Constant / Pattern | Used By |
|---|---|---|
| ROR13 | `ror eax, 0xD` in loop | Metasploit stagers, many shellcode |
| djb2 | `hash = hash * 33 + c` (multiply by 0x21) | Custom implementations |
| FNV-1a | `hash = hash ^ c; hash *= 0x01000193` (32-bit prime) | Various |
| imm32 inline | No loop, direct `cmp eax, 0xDEADBEEF` | Simple obfuscators |
| CRC32 | Polynomial-based loop | Less common |

### ROR13 Pattern in Assembly
```asm
; hash_api:
xor edi, edi        ; hash = 0
xor esi, esi
.next_char:
  lodsb             ; AL = next byte of function name
  test al, al
  jz .done
  ror edi, 0xD      ; rotate right 13 bits
  add edi, eax      ; add character
  jmp .next_char
.done:
  ret               ; EDI = hash
```

### Detection: Search for the rotation constant
```
# radare2: search for ROR with 0xD
/x c1c80d          # ror eax, 0x0d
/x c1cf0d          # ror edi, 0x0d

# capa will identify "api hashing" capability automatically
capa unpacked_sample.exe
```

### djb2 Pattern
```asm
; multiply by 0x21 (33)
mov eax, 0x1505    ; initial hash seed for djb2
; loop: eax = eax * 33 + byte
; look for imul with 0x21 or shift-add: (hash << 5) + hash + c
```

---

## Step 2 — Log Dynamic API Resolution

When the binary resolves APIs at runtime via GetProcAddress or custom resolver:

### Method A: Frida GetProcAddress hook
```javascript
const GetProcAddress = Module.getExportByName('kernel32.dll', 'GetProcAddress');
Interceptor.attach(GetProcAddress, {
  onEnter(args) {
    const modHandle = args[0];
    const procName = args[1];
    // ordinal import: (procName & 0xFFFF0000) == 0
    if (procName.toUInt32() > 0xFFFF) {
      console.log(`GetProcAddress: ${procName.readUtf8String()}`);
    } else {
      console.log(`GetProcAddress ordinal: ${procName.toUInt32()}`);
    }
  },
  onLeave(retval) {
    console.log(`  -> 0x${retval.toString(16)}`);
  }
});
```

### Method B: x64dbg breakpoint script
```
// Set BP on GetProcAddress, log args:
bp GetProcAddress
bpcnd GetProcAddress, "1"
// In conditional log: "{r:rcx} {r:rdx} [rdx]"
```

### Method C: API Monitor / Process Monitor
Record all WinAPI calls — look for `GetProcAddress` return values mapped to known APIs.

---

## Step 3 — pe-sieve IAT Dump

pe-sieve scans a running process and identifies modified/suspicious PE sections.

### Usage
```bash
# Scan process (PID 1234), dump suspicious modules
pe-sieve.exe /pid 1234 /dump 3 /iat 1

# Flags:
#   /dump 3 = dump all PE modules
#   /iat 1 = scan and report IAT anomalies
#   /hooks = detect hooked functions too
```

### Output
```
[!] Module: 0x140000000 malware.exe
    IAT scan: 23 entries invalid (zeros), 5 suspect thunks
    Dumped to: process_1234\dump_malware.exe
```

### Interpret Results
- **Zeros in IAT**: Not yet resolved (pre-unpacking dump) — wait for OEP
- **Thunk pointing to allocated memory**: Runtime-resolved function — log with Frida
- **IAT entries pointing to middle of function**: IAT hooks (AV/EDR or malware hooking)

---

## Step 4 — Scylla Fix Imports

After obtaining a valid unpacked dump (post-OEP), use **Scylla** (x64dbg plugin or standalone) to rebuild the IAT.

### Workflow in x64dbg + Scylla
1. Let the packer unpack (run to OEP — see packer-unpacking skill)
2. In x64dbg: pause at OEP
3. Open Scylla (Plugins → Scylla)
4. **IAT Autosearch** → Scylla auto-detects IAT VA and size
5. **Get Imports** → resolves all thunks visible in IAT
6. Review: unresolved entries shown in red
   - Right-click unresolved → "Is Valid?" to check address
   - "Trace invalid imports" → attempt deeper resolution
   - Manually fix remaining entry (if you know which API it points to)
7. **Fix Dump** → select the dump file from pe-sieve output
8. Scylla rewrites the IAT and saves a `_SCY.exe` fixed file
9. Open fixed file in Ghidra / IDA → imports now visible

### Common Issues

| Problem | Fix |
|---|---|
| Many red (invalid) entries | Binary may still be partially unpacked; dump later |
| Entries resolving to wrong DLL | pe-sieve dump captured wrong memory snapshot |
| Fix Dump fails | Use "Rebuild IAT" instead; manually set IAT offset |
| All imports from single DLL | Loader-stub may forward all calls through single trampoline |

---

## Alternative: Hollow Process / Manual Map

When the binary creates a new process and injects (process hollowing):

1. Use process monitors to detect `NtUnmapViewOfSection` + `WriteProcessMemory` + `SetThreadContext`
2. Attach debugger to the **child** process after injection
3. pe-sieve scan the child PID (not parent)
4. Dump + Scylla on child's memory

---

## Quick Reference: API Hash Lookup

Pre-computed hash databases exist for common functions:

### ROR13 table lookup (Python)
```python
import struct, ctypes
def ror13(s: str) -> int:
    h = 0
    for c in (s + '\x00'):
        h = ctypes.c_uint32(((h >> 13) | (h << 19)) + ord(c)).value
    return h

# Common values:
# LoadLibraryA = 0xEC0E4E8E
# GetProcAddress = 0x7C0DFCAA
# VirtualAlloc = 0x91AFCA54
# WinExec = 0x98FE8A0E
# CreateProcessA = 0x16B3FE72
```

Online tools: `apihash.dkhuber.org` (offline tool), VirusTotal YARA rules with API hash constants.

---

## Evidence Required Before Claiming Reconstruction

- Show actual log of `GetProcAddress` calls with function names (if dynamic logging used)
- Show Scylla "Get Imports" screenshot or report listing resolved functions
- Confirm: dumped binary opens in Ghidra/IDA with imports visible in import table
- State which hash algorithm was identified and how (constant found, or FLOSS output, or capa rule match)
