---
name: eni-reverse-deep
description: 全局自动路由 | Deep reverse engineering for PE, ELF, Mach-O, firmware, drivers, APK/DEX, .NET, Go, Rust, Unity IL2CPP, Unreal, packed binaries, custom VMs, and undocumented protocols. Use when Codex receives a binary, disassembly, pseudocode, crash, native library, game artifact, firmware image, obfuscated application, or needs IDA/Ghidra/Frida/angr/Unicorn automation, algorithm recovery, unpacking, patching, or protocol reconstruction.
x-alice-class: reverse
---

# Cold Coffee Reverse Deep

Work from artifact to verified recovered behavior.

## Start

1. Hash and triage the artifact with `scripts/triage_binary.py`.
2. Preserve original files; place derived files in a separate work directory.
3. Identify format, architecture, compiler/runtime clues, protections, imports, strings, and likely entry paths.
4. Build an address/function/structure map while analyzing.

## Select references

- Native PE/ELF/Mach-O, drivers, firmware: read `references/native-workflow.md`.
- .NET, Java/Android, Go/Rust, Unity/Unreal: read `references/managed-game.md`.
- Packers, anti-debug, virtualization, control-flow obfuscation: read `references/unpacking-obfuscation.md`.
- Network messages or binary formats: read `references/protocol-reverse.md`.

## Execute

- Combine static decompilation with debugger traces, watchpoints, hooks, dumps, and controlled input changes.
- Recover calling conventions, structs, vtables, state machines, packet layouts, and data transformations.
- Prefer scripts for repeatable extraction: IDAPython, Ghidra, r2pipe, Frida, angr/Z3, Unicorn, parsers, scanners, and patchers.
- Test recovered algorithms against original samples.

## Deliver

Return the artifact hash, target profile, key addresses/functions, recovered data structures, confirmed behavior, scripts, debugger commands, and verification results. Distinguish confirmed observations from hypotheses.
