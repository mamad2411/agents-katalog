---
name: ghidra-re
description: >
  Install, configure, and operate Ghidra for binary reverse engineering. Use when the
  user needs to analyze executables, firmware, or malware with Ghidra; when performing
  static analysis, decompilation, function analysis, or patching; when scripting Ghidra
  with Java or Python (Jython/PyGhidra); when running headless batch analysis; or when
  comparing Ghidra workflows to IDA Pro or radare2. Covers installation, CodeBrowser
  navigation, decompiler, data types, debugging, plugin development, and CTF workflows.
  Source: https://github.com/NationalSecurityAgency/ghidra
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/NationalSecurityAgency/ghidra
  stars: '66535'
---

# ghidra-re Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs to reverse engineer a binary, firmware image, or malware sample
- Analyzing compiled code with Ghidra's decompiler or disassembler
- Writing Ghidra scripts to automate analysis (Java or Python)
- Running headless Ghidra analysis in CI/CD or batch workflows
- Patching binaries, recovering symbols, or managing data types
- The user asks how Ghidra compares to IDA Pro or radare2/Cutter

## What Ghidra Is

Ghidra is the NSA's open-source software reverse engineering (SRE) framework, released
in 2019. It provides a full interactive GUI (CodeBrowser), a powerful decompiler that
produces C-like pseudocode, and a scriptable API in Java and Python. It supports x86,
x86-64, ARM, AARCH64, MIPS, PowerPC, and 30+ other architectures, making it the
go-to free alternative to IDA Pro for malware analysis, firmware reversing, and CTFs.

## Installation

```bash
# Prerequisites: Java 17+ (JDK, not JRE)
java -version    # must be 17+
sudo apt install openjdk-17-jdk   # Debian/Ubuntu

# Download latest release from GitHub releases
curl -LO https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.1.2_build/ghidra_11.1.2_PUBLIC_20240709.zip
unzip ghidra_11.1.2_PUBLIC_20240709.zip
cd ghidra_11.1.2_PUBLIC

# Launch GUI
./ghidraRun                       # Linux/macOS
ghidraRun.bat                     # Windows

# Optional: add to PATH
echo 'export PATH=$PATH:/opt/ghidra_11.1.2_PUBLIC' >> ~/.bashrc
```

### PyGhidra (Python 3 binding)

```bash
pip install pyghidra
# Enables Python 3 scripting instead of Jython 2.7
python3 -c "import pyghidra; pyghidra.start()"
```

## Project Setup

```
File > New Project
  ├── Non-Shared Project (local, default)
  └── Shared Project (team server / Ghidra Server)

File > Import File   (or drag binary into project window)
  ├── Format: auto-detected (ELF, PE, Mach-O, raw binary, firmware)
  ├── Language: auto-detected or manually set (e.g., x86:LE:64:default)
  └── Options: load external libraries, symbol files, apply labels

# After import: double-click to open in CodeBrowser
# "Analyze Now?" dialog → Yes (runs auto-analysis)
```

## CodeBrowser Navigation

```
Key bindings (defaults):
  G               → Go to address
  L               → Edit label at cursor
  ;               → Add comment (pre/post/EOL/plate/repeatable)
  N               → Rename current function/variable
  T               → Retype variable (change data type)
  X               → Cross-references (XREFs) list
  Ctrl+F          → Search program text
  Ctrl+Shift+F    → Search memory bytes
  Ctrl+G          → Go to specific address
  Ctrl+E          → Edit instruction bytes (patch)
  Ctrl+Alt+↑/↓    → Navigate call history back/forward
  F12 / Decompile → Open decompiler for current function
  Space           → Toggle listing ↔ decompiler focus

Windows:
  CodeBrowser     → Disassembly listing
  Decompiler      → C pseudocode
  Symbol Tree     → Functions, labels, namespaces
  Data Type Manager → structs, enums, typedefs
  Program Trees   → Segment/section map
  Byte Viewer     → Hex dump
  References      → XREF browser
  Bookmarks       → User-defined bookmarks
```

## Decompiler Usage

```
# Open decompiler: Window > Decompiler  (or double-click function)
# Decompiler pane shows C-like pseudocode synchronized with listing

# Key operations in decompiler pane:
N           → Rename variable
T           → Retype variable (assign struct pointer, etc.)
Ctrl+L      → Override function signature
Right-click → "Auto Fill in Structure" (recover struct from access pattern)
Right-click → Commit Params/Return

# Improving decompiler output:
1. Rename cryptic vars: iVar1 → decrypted_len
2. Assign types: assign DWORD* → struct MyHeader*
3. Mark calling convention: __stdcall, __fastcall, __thiscall
4. Import PDB (Windows): File > Load PDB File
```

## Function Analysis

```
# List all functions
Window > Symbol Tree > Functions folder

# Find function by name
Ctrl+F in Symbol Tree

# Identify function purpose via:
1. String references: find string xrefs from function
2. Import calls: check which API the function wraps
3. Called-from: XREF 'c' (called-by) list

# Rename/annotate functions
Right-click function name > Edit Function
  - Change name, return type, parameters, calling convention

# Detect and create functions in shellcode / position-independent code
D   → Disassemble at cursor
F   → Create function at cursor
```

## Data Type Management

```
# Open: Window > Data Type Manager

# Apply struct to pointer
1. Define struct in Data Type Manager (New > Struct)
2. In decompiler, right-click variable > Retype Variable
3. Select your struct type

# Import C headers to auto-create types
File > Parse C Source > add .h files
# Useful for: Windows types (windows.h via NTDDK headers),
# OpenSSL structs, network protocol headers

# Export types as C header
File > Export > Export Program as C Header

# Apply array
In listing: select bytes > right-click > Data > array
```

## Scripting with Ghidra

### Java Script (Script Manager)

```java
// Window > Script Manager > New Script > Java
// Example: list all functions with "crypt" in name

import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;

public class FindCryptFunctions extends GhidraScript {
    @Override
    public void run() throws Exception {
        FunctionManager fm = currentProgram.getFunctionManager();
        for (Function f : fm.getFunctions(true)) {
            if (f.getName().toLowerCase().contains("crypt")) {
                println(f.getEntryPoint() + "  " + f.getName());
            }
        }
    }
}
```

### Python Script (Jython 2.7 — built-in, or PyGhidra for Python 3)

```python
# Window > Script Manager > New Script > Python
# Built-in Jython example: rename all FUN_ functions with xref heuristics

from ghidra.program.model.listing import FunctionManager

fm = currentProgram.getFunctionManager()
for func in fm.getFunctions(True):
    if func.getName().startswith("FUN_"):
        xrefs = getReferencesTo(func.getEntryPoint())
        print("{} <- {} xrefs".format(func.getEntryPoint(), len(xrefs)))
```

```python
# PyGhidra (Python 3) — standalone script outside GUI
import pyghidra
with pyghidra.open_program("/path/to/binary") as flat_api:
    for func in flat_api.currentProgram.getFunctionManager().getFunctions(True):
        print(func.getName(), func.getEntryPoint())
```

### Useful Script Examples

```python
# Find all calls to strcmp / strcpy (import detection)
from ghidra.program.model.symbol import SymbolType

sym_table = currentProgram.getSymbolTable()
for sym in sym_table.getAllSymbols(True):
    if sym.getName() in ['strcmp', 'strcpy', 'system', 'exec']:
        for ref in getReferencesTo(sym.getAddress()):
            print("Call to {} at {}".format(sym.getName(), ref.getFromAddress()))
```

## Headless Analysis Mode

```bash
# analyzeHeadless: batch analyze without GUI
# Syntax: analyzeHeadless <projectDir> <projectName> [options]

# Import and analyze new binary
./support/analyzeHeadless /tmp/ghidra_projects MyProject \
  -import /path/to/binary \
  -postScript ExportFunctions.py \
  -deleteProject

# Analyze existing project
./support/analyzeHeadless /tmp/ghidra_projects MyProject \
  -process binary_name \
  -postScript FindCryptFunctions.java

# Run script on multiple binaries
./support/analyzeHeadless /tmp/proj BatchJob \
  -import /malware/samples/*.exe \
  -postScript StringExtractor.py /tmp/strings_out.txt \
  -deleteProject

# Useful flags
-noanalysis          # import without auto-analysis (faster for raw dump)
-loader BinaryLoader # force raw binary loader
-processor x86:LE:64:default  # set arch manually
-cspec default        # calling convention spec
-readOnly            # don't modify project
-log /tmp/ghidra.log # log output to file
```

## Patching Binaries

```
# In CodeBrowser listing view:
1. Navigate to instruction to patch
2. Right-click > Patch Instruction  (GUI assembler)
   OR
   Ctrl+E → edit raw bytes directly

# NOP out a conditional jump:
1. Select JNZ / JE bytes
2. Right-click > Patch Instruction → type NOP

# Export patched binary:
File > Export Program > Format: Binary (raw bytes)
File > Export Program > Format: ELF  (preserve headers)

# Via Script:
from ghidra.program.model.mem import MemoryAccessException
addr = toAddr(0x401234)
setBytes(addr, [0x90, 0x90])   # NOP NOP
```

## Debugging Integration

```
# Ghidra Debugger (Ghidra 10.2+)
Window > Debugger
  - Supports GDB, WinDbg, DBGENG backends
  - Use "Connect" to attach to a running process or start a new one

# GDB integration workflow:
1. Start target: gdbserver :1234 ./binary
2. In Ghidra Debugger: Debugger > Connect > gdb
   target remote localhost:1234
3. Synchronized stepping in decompiler and listing

# For malware: prefer snapshots / qemu-based debugging
```

## Plugin Development

```java
// ghidra_scripts/ or extension project in Eclipse + GhidraDev plugin

// Minimal GhidraScript plugin:
import ghidra.app.plugin.core.analysis.AbstractAnalyzer;
import ghidra.program.model.listing.Program;
import ghidra.util.task.TaskMonitor;

// Full plugin: File > Configure > Install Extensions
// Build with Gradle:
gradle buildExtension
// Output: dist/ghidra_<ver>_<date>_MyPlugin.zip
// Install: File > Install Extensions > select ZIP
```

## Common Workflows

### Malware Analysis

```
1. Import sample: File > Import, enable "Load External Libraries" if needed
2. Auto-analyze (accept defaults, add "Aggressive Instruction Finder")
3. Check imports: Symbol Tree > Imports → identify suspicious APIs
   (VirtualAlloc, WriteProcessMemory, CreateRemoteThread, WinExec)
4. Find strings: Window > Defined Strings → look for URLs, registry keys, mutexes
5. XREF interesting strings back to functions
6. Rename functions as purpose becomes clear
7. Focus on WinMain / DllMain entry point, trace call graph
```

### CTF Binary Exploitation Reversing

```
1. checksec --file=binary    (run externally; note PIE, NX, canary)
2. Import into Ghidra, analyze
3. Find main(): Symbol Tree > Functions > main
4. Decompile: look for vuln patterns (strcpy, gets, sprintf to stack buffer)
5. Find win function / magic check: search strings for "flag", "correct"
6. Patch check in binary or build exploit from decompiled logic
7. Export patched binary for testing
```

### Firmware Reversing

```bash
# Extract firmware first
binwalk -e firmware.bin         # extract file systems
cd _firmware.bin.extracted/

# Import squashfs root filesystem binaries into Ghidra
# For raw flash: use "Raw Binary" loader, manually set base address
# ARM Cortex-M: processor = ARM:LE:32:Cortex, base = 0x08000000

./support/analyzeHeadless /tmp/proj FirmwareAnalysis \
  -import _firmware.bin.extracted/squashfs-root/bin/httpd \
  -postScript AutoRenameThunks.py \
  -deleteProject
```

## Comparison: Ghidra vs IDA Pro vs radare2

| Feature | Ghidra | IDA Pro | radare2 |
|---|---|---|---|
| Cost | Free / Open source | $3k+ commercial | Free / Open source |
| Decompiler | Built-in (free) | Hex-Rays (+cost) | Cutter/r2dec/retdec |
| Scripting | Java, Python | IDAPython, IDC | r2pipe, JavaScript |
| Headless mode | Yes (`analyzeHeadless`) | Yes (idat -A) | Yes (r2 -q) |
| Collaboration | Ghidra Server | IDA teams | No built-in |
| Plugin ecosystem | Growing | Mature | Mature |
| Best for | Large binaries, firmware | Commercial malware | CLI/scripting workflows |

## Troubleshooting

| Symptom | Fix |
|---|---|
| "Unsupported major.minor version" on launch | Java version mismatch; install JDK 17+ |
| Decompiler shows `??` types everywhere | Run full auto-analysis; enable all analyzers |
| Headless crashes with OutOfMemoryError | Edit `support/launch.sh`: increase `-Xmx` (e.g., `-Xmx8G`) |
| Script not found in Script Manager | Ensure script is in `~/ghidra_scripts/` or configured path |
| XREF list empty for function | Function may be called via indirect pointer; search for addr in `.data` |
| Python 3 script fails in Jython | Use PyGhidra (`pip install pyghidra`) for Python 3 support |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
