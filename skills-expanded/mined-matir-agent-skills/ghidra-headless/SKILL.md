---
name: ghidra-headless
description: Reverse engineers binaries using Ghidra's headless analyzer. Use when decompiling executables, extracting functions, strings, symbols, or analyzing call graphs from compiled binaries without the Ghidra GUI.
allowed-tools:
- Bash
- Read
- Grep
- Glob
metadata:
  version: 0.2.0
  category: tooling
---
# Ghidra Headless

## Quick Start
```bash
ghidra-headless /path/to/project ProjectName -import /path/to/binary
```

## Workflow
1. Prepare Ghidra project directory.
2. Run headless analyzer with import or script flags.
3. Review analysis logs or output files.

## Rules & Constraints
- Ensure project path exists and is writable.
- Do not run concurrent headless instances on the same project.

## When to Use
- Automated binary analysis.
- Scripted decompilation of multiple binaries.

## When NOT to Use
- Interactive GUI debugging.
- Manual reverse engineering that requires visual context.

## References
- [Skill Manual](references/ghidra-headless-manual.md)
