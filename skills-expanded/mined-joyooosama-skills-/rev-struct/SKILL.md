---
name: rev-struct
description: Reconstruct data structures by analyzing memory access patterns across functions
---

# rev struct

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- func-name: sub_401000
- func-address: 0x401000
- callers: 0x402000, 0x403000    // List of functions that call this function
- callees: 0x404000, 0x405000    // List of functions called by this function
- Called as function pointer 鈫?function pointer
- Passed to `strlen`/`printf` 鈫?string pointer
- Compared with constants 鈫?enum/flags
- Increment/decrement operations 鈫?counter/index

## Available sections

- rev-struct - Structure Recovery
- Pre-check
- Export Directory Structure
- Function File Format (decompile/*.c)
- Structure Recovery Steps
- Step 1: Read Target Function
- Step 2: Collect Memory Access Patterns
- Step 3: Traverse Callers for Analysis
- Step 4: Traverse Callees for Analysis
- Step 5: Aggregate and Infer
- Output Format

