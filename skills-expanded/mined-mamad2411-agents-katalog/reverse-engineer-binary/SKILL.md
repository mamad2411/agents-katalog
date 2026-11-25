---
name: reverse-engineer-binary
description: Analyze a compiled/binary file to understand what it does — native executables (.exe/EXE, ELF, Mach-O), Java (.class/.jar), .NET, shared libraries. Identify the format, pull strings, inspect headers/imports, and disassemble or decompile. Use when given a binary/executable/jar to reverse-engineer, inspect, or explain.
---

# Reverse-engineer / analyze a binary

Work in the sandbox with run_code. Available: `file`, `xxd`, `unzip`, `java`,
`javap`, Python (pip-install `capstone`, `pefile`, `pyelftools`, `macholib` as
needed). `strings`/`objdump`/`readelf` are NOT installed — use the bundled
`scripts/strings.py` and the Python libraries instead.

## 1. Identify the file
```bash
file target.bin
xxd target.bin | head -4          # magic bytes: MZ=PE/.exe, 7f454c46=ELF, cafebabe=Java .class, feedface/cffaedfe=Mach-O, PK=zip/jar
```

## 2. Pull strings (fast signal: URLs, paths, commands, versions, keys, libs)
```bash
python scripts/strings.py target.bin 5 | head -100
python scripts/strings.py target.bin 5 | grep -iE "http|/api|key|token|password|cmd|exec|\.dll|\.so" | head
```

## 3. By format

### Native PE / .exe (Windows)
```bash
pip install -q pefile capstone
python - <<'PY'
import pefile
pe = pefile.PE("target.exe")
print("entry:", hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
print("sections:", [(s.Name.decode(errors='replace').strip('\x00'), hex(s.SizeOfRawData)) for s in pe.sections])
for e in getattr(pe,'DIRECTORY_ENTRY_IMPORT',[]):
    print(e.dll.decode(), "->", [imp.name.decode() for imp in e.imports if imp.name][:15])
PY
```
High section entropy ⇒ likely packed/obfuscated (note it). Disassemble a region with `capstone`.

### Native ELF (Linux)
```bash
pip install -q pyelftools capstone
python - <<'PY'
from elftools.elf.elffile import ELFFile
f=ELFFile(open("target","rb"))
print("arch:",f.get_machine_arch(),"entry:",hex(f.header.e_entry))
print("sections:",[s.name for s in f.iter_sections()])
PY
```
(Mach-O: use `macholib`.)

### Java (.class / .jar)
```bash
javap -p -c Target.class | head -80                 # disassemble bytecode of one class
unzip -o app.jar -d app_out >/dev/null              # a .jar is a zip
cat app_out/META-INF/MANIFEST.MF                     # find Main-Class / version
ls app_out                                           # package layout, bundled libs
javap -p -c app_out/com/example/Main.class | head    # disassemble a class
```
For readable Java source, decompile with CFR (single jar, runs on the installed JVM):
```bash
curl -L -o cfr.jar https://github.com/leibnitz27/cfr/releases/download/0.152/cfr-0.152.jar
java -jar cfr.jar app.jar --outputdir src_out >/dev/null
# then explore src_out with the explore-codebase skill (grep, not read-all)
```

## 4. Synthesize
Report: file type/arch, what it appears to do, notable imports/APIs/strings, network
or filesystem behavior, signs of packing/obfuscation, and (if asked) the decompiled
logic of the relevant part. Cite the concrete evidence (a string, an import, a line).

## Notes
- Prefer STATIC analysis — you usually don't need to run the binary to understand
  it, and running it isn't what these tools do.
- Keep pip installs minimal; clean up large extracted folders when done.
