---
name: reverse-engineering-binaries-with-radare2-rizin
description: 'Reverse engineers binaries using radare2/rizin interactively, covering analysis
  initialization, navigation, disassembly and graph views, patching, and the visual mode workflow.
  Activates for requests to reverse a binary with radare2 or rizin, learn r2 commands, or navigate
  and disassemble a sample in r2.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - radare2
  - rizin
  - disassembly
  - static-analysis
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1059
  - T1587.001
d3fend:
  - D3-DA
  - D3-SDA
references:
  - 'The radare2 book — https://book.rada.re/'
  - 'Rizin documentation — https://rizin.re/'
---

# Reverse Engineering Binaries With radare2/rizin

## When to Use

- You want to statically reverse a binary with the radare2/rizin command set: analyze, navigate
  functions, read disassembly/graphs, and patch.
- You prefer a scriptable, terminal-based RE workflow.

**Do not use** r2's debug mode (`-d`) to run untrusted samples on your host — for static RE, open
without debugging. Work in an isolated environment.

## Prerequisites

- radare2 or rizin installed and the sample (read inertly).

## Safety & Handling

- Static analysis does not execute the sample; keep the working directory isolated.

## Workflow

### Step 1: Open and analyze

```bash
python scripts/analyst.py cheatsheet analyze
```

Prints the core sequence: open read-only (`r2 -e bin.cache=true sample`), `aaa` to analyze, `afl`
to list functions, `iI`/`ie` for info/entrypoint.

### Step 2: Navigate and disassemble

Use `s <addr>`/`s main` to seek, `pdf` to print a function, `VV` for the graph view, and `axt` for
cross-references.

### Step 3: Annotate

Rename with `afn`, add comments with `CC`, define data with `Cd`, and flag locations with `f`.

### Step 4: Patch (optional)

In write mode (`-w`), use `wa`/`wx` to assemble/patch and re-verify with `pdf`.

## Validation

- `aaa` completes and `afl` lists functions before deeper navigation.
- Commands used are real r2/rizin commands (verifiable in the book).
- Patches are re-disassembled to confirm the intended change.

## Pitfalls

- Forgetting `aaa`, leaving functions undefined.
- Confusing radare2 and rizin command differences in scripts.
- Opening with `-d` (debug/run) when only static analysis is intended.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the command cheatsheet tool.
- The radare2 book and Rizin docs (linked in frontmatter).
