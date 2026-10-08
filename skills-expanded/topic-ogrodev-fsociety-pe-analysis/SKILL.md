---
name: pe-analysis
description: |
  Activate this skill whenever the user mentions PE analysis, PE file, PE header, portable executable,
  Windows executable analysis, EXE analysis, DLL analysis, SYS driver analysis, OCX analysis,
  PE structure, PE format, PE parsing, PE triage, PE inspection, binary headers, file headers,
  DOS header, MZ header, COFF header, optional header, PE signature, image base, entry point,
  AddressOfEntryPoint, section table, section headers, section entropy, section permissions,
  .text section, .rdata section, .rsrc section, .reloc section, .data section, UPX section,
  import table, IAT, import address table, import directory, DLL imports, suspicious imports,
  API hashing, GetProcAddress hashing, delayed imports, bound imports,
  export table, EAT, export address table, DLL exports, forwarded exports, ordinal exports,
  resource table, resource directory, embedded resources, PE resources, resource extraction,
  version info, file version, manifest, embedded manifest, icon extraction,
  overlay data, appended data, PE overlay, data after last section,
  PE anomalies, header anomalies, suspicious PE, malformed PE, corrupted PE,
  timestamp analysis, compile time, TimeDateStamp, checksum validation, PE checksum,
  rich header, Rich signature, linker info, compiler detection,
  debug directory, PDB path, debug info, CodeView,
  authenticode, digital signature, signed binary, certificate validation,
  TLS callbacks, TLS directory, thread local storage,
  data directories, CLR header, .NET PE, COM descriptor,
  pefile, pestudio, PE-bear, CFF Explorer, dumpbin, objdump, readpe,
  packed binary detection, packer identification, UPX detection, section padding,
  security features check, ASLR, DEP, NX, CFG, SafeSEH, guard flags,
  PE file triage, unknown binary triage, suspicious binary, malware triage,
  binary classification, executable classification, initial binary assessment.
version: 2.0.0
---

# PE File Analysis

Portable Executable analysis is the foundation of Windows binary reverse engineering. Every .exe, .dll, .sys, .ocx, and .scr on Windows follows the PE format. Master PE structure and you can triage unknown binaries in minutes -- determine if they are packed, what they do, what anomalies they exhibit, and whether they warrant deeper analysis.

## Triage Workflow

Follow this sequence when analyzing an unknown PE file. Each step builds on the previous one.

### Step 1 — Compute Hashes and Basic Identification

Hash the binary first. Check hashes against known databases before spending time on manual analysis.

```bash
# SHA256 + MD5 + file type
node ${CLAUDE_PLUGIN_ROOT}/scripts/binary-hasher.js hash <binary>
file <binary>

# Check analysis database for prior work
node ${CLAUDE_PLUGIN_ROOT}/scripts/analysis-tracker.js check <sha256> pe-analysis
```

Record the hash immediately. Every subsequent finding references this hash.

### Step 2 — Header Analysis

Extract PE headers to determine architecture, compile time, entry point, and security features.

```bash
# Full header dump with radare2
r2 -qc 'iH' <binary>
r2 -qc 'iI' <binary>
```

```python
import pefile, time
pe = pefile.PE('<binary>')

# Compile timestamp
ts = pe.FILE_HEADER.TimeDateStamp
print(f"Compile time: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(ts))} UTC")
print(f"Machine: {hex(pe.FILE_HEADER.Machine)}")
print(f"Entry point: {hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)}")
print(f"Image base: {hex(pe.OPTIONAL_HEADER.ImageBase)}")
print(f"Subsystem: {pe.OPTIONAL_HEADER.Subsystem}")

# Security features
flags = pe.OPTIONAL_HEADER.DllCharacteristics
print(f"ASLR: {bool(flags & 0x40)}, DEP: {bool(flags & 0x100)}, CFG: {bool(flags & 0x4000)}")
print(f"No SEH: {bool(flags & 0x400)}, Force integrity: {bool(flags & 0x80)}")
```

Check for anomalies: future timestamps, epoch zero, entry point outside `.text`, missing ASLR/DEP.

See `references/pe-headers.md` for complete field reference.

### Step 3 — Section Analysis

Sections reveal packing, encryption, and structural manipulation.

```bash
r2 -qc 'iS' <binary>       # Section table
r2 -qc 'iSS' <binary>      # Sections with entropy
```

```python
for s in pe.sections:
    name = s.Name.decode().rstrip('\x00')
    entropy = s.get_entropy()
    raw = s.SizeOfRawData
    virt = s.Misc_VirtualSize
    ratio = virt / raw if raw > 0 else float('inf')
    chars = s.Characteristics
    rwx = f"{'R' if chars & 0x40000000 else '-'}{'W' if chars & 0x80000000 else '-'}{'X' if chars & 0x20000000 else '-'}"
    packed = "PACKED" if entropy > 7.0 else "HIGH" if entropy > 6.5 else ""
    inflated = "INFLATED" if ratio > 10 else ""
    print(f"{name:8s} raw={raw:>8d} virt={virt:>8d} ratio={ratio:>6.1f} entropy={entropy:.2f} {rwx} {packed} {inflated}")
```

Red flags: entropy > 7.0, VirtualSize >> RawSize, RWX permissions, packer section names (.UPX, .aspack, .themida, .vmp).

See `references/section-analysis.md` for section deep dive.

### Step 4 — Import Analysis

Imports reveal the binary's capabilities. Missing or minimal imports suggest packing or dynamic resolution.

```bash
r2 -qc 'ii' <binary>
r2 -qc 'ii~CreateRemote' <binary>    # Search for injection APIs
r2 -qc 'ii~Virtual' <binary>         # Search for memory manipulation
```

```python
if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        dll = entry.dll.decode()
        funcs = [i.name.decode() if i.name else f"ord#{i.ordinal}" for i in entry.imports]
        print(f"{dll} ({len(funcs)} imports): {', '.join(funcs[:5])}{'...' if len(funcs) > 5 else ''}")
else:
    print("NO IMPORT TABLE — likely packed or manually resolved")
```

Few imports (< 5 functions) from kernel32.dll only = strong packing indicator. Look for LoadLibrary + GetProcAddress as the only imports -- this means the binary resolves everything at runtime.

See `references/import-export-tables.md` for import/export deep dive.

### Step 5 — Resource Analysis

Resources can contain embedded executables, encrypted payloads, configuration data, and second-stage droppers.

```bash
r2 -qc 'ir' <binary>        # List resources
```

```python
if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
    def walk_resources(entry, level=0):
        if hasattr(entry, 'directory'):
            for e in entry.directory.entries:
                walk_resources(e, level + 1)
        elif hasattr(entry, 'data'):
            rva = entry.data.struct.OffsetToData
            size = entry.data.struct.Size
            data = pe.get_data(rva, size)
            entropy = pefile.SectionStructure.entropy_H(data)
            header = data[:4].hex() if len(data) >= 4 else data.hex()
            print(f"{'  '*level}Resource at RVA {hex(rva)}: {size} bytes, entropy={entropy:.2f}, magic={header}")
    for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        walk_resources(entry)
```

Look for: resources with MZ/PE headers (embedded executables), high-entropy resources (encrypted payloads), unusually large resources, RT_RCDATA entries.

See `references/resource-analysis.md` for resource deep dive.

### Step 6 — Overlay and Appended Data

Data appended after the last PE section is called the overlay. Packed binaries, installers, and droppers use overlays to store payloads.

```python
overlay_offset = pe.get_overlay_data_start_offset()
if overlay_offset:
    file_size = os.path.getsize('<binary>')
    overlay_size = file_size - overlay_offset
    with open('<binary>', 'rb') as f:
        f.seek(overlay_offset)
        header = f.read(16)
    print(f"Overlay at offset {hex(overlay_offset)}: {overlay_size} bytes ({overlay_size/1024:.1f} KB)")
    print(f"First 16 bytes: {header.hex()}")
    print(f"Overlay is {overlay_size * 100 / file_size:.1f}% of total file size")
else:
    print("No overlay data")
```

Large overlays relative to PE size indicate appended payloads. Check overlay headers for known signatures (PK for ZIP, MZ for embedded PE, 7z/RAR headers).

See `references/overlay-analysis.md` for overlay extraction and encrypted overlay detection.

### Step 7 — Anomaly Assessment

Run a comprehensive anomaly check to flag everything suspicious.

```python
warnings = []

# Timestamp anomalies
ts = pe.FILE_HEADER.TimeDateStamp
if ts == 0: warnings.append("TIMESTAMP: epoch zero (zeroed out)")
if ts > time.time(): warnings.append("TIMESTAMP: future date (forged)")
if ts < 946684800: warnings.append("TIMESTAMP: before 2000 (suspicious)")

# Entry point anomalies
ep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
ep_section = None
for s in pe.sections:
    if s.VirtualAddress <= ep < s.VirtualAddress + s.Misc_VirtualSize:
        ep_section = s.Name.decode().rstrip('\x00')
        break
if ep_section and ep_section != '.text':
    warnings.append(f"ENTRY POINT: in {ep_section} (expected .text)")
if ep == 0:
    warnings.append("ENTRY POINT: zero (DLL or anomalous)")

# Section anomalies
for s in pe.sections:
    name = s.Name.decode().rstrip('\x00')
    entropy = s.get_entropy()
    chars = s.Characteristics
    if entropy > 7.0: warnings.append(f"SECTION {name}: entropy {entropy:.2f} (packed/encrypted)")
    if (chars & 0x20000000) and (chars & 0x80000000): warnings.append(f"SECTION {name}: RWX permissions")
    if s.SizeOfRawData == 0 and s.Misc_VirtualSize > 0: warnings.append(f"SECTION {name}: raw=0, virt>0 (runtime unpacking)")

# Checksum
reported = pe.OPTIONAL_HEADER.CheckSum
actual = pe.generate_checksum()
if reported != 0 and reported != actual:
    warnings.append(f"CHECKSUM: mismatch (reported={hex(reported)}, actual={hex(actual)})")

# Security features missing
flags = pe.OPTIONAL_HEADER.DllCharacteristics
if not (flags & 0x40): warnings.append("SECURITY: ASLR disabled")
if not (flags & 0x100): warnings.append("SECURITY: DEP/NX disabled")

# Import anomalies
if not hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
    warnings.append("IMPORTS: no import table (packed or manual resolution)")
elif len(pe.DIRECTORY_ENTRY_IMPORT) <= 2:
    total_funcs = sum(len(e.imports) for e in pe.DIRECTORY_ENTRY_IMPORT)
    if total_funcs < 10:
        warnings.append(f"IMPORTS: minimal ({total_funcs} functions from {len(pe.DIRECTORY_ENTRY_IMPORT)} DLLs) — likely packed")

# TLS callbacks
if hasattr(pe, 'DIRECTORY_ENTRY_TLS') and pe.DIRECTORY_ENTRY_TLS:
    warnings.append("TLS: TLS callbacks present (anti-debug / pre-main code execution)")

for w in warnings:
    print(f"[!] {w}")
if not warnings:
    print("[+] No anomalies detected")
```

See `references/pe-anomalies.md` for the complete anomaly reference.

### Step 8 — Log and Report

Record all findings in the analysis tracker and generate a structured report.

```bash
# Log the analysis
node ${CLAUDE_PLUGIN_ROOT}/scripts/analysis-tracker.js add <sha256> pe-analysis completed \
  --binary "<filename>" \
  --notes "Summary of key findings"

# Log suspicious findings
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add "<filename>" suspicious-import \
  "CreateRemoteThread+VirtualAllocEx" HIGH "Process injection capability" --db ioc
```

## Report Template

When reporting PE analysis results, use this structure:

```
## PE Analysis: <filename>
SHA256: <hash>
File type: <type> | Architecture: <arch> | Size: <size>

### Headers
- Compile time: <timestamp>
- Entry point: <address> (section: <name>)
- Image base: <address>
- Subsystem: <type>
- Security: ASLR=<y/n> DEP=<y/n> CFG=<y/n>

### Sections
| Name | Raw Size | Virt Size | Entropy | Perms | Notes |
|------|----------|-----------|---------|-------|-------|

### Imports (<count> DLLs, <count> functions)
- Suspicious: <list of flagged imports>
- Notable DLLs: <list>

### Anomalies
- <anomaly 1>
- <anomaly 2>

### Assessment
Verdict: CLEAN | SUSPICIOUS | PACKED | MALICIOUS
Confidence: LOW | MEDIUM | HIGH
Recommended next steps: <actions>
```

## Tool Reference

| Tool | Install | Best For |
|------|---------|----------|
| `pefile` (Python) | `pip install pefile` | Scriptable PE parsing, field-level access, entropy calculation |
| `radare2` | `apt install radare2` | Quick CLI header/section/import dumps, disassembly |
| `pestudio` | Windows only | GUI static analysis, threat scoring, VirusTotal integration |
| `PE-bear` | github.com/hasherezade | GUI PE viewer, section hex view, anomaly highlighting |
| `CFF Explorer` | Windows only | PE editor, data directory browser, resource viewer |
| `dumpbin` | Visual Studio | MSVC PE dump utility (`/headers`, `/imports`, `/exports`, `/disasm`) |
| `objdump` | `apt install binutils` | GNU PE dump (`-x` headers, `-p` private headers, `-d` disasm) |
| `readpe` | `apt install pev` | Lightweight PE parser (`readpe -h`, `readpe -S`, `readpe -i`) |
| `binwalk` | `apt install binwalk` | Overlay/embedded file detection, entropy visualization |
| `die` | Detect It Easy | Packer/compiler/linker identification |

### dumpbin Quick Reference (Windows / Wine)

```bash
dumpbin /headers <binary>     # All headers
dumpbin /imports <binary>     # Import table
dumpbin /exports <binary>     # Export table
dumpbin /dependents <binary>  # DLL dependencies
dumpbin /disasm <binary>      # Disassembly
```

### objdump Quick Reference

```bash
objdump -x <binary>           # All headers
objdump -p <binary>           # Private headers (PE-specific)
objdump -d <binary>           # Disassembly
objdump -t <binary>           # Symbol table
```

### readpe Quick Reference

```bash
readpe -h <binary>            # PE headers
readpe -S <binary>            # Sections
readpe -i <binary>            # Imports
readpe -e <binary>            # Exports
readpe -r <binary>            # Resources
```

## Packing Detection Summary

A binary is likely packed if it exhibits THREE or more of these indicators:

1. Section entropy > 7.0 (especially .text or first section)
2. VirtualSize >> SizeOfRawData (10x+ ratio)
3. Few imports (< 10 functions, or only LoadLibrary/GetProcAddress)
4. No import table at all
5. Packer-named sections (.UPX, .aspack, .themida, .vmp0, .nsp0)
6. Entry point outside .text section
7. RWX section permissions
8. Section with RawSize=0 but VirtualSize > 0
9. Large overlay data
10. Strings analysis returns minimal readable strings

When packing is confirmed, route to the unpacking workflow (`/unpack` command).

## .NET PE Detection

.NET executables are PE files with a CLR header. Detect them early because .NET binaries require different analysis tools (ILSpy, dnSpy, de4dot).

```python
# Check for .NET
clr_dir = pe.OPTIONAL_HEADER.DATA_DIRECTORY[14]  # COM_DESCRIPTOR / CLR
if clr_dir.VirtualAddress != 0:
    print(".NET binary detected — use /dotnet command for analysis")
```

Signs of .NET PE: imports only `mscoree.dll` with `_CorExeMain` or `_CorDllMain`, has CLR data directory entry, contains `#Strings`/`#US`/`#GUID`/`#Blob` metadata streams.

## References

| Reference | Coverage |
|-----------|----------|
| `references/pe-headers.md` | DOS header, PE signature, COFF header, Optional header, data directories, Rich header, timestamps |
| `references/section-analysis.md` | Section structure, entropy analysis, permissions, TLS callbacks, packer indicators |
| `references/import-export-tables.md` | Import architecture, suspicious APIs, API hashing, delayed imports, export analysis, DLL side-loading |
| `references/resource-analysis.md` | Resource tree, embedded PE detection, version info, manifests, high-entropy resources |
| `references/pe-anomalies.md` | Header/section/import anomalies, timestamp correlation, Rich header attribution, Authenticode analysis |
| `references/overlay-analysis.md` | Overlay detection, extraction, embedded PE discovery, XOR-encrypted overlay detection |
