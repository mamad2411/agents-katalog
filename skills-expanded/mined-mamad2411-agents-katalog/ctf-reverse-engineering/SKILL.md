---
name: ctf-reverse-engineering
description: Solve CTF Reverse Engineering challenges involving binaries, APKs, bytecode,
  firmware, obfuscated scripts, crackmes, license checks, and custom VMs. Use when
  a CTF challenge gives an executable, shared library, APK/JAR/class, wasm, firmware
  blob, or obfuscated program to analyze.
version: 1.0.0
license: MIT
metadata:
  hermes_origin: import
tags:
- ctf
- reverse-engineering
- binary
- crackme
- ghidra
- angr
- apk
- wasm
related_skills: []
---

# CTF Reverse Engineering

## First Workflow

1. Preserve artifact and compute hash.
2. Identify format/arch/packing: ELF/PE/Mach-O/APK/JAR/WASM/Python/.NET.
3. Run low-cost static checks: `file`, `strings`, imports, sections, symbols.
4. Determine execution safety. Prefer offline/static; sandbox unknown binaries.
5. Locate flag checks: compare functions, crypto routines, input validation, suspicious constants.
6. Choose path: static solve, dynamic debug, symbolic execution, decompile, patch, or emulate.
7. Script key extraction/constraint solving reproducibly.

## Attack Families

- Straight strings or encoded constants.
- XOR/add/rotate obfuscation.
- Serial/license checks and constraint solving.
- Anti-debug/anti-VM/time checks.
- Packed binaries and self-modifying code.
- Custom VM bytecode.
- Native crypto verification with hardcoded keys.
- Unity Mono / C# games: inspect `*_Data/Managed/Assembly-CSharp.dll`, dump `#US` user strings, identify gameplay/API classes, then disassemble/decompile coroutine state machines such as `<RollCoroutine>d__N.MoveNext`.
- Android APK reverse: Java/Kotlin, native libs, resources, manifest.
- Python bytecode, JS obfuscation, Lua, .NET, Java class/JAR.
- WASM reverse and browser glue code.
- SageMath / Cython whole-program binaries: flagged by a tiny `.rodata` (often <100 bytes — just `Correct!`/`Fail...`/`Input flag:`/prefix), libc-only PLT imports with NO `libgmp`/`libpython`/`libntl`, and the build path leak `~/miniconda3/envs/sage/lib` in `.dynstr`. The entire GMP/NTL/Sage rings are statically inlined into `.text` (multi-MB). Bignum constants are NOT stored as decimal strings — `strings` finds zero long-number literals. All arithmetic dispatches through indirect `callq *%rcx`/`*%rdx` against per-type descriptor tables (vtable-like). Each element type has a 2-quad descriptor `[vtable_ptr, value_ptr]`; operations sign-test `%rax` after each call (`jns`/`js`) to drive a Sage `try/except` state machine whose success branch calls `puts("Correct!"); exit(0)` and fail branch calls `puts("Fail..."); exit(1)` via registered callback pointers. See `references/sagemath-inline-bignum-pattern.md` for the dispatch reconstruction and the only viable attack shape (symbolic execution on real x86-64 Linux — NOT macOS arm64).

## Unity Mono CTF Workflow

1. Extract the game archive and locate `*_Data/Managed/Assembly-CSharp.dll`.
2. Dump user strings before opening heavyweight tools; challenge endpoints and JSON fragments often live in the `#US` heap. With `dnfile`, prefer `dn.net.user_strings.get(offset).value`; `value_bytes` is a method in some versions, not a bytes property.
3. If ILSpy GUI/cask is awkward on macOS, install/use `dotnetfile` as a lightweight fallback:
   `python3 -m pip install --user dotnetfile` then `~/Library/Python/3.9/bin/dotnetfile_disassemble Assembly-CSharp.dll > disasm.txt`.
4. For Unity web/API mechanics, search disassembly for `UnityWebRequest`, `UploadHandlerRaw`, `DownloadHandlerBuffer`, `SetRequestHeader`, `POST`, `Content-Type`, URL strings, and coroutine state-machine `MoveNext` methods.
5. Reconstruct JSON bodies from adjacent `ldstr` + `String.Format` fragments, then probe the endpoint conservatively. If the endpoint resolves to private/routed CTF infrastructure and times out, continue extracting local fallback logic and document the exact request shape rather than guessing a flag.
6. For API probing after Unity reversing, do not batch many paths/payloads behind one long timeout: first send one short-timeout request to `/` using the exact recovered method/body/header, then expand paths or fuzz fields only after observing status codes. Long all-path loops can consume the session budget without a useful response.

## Unity Mono / Assembly-CSharp workflow

1. Unzip nested challenge archives into a scratch directory and identify the Unity layout (`<Game>.exe`, `<Game>_Data/Managed/Assembly-CSharp.dll`, `StreamingAssets/`).
2. Search `Assembly-CSharp.dll` first, not Unity engine DLLs. Extract `#Strings` metadata for type/method names and `#US` user strings for UI text, endpoints, JSON templates, rarity names, and flag-like strings.
3. Treat URL strings and gameplay/server class names as first-class clues. A Unity CTF may put the flag behind a remote endpoint used by the game (for example a gacha/roll API) rather than inside assets.
4. Enumerate relevant types and methods with `dnfile` when ILSpy/mono tools are unavailable. Use `.row` on `MDTableIndex` entries (`method_index.row.Name`, `field_index.row.Name`). For `dnfile` `UserString`, prefer `.value`; `value_bytes` is a method in some versions, so do not slice it as a bytes property.
5. Decompile or disassemble coroutine state machines (`<MethodName>d__N.MoveNext`) as well as the parent method. Unity HTTP/gameplay logic often lives in the generated `MoveNext`, while the parent method only constructs the enumerator.
6. Once an endpoint/body template is recovered, switch from static reversing to deterministic API probing: verify path, method, JSON body, and response schema; then automate the request that triggers the challenge condition.

## Nuitka onefile CTF workflow

Use this when a Linux ELF / packed Python challenge shows Nuitka markers such as `NUITKA_ONEFILE_PARENT`, `NUITKA_ONEFILE_DIRECTORY`, `NUITKA_ORIGINAL_ARGV0`, `{TEMP}/onefile_{PID}_{TIME}`, or `nuitka_module_loader`.

1. Do not stop at normal ELF strings; first determine whether the file is a Nuitka onefile outer stub.
2. Check EOF metadata. Some Nuitka onefile builds end with an 8-byte little-endian payload size; subtract it from EOF to locate the compressed payload.
3. If the payload starts with zstd magic `28 b5 2f fd` and one-shot decompression complains about missing content size, use streaming zstd decompression.
4. The decompressed blob can be a table of records: `filename\0`, one flag byte, 8-byte little-endian size, then file data. Extract each record and inspect the inner `app.bin` / shared objects.
5. For Nuitka-compiled Python, user source may not be present as `.pyc`, but symbols/constants often survive in `.data` string pools. Search around `app.py`, `__main__`, function/class names, UI strings, filenames, and challenge-specific constants to reconstruct source-level structure.
6. For crypto/reversing hybrids, extract function names and constants first (`derive_*`, `pack_*`, magic values, hash constants, alphabets, file formats), then hand off to the crypto skill before attempting expensive lattice/solver work.
7. On macOS/ARM analyzing Linux x86-64 Nuitka ELFs, keep static progress even when you cannot execute the binary: use Python ELF program-header parsing to map file offsets to VMAs, then use Capstone to scan RIP-relative references into `.rodata`/`.data` constants. Also search for duplicate `app.py` / `__main__` constant blobs; Nuitka may embed near-identical module constant tables for `.__main__` and `__parents_main__`.
8. For Nuitka constants blobs, do not rely only on printable strings. Adjacent one-byte tags often encode useful Python object structure: strings may be prefixed by marker bytes such as `a`, `u`, `T`, `l`, `g`; large integers, tuples, local variable names, and function names can be recovered by dumping the raw hex around `app.py`, `__compiled__`, `__main__`, and challenge-specific constants.
9. For modern Nuitka DataComposer constant blobs, chunk layout is `name\0 + uint32_le(part_len) + part`, where `part` starts with `uint16_le(count)` followed by serialized constants and a final `.` tag. Tags are defined in `nuitka/build/include/nuitka/constants_blob_spec.h` (`T/L/D/S/P` containers, `l/q/g/G` integers, `a/u/v` strings, `b/c/d` bytes, `C` code-object specs, `.` end). If strings such as `app.py`, `derive_secret`, or hash constants have no normal code xrefs, treat them as DataComposer constants, parse the blob structure, and recover source-level constants before attempting crypto solving. Use `scripts/nuitka_datacomposer_dump.py` for a partial parser, and see `references/nuitka-datacomposer-constants.md` for the chunk workflow and native-xref follow-up.

## Default Tools

```bash
~/homebrew/bin/brew install ghidra radare2 rizin binwalk jadx apktool llvm
python3 -m pip install --user angr z3-solver capstone unicorn lief pycryptodome uncompyle6 pycdc zstandard
```

## Reference Files

- `references/reversing-playbook.md` — format-specific triage and solve paths.
- `references/binary-debugging-cheatsheet.md` — gdb/lldb/radare/Ghidra workflow.
- `references/unity-mono-api-gacha-notes.md` — session-derived Unity gacha/API reversing patterns and endpoint probing discipline.
- `references/nuitka-datacomposer-constants.md` — DataComposer chunk parsing, constants recovery, and native-xref next steps for stripped Nuitka CTF binaries.
- `references/nuitka-native-app-recovery-notes.md` — session-derived notes for Nuitka onefile/native app recovery when user `app.py` is compiled to native code and only metadata/constants survive as DataComposer blobs.
- `references/sagemath-inline-bignum-pattern.md` — triage and recovery for SageMath/Cython whole-program Linux ELFs: tiny `.rodata`, libc-only PLT, inline GMP/NTL, indirect callback dispatch, and why macOS arm64 cannot host symbolic execution for these binaries. Includes the three 512-bit constants extracted from the R3CTF "lift" challenge, the dispatcher callback pattern, and the Hensel lifting attack shape.
- `references/colima-x86_64-emulation-on-macos.md` — run x86-64 Linux CTF binaries on macOS arm64 via Colima + qemu-user-static + binfmt_misc; covers setup, limitations (no gdb/ptrace), and recommended workflow.

## Scripts

- `scripts/rev_triage.py` — first-pass artifact triage with hashes, format, strings, and suspicious markers.
- `scripts/nuitka_datacomposer_dump.py` — partial parser/dumper for Nuitka DataComposer constants blobs; use before native reversing when `.bytecode`, `__main__`, or `__parents_main__` chunks appear.
- `scripts/decode_whc2_wrapper.py` — decode the outer wrapper's two-byte rodata encoding to extract the embedded Go binary (WhC2 v0.1 pattern).
- `scripts/go_pclntab_parser.py` — parse Go 1.20+ pclntab to map function names to addresses; works on stripped Go binaries.

## 2025-2026 AI-Assisted Reverse Engineering & Tool Updates

### AI-Powered RE Tools (Game-Changing)

**OGhidra 3** (LLNL) — AI-powered Ghidra with LLM integration:
- Bridges LLMs (Ollama, custom APIs) with Ghidra via MCP (Model Context Protocol)
- **Smart Tool Buttons**: Analyze Current Function, Rename All Functions (bulk AI naming), Analyze Imports, Analyze Strings, Generate Security Report
- **Agentic Loop**: Plan → Execute → Review → Replan (adaptive analysis cycle)
- **RAG**: Vector embeddings for semantic search over analyzed functions
- **Malware Pattern Detection**: 12+ patterns with MITRE ATT&CK mappings
- **Session Management**: Save/restore analysis sessions
- Supports Ghidra 11.3.2+ and 12.0.3 (recommended)
- Install: `github.com/llnl/OGhidra`

**GhidraMCP** — MCP server for Ghidra:
- Exposes Ghidra's decompiler, function list, data types via JSON-RPC
- LLM can call `list_functions`, `decompile_function`, `rename_function`, `set_comment`, etc.
- Combined with Claude/GPT, enables natural language binary analysis

**IDA MCP** — Used at DEF CON 33 to solve CTF in 12 minutes:
- Exposes IDA Pro's decompiler and analysis via MCP
- LLM reads decompilation, renames functions, identifies protocol, writes exploit
- The DEF CON 33 workflow: `gather knowledge (from IDA) → formulate hypothesis → create exploit script → analyze script output → apply new findings to IDA` in a loop

**Agentic RE** (DEF CON 33 training):
- "Automating Reverse Engineering & Vulnerability Research with AI"
- Combines LLMs + MCP + Ghidra for autonomous binary analysis
- Design AI agents that can independently reverse engineer binaries

### Ghidra 12.0.3 Updates (2025-2026)

- **VS Code Integration**: Ghidra extension for VS Code (Monaco editor integration)
- **PyGhidra**: Python scripting directly in Ghidra without Java bridge overhead
- **PCode Emulation**: Enhanced emulation capabilities for dynamic analysis within Ghidra
- **Decompiler improvements**: Better C++ recovery, RTTI support, lambda reconstruction
- **Relative vtables analysis**: New analysis passes for Clang/LLVM relative vtables (4-byte offsets instead of 8-byte pointers)

### IDA Pro 9.0+ Updates

- **Hex-Rays decompiler**: Improved C++ recovery, better type inference
- **Lumina**: Cloud-based function signature sharing
- **Batch analysis**: API for automated processing of multiple binaries
- **MCP integration**: Third-party plugins for LLM-driven analysis

### AI-Powered RE Workflow Integration for CTF (2025-2026)

**MCP + LLM Binary Analysis** — proven at DEF CON 33 (12-minute solve):

1. **Install IDA Pro MCP** (`github.com/mrexodia/ida-pro-mcp`) or **GhidraMCP/ReVa** (`github.com/cyberkaida/reverse-engineering-assistant`)
2. Load challenge binary into IDA/Ghidra
3. LLM interacts via MCP tool calls: `list_functions`, `decompile_function`, `rename_function`, `set_comment`, `get_xrefs`
4. LLM identifies protocol, renames functions, discovers flag exfil path
5. LLM generates exploit script from decompilation
6. **Critical feedback loop**: update IDA decompilation with findings → LLM reads updated decompilation → iterates
7. Loop until flag: `gather knowledge → formulate hypothesis → create exploit → analyze output → update decompilation`

**GhidraMCP (ReVa) capabilities** — 110 tools including:
- Decompile, disassemble, cross-reference, annotate, batch analysis
- Headless/Docker mode for CI/CD integration
- Semantic search via vector embeddings (RAG over analyzed functions)
- Malware pattern detection (12+ MITRE ATT&CK patterns)

**OGhidra (LLNL)** — AI-powered Ghidra with agentic loop:
- Plan → Execute → Review → Replan (adaptive analysis cycle)
- Smart Tool Buttons: Analyze Function, Rename All (bulk AI naming), Generate Security Report
- Supports Ghidra 11.3.2+ and 12.0.3

**Practical tips from DEF CON 33 field report**:
- Give the LLM the flag format upfront (e.g., "flag{...}")
- Let LLM run Python scripts to check its own work
- Simple exploitation paths (no obfuscation tricks) work best
- Complex obfuscated challenges resist LLM solving — use traditional RE for those
- UAF→overlap→forge vtable type challenges can be partially automated (enumerate vtables with IDA Python, then LLM finds useful virtual functions for COOP)

**AngR + dAngr** (2025 update):
- dAngr: LLM-guided symbolic execution — uses AI to prune exploration branches
- LIFT: LLM-optimized intermediate representation for better decompilation
- Improved AArch64, RISC-V, WASM architecture support

### Modern Obfuscation Patterns (2025-2026)

| Obfuscation | Detection | Bypass |
|---|---|---|
| **Tigress** | Multiple virtualization passes, anti-tamper | Dynamic analysis, trace VM handlers |
| **O-LLVM 2025** | Control flow flattening, bogus control flow | Symbolic execution with angr, or LLM-assisted pattern matching |
| **Relative vtables** | 4-byte offsets instead of 8-byte pointers | IDA/Ghidra scripts to resolve offsets; COOP for exploitation |
| **WASM obfuscation** | Custom sections, import/export obfuscation | wasm-decompile, wasm2c, or browser debugger |
| **Flutter/Dart** | AOT compilation, obfuscated snapshots | Doldrums, reFlutter, or snapshot hash database |
| **React Native** | Hermes bytecode | hermes-dec, or trace through JS bridge |
| **Nuitka onefile** | Zstd compressed Python+native | DataComposer chunk parsing (see references) |

## macOS ARM64 → Linux x86-64 Static Analysis (Capstone)

When the challenge binary is x86-64 Linux ELF and **local execution fails** (Docker + qemu-user can't run glibc 2.38+ binaries, or Colima binfmt_misc won't execute them), use Capstone for static-only disassembly:

```bash
python3 -m pip install --user capstone
```

### Jump Table Dispatch Recovery (PIE + stripped)

PIE binaries use RIP-relative LEA to load the jump table base, then dispatch via indexed jump. Recover all menu/command targets:

```python
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import struct

md = Cs(CS_ARCH_X86, CS_MODE_64)

# Find LEA RBX, [RIP+disp] → this loads the jump table base
for addr in range(text_start, text_end):
    if data[addr:addr+3] == b'\x48\x8d\x1d':  # LEA RBX, [RIP+disp32]
        disp = struct.unpack('<i', data[addr+3:addr+7])[0]
        jt_base = addr + 7 + disp  # RIP-relative target
        # Dump jump table entries (32-bit signed offsets from table base)
        for i in range(7):  # typical menu has 0-6 options
            rel = struct.unpack('<i', data[jt_base + i*4:jt_base + i*4 + 4])[0]
            target = jt_base + rel
            print(f"Option {i}: -> 0x{target:x}")
```

**Hidden option 0**: The jump table dispatch uses `cmp eax, 6; ja loop` to bound input to 0-6, but the MENU only shows 1-6. Option 0 maps to a hidden target (often the menu loop itself = no-op, or a debug/backdoor function). Always dump option 0.

### scanf Non-Numeric Input → exit() Pattern

When a CTF binary reads menu input via `scanf("%d")`, non-numeric input ("flag", "show") causes scanf to return 0. The error handler calls `exit(1)`:

```asm
call scanf       ; scanf("%d", &var)
cmp eax, 1       ; did scanf read exactly 1 item?
jne error        ; no → exit
...
error:
mov edi, 1
call exit        ; exit(1) — program terminates instantly
```

**Implication**: Command-name injection via menu prompts is **impossible** with this pattern — non-numeric input terminates the binary. The vulnerability must be in sub-menu handlers (buffer overflow in fread, missing bounds check, format string in printf).

### String Reference Recovery from .text

For stripped PIE binaries, recover all string references by scanning LEA RIP-relative instructions:

```python
for addr in range(text_start, text_end - 7):
    if data[addr:addr+3] == b'\x48\x8d':  # LEA r64, [RIP+disp32]
        disp = struct.unpack('<i', data[addr+3:addr+7])[0]
        target = addr + 7 + disp
        if 0x2000 <= target < 0x2400:  # .rodata VMA range
            # Read null-terminated string at target
            end = data.find(b'\x00', target)
            s = data[target:end].decode('ascii', errors='replace')
            if len(s) > 1 and len(s) < 40:
                print(f"0x{addr:x}: '{s}'")
```

**Pitfall**: `&` in numpy/Python within a shell heredoc (`python3 << 'EOF'`) is interpreted as shell background operator. Use `np.logical_and()` or write the script to a file first.

## Maintenance Rule

Patch this skill when a reverse challenge teaches a new packer, VM pattern, anti-debug bypass, decompiler workflow, or script template.
