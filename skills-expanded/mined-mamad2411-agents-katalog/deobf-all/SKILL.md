---
name: deobf-all
description: >-
  Master dispatcher for deobfuscation workflows. Loads the right combination of
  deobf and reverse-engineering skills based on target type — native binary,
  JavaScript, VM-protected, packed, or CTF. Use when you need comprehensive
  deobfuscation capabilities for any target.
---

# Deobf-All — Unified Deobfuscation Dispatcher

> When you encounter **any** obfuscated or protected code, this skill triages
> the target first, then loads **only the relevant sub-skills** — not all 9 at
> once. This minimises tool calls and context usage.

## 0. EXECUTION CONTRACT (read first)

```
DO NOT read_skill all 9 sub-skills blindly.
Instead: triage → load P0 → route → load P1/P2 only if needed.
```

| Phase | Action | Tool calls |
|-------|--------|------------|
| Triage | Inspect target file, identify type | 0–1 (read_file / file command) |
| Load P0 | `read_skill` for 1–2 core skills | 1–2 |
| Route | Decide if P1/P2 are needed | 0 |
| Load P1/P2 | `read_skill` only for skills the route demands | 0–3 |

**Goal**: never exceed 5 `read_skill` calls per invocation unless the target is truly unknown.

## 1. SUB-SKILL INVENTORY

| # | Skill | Purpose | Layer |
|---|-------|---------|-------|
| 1 | `code-obfuscation-deobfuscation` | Native binary deobf: CFF, opaque predicates, string encrypt, import hiding, anti-disasm | **P0** |
| 2 | `ast-deobfuscation` | JavaScript AST deobf: pattern detection, pipeline, site-specific adapters | **P0** (JS only) |
| 3 | `vm-and-bytecode-reverse` | VM protectors (VMProtect/Themida), custom VM dispatcher, opcode mapping | **P1** |
| 4 | `anti-debugging-techniques` | Anti-debug detection & bypass (ptrace, PEB, timing, TLS, VEH) | **P1** |
| 5 | `symbolic-execution-tools` | angr/Z3/Triton: automated constraint solving, emulation unpacking | **P1** |
| 6 | `binary-protection-bypass` | ASLR/NX/PIE/Canary/RELRO bypass | **P2** |
| 7 | `ctf-reverse` | CTF reverse engineering methodology | **P2** |
| 8 | `anti-reversing-techniques` | Anti-reversing identification & circumvention | **P2** |
| 9 | `deep-analysis` | Deep reverse engineering triage (comprehensive analysis) | **P2** |

## 2. TRIAGE — Do This First (before any read_skill)

Inspect the target and determine:

1. **Target type**: native binary (ELF/PE/Mach-O) / JavaScript / bytecode (DotNet/Java/Python) / other
2. **Obfuscation family** (if identifiable): CFF, VM protection, string encryption, packing, JS obfuscator (obfuscator.io, JSFuck, etc.)
3. **Presence of anti-debug / anti-reversing** layers
4. **Context**: CTF challenge? Production analysis? Quick cleanup?

**Output**: A triage line, e.g. `TRIAGE: native PE, VMProtect, has anti-debug → P0:code-obfuscation-deobfuscation P1:vm-and-bytecode-reverse,anti-debugging-techniques`

## 3. ROUTING MATRIX — Load Only What's Needed

Based on triage, `read_skill` **only** for the skills marked ✓:

| Target | P0 core-deobf | P0 ast-deobf | P1 vm-reverse | P1 anti-debug | P1 symbolic | P2 bin-bypass | P2 ctf-rev | P2 anti-rev | P2 deep |
|--------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Native binary, general | ✓ | | | | | | | | |
| Native + VM protection | ✓ | | ✓ | | | | | | |
| Native + VM + anti-debug | ✓ | | ✓ | ✓ | | | | | |
| Native + CFF (OLLVM) | ✓ | | | | ✓ | | | | |
| Native + packed + anti-rev | ✓ | | | | | ✓ | | ✓ | |
| JavaScript (any) | | ✓ | | | | | | | |
| JS + heavy obfuscation | ✓ | ✓ | | | | | | | |
| DotNet/Java/Python bytecode | ✓ | | ✓ | | ✓ | | | | |
| CTF reverse challenge | ✓ | | | | | | ✓ | | ✓ |
| Unknown / unclear | | | | | | | | | ✓ |

**Rule**: If a cell is empty, do NOT load that skill. This keeps tool calls minimal.

## 4. WORKFLOW

### Step 1: Triage (0–1 tool call)
Inspect the target. Use `read_file` for source code or `file`/`DIE`/`PEiD` output for binaries. Produce the triage line.

### Step 2: Load P0 (1–2 tool calls)
`read_skill` for the P0 skill(s) the route demands. For native binaries that's `code-obfuscation-deobfuscation`; for JavaScript that's `ast-deobfuscation`.

### Step 3: Load P1/P2 only if routed (0–3 tool calls)
Only `read_skill` for P1/P2 skills that the routing matrix marks ✓ for your target type.

### Step 4: Deobfuscate
- **Static first**: pattern matching, CFF reduction, string decryption, dispatcher inlining
- **Dynamic if blocked**: debugger scripting, emulation, symbolic execution
- For JS: run `scripts/detect-patterns.js` from ast-deobfuscation first, then apply the matching pipeline
- For native: identify protector (VMProtect/Themida/OLLVM/custom) before choosing strategy

### Step 5: Validate
- Compare deobfuscated output to original symptoms
- Verify functional equivalence
- Check for residual/nested obfuscation layers

## 5. FALLBACK — When Triage Is Uncertain

If you cannot determine the target type after inspection:

1. `read_skill` for `deep-analysis` (P2)
2. Follow deep-analysis methodology to classify the target
3. Return to the routing matrix with the classification result
4. Load the appropriate P0/P1 skills

This is the **only** scenario where you should load a P2 skill before P0.

## 6. QUICK REFERENCE CHECKLISTS

### Native Binary
1. [ ] Triage: identify protector/packer (file, DIE, PEiD)
2. [ ] Load P0: `code-obfuscation-deobfuscation`
3. [ ] Anti-debug? → Load `anti-debugging-techniques`
4. [ ] VM-protected? → Load `vm-and-bytecode-reverse`
5. [ ] Stuck on CFF? → Load `symbolic-execution-tools`
6. [ ] Packed/protected? → Load `binary-protection-bypass`
7. [ ] Anti-reversing? → Load `anti-reversing-techniques`
8. [ ] Deobfuscate → validate

### JavaScript
1. [ ] Triage: identify obfuscator (obfuscator.io, JSFuck, custom)
2. [ ] Load P0: `ast-deobfuscation`
3. [ ] Run `scripts/detect-patterns.js` to identify site/framework
4. [ ] Apply matching pipeline (CFF reduction, string decryption, dispatcher inline)
5. [ ] Heavy obfuscation? → also load `code-obfuscation-deobfuscation`
6. [ ] Re-parse after each stage → validate

### CTF
1. [ ] Load P2: `ctf-reverse` + `deep-analysis`
2. [ ] Identify challenge type (VM, packing, crypto, custom)
3. [ ] Load P0/P1 per routing matrix
4. [ ] Solve → validate flag
