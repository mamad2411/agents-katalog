---
name: binary-diffing
description: |
  This skill activates when the user mentions "patch analysis", "binary diff", "binary diffing",
  "bindiff", "BinDiff", "Diaphora", "diaphora", "radiff2", "DarunGrim", "turbodiff",
  "version comparison", "what changed between versions", "compare binaries", "diff binaries",
  "function comparison", "code delta", "patch Tuesday", "Patch Tuesday diffing",
  "security patch analysis", "CVE diffing", "1-day exploit", "1day", "n-day",
  "vulnerability discovery through diffing", "binary comparison", "patch diffing",
  "firmware diff", "firmware comparison", "firmware update analysis",
  "malware variant comparison", "malware evolution", "malware diff",
  "function matching", "similarity scoring", "code similarity",
  "graph diff", "CFG comparison", "control flow diff",
  "before and after patch", "pre-patch post-patch", "patch gap",
  "Microsoft update diff", "KB diff", "hotfix analysis",
  "variant analysis", "binary delta", "code diff",
  "what did the patch fix", "find the vulnerability from the patch",
  "exploit from patch", "patch to exploit", "diffing workflow",
  or discusses comparing two versions of a binary to identify changes,
  security patches, vulnerability root causes, or behavioral evolution.
version: 2.0.0
---

# Binary Diffing

## Overview

Binary diffing compares two versions of a compiled binary to isolate exactly what changed. This is one of the highest-value reverse engineering techniques because it converts a vendor's patch into a roadmap pointing straight at the vulnerability. The same technique applies to tracking malware evolution, understanding firmware updates, and auditing software changes between releases.

**Why this matters**: When Microsoft ships a Patch Tuesday update, the patch itself tells you what was vulnerable. A well-executed diff workflow can identify the exploitable condition in hours, not days.

## Core Use Cases

| Use Case | Input | Output |
|----------|-------|--------|
| Patch analysis (1-day development) | Pre-patch + post-patch binary | Vulnerable function, root cause, exploitable condition |
| CVE reproduction | Advisory + patched binary pair | Proof of concept targeting the patched flaw |
| Malware variant tracking | Sample A + Sample B | Behavioral delta, new capabilities, C2 changes |
| Firmware update analysis | Firmware v1 + v2 (extracted) | Changed drivers, new mitigations, removed features |
| Software audit | Release N + Release N+1 | Security-relevant changes, regression candidates |

## Tool Routing

| Task | Tool | When to Use |
|------|------|-------------|
| Byte-level diff | `radiff2 <old> <new>` | Quick triage — see raw byte changes |
| Code block comparison | `radiff2 -C <old> <new>` | Identify changed basic blocks |
| Graph-based diffing | BinDiff (via Ghidra/IDA export) | Deep function matching with CFG comparison |
| Scriptable diffing | Diaphora (Ghidra/IDA plugin) | Customizable matching, SQL-backed results |
| Similarity scoring | `ssdeep -l <old> <new>` | Quick similarity percentage between files |
| Section comparison | `r2 -qc 'iS' <old>` vs `<new>` | Detect section size/permission changes |
| Import/export delta | `r2 -qc 'ii'` / `r2 -qc 'iE'` | New APIs, removed functions |
| String delta | `strings` or `floss` on both | New URLs, error messages, config values |
| Function listing | `r2 -qc 'aaa; afl'` on both | Function count, name, and size comparison |

## Methodology

### Phase 1 — Triage

Determine whether a meaningful diff is feasible and estimate scope.

1. **Hash both binaries** — confirm they are actually different (`sha256sum`, `md5sum`)
2. **Check fuzzy similarity** — `ssdeep -l old.dll new.dll` gives a percentage; above 90% means a targeted patch, below 50% suggests a major rewrite
3. **Compare file metadata** — timestamps, version info (`r2 -qc 'iV'`), digital signatures, file size delta
4. **Compare sections** — `r2 -qc 'iS'` on both; a changed `.text` section means code modifications, changed `.rdata` may indicate string/constant changes
5. **Compare imports/exports** — new imports reveal new functionality or mitigations (e.g., adding `__security_check_cookie` suggests stack cookie enforcement)

If ssdeep similarity is high (>85%) and only `.text` changed, this is a surgical patch — ideal for 1-day analysis.

### Phase 2 — Function-Level Diffing

This is where the real work happens. The goal is to identify which functions changed and how.

**Using radiff2 (fast, CLI-native)**:
```bash
# List all function differences with sizes
radiff2 -C old.dll new.dll

# Graph diff for a specific function pair
radiff2 -g old.dll new.dll > diff.dot
```

**Using BinDiff (gold standard for large binaries)**:
1. Export `.BinExport` files from Ghidra or IDA for both binaries
2. Run BinDiff on the export pair
3. Sort results by similarity score — functions at 0.9-0.99 are partially matched (the interesting ones)
4. Ignore 1.0 matches (identical) and 0.0 matches (unmatched/new)

**Using Diaphora (scriptable, SQL-backed)**:
1. Run Diaphora export on both binaries in Ghidra/IDA
2. Open the diff database — results are stored in SQLite
3. Focus on "partial matches" tab — these are modified functions
4. Use the pseudo-code diff view to see decompiled changes side-by-side

### Phase 3 — Root Cause Analysis

For each modified function, determine what the patch actually fixes.

1. **Decompile both versions** — compare pseudo-code side by side
2. **Identify the delta** — look for added bounds checks, new validation, changed buffer sizes, added error handling
3. **Classify the change**:
   - Added length/size check → buffer overflow fix
   - Added NULL check → null pointer dereference fix
   - Changed integer arithmetic → integer overflow fix
   - Added input validation → injection or type confusion fix
   - Changed memory allocator → use-after-free or double-free fix
   - Added authentication check → privilege escalation fix
4. **Map to vulnerability class** — CWE ID, attack vector, exploitability
5. **Assess exploitability** — can you reach the vulnerable code path? What are the constraints?

### Phase 4 — Reporting

Document findings in a structured format. See the report template below.

## Patch Change Classification

| Change Pattern | Likely Vulnerability | CWE | Exploitability |
|---------------|---------------------|-----|----------------|
| Added bounds check on buffer write | Stack/heap buffer overflow | CWE-120/122 | High — classic memory corruption |
| Added integer overflow check before alloc | Integer overflow → heap overflow | CWE-190 | High — controllable allocation size |
| Added NULL pointer check | NULL dereference (DoS or code exec) | CWE-476 | Medium — depends on mapping NULL page |
| Added reference counting / free guard | Use-after-free | CWE-416 | High — heap spray + type confusion |
| Changed `memcpy` size calculation | Buffer over-read or over-write | CWE-125/787 | High — information leak or RCE |
| Added type validation | Type confusion | CWE-843 | High — object layout mismatch |
| Added authentication/authorization check | Privilege escalation / auth bypass | CWE-862 | Critical — direct security boundary skip |
| Removed dangerous API call | Command/code injection | CWE-78/94 | Varies — depends on input control |
| Changed deserialization logic | Insecure deserialization | CWE-502 | High — RCE through crafted objects |
| Added ASLR/CFG/CET markers | Missing mitigation | N/A | Raises exploitation difficulty |

## Function Matching Strategies

When automated tools produce poor matches (common with heavily optimized or obfuscated binaries), use these manual strategies:

1. **String anchoring** — find unique strings in the patched function, locate the same string in the old binary
2. **Import cross-references** — if the patched function calls a distinctive API, find all callers of that API in the old binary
3. **Constant matching** — magic numbers, error codes, and hash constants survive compilation changes
4. **Call graph topology** — match based on the shape of who-calls-whom, not just function content
5. **Basic block count heuristic** — functions with similar block counts and edge counts are likely matches
6. **Symbol carryover** — if either binary has partial symbols (PDB, DWARF), use them to anchor matches

## Diff Report Template

```markdown
# Binary Diff Report: <component-name>

**Date**: YYYY-MM-DD
**Analyst**: <name>
**CVE/Advisory**: <CVE-YYYY-XXXXX or advisory reference>

## Binaries Compared

| Property | Old (Pre-patch) | New (Post-patch) |
|----------|----------------|-----------------|
| File | <filename> | <filename> |
| SHA256 | <hash> | <hash> |
| Version | <version> | <version> |
| Size | <bytes> | <bytes> |
| ssdeep similarity | <percentage> | — |

## Executive Summary

<1-2 sentences: what the patch fixes and its security impact>

## Changed Functions

| Function | Old Address | New Address | Similarity | Change Type |
|----------|-----------|-----------|------------|-------------|
| <name> | 0x... | 0x... | 0.XX | Modified |

## Detailed Analysis

### <function-name>

**What changed**: <description of the code delta>

**Vulnerability**: <what was exploitable before the patch>

**Root cause**: <CWE, attack vector, constraints>

**Exploitability assessment**: <can this be weaponized? what's needed?>

## New/Removed Functions

<list any functions that were added or removed entirely>

## Import/Export Changes

<new or removed API imports and their significance>

## Recommendations

<for defensive teams: detection signatures, IOC patterns>
<for offensive teams: exploitation feasibility, PoC direction>
```

## Quick Reference: radiff2 Flags

| Flag | Purpose | Example |
|------|---------|---------|
| (none) | Byte-level diff | `radiff2 old new` |
| `-c` | Count differences | `radiff2 -c old new` |
| `-C` | Code/function diff | `radiff2 -C old new` |
| `-g` | Graph diff (DOT output) | `radiff2 -g old new` |
| `-s` | Similarity metrics | `radiff2 -s old new` |
| `-u` | Unified diff format | `radiff2 -u old new` |
| `-d` | Generate delta patch | `radiff2 -d old new` |
| `-A` | Set architecture | `radiff2 -A arm old new` |
| `-a` | Algorithm selection | `radiff2 -a bytes old new` |

## References

- `references/patch-analysis.md` — Full Patch Tuesday workflow, binary acquisition, 1-day methodology
- `references/tool-workflows.md` — BinDiff, Diaphora, radiff2 detailed usage guides
- `references/function-matching.md` — Matching algorithms, scoring, manual correlation techniques
- `references/binary-type-strategies.md` — Diffing strategies for PE, ELF, firmware, .NET, kernel drivers
