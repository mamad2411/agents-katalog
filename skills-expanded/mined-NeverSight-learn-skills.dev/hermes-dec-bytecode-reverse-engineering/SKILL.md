---
name: hermes-dec-bytecode-reverse-engineering
description: Disassemble and decompile React Native Hermes bytecode (HBC) files for reverse engineering
triggers:
  - decompile hermes bytecode
  - disassemble react native hbc file
  - reverse engineer hermes bundle
  - parse hermes bytecode headers
  - extract javascript from android apk
  - analyze hermes vm bytecode
  - convert hbc to javascript
  - decode react native bundle
---

# Hermes-Dec Bytecode Reverse Engineering

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## Overview

`hermes-dec` is a reverse-engineering tool for disassembling and decompiling React Native applications compiled to Hermes VM bytecode (HBC) format. It provides three main utilities:

- **hbc-file-parser**: Parse and display HBC file headers and metadata
- **hbc-disassembler**: Convert bytecode to assembly-like representation (.hasm)
- **hbc-decompiler**: Decompile bytecode to pseudo-JavaScript code

Hermes is the default JavaScript engine for React Native on Android (since RN 0.70) and is commonly found in mobile apps at `assets/index.android.bundle`.

## Installation

```bash
# Using pipx (recommended for CLI tools)
pipx install hermes-dec

# Using uv
uv tool install hermes-dec

# Using pip
pip install hermes-dec

# From source
git clone https://github.com/P1sec/hermes-dec.git
cd hermes-dec
pip install -e .
```

### System-specific installations

```bash
# Ubuntu (Snap)
sudo snap install hermes-dec
# Commands become: hermes-dec.hbc-disassembler, hermes-dec.hbc-file-parser, hermes-dec.hbc-decompiler

# Arch Linux (AUR)
yay -S hermes-dec
```

## Extracting Hermes Bytecode from APK

React Native Android apps package Hermes bytecode in APK files. Extract it first:

```bash
# APK files are ZIP archives
unzip my_application.apk -d my_application/
cd my_application/

# Verify it's Hermes bytecode
file assets/index.android.bundle
# Output: assets/index.android.bundle: Hermes JavaScript bytecode, version 84

# Or use 7z
7z x my_application.apk
```

Common locations in APK:
- `assets/index.android.bundle` (main bundle)
- `assets/*.hbc` (additional bundles)
- `assets/index.android.bundle.hbc`

## Core Commands

### 1. Parse File Headers

Inspect HBC file structure, bytecode version, and metadata:

```bash
# Display file information to stdout
hbc-file-parser assets/index.android.bundle

# Save output to file
hbc-file-parser assets/index.android.bundle > analysis.txt
```

**Example output:**
```
Hermes Bytecode File v84
File size: 2,453,678 bytes
SHA1 hash: a1b2c3d4...
Number of functions: 1,234
String table size: 45,678 entries
Debug info: present
```

### 2. Disassemble to Assembly

Convert bytecode to human-readable assembly (.hasm format):

```bash
# Output to stdout
hbc-disassembler assets/index.android.bundle

# Save to file
hbc-disassembler assets/index.android.bundle output.hasm

# Typical workflow
hbc-disassembler index.android.bundle disassembled.hasm
```

**Example .hasm output:**
```assembly
Function<loginUser>(3 params, 15 registers):
Offset in debug table: source 0x0000
    LoadParam         r2, 1
    LoadParam         r3, 2
    LoadConstString   r1, "username"
    GetByVal          r0, r2, r1
    LoadConstString   r1, "password"
    GetByVal          r4, r2, r1
    Call2             r0, r3, r0, r4
    Ret               r0
```

### 3. Decompile to Pseudo-JavaScript

Generate pseudo-JavaScript code (not yet valid JS, missing control flow):

```bash
# Output to stdout
hbc-decompiler assets/index.android.bundle

# Save to file
hbc-decompiler assets/index.android.bundle decompiled.js

# Typical workflow
hbc-decompiler index.android.bundle output.js
```

**Example decompiled output:**
```javascript
function loginUser(param0, param1, param2) {
  var r0, r1, r2, r3, r4;
  r2 = param1;
  r3 = param2;
  r1 = "username";
  r0 = r2[r1];
  r1 = "password";
  r4 = r2[r1];
  r0 = r3(r0, r4);
  return r0;
}
```

## Practical Workflows

### Full Analysis Pipeline

```bash
#!/bin/bash
# analyze_hbc.sh - Complete Hermes bytecode analysis

APK_FILE="$1"
OUTPUT_DIR="analysis_$(date +%Y%m%d_%H%M%S)"

mkdir -p "$OUTPUT_DIR"

# Extract APK
echo "[+] Extracting APK..."
unzip -q "$APK_FILE" -d "$OUTPUT_DIR/extracted"

# Find HBC files
echo "[+] Locating HBC files..."
find "$OUTPUT_DIR/extracted" -name "*.bundle" -o -name "*.hbc" > "$OUTPUT_DIR/hbc_files.txt"

# Process each HBC file
while IFS= read -r hbc_file; do
    basename=$(basename "$hbc_file")
    echo "[+] Processing $basename..."
    
    # Parse headers
    hbc-file-parser "$hbc_file" > "$OUTPUT_DIR/${basename}.info.txt"
    
    # Disassemble
    hbc-disassembler "$hbc_file" "$OUTPUT_DIR/${basename}.hasm"
    
    # Decompile
    hbc-decompiler "$hbc_file" "$OUTPUT_DIR/${basename}.js"
    
done < "$OUTPUT_DIR/hbc_files.txt"

echo "[+] Analysis complete in $OUTPUT_DIR"
```

### Searching for Specific Functions

```bash
# Disassemble and search for API endpoints
hbc-disassembler index.android.bundle output.hasm
grep -i "https://" output.hasm

# Find authentication-related code
grep -i -E "(token|auth|password|login)" output.hasm

# Decompile and search for specific strings
hbc-decompiler index.android.bundle output.js
grep -i "api_key" output.js
```

### Comparing Versions

```bash
# Compare two versions of the same app
hbc-disassembler old_version/index.android.bundle old.hasm
hbc-disassembler new_version/index.android.bundle new.hasm

# Diff the assembly
diff -u old.hasm new.hasm > changes.diff

# Or use a better diff tool
code --diff old.hasm new.hasm
```

## Python API Usage

While hermes-dec is primarily a CLI tool, you can import its modules in Python:

```python
#!/usr/bin/env python3
"""
Example: Programmatic access to hermes-dec functionality
"""
import sys
from pathlib import Path

# Import hermes-dec modules (structure may vary by version)
# Note: Internal API may change; CLI is the stable interface

def analyze_hbc_file(hbc_path: Path):
    """
    Analyze an HBC file programmatically
    """
    if not hbc_path.exists():
        print(f"Error: {hbc_path} not found")
        return
    
    # Read file header
    with open(hbc_path, 'rb') as f:
        magic = f.read(8)
        if magic[:4] != b'\xC6\x1F\xBC\x03':
            print("Not a valid Hermes bytecode file")
            return
        
        # Version is at offset 4
        version = int.from_bytes(magic[4:8], 'little')
        print(f"Hermes bytecode version: {version}")
    
    # For detailed parsing, use the CLI tools
    import subprocess
    
    # Get file info
    result = subprocess.run(
        ['hbc-file-parser', str(hbc_path)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("\n=== File Info ===")
        print(result.stdout)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <hbc_file>")
        sys.exit(1)
    
    analyze_hbc_file(Path(sys.argv[1]))
```

### Batch Processing Script

```python
#!/usr/bin/env python3
"""
Batch process multiple APK files for Hermes bytecode analysis
"""
import subprocess
import zipfile
from pathlib import Path
from typing import List

def extract_hbc_from_apk(apk_path: Path, output_dir: Path) -> List[Path]:
    """
    Extract HBC files from an APK
    Returns list of extracted HBC file paths
    """
    hbc_files = []
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(apk_path, 'r') as apk:
        for name in apk.namelist():
            if name.endswith('.bundle') or name.endswith('.hbc'):
                # Extract file
                target = output_dir / Path(name).name
                with apk.open(name) as source, open(target, 'wb') as dest:
                    dest.write(source.read())
                
                # Verify it's HBC
                if is_hermes_bytecode(target):
                    hbc_files.append(target)
                    print(f"[+] Extracted {name} -> {target}")
    
    return hbc_files

def is_hermes_bytecode(file_path: Path) -> bool:
    """Check if file is Hermes bytecode"""
    try:
        with open(file_path, 'rb') as f:
            magic = f.read(4)
            return magic == b'\xC6\x1F\xBC\x03'
    except:
        return False

def decompile_hbc(hbc_path: Path, output_path: Path):
    """Decompile HBC file to pseudo-JavaScript"""
    subprocess.run(
        ['hbc-decompiler', str(hbc_path), str(output_path)],
        check=True
    )
    print(f"[+] Decompiled {hbc_path.name} -> {output_path}")

def main():
    apk_dir = Path("apks")
    output_base = Path("decompiled")
    
    for apk in apk_dir.glob("*.apk"):
        print(f"\n[*] Processing {apk.name}")
        
        # Create output directory for this APK
        apk_output = output_base / apk.stem
        apk_output.mkdir(parents=True, exist_ok=True)
        
        # Extract HBC files
        hbc_files = extract_hbc_from_apk(apk, apk_output / "extracted")
        
        # Decompile each
        for hbc in hbc_files:
            js_output = apk_output / f"{hbc.stem}.js"
            try:
                decompile_hbc(hbc, js_output)
            except subprocess.CalledProcessError as e:
                print(f"[!] Failed to decompile {hbc.name}: {e}")

if __name__ == "__main__":
    main()
```

## Understanding Output Formats

### Assembly (.hasm) Format

The disassembler outputs Hermes VM assembly instructions:

```assembly
Function<ComponentName>(params, registers):
    # Instruction    Dest  Source1  Source2
    LoadParam        r0,   1        # Load first parameter
    LoadConstString  r1,   "key"    # Load string constant
    GetByVal         r2,   r0, r1   # Property access: r0[r1]
    Call             r3,   r2       # Function call
    Ret              r3              # Return value
```

Common opcodes:
- `LoadParam`: Load function parameter
- `LoadConst*`: Load constants (string, number, undefined, etc.)
- `GetByVal`/`PutByVal`: Property access
- `Call*`: Function calls
- `NewObject`/`NewArray`: Object/array creation
- `Ret`: Return from function
- `Jmp*`: Jump instructions (control flow)

### Pseudo-JavaScript Format

The decompiler outputs register-based pseudo-code:

```javascript
// Not yet valid JavaScript - shows data flow
function example(param0, param1) {
  var r0, r1, r2, r3;  // Registers
  r0 = param0;          // Parameter assignment
  r1 = "property";      // String constant
  r2 = r0[r1];          // Property access
  r3 = someFunc(r2);    // Function call
  return r3;
}
```

**Limitations:**
- No control flow reconstruction (loops, conditionals appear linear)
- Register-based (not variable-based)
- May have dead code
- Requires manual cleanup for valid JS

## Troubleshooting

### Not a Hermes Bytecode File

```bash
$ file index.android.bundle
index.android.bundle: ASCII text, with very long lines
```

**Solution**: This is minified JavaScript, not Hermes bytecode. The app doesn't use Hermes engine or you have the wrong file.

### Unsupported Bytecode Version

```
Error: Unsupported bytecode version 96
```

**Solution**: Update hermes-dec to the latest version:
```bash
pipx upgrade hermes-dec
# or
pip install --upgrade hermes-dec
```

If still unsupported, check the [GitHub issues](https://github.com/P1sec/hermes-dec/issues) or open a new one.

### Incomplete Decompilation

The decompiler output is incomplete or has missing functions.

**Solution**: Try disassembly first to understand structure:
```bash
# Disassemble to see raw instructions
hbc-disassembler file.bundle output.hasm

# Then manually interpret critical sections
# The decompiler is best-effort; some complex patterns may not decompile
```

### Empty Output Files

```bash
$ hbc-decompiler index.android.bundle output.js
$ wc -l output.js
0 output.js
```

**Solution**: Check file format and permissions:
```bash
# Verify it's HBC
file index.android.bundle
hexdump -C index.android.bundle | head

# Check permissions
ls -la index.android.bundle

# Try with stdout first
hbc-decompiler index.android.bundle
```

### APK Extraction Issues

```bash
$ unzip app.apk
error: cannot find or open app.apk
```

**Solution**: Ensure APK is not corrupted:
```bash
# Verify ZIP structure
7z t app.apk

# Try alternative extraction
jar xf app.apk
# or
python -m zipfile -e app.apk output_dir/
```

## Advanced Techniques

### Finding Obfuscated Strings

```bash
# Decompile and search for base64
hbc-decompiler index.android.bundle output.js
grep -E '[A-Za-z0-9+/]{20,}={0,2}' output.js

# Look for hex patterns
grep -E '0x[0-9a-fA-F]{4,}' output.js
```

### Extracting API Endpoints

```bash
# Search for URLs in disassembly
hbc-disassembler index.android.bundle output.hasm
grep -oE 'https?://[^"]+' output.hasm | sort -u > endpoints.txt

# Find in decompiled code
hbc-decompiler index.android.bundle output.js
grep -oE '(http|https)://[a-zA-Z0-9./?=_-]*' output.js | sort -u
```

### Cross-referencing Functions

```bash
# Find function definitions and calls
hbc-disassembler index.android.bundle output.hasm
grep "Function<" output.hasm > functions.txt
grep "Call" output.hasm > calls.txt

# Analyze function call graph
awk '/Function</{print $0} /Call/{print "  -> " $0}' output.hasm
```

## Documentation Resources

- [Hermes VM Design Docs](https://hermesengine.dev/docs/vm/)
- [Bytecode Format Spec](https://github.com/facebook/hermes/tree/main/doc)
- [Opcode Reference](https://p1sec.github.io/hermes-dec/opcodes_table.html)
- [React Native Hermes Guide](https://reactnative.dev/docs/hermes)
- [P1sec Blog Post](https://www.p1sec.com/blog/releasing-hermes-dec-an-open-source-disassembler-and-decompiler-for-the-react-native-hermes-bytecode)

## Version Compatibility

Hermes bytecode versions and React Native releases:
- v59: Hermes 0.1.0 (July 2019)
- v74: React Native 0.64 (iOS support)
- v84: React Native 0.70 (default on Android)
- v90+: Recent React Native versions (2023+)

Check bytecode version:
```bash
hbc-file-parser file.bundle | grep -i version
```
