---
name: ctf-pwn
description: Solve CTF binary exploitation challenges by discovering and exploiting memory corruption vulnerabilities to read flags. Use for buffer overflows, format strings, heap exploits, ROP challenges, or any pwn/exploitation task.
---

# ctf pwn

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- Input sources: stdin, network, files, environment, arguments
- Data destinations: stack buffers, heap allocations, global variables
- Transformations: parsing, copying, formatting, decoding
- Buffer boundaries: Fixed-size arrays, allocation sizes
- Type safety: Integer types, pointer validity, structure layouts
- Control flow integrity: Return addresses, function pointers, vtables
- Memory writes: Overwrite critical data (return addresses, function pointers, flags)
- Memory reads: Leak information (addresses, canaries, pointer values)

## Available sections

- CTF Binary Exploitation (Pwn)
- Purpose
- Conceptual Framework
- The Exploitation Mindset
- Core Question Sequence
- Core Methodologies
- Vulnerability Discovery
- Memory Layout Understanding
- Exploitation Planning
- Flexible Workflow
- Phase 1: Binary Reconnaissance (5-10 tool calls)
- Phase 2: Vulnerability Analysis (10-15 tool calls)

## Bundled resources

- patterns.md

Open these resources only if the current task needs deeper detail or executable helpers.
