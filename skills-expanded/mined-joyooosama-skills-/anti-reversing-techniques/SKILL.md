---
name: anti-reversing-techniques
description: Understand anti-reversing, obfuscation, and protection techniques encountered during software analysis. Use when analyzing protected binaries, bypassing anti-debugging for authorized analysis, or understanding software protection mechanisms.
---

# anti reversing techniques

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- Use hardware breakpoints instead of software
- Patch timing checks
- Use VM with controlled time
- Hook timing APIs to return consistent values
- Use bare-metal analysis environment
- Harden VM (remove guest tools, change MAC)
- Patch detection code
- Use specialized analysis VMs (FLARE-VM)

## Available sections

- Anti-Reversing Techniques
- Anti-Debugging Techniques
- Windows Anti-Debugging
- x64dbg: ScyllaHide plugin
- Patches common anti-debug checks
- Manual patching in debugger:
- - Set IsDebuggerPresent return to 0
- - Patch PEB.BeingDebugged to 0
- - Hook NtQueryInformationProcess
- IDAPython: Patch checks
- Linux Anti-Debugging
- LD_PRELOAD to hook ptrace

