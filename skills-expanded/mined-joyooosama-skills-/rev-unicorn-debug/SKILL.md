---
name: rev-unicorn-debug
description: Debug and emulate specific code fragments or functions using the Unicorn engine. Activate when the user wants to emulate a function with Unicorn, trace binary execution without running the full program, decrypt or decode data by emulating the algorithm, or bypass environment dependencies (JNI, syscalls, libc) during emulation.
---

# rev unicorn debug

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- Unmapped memory fetch 鈫?missing code page, map it
- Unmapped memory read/write 鈫?missing data section or uninitialized pointer, map or hook
- Hitting an import stub 鈫?identify the function, add a simulation hook
- Infinite loop 鈫?add a code hook with execution counter, stop after threshold

## Available sections

- rev-unicorn-debug - Unicorn Emulation Debugger
- Core Principles
- Environment Simulation Strategy
- Callback Types to Use
- Iterative Debugging Workflow
- Architecture Quick Reference

