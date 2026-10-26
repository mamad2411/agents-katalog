---
name: ghidra-idareverseengineeringskill
description: "Ghidra and IDA Pro workflows for binary analysis: headless analysis, decompiler output, scripting (Ghidra Java/Python, IDAPython), function recovery, types, signatures, and xrefs. Use when the user asks for Ghidra, IDA, analyzeHeadless, IDAPython, Ghidra scripts, FLIRT/FunctionID, or database-driven reverse engineering of owned/lab/CTF binaries — not for unauthorized analysis of third-party malware outside a safe lab."
  Ghidra and IDA Pro workflows for binary analysis: headless analysis, decompiler
  output, scripting (Ghidra Java/Python, IDAPython), function recovery, types,
  signatures, and xrefs. Use when the user asks for Ghidra, IDA, analyzeHeadless,
  IDAPython, Ghidra scripts, FLIRT/FunctionID, or database-driven reverse engineering
  of owned/lab/CTF binaries — not for unauthorized analysis of third-party malware
  outside a safe lab.
---

# Ghidra and IDA Reverse Engineering

## Scope And Authorization

- **In scope:** binaries you own, vendor-supplied samples under license, CTF/lab challenges, malware **only** in isolated analysis environments with explicit authorization.
- **Out of scope:** reverse engineering to circumvent license/protections unlawfully; executing untrusted samples on production hosts; distributing cracked software.
- Keep samples in a disposable VM/container; no shared host mounts with credentials.
- Redact customer PII found in strings from notes when not required for the task.
- Pair custom loaders/scripts that ship in product repos with `code-quality-standards`.

## When To Use

- Static RE of PE/ELF/Mach-O with Ghidra or IDA Pro.
- Headless batch analysis, auto-commenting, or CI-assisted triage of builds.
- Recovering call graphs, structs, enums, and cross-references.
- Porting analysis between Ghidra (`.gpr`/project) and IDA (`.i64`/`.idb`) workflows.
- Applying signatures (FID, FLIRT), type libraries, and processor modules.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Nested binary-re static playbook | `binary-re/static-analysis` |
| Dynamic debugging / instrumentation | `binary-re/dynamic-analysis` |
| Tool install and version pins | `binary-re/tool-setup` |
| Synthesis / reporting of RE findings | `binary-re/synthesis` |
| SSL pinning bypass on owned mobile apps | `mobile-ssl-pinning-bypass` |
| Protocol recovery from traffic | `protocol-reverse-engineering` / `NetworkProtocolAnalysisSkill` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Ghidra | IDA |
| --- | --- | --- |
| Project model | Project + program; shared/versioned projects | IDB/i64 database per file |
| Headless | `analyzeHeadless` | `idat`/`ida64` batch + scripts |
| Scripting | Java, Jython/PyGhidra, GhidraDev | IDAPython, IDC |
| Decompiler | P-Code → decompiler window | Hex-Rays (licensed) |
| Types | Data Type Manager, archives | Local types, TIL, header parse |
| Signatures | FunctionID, BSim (version-dependent) | FLIRT, Lumina (policy-dependent) |
| Xrefs | Cross Reference API / UI | `XrefsTo` / `XrefsFrom` |

## Workflow

### 1. Confirm scope, isolation, and success criteria

1. Record sample hash (SHA-256), origin, OS/arch, authorization, and isolation boundary.
2. Success examples: entrypoints mapped; crypto/network funcs named; struct for key packet recovered; headless script emits JSON report.
3. Snapshot the VM; disable outbound net unless traffic capture is in scope.

### 2. Triage the file before deep RE

```bash
sha256sum sample.bin
file sample.bin
# Optional first pass
rabin2 -I sample.bin 2>/dev/null || true
strings -n 8 sample.bin | head -n 50
```

1. Note packer/compiler hints (UPX, rich header, Go build ID).
2. If packed, plan unpack (dynamic) before trusting static CFG — route heavy dynamic work to `binary-re/dynamic-analysis`.
3. Prefer **immutable original** + working copy for databases.

### 3. Ghidra interactive / headless

**Import and analyze (GUI):** New project → Import → auto-analyze with default analyzers; enable demanglers for C++/Rust when relevant.

**Headless batch:**

```bash
analyzeHeadless /path/to/projects ProjName \
  -import /samples/sample.bin \
  -processor x86:LE:64:default \
  -analysisTimeoutPerFile 300 \
  -postScript ExportDecomp.java \
  -scriptPath /path/to/ghidra_scripts \
  -deleteProject   # only for ephemeral CI; keep projects for real work
```

**Minimal post-script goals:** rename functions by string xref; export decompiler for selected symbols; dump xrefs to `recv`/`send`/`connect`.

```text
# Pseudocode intent for Ghidra script
# for fn in getFunctionManager().getFunctions(True):
#   if has_interesting_strings(fn): rename(fn); book_mark(fn)
```

1. Pin Ghidra version in notes (P-Code/analyzer diffs across releases).
2. Use Data Type Manager: import headers or apply known OS types before inventing structs.
3. Document load base / relocation for firmware and position-independent samples.

### 4. IDA Pro interactive / batch

```bash
# Batch analyze (paths vary by install)
ida64 -A -S"/scripts/export_funcs.py" sample.bin
# or idat64 for text-mode
```

**IDAPython sketch:**

```python
import idautils, ida_funcs, ida_name, idc

for ea in idautils.Functions():
    name = ida_funcs.get_func_name(ea)
    # xrefs to address
    for xref in idautils.XrefsTo(ea):
        pass
```

1. Apply FLIRT only when signature source is trusted; wrong sigs poison names.
2. Create structs in Local Types; retype pointers at call sites; refresh decompiler.
3. Use Close/rebase carefully; record image base in the report.

### 5. Function recovery, types, and xrefs (both tools)

1. Seed from imports/syscalls: crypto (`BCrypt*`, `EVP_*`), net (`connect`, `WSASend`), file IO.
2. Follow **string → xref → function** for command handlers and license checks.
3. Build argument types from decompiler, then push types into callees (propagation).
4. For C++, recover vtables carefully; do not trust first-pass demangle alone.
5. Export findings: annotated function list, key structs, CFG screenshots only when needed.

### 6. Verify hypotheses with evidence

| Check | Evidence |
| --- | --- |
| “This is AES key schedule” | Constants (S-box), round structure, xrefs to buffer sizes 16/24/32 |
| “Handler for opcode X” | Switch/jump table + packet length checks + sample input |
| “Dead code” | No xrefs **and** not reached from TLS callbacks/exports/interrupt |

1. Prefer multi-sample confirmation or one controlled input change under dynamic RE.
2. Never claim crypto strength without algorithm identification notes.

### 7. Hand off

1. Deliver: hash, tool+version, DB path, renamed symbol map, open questions.
2. Scripts and type archives under version control without sample binaries if policy requires.
3. Route exploit development, unpacking, or traffic RE to specialized skills.

## Tooling Cheatsheet

| Task | Ghidra | IDA |
| --- | --- | --- |
| Search string | Search → For Strings / Script | Shift+F12 |
| Xrefs | Ctrl+Shift+F / API | `x` on address |
| Decompiler | Window → Decompile | F5 (Hex-Rays) |
| Types | Data Type Manager | Shift+F1 Local Types |
| Bookmarks | Bookmark manager | `Alt+M` |
| Diff (related builds) | Version tracking / BSim | BinDiff / Diaphora (external) |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Isolation | Detonates only in lab VM | Opens malware on analyst laptop with mail tokens |
| Naming | Evidence-based renames | Mass auto-rename from weak FLIRT |
| Types | Header/TIL + verified sizes | Random `int` everywhere |
| Headless | Reproducible script + version pin | Manual-only tribal knowledge |
| Claims | Tied to xrefs/samples | “Looks like backdoor” with no path |

## Output Checklist

- [ ] Authorization and isolation recorded; sample hash fixed
- [ ] Tool and version pinned; original sample immutable
- [ ] Analysis DB created; auto-analysis completed or justified skip
- [ ] Key functions named with xref/string evidence
- [ ] Critical structs/enums defined and applied
- [ ] Headless/script path documented if batch used
- [ ] Hypotheses verified or marked uncertain
- [ ] Hand-off notes + next skill routes listed
- [ ] No secrets/PII leaked in exports

## Rules

- Authorized samples and safe labs only.
- Evidence-driven RE: runtime/dynamic proof beats comments when they conflict.
- Do not execute unknown binaries outside isolation.
- Keep focus on Ghidra/IDA database workflows; broader binary-re trees own playbooks.
- Never commit customer malware samples or license keys into public repos.
