---
name: ghidra-scripting-basics
description: >
  Basics of Ghidra scripting (primarily Python/Jython or PyGhidra where available):
  navigate Program API, list functions/symbols, xrefs, comments, headless postScripts,
  and safe automation patterns. Use on authorized binaries in lab/CTF/owned codebases.
---

# Ghidra Scripting Basics

## Scope And Authorization

- **In scope:** Automating analysis on authorized samples and projects.
- **Out of scope:** Scripts designed solely to strip licensing from commercial software
  you do not own; unlicensed distribution of decompiled code.
- Scripts can modify databases and write files — use throwaway project copies for experiments.
- Prefer read-only exploration first; commit analyses deliberately.

## When To Use

- Bulk renaming, commenting, or exporting function lists.
- Finding xrefs to strings/imports quickly.
- Writing `-postScript` helpers for `analyzeHeadless`.
- Learning Ghidra Program API before Java-heavy modules.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Headless batch driver | `ghidra-headless-analyze` |
| Java GhidraScript / analyzers | `ghidra-scripting-java` |
| GDB pretty printers | `gdb-python-pretty-printers` |
| Full binary RE methodology | binary-re static-analysis skills |
| Implementation quality product code | `code-quality-standards` |

## Concepts

| API surface | Use |
| --- | --- |
| `currentProgram` | Active program |
| `FlatProgramAPI` / script helpers | Simplified address/function ops in scripts |
| `FunctionManager` | Enumerate functions |
| `SymbolTable` | Names, labels |
| `ReferenceManager` | Xrefs |
| `Listing` | Instructions, comments |
| `monitor` | Cancellation / progress |
| Headless args | `getScriptArgs()` |

**Runtime note:** Classic Ghidra uses Jython 2 for many “Python” scripts; newer setups may
use PyGhidra (CPython). Write portable simple scripts; test on your Ghidra version.

## Workflow

### 1. Environment

1. Open program in CodeBrowser or plan headless postScript.
2. Script Manager → New → Python (or Java if required).
3. Success: script prints function count; exports CSV; idempotent re-run.

### 2. Minimal script skeleton

```python
#@category Lab
#@menupath Tools.Lab.ExportFunctions

from ghidra.program.model.symbol import SymbolType

fm = currentProgram.getFunctionManager()
print("Program: {}".format(currentProgram.getName()))
print("Functions: {}".format(fm.getFunctionCount()))

for f in fm.getFunctions(True):
    print("0x{} {}".format(f.getEntryPoint(), f.getName()))
```

### 3. Strings and xrefs

```python
# Find string and xrefs (simplified pattern)
listing = currentProgram.getListing()
refman = currentProgram.getReferenceManager()
# Prefer defined data iteration or memory find APIs for your version
# Pseudo:
# addr = find("password")
# for ref in getReferencesTo(addr):
#     print(ref.getFromAddress())
```

Practical approach in UI first: Search → For Strings → then automate once pattern known.

### 4. Comments and bookmarks

```python
# Plate comment at function entry
from ghidra.program.model.listing import CodeUnit

func = getFunctionAt(currentAddress)  # Flat API if available in script context
if func:
    listing = currentProgram.getListing()
    listing.setComment(func.getEntryPoint(), CodeUnit.PLATE_COMMENT, "Reviewed by script")
```

### 5. Headless integration

```bash
analyzeHeadless PROJECT_DIR Proj \
  -process binary.elf \
  -scriptPath /path/to/scripts \
  -postScript ExportFunctions.py /out/funcs.txt
```

```python
# ExportFunctions.py
args = getScriptArgs()
out_path = args[0] if args else "functions.txt"
fm = currentProgram.getFunctionManager()
with open(out_path, "w") as fh:
    for f in fm.getFunctions(True):
        fh.write("{} {}\n".format(f.getEntryPoint(), f.getName()))
print("Wrote {}".format(out_path))
```

### 6. Safe mutation patterns

| Pattern | Guidance |
| --- | --- |
| Transactions | Wrap DB changes in open transaction if required by API |
| Idempotent names | Prefix `AUTO_` to detect re-runs |
| monitor.checkCanceled() | Long loops |
| Copies | Duplicate program before mass rename |
| Output | Write under controlled `out/` path only |

### 7. Debugging scripts

1. Print types and addresses frequently.
2. Use GUI Script Manager console output.
3. Catch exceptions; still log address of failure.
4. Reduce to minimal repro on one function.

### 8. Verify

- Re-run script twice → stable output.
- Spot-check 3 functions in decompiler vs export.
- Headless log shows script completed without exception.

## API task table

| Task | Starting point |
| --- | --- |
| List functions | `FunctionManager.getFunctions` |
| Rename function | `function.setName(...)` with source type |
| Get instruction | `Listing.getInstructionAt` |
| Xrefs to addr | `ReferenceManager.getReferencesTo` |
| Memory bytes | `Memory.getByte` / `getBytes` |
| Create bookmark | `BookmarkManager.setBookmark` |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | One task per script | 2k-line mega-script |
| Portability | Test Jython vs PyGhidra | Assume CPython packages always exist |
| Output | Explicit path args | Hardcoded `/tmp` secrets |
| Mutations | Transaction + prefix | Silent mass rename no undo plan |
| Auth | Owned samples | Mass decompile commercial suite for leak |

## Output Checklist

- [ ] Ghidra version / script runtime noted
- [ ] Sample authorization recorded
- [ ] Script solves one clear task
- [ ] Console/file output verified
- [ ] Headless args documented if used
- [ ] Idempotent behavior considered
- [ ] No untrusted path writes
- [ ] Cross-link to Java skill if analyzer needed

## Rules

- Authorized programs only.
- Prefer non-destructive exports before mass DB edits.
- Handle `monitor` cancellation in long jobs.
- Do not ship malware samples in script repos.
- Advanced Java analyzers → `ghidra-scripting-java`.
