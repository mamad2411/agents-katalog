---
name: binary-ninja-hlil
description: >
  Binary Ninja High Level IL (HLIL) for owned/lab reverse engineering: reading HLIL,
  lifting levels (LLIL/MLIL/HLIL), renaming, type application, cross-references, and
  Python API snippets for automation. Use when analyzing functions in Binary Ninja —
  not for unauthorized cracking or bypassing commercial protections without authority.
---

# Binary Ninja HLIL

## Scope And Authorization

- **In scope:** Binaries in Binary Ninja under ownership, CTF/lab, or written authorization.
- **Out of scope:** Piracy, unauthorized DRM defeat, or distributing decompiled proprietary code unlawfully.
- Work on copies; record hashes; isolate untrusted samples.
- Pair broader RE flow with `binary-re`; r2/Ghidra static with `binary-re/static-analysis`.

## When To Use

- Understanding a function via HLIL pseudo-C rather than raw assembly.
- Navigating IL levels when HLIL is messy (drop to MLIL/LLIL).
- Applying types/structures to clean up HLIL.
- Scripting bulk renames or HLIL scans with the BN Python API.
- Comparing BN HLIL notes with r2 `pdg` / Ghidra output.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| End-to-end RE routing | `binary-re` |
| r2/Ghidra static without BN | `binary-re/static-analysis` |
| Tool bootstrap without BN | `binary-re/tool-setup` |
| Dynamic debugging | `binary-re/dynamic-analysis` |
| Implementation quality for scripts | `code-quality-standards` |

## Domain Focus

| IL level | Character |
| --- | --- |
| Lifted IL | Very close to architecture |
| LLIL | Low-level, explicit flags/memory |
| MLIL | Medium; folded ops, clearer SSA-ish form |
| HLIL | High-level control flow, closer to decompiled C |
| Tooling | Binary Ninja UI, `binaryninja` Python API, BN headless where licensed |

## Workflow

### 1. Confirm scope and success criteria

1. Sample hash, target functions, BN version/license, authorization.
2. Success: HLIL readable with renames/types; behavior hypothesis evidenced; notes exportable.
3. If BN unavailable, fall back to Ghidra/r2 static skills.

### 2. Inventory binary in BN

1. Open copy of sample; confirm arch/platform detected.
2. Run analysis until linear sweep + recursive descent complete.
3. Note entry points, imports, strings pane hits.

```text
# UI: Imports, Strings, Symbols
# Confirm analysis state finished before trusting HLIL completeness
```

### 3. Baseline function triage

1. Sort functions by size/callers; jump to `main`/exports/string xrefs.
2. For each candidate, view **HLIL**; if nonsense, try **MLIL** then disasm.
3. Record addresses (file offset / VA) for reproducibility.

### 4. Work the HLIL

**Reading practices:**

1. Rename variables (`uVar1` → `sock_fd`) as soon as role is clear.
2. Apply types: pointers, structs for protocol headers; re-render HLIL.
3. Collapse recovered library thunks; focus on app logic.
4. Follow HLIL calls; keep a call graph note for synthesis.
5. When optimizers obscure intent (flattened CFG), document blocks in MLIL.

**Python API sketch (authorized automation):**

```python
import binaryninja as bn

bv = bn.load("sample")
for f in bv.functions:
    if f.name == "main" or "encrypt" in f.name.lower():
        hlil = f.hlil
        if hlil:
            print(f.name, f.start, len(list(hlil.instructions)))
            # print(hlil.root)  # tree form depending on API version
bv.file.close()
```

1. Use headless/scripting only per your BN license terms.
2. Export annotations (names/types) with the BNDB; don’t only keep screenshots.
3. Cross-check crypto constants with known algorithms (AES S-box, etc.).

### 5. Verify with evidence

1. HLIL condition matches disassembly branch.
2. String xref in HLIL matches data var address.
3. Optional dynamic check in sandbox confirms IO HLIL suggests.
4. Second tool (Ghidra/r2) agrees on high-level behavior for critical claims.

### 6. Observe and harden (analysis hygiene)

1. Save BNDB frequently; version large renames.
2. Avoid pasting full proprietary decompilation into public tickets.
3. Redact discovered secrets; rotate if real credentials.

### 7. Hand off

1. Function summaries: address, HLIL-derived purpose, confidence.
2. Unresolved: needs dynamic, missing types, obfuscation.
3. Link `binary-re/synthesis` for final report structure.

## HLIL Quality Tips

| Problem | Action |
| --- | --- |
| `if (*(x+4))` noise | Apply struct type |
| Wrong call args | Fix prototype / calling conv |
| Mega-function | Split views; find natural SESE regions |
| Opaque predicates | Note; verify dynamically |
| Inlined junk | Focus on import boundaries |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Workflow | Rename+types iteratively | Read raw HLIL once, give up |
| Levels | Drop to MLIL when stuck | Trust broken HLIL blindly |
| Evidence | VA + screenshot/notes | “It decrypts stuff” |
| Tools | BN + second opinion on crypto | Single decompiler gospel |
| Scope | Authorized samples | Crack protected apps without rights |

## Output Checklist

- [ ] Sample hash and BN project/BNDB path recorded
- [ ] Target functions listed with addresses
- [ ] HLIL reviewed; renames/types applied
- [ ] MLIL/disasm used where HLIL insufficient
- [ ] Hypotheses evidenced
- [ ] Cross-check or dynamic follow-up planned
- [ ] Notes ready for synthesis
- [ ] Secrets redacted

## Rules

- Authorized/lab use only; respect licenses and law.
- Evidence-driven; verify decompiler output.
- Prefer isolated analysis environments for untrusted binaries.
- Do not turn RE notes into unauthorized exploit kits.
- Route non-BN workflows to `binary-re/*` skills.
